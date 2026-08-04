# Five derived metrics over the HSL HFP `vp` stream

## 1. The five metrics

1. **Route lateness distribution (median and 90th percentile), per `route` + `dir`, per 5-minute tumbling window.** The 50th and 90th percentile of `-dl` (the sign is flipped, because the schema states that negative `dl` means late). A single trip's deviation tells an operator nothing about the line; the median says whether the corridor is healthy and the P90 says whether the tail is being driven by a few crippled runs. This is the metric a control-room screen is built around.
2. **Lateness accrual rate per vehicle-trip, seconds of lateness gained per second of running.** The net change in `-dl` across the window divided by the seconds actually spanned by the message pairs that produced it. `dl` says how late a trip *is*; this says whether it is still getting later, and at what pace. A trip at +60 s and shedding delay needs no intervention; a trip at +60 s and accruing 0.3 s/s will be at +300 s within the next ten minutes and is the one to hold or short-turn.
3. **Non-satellite position share per vehicle-trip.** The fraction of messages in the window whose `loc` is not `GPS`. `loc` is the `observingProcedure` for `lat`/`long`, and the specification is explicit that procedure identity is comparability-critical — a run reported mostly by `ODO`, `DR` or `MAN` is not delivering positions of the same kind as one reported by `GPS`. This is both a fleet-equipment fault signal and the gate that tells a downstream consumer when passenger-facing arrival predictions built on this vehicle's position should be distrusted.
4. **Distance advanced per vehicle-trip in the window, from the odometer.** The sum of the non-negative successive increments of `odo`. The absolute `odo` value is meaningless across vehicles because the reset instant is not carried, but *within* one trip the counter accumulates monotonically, so its increments are a well-defined distance. This gives ground truth for movement that owes nothing to satellite reception, and it separates "stopped in traffic" from "stopped transmitting".
5. **Maximum inter-message interval per vehicle-trip, and a staleness flag.** The largest `DATEDIFF(second, previous tst, tst)` in the window, flagged when it exceeds ten times the declared one-second cadence. The specification permits a consumer to use a declared cadence to size a staleness threshold and to make an absent value detectable as a gap — as its own processing decision, not as a claim about the data. It is what distinguishes a vehicle that is late from a vehicle that has stopped reporting, which are different faults with different responses.

## 2. The query

```sql
-- Event time is `tst`: it is the only member carrying semanticRole
-- `phenomenonTime`. `ttarr`, `ttdep` and `journey_start` carry `scheduledTime`,
-- which the specification forbids reading as a phenomenon time.
WITH Keyed AS (
    SELECT
        oper, veh, route, dir, loc, dl, odo, tst,
        journey_start.ordinal AS trip_ordinal,
        -- `veh` carries `featureOfInterest` but the schema states it is unique
        -- only with `oper`, so the physical source is the pair. The trip key
        -- adds the operating-day position, which bounds the odometer reset.
        -- Composite keys are built here so that every PARTITION BY below
        -- names a single column.
        CONCAT(CAST(oper AS nvarchar(max)), ':', CAST(veh AS nvarchar(max)))
            AS vehicle_key,
        CONCAT(CAST(oper AS nvarchar(max)), ':', CAST(veh AS nvarchar(max)), ':',
               journey_start.ordinal) AS trip_key
    FROM hfp TIMESTAMP BY tst
),
Stepped AS (
    -- Successive messages of one vehicle on one trip. LIMIT DURATION is
    -- required by the dialect; ten minutes is a deliberate reach-back bound.
    SELECT
        trip_key, vehicle_key, oper, veh, route, dir, trip_ordinal, loc, tst,
        dl, odo,
        DATEDIFF(second,
                 LAG(tst, 1) OVER (PARTITION BY trip_key
                                   LIMIT DURATION(minute, 10)),
                 tst)                                              AS step_seconds,
        LAG(dl,  1) OVER (PARTITION BY trip_key
                          LIMIT DURATION(minute, 10))              AS prev_dl,
        LAG(odo, 1) OVER (PARTITION BY trip_key
                          LIMIT DURATION(minute, 10))              AS prev_odo
    FROM Keyed
),
Steps AS (
    SELECT
        trip_key, vehicle_key, oper, veh, route, dir, trip_ordinal, loc, tst,
        step_seconds,
        -- Lateness in the conventional sign: the schema declares `dl` negative
        -- when the vehicle is late.
        CASE WHEN dl IS NULL THEN NULL
             ELSE -CAST(dl AS bigint) END                          AS lateness_s,
        -- Numerator and denominator of the accrual rate, kept apart so that the
        -- window aggregate divides totals rather than averaging per-pair rates.
        CASE WHEN step_seconds > 0 AND prev_dl IS NOT NULL AND dl IS NOT NULL
             THEN CAST(prev_dl AS bigint) - CAST(dl AS bigint)
             END                                                   AS lateness_gain_s,
        CASE WHEN step_seconds > 0 AND prev_dl IS NOT NULL AND dl IS NOT NULL
             THEN step_seconds
             END                                                   AS lateness_span_s,
        -- Odometer increments only. A trip-start reset appears as a decrease and
        -- is discarded rather than counted as distance.
        CASE WHEN prev_odo IS NOT NULL AND odo IS NOT NULL AND odo >= prev_odo
             THEN odo - prev_odo
             END                                                   AS odo_step_m
    FROM Stepped
),
RouteLateness AS (
    -- Metric 1. Window: tumbling, 5 minutes. Partitioned by route and direction.
    -- NOTE: I am unsure Azure Stream Analytics accepts the `WITHIN GROUP`
    -- aggregate spelling of PERCENTILE_CONT; its documented form is the
    -- analytic `PERCENTILE_CONT(p) OVER (PARTITION BY ... ORDER BY ...)`.
    -- If this form is rejected, AVG(lateness_s) and MAX(lateness_s) are certain
    -- substitutes, at the cost of the tail statistic.
    SELECT
        route,
        dir,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY lateness_s)
            AS route_lateness_p50_s,
        PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY lateness_s)
            AS route_lateness_p90_s
    FROM Steps
    GROUP BY route, dir, TumblingWindow(minute, 5)
),
TripWindow AS (
    -- Metrics 2 to 5. Window: tumbling, 5 minutes.
    -- Partitioned by the vehicle-trip: (oper, veh, journey_start.ordinal).
    SELECT
        trip_key, vehicle_key, oper, veh, route, dir, trip_ordinal,
        COUNT(*)                                                   AS samples,
        CASE WHEN SUM(lateness_span_s) > 0
             THEN CAST(SUM(lateness_gain_s) AS float)
                  / CAST(SUM(lateness_span_s) AS float)
             END                                                   AS lateness_accrual_s_per_s,
        CAST(SUM(CASE WHEN loc <> 'GPS' THEN 1 ELSE 0 END) AS float)
             / CAST(COUNT(*) AS float)                             AS non_gps_fix_share,
        SUM(odo_step_m)                                            AS odo_distance_m,
        MAX(step_seconds)                                          AS max_message_gap_s
    FROM Steps
    GROUP BY trip_key, vehicle_key, oper, veh, route, dir, trip_ordinal,
             TumblingWindow(minute, 5)
)
SELECT
    System.Timestamp()               AS window_end,
    t.oper,
    t.veh,
    t.route,
    t.dir,
    t.trip_ordinal,
    r.route_lateness_p50_s,          -- metric 1
    r.route_lateness_p90_s,          -- metric 1
    t.lateness_accrual_s_per_s,      -- metric 2
    t.non_gps_fix_share,             -- metric 3
    t.odo_distance_m,                -- metric 4
    t.max_message_gap_s,             -- metric 5
    -- Ten times the declared one-second cadence. The threshold is a consumer
    -- decision about staleness, not an assertion that the feed is malformed.
    CASE WHEN t.max_message_gap_s > 10 THEN 1 ELSE 0 END
                                     AS message_gap_flag,           -- metric 5
    t.samples                        -- denominator of metric 3, not a claim
INTO output
FROM TripWindow t
JOIN RouteLateness r
  -- Both sides are 5-minute tumbling aggregates emitted at the same window end,
  -- so the dialect-required time predicate is a zero-width one.
  ON t.route = r.route
 AND t.dir   = r.dir
 AND DATEDIFF(minute, t, r) BETWEEN 0 AND 0
```

Reading the output: `lateness_accrual_s_per_s` is positive when the trip is losing time. `route_lateness_p50_s` and `route_lateness_p90_s` are positive when the line is running late. `non_gps_fix_share` qualifies `lat`/`long` only — `loc` is declared the procedure that produced those two members — so it is reported beside the other metrics rather than used to filter them; `dl` and `odo` do not come from it.

## 3. What I did not compute

* **Any aggregate of `occu`.** Mean or peak occupancy per route is the obvious commercial metric and it is unsound here. The schema states that only Suomenlinna ferries report a measured value and every other vehicle class transmits a constant, and it says a consumer must know the transport mode before reading it. No member of the record carries transport mode. Averaging `occu` over a mixed fleet would average measurements with placeholders and produce a number with no referent.
* **Ground distance or a speed cross-check from `lat` and `long`.** Displacement between successive positions, compared against `spd`, would be a genuine residual and would catch a stuck receiver. `coordinateReferenceSystem` identifies EPSG:4326 and fixes the axis order as `lat` then `long`, and that is all it does: the specification states that these annotations make an incompatibility detectable and define no conversion, and that transforming values so they can be combined is the work of a tool holding the authoritative definitions. Turning decimal degrees into metres requires a projection that neither file supplies, and I will not assume one. Metric 4 uses `odo` instead, which is already in metres.
* **Any time-weighted mean or integral of `acc`.** `acc` carries `phenomenonTimeRelation: interval` and declares no `supportPeriod`; the schema says the interval's opening boundary is not carried, that its length varies with the actual spacing of messages, and — explicitly — that the one-second cadence on `tst` does not bound it. The specification's rule is that an `interval` result with neither a boundary pair nor a `supportPeriod` has a declared support whose extent is indeterminate. Averaging or integrating values of unknown and unequal support is not licensed, so I left `acc` out entirely rather than compute a harsh-braking rate that silently assumes equal intervals.
* **Elapsed time since scheduled departure, from `journey_start` and `tst`.** This looks like the most natural derived quantity in the record and it is forbidden by the record itself. The `OperatingDayClockPosition` meta-type states that a position is not an RFC 3339 civil instant and MUST NOT be compared with one without applying the regime; `oday` looks like a calendar date and is not one, and `start` wraps within the operating day. The schema carries no UTC offset for Helsinki local time, so the regime cannot be applied from these two files. `journey_start.ordinal` is used only as an opaque, correctly-sorting key.
* **A departure or arrival residual from `tst` against `ttarr` / `ttdep`.** `ttarr` and `ttdep` are `scheduledTime`, which the specification forbids reading as a phenomenon time or as an actual time, and the record carries no `actualTime`. `stop` names the stop the vehicle *most recently departed from*, so the first `tst` bearing a given `stop` is not the arrival instant at it. Any residual built this way would be a proxy of unknown bias competing with `dl`, which the schema states is computed onboard against the schedule anchored at `journey_start` and is the authoritative deviation.
* **Circular statistics or a turn rate on `hdg`.** `hdg` declares `minimum: 0` and `maximum: 360`, so north is admitted under two values, and no `vectorReferenceFrames` annotation is present to establish a frame for differencing. A linear mean of a circular quantity is wrong at the wrap point, and unwrapping it correctly is a convention neither file states.
* **Door-open dwell time from `drst`.** Counting `0 → 1` transitions would be sound and I could have made it a sixth metric; converting those transitions into *seconds* of door-open time would not be, because it requires treating each message as covering one second, and the specification states that a cadence is not a completeness assertion and does not assert that every position has a record. I left the whole member out to stay at five rather than ship the transition count in place of something more valuable.
* **Grouping by `desi`.** `desi` is described as the head-sign display label and explicitly not the GTFS route identifier. All route-level grouping is on `route` and `dir`, which are both required members.

## 4. Assumptions

* **Assumption.** The five-minute tumbling window is my choice. The only timing fact the two files establish is the one-second cadence on `tst`; nothing in them fixes an aggregation period.
* **Assumption.** The ten-minute `LIMIT DURATION` on every `LAG` is my choice. It censors metric 5: a genuine reporting gap longer than ten minutes yields a NULL previous message rather than a large `max_message_gap_s`, so the metric detects gaps up to that bound and the absence of rows detects longer ones.
* **Assumption.** The staleness threshold of ten seconds is mine, chosen as ten times the declared cadence. The specification is clear that an instance departing from a declared cadence is not thereby invalid, so this flag is a processing decision and not a validity claim.
* **Assumption.** `(oper, veh, journey_start.ordinal)` identifies one continuous run — that is, a vehicle is on one such trip at a time and does not interleave messages from two. The schema states that `oper` + `veh` identifies the physical vehicle and that `oday` + `start` identifies the trip; that their combination is contiguous in the stream is my inference.
* **Assumption.** The odometer reset at actual trip start moves the counter *downward*, so filtering to non-negative increments discards it. The schema says the counter is reset and accumulates from that reset; it does not state the value it resets to.
* **Assumption.** `ODO`, `DR`, `MAN` and `N/A` are grouped together as "not satellite-fixed" in metric 3. The enum's own descriptions support the grouping — they name propagation, manual entry, and an undetermined method as against a satellite fix — but the schema states no ranking of position quality among them, so the metric deliberately reports one share rather than a graded score.
* **Assumption.** `dl` and `odo` are not in the schema's `required` list, so they may be absent from any message. The aggregates skip NULLs, which means metrics 1, 2 and 4 are computed over an unstated subset of the messages counted by `samples`. A production job should carry per-metric denominators; I did not add them because they would read as additional metrics.
* **Assumption.** The dialect accepts `PERCENTILE_CONT` in the aggregate position of a windowed `GROUP BY`, and accepts a zero-width `DATEDIFF` predicate joining two windowed aggregates. Both are flagged in comments in the query, with the fallback stated for the first.
* **Assumption.** Out-of-order and late-arrival tolerance for `TIMESTAMP BY tst` is configured on the job rather than in the query. `tst` is generated by the vehicle, and the schema does not state that messages reach the broker in the order the vehicles sampled them.
