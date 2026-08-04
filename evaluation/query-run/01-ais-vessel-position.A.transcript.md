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
