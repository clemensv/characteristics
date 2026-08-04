# Five derived metrics over `VehicleEvent`

## 1. The five metrics

1. **Departure deviation at each served stop** — at the record where the vehicle stops carrying a given `stop`, the signed difference `tst − ttdep` in seconds, averaged and worst-cased per `route`+`dir` per window. This is the punctuality signal, and it is the only lateness figure whose unit is certain, because both operands are declared `datetime`.
2. **Deviation trend** — the change in that average between consecutive windows, expressed per minute. It separates "late but steady" from "deteriorating right now", which is what decides whether a controller intervenes; the level alone does not.
3. **Peak and mean occupancy** — `MAX(occu)` and `AVG(occu)` per `route`+`dir` per window. Crowding is the second thing a controller can act on (hold, short-turn, inject a vehicle), and the peak matters more than the mean because it is the vehicle that is full.
4. **Active vehicle count** — distinct reporting vehicles per `route`+`dir` per window. Answers "is the service that is actually on the road the service that was planned", which no single record can answer.
5. **Worst reporting gap** — the longest interval between successive records of any one vehicle on that `route`+`dir` in the window. It bounds the accuracy of metrics 1–4, all of which are sampled from this stream, and it surfaces vehicles that have dropped out of the feed.

## 2. The query

Event time is `tst`. Per-vehicle sequencing partitions on `oper`+`veh` combined into one key. Aggregation is a **5-minute tumbling window**, grouped by `route`+`dir`; the trend in metric 2 is a `LAG` across consecutive emissions of that same tumbling window.

```sql
WITH keyed AS (
    -- Event time is declared once, here, and is `tst` and nothing else.
    SELECT
        CONCAT(CAST(oper AS nvarchar(max)), ':', CAST(veh AS nvarchar(max))) AS vehicle_key,
        CONCAT(route, '/', dir)                                              AS service_key,
        route,
        dir,
        tst,
        stop,
        ttdep,
        occu
    FROM input TIMESTAMP BY tst
),

-- The individual source is the vehicle, so every LAG partitions on vehicle_key.
sequenced AS (
    SELECT
        vehicle_key,
        service_key,
        route,
        dir,
        tst,
        stop,
        occu,
        LAG(tst)   OVER (PARTITION BY vehicle_key LIMIT DURATION(minute, 10)) AS prev_tst,
        LAG(stop)  OVER (PARTITION BY vehicle_key LIMIT DURATION(minute, 10)) AS prev_stop,
        LAG(ttdep) OVER (PARTITION BY vehicle_key LIMIT DURATION(minute, 10)) AS prev_ttdep
    FROM keyed
),

scored AS (
    SELECT
        vehicle_key,
        service_key,
        route,
        dir,
        occu,
        -- metric 5, per record: silence since this vehicle's previous record
        CAST(DATEDIFF(second, prev_tst, tst) AS float) AS report_gap_sec,
        -- metric 1, per record: emitted only on the record after the last one
        -- that carried a given `stop`; the previous record is then the latest
        -- observation while the vehicle was still at that stop.
        CASE
            WHEN prev_stop  IS NOT NULL
             AND prev_ttdep IS NOT NULL
             AND (stop IS NULL OR stop <> prev_stop)
            THEN CAST(DATEDIFF(second, prev_ttdep, prev_tst) AS float)
        END AS departure_deviation_sec
    FROM sequenced
),

-- TumblingWindow, 5 minutes, one row per route+direction.
per_window AS (
    SELECT
        service_key,
        route,
        dir,
        System.Timestamp()                 AS window_end,
        AVG(departure_deviation_sec)       AS avg_departure_deviation_sec,   -- metric 1
        MAX(departure_deviation_sec)       AS worst_departure_deviation_sec, -- metric 1
        COUNT(departure_deviation_sec)     AS stop_departures_seen,          -- support for 1
        MAX(occu)                          AS peak_occupancy,                -- metric 3
        AVG(occu)                          AS mean_occupancy,                -- metric 3
        COUNT(DISTINCT vehicle_key)        AS active_vehicles,               -- metric 4
        MAX(report_gap_sec)                AS worst_report_gap_sec           -- metric 5
    FROM scored
    GROUP BY service_key, route, dir, TumblingWindow(minute, 5)
)

SELECT
    p.route,
    p.dir,
    p.window_end,
    p.avg_departure_deviation_sec,
    p.worst_departure_deviation_sec,
    p.stop_departures_seen,
    -- metric 2: window-over-window rate of change of the average deviation,
    -- normalised by the real elapsed time between the two emissions, because a
    -- route with no traffic in a window emits no row and the previous row may
    -- therefore be more than one window old.
    CASE
        WHEN DATEDIFF(minute,
                 LAG(p.window_end) OVER (PARTITION BY p.service_key LIMIT DURATION(minute, 20)),
                 p.window_end) > 0
        THEN (p.avg_departure_deviation_sec
              - LAG(p.avg_departure_deviation_sec)
                    OVER (PARTITION BY p.service_key LIMIT DURATION(minute, 20)))
             / DATEDIFF(minute,
                 LAG(p.window_end) OVER (PARTITION BY p.service_key LIMIT DURATION(minute, 20)),
                 p.window_end)
    END AS deviation_trend_sec_per_min,
    p.peak_occupancy,
    p.mean_occupancy,
    p.active_vehicles,
    p.worst_report_gap_sec
INTO output
FROM per_window p
-- Two constructs I cannot verify without the dialect reference: COUNT(DISTINCT ...)
-- inside a windowed GROUP BY, and LAG applied to an already-aggregated step. Both
-- are, to my knowledge, supported; if COUNT(DISTINCT ...) is not, metric 4 can be
-- rebuilt as a two-step count over a per-vehicle grouping.
```

## 3. What I did not compute

* **Anything built on `dl`.** `dl` is an `int32` with no declared unit, sign convention or reference point. The single instance settles it negatively: `dl` is −95, while `tst` − `ttarr` for the same record is −15.7 s. Whatever `dl` measures, it is not the residual in seconds against `ttarr`, so neither `AVG(dl)` nor `LAG(dl)` deltas can be given a unit. I derived punctuality from `tst` and `ttdep` instead, where the unit is forced by the types.
* **Speed cross-check between `spd` and `odo`.** `(odo − LAG(odo)) / DATEDIFF(second, prev_tst, tst)` compared against `spd` would be a good sensor-health residual, but it requires assuming `odo` is in metres and `spd` in metres per second. The schema declares neither. `odo` also has only `minimum: 0` and no reset semantics, so a delta spanning a reset would be a large negative number indistinguishable from a real value.
* **Harsh-braking or harsh-acceleration flags from `acc`.** `acc` has no declared unit and the schema declares no threshold. Any cut-off would be a number I invented.
* **Turn rate from `hdg`.** `hdg` is bounded `0..360` inclusive, so 0 and 360 are both legal for the same bearing, and nothing states whether the value wraps. `hdg − LAG(hdg)` is therefore not well defined without inventing wrap handling.
* **Distance travelled, or geofencing, from `lat`/`long`.** Beyond needing a spatial distance function, `loc` declares that a fix may come from `ODO`, `MAN`, `DR` or `N/A` as well as `GPS`, and the schema says nothing about the accuracy attached to each. Mixing those provenances into one distance sum is unsound.
* **Headway between successive vehicles at the same stop** — `LAG(tst) OVER (PARTITION BY stop ...)`. This is arguably the most valuable transit metric after punctuality, and I wanted it. It needs exactly one record per vehicle per stop. The feed evidently emits many records carrying the same `stop` (`stop`, `ttarr` and `ttdep` are all present on a record whose `tst` precedes `ttarr`), and nothing in the schema marks which record is the arrival. Approximating it would produce plausible-looking numbers that are really a function of the sampling rate, so I left it out.
* **Dwell time from `drst`.** Pairing `drst` 0→1 with 1→0 would give dwell per stop, and dwell is where delay is manufactured. But the schema states only that `drst` is 0 or 1; it does not say what either value means, and the measured duration would be quantised to the reporting interval.
* **Journey-level aggregates keyed on `journey_start.ordinal`.** The four-digit suffix in the instance is `0165` while `start` is `07:15`, so `ordinal` does not encode the start time, and its uniqueness scope (per operator? per day? globally?) is undeclared. I did not use it as a grouping key.
* **The share of records where `loc <> 'GPS'`.** Sound, cheap, and a real quality indicator. Dropped because none of the five metrics consumes `lat`/`long`, so position provenance would not qualify any of them — and five means five.
* **`desi` as a grouping key.** It is a separate string from `route` (`551` vs `2551`); I grouped on `route`+`dir` only and did not assume the two are interchangeable.

## 4. Assumptions

Each of the following is an assumption; none is established by the schema or the instance.

1. **`tst` is the observation time of the record**, is the correct event time for the job, and is UTC. Only the `Z` suffix in the instance supports this.
2. **`oper` and `veh` together identify a vehicle**; `veh` alone may collide across operators. Hence the composite `vehicle_key`.
3. **`route` + `dir` identify a service pattern** worth grouping on, and are stable within a journey.
4. **`stop` identifies the stop that `ttarr` and `ttdep` in the same record refer to**, and is carried contiguously — one uninterrupted run of records per stop visit. If `stop` flickers between a value and null during a single visit, metric 1 will emit more than one deviation for that visit.
5. **The last record carrying a given `stop` was emitted at or near the vehicle's departure from it**, so `tst` on that record approximates the actual departure and `tst − ttdep` approximates departure deviation. The error is bounded by the reporting interval, which is exactly what metric 5 measures — the two metrics are meant to be read together.
6. **`occu` is comparable across vehicles on the declared 0–100 scale.** The schema gives the bounds but not the meaning. If it is a raw passenger count rather than a percentage of capacity, `MAX(occu)` is still a useful alarm but `AVG(occu)` cannot be compared between routes running different vehicle types.
7. **`ttarr`/`ttdep` are absent on some records** (they are not in `required`), and `AVG`/`MAX`/`COUNT` skip nulls, so windows containing no stop departure yield a null deviation rather than a zero.
8. **Records for one vehicle arrive in `tst` order**, or late arrivals are absorbed by the job's out-of-order tolerance. `LAG` assumes this.
9. **A 10-minute `LIMIT DURATION` is long enough to reach a vehicle's previous record.** If a vehicle reports less often than that, its gap and its stop deviation are silently dropped rather than reported as large.
10. **Metric 5 is retrospective.** A gap is measured on the record that ends it, so a vehicle that goes silent and never returns produces no gap at all — it disappears instead from `active_vehicles` (metric 4). The two must be read together for that reason.
11. **A 5-minute window and a 20-minute `LIMIT DURATION` for the trend** are my choice, not the feed's. Nothing in the two files indicates the reporting cadence or the timetable granularity; the instance's single `tst` cannot establish either.
