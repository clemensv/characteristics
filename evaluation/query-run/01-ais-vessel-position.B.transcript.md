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
confidence model, or processing effect", and that omission "does not imply
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
