# Five derived metrics for the JMA `EarthquakeReport` stream

## 1. The five metrics

1. **Solution latency** — `report_datetime` minus `origin_datetime`, in seconds, summarised per window as mean, p95 and max. The schema states that the report time is when the hypocentre and magnitude solution *became available* and that it is later than and independent of the origin time, so this difference is real production time between rupture and a usable answer. It is the feed's core service level, and the tail matters far more than the mean.
2. **Magnitude revision between successive bulletins of the same earthquake** — current `magnitude` minus the previous serial's `magnitude`, partitioned by `event_id`, reported as the largest upward and largest downward revision in the window and the number of bulletins that moved. `event_id` is explicitly shared across serials and `magnitude` is a computed solution, so revision is expected; an operator needs to know whether a number already acted on is still moving, and in which direction.
3. **Distinct-event rate** — count of distinct `event_id` per window. Seismic bulletin traffic is bursty; a jump in the number of separate earthquakes referenced per window is the aftershock/swarm signal and simultaneously the load signal for anything consuming the feed.
4. **Amendment share** — fraction of bulletins in the window whose `info_type` is not `ISSUED`, together with the outright `CANCELLED` count. `CANCELLED` retracts a bulletin, so downstream state built on it must be unwound; a rising amendment share is the trust indicator for the feed as a whole.
5. **Distribution latency** — `control_datetime` minus `report_datetime`, in seconds, mean and max per window. The schema goes out of its way to separate completion of the solution from handover into the distribution channel. Splitting this from metric 1 tells the operator whether a delay belongs to JMA's analysis or to the distribution path — different owner, different remedy.

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
--
-- Event time is report_datetime: the instant this bulletin's solution became
-- available, and the only one of the three timestamps that distinguishes the
-- serials of a single earthquake. origin_datetime is deliberately NOT the event
-- time -- every serial of one event repeats it, so a whole revision sequence
-- would collapse onto a single instant and LAG would have no ordering to work
-- with. control_datetime is a distribution-channel artefact, so using it would
-- fold channel delay into the window boundaries.
WITH Bulletins AS
(
    -- Record grain. Per-source partitioning happens here: event_id is the only
    -- member that identifies "one source" in the sense of a series of records
    -- describing the same thing over time. LIMIT DURATION is required on LAG.
    SELECT
        event_id,
        serial,
        info_type,
        magnitude,
        DATEDIFF(second, origin_datetime, report_datetime)  AS solution_latency_s,
        DATEDIFF(second, report_datetime, control_datetime) AS distribution_latency_s,
        LAG(magnitude, 1) OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_magnitude,
        LAG(serial,    1) OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_serial
    FROM input TIMESTAMP BY report_datetime
),
Derived AS
(
    SELECT
        event_id,
        solution_latency_s,
        distribution_latency_s,
        -- Only a genuine forward revision counts. serial > prev_serial guards
        -- against a re-delivered or out-of-order bulletin being read as a
        -- magnitude change. NULL magnitudes (震度速報 and similar bulletins that
        -- carry no magnitude) yield NULL and drop out of the aggregate.
        CASE
            WHEN magnitude      IS NOT NULL
             AND prev_magnitude IS NOT NULL
             AND prev_serial    IS NOT NULL
             AND serial > prev_serial
            THEN magnitude - prev_magnitude
        END AS magnitude_revision,
        CASE WHEN info_type <> 'ISSUED'    THEN 1 ELSE 0 END AS is_amended,
        CASE WHEN info_type  = 'CANCELLED' THEN 1 ELSE 0 END AS is_cancelled
    FROM Bulletins
)
SELECT
    System.Timestamp()                          AS window_end,
    COUNT(*)                                    AS bulletin_count,

    -- Metric 3: distinct-event rate.
    COUNT(DISTINCT event_id)                    AS distinct_event_count,

    -- Metric 1: solution latency, origin -> report.
    AVG(solution_latency_s)                     AS avg_solution_latency_s,
    MAX(solution_latency_s)                     AS max_solution_latency_s,
    -- The prompt states PERCENTILE_CONT is available. In the product it is an
    -- analytic function taking an OVER clause; I am not certain this exact form
    -- composes with the tumbling GROUP BY in a single pass. If it is rejected,
    -- drop this line -- avg and max above still carry the metric.
    PERCENTILE_CONT(0.95) OVER (ORDER BY solution_latency_s) AS p95_solution_latency_s,

    -- Metric 2: magnitude revision across serials of the same event_id.
    MAX(magnitude_revision)                     AS largest_magnitude_upgrade,
    MIN(magnitude_revision)                     AS largest_magnitude_downgrade,
    SUM(CASE WHEN magnitude_revision IS NOT NULL THEN 1 ELSE 0 END)
                                                AS bulletins_with_magnitude_change,

    -- Metric 4: amendment share and cancellations.
    CAST(SUM(is_amended) AS float) / COUNT(*)   AS amended_share,
    SUM(is_cancelled)                           AS cancelled_count,

    -- Metric 5: distribution latency, report -> control.
    AVG(distribution_latency_s)                 AS avg_distribution_latency_s,
    MAX(distribution_latency_s)                 AS max_distribution_latency_s
INTO output
FROM Derived
-- Tumbling window, 15 minutes, non-overlapping. Tumbling rather than hopping or
-- sliding because metrics 3 and 4 are counts and shares that must not be
-- double-counted across overlapping windows.
GROUP BY TumblingWindow(minute, 15)
```

The window-level `GROUP BY` deliberately does **not** include `event_id`. Metrics 3 and 4 are cross-event by construction — grouping by `event_id` would make `COUNT(DISTINCT event_id)` identically 1. Per-earthquake identity is used where it belongs, in the `PARTITION BY event_id` of the two `LAG` calls, so metric 2 never compares across earthquakes.

## 3. What I did not compute

- **Great-circle relocation distance between successive serials, from `latitude` and `longitude`.** The obvious "has the hypocentre moved?" metric, and the one I most wanted. Left out because converting a degree difference to a distance needs either trigonometry or a degrees-to-kilometres constant, and the two files establish neither; a constant would be domain knowledge I imported. `depth_km` alone could be differenced safely, but a depth shift without the horizontal shift is a misleading half of the answer.
- **Escalation of `max_intensity` between serials, and any average of `max_intensity` or `affected_prefectures[].max_intensity`.** These are ordinal strings (`5-`, `5+`, `6-`), and the files establish only that a maximum is defined over them, not that the steps are equal. Subtracting or averaging encoded ranks would assert an interval scale the schema does not license. Metric 2 already gives a revision signal on a member that *is* numeric.
- **Mean or sum of `magnitude` over a window.** Each earthquake contributes a variable number of bulletins, so a window mean is weighted by revision churn rather than by seismicity, and `magnitude` is null for several bulletin types. Deduplicating to the latest serial per event first would fix the weighting but not the second problem: the files do not establish that JMA magnitudes are additively combinable, so the mean has no stated meaning.
- **Any inter-arrival interval or missed-report residual built on gaps between `origin_datetime` values.** The schema says outright that earthquakes are not scheduled and that successive origin times carry no period. A "time since last event" or an expected-arrival residual would present noise as a signal. Counting events per fixed window (metric 3) is a rate and is not the same claim.
- **A windowed rate over `tsunami_possible`.** The schema says the value is inferred from free-text comments by the bridge and is an estimate of the bulletin's intent, not a published coded field, and it is nullable. Aggregating it would turn an inference into a measurement.
- **Ranking `bulletin_type` as a solution-maturity ordinal.** The description calls it "the scale on which the maturity of the solution is expressed", which is tempting, but the enum (`VXSE51`, `VXSE52`, `VXSE53`, `VXSE5k`, `VXSE61`, `VYSE52`) is given without any stated order. I would have to invent the ranking.
- **Grouping any aggregate by `epicenter_area_code`.** It is nullable, and the bulletin types that omit it are named in the schema. Grouping on it would silently exclude exactly those bulletins and bias every count, and the files supply no mapping from code to region beyond the name.
- **Breadth of the felt footprint, `GetArrayLength(affected_prefectures)`.** Sound and computable, and it ranked sixth — it lost to the five above rather than being unsound. I am also not fully certain of the array-length function name in this dialect.

## 4. Assumptions

- **Assumption:** `report_datetime` is non-decreasing across the serials of one `event_id`, so `LAG` ordered by event time returns the immediately preceding revision. The `serial > prev_serial` guard limits the damage if it is not, but does not fully repair it.
- **Assumption:** all revisions of an earthquake arrive within 6 hours of one another, which is what `LIMIT DURATION(hour, 6)` encodes. The files state nothing about how long a revision sequence stays open.
- **Assumption:** the 15-minute tumbling window is arbitrary. The files establish no cadence for this feed — indeed they deny one — so the size must come from the operator's alerting interval, not from the data.
- **Assumption:** `origin_datetime <= report_datetime <= control_datetime`, so both latencies are non-negative. The schema states report is later than origin; for control it says only that it records handover of the *finished* bulletin, which implies but does not state ordering. A negative value in either column should be treated as a clock or pipeline fault, not as a fast solution.
- **Assumption:** the RFC3339 strings in `origin_datetime`, `report_datetime` and `control_datetime` are parsed into datetime values by the ingest, so `DATEDIFF` receives datetimes and not strings. If they arrive as strings an explicit `CAST(... AS datetime)` is needed on each.
- **Assumption:** `COUNT(DISTINCT event_id)` is supported inside a windowed aggregate in this dialect.
- **Assumption (semantic, and the weakest one):** the distinct-event count in a window counts earthquakes *referenced* in that window, not earthquakes that *ruptured* in it. Because the window is on `report_datetime`, a late revision of an older earthquake contributes to the current window. I chose not to filter to first bulletins because the files do not establish whether the first serial is 0 or 1 — `serial` has a minimum of 0, and the one instance available carries serial 2.
