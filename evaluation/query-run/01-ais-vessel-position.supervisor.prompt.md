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

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order Latitude, Longitude. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. `TimeReceived` is an operational instant (`ingestionTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `TimeReceived` as the event time of the observation.

3. `Timestamp` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `Timestamp` as the time the record was produced, received, or published, or using a different member for event time.

4. Successive `Timestamp` values are expected at cadence `irregular`. A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

5. `Valid` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `Valid` as an observed quantity.

6. `Latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `Latitude`.

7. `Longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `Longitude`.

8. `PositionAccuracy` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `PositionAccuracy` as an observed quantity.

9. `Raim` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `Raim` as an observed quantity.

10. `Sog` is expressed in `[kn_i]`.
   wrong reading: Assuming a different or conventional unit for `Sog`.

11. `Cog` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `Cog`.

12. `TrueHeading` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `TrueHeading`.


TRANSCRIPT A

# Five derived metrics over the Class B position report stream

## 1. The five metrics

Ordered most valuable first. All five are computed per `UserID`, which the schema
marks `semanticRole: featureOfInterest` — the individual source.

1. **Reporting gap** — seconds between consecutive receipts from the same MMSI
   (max and mean over the window). The schema declares the cadence `irregular`,
   so an operator cannot assume a fixed interval; the gap series is the only way
   to tell "this station is reporting" from "this station has gone quiet", which
   is the first question anyone asks of a position feed. Silence is also the
   failure mode that no field in the record announces.

2. **Unusable-fix fraction** — share of reports in the window that are not a
   usable position fix: `Valid = false` (decoder failure), or `Timestamp` in
   60–63 (fix time unavailable / manual entry / dead reckoning / positioning
   system inoperative), or `Latitude`/`Longitude` at their 91 / 181 sentinels.
   This tells the operator what proportion of the positions being consumed are
   real fixes rather than sentinel or dead-reckoned output — the difference
   between a track and a guess. It is licensed entirely by the three
   `resultQuality` members and the `phenomenonTime` sentinel list.

3. **Fix-to-receipt lag** — seconds between the position fix and the ingest
   receipt (mean and max), obtained as the second-of-minute of `TimeReceived`
   minus `Timestamp`, wrapped into 0–59. The schema states outright that
   `TimeReceived` "follows the position fix by the propagation and queueing
   delay of the terrestrial receiver network" and that the enclosing minute of
   the fix is recovered from the receipt time, so this residual is a direct
   measurement of receiver-network health and of how stale a displayed position
   is. Rising lag degrades every downstream consumer silently.

4. **Drift angle** — circular absolute difference between `TrueHeading` and
   `Cog`, in degrees, evaluated only while the station reports non-zero `Sog`.
   Both members are declared in degrees true, so the difference is a residual
   between where the hull points and where the station is actually going. A
   persistent non-zero value is the signature of set-and-drift or of a compass
   disagreeing with the position-fixing system; either is something an operator
   wants raised.

5. **Course turn rate** — signed circular change in `Cog` divided by the elapsed
   receipt interval, reported as the largest absolute value in the window
   (deg/s). The record carries no turn-rate member at all, so this is the only
   available manoeuvre indicator; it separates a station holding a lane from one
   altering course.

`ReportCount` also appears in the output. It is the sample size behind the
fractions and statistics above, not a sixth metric.

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
-- Input alias: input.  Output sink: output.
WITH

-- Screen every "not available" encoding the schema names, so that no aggregate
-- downstream can average a sentinel into a real value.
Clean AS
(
    SELECT
        UserID,
        TimeReceived,
        DATEPART(second, TimeReceived)                             AS RecvSecond,
        CASE WHEN Timestamp BETWEEN 0 AND 59 THEN Timestamp END    AS FixSecond,
        CASE WHEN Sog < 102.3            THEN Sog END              AS SogKn,
        CASE WHEN Cog < 360.0            THEN Cog END              AS CogDeg,
        CASE WHEN TrueHeading <= 359     THEN TrueHeading * 1.0 END AS HdgDeg,
        -- A report is a usable fix only if the decoder succeeded, the
        -- position-fixing system produced a real second-of-minute (not
        -- 60 unavailable / 61 manual / 62 dead-reckoning / 63 inoperative),
        -- and neither coordinate sits on its "not available" sentinel.
        -- NOTE: boolean members are compared to 1 here; if the JSON boolean is
        -- surfaced as a string this needs to be = 'true'. I cannot verify which.
        CASE
            WHEN Valid = 1
             AND Timestamp BETWEEN 0 AND 59
             AND Latitude  BETWEEN  -90.0 AND  90.0
             AND Longitude BETWEEN -180.0 AND 180.0
            THEN 0 ELSE 1
        END                                                        AS IsUnusableFix
    FROM input
    TIMESTAMP BY TimeReceived   -- the only full datetime member in the record
),

-- Reach the previous report of the same station. LIMIT DURATION is required;
-- 30 minutes bounds the longest silence this query can measure.
Prev AS
(
    SELECT
        UserID, TimeReceived, RecvSecond, FixSecond,
        SogKn, CogDeg, HdgDeg, IsUnusableFix,
        DATEDIFF(second,
                 LAG(TimeReceived, 1) OVER (PARTITION BY UserID
                                            LIMIT DURATION(minute, 30)),
                 TimeReceived)                                     AS GapSeconds,
        LAG(CogDeg, 1) OVER (PARTITION BY UserID
                             LIMIT DURATION(minute, 30))           AS PrevCogDeg
    FROM Clean
),

-- Per-event derivations. FLOOR is used instead of the % operator so that the
-- circular arithmetic is well defined on doubles; I am relying on FLOOR and
-- DATEPART being available.
Derived AS
(
    SELECT
        UserID,
        GapSeconds,                                   -- metric 1, per event
        IsUnusableFix,                                -- metric 2, per event

        -- metric 3: seconds from fix to receipt, wrapped into 0..59
        CASE WHEN FixSecond IS NOT NULL
             THEN (RecvSecond - FixSecond)
                  - 60.0 * FLOOR((RecvSecond - FixSecond) / 60.0)
        END                                                        AS ReceiveLagSec,

        -- metric 4: |heading - course| as a circular difference in [0,180]
        CASE WHEN HdgDeg IS NOT NULL AND CogDeg IS NOT NULL AND SogKn > 0.0
             THEN ABS( ((HdgDeg - CogDeg + 180.0)
                        - 360.0 * FLOOR((HdgDeg - CogDeg + 180.0) / 360.0))
                       - 180.0 )
        END                                                        AS DriftAngleDeg,

        -- metric 5: signed course change per second, circular difference / dt
        CASE WHEN CogDeg IS NOT NULL AND PrevCogDeg IS NOT NULL
              AND SogKn > 0.0 AND GapSeconds > 0
             THEN ( ((CogDeg - PrevCogDeg + 180.0)
                     - 360.0 * FLOOR((CogDeg - PrevCogDeg + 180.0) / 360.0))
                    - 180.0 )
                  / GapSeconds
        END                                                        AS TurnRateDegPerSec
    FROM Prev
)

SELECT
    UserID,
    System.Timestamp()                AS WindowEnd,
    COUNT(*)                          AS ReportCount,
    MAX(GapSeconds)                   AS M1_MaxReportGapSec,
    AVG(GapSeconds * 1.0)             AS M1_AvgReportGapSec,
    AVG(IsUnusableFix * 1.0)          AS M2_UnusableFixFraction,
    AVG(ReceiveLagSec)                AS M3_AvgReceiveLagSec,
    MAX(ReceiveLagSec)                AS M3_MaxReceiveLagSec,
    AVG(DriftAngleDeg)                AS M4_AvgDriftAngleDeg,
    MAX(DriftAngleDeg)                AS M4_MaxDriftAngleDeg,
    MAX(ABS(TurnRateDegPerSec))       AS M5_MaxAbsTurnRateDegPerSec
INTO output
FROM Derived
-- Tumbling window, 5 minutes, partitioned by the transmitting station.
GROUP BY UserID, TumblingWindow(minute, 5)
```

Event time: `TIMESTAMP BY TimeReceived`, and no other member. `Timestamp` is an
`int32` second-of-minute with four sentinel values, not a point in time, so it
cannot serve as the event time even though it is the `phenomenonTime`.

Windows: one `TumblingWindow(minute, 5)`, partitioned by `UserID`. `LAG` uses
`LIMIT DURATION(minute, 30)`.

## 3. What I did not compute

* **Great-circle distance between successive `Latitude`/`Longitude` pairs, and
  the implied speed compared against `Sog`.** This is the metric I most wanted:
  the residual between distance-derived speed and reported `Sog` is a strong
  integrity signal. I left it out because the files give me a CRS binding
  (EPSG:4326 over `Latitude`, `Longitude`) but no ellipsoid parameters, no earth
  radius, and no distance contract. Writing a haversine would mean importing a
  constant the two files do not establish, and the correctness of the metric
  would rest entirely on that import. `ST_DISTANCE` may exist in this dialect,
  but I would then be assuming its datum handling as well.

* **Anything combining two different `UserID` values** — traffic density in a
  geographic cell, count of distinct stations in an area, closest-point-of-
  approach between two stations. All require the distance model above plus a
  grid or a self-join of the stream; neither file licenses either.

* **Aggregates across `UserID`** — for example a mean `Sog` over all stations in
  the window. `UserID` is the `featureOfInterest`; averaging a measured quantity
  across distinct features of interest produces a number with no referent. Every
  aggregate above is partitioned by `UserID`.

* **Speed change rate**, `(Sog - LAG(Sog)) / GapSeconds`. This was the sixth
  candidate and is sound. It was dropped to stay at five: it and the `Cog` turn
  rate both describe manoeuvre, and turn rate was preferred because the record
  contains no turn-rate member at all, whereas the `Sog` series is itself
  carried and its changes are directly visible to an operator.

* **Per-window dispersion of `Sog`** (`STDEV`, `PERCENTILE_CONT`). Computable,
  but I could not say what it means here beyond "the speed varied", and the
  files do not license reading speed variance as sea state, load, or anything
  else.

* **Transition counts on `AssignedMode` and `ClassBUnit`.** A change in
  `AssignedMode` (autonomous to base-station-controlled) would be a genuine
  derived event, and `ClassBUnit` governs the transmission schedule, so a flip
  in either would change the expected cadence. I left both out because nothing
  in the two files establishes that these flags change within a session, and
  emitting a transition counter implies an event I cannot show exists.

* **Anything from `ClassBDisplay`, `ClassBDsc`, `ClassBBand`, `ClassBMsg22`.**
  These are equipment capability flags, carry no `semanticRole`, and describe
  the unit rather than the observation. Counting or averaging them yields an
  attribute of the hardware, not a metric of the stream.

* **`PositionAccuracy` and `Raim` folded into metric 2.** Both are
  `resultQuality`, but they state an accuracy tier (better or worse than 10 m)
  and whether integrity monitoring is switched on — not whether the report is
  usable. Mixing a tier flag into a validity fraction would produce a number
  that answers neither question. They could each carry their own per-window
  fraction; that would have been padding.

* **Reconstructing an absolute fix time from `Timestamp` plus the minute of
  `TimeReceived`, and using it as the event time.** The reconstruction is
  ambiguous whenever the receive lag crosses a minute boundary, and it is
  undefined for `Timestamp` 60–63. I use the reconstruction only as a lag
  residual (metric 3), where the ambiguity is the metric's known limit, and
  never as a timestamp.

## 4. Assumptions

Each of the following is an assumption; none is established by the schema or the
instance.

* **Assumption:** `TimeReceived` is acceptable as event time. Every window is
  therefore in receiver-network time, not fix time, and is skewed by the
  propagation and queueing delay the schema describes. This is sound only if
  that delay is small relative to the 5-minute window.
* **Assumption:** the fix-to-receipt lag is under 60 seconds. `Timestamp` is a
  second-of-minute only, so metric 3 measures lag modulo 60 and aliases silently
  if the true lag is a minute or more.
* **Assumption:** `Cog`, and therefore the drift angle and the turn rate, are
  meaningful only while the station is moving. I gate metrics 4 and 5 on
  `Sog > 0`. The files do not state that course over ground is undefined at zero
  speed over ground; the specific gate value of 0 is mine.
* **Assumption:** 30 minutes is long enough for `LIMIT DURATION`. The declared
  cadence is `irregular` and no expected interval is given, so silences longer
  than 30 minutes are not measured at all — `GapSeconds` simply becomes null and
  the station looks like a fresh partition.
* **Assumption:** the 5-minute tumbling window is an appropriate aggregation
  size. Nothing in the files implies a natural period.
* **Assumption:** values at or beyond the stated sentinels (`Sog` 102.3, `Cog`
  360, `TrueHeading` 511, `Timestamp` 60–63, `Latitude` 91, `Longitude` 181)
  mean "not available" and no other out-of-range encoding exists.
* **Assumption:** boolean members compare correctly against `1`. If the JSON
  booleans surface as strings, `Valid = 1` must become `Valid = 'true'`.
* **Assumption:** `FLOOR`, `ABS`, `DATEPART(second, ...)` and `LAG` over a
  `datetime` column are supported in this dialect. I avoided the `%` operator on
  doubles because I could not confirm it.
* **Assumption:** `UserID` identifies one station stably for the duration of a
  window, so partitioning by it groups one source.
* **Assumption:** aggregates ignore nulls in the usual SQL way, so events
  screened out by the sentinel logic drop out of the mean rather than
  contributing zero.
* **Assumption:** the input alias is `input` and a single sink named `output`
  exists.


TRANSCRIPT B

# StandardClassBPositionReport — five derived metrics

## Before the metrics: which member is the event time

The schema declares two temporal members and they carry different roles.

* `Timestamp` is `semanticRole: phenomenonTime` — the time the fix applies to.
  It is an `int32` second-of-minute, 0–59, with 60–63 as sentinels. It is not a
  temporal position on any axis; it cannot be given to `TIMESTAMP BY`.
* `TimeReceived` is `semanticRole: ingestionTime` — the time the aisstream.io
  ingest service accepted the record.

`TimeReceived` is therefore the only member `TIMESTAMP BY` can take. The
specification is explicit about what that costs: of `ingestionTime`,
`scheduledTime`, `actualTime` and the other operational roles it says "These
operational values describe the handling of the record. A processor MUST NOT
read any of them as `phenomenonTime`, `resultTime`, `observedProperty`,
`featureOfInterest`, or `observingProcedure`."

So every window below is a window of **arrival**, not of **occurrence**, and no
metric below divides anything by an interval measured on `TimeReceived` and
calls the result a rate of change of the world. That constraint is what
determines which five metrics are sound, and it is the reason several obvious
ones are in section 3 instead.

`UserID` is `semanticRole: featureOfInterest`, so it is what identifies an
individual source and it is the partition key.

---

## 1. The five metrics

Ordered by value to an operator of this feed. Grain of all five: one row per
`UserID` per five-minute tumbling window of receipt time.

1. **Usable-position fraction.** The share of a station's reports in the window
   that both decoded (`Valid` true) and carry an in-range position
   (`Latitude` ≠ 91, `Longitude` ≠ 181). This is the first thing an operator
   needs, because it bounds the trustworthiness of everything downstream: a
   station at 0.4 is not a station whose track you may plot. `Valid` is a
   `resultQuality` declaration and the position sentinels are stated in the
   `description` of `Latitude` and `Longitude`.

2. **Report interval, median and maximum.** Seconds between successive receipts
   for one `UserID`, summarised per window. This is the only continuity handle
   the feed offers — it tells you whether a station is still transmitting and
   how coarsely. It is reported and deliberately **not** thresholded; see
   section 3.

3. **Fix-to-receipt second offset, median.** The residual between the two
   declared time roles: the second-of-minute of `TimeReceived` minus
   `Timestamp`, taken modulo 60. It is the only cross-check the record permits
   between when the fix was generated and when the receiver network delivered
   it, and it is what tells you a terrestrial receiver has started to queue.

4. **Position-quality profile.** Two fractions over the window: reports with
   `PositionAccuracy` true (DGNSS-grade, better than 10 m) and reports with
   `Raim` true (integrity-monitored). These govern how tightly a consumer may
   use the position — a 10 m fix and a 30 m fix are not interchangeable inputs
   to a berth-occupancy or close-quarters calculation. Reported as two separate
   numbers, not combined; see section 3.

5. **Largest kinematic step.** The greatest absolute change in `Sog` between
   successive reports of one station in the window, and the greatest circular
   change in `Cog`. A step is a manoeuvre or a bad decode, and both are worth
   surfacing. This is a per-report **difference**, not a per-second rate,
   precisely because the available clock is ingest time.

`ReportsInWindow` is also emitted; it is the denominator of metrics 1 and 4 and
context for the rest, not a sixth metric.

---

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
-- Event time: TimeReceived (semanticRole: ingestionTime). See notes above.
-- Source identity: UserID (semanticRole: featureOfInterest).
-- Window: TumblingWindow(minute, 5) -- size is an assumption, see section 4.

WITH Decoded AS
(
    SELECT
        UserID,
        TimeReceived,

        -- 'Valid' is the decoder's resultQuality flag. Booleans are compared as
        -- bits here; if the runtime rejects "= 1", the form is "= 'true'".
        CASE WHEN Valid = 1 THEN 1 ELSE 0 END AS DecodeOk,

        -- Availability tests use the out-of-range encodings that the schema
        -- descriptions state: 91 / 181 for position, 102.3 for Sog, 360 for
        -- Cog, 60-63 for Timestamp. Written as inequalities rather than
        -- equality so that no float is compared for exact equality.
        CASE WHEN Latitude  BETWEEN  -90 AND  90
              AND Longitude BETWEEN -180 AND 180 THEN 1 ELSE 0 END AS PositionPresent,

        CASE WHEN Sog < 102.3 THEN Sog END AS SogKn,
        CASE WHEN Cog < 360   THEN Cog END AS CogDeg,
        CASE WHEN Timestamp BETWEEN 0 AND 59 THEN Timestamp END AS FixSecond,

        -- Two independent resultQuality flags, kept separate.
        CASE WHEN PositionAccuracy = 1 THEN 1 ELSE 0 END AS HighAccuracy,
        CASE WHEN Raim             = 1 THEN 1 ELSE 0 END AS RaimInUse
    FROM input
    TIMESTAMP BY TimeReceived
),

Stepped AS
(
    SELECT
        UserID,
        DecodeOk,
        PositionPresent,
        HighAccuracy,
        RaimInUse,

        -- Interval between successive receipts for one station.
        -- LIMIT DURATION is required by the dialect; 1 hour is a lookback bound,
        -- not a window, and is an assumption (section 4).
        DATEDIFF(second,
                 LAG(TimeReceived, 1)
                     OVER (PARTITION BY UserID LIMIT DURATION(hour, 1)),
                 TimeReceived) AS ReportIntervalSec,

        -- Per-report change in speed over ground. NULL when either report
        -- carried the 'not available' encoding, which drops it from MAX.
        ABS(SogKn - LAG(SogKn, 1)
                        OVER (PARTITION BY UserID LIMIT DURATION(hour, 1)))
            AS SogStepKn,

        -- Per-report change in course over ground, taken the short way round
        -- the circle. Cog is documented as 0-359.9, so it wraps.
        180 - ABS(ABS(CogDeg - LAG(CogDeg, 1)
                                   OVER (PARTITION BY UserID LIMIT DURATION(hour, 1)))
                  - 180)
            AS CogStepDeg,

        -- Second-of-minute residual between the fix (phenomenonTime) and the
        -- receipt (ingestionTime), modulo 60. Written as a CASE rather than a
        -- '%' operator, which I am not certain this dialect supports.
        CASE
            WHEN DATEPART(second, TimeReceived) >= FixSecond
                THEN DATEPART(second, TimeReceived) - FixSecond
            ELSE DATEPART(second, TimeReceived) - FixSecond + 60
        END AS FixToReceiptOffsetSec
    FROM Decoded
)

SELECT
    UserID,
    System.Timestamp() AS WindowEnd,
    COUNT(*)           AS ReportsInWindow,

    -- Metric 1: usable-position fraction
    SUM(CASE WHEN DecodeOk = 1 AND PositionPresent = 1 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*) AS UsablePositionFraction,

    -- Metric 2: report interval, median and worst case
    PERCENTILE_CONT(0.5)
        OVER (PARTITION BY UserID ORDER BY ReportIntervalSec)
        AS MedianReportIntervalSec,
    MAX(ReportIntervalSec) AS LongestReportIntervalSec,

    -- Metric 3: fix-to-receipt offset, median
    PERCENTILE_CONT(0.5)
        OVER (PARTITION BY UserID ORDER BY FixToReceiptOffsetSec)
        AS MedianFixToReceiptOffsetSec,

    -- Metric 4: position-quality profile, two separate fractions
    SUM(HighAccuracy) * 1.0 / COUNT(*) AS HighAccuracyFraction,
    SUM(RaimInUse)    * 1.0 / COUNT(*) AS RaimInUseFraction,

    -- Metric 5: largest kinematic step
    MAX(SogStepKn)  AS MaxSpeedStepKn,
    MAX(CogStepDeg) AS MaxCourseStepDeg

INTO output
FROM Stepped
GROUP BY UserID, TumblingWindow(minute, 5)
```

Window inventory, as required: one aggregation, `TumblingWindow(minute, 5)`,
partitioned by `UserID`. The `LIMIT DURATION(hour, 1)` clauses are the
dialect-mandated lookback bound on `LAG`, not windows.

---

## 3. What I did not compute

**Distance, over-ground track, or a speed derived from position.** Two reasons,
either sufficient. First, the divisor would have to be a `TimeReceived`
interval, and `TimeReceived` is `ingestionTime`; the specification forbids
reading an operational time role as `phenomenonTime`. Second, the
`coordinateReferenceSystem` annotation identifies EPSG:4326 and binds
`Latitude`, `Longitude` to its axes in that order, but the specification says
"This specification does not define a CRS, datum, coordinate operation, or
transformation" and that without a definition source a processor "MUST preserve
the declaration but treat those checks and coordinate transformations as
indeterminate". So no `ST_DISTANCE`, no great-circle leg length, and in
particular no dead-reckoning residual of position-derived speed against `Sog`.

**Rate of turn from `Cog`, or acceleration from `Sog`.** Same first reason. The
numerator is a change in a `phenomenonTime`-stamped observation value and the
only available denominator is an ingest-time interval. I compute the step and
stop there; a step in knots is a fact, a step in knots per second would be a
substitution the specification forbids.

**`Cog` minus `TrueHeading`.** This is the residual an AIS operator would reach
for first, and I left it out. Both members carry
`observedProperty: http://qudt.org/vocab/quantitykind/Angle`, and the
specification states that "quantity-kind classification" does not establish
equivalence and that "Only a reviewed `exactMatch` can provide evidence that two
distinct identifiers denote the same observable property". Neither member
carries a `vectorReferenceFrames` binding, so nothing in the annotation model
places them on a common angular datum; the words "degrees true" appear only in
their `description`, and a binding "MUST NOT be repaired from property names,
descriptions, labels, or samples". Subtracting them would be an arithmetic
operation the schema does not license.

**An absolute phenomenon time reconstructed from `Timestamp`.** The description
of `Timestamp` says "the enclosing minute is recovered from the receipt time".
That is a calculation stated in prose, and the specification says a processor
"MUST NOT parse a `description` or reproduce a calculation from it". Metric 3
therefore uses the second-of-minute residual modulo 60, which requires no
reconstruction — and pays for that with the wrap noted in section 4.

**Staleness flags, silent-vessel alerts, or a missing-report count.**
`Timestamp` carries `cadence: { "kind": "irregular" }` — no `period`. The
specification says cadence "is an expectation and not a constraint", that it
"does not assert that every position has a record, that records arrive in
order", and that it is a *declared period* that "sizes a window, sets a
threshold beyond which a value is treated as stale, and makes an absent value
detectable as a gap". With `irregular` there is no declared period, so there is
no threshold I may set and no gap I may count. Metric 2 reports the observed
interval and asserts nothing about whether it is late.

**Any fleet-level or area aggregate across MMSIs** — mean speed of all vessels
in a window, vessel count per grid cell, traffic density. `UserID` is the
`featureOfInterest` and the schema declares one feature per record and nothing
that groups features into a fleet, a class, or an area. `ClassBUnit` is
`semanticRole: status` — the operating state of the station, not a vessel
category. Grid-cell density would additionally need the coordinate operation
ruled out above.

**A composite quality score over `Valid`, `PositionAccuracy` and `Raim`.** All
three are `resultQuality`, and the specification says each direct property with
that role "projects one" qualifier, that it "defines no threshold, ordering,

acceptable quality". Weighting them into one number would invent an ordering the
schema does not supply. Metric 1 uses `Valid` for a usability gate only, and
metric 4 reports the other two side by side.

**Transitions in `AssignedMode`, `ClassBUnit`, `ClassBDisplay`, `ClassBDsc`,
`ClassBBand`, `ClassBMsg22`.** A flip in a station's declared unit type or
capabilities between successive reports of one MMSI would be a plausible
integrity signal, and I considered it. `AssignedMode` and `ClassBUnit` are
`semanticRole: status`, and the specification says status "qualifies the record
rather than the phenomenon" and that "A change of status does not change what
was observed" — a change is expressly permitted and means nothing anomalous. The
four `ClassB*` capability flags carry no `semanticRole` at all, and "Omission
means undeclared". Nothing in the two files says these ought to be constant per
MMSI, so a flip-count would be a metric whose interpretation I supplied myself.

**`TrueHeading` is unused entirely**, for the reason given above; the only thing
I could soundly do with it is count its 511 sentinel, which duplicates the shape
of metric 1 without adding to it.

---

## 4. Assumptions

Each of these is something the query relies on that the schema and the instance
do not establish.

1. **ASSUMPTION — window size.** `TumblingWindow(minute, 5)` is arbitrary.
   `cadence` is `irregular` and declares no `period`, so nothing in the files
   fixes a natural aggregation interval. Five minutes is a guess at operator
   convenience, not a derivation.
2. **ASSUMPTION — `LAG` lookback.** `LIMIT DURATION(hour, 1)` is arbitrary for
   the same reason. A station silent longer than an hour yields NULL from `LAG`
   and drops out of metrics 2 and 5 rather than registering as a gap.
3. **ASSUMPTION — sentinel encodings.** 91 / 181 for position, 102.3 for `Sog`,
   360 for `Cog`, 60–63 for `Timestamp` are taken from the `description` text of
   those members. They are prose documentation, not annotations; if the feeder
   changes them these tests fail silently.
4. **ASSUMPTION — `Valid` polarity.** That `Valid` true means the record is
   usable is taken from its description. The specification supplies no scale,
   ordering, or processing effect for `resultQuality`, so the gate in metric 1
   is my reading of the feeder's own prose.
5. **ASSUMPTION — boolean comparison.** Booleans are compared as `= 1`. The
   runtime may require `= 'true'` instead.
6. **ASSUMPTION — arrival order.** `LAG` treats the previous event within the
   partition as the previous report of that station. The specification states
   that cadence "does not assert ... that records arrive in order", and nothing
   else in the files does either.
7. **ASSUMPTION — absent optional members.** `Sog`, `Cog`, `PositionAccuracy`
   and `Raim` are not in `required`. A missing `PositionAccuracy` or `Raim` is
   counted in the denominator but not the numerator of metric 4, i.e. treated as
   "not declared high accuracy" / "not declared RAIM"; a missing `Sog` or `Cog`
   drops that step from metric 5. That choice follows the specification's
   "Omission ... never implies compatible, successful, or acceptable data", but
   the specific fold is mine.
8. **ASSUMPTION — offset under one minute.** Metric 3 is modulo 60 by
   construction. If the receiver path ever delays a sentence by 60 seconds or
   more, the offset wraps and reads low with no indication that it has. The
   files give no way to detect this.
9. **ASSUMPTION — MMSI uniqueness.** That one `UserID` is one station for the
   duration of a window. The schema declares no `identity` and no uniqueness
   constraint; `featureOfInterest` states what the member is for, and the
   specification adds that "Feature identity MUST NOT be inferred from
   observation identity, location, property names, or transport metadata" —
   which means the declared role is all I have and I am taking it at face value.
10. **ASSUMPTION — `PERCENTILE_CONT` form.** I have written it as
    `PERCENTILE_CONT(0.5) OVER (PARTITION BY UserID ORDER BY <expr>)` alongside
    a `GROUP BY UserID, TumblingWindow(...)`, repeating the group key inside the
    `OVER` clause. I am reasonably confident this is the dialect's shape but
    cannot verify it; if it is not, the two medians become `AVG` at some cost in
    robustness to outliers.
11. **ASSUMPTION — float comparisons.** `Sog < 102.3` and `Cog < 360` are used
    in place of equality against the sentinel, on the assumption that no valid
    value reaches those bounds. The descriptions give 102.2 kn and 359.9° as the
    top valid values, which supports this, but the decoder's rounding is not
    stated.
12. **ASSUMPTION — the observable-property references are not resolvable.** The
    record-level `observedProperty` points at
    `https://catalog.example.org/...` with `kind: example-catalog`, which the
    specification itself describes as the placeholder "where the cited catalog is
    fictional". I therefore treat it as indeterminate rather than as evidence
    about what may be combined, which is what the specification prescribes for an
    unresolved reference.


TRANSCRIPT C

# Five derived metrics for the Class B (Message 18) position stream

## 1. The five metrics

Ordered most to least valuable.

1. **Report gap (seconds since the same station's previous usable report), per MMSI.**
   Derived by differencing `TimeReceived` against its own predecessor for the same
   `UserID`. Silence is the primary failure mode of a receiver network: an operator
   needs to know which stations went quiet, and for how long, before any downstream
   consumer treats a stale position as current.

2. **Degraded-report ratio, per MMSI per window.**
   The share of reports in the window that carry `Valid = false` or a
   sentinel in `Latitude` (91), `Longitude` (181) or `Timestamp` (60–63). This is the
   trust gate: it tells the operator what fraction of a station's traffic is unusable,
   and it is the denominator-aware companion to every other metric here, all of which
   silently drop those rows.

3. **Fix-to-receipt lag in seconds, per MMSI.**
   The residual between the declared phenomenon time and the declared receipt time:
   `second-of-minute(TimeReceived) − Timestamp`, wrapped modulo 60. The schema states
   that `TimeReceived` "follows the position fix by the propagation and queueing delay
   of the terrestrial receiver network" and that "the enclosing minute is recovered
   from the receipt time", so this difference is exactly the quantity the two members
   are documented to bracket. It measures ingest-path health and the true age of every
   position the pipeline serves.

4. **Speed-over-ground acceleration in knots per minute, per MMSI.**
   `Sog` differenced against its predecessor and divided by the elapsed report gap.
   A rate of change of speed is what distinguishes a manoeuvre from a steady transit,
   and an implausible step in it is the cheapest available signal that a report was
   mis-attributed to the wrong MMSI or that the position-fixing system is unstable.

5. **Course-over-ground versus true-heading residual in degrees, per MMSI.**
   The wrapped angular difference `|Cog − TrueHeading|`, folded to 0–180°. Two
   independently sourced members — one from the position-fixing system, one from the
   compass or gyro — describing the same physical direction. A persistent non-zero
   residual is the station's drift/set angle or a faulty compass; either is something
   an operator of this feed wants surfaced rather than averaged away.

`ReportsInWindow` is emitted as the denominator for metric 2 and as context; it is a
count of carried records and is not claimed as one of the five.

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
-- Event time  : TimeReceived (the only full datetime member in the schema).
-- Source key  : UserID (MMSI), used for every PARTITION BY and for GROUP BY.
-- Window      : TumblingWindow(minute, 5) in the final aggregation.
-- LAG horizon : LIMIT DURATION(minute, 30) on every LAG (required by the dialect).

WITH Cleaned AS
(
    SELECT
        UserID,
        TimeReceived,
        -- Boolean members are assumed to arrive as bit and to compare against 1/0.
        Valid,

        -- Second-of-minute of the fix, only when it is a real second (0-59).
        CASE WHEN Valid = 1 AND [Timestamp] <= 59
             THEN [Timestamp]
             ELSE NULL
        END AS FixSecond,

        -- Sog sentinel: 102.3 = not available.
        CASE WHEN Valid = 1 AND Sog <= 102.2
             THEN Sog
             ELSE NULL
        END AS SogKn,

        -- Cog sentinel: decoded 360 = not available.
        CASE WHEN Valid = 1 AND Cog < 360
             THEN Cog
             ELSE NULL
        END AS CogDeg,

        -- TrueHeading sentinel: 511 = not available.
        CASE WHEN Valid = 1 AND TrueHeading <= 359
             THEN TrueHeading
             ELSE NULL
        END AS HdgDeg,

        -- Metric 2 numerator: decode failure or any position/time sentinel.
        CASE WHEN Valid = 1
                  AND Latitude    <> 91
                  AND Longitude   <> 181
                  AND [Timestamp] <= 59
             THEN 0
             ELSE 1
        END AS IsDegraded
    FROM input TIMESTAMP BY TimeReceived
),

Lagged AS
(
    SELECT
        UserID,
        TimeReceived,
        Valid,
        FixSecond,
        SogKn,
        CogDeg,
        HdgDeg,
        IsDegraded,
        LAG(TimeReceived, 1) OVER (PARTITION BY UserID LIMIT DURATION(minute, 30)) AS PrevTimeReceived,
        LAG(Valid,        1) OVER (PARTITION BY UserID LIMIT DURATION(minute, 30)) AS PrevValid,
        LAG(SogKn,        1) OVER (PARTITION BY UserID LIMIT DURATION(minute, 30)) AS PrevSogKn
    FROM Cleaned
),

Derived AS
(
    SELECT
        UserID,
        IsDegraded,

        -- Metric 1: gap between consecutive decodable reports from the same station.
        CASE WHEN Valid = 1 AND PrevValid = 1
             THEN DATEDIFF(second, PrevTimeReceived, TimeReceived)
             ELSE NULL
        END AS ReportGapSeconds,

        -- Metric 3: fix-to-receipt lag, reconstructed modulo 60 seconds.
        -- '%' is used as the modulo operator; if it is unsupported, substitute
        -- (x - 60 * FLOOR(x / 60)).
        CASE WHEN FixSecond IS NOT NULL
             THEN ((DATEPART(second, TimeReceived) - FixSecond) + 60) % 60
             ELSE NULL
        END AS FixToReceiptLagSec,

        -- Metric 4: |dSog/dt| in knots per minute. NULL unless both speeds and the
        -- gap are usable; the gap guard also removes division by zero.
        CASE WHEN SogKn IS NOT NULL
                  AND PrevSogKn IS NOT NULL
                  AND Valid = 1 AND PrevValid = 1
                  AND DATEDIFF(second, PrevTimeReceived, TimeReceived) > 0
             THEN ABS(SogKn - PrevSogKn) * 60.0
                  / DATEDIFF(second, PrevTimeReceived, TimeReceived)
             ELSE NULL
        END AS AbsSogAccelKnPerMin,

        -- Metric 5: course/heading residual folded to 0-180 degrees.
        CASE WHEN CogDeg IS NOT NULL AND HdgDeg IS NOT NULL
             THEN ABS((((CogDeg - HdgDeg) + 540) % 360) - 180)
             ELSE NULL
        END AS CourseHeadingResidualDeg
    FROM Lagged
)

SELECT
    System.Timestamp() AS WindowEnd,
    UserID,
    COUNT(*)           AS ReportsInWindow,               -- denominator / context only

    -- Metric 1, over TumblingWindow(minute, 5), partitioned by UserID
    MAX(ReportGapSeconds) AS MaxReportGapSec,
    AVG(ReportGapSeconds) AS AvgReportGapSec,

    -- Metric 2, over TumblingWindow(minute, 5), partitioned by UserID
    SUM(IsDegraded) * 1.0 / COUNT(*) AS DegradedReportRatio,

    -- Metric 3, over TumblingWindow(minute, 5), partitioned by UserID
    AVG(FixToReceiptLagSec) AS AvgFixToReceiptLagSec,
    MAX(FixToReceiptLagSec) AS MaxFixToReceiptLagSec,

    -- Metric 4, over TumblingWindow(minute, 5), partitioned by UserID
    MAX(AbsSogAccelKnPerMin) AS MaxAbsSogAccelKnPerMin,

    -- Metric 5, over TumblingWindow(minute, 5), partitioned by UserID
    AVG(CourseHeadingResidualDeg) AS AvgCourseHeadingResidualDeg,
    MAX(CourseHeadingResidualDeg) AS MaxCourseHeadingResidualDeg
INTO output
FROM Derived
GROUP BY UserID, TumblingWindow(minute, 5)
```

## 3. What I did not compute

* **Great-circle distance between successive `Latitude`/`Longitude` pairs, and the
  implied-speed residual against `Sog`.** This is the most tempting metric in the
  feed and I left it out twice over: the dialect offers no geodesic function, and
  computing one by hand requires an earth model that the schema does not supply — it
  names WGS-84 decimal degrees and nothing else. The files also give no position
  uncertainty beyond the coarse `PositionAccuracy` boolean ("better than 10 m" /
  "greater than 10 m"), so any threshold on the residual would be invented rather
  than licensed.

* **Spatial aggregation: binning `Latitude`/`Longitude` to a grid for traffic density
  or vessel counts per cell.** Nothing in the two files establishes a cell size, a
  region of interest, or a projection. Picking one would be a domain assertion.

* **Rate of turn from successive `Cog`.** Message 18 carries no rate-of-turn member,
  and differencing a single noisy course value is weaker than the `Cog`/`TrueHeading`
  residual I kept, which compares two independently sourced members.

* **Separate rates for `Timestamp` = 61 (manual input), 62 (dead reckoning) and 63
  (inoperative).** Each is a legitimate flag rate, but the schema gives no basis for
  ranking their severity against one another, and splitting them out would spend three
  of the five slots on one member. They are collapsed into the degraded-report ratio.

* **`PositionAccuracy` and `Raim` mix (fraction high-accuracy, fraction RAIM in use).**
  Both describe the transmitting station's own position-fixing configuration, which the
  schema presents as a property of the equipment rather than of the moment. A rate over
  a window therefore measures fleet composition, not a change in conditions, and would
  be near-constant per MMSI.

* **`ClassBUnit`, `ClassBDisplay`, `ClassBDsc`, `ClassBBand`, `ClassBMsg22` aggregates.**
  These are declared capability flags of the unit. Counting them produces an equipment
  inventory, not a stream metric.

* **`AssignedMode` transition count (autonomous ↔ base-station controlled, via `LAG`).**
  This one is sound and derivable — I dropped it purely on value. The files establish
  what the flag means but nothing about how often assignment changes, so I could not
  justify it above any of the five above.

* **`PERCENTILE_CONT` on the lag and gap distributions.** In this dialect
  `PERCENTILE_CONT` takes an `OVER` clause rather than composing with `GROUP BY`, so it
  does not fit the single-statement, windowed-aggregate shape required here. `AVG` and
  `MAX` are used instead, which are more outlier-sensitive.

* **Any cross-station aggregate** (distinct MMSI counts, fleet-wide averages). The
  only identifier in the schema is `UserID`; nothing groups stations into a fleet or an
  area, so any such aggregate would be over an arbitrary set.

## 4. Assumptions

Each of the following is relied on by the query and is **not** established by the
schema or the instance.

* **Assumption:** the input stream is aliased `input` and the output sink `output`.
* **Assumption:** `TimeReceived` is a sound event time. It is the only member with
  full date resolution (`Timestamp` gives second-of-minute only), so it is the only
  possible choice, but the schema explicitly says it lags the phenomenon time by a
  variable network delay — so window boundaries are receipt boundaries, not fix
  boundaries.
* **Assumption:** the fix-to-receipt delay is under 60 seconds, which is what makes the
  modulo-60 reconstruction in metric 3 unambiguous. The schema bounds the delay
  nowhere. If the delay exceeds a minute the metric silently wraps.
* **Assumption:** `DATEPART(second, TimeReceived)` and `Timestamp` are on the same
  clock basis. `Timestamp` is documented as a UTC second; `TimeReceived` is an instant
  and the instance carries `Z`, so I treat both as UTC.
* **Assumption:** the feed is not deduplicated across receivers. If the same
  transmission arrives twice from two shore stations, metric 1 understates gaps and
  metric 4 sees a zero-elapsed pair (guarded to NULL by the `> 0` check).
* **Assumption:** `UserID` (MMSI) is stable and uniquely identifies one station for the
  duration of a window. The schema says it is the identity of the transmitting station;
  it does not say it cannot be reused, shared or spoofed.
* **Assumption:** JSON booleans (`Valid`, and the sentinel guards that depend on it)
  surface as a `bit`-like type comparable to `1`. If they surface as strings, every
  `= 1` comparison needs rewriting.
* **Assumption:** sentinel values arrive exactly as declared — `Latitude` exactly 91,
  `Longitude` exactly 181, `Cog` exactly 360, `TrueHeading` exactly 511. `Sog` is
  compared as `<= 102.2` rather than `<> 102.3` because it is a `double` and the
  schema's sentinel (102.3) is not exactly representable.
* **Assumption:** the 5-minute tumbling window and the 30-minute `LIMIT DURATION`
  horizon are operationally reasonable. Nothing in the files states a Class B reporting
  interval, so neither figure is derived from the schema; the `LIMIT DURATION` must
  exceed the longest gap you still wish to measure, or metric 1 truncates.
* **Assumption:** aggregates ignore NULLs (standard behaviour), so `AVG` and `MAX` for
  metrics 1, 3, 4 and 5 are taken over usable rows only, while `COUNT(*)` and the
  metric-2 ratio are taken over all rows. The two therefore have different denominators
  by design.
* **Assumption:** the `%` modulo operator is available. I am not certain of this in
  this dialect; the comment in the query gives a `FLOOR`-based substitute.
* **Assumption:** a report whose `Valid` is false may still have a trustworthy
  `UserID`. The query uses it to attribute the row to a station for the metric-2
  denominator, while excluding it from every other computation. The schema says only
  that such a message "could not be fully decoded", which does not guarantee the MMSI
  survived.


TRANSCRIPT D

# Five derived metrics for `StandardClassBPositionReport`

## 1. The five metrics

1. **Report interval and long-gap count** (per `UserID`, per window) — the elapsed
   seconds between consecutive `TimeReceived` values for one source, summarised as
   mean, max, and a count of intervals over a threshold. Most valuable because every
   other metric here is a rate, and a rate whose denominator is unknown is
   uninterpretable; it is also the first thing an operator checks when a source goes
   quiet or the ingest path stalls.
2. **Quality-flag share** (per `UserID`, per window) — the fraction of reports in the
   window in which `Valid`, `PositionAccuracy` and `Raim` are each set. Valuable
   because it separates "the source did something" from "the source emitted junk",
   and it must be read *before* metrics 3–5 are trusted. I report three independent
   shares rather than one composite score, because only `Valid` has a name that
   licenses a polarity; for `PositionAccuracy` and `Raim` the actionable signal is a
   shift in the share, not its level.
3. **Turn rate from `Cog`** — the shortest-arc change in `Cog` between consecutive
   reports divided by the elapsed seconds, summarised as peak turn rate and total
   absolute course change in the window. Valuable because a course change is the
   clearest evidence of a manoeuvre, and total course change per window separates a
   source holding a line from one that is working.
4. **Speed change rate from `Sog`** — `|ΔSog|` between consecutive reports divided by
   elapsed seconds, as mean and peak. Valuable for the same manoeuvre-detection
   reason, and because an implausibly large value is a strong indicator of two
   distinct sources sharing one `UserID`, or of a corrupted record.
5. **`Cog`–`TrueHeading` residual** — the absolute shortest-arc difference between the
   two direction members, as mean and peak per window. Valuable because these are two
   independently reported directions; a persistent divergence is either a real
   physical condition or a failing sensor, and either way it is a condition the
   operator wants raised. Ranked last because it is the metric that leans hardest on
   an assumption the files do not state (see A3).

`ReportCount` appears in the output as the denominator for metric 2. It is context,
not one of the five.

## 2. The query

```sql
-- Event time is TimeReceived: the only datetime member in the schema, and one of
-- the six required members. Timestamp (int32) is NOT used as event time; see §3.
WITH Ordered AS
(
    SELECT
        UserID,
        TimeReceived,
        Sog,
        Cog,
        TrueHeading,
        Valid,
        PositionAccuracy,
        Raim,
        -- LIMIT DURATION is required by the dialect. 30 minutes is a deliberate
        -- over-provision: any inter-report gap longer than this horizon returns
        -- NULL rather than a large number, which would hide exactly the worst
        -- gaps from metric 1. See A7.
        LAG(TimeReceived, 1) OVER (PARTITION BY UserID LIMIT DURATION(minute, 30)) AS PrevTimeReceived,
        LAG(Sog, 1)          OVER (PARTITION BY UserID LIMIT DURATION(minute, 30)) AS PrevSog,
        LAG(Cog, 1)          OVER (PARTITION BY UserID LIMIT DURATION(minute, 30)) AS PrevCog
    FROM input TIMESTAMP BY TimeReceived
),
Stepped AS
(
    SELECT
        UserID,
        DATEDIFF(second, PrevTimeReceived, TimeReceived) AS GapSeconds,
        Sog - PrevSog AS SogDelta,
        -- Shortest-arc wrap without a modulo operator: both operands are assumed
        -- to lie on the same 0..360 datum, so the raw difference is in
        -- (-360, 360) and one correction suffices.
        CASE
            WHEN (Cog - PrevCog) >  180 THEN (Cog - PrevCog) - 360
            WHEN (Cog - PrevCog) < -180 THEN (Cog - PrevCog) + 360
            ELSE (Cog - PrevCog)
        END AS CourseChangeDeg,
        -- TrueHeading is not in the required set, so it may be absent.
        CASE
            WHEN TrueHeading IS NULL OR Cog IS NULL THEN NULL
            WHEN (Cog - TrueHeading) >  180 THEN ABS((Cog - TrueHeading) - 360)
            WHEN (Cog - TrueHeading) < -180 THEN ABS((Cog - TrueHeading) + 360)
            ELSE ABS(Cog - TrueHeading)
        END AS CogHeadingResidualDeg,
        Valid,
        PositionAccuracy,
        Raim
    FROM Ordered
),
Rated AS
(
    SELECT
        UserID,
        GapSeconds,
        CourseChangeDeg,
        CogHeadingResidualDeg,
        Valid,
        PositionAccuracy,
        Raim,
        CASE WHEN GapSeconds > 0
             THEN ABS(SogDelta) / CAST(GapSeconds AS float)
             ELSE NULL END AS SogRatePerSec,
        CASE WHEN GapSeconds > 0
             THEN ABS(CourseChangeDeg) / CAST(GapSeconds AS float)
             ELSE NULL END AS TurnRateDegPerSec
    FROM Stepped
)
SELECT
    UserID,
    System.Timestamp() AS WindowEnd,
    COUNT(*)           AS ReportCount,

    -- Metric 1: report interval and long-gap count
    AVG(CAST(GapSeconds AS float))                    AS MeanReportIntervalSec,
    MAX(GapSeconds)                                   AS MaxReportIntervalSec,
    SUM(CASE WHEN GapSeconds > 180 THEN 1 ELSE 0 END) AS LongGapCount,

    -- Metric 2: quality-flag share. NULL-guarded so that an absent optional
    -- member is excluded from the average rather than counted as false.
    -- Dialect note: I am unsure whether a JSON boolean surfaces as bit or as
    -- bigint here; if `= 1` does not compile, use CAST(<member> AS bigint) = 1.
    AVG(CASE WHEN Valid = 1 THEN 1.0 ELSE 0.0 END)    AS ValidShare,
    AVG(CASE WHEN PositionAccuracy IS NULL THEN NULL
             WHEN PositionAccuracy = 1 THEN 1.0 ELSE 0.0 END) AS PositionAccuracyShare,
    AVG(CASE WHEN Raim IS NULL THEN NULL
             WHEN Raim = 1 THEN 1.0 ELSE 0.0 END)             AS RaimShare,

    -- Metric 3: turn rate from Cog
    MAX(TurnRateDegPerSec)       AS PeakTurnRateDegPerSec,
    SUM(ABS(CourseChangeDeg))    AS TotalCourseChangeDeg,

    -- Metric 4: speed change rate from Sog (in Sog units per second; the unit of
    -- Sog is not declared by either file, so neither is the unit of this rate)
    AVG(SogRatePerSec)           AS MeanSogChangePerSec,
    MAX(SogRatePerSec)           AS PeakSogChangePerSec,

    -- Metric 5: Cog-TrueHeading residual
    AVG(CogHeadingResidualDeg)   AS MeanCogHeadingResidualDeg,
    MAX(CogHeadingResidualDeg)   AS PeakCogHeadingResidualDeg

INTO output
FROM Rated
GROUP BY UserID, TumblingWindow(minute, 5)
```

Window type and size: a **5-minute tumbling window**, partitioned by `UserID`, the
only member in the schema that identifies an individual source. Tumbling rather than
hopping or sliding because these are periodic health and manoeuvre summaries where
non-overlapping, non-double-counting buckets are what an operator wants; a hopping
window would report the same long gap in several consecutive outputs.

## 3. What I did not compute

* **Implied speed from `Latitude`/`Longitude`, and its residual against `Sog`.** This
  would be the single strongest cross-check available — a position-derived speed
  against a reported one. I left it out because it needs three things neither file
  states: that `Latitude`/`Longitude` are degrees, what earth model or projection
  converts a degree difference to a distance, and what unit `Sog` is in. A residual
  between two quantities in unknown and possibly different units is not a metric.
* **Distance travelled / track length** from successive `Latitude`/`Longitude`. Same
  problem, plus a second one: a degree of `Longitude` is not a fixed distance and
  varies with `Latitude`, so summing raw coordinate deltas produces a number that
  means nothing consistent.
* **A residual between `Timestamp` (int32) and `TimeReceived` (datetime).** A
  second-of-minute reading of `Timestamp` is the obvious guess, and it is only a
  guess: the schema declares nothing but `int32`, and in the one example `Timestamp`
  is `7` while `TimeReceived` ends `:09Z`, so the single record available does not
  even let me calibrate the guess. I therefore do not use `Timestamp` at all,
  including as the event time.
* **Any rate or transition count over `AssignedMode`, `ClassBUnit`, `ClassBDisplay`,
  `ClassBDsc`, `ClassBBand`, `ClassBMsg22`.** These are computable — a share, or a
  count of flips — but the files establish no meaning for any of the six, and all six
  are `true` in the one example, so I have neither a semantics nor a baseline. A
  number I could not tell the operator how to act on is worse than no number.
* **Geofence or area-occupancy counts** from `Latitude`/`Longitude`. Requires a
  boundary definition; the two files supply none, and inventing one would be
  inventing a fact about the domain.
* **Dispersion of position via `STDEV(Latitude)`, `STDEV(Longitude)`** as a
  moving/stationary discriminator. Left out for the unit reason above, and because
  the two standard deviations are not comparable to each other at an arbitrary
  latitude, so they cannot be combined into a single scalar.
* **Fleet-wide `COUNT(DISTINCT UserID)` per window** as a coverage metric. Genuinely
  valuable, and cut only because the budget is five and I judged per-source
  continuity (metric 1) more actionable than an aggregate that tells you the total
  moved without telling you which source stopped. It also does not partition by
  source, so it would not fit this query's output shape without a second grouping.
* **Suppressing the turn rate when `Sog` is at or near zero.** The wrapped `ΔCog` is
  dominated by noise when a source is barely moving, which will inflate
  `PeakTurnRateDegPerSec`. I did not add the guard because the files establish no
  `Sog` threshold below which `Cog` stops being meaningful, and picking one would be
  inventing a domain fact. It is a known limitation of metric 3, not an oversight.

## 4. Assumptions

* **A1 (assumption).** `TimeReceived` is the event time — the instant the observation
  applies to — and is what the stream should be ordered by. The schema says only that
  it is a required `datetime`; the name is the entire basis for this choice.
* **A2 (assumption).** Events arrive in, or close to, `TimeReceived` order.
  `TIMESTAMP BY` and `LAG` both depend on this; sustained out-of-order arrival will
  produce negative `GapSeconds` and spurious deltas. No late-arrival tolerance is
  configured here because the files establish no expected disorder.
* **A3 (assumption).** `Cog` and `TrueHeading` are angles in the same unit and on the
  same 0–360 datum, so their difference is meaningful. The only support is the single
  instance (`287.3` and `285`); the schema declares no unit for either, and they have
  different declared types (`double` and `int32`). Metric 5 is void if this is wrong.
* **A4 (assumption).** `UserID` identifies one physical source, is stable over the
  window, and is not reused by another source within it. Nothing in the files says so.
* **A5 (assumption).** The true course change between two consecutive reports is less
  than 180°, so the shortest-arc wrap recovers it. This fails after a long gap or
  during a fast turn, in which case metric 3 understates the change and may invert
  its sign.
* **A6 (assumption).** No out-of-band sentinel or "unavailable" encoding exists for
  `TrueHeading`, `Sog` or `Cog`. The files declare none, so every present value is
  treated as a real measurement. If the feed does use sentinels, metrics 3, 4 and 5
  will be corrupted rather than merely noisy.
* **A7 (assumption).** The `LIMIT DURATION(minute, 30)` horizon on `LAG` exceeds the
  real reporting interval. Where it does not, `PrevTimeReceived` is NULL and the gap
  is silently dropped instead of being reported as large — which is the failure mode
  metric 1 exists to catch. Detecting silences longer than the horizon needs a
  separate absence-detection pattern, not this query.
* **A8 (assumption).** The threshold in `LongGapCount` (180 seconds) is arbitrary.
  Nothing in the two files establishes a reporting cadence, so no threshold is
  licensed; it is a placeholder to be calibrated against observed traffic.
* **A9 (assumption).** The 5-minute window size is likewise arbitrary, chosen only so
  that it plausibly contains several reports per source given no stated cadence.
* **A10 (assumption).** `Sog` is a non-negative scalar in a fixed unit, so
  differencing successive values is meaningful even though the unit is unknown.
  Metric 4 is therefore expressed in "`Sog` units per second" and cannot be given a
  physical name.
* **A11 (assumption).** `Valid = false` denotes a report that should not be trusted.
  This reads a polarity out of the member's name. I deliberately do not extend the
  same reading to `PositionAccuracy` or `Raim`, which is why metric 2 reports their
  raw shares instead of folding them into a single "degraded" rate.
