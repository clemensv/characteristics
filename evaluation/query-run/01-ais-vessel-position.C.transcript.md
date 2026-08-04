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
