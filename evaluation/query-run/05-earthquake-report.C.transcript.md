# EarthquakeReport — five derived metrics

## 1. The five metrics

1. **Intensity escalation step** — the change in the ordinal rank of `max_intensity` between consecutive bulletins carrying the same `event_id`; a positive step means a revision raised the assessed shaking, which is the one change in this feed most likely to force a different downstream response.
2. **Bulletin latency**, decomposed — `DATEDIFF(second, origin_datetime, control_datetime)`, split into analysis lag (`origin_datetime`→`report_datetime`) and publication lag (`report_datetime`→`control_datetime`); it tells the operator how late the news is *and* which half of the producer's pipeline is responsible.
3. **Missed-bulletin count** — gaps in `serial` between consecutive observed bulletins of an event (`serial - prev_serial - 1`); a numbered sequence is the only thing in this record that lets you notice silent loss, and losing a bulletin means running on a superseded intensity.
4. **Magnitude revision drift** — `ABS(magnitude - prev_magnitude)` between consecutive bulletins of the same event; it measures how much the solution moves after first publication, i.e. how much an early bulletin can be trusted.
5. **Amendment share** — the fraction of an event's bulletins whose `info_type` is `CORRECTED` or `CANCELLED`, with a separate cancelled flag; a retraction rate is the cheapest available quality signal for the feed and for the individual event.

## 2. The query

```sql
-- Azure Stream Analytics / Fabric Eventstream SQL operator.
-- Event time is control_datetime (see assumptions). Aggregation window:
-- TumblingWindow(minute, 10), partitioned by event_id, which is the only
-- member that identifies an individual source (one earthquake, many bulletins).

WITH Bulletins AS (
    SELECT
        event_id,
        serial,
        info_type,
        magnitude,
        max_intensity,
        -- Metric 2: latency and its two additive halves.
        DATEDIFF(second, origin_datetime, report_datetime)   AS analysis_lag_sec,
        DATEDIFF(second, report_datetime,  control_datetime) AS publish_lag_sec,
        DATEDIFF(second, origin_datetime,  control_datetime) AS total_latency_sec,
        -- Ordinal rank taken from the order in which the max_intensity enum is
        -- declared. max_intensity is NOT in "required", so this is NULL whenever
        -- the member is absent, and every metric built on it is null-guarded.
        CASE
            WHEN max_intensity = '1'  THEN 1
            WHEN max_intensity = '2'  THEN 2
            WHEN max_intensity = '3'  THEN 3
            WHEN max_intensity = '4'  THEN 4
            WHEN max_intensity = '5-' THEN 5
            WHEN max_intensity = '5+' THEN 6
            WHEN max_intensity = '6-' THEN 7
            WHEN max_intensity = '6+' THEN 8
            WHEN max_intensity = '7'  THEN 9
            ELSE NULL
        END AS intensity_rank
    FROM input TIMESTAMP BY control_datetime
),

Sequenced AS (
    -- Reach the previous bulletin of the SAME earthquake. LIMIT DURATION is
    -- mandatory; 6 hours is an operational choice, not something the files state.
    -- LAG runs before the GROUP BY, so a comparison still works when the two
    -- bulletins land in different tumbling windows.
    SELECT
        event_id,
        serial,
        info_type,
        analysis_lag_sec,
        publish_lag_sec,
        total_latency_sec,
        intensity_rank,
        magnitude,
        LAG(intensity_rank, 1) OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_intensity_rank,
        LAG(magnitude, 1)      OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_magnitude,
        LAG(serial, 1)         OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_serial
    FROM Bulletins
),

Derived AS (
    SELECT
        event_id,
        intensity_rank,
        total_latency_sec,
        analysis_lag_sec,
        publish_lag_sec,
        -- Metric 1. Negative values are downgrades; NULL when either bulletin
        -- omitted max_intensity.
        CASE WHEN intensity_rank IS NULL OR prev_intensity_rank IS NULL
             THEN NULL
             ELSE intensity_rank - prev_intensity_rank
        END AS intensity_step,
        -- Metric 4. magnitude is optional and nullable, so guard both sides.
        CASE WHEN magnitude IS NULL OR prev_magnitude IS NULL
             THEN NULL
             ELSE ABS(magnitude - prev_magnitude)
        END AS magnitude_drift,
        -- Metric 3. Only detects gaps BETWEEN observed bulletins; if the first
        -- bulletin we see already has serial 2 (as the example does) we cannot
        -- tell whether 0 and 1 were lost or never existed, so we score 0.
        CASE WHEN prev_serial IS NULL THEN 0
             WHEN serial - prev_serial > 1 THEN serial - prev_serial - 1
             ELSE 0
        END AS serial_gap,
        -- Metric 5.
        CASE WHEN info_type = 'CORRECTED' OR info_type = 'CANCELLED' THEN 1 ELSE 0 END AS is_amendment,
        CASE WHEN info_type = 'CANCELLED' THEN 1 ELSE 0 END AS is_cancelled
    FROM Sequenced
)

SELECT
    System.Timestamp()                  AS window_end,
    event_id,
    COUNT(*)                            AS bulletins,               -- context / denominator
    MAX(intensity_rank)                 AS peak_intensity_rank,     -- context for metric 1
    MAX(intensity_step)                 AS max_intensity_step,      -- metric 1
    MAX(total_latency_sec)              AS worst_total_latency_sec, -- metric 2
    AVG(total_latency_sec)              AS avg_total_latency_sec,   -- metric 2
    AVG(analysis_lag_sec)               AS avg_analysis_lag_sec,    -- metric 2 (split)
    AVG(publish_lag_sec)                AS avg_publish_lag_sec,     -- metric 2 (split)
    SUM(serial_gap)                     AS missed_bulletins,        -- metric 3
    MAX(magnitude_drift)                AS max_magnitude_drift,     -- metric 4
    SUM(is_amendment) * 1.0 / COUNT(*)  AS amendment_share,         -- metric 5
    MAX(is_cancelled)                   AS cancelled_flag           -- metric 5
INTO output
FROM Derived
GROUP BY event_id, TumblingWindow(minute, 10)
```

Deliberate syntax choices, so that nothing here rests on a construct I cannot
check: searched `CASE` rather than the simple `CASE expr WHEN` form; `OR`
rather than an `IN` list; no `CROSS APPLY GetArrayElements`, no geospatial
functions, no `PERCENTILE_CONT`.

## 3. What I did not compute

* **Residual between `max_intensity` and `MAX(affected_prefectures[].max_intensity)`.** An internal-consistency check, and in the one example the two agree ("4"). Left out because nothing in the schema says the top-level member is *defined* as the maximum over that array — the array may enumerate only the prefectures the producer chose to list. Computing it would also need `CROSS APPLY GetArrayElements(affected_prefectures)`, which I cannot confirm the Fabric SQL operator accepts.
* **Epicentre drift between revisions, from `latitude`, `longitude` and `depth_km`.** A delta in degrees is not a distance (a degree of longitude shrinks with latitude), a real great-circle distance needs trigonometry or `ST_DISTANCE`/`CreatePoint` whose availability here I cannot verify, and all three members are optional so the per-event series is gappy.
* **Tsunami transition on `tsunami_possible`.** A false→true flip across revisions would be highly actionable, but the member is required *and* nullable and the files assign no meaning to null. A null→true step cannot be distinguished from "the earlier bulletin simply did not carry a value", and treating null as false would be inventing a fact.
* **Energy or seismic-moment aggregation from `magnitude`.** The schema gives `magnitude` no scale, no unit and no bounds. Any exponential energy conversion, or summing releases over a window, would be imported domain knowledge.
* **Depth banding of `depth_km`** into shallow / intermediate / deep. No thresholds are declared anywhere in the two files; only the range 0–700 is.
* **Feed-wide latency percentiles** — `PERCENTILE_CONT` over `total_latency_sec`. The statement is grouped by `event_id`, and a single event contributes too few bulletins for a percentile to be meaningful. A useful percentile needs a second output grouped only by the window, which a single statement cannot emit alongside this one.
* **Mix ratios over `bulletin_type` and `epicenter_area_code`.** The enum members `VXSE51`…`VYSE52` and the area codes have no stated meaning in either file, so a share-per-type figure would not be interpretable; `epicenter_area_code` is also optional and nullable.
* **Event-arrival rate as a seismicity rate, and aftershock-sequence clustering.** Both would require assuming the feed is complete and inventing a space/time threshold for "same sequence".
* **Inter-bulletin interval**, `DATEDIFF(second, prev_control_datetime, control_datetime)`. Dropped as largely redundant with `bulletins` counted over a fixed 10-minute window.
* **Parsing `event_id` as a timestamp.** Its 14 digits equal `origin_datetime` in the single example, but the schema declares only `^[0-9]{14}$`. It is used strictly as an opaque partition key.

## 4. Assumptions

* *Assumption:* `control_datetime` is the publication-side timestamp and is non-decreasing in the order records are produced, which is why it is the event time. The only support is the single example (14:38:12 ≥ 14:38:00 ≥ 14:32:07). `origin_datetime` was rejected because every revision of one earthquake repeats it, which would collapse a whole bulletin sequence onto one instant.
* *Assumption:* `event_id` is stable across revisions and identifies one earthquake. The schema never says so; the example's `report_id` of `20260729143207_2` = `event_id` + `_` + `serial` is what suggests it.
* *Assumption:* `serial` increments by exactly 1 per new bulletin of an event, so `serial - prev_serial - 1` counts missed bulletins. The schema states only `integer, minimum 0`.
* *Assumption:* the declaration order of the `max_intensity` enum (`1,2,3,4,5-,5+,6-,6+,7`) is ascending severity. The file declares the order; it does not declare that the order means severity. Ranks 1–9 are mine.
* *Assumption:* all revisions of one event arrive inside `LIMIT DURATION(hour, 6)`. Nothing states how long an event remains under revision.
* *Assumption:* `TumblingWindow(minute, 10)` is a reasonable reporting cadence. The files establish no cadence at all; this number is arbitrary and should be tuned.
* *Assumption:* an absent `max_intensity` or a null `magnitude` means "not carried in this bulletin", not zero. Both are outside `required`, so every metric touching them is null-guarded and simply yields no value rather than a false one.
* *Assumption:* records reach the query in approximately `control_datetime` order, within whatever out-of-order tolerance the job is configured with.
* *Assumption:* the input and output aliases are `input` and `output`.
* *Assumption / limitation:* latency is measured entirely inside the record's own clock domain. The record carries no ingestion or arrival timestamp, so true end-to-end delivery lag from producer to this query is not observable from these two files.
