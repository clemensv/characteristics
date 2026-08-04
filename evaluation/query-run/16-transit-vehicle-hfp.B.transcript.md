# HSL HFP `vp` — five derived metrics

## 1. The five metrics

1. **Delay drift rate** (`delay_drift_s_per_s`) — seconds of lateness accrued per second of running, per vehicle-run per window, computed as the change in `dl` between successive messages divided by the elapsed time between them, with the sign flipped so that positive means *falling further behind*. `dl` alone says a vehicle is 95 s late; the drift says whether it is still losing time or clawing it back, and that is what decides whether to hold, short-turn or inject a vehicle. This is the single most actionable number the feed supports.
2. **Adherence residual against route peers** (`lateness_vs_route_s`, with `route_stdev_lateness_s` as its context) — the vehicle-run's mean lateness in the window minus the mean lateness of *all* vehicles on the same `route` and `dir` in the same window, plus the spread of that peer group. This separates "this vehicle has a problem" from "this corridor has a problem", which are two different interventions. The spread is the honest, feed-supported proxy for adherence dispersion across the route.
3. **Cadence ratio and worst gap** (`cadence_ratio`, `worst_gap_s`) — messages actually received divided by the number the schema's declared `PT1S` cadence on `tst` predicts over the same covered time, plus the longest observed inter-message interval. This is a residual against a reference the schema itself declares, and it gates every other number here: a vehicle silent for 90 s has produced *no* data, not good data. It also tells you whether sample-count statistics (metric 4) may stand in for time.
4. **Non-satellite position ratio** (`non_gps_sample_ratio`) — share of messages in the window whose `loc` is not `GPS`. The schema states plainly that `ODO`, `DR` and `MAN` positions are propagated or hand-entered rather than fixed, and that `loc` changes without warning between messages of the same trip. Any map-matching, ETA or geofence built on `lat`/`long` is worth exactly what this ratio says it is worth, and there is no other way to know.
5. **Doors-open time** (`doors_open_s`) — time-weighted seconds in the window with `drst = 1`. It is the portion of running time an operator can actually manage. Read alongside metric 1 it distinguishes a boarding problem (drift up, doors-open time up) from a traffic problem (drift up, doors-open time flat).

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
-- Input : hfp     (HSL HFP `vp` events)
-- Output: output
--
-- Grain of the output: one row per vehicle-run per 5-minute tumbling window,
-- carrying its own four per-vehicle metrics plus its residual against the
-- route+direction peer group aggregated over the same 5-minute window.

WITH

-- ---------------------------------------------------------------------------
-- keyed
--   Event time is declared once, on `tst`: it is the phenomenonTime the vehicle
--   itself sampled. `ttarr` / `ttdep` are scheduledTime -- planned, not
--   observed -- and are not candidates. `journey_start` is a position in the
--   operating-day regime, explicitly not an RFC 3339 civil instant, so
--   `journey_start.ordinal` is used here only as an opaque identity token: it
--   is never parsed, and never compared with `tst`.
--   `dl` is sign-inverted here, once, at the boundary: the feed makes it
--   negative when late, so `lateness_s` is positive when late.
-- ---------------------------------------------------------------------------
keyed AS (
    SELECT
        CONCAT(CAST(oper AS nvarchar(max)), ':', CAST(veh AS nvarchar(max)),
               ':', journey_start.ordinal)                      AS trip_key,
        journey_start.ordinal                                   AS trip_ordinal,
        oper,
        veh,
        desi,
        route,
        dir,
        tst,
        loc,
        drst,
        (-1) * dl                                               AS lateness_s
    FROM hfp TIMESTAMP BY tst
),

-- ---------------------------------------------------------------------------
-- paired
--   Each sample is paired with its predecessor on the same vehicle-run, so that
--   the interval it closes is known. LAG is partitioned by trip_key, so no pair
--   ever straddles a trip boundary (where `dl` re-anchors on a new
--   `journey_start`). LIMIT DURATION(minute, 10) is the required bound.
--   gap_s is taken in milliseconds and scaled, because `tst` carries
--   millisecond precision and the declared cadence is only 1 s -- second-
--   resolution differencing would quantise away most of the jitter.
-- ---------------------------------------------------------------------------
paired AS (
    SELECT
        trip_key, trip_ordinal, oper, veh, desi, route, dir,
        tst, loc, drst, lateness_s,

        DATEDIFF(millisecond,
                 LAG(tst, 1) OVER (PARTITION BY trip_key
                                   LIMIT DURATION(minute, 10)),
                 tst) / 1000.0                                  AS gap_s,

        lateness_s
          - LAG(lateness_s, 1) OVER (PARTITION BY trip_key
                                     LIMIT DURATION(minute, 10)) AS d_lateness_s
    FROM keyed
),

-- ---------------------------------------------------------------------------
-- trip_5min
--   Window: TumblingWindow(minute, 5). Partition: the vehicle-run (trip_key).
--   Metrics 1, 3, 4, 5 are computed here.
-- ---------------------------------------------------------------------------
trip_5min AS (
    SELECT
        System.Timestamp()                                      AS window_end,
        trip_key, trip_ordinal, oper, veh, desi, route, dir,

        COUNT(*)                                                AS samples,

        -- METRIC 1 -- delay drift: total lateness accrued over the window
        -- divided by the elapsed running time it was accrued over. Both sums
        -- are restricted to samples that actually have a predecessor and a
        -- `dl`, so numerator and denominator cover the same intervals.
        SUM(CASE WHEN d_lateness_s IS NOT NULL THEN d_lateness_s ELSE 0 END)
          / NULLIF(SUM(CASE WHEN d_lateness_s IS NOT NULL
                            THEN gap_s ELSE 0 END), 0)          AS delay_drift_s_per_s,

        -- METRIC 3 -- residual against the declared PT1S cadence on `tst`.
        -- Expected message count over the covered time is SUM(gap_s) / 1 s;
        -- cadence_ratio = 1.0 means on cadence, 0.5 means half the messages
        -- the schema says to expect. No threshold is invented.
        SUM(CASE WHEN gap_s IS NOT NULL THEN 1 ELSE 0 END)
          / NULLIF(SUM(gap_s), 0)                               AS cadence_ratio,
        MAX(gap_s)                                              AS worst_gap_s,
        MAX(gap_s) - 1.0                                        AS worst_cadence_residual_s,

        -- METRIC 4 -- share of samples whose position was not satellite-fixed.
        -- Sample-weighted, not time-weighted; cadence_ratio above says how far
        -- those two readings may diverge.
        SUM(CASE WHEN loc <> 'GPS' THEN 1.0 ELSE 0.0 END)
          / COUNT(*)                                            AS non_gps_sample_ratio,

        -- METRIC 5 -- time-weighted doors-open seconds. Each interval is
        -- attributed to the door state observed at its closing sample.
        SUM(CASE WHEN drst = 1 AND gap_s IS NOT NULL
                 THEN gap_s ELSE 0 END)                         AS doors_open_s,

        -- input to metric 2
        AVG(lateness_s)                                         AS trip_mean_lateness_s
    FROM paired
    GROUP BY
        trip_key, trip_ordinal, oper, veh, desi, route, dir,
        TumblingWindow(minute, 5)
),

-- ---------------------------------------------------------------------------
-- route_5min
--   Window: TumblingWindow(minute, 5), the same size and alignment as above.
--   Partition: route + direction, across all vehicles. This is the peer
--   reference for metric 2.
-- ---------------------------------------------------------------------------
route_5min AS (
    SELECT
        System.Timestamp()                                      AS window_end,
        route,
        dir,
        AVG(lateness_s)                                         AS route_mean_lateness_s,
        STDEV(lateness_s)                                       AS route_stdev_lateness_s,
        COUNT(*)                                                AS route_samples
    FROM paired
    GROUP BY route, dir, TumblingWindow(minute, 5)
)

SELECT
    t.window_end,
    t.oper,
    t.veh,
    t.trip_ordinal,
    t.desi,
    t.route,
    t.dir,
    t.samples,

    -- 1
    t.delay_drift_s_per_s,
    -- 2
    t.trip_mean_lateness_s - r.route_mean_lateness_s            AS lateness_vs_route_s,
    r.route_stdev_lateness_s,
    r.route_samples,
    -- 3
    t.cadence_ratio,
    t.worst_gap_s,
    t.worst_cadence_residual_s,
    -- 4
    t.non_gps_sample_ratio,
    -- 5
    t.doors_open_s
INTO output
FROM trip_5min t
LEFT OUTER JOIN route_5min r
    ON  t.route = r.route
    AND t.dir   = r.dir
    -- Both sides are emitted at the end of the same 5-minute tumbling window,
    -- so their event times coincide. The DATEDIFF bound is required on every
    -- ASA join. I am reasonably but not fully certain that joining two
    -- windowed CTEs this way is accepted; if it is not, split into two
    -- statements writing to two outputs and join downstream.
    AND DATEDIFF(minute, t, r) BETWEEN 0 AND 0
```

## 3. What I did not compute

* **Anything over `occu`.** The schema says only Suomenlinna ferries report a measured value and every other vehicle class transmits a constant, and that a consumer must know the transport mode first. No member of this record carries transport mode: `desi` is a head-sign display label and `route` is an opaque GTFS identifier, and neither file establishes how to map either to a mode. Any average, percentile or trend over `occu` would silently blend a measurement with a constant.
* **Distance, ground speed or geofencing from `lat` / `long`.** Converting two coordinate pairs into a distance needs a geodesic formula and an ellipsoid constant. The files declare the CRS (EPSG:4326) but supply neither, so I would be importing them. Worse, `lat` and `long` are optional and, when `loc` is `ODO`, `DR` or `MAN`, are propagated or hand-entered rather than fixed, so a distance computed across them would be partly fabricated. Metric 4 measures that exposure instead of hiding it.
* **Aggregates over `acc` — mean acceleration, harsh-braking counts.** The schema states `acc` is not measured, is derived from two speed samples, inherits the noise of both, is undefined for the first message of a trip, and characterises an interval whose opening boundary the record does not carry and whose length varies. Summing or averaging quantities whose support periods differ per sample is unsound, and any harsh-braking threshold would be a number neither file states. Where I needed a rate of change (metric 1) I built it from `LAG` myself, where I know exactly which interval it spans.
* **Turn rate or heading dispersion from `hdg`.** The declared range is `0`–`360` inclusive, which makes 0 and 360 both admissible for the same bearing; nothing in the files says how the wrap is to be handled, and nothing says whether `hdg` is meaningful while `spd` is 0. Circular statistics on an ambiguously-bounded member would look precise and be wrong.
* **Distance or average speed from `odo`.** `odo` is monotone only within one actual trip run, and the counter resets when the vehicle *actually* begins the trip — an instant the record does not carry. `journey_start` is the *scheduled* departure, and `dl` exists precisely because the two differ. So a window that straddles the reset would produce a negative or nonsensical `MAX(odo) - MIN(odo)`, and I cannot detect the straddle from the record. Partitioning by `journey_start.ordinal` does not fix this, because the reset falls inside that partition.
* **Stop-level arrival or departure lateness from `ttarr` / `ttdep` against `tst`.** On a `vp` event, `stop` names the stop the vehicle *most recently departed from*, so I cannot identify the arrival or departure instant from `vp` messages alone. Any such figure would also duplicate `dl`, which is already computed onboard against the same schedule, and the two would disagree without me being able to say which is right.
* **Per-stop dwell attribution.** Metric 5 is doors-open time per vehicle-run per window, not per stop, for the reason above: `stop` refers backwards, so binding a doors-open interval to a specific stop identifier is not licensed by the files.
* **On-time performance percentage.** Reporting "X% on time" requires an on-time threshold in seconds. Neither file states one, and the sign convention on `dl` is the only thing the files establish about its interpretation. Metrics 1 and 2 use `dl` without needing a threshold.
* **`PERCENTILE_CONT` median and P90 of lateness.** I wanted these for metric 2 — they are more robust than mean and standard deviation. In this dialect `PERCENTILE_CONT` is an `OVER`-clause analytic returning a per-row value, and I am not confident it composes with a `GROUP BY ... TumblingWindow`. `AVG` and `STDEV` are unambiguously available as aggregates, so I used those and accepted the loss of robustness rather than ship syntax I cannot verify.
* **`COUNT(DISTINCT trip_key)` on the route aggregate.** It would have told an operator how many vehicles the route reference in metric 2 rests on, which matters. I used `COUNT(*)` of samples instead because I am unsure `COUNT(DISTINCT ...)` is supported inside a windowed aggregate here.

## 4. Assumptions

* **A1 — trip identity.** I key a vehicle-run as `oper : veh : journey_start.ordinal`. The schema says the `oper`/`veh` pair identifies the physical vehicle, and that `journey_start` identifies the trip; it does **not** say that `journey_start` alone is unique across routes, so I include the vehicle to guarantee per-vehicle continuity for `LAG`. *Assumption:* that no single vehicle serves two distinct trips with the same `journey_start.ordinal` inside one window.
* **A2 — interval attribution for door state.** Metric 5 attributes the whole interval `(previous tst, tst]` to the value of `drst` observed at `tst`. *Assumption:* the door state held for that interval. The files give `drst` as a state at an instant only.
* **A3 — `drst` absence.** The schema says `drst` is absent when the onboard system cannot determine it. Those samples contribute 0 to `doors_open_s`, i.e. they are treated as "not known to be open", not as "closed". *Assumption:* that under-counting is preferable to imputing; a vehicle with sparse `drst` will read as having low doors-open time.
* **A4 — gaps longer than the LAG bound are invisible.** `LIMIT DURATION(minute, 10)` makes `LAG` return NULL when the previous message is more than ten minutes back, so `worst_gap_s` cannot exceed ~600 s and a truly long silence is reported as *fewer paired samples* rather than as a large gap. *Assumption:* ten minutes is a reasonable ceiling; the files declare only the `PT1S` cadence and say nothing about outage length.
* **A5 — window sizes.** The 5-minute tumbling window is an operational choice, not a fact from the files. The only timing the schema declares is the `PT1S` cadence on `tst`, which sets the *lower* bound of meaningful aggregation, not this one. *Assumption.*
* **A6 — non-`GPS` grouping.** Metric 4 groups `ODO`, `DR`, `MAN` and `N/A` together as "not satellite-fixed". The `altenums` descriptions license reading `ODO`/`DR`/`MAN` this way; `N/A` means the system could not determine the method, which is not the same thing, and I fold it in as a conservative choice. *Assumption.*
* **A7 — `dl` presence.** `dl` is not in the schema's `required` list, so it may be absent. Metric 1 excludes intervals where it is, on both sides of the ratio. Metric 2's `AVG`/`STDEV` skip NULLs. *Assumption:* `dl` is absent rarely enough that the surviving samples are representative; if it is systematically absent for some vehicles, metrics 1 and 2 are quietly computed over a biased subset.
* **A8 — `route` and `dir` are stable within a vehicle-run.** They appear in the `GROUP BY` of `trip_5min`. If a vehicle changes either mid-window it will emit two rows for that window. *Assumption:* this is acceptable rather than an error to be masked.
* **A9 — event ordering.** `TIMESTAMP BY tst` means `LAG` sees events in `tst` order, subject to the job's late-arrival and out-of-order policies, which are configured outside the query. Sub-second reordering would corrupt `gap_s` and `d_lateness_s`. *Assumption:* those policies are set appropriately for a ~1 Hz mobile feed.
* **A10 — dialect details I could not verify.** Multi-argument `CONCAT`; `CAST(... AS nvarchar(max))`; dotted access to `journey_start.ordinal`; `LEFT OUTER JOIN` between two windowed CTEs with `DATEDIFF(minute, t, r) BETWEEN 0 AND 0` to align identical tumbling windows. Each is a standard shape in this dialect, but I have no specification to check against. *Assumptions*, flagged in comments at the point of use.
* **A11 — input and output names.** The stream is named `hfp` and the sink `output`. Neither file states either. *Assumption.*
