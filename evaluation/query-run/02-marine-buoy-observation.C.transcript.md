# BuoyObservation — five derived metrics

## 1. The five metrics

1. **Gust factor** — `gust / wind_speed` per report, then the window maximum and mean. It is a ratio of two members the schema types identically, so it is dimensionless and survives the fact that no unit is declared anywhere in the schema; an operator watching for squalls wants the peak-to-sustained ratio, and neither member alone shows it.
2. **Pressure rate of change per hour** — signed change in `pressure` between successive reports from the same `station_id`, normalised to an hour by the actual gap between reports. Even without knowing the unit of `pressure`, the sign and the magnitude relative to the same station's own history are the earliest warning this record set contains.
3. **Wave-height rate of change per hour** — the same successive-difference treatment of `wave_height`. `wave_height` itself is carried; whether the sea is building or decaying, and how fast, is not, and that is the part an operator acts on.
4. **Wind/wave misalignment** — the circular difference between `wind_direction` and `mean_wave_direction`, folded into 0–180°. This is the only cross-member relation the record licenses between the wind block and the wave block: it separates a wave field lying with the local wind from one running across it, which no single member reveals.
5. **Measurement completeness** — fraction of the 14 optional measurement members actually present, averaged over the window per station. The schema requires only `station_id`, `latitude`, `longitude` and `timestamp`; the one example record already omits `visibility` and `tide`, so partial reports are normal and silent channel loss is otherwise invisible.

The query also emits `reports` and `max_report_gap_seconds`. Those are diagnostics that make metrics 2 and 3 interpretable (a rate is meaningless without knowing the interval it was measured over) and are **not** claimed as part of the five.

## 2. The query

```sql
-- Azure Stream Analytics / Fabric Eventstream SQL. Single statement.
-- Event time member: timestamp. Source identity: station_id.
WITH
Observed AS (
    SELECT
        station_id,
        System.Timestamp()                  AS obs_time,   -- outside a window, this is the event time
        pressure,
        wave_height,
        wind_speed,
        gust,
        wind_direction,
        mean_wave_direction,
        -- previous report from the SAME station; LIMIT DURATION is mandatory on LAG
        LAG(pressure, 1)           OVER (PARTITION BY station_id LIMIT DURATION(hour, 3)) AS prev_pressure,
        LAG(wave_height, 1)        OVER (PARTITION BY station_id LIMIT DURATION(hour, 3)) AS prev_wave_height,
        -- I am not certain LAG accepts System.Timestamp() as its expression; if it does not,
        -- substitute LAG(CAST([timestamp] AS datetime), 1) OVER (...)
        LAG(System.Timestamp(), 1) OVER (PARTITION BY station_id LIMIT DURATION(hour, 3)) AS prev_obs_time,
        -- every member except station_id / latitude / longitude / timestamp is optional
        (CASE WHEN wind_direction       IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN wind_speed           IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN gust                 IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN wave_height          IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN dominant_wave_period IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN average_wave_period  IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN mean_wave_direction  IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN pressure             IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN air_temperature      IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN water_temperature    IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN dewpoint             IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN pressure_tendency    IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN visibility           IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN tide                 IS NULL THEN 0 ELSE 1 END)   AS members_present
    FROM input TIMESTAMP BY [timestamp]
),
PerReport AS (
    SELECT
        station_id,
        obs_time,
        members_present,
        DATEDIFF(second, prev_obs_time, obs_time) AS gap_seconds,

        -- (1) gust factor: dimensionless, guarded against a calm report
        CASE WHEN wind_speed > 0
             THEN gust / wind_speed
             ELSE NULL END AS gust_factor,

        -- (2) pressure change, normalised to declared-units-per-hour
        CASE WHEN DATEDIFF(second, prev_obs_time, obs_time) > 0
             THEN (pressure - prev_pressure) * 3600.0
                  / DATEDIFF(second, prev_obs_time, obs_time)
             ELSE NULL END AS pressure_rate_per_hour,

        -- (3) wave height change, normalised to declared-units-per-hour
        CASE WHEN DATEDIFF(second, prev_obs_time, obs_time) > 0
             THEN (wave_height - prev_wave_height) * 3600.0
                  / DATEDIFF(second, prev_obs_time, obs_time)
             ELSE NULL END AS wave_height_rate_per_hour,

        -- (4) circular difference folded into [0, 180]
        CASE WHEN ABS(wind_direction - mean_wave_direction) > 180
             THEN 360.0 - ABS(wind_direction - mean_wave_direction)
             ELSE ABS(wind_direction - mean_wave_direction) END AS wind_wave_misalignment_deg
    FROM Observed
)
SELECT
    station_id,
    System.Timestamp()                          AS window_end,   -- end of the tumbling window
    COUNT(*)                                    AS reports,      -- diagnostic
    MAX(gust_factor)                            AS gust_factor_max,              -- (1)
    AVG(gust_factor)                            AS gust_factor_avg,              -- (1)
    AVG(pressure_rate_per_hour)                 AS pressure_rate_per_hour,       -- (2)
    AVG(wave_height_rate_per_hour)              AS wave_height_rate_per_hour,    -- (3)
    AVG(wind_wave_misalignment_deg)             AS wind_wave_misalignment_deg,   -- (4)
    SUM(members_present) * 1.0 / (COUNT(*) * 14.0) AS measurement_completeness,  -- (5)
    MAX(gap_seconds)                            AS max_report_gap_seconds        -- diagnostic
INTO output
FROM PerReport
GROUP BY
    station_id,
    TumblingWindow(minute, 60)   -- tumbling, 60 minutes, one row per station per hour
```

Window summary: one **TumblingWindow of 60 minutes**, partitioned by `station_id`; the successive-difference metrics use `LAG` over a **3-hour LIMIT DURATION** partitioned by `station_id`.

## 3. What I did not compute

* **A residual of `pressure` change against `pressure_tendency`.** This is the one declared reference in the record and the obvious candidate, and I left it out. `pressure_tendency` has no declared averaging period, no declared unit, and no declared sign convention. Without the period I cannot difference it against an observed change over a known interval. The only unit-free version is a sign-agreement flag, and that is unsound too: pressure genuinely reverses direction, so at every turning point the observed short-interval change and a tendency computed over a longer period would legitimately disagree, and the flag would fire on correct data. A check that alarms on normal behaviour is worse than no check.
* **Wave steepness from `wave_height` and `dominant_wave_period`.** Relating a period to a wavelength requires the deep-water dispersion relation and consistent units for both members. The files establish neither. That is imported physics, not something these two files license.
* **The ratio `dominant_wave_period / average_wave_period`.** Arithmetically it is safe — both are periods and the ratio is dimensionless. I dropped it because the files do not say what distinguishes "dominant" from "average", so I could not state what the ratio means or which direction of departure from 1 is the one an operator should care about. A number I cannot interpret is not a metric.
* **Dewpoint depression, `air_temperature - dewpoint`.** The subtraction is sound if both share a scale, but its entire value rests on the relationship between dewpoint and saturation, which the files never state. I would be asserting meteorology the schema does not carry.
* **Air–sea temperature difference, `air_temperature - water_temperature`.** Ranked sixth. Sound under the same-scale assumption and I would add it if I had a sixth slot, but I judged the two rate metrics and the completeness metric more directly actionable, and the brief was five.
* **Arithmetic mean or `STDEV` of `wind_direction` or `mean_wave_direction` themselves.** These are circular quantities; the arithmetic mean of 350 and 10 is 180, which is the opposite of the right answer. Only the folded difference between them is averaged, and that is a magnitude in [0, 180], for which the arithmetic mean is valid.
* **`STDEV(wave_height)` within the window.** Sound, but largely redundant with metric 3, and with an undeclared reporting cadence the spread would mix genuine sea-state change with sampling density.
* **Anything using `latitude` and `longitude`** — drift from a home position, distance between stations, regional averages. There is no declared reference position to form a residual against, great-circle distance needs an earth model the files do not provide, and a single example record does not establish that more than one station exists or that a station's position is meant to be fixed.
* **Anything using `tide` or `visibility`.** `tide` is a level relative to a datum, and no datum is declared, so no residual or threshold is possible. Both are absent from the only example record. They are counted in the completeness metric and otherwise untouched.
* **Threshold flags in absolute units** — sea-state or wind-force classification, storm-pressure alarms. Every such threshold needs a unit, and no unit is declared for any member.

## 4. Assumptions

Each of the following is an **assumption**; none is established by the schema or the instance.

1. **Assumption:** `timestamp` is the observation time and is the correct event time. It is the only `datetime` member, which is why it is the one named in `TIMESTAMP BY`. I also assume its lexical form (`"2026-07-30T11:50:00Z"` in the instance) is parsed as an instant by the runtime.
2. **Assumption:** `station_id` identifies one physical source and is stable over time, making it a valid `PARTITION BY` key and a valid `LAG` partition.
3. **Assumption:** `gust` and `wind_speed` are expressed in the same unit, so their ratio is dimensionless. No unit is declared for either.
4. **Assumption:** `wind_direction` and `mean_wave_direction` are in degrees on [0, 360) and use the *same* reference convention — both "from" or both "toward". The schema declares them only as `double`. If the conventions differ, metric 4 is offset by 180° and the folded value is wrong.
5. **Assumption:** the rate metrics are in "declared-unit per hour". Since no unit is declared for `pressure` or `wave_height`, their magnitudes are comparable only to other reports from this same feed, not to any external scale.
6. **Assumption:** reports arrive more often than once per hour, so a 60-minute tumbling window contains several of them, and more often than once per 3 hours, so the `LAG` `LIMIT DURATION` reaches the previous report. The files contain exactly one record and establish no reporting cadence; both window sizes are guesses and should be re-tuned once the real interval is known.
7. **Assumption:** an absent member means the channel did not report, not that its value is zero. This drives metric 5 and the `IS NULL` guards. The schema makes all 14 measurement members optional and the instance omits `visibility` and `tide`, which is consistent with this reading but does not prove it.
8. **Assumption:** `gust >= wind_speed` is *not* guaranteed. The schema declares `$uses: ["JSONStructureValidation"]` but carries no validation keywords at all — no ranges, no units, no descriptions — so nothing constrains the values. A gust factor below 1 is therefore not treated as an error by the query.
9. **Assumption:** out-of-order and late arrivals are handled by the job's late-arrival policy, which is not part of the query and is not declared anywhere in the two files. `LAG` semantics depend on it.
10. **Assumption:** `AVG`, `MAX` and `SUM` ignore NULL inputs as in standard SQL, so partial reports reduce the sample size of a metric rather than poisoning it.
