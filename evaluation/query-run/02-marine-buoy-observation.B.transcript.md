# BuoyObservation — five derived metrics

## 1. The five metrics

1. **Gust factor** — `gust / wind_speed`, emitted both for the newest record in the window and as the window maximum. The schema states that `gust` is the peak short-interval speed *within the same averaging window that produced* `wind_speed`, so the ratio is a like-for-like comparison and is dimensionless: it is the one wind metric that stays valid even though the schema refuses to fix the length of that averaging window (8 min for buoys, 2 min for land stations, and the record does not say which). An operator wants it because it separates a steady blow from a gusty, squally one at the same mean speed, which is the difference that matters to anything floating or lifting.

2. **Pressure rate of change, hPa per hour** — the signed change in `pressure` between the first and last record of the window, divided by the *actual* elapsed seconds between those two records. `pressure_tendency` is carried and describes the preceding 3 hours; this is computed and refreshes every 5 minutes, so an operator sees a pressure fall developing without waiting for the three-hour figure to catch up.

3. **Cadence completeness** — `COUNT(*)` over the window against the count the declared `cadence` (`fixed`, `PT5M`) implies. This is a residual against a reference the schema itself declares. An operator wants it because a station that has stopped reporting, or is reporting off-slot, is invisible in every other metric here — they simply go quiet — and because it tells you whether to trust metrics 2 and 4, both of which depend on the window being fully populated.

4. **Pressure-tendency residual** — the observed 3-hour change in `pressure` reconstructed from the stream, minus the declared `pressure_tendency` for the same interval. The schema defines `pressure_tendency` as the signed change in sea-level pressure over the preceding 3 hours, and the stream carries `pressure`; therefore the stream can reproduce that quantity, and a non-trivial disagreement is a defect in the barometer, in the reduction to sea level, or in the producer's encoding. An operator wants it as a self-contained quality check that needs no external reference.

5. **Wave period spread** — `dominant_wave_period - average_wave_period`, and its maximum over the window. Both are seconds, both share the same `supportPeriod` of `PT20M` anchored at the end, so the subtraction is between two summaries of the same 20 minutes. The schema says `dominant_wave_period` is the period of the band carrying maximum energy while `average_wave_period` is the mean of all wave periods; a large positive spread therefore means the energy peak sits well away from the bulk of the field, i.e. a long-period component coexisting with a shorter-period one. An operator wants it because a single significant wave height hides that structure entirely.

## 2. The query

```sql
-- Event time is the member the schema marks semanticRole=phenomenonTime.
-- Source identity is station_id, the member the schema marks
-- semanticRole=featureOfInterest; everything is partitioned by it.
WITH observations AS (
    SELECT
        station_id,
        [timestamp] AS observed_at,
        pressure,
        pressure_tendency,
        -- guard: the ratio is undefined at zero wind
        CASE WHEN wind_speed > 0 THEN gust / wind_speed END AS gust_factor,
        -- NULL if either period member is absent, which is the wanted behaviour
        dominant_wave_period - average_wave_period AS wave_period_spread
    FROM input
    TIMESTAMP BY [timestamp]
),

-- Window type: HoppingWindow. Size 185 minutes, hop 5 minutes, per station.
-- The size is 185 and not 180 deliberately: at the declared PT5M cadence a
-- full window holds 37 records whose first and last are exactly 36 x 300 s
-- = 3 hours apart, which is the interval pressure_tendency declares. A
-- 180-minute window would span only 175 minutes of observations and the
-- residual in metric 4 would compare mismatched intervals. The 5-minute hop
-- makes the output refresh at the cadence of the feed.
station_window AS (
    SELECT
        station_id,
        System.Timestamp() AS window_end,
        COUNT(*) AS record_count,
        MAX(gust_factor) AS gust_factor_max,
        MAX(wave_period_spread) AS wave_period_spread_max,
        -- TopOne() OVER (ORDER BY ...) returns the whole record; I am
        -- reasonably but not fully confident of this exact form and of the
        -- dotted field access on its result in every version of this dialect.
        -- It is used instead of LAG(pressure, 36) so that the endpoints are
        -- found by time rather than by counting records, which would break
        -- silently whenever the station drops a slot.
        TopOne() OVER (ORDER BY observed_at DESC) AS newest,
        TopOne() OVER (ORDER BY observed_at ASC) AS oldest
    FROM observations
    GROUP BY station_id, HoppingWindow(minute, 185, 5)
),

spans AS (
    SELECT
        station_id,
        window_end,
        record_count,
        gust_factor_max,
        wave_period_spread_max,
        newest.gust_factor AS gust_factor_latest,
        newest.pressure AS pressure_newest,
        oldest.pressure AS pressure_oldest,
        newest.pressure_tendency AS pressure_tendency_declared,
        DATEDIFF(second, oldest.observed_at, newest.observed_at) AS span_seconds
    FROM station_window
)

SELECT
    station_id,
    window_end,
    record_count,

    -- 1. Gust factor: newest record, and the worst seen in the window.
    gust_factor_latest,
    gust_factor_max,

    -- 2. Pressure rate of change, hPa/hour, over the actual observed span.
    --    Suppressed below an hour of span: too short to be a trend.
    CASE
        WHEN span_seconds >= 3600
        THEN (pressure_newest - pressure_oldest) * 3600.0 / span_seconds
    END AS pressure_rate_hpa_per_hour,

    -- 3. Cadence completeness against the declared PT5M cadence.
    --    37 = 185 minutes / 5 minutes. Below 1.0 means dropped slots;
    --    above 1.0 means duplicate or off-slot records, equally informative.
    CAST(record_count AS float) / 37.0 AS cadence_completeness,

    -- 4. Residual of the reconstructed 3-hour pressure change against the
    --    declared pressure_tendency. Only evaluated when the window endpoints
    --    really are 3 hours apart (+/- 5 minutes), so a gapped window
    --    produces NULL rather than a false alarm.
    CASE
        WHEN ABS(span_seconds - 10800) <= 300
             AND pressure_tendency_declared IS NOT NULL
        THEN (pressure_newest - pressure_oldest) - pressure_tendency_declared
    END AS pressure_tendency_residual_hpa,

    -- 5. Wave period spread, worst in the window.
    wave_period_spread_max

INTO output
FROM spans
```

## 3. What I did not compute

* **Wind-versus-wave misalignment**, `wind_direction` against `mean_wave_direction`. The schema states the convention for `wind_direction` explicitly — "the direction the wind is coming from" — and pointedly states no convention for `mean_wave_direction`. The difference is therefore ambiguous by 180 degrees, and a misalignment metric that may be inverted is worse than none. Separately, the two members do not describe the same interval: `mean_wave_direction` carries `supportPeriod` `PT20M`, while `wind_direction` carries none at all because its averaging period depends on station type that the record does not transmit.
* **Any mean or standard deviation of a direction member** — `wind_direction`, `mean_wave_direction`. These are circular quantities; arithmetic `AVG` over them is wrong across the 0/360 discontinuity, and the dialect offers no circular-mean aggregate. `MAX(gust_factor)` is safe in a way `AVG(wind_direction)` is not.
* **Wave steepness**, e.g. `wave_height / (dominant_wave_period * dominant_wave_period)`. Turning a height and a period into a steepness requires the deep-water dispersion relation. The two files supply no such relation, no water depth, and no constant; the ratio would be a number with no defined meaning.
* **Windowed mean of `wave_height`, `average_wave_period` or `dominant_wave_period`.** Records arrive every 5 minutes but each of these carries a `supportPeriod` of `PT20M` anchored at the end, so four consecutive records describe overlapping 20-minute intervals. A mean over them is a mean of non-independent, overlapping samples. `wave_height` compounds this: it is already the mean of the highest third of the waves, so averaging it again produces a statistic of a statistic whose meaning the schema does not define. I accepted the same overlap objection for `MAX(wave_period_spread)` in metric 5 because a maximum over overlapping supports still answers "did the spread reach this value", whereas a mean answers nothing definite.
* **Windowed aggregate of `pressure_tendency` itself.** It already summarises a `PT3H` interval; averaging values whose supports overlap by 2 hours 55 minutes is not interpretable. Its value in the query is as a reference to subtract against, not as something to aggregate.
* **`water_temperature - air_temperature`, and `air_temperature - dewpoint`.** Both subtractions are clean — same unit `CEL`, same `phenomenonTimeRelation` of `instant`, same platform — and I nearly used one of them. I left both out because everything that would make them *actionable* to an operator (sea fog, boundary-layer stability, approach to saturation) is meteorology the two files do not state. A bare signed temperature difference is not worth one of five places.
* **Anything derived from `visibility` or `tide`.** Both are absent from the only instance and neither is in `required`. The schema says `visibility` is "generally only available on C-MAN stations" with a range capped at 1.6 nmi, and `tide` is a coastal and C-MAN measurement; the record carries nothing that says which kind of platform it came from, so a metric over either would be null for most sources and could not distinguish "sensor not fitted" from "sensor failed". A tidal rate of change would additionally require separating astronomical tide from surge, which needs a harmonic prediction not present here.
* **Platform drift from `latitude` and `longitude`.** Nothing in the schema says whether the platform is moored or free-drifting, so there is no basis for deciding that a change in position is an anomaly rather than the normal behaviour of the source.
* **Any cross-station aggregation**, e.g. a regional mean `pressure`. `station_id` is the declared `featureOfInterest`; the files define no grouping of stations, and `latitude`/`longitude` under EPSG:4326 do not by themselves license a spatial bucket without a declared tessellation.
* **A named alert threshold on the gust factor or the pressure rate.** Both metrics are emitted as numbers rather than as boolean flags because the files supply no threshold for either, and any constant I chose would be imported from outside them.

## 4. Assumptions

* **Assumption:** the input stream is named `input` and the sink `output`.
* **Assumption:** absent measurements arrive as SQL `NULL`. The files state that only `station_id`, `latitude`, `longitude` and `timestamp` are required, and the instance omits `visibility` and `tide` entirely, but they do not say how an absent value is represented on the wire. If the producer instead passes through a numeric fill value for a missing reading, every metric above is corrupted and no guard in this query would catch it.
* **Assumption:** the declared `cadence` of `PT5M` is the intended publication rate for *every* station, so a shortfall in `record_count` is a gap rather than a legitimate slower rate. The schema says the producer "is expected to publish one record per station per five-minute slot", which is the basis for this, but it is an expectation and not a constraint.
* **Assumption:** records land on aligned 5-minute slots. This is what makes a 185-minute window span exactly 3 hours of observations and therefore what makes metric 4 an interval-matched comparison. The `+/- 300 s` guard limits the damage if it is false, at the cost of suppressing the residual instead.
* **Assumption:** `station_id` is stable over time and not reassigned between platforms; the schema calls it an identifier assigned by NDBC but says nothing about reuse.
* **Assumption:** `timestamp` is an acceptable event time for the whole record. The schema marks it `phenomenonTime`, but the record's members do not all describe that instant: the wave members summarise the preceding `PT20M`, `pressure_tendency` the preceding `PT3H`, and the wind members an interval of undeclared length. Aligning all of them on their common end anchor is the only choice the schema supports, but it means the window boundaries cut through the support periods of most members.
* **Assumption:** a `wind_speed` of exactly zero is a genuine calm rather than a placeholder; the query emits `NULL` for the gust factor in that case rather than treating it as an infinite ratio.
* **Assumption:** the sign convention for `pressure_tendency` is applied consistently by the producer — the schema states negative means falling — since the residual in metric 4 is a signed subtraction and a producer that inverted the sign would show as a residual of twice the tendency rather than as an obvious error.
* **Assumption about the dialect, not the data:** `TopOne() OVER (ORDER BY ...)` as a windowed aggregate, and dotted field access on the record it returns, are supported. The alternative, `LAG(pressure, 36) OVER (PARTITION BY station_id LIMIT DURATION(hour, 3))`, is syntax I am more confident of but is semantically worse, because a fixed record offset silently means something other than "3 hours ago" the moment a station drops a slot.
* **Design note, not an assumption:** metrics 2 and 4 share the same two pressure endpoints. They are kept separate because one is the magnitude and sign of a trend and the other is a consistency check on a carried member; a reader should treat metric 4 as meaningful only when metric 3 shows the window was fully populated.
