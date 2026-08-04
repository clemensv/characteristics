# Five derived metrics for the HSL HFP `vp` stream

## 1. The five metrics

1. **Route-direction lateness distribution** — median and 90th-percentile of `-dl`
   over a 5-minute tumbling window, grouped by `route` + `dir`. The schema states
   the sign convention is inverted, so flipping it once yields "seconds late"
   (positive) / "seconds early" (negative). This is the headline punctuality of
   the service as a passenger experiences it, and the p90 exposes the tail that a
   mean hides.
2. **Per-trip lateness drift** — the change in `-dl` per second between
   successive messages of the *same* trip, averaged over the window. It separates
   "late and still losing time" from "late but recovering", which is the
   distinction a controller acts on; the level alone does not carry it.
3. **Non-GPS position share** — fraction of a vehicle's messages in the window
   whose `loc` is not `GPS`. The schema says `loc` switches without warning to
   `ODO`/`DR`/`MAN`, meaning the coordinates were propagated or typed in rather
   than fixed. This is the trust gate on every position-derived product
   downstream, and it is the only quality signal the record carries about `lat`
   and `long`.
4. **Maximum inter-message interval per vehicle** — the largest gap between
   consecutive `tst` values in the window, in seconds. The feed is expected at
   roughly 1 Hz per vehicle, so the largest gap detects onboard-unit or telemetry
   dropout and bounds how stale that vehicle's last known state is.
5. **Door-open seconds per trip** — time accumulated while `drst` = 1, measured
   from differences between successive `tst` values rather than by counting
   messages. Door-open time is the vehicle's service time at stops and the main
   controllable component of running time; measuring it in seconds makes it
   immune to changes in message cadence.

## 2. The query

```sql
WITH
-- ---------------------------------------------------------------------------
-- keyed: build identity keys and correct the delay sign once.
--
-- A vehicle is identified only by (oper, veh) -- `veh` is stated to be unique
-- only in combination with `oper`. A trip additionally needs route, dir and the
-- operating-day position. `journey_start.ordinal` is used strictly as an opaque
-- discriminator: no arithmetic and no comparison against `tst` is done with it,
-- because it is a position in the operating-day regime and not a civil instant.
--
-- Composite single-column keys are built here so that every PARTITION BY below
-- takes exactly one column, which avoids relying on multi-column PARTITION BY
-- in the analytic functions.
-- ---------------------------------------------------------------------------
keyed AS (
    SELECT
        tst,
        route,
        dir,
        loc,
        drst,
        CONCAT(CAST(oper AS nvarchar(max)), ':', CAST(veh AS nvarchar(max)))
            AS vehicle_key,
        CONCAT(CAST(oper AS nvarchar(max)), ':', CAST(veh AS nvarchar(max)), ':',
               route, ':', dir, ':', journey_start.ordinal)
            AS trip_key,
        CONCAT(route, ':', dir) AS route_dir,
        -- `dl` is NEGATIVE when the vehicle is LATE. Flip it once here so every
        -- number downstream reads "seconds late". `dl` is optional, hence NULL.
        CASE WHEN dl IS NULL THEN NULL ELSE -1 * dl END AS lateness_s
    FROM hfp TIMESTAMP BY tst      -- `tst` is the instant the vehicle sampled
                                   -- the reported state; it is the only member
                                   -- that is an observation instant.
),

-- ---------------------------------------------------------------------------
-- paired: reach the previous message. Gaps are taken per VEHICLE (feed health
-- follows the physical unit across trips); delay drift and door state are taken
-- per TRIP, because `dl` is anchored at `journey_start` and is not comparable
-- across trips. LIMIT DURATION is required by the dialect.
-- ---------------------------------------------------------------------------
paired AS (
    SELECT
        tst, route, dir, route_dir, vehicle_key, trip_key, loc, drst, lateness_s,
        DATEDIFF(millisecond,
                 LAG(tst, 1) OVER (PARTITION BY vehicle_key
                                   LIMIT DURATION(minute, 10)),
                 tst) AS veh_gap_ms,
        DATEDIFF(millisecond,
                 LAG(tst, 1) OVER (PARTITION BY trip_key
                                   LIMIT DURATION(minute, 10)),
                 tst) AS trip_gap_ms,
        LAG(lateness_s, 1) OVER (PARTITION BY trip_key
                                 LIMIT DURATION(minute, 10)) AS prev_lateness_s,
        LAG(drst, 1)       OVER (PARTITION BY trip_key
                                 LIMIT DURATION(minute, 10)) AS prev_drst
    FROM keyed
),

-- ---------------------------------------------------------------------------
-- derived: per-event quantities. The 30 000 ms ceiling is an assumption (see
-- section 4): beyond it the interval is treated as a telemetry gap, so it is
-- neither credited as door-open time nor used as a drift denominator.
-- ---------------------------------------------------------------------------
derived AS (
    SELECT
        tst, route, dir, route_dir, vehicle_key, trip_key, lateness_s, veh_gap_ms,
        -- metric 3 indicator: `loc` is required, so no NULL guard. 'N/A' counts
        -- as non-GPS, as do ODO, DR and MAN.
        CASE WHEN loc = 'GPS' THEN 0 ELSE 1 END AS non_gps,
        -- metric 2: seconds of lateness gained per second of elapsed time,
        -- over an interval this query measures itself.
        CASE WHEN prev_lateness_s IS NOT NULL
              AND lateness_s IS NOT NULL
              AND trip_gap_ms > 0
              AND trip_gap_ms <= 30000
             THEN (lateness_s - prev_lateness_s) * 1000.0 / trip_gap_ms
             ELSE NULL
        END AS drift_s_per_s,
        -- metric 5: the interval [prev_tst, tst] is credited as door-open only
        -- if the doors were open at its start. `drst` is absent when the
        -- onboard system cannot determine it; absent contributes nothing.
        CASE WHEN prev_drst = 1
              AND trip_gap_ms > 0
              AND trip_gap_ms <= 30000
             THEN trip_gap_ms / 1000.0
             ELSE 0.0
        END AS door_open_s
    FROM paired
),

-- ---------------------------------------------------------------------------
-- veh_win: metrics 2, 3, 4, 5. Window: 5-minute TumblingWindow.
-- Partitioned by trip (and therefore by vehicle, which a trip determines).
-- ---------------------------------------------------------------------------
veh_win AS (
    SELECT
        vehicle_key, trip_key, route_dir, route, dir,
        System.Timestamp()             AS window_end,
        AVG(drift_s_per_s)             AS lateness_drift_s_per_s,   -- metric 2
        SUM(non_gps) * 1.0 / COUNT(*)  AS non_gps_share,            -- metric 3
        MAX(veh_gap_ms) / 1000.0       AS max_report_gap_s,         -- metric 4
        SUM(door_open_s)               AS door_open_s,              -- metric 5
        COUNT(*)                       AS msg_count                 -- denominator
                                                                    -- for metric 3,
                                                                    -- not a metric
    FROM derived
    GROUP BY vehicle_key, trip_key, route_dir, route, dir,
             TumblingWindow(minute, 5)
),

-- ---------------------------------------------------------------------------
-- route_win: metric 1. Window: 5-minute TumblingWindow, partitioned by the
-- route/direction pair. Grouping is on `route` (the GTFS identifier), not on
-- `desi`, which the schema declares to be a display label.
--
-- Dialect note: PERCENTILE_CONT is used in the documented
-- OVER (PARTITION BY ... ORDER BY ...) form inside a windowed GROUP BY. I am
-- confident the function exists but not certain of this exact combination; if
-- it is rejected, substitute a plain aggregate such as AVG(lateness_s) and
-- MAX(lateness_s) and lose the tail detail.
-- ---------------------------------------------------------------------------
route_win AS (
    SELECT
        route_dir,
        PERCENTILE_CONT(0.5) OVER (PARTITION BY route_dir ORDER BY lateness_s)
            AS median_lateness_s,
        PERCENTILE_CONT(0.9) OVER (PARTITION BY route_dir ORDER BY lateness_s)
            AS p90_lateness_s
    FROM derived
    WHERE lateness_s IS NOT NULL
    GROUP BY route_dir, TumblingWindow(minute, 5)
)

-- ---------------------------------------------------------------------------
-- Output at vehicle-trip grain, with the route-level punctuality of the same
-- 5-minute window attached. LEFT JOIN so that the quality metrics still emit
-- for a window in which no vehicle on that route reported `dl`. The dialect
-- requires a DATEDIFF bound on a join; both sides are aligned 5-minute tumbling
-- windows, so the bound is zero.
-- ---------------------------------------------------------------------------
SELECT
    v.window_end,
    v.route,
    v.dir,
    v.vehicle_key,
    v.trip_key,
    r.median_lateness_s,          -- metric 1 (positive = seconds late)
    r.p90_lateness_s,             -- metric 1
    v.lateness_drift_s_per_s,     -- metric 2 (positive = losing time)
    v.non_gps_share,              -- metric 3
    v.max_report_gap_s,           -- metric 4
    v.door_open_s,                -- metric 5
    v.msg_count
INTO metrics
FROM veh_win v
LEFT JOIN route_win r
    ON v.route_dir = r.route_dir
   AND DATEDIFF(second, v, r) BETWEEN 0 AND 0
```

## 3. What I did not compute

* **Anything from `occu`.** The schema states that only Suomenlinna ferries
  report a measured value and that every other vehicle class transmits a
  constant. The record carries no transport mode, so no consumer of this stream
  alone can tell a measurement from a constant. Any occupancy average would be a
  mixture of the two.
* **Averages or spreads of `hdg`.** It is degrees clockwise from north, a
  circular quantity: `AVG` and `STDEV` are wrong across the 359°/0° wrap, and a
  turn rate from `LAG` would need wrap-corrected differencing. Nothing in the two
  files establishes a vector-mean convention, so I left heading out entirely.
* **Any aggregate of `acc`.** The schema is explicit that the vehicle does not
  measure it: it is already a difference of two `spd` samples over an interval
  whose length the record does not carry, it is undefined for the first message
  of a trip, and no support period is declared. Aggregating it would re-express
  `spd` with doubled noise and an indeterminate support period. Metric 2 is the
  sound alternative: a rate of change over an interval the query measures itself
  from consecutive `tst` values.
* **`odo`-derived distance, and an `odo`-versus-`spd` residual.** Tempting,
  because they are two independent statements about progress. Rejected on two
  grounds the schema states: the `odo` counter resets when the vehicle actually
  begins the trip and the reset instant is not carried, so a negative delta
  cannot be distinguished from a reset without an out-of-band signal; and `spd`
  is instantaneous at `tst` whereas an `odo` delta is a mean over a
  variable-length interval, so the two are not like-for-like and the residual
  would not be a measurement of anything.
* **Keying door-open time (metric 5) to a stop.** `stop` names the stop the
  vehicle *most recently departed from* and is absent between stop relations, so
  the record does not identify the stop currently being served. Attributing a
  dwell to `stop` would credit it to the wrong stop. Metric 5 is therefore
  reported per trip.
* **An observed-minus-timetabled residual from `ttarr` / `ttdep` against `tst`.**
  Both are planned times, populated only inside a stop relation, and they refer
  to the stop named by `stop` — which, per the point above, is the stop already
  departed. The residual would compare a plan for one stop against an
  observation at another. `dl` already carries the schedule residual, computed
  onboard against `journey_start`, and metrics 1 and 2 use that instead.
* **Elapsed time since scheduled departure, from `journey_start` and `tst`.** The
  `OperatingDayClockPosition` meta-type states that a position is not an RFC 3339
  civil instant and must not be compared with one without applying the regime,
  which involves an approximately 04:30 boundary and a clock component that wraps
  within a day. I use `ordinal` only as an opaque trip discriminator and do no
  arithmetic on it.
* **Speed or distance from `lat` / `long`.** The coordinates are optional and,
  when `loc` is `ODO`, `DR` or `MAN`, they were propagated from other sensors or
  entered by a human rather than fixed by satellite. Even granting a geodesic
  distance function in the dialect, a position-derived speed would silently mix
  fixed and propagated points. Metric 3 is what I compute instead: the share of
  positions you cannot trust.
* **Grouping punctuality by `desi`.** It is the head-sign label, not the GTFS
  route identifier, so it may merge or split routes. Metric 1 groups on `route`
  and `dir`.
* **Headway between successive vehicles on a route.** It needs a shared
  reference point and a stop sequence. The record gives neither: `stop` is
  intermittent and refers to the previously departed stop, and there is no
  ordering of stops along the route.
* **Any comparison of `oper` against the owning operator.** The schema notes the
  two may differ under subcontracting, but the record carries only the operating
  one; the topic-borne owner is not in the payload.

## 4. Assumptions

* **Assumption.** `tst` is the correct event time for all five metrics, and
  messages arrive within whatever late-arrival and out-of-order tolerance the job
  is configured with. That tolerance is a job setting, not part of this SQL.
* **Assumption.** An inter-message interval longer than 30 s within a trip is a
  telemetry gap rather than a genuine one-sample observation, so intervals above
  that ceiling are excluded from the door-open accumulation and from the drift
  denominator. The schema says the ~1 s cadence states what the vehicle is
  expected to emit next and does not bound the actual spacing, so 30 s is my
  choice, not the schema's.
* **Assumption.** The tuple (`oper`, `veh`, `route`, `dir`,
  `journey_start.ordinal`) is unique per trip — i.e. one vehicle does not run two
  distinct trips with the same operating-day position on the same route and
  direction. The schema says the (`oday`, `start`) pair identifies the trip, and
  `ordinal` is its canonical rendering, but uniqueness against the vehicle is not
  stated.
* **Assumption.** Absence of `dl` is not systematically correlated with lateness.
  Metric 1 discards rows where `dl` is missing; if missingness rises with delay,
  the percentiles are optimistic.
* **Assumption.** The nested member is reachable as `journey_start.ordinal`. If
  the input serialization presents the record differently, substitute
  `GetRecordPropertyValue(journey_start, 'ordinal')`.
* **Assumption.** A 5-minute tumbling window and the 0.9 percentile are
  operational choices. Nothing in the two files sets a reporting cadence or a
  tail quantile.
* **Assumption.** The two 5-minute tumbling windows in `veh_win` and `route_win`
  are aligned to the same boundaries, so `DATEDIFF(second, v, r) BETWEEN 0 AND 0`
  matches the corresponding pair of window ends.
* **Assumption.** `route` and `dir` do not change within a trip, so grouping the
  vehicle-level metrics by trip key also fixes the route and direction carried on
  the output row.
* **Assumption about the dialect, not the domain.** The
  `PERCENTILE_CONT(p) OVER (PARTITION BY ... ORDER BY ...)` form used inside a
  windowed `GROUP BY` is supported as written; the fallback is noted in the
  comment on `route_win`.
