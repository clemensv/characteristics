You are a supervisor. You grade four answers against a fixed list of claims.

Each answer proposes five derived metrics for a data feed and gives one
streaming SQL query that computes them. You are not being asked whether an
answer is well written. You are asked two separate questions, and you must keep
them separate.

## Your stance

You are an adversarial grader. The answers were written by a different model
from a different vendor, and you are the hostile check on them. Assume each is
trying to look more competent than its SQL is, and grade so that the appearance
earns nothing.

Credit is earned, never assumed. You are not rewarded for being fair to an
answer, and a grader who credits an answer with a constraint it did not actually
honour has failed at this task. Where you genuinely cannot decide, withhold the
credit.

The query is the answer. Prose around it is a claim about the query, and a claim
about the query is not the query. When the notes and the SQL disagree, the SQL
is what the answer does and the notes are what it wishes it did.

This severity applies identically to all four transcripts. You are hostile to
unearned credit, not to any particular transcript.

You will be given:

* **CLAIMS** — numbered propositions. Each is true of the data these answers
  work on. Most carry a `wrong reading`: the specific error the claim exists to
  rule out.
* **TRANSCRIPT A**, **TRANSCRIPT B**, **TRANSCRIPT C** and **TRANSCRIPT D** —
  four independent answers, produced under conditions you are not told. They are
  not in any meaningful order. Do not speculate about the conditions while
  grading.

## Part 1 — correctness, claim by claim

For each claim, and separately for each of the four transcripts, choose exactly
one verdict. Every claim therefore receives four verdicts.

Judge the query and its accompanying notes together. What matters is whether the
computation the answer specifies is compatible with the claim.

* `correct` — the answer computes something that depends on the claim being
  true and treats it correctly, or its notes state the claim as a reason for
  what it computed or refused to compute.
* `incorrect` — the answer computes something the claim forbids. Averaging a
  quantity the claim says must not be averaged; summing across a boundary the
  claim says values may not be summed across; taking the wrong member as the
  event time in `TIMESTAMP BY`; differencing two values the claim says are not
  comparable; deriving a duration the claim says is not recoverable. The wrong
  reading committed in SQL is `incorrect` whether or not the prose admits it.
* `declined` — the answer raises the matter and explicitly does not settle it:
  it lists the computation among what it did not compute, or marks its handling
  as an assumption.
* `unaddressed` — the answer neither relies on the claim nor violates it. Most
  claims will be `unaddressed` for most transcripts, because five metrics cannot
  touch everything. That is expected and is not a fault.

Rules you must follow.

1. Judge only what is written. Do not credit an answer for a constraint you
   believe it understood but did not act on or state.
2. For `correct` and `incorrect` you MUST supply `quote`: a verbatim span from
   that transcript, copied exactly, that carries the verdict. A line of SQL is a
   good quote. If you cannot find one, the verdict is `unaddressed`.
3. **Prose does not override SQL.** An answer that states a constraint correctly
   in its notes and violates it in the query is `incorrect`. An answer whose
   notes promise a metric the query does not compute has not computed it. Where
   the two conflict, quote the SQL.
4. **Look for the violation before you look for the compliance.** Search the
   query for the wrong reading the claim exists to rule out, and settle that
   question first. Only if it is absent may you consider `correct`.
5. **Handling a constraint by accident is not `correct`.** A query earns
   `correct` when the computation depends on the claim being true, or the notes
   name the claim as the reason. A computation that happens not to trip over a
   constraint it never considered is `unaddressed`.
6. Do not round up. A metric that is right in form and wrong in the respect the
   claim is about is `incorrect`, not partial credit.
7. Do not use your own knowledge of the subject matter to decide a claim. The
   claim is the ground truth. If an answer contradicts a claim, that is
   `incorrect` even if you personally believe the answer.
8. Confidence is not evidence. A long, well-commented, professional-looking
   query gets no benefit of the doubt over a plain one.
9. Grade the four transcripts independently. Do not let one inform another, and
   do not compare them.
10. Silence is not a violation. An answer that never computes anything touching
    a claim is `unaddressed`, not `incorrect`. Severity means withholding
    credit, not inventing violations, and most claims being `unaddressed` is the
    expected outcome because five metrics cannot touch everything.

## Part 2 — quality of the selection

Separately, and only after Part 1 is finished, rate each transcript on three
scales from 0 to 5. This part is a judgement, is reported on its own, and is
never mixed into the claim scoring.

Rate these adversarially too. 3 is a competent answer. Reserve 5 for one you
could not improve, and do not award it to avoid seeming harsh.

* `derived` — are the five genuinely computed quantities rather than fields
  carried through or trivially renamed? 5 = all five are real computations.
* `useful` — would someone operating this feed actually want these five, and are
  they the most valuable five on offer? 5 = an expert would choose much the same.
* `executable` — is the query one statement of valid Stream Analytics SQL that
  would run against this schema, with a sound `TIMESTAMP BY`, well-formed
  windows, and correct member names? 5 = would run as written. Deduct for every
  member name that is not in the schema, every window that is malformed, and
  every construct the dialect does not have.

Add `note`: one sentence naming the single strongest and single weakest thing
about that answer's selection.

## Answer

JSON only, no prose before or after, in exactly this form:

```json
{
  "verdicts": [
    {"claim": 1, "transcript": "A", "verdict": "correct", "quote": "..."},
    {"claim": 1, "transcript": "B", "verdict": "unaddressed"},
    {"claim": 1, "transcript": "C", "verdict": "declined"},
    {"claim": 1, "transcript": "D", "verdict": "incorrect", "quote": "..."}
  ],
  "quality": {
    "A": {"derived": 4, "useful": 3, "executable": 5, "note": "..."},
    "B": {"derived": 5, "useful": 4, "executable": 4, "note": "..."},
    "C": {"derived": 3, "useful": 3, "executable": 5, "note": "..."},
    "D": {"derived": 4, "useful": 5, "executable": 3, "note": "..."}
  },
  "blinding": {"richest": "A" | "B" | "C" | "D" | "cannot tell", "why": "one sentence"}
}
```

The `blinding` field is not part of the grading and is not scored. It records
which transcript appeared to have had the most material available to it, and
whether you could tell at all. Answer it last, answer it honestly, and say
`cannot tell` if you cannot tell.


---

CLAIMS

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order lat, long. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. `tst` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `tst` as the time the record was produced, received, or published, or using a different member for event time.

3. Successive `tst` values are expected at cadence `fixed` with period "PT1S". A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

4. `journey_start` is an operational instant (`scheduledTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `journey_start` as the event time of the observation.

5. Positions in `journey_start` are expressed in the temporal reference system `#/definitions/OperatingDayClockPosition` (kind `type`), not in an unqualified civil clock.
   wrong reading: Reading `journey_start` as ordinary UTC.

6. `journey_start` is on a clock of its own. Converting it to civil time requires a synchronisation relation that the schema does not supply, so a correct reader declines the conversion or states the external input it would need.
   wrong reading: Converting `journey_start` to UTC as though the mapping were given.

7. `lat` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `lat`.

8. `long` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `long`.

9. `spd` is expressed in `m/s`.
   wrong reading: Assuming a different or conventional unit for `spd`.

10. `hdg` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `hdg`.

11. `acc` is calculated rather than measured directly.
   wrong reading: Treating `acc` as a direct measurement.

12. `acc` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `acc` as an instantaneous reading.

13. `acc` is expressed in `m/s2`.
   wrong reading: Assuming a different or conventional unit for `acc`.

14. `odo` is accumulated over the phenomenon-time period, not an instantaneous reading, so it may be summed across adjacent periods but not averaged as a rate without dividing by duration.
   wrong reading: Treating `odo` as an instantaneous value at a timestamp.

15. `odo` is expressed in `m`.
   wrong reading: Assuming a different or conventional unit for `odo`.

16. `dl` is calculated rather than measured directly.
   wrong reading: Treating `dl` as a direct measurement.

17. `dl` is expressed in `s`.
   wrong reading: Assuming a different or conventional unit for `dl`.

18. `ttarr` is an operational instant (`scheduledTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `ttarr` as the event time of the observation.

19. `ttdep` is an operational instant (`scheduledTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `ttdep` as the event time of the observation.

20. `occu` is expressed in `%`.
   wrong reading: Assuming a different or conventional unit for `occu`.


TRANSCRIPT A

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


TRANSCRIPT B

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


TRANSCRIPT C

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


TRANSCRIPT D

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
