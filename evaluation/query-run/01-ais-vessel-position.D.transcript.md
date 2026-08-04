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
