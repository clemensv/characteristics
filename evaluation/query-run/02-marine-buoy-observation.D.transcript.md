# Five derived metrics over the BuoyObservation stream

## 1. The five metrics

1. **Sea-level pressure rate of change, in hPa per hour, per station.** The
   signed difference between `pressure` in this record and in the previous
   record from the same station, divided by the *measured* elapsed seconds
   between them and scaled to an hour. `pressure` is declared
   `phenomenonTimeRelation: instant`, so two readings from one station are two
   points on one curve and their difference is a rate. An operator wants the
   fastest fall in the hour: a deepening low is the single most consequential
   thing this feed can show, and the record's own `pressure_tendency` only
   resolves it over three hours.

2. **Gust factor, `gust / wind_speed`, per record, and its hourly maximum and
   mean.** Dimensionless: both members are `m/s`. The schema states that `gust`
   is "the greatest short-interval wind speed observed within the same averaging
   window that produced `wind_speed`" — so the ratio is a ratio of two summaries
   of *one* set of samples, and it remains sound even though the length of that
   window is not declared. An operator wants gustiness because a high ratio
   distinguishes a squall or a convective downdraught from a steady blow at the
   same mean speed, and because a ratio drifting toward 1.0 or toward absurdity
   points at the anemometer rather than the weather.

3. **Wave-height change between two non-overlapping 20-minute supports, per
   station.** `wave_height` carries `supportPeriod {length: PT20M, anchor: end}`,
   and `timestamp` carries `cadence {fixed, PT5M}`, so consecutive records
   describe periods that overlap by fifteen minutes. This metric compares the
   current record against the record whose support *closes twenty minutes
   earlier* — i.e. `[t-40m, t-20m)` against `[t-20m, t)` — and emits nothing
   when the elapsed time is not actually about twenty minutes. An operator wants
   the build or decay rate of the sea state, and this is the only wave
   difference in the feed that is a difference between disjoint periods.

4. **Dewpoint spread, `air_temperature - dewpoint`, and its hourly minimum.**
   Both are `CEL` and both are `phenomenonTimeRelation: instant`, so the
   subtraction is between like quantities at one instant. Its value is that the
   record carries no humidity member: the schema states `dewpoint` is computed
   from air temperature and relative humidity by a deterministic formula, so at
   a fixed `air_temperature` the spread varies only with the humidity channel,
   and the spread is the only way to see that channel at all. An operator
   watching for a closing spread is watching the one input the feed hides.

5. **Reporting completeness and worst gap against the declared cadence, per
   station.** `timestamp` declares `cadence {kind: fixed, period: PT5M}`, so a
   one-hour window expects twelve records; the metric reports the observed count
   as a percentage of that, plus the longest observed interval between
   successive `timestamp` values. An operator wants a station that has gone
   quiet to be visible as a gap rather than as a flat line, and wants to know
   the denominator before reading metrics 1–4 for that hour. Per
   {{cadence}} in the specification this is a decision the consumer makes about
   its own processing; it is reported, never enforced, and a shortfall does not
   make any record invalid.

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
-- Event time is `timestamp` (semanticRole: phenomenonTime). The source is
-- `station_id` (semanticRole: featureOfInterest); everything partitions by it.
-- `timestamp` is bracket-quoted throughout in case it collides with a
-- reserved word in this dialect.

WITH Observation AS
(
    SELECT
        station_id,
        [timestamp]                          AS phenomenon_time,
        pressure,
        wind_speed,
        gust,
        wave_height,
        air_temperature,
        dewpoint,

        -- Immediately preceding record from this station. The timestamp is
        -- carried so that elapsed time is measured, not assumed from cadence.
        LAG([timestamp], 1)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_time,
        LAG(pressure, 1)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_pressure,

        -- Fourth record back. At the declared PT5M cadence that record closes
        -- the 20-minute wave support immediately preceding the current one.
        -- Its timestamp is carried so the 20-minute assumption is *verified*
        -- below rather than trusted.
        LAG([timestamp], 4)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prior_support_time,
        LAG(wave_height, 4)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prior_support_wave_height

    FROM input TIMESTAMP BY [timestamp]
),

PerRecord AS
(
    SELECT
        station_id,
        phenomenon_time,

        -- METRIC 5a: observed interval between successive phenomenon times.
        DATEDIFF(second, prev_time, phenomenon_time) AS gap_seconds,

        -- METRIC 1: signed pressure change normalised to hPa/hour by the
        -- measured elapsed time, so a missed beat lengthens the denominator
        -- instead of corrupting the rate. Intervals longer than one hour are
        -- discarded rather than extrapolated.
        CASE
            WHEN pressure IS NULL OR prev_pressure IS NULL THEN NULL
            WHEN DATEDIFF(second, prev_time, phenomenon_time) <= 0 THEN NULL
            WHEN DATEDIFF(second, prev_time, phenomenon_time) > 3600 THEN NULL
            ELSE (pressure - prev_pressure) * 3600.0
                 / DATEDIFF(second, prev_time, phenomenon_time)
        END AS pressure_rate_hpa_per_hour,

        -- METRIC 2: gust factor. Dimensionless; both members are m/s and the
        -- schema states they summarise the same averaging window.
        CASE
            WHEN gust IS NULL OR wind_speed IS NULL OR wind_speed <= 0 THEN NULL
            ELSE gust / wind_speed
        END AS gust_factor,

        -- METRIC 3: wave-height change across two NON-OVERLAPPING PT20M
        -- supports. Emitted only when the two anchoring positions really are
        -- about 20 minutes apart (1200 s, +/- 60 s), otherwise the two supports
        -- overlap or are disjoint by an unknown amount and the difference is
        -- not a 20-minute change.
        CASE
            WHEN wave_height IS NULL OR prior_support_wave_height IS NULL THEN NULL
            WHEN DATEDIFF(second, prior_support_time, phenomenon_time)
                 BETWEEN 1140 AND 1260
                 THEN wave_height - prior_support_wave_height
            ELSE NULL
        END AS wave_height_change_20min,

        -- METRIC 4: dewpoint spread, in degrees Celsius of DIFFERENCE.
        CASE
            WHEN air_temperature IS NULL OR dewpoint IS NULL THEN NULL
            ELSE air_temperature - dewpoint
        END AS dewpoint_spread
    FROM Observation
)

SELECT
    station_id,
    System.Timestamp() AS window_end,

    -- METRIC 1: most negative rate is the fastest fall; the absolute maximum
    -- catches a rapid rise behind a front as well.
    MIN(pressure_rate_hpa_per_hour)      AS min_pressure_rate_hpa_per_hour,
    MAX(ABS(pressure_rate_hpa_per_hour)) AS max_abs_pressure_rate_hpa_per_hour,

    -- METRIC 2
    MAX(gust_factor)                     AS max_gust_factor,
    AVG(gust_factor)                     AS avg_gust_factor,

    -- METRIC 3: order statistics only. See section 3 on why no mean is taken
    -- over the raw wave members.
    MAX(wave_height_change_20min)        AS max_wave_height_rise_20min,
    MIN(wave_height_change_20min)        AS max_wave_height_fall_20min,

    -- METRIC 4
    MIN(dewpoint_spread)                 AS min_dewpoint_spread,

    -- METRIC 5: 12 = one hour divided by the declared PT5M cadence. This is
    -- an expectation, not a guarantee; the value is reported, not asserted.
    COUNT(*)                             AS records_in_window,
    COUNT(*) * 100.0 / 12.0              AS reporting_completeness_pct,
    MAX(gap_seconds)                     AS max_gap_seconds

INTO output
FROM PerRecord
-- Window: TumblingWindow, 60 minutes, non-overlapping. Sixty is an integer
-- multiple of both the declared PT5M cadence and the PT20M wave support, so a
-- window holds a whole number of each.
GROUP BY station_id, TumblingWindow(minute, 60)
```

## 3. What I did not compute

* **Wave steepness, or any combination of `wave_height` with
  `dominant_wave_period` or `average_wave_period`.** Relating a height to a
  period requires the deep-water dispersion relation. Neither file states it,
  and the specification forbids repairing a missing fact from units,
  descriptions or property names.

* **Wind–wave misalignment, `wind_direction` minus `mean_wave_direction`.**
  `wind_direction` is explicitly "the direction the wind is coming from".
  `mean_wave_direction` states no from/toward convention at all. A convention
  mismatch is a 180-degree error and every value would still validate. Their
  supports differ as well: `mean_wave_direction` has `supportPeriod` PT20M and
  `wind_direction` has none.

* **Any window mean of `wind_direction` or `mean_wave_direction`.** Degrees
  wrap at 360 and an arithmetic mean of angles is wrong near north. Beyond
  that, `wind_direction` is already `derivation: statistic, statistic: mean`
  and `mean_wave_direction` is `derivation: calculated` from spectral
  directional moments; the specification states that `statistic` does not
  authorise recomputation and that a processor must not read an instruction out
  of these keywords. A vector mean would require the energy weighting the
  record does not carry.

* **A residual of `pressure_tendency` against a three-hour difference of
  `pressure`.** `pressure_tendency` declares `supportPeriod {PT3H, end}`, so
  the reference exists and the residual is exactly the shape the task calls
  valuable. Reconstructing the comparison term requires locating the record
  three hours back, which means either a fixed `LAG` offset of 36 or a trust in
  `cadence`. The specification is explicit that cadence is an expectation and
  not a constraint, that it does not assert a record exists for any position,
  and that a processor must not act as though it does. A fixed offset would
  silently compare the wrong interval on any hour that dropped a beat, and the
  error would be invisible in the output. Metric 1 measures its elapsed time
  instead of assuming it, which is why it is a short-interval rate rather than
  this residual.

* **Any mean, sum or standard deviation of `wave_height`,
  `dominant_wave_period`, `average_wave_period` or `mean_wave_direction` over a
  window.** Their `supportPeriod` is PT20M anchored at `end` and the cadence is
  PT5M, so consecutive records overlap by fifteen minutes. A windowed mean
  would weight the middle of the window roughly four times over, and a sum
  would count the same water four times. Only order statistics over published
  values and the disjoint-support comparison of metric 3 survive that overlap.

* **Cross-station aggregation of `wind_speed`, `gust` or `wind_direction`, and
  any treatment of them as a fixed-length average.** The schema declares no
  `supportPeriod` for these three and says so deliberately: the averaging
  length follows the station type, which the record does not carry. Per the
  specification the extent is then indeterminate and a nominal length must not
  be substituted. So an eight-minute mean from a buoy and a two-minute mean
  from a C-MAN station may not be pooled. The gust factor of metric 2 survives
  only because the ratio is taken within one record, where the schema states
  both members share one window.

* **Anything derived from `tide` or `visibility`.** Neither is in `required`
  and neither appears in the instance. `tide` is stated relative to Mean Lower
  Low Water, a station-specific datum, and no vertical
  `coordinateReferenceSystem` binds it — the schema's only CRS annotation binds
  `latitude` and `longitude` to EPSG:4326. Differencing tide across stations is
  therefore unsound, and the specification is clear that a datum stated in
  prose is not a binding a processor may act on. `visibility` is stated to be
  generally available only on C-MAN stations, which the record cannot identify.

* **Publication latency or feed freshness against arrival.** The schema
  declares `phenomenonTime` and nothing else temporal: there is no `resultTime`
  and no `ingestionTime`, and the specification forbids reading an operational
  time out of a phenomenon time. Metric 5 measures the interval between
  successive phenomenon times, which is a different quantity and is not a
  delivery-delay metric.

* **Anything from `latitude` and `longitude`** — drift of a moored buoy,
  station separation, spatial clustering. The CRS binding is present and
  unambiguous (EPSG:4326, `["latitude","longitude"]`, authoritative axis
  order), but neither file establishes whether the position is fixed per
  station or updated per record, and the specification explicitly declines to
  define coordinate operations or transformations, so a distance computation
  would rest on an ellipsoid model neither file supplies.

* **Air–sea temperature difference, `water_temperature - air_temperature`.**
  This one is sound — same unit `CEL`, both `derivation: measured`, both
  `phenomenonTimeRelation: instant`, same station and same phenomenon time —
  and I ranked it sixth and dropped it to keep to five. I note it here rather
  than in section 1 because the two files establish nothing about what the
  difference *means*, so its operator value is confined to cross-checking two
  independent sensors.

* **Any threshold flag, quality gate or "good data" indicator.** The schema
  carries no member with `semanticRole: resultQuality` and none with
  `semanticRole: status`, and it declares no `enum`, minimum or maximum on any
  numeric member. The specification states that omission never implies
  acceptable quality. I therefore raise no flag anywhere, including the
  otherwise obvious one on a negative dewpoint spread: that dewpoint cannot
  exceed air temperature is a fact about the atmosphere, not a fact these two
  files state.

## 4. Assumptions

* **Assumption.** `timestamp` is the correct event time for windowing. The
  schema gives it `semanticRole: phenomenonTime` and the record carries no
  other temporal member, so this follows; what does not follow, and is assumed,
  is that phenomenon time is an acceptable proxy for arrival ordering. Late and
  duplicate arrivals are left to the job's late-arrival and out-of-order
  policy, which is configuration and not part of this query.

* **Assumption.** `station_id` identifies one physical platform, that
  identifiers are not reused across platforms, and that one station emits at
  most one record per five-minute slot. The schema says the identifier is
  assigned by NDBC and identifies the observing platform; uniqueness over time
  and non-duplication in the stream are not stated.

* **Assumption (dialect).** `LAG` accepts an offset argument greater than 1 in
  this dialect. If it does not, metric 3 must be rewritten — the offset of 4 is
  load-bearing there. I could not verify this, as instructed.

* **Assumption (dialect).** `timestamp` needs bracket-quoting to avoid a
  reserved-word collision, and `ABS` is available. Neither is established by
  the files.

* **Assumption.** The ±60-second tolerance on metric 3's twenty-minute
  comparison is my choice. The files establish the PT20M support and the PT5M
  cadence but no tolerance for jitter; `timestamp` is stated to be constructed
  from minute-resolution columns, which is what makes a one-minute band
  plausible rather than principled.

* **Assumption.** The one-hour discard threshold in metric 1, and the
  suppression of the metric across gaps longer than that, are my choices. The
  files state no interval beyond which two `pressure` readings stop being
  usefully comparable.

* **Assumption.** The denominator 12 in `reporting_completeness_pct` treats the
  declared `cadence` of PT5M as the expected delivery rate for a full hour. The
  specification states this is an expectation and not a constraint; the query
  reports the ratio and draws no conclusion from it.

* **Assumption.** `dewpoint_spread` and the wave-height change are differences,
  not values on the underlying scale. A difference of two `CEL` values is a
  temperature interval and a difference of two `m` wave heights is a length
  change; the output column names say so but no unit annotation travels with
  them, and a downstream consumer that treats
  `min_dewpoint_spread` as a temperature will be wrong.

* **Assumption.** Successive `pressure` values from one station are comparable
  to each other. The schema states the value is reduced to sea level by the
  standard atmosphere from the station elevation, and I assume that elevation
  is constant for a given station over the window, so the reduction is a fixed
  transform and cancels in the difference. Nothing in the two files states that
  station elevation is fixed.

* **Assumption.** Every member other than `station_id`, `latitude`,
  `longitude` and `timestamp` may be absent from any record, since `required`
  lists only those four. Every metric is guarded for NULL on that basis, and
  each aggregate is therefore computed over an unstated and varying number of
  contributing records. The output does not report those per-metric counts.
