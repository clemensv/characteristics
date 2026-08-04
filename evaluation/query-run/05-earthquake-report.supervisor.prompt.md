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

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order latitude, longitude. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. `origin_datetime` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `origin_datetime` as the time the record was produced, received, or published, or using a different member for event time.

3. Successive `origin_datetime` values are expected at cadence `irregular`. A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

4. `report_datetime` is an operational instant (`resultTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `report_datetime` as the event time of the observation.

5. `control_datetime` is an operational instant (`ingestionTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `control_datetime` as the event time of the observation.

6. `latitude` is calculated rather than measured directly.
   wrong reading: Treating `latitude` as a direct measurement.

7. `latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `latitude`.

8. `longitude` is calculated rather than measured directly.
   wrong reading: Treating `longitude` as a direct measurement.

9. `longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `longitude`.

10. `depth_km` is calculated rather than measured directly.
   wrong reading: Treating `depth_km` as a direct measurement.

11. `depth_km` is expressed in `km`.
   wrong reading: Assuming a different or conventional unit for `depth_km`.

12. `magnitude` is calculated rather than measured directly.
   wrong reading: Treating `magnitude` as a direct measurement.

13. `max_intensity` is already a `maximum` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `max_intensity` as though it were a raw sample.

14. `bulletin_type` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `bulletin_type` as an observed quantity.

15. `tsunami_possible` is `estimated` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `tsunami_possible` as a measured observation.

16. `max_intensity` is already a `maximum` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `max_intensity` as though it were a raw sample.


TRANSCRIPT A

# Five derived metrics over `EarthquakeReport`

## 1. The five metrics

1. **Solution publication latency, 95th percentile, per bulletin product and status** —
   `report_datetime − origin_datetime`, summarised over a window and grouped by
   `bulletin_type` and `info_type`. The schema declares `origin_datetime` as
   `phenomenonTime` and `report_datetime` as `resultTime` and states outright that the
   latter "is later than, and independent of, the origin time", so the difference is the
   time the feed took to turn a rupture into a published solution. `bulletin_type` is
   annotated `semanticRole: resultQuality` and its altenums say `VXSE51` is issued
   "within about a minute and a half … before the source parameters are determined"
   while `VXSE53` carries determined parameters, so latency is only meaningful *per
   product*: pooling them describes nothing. This is the operator's alerting SLA.

2. **Magnitude revision delta between successive bulletins of one earthquake** —
   `magnitude − LAG(magnitude)` partitioned by `event_id`. `event_id` is stable across
   "multiple serial reports for the same earthquake", and `magnitude` is
   `derivation: calculated` — a solution that is recomputed as more stations report. A
   non-zero delta says the size estimate is still moving, which is what a downstream
   consumer needs before it acts on the current number.

3. **Bulletin count per earthquake (revision churn)** — count of records sharing one
   `event_id` over a session. Tells the operator how many downstream updates one
   earthquake generates and whether the solution has settled. A high count is an
   unsettled event; it also sizes the amplification factor between events and messages.

4. **Distinct earthquakes per seismic source region per rolling window** —
   `COUNT(DISTINCT event_id)` grouped by `epicenter_area_code`, which is annotated
   `semanticRole: featureOfInterest` and "names the seismic source region that the
   bulletin describes". Counting *events*, not bulletins, is the whole point: serial
   reports would otherwise multiply-count one earthquake. A rising count in one region
   is a swarm or an aftershock sequence.

5. **Distribution handover lag, maximum per window** —
   `control_datetime − report_datetime`. `control_datetime` is `semanticRole:
   ingestionTime` and "records the handover of the finished bulletin into the
   distribution channel rather than the completion of the solution", so this separates
   delay in the *pipe* from delay in the *solution* (metric 1). Without it, a plumbing
   outage is indistinguishable from slow seismology.

## 2. The query

```sql
-- Event time is report_datetime (semanticRole: resultTime). It is the only member that
-- advances per bulletin: origin_datetime is shared by every serial report of one
-- earthquake (the schema says the event id is built from it), so timestamping by it
-- would place a serial-2 correction minutes of wall-clock in the past and expose it to
-- being dropped as late. control_datetime is an operational value; the specification
-- says operational values describe the handling of the record and MUST NOT be read as
-- resultTime, so it is measured, not used as the clock.

WITH

-- Stage 1: per-bulletin durations. Both differences are licensed by the schema itself,
-- which states that report_datetime is later than origin_datetime and that
-- control_datetime is a later handover of the finished bulletin. No window.
Bulletins AS
(
    SELECT
        event_id,
        serial,
        info_type,
        bulletin_type,
        epicenter_area_code,
        magnitude,
        DATEDIFF(second, origin_datetime, report_datetime)  AS solution_latency_s,
        DATEDIFF(second, report_datetime, control_datetime) AS handover_lag_s
    FROM input TIMESTAMP BY report_datetime
),

-- Stage 2a: the magnitude series for one earthquake. CANCELLED bulletins are dropped
-- because the altenum defines CANCELLED as "Withdrawal of a bulletin already
-- published" — a withdrawal is not a new estimate. NULL magnitudes are dropped because
-- the schema says magnitude is absent for 震度速報 and related products.
MagnitudeSolutions AS
(
    SELECT event_id, serial, magnitude
    FROM Bulletins
    WHERE magnitude IS NOT NULL
      AND info_type <> 'CANCELLED'
),

-- Stage 2b: successive-record difference, partitioned by the earthquake. No window;
-- LIMIT DURATION is the required reach of LAG, not an aggregation window.
MagnitudeRevision AS
(
    SELECT
        System.Timestamp() AS emit_time,
        event_id,
        magnitude,
        LAG(magnitude, 1) OVER (PARTITION BY event_id LIMIT DURATION(hour, 6))
            AS previous_magnitude
    FROM MagnitudeSolutions
),

-- Stage 3: TumblingWindow, 15 minutes. Partitioned by bulletin_type (resultQuality:
-- the maturity of the solution) and info_type (status: where the bulletin stands in
-- the revision sequence). Metrics 1 and 5 both fall out of this one aggregation.
LatencyByProduct AS
(
    SELECT
        System.Timestamp() AS window_end,
        bulletin_type,
        info_type,
        -- I am not certain Azure Stream Analytics accepts the WITHIN GROUP form;
        -- it documents PERCENTILE_CONT as an analytic function taking an OVER clause.
        -- MAX(solution_latency_s) is the certain fallback if this is rejected.
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY solution_latency_s)
            AS solution_latency_p95_s,
        MAX(handover_lag_s) AS handover_lag_max_s
    FROM Bulletins
    GROUP BY bulletin_type, info_type, TumblingWindow(minute, 15)
),

-- Stage 4: SessionWindow, 30-minute gap, 6-hour maximum duration. Partitioned by
-- event_id, which is the identifier the schema gives for one earthquake.
EventChurn AS
(
    SELECT
        System.Timestamp() AS window_end,
        event_id,
        COUNT(*) AS bulletin_count
    FROM Bulletins
    GROUP BY event_id, SessionWindow(minute, 30, 360)
),

-- Stage 5: HoppingWindow, 6-hour window advancing every 1 hour. Partitioned by
-- epicenter_area_code (featureOfInterest). Rows with no hypocentre metadata are
-- excluded: the schema says the code is null for 震度速報 and related products, and a
-- null region is not a region.
RegionActivity AS
(
    SELECT
        System.Timestamp() AS window_end,
        epicenter_area_code,
        -- COUNT(DISTINCT ...) is required here so that serial reports of one
        -- earthquake are not counted as separate earthquakes. I am not fully certain
        -- of its support in this dialect inside a windowed GROUP BY.
        COUNT(DISTINCT event_id) AS distinct_events
    FROM Bulletins
    WHERE epicenter_area_code IS NOT NULL
    GROUP BY epicenter_area_code, HoppingWindow(hour, 6, 1)
)

-- Single narrow output: one row per metric observation. INTO is placed on the first
-- branch of the UNION; if the dialect rejects INTO on a UNION, the same WITH clause
-- can drive one SELECT ... INTO per stage instead.
SELECT
    window_end                              AS window_end,
    'solution_latency_p95_s'                AS metric,
    'bulletin_type/info_type'               AS scope_kind,
    CONCAT(bulletin_type, '/', info_type)   AS scope_key,
    CAST(solution_latency_p95_s AS float)   AS value
INTO output
FROM LatencyByProduct

UNION

SELECT
    emit_time,
    'magnitude_revision_delta',
    'event_id',
    event_id,
    CAST(magnitude - previous_magnitude AS float)
FROM MagnitudeRevision
WHERE previous_magnitude IS NOT NULL

UNION

SELECT
    window_end,
    'event_bulletin_count',
    'event_id',
    event_id,
    CAST(bulletin_count AS float)
FROM EventChurn

UNION

SELECT
    window_end,
    'distinct_events_6h',
    'epicenter_area_code',
    epicenter_area_code,
    CAST(distinct_events AS float)
FROM RegionActivity

UNION

SELECT
    window_end,
    'handover_lag_max_s',
    'bulletin_type/info_type',
    CONCAT(bulletin_type, '/', info_type),
    CAST(handover_lag_max_s AS float)
FROM LatencyByProduct
```

## 3. What I did not compute

* **A window maximum over `max_intensity`, or over `affected_prefectures[].max_intensity`.**
  Both carry `derivation: statistic` with `statistic: maximum`. The specification's
  `statistic` section states that the keyword "does not state a window alignment, a
  weighting, a sample count, a treatment of missing values … and a processor MUST NOT
  recompute a result from it." Independently, neither file establishes an ordering over
  the enum `1, 2, 3, 4, 5-, 5+, 6-, 6+, 7`; it is a listing, not a declared ordinal
  scale, and `MAX()` over those strings would compare them lexicographically, ranking
  `5-` above `5+` and both below `7` by accident rather than by meaning.

* **`AVG(magnitude)` or a summed release over a window.** `magnitude` is annotated
  `derivation: calculated`, and its only concept binding is
  `qudt:vocab/quantitykind/Dimensionless`. Neither file states that the JMA scale is
  linear-additive, so a mean or a sum of magnitudes is arithmetic without a declared
  meaning. (The description's remark that the scale is "similar to Richter magnitude"
  is prose, and I have not used it to license or forbid anything.)

* **`MAX(magnitude)` per region per window — the largest earthquake in the window.**
  This one is tempting and I left it out for a structural reason, not a scale reason:
  the stream carries several bulletins per `event_id` with revised magnitudes, so a
  window `MAX` over bulletins is a maximum over *revisions*, not over *earthquakes*.
  Picking the authoritative value per event needs a rule for choosing among `serial`
  values, and `serial` is documented only as "the revision sequence" with `minimum: 0`
  — neither file says which serial is the first, nor that the highest serial seen so far
  is final.

* **Hypocentre separation between successive events, and any 3-D hypocentre distance.**
  `coordinateReferenceSystem` declares `coordinates: ["latitude", "longitude"]` only.
  The specification states that "properties not named by `coordinates` are not part of
  the coordinate", so `depth_km` may not be treated as a third axis of that CRS. And
  EPSG:4326 is angular: converting a degree separation of `latitude`/`longitude` into
  kilometres needs an ellipsoid or radius constant that neither file supplies.

* **Gap, staleness or missed-event detection.** `origin_datetime` declares
  `cadence: { "kind": "irregular" }`. The specification defines `irregular` as
  "observations occur without a regular period", prohibits `period` for that kind, and
  says cadence "does not assert that every position has a record, that records arrive in
  order". There is therefore no expected interval against which an absence is a gap.

* **Any aggregate over `tsunami_possible`.** It is `derivation: estimated`, inferred by
  the bridge from free-text comments, and `null` means "no tsunami-related detail text
  was available or fetched". A count of `true` over a window would fold "no concern"
  together with "not fetched"; the specification's annotation model states that
  "omission means undeclared … It never implies compatible, successful, or acceptable
  data."

* **A count of `affected_prefectures` as a shaking-footprint metric.** Sound in
  principle, but the array is empty for products that carry no intensity summary —
  `VXSE52` is described as "determined source parameters *without* an observed-intensity
  summary" — so an unconditioned count mixes structural zeros with real footprints. It
  would need to be conditioned on `bulletin_type`, and it ranked below the five above.

* **A second timestamp parsed out of `event_id`.** The description says JMA uses the
  origin time in `YYYYMMDDHHMMSS` form as the event id, but the files do not state the
  time zone of those digits, and `origin_datetime` already carries that instant in UTC.

## 4. Assumptions

* **Assumption:** `report_datetime` is close enough to monotone across the stream to
  serve as event time. The schema establishes only that it is later than
  `origin_datetime` for a given bulletin, not that successive bulletins are published in
  order. Any late-arrival and out-of-order tolerance is configured on the job, not in
  this query.
* **Assumption:** the window sizes — `TumblingWindow(minute, 15)`,
  `HoppingWindow(hour, 6, 1)`, `SessionWindow(minute, 30, 360)`. Nothing in the two
  files sizes them; `cadence` is `irregular` and therefore supplies no period.
* **Assumption:** `LIMIT DURATION(hour, 6)` bounds the reach of `LAG` for one
  `event_id`. The files state no horizon over which revisions to one earthquake stop
  arriving.
* **Assumption:** event-time order within one `event_id` agrees with `serial` order, so
  that `LAG` reaches the previous revision. `serial` is the declared revision sequence;
  the query orders by the event-time clock instead, and does not reorder by `serial`.
* **Assumption:** `LAG` evaluated in `MagnitudeRevision` reaches the previous row of the
  *filtered* `MagnitudeSolutions` set rather than the previous row of the raw input.
* **Assumption:** excluding `info_type = 'CANCELLED'` from the magnitude series is
  correct. The altenum describes CANCELLED as "Withdrawal of a bulletin already
  published"; reading a withdrawal as contributing no new magnitude estimate is my
  interpretation, not a stated rule.
* **Assumption:** absent optional members (`magnitude`, `epicenter_area_code`, and the
  members the schema says may be omitted such as `latitude`, `longitude`, `depth_km`,
  `max_intensity`) surface as SQL `NULL` at runtime.
* **Assumption:** dialect support for `PERCENTILE_CONT ... WITHIN GROUP`,
  `COUNT(DISTINCT ...)` inside a windowed `GROUP BY`, and `INTO` on the first branch of a
  `UNION`. Each is flagged in a comment in the query, with a fallback where one exists.
* **Assumption:** a single input stream, aliased `input`, carrying only records of this
  type.


TRANSCRIPT B

# Five derived metrics over the JMA earthquake bulletin stream

## 1. The five metrics

1. **Time to determined solution** — `DATEDIFF(second, origin_datetime, report_datetime)` for bulletins that actually carry a source solution, summarised per source region per window. It is the interval between the member declared `phenomenonTime` and the member declared `resultTime`, so it is the feed's headline timeliness figure: nothing downstream can act earlier than this number.
2. **Magnitude revision between consecutive bulletins of one earthquake** — signed change in `magnitude` against the previous bulletin sharing the same `event_id`. `serial` is declared to be a revision sequence, so the same earthquake is restated repeatedly; a revision changes the size of an event *after* downstream systems have already acted on the earlier bulletin, which makes the largest upgrade and downgrade in a window the most consequential content change this feed emits.
3. **Seismic-intensity escalation** — change in the rank of `max_intensity` on the declared shindo ordering, against the previous bulletin for the same `event_id`, plus a count of escalating bulletins. `max_intensity` is the member that describes what was felt rather than what ruptured, so an upward step is the operational trigger, and it can move independently of `magnitude`.
4. **Distinct-event rate and revision load per source region** — `COUNT(DISTINCT event_id)` and bulletins-per-event, grouped by `epicenter_area_code`. Because many bulletins share one `event_id`, a raw bulletin count is not an earthquake count; the distinct count is the real rate, and several distinct events in one area in one hour is the signature of a swarm or aftershock sequence. The ratio says how much of the traffic is new events versus restatement.
5. **Distribution handover lag** — `DATEDIFF(second, report_datetime, control_datetime)`, the interval between the declared `resultTime` and the declared `ingestionTime`. It is the only metric here that measures the channel rather than JMA, so it is what separates "the analysis was slow" from "our own pipeline is backed up".

## 2. The query

```sql
-- Output grain: one row per JMA hypocentre area code per hopping window.
WITH Bulletins AS (
    -- Event time is control_datetime, the member carrying semanticRole
    -- ingestionTime: it is the only member whose ordering is the order in which
    -- bulletins reach the distribution channel. origin_datetime declares
    -- cadence "irregular" and a late serial for an old earthquake can be
    -- published at any time, so origin_datetime would arrive arbitrarily
    -- out of order. report_datetime is the solution time, not an arrival time.
    SELECT
        event_id,
        serial,
        info_type,
        bulletin_type,
        magnitude,
        -- flashes carry no hypocentre, so epicenter_area_code is nullable;
        -- bucket them rather than drop them (see assumptions)
        COALESCE(epicenter_area_code, 'UNLOCALISED') AS source_area_code,

        -- M1: rupture (phenomenonTime) -> solution published (resultTime)
        DATEDIFF(second,
                 CAST(origin_datetime AS datetime),
                 CAST(report_datetime AS datetime)) AS solution_latency_s,

        -- M5: solution published (resultTime) -> channel handover (ingestionTime)
        DATEDIFF(second,
                 CAST(report_datetime AS datetime),
                 CAST(control_datetime AS datetime)) AS handover_lag_s,

        -- Rank of the shindo enum in the order the enum declares, whose
        -- descriptions are monotone in severity (5- below 5+, 6- below 6+).
        -- This is a position on a declared ordering, not a physical quantity.
        CASE
            WHEN max_intensity = '1'  THEN 1
            WHEN max_intensity = '2'  THEN 2
            WHEN max_intensity = '3'  THEN 3
            WHEN max_intensity = '4'  THEN 4
            WHEN max_intensity = '5-' THEN 5
            WHEN max_intensity = '5+' THEN 6
            WHEN max_intensity = '6-' THEN 7
            WHEN max_intensity = '6+' THEN 8
            WHEN max_intensity = '7'  THEN 9
            ELSE NULL
        END AS intensity_rank
    FROM input TIMESTAMP BY control_datetime
),
Revised AS (
    -- Successive-bulletin comparison inside one earthquake. event_id is the
    -- only member stable across the revision sequence, so it is the partition
    -- key for LAG. CANCELLED bulletins withdraw a bulletin rather than restate
    -- a solution, so they are excluded: their timestamps are not a solution
    -- time and their values are not a revision.
    SELECT
        event_id,
        source_area_code,
        magnitude,
        intensity_rank,
        solution_latency_s,
        handover_lag_s,
        magnitude
            - LAG(magnitude, 1)
              OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS magnitude_delta,
        intensity_rank
            - LAG(intensity_rank, 1)
              OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS intensity_rank_delta
    FROM Bulletins
    WHERE info_type <> 'CANCELLED'
)
SELECT
    System.Timestamp() AS window_end,
    source_area_code,

    -- M1  time to determined solution
    -- magnitude IS NOT NULL is the test for "this bulletin carries a
    -- determined source solution" (see assumptions)
    AVG(CASE WHEN magnitude IS NOT NULL THEN solution_latency_s ELSE NULL END)
        AS avg_time_to_solution_s,
    MAX(CASE WHEN magnitude IS NOT NULL THEN solution_latency_s ELSE NULL END)
        AS worst_time_to_solution_s,
    SUM(CASE WHEN magnitude IS NOT NULL THEN 1 ELSE 0 END)
        AS determined_solutions,
    -- I would prefer a 95th percentile here, but I could not verify the exact
    -- ASA spelling of PERCENTILE_CONT inside a windowed GROUP BY, so it is left
    -- commented out rather than written wrongly:
    -- PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY CAST(solution_latency_s AS float))
    --     OVER (PARTITION BY source_area_code) AS p95_time_to_solution_s,

    -- M2  magnitude revision against the previous bulletin of the same event
    MAX(magnitude_delta) AS largest_magnitude_upgrade,
    MIN(magnitude_delta) AS largest_magnitude_downgrade,
    SUM(CASE WHEN ABS(magnitude_delta) >= 0.5 THEN 1 ELSE 0 END)
        AS material_magnitude_revisions,   -- 0.5 is an operator threshold, not a JMA one

    -- M3  seismic-intensity escalation, in steps on the declared shindo ordering
    MAX(intensity_rank_delta) AS largest_intensity_escalation_steps,
    SUM(CASE WHEN intensity_rank_delta > 0 THEN 1 ELSE 0 END)
        AS escalating_bulletins,
    MAX(intensity_rank) AS peak_intensity_rank,

    -- M4  distinct-event rate and revision load for this source region
    COUNT(DISTINCT event_id) AS distinct_events,   -- unsure whether ASA permits
                                                   -- COUNT(DISTINCT) here; if not,
                                                   -- it must be pre-aggregated upstream
    COUNT(*) AS bulletins,
    CASE WHEN COUNT(DISTINCT event_id) > 0
         THEN CAST(COUNT(*) AS float) / COUNT(DISTINCT event_id)
         ELSE NULL
    END AS bulletins_per_event,
    MAX(magnitude) AS largest_magnitude,   -- max only: order-preserving, no arithmetic

    -- M5  distribution handover lag
    AVG(handover_lag_s) AS avg_handover_lag_s,
    MAX(handover_lag_s) AS worst_handover_lag_s

INTO output
FROM Revised
-- Window: HoppingWindow, 60-minute window advancing every 5 minutes. One hour
-- is long enough to hold a short aftershock burst; the 5-minute hop keeps the
-- swarm signal from waiting a whole window. Partitioned by source_area_code,
-- derived from epicenter_area_code, which the schema declares as the
-- featureOfInterest naming the seismic source region.
GROUP BY source_area_code, HoppingWindow(minute, 60, 5)
```

## 3. What I did not compute

- **Distance between successive hypocentres of one event, and epicentre clustering between events.** The schema declares EPSG:4326 over `latitude` and `longitude`, so the coordinates are geographically interpretable, but a distance needs an Earth radius and a geodesic formula, and neither file supplies either. `latitude`, `longitude` and `depth_km` are also *omitted* members rather than nullable ones, so a `LAG` over them would silently compare a bulletin that has coordinates against one that never had any.
- **`AVG(magnitude)` and `STDEV(magnitude)`.** The files describe `magnitude` as dimensionless, computed from displacement amplitudes by a published formula, and "similar to Richter magnitude". Nothing there licenses treating the scale as additive, so I use `MAX(magnitude)` only, which needs the ordering and nothing else.
- **Any arithmetic mean of `max_intensity` or of `affected_prefectures[].max_intensity`.** Both are ordinal string enums. I take rank *differences* between successive bulletins and report them as a count of steps on the declared ordering, which is the weakest reading that still answers "did it get worse"; I do not average them and do not treat one step as a fixed amount of shaking.
- **Any residual of `max_intensity` against `magnitude` and `depth_km`** — that is, an "observed intensity versus expected intensity" check. The two files establish no relation between the JMA magnitude scale and the shindo scale and give no attenuation model, so such a residual would be invented.
- **A felt-area metric from `affected_prefectures`** — entry count, or growth of the array across serials, or comparison of each `affected_prefectures[].max_intensity` against the report-level `max_intensity`. The schema calls the source `int[]` a *compact* list and does not state that it enumerates every affected prefecture, so its cardinality is not a footprint and a growth between serials cannot be told apart from JMA changing how much of the list it publishes.
- **A feed-silence or staleness alarm from gaps between successive `control_datetime` values.** `origin_datetime` declares `cadence: irregular` — "Earthquakes are not scheduled, so successive values carry no period." A gap in this stream is therefore indistinguishable from a quiet period, and an alarm on it would fire on the normal state of the feed.
- **Aggregation of `tsunami_possible`.** It is marked `derivation: estimated` and the description says it is inferred from free-text comments by the bridge rather than published as a coded field. A rate over it would report the bridge's text parser, not JMA.
- **Delta of `depth_km` between successive serials.** This one is sound and computable, and I left it out only for the five-metric budget: it moves with the same hypocentre re-inversion that M2 already reports through `magnitude`.
- **A standalone `info_type` correction/cancellation rate.** Also sound, also cut for budget. `CANCELLED` is handled instead as a filter, so it does not pollute the latency and revision figures.

## 4. Assumptions

- *Assumption:* the input alias is `input` and the sink alias is `output`.
- *Assumption:* `control_datetime` is close enough to monotone in arrival order to serve as event time, and bulletins for one `event_id` reach the channel in ascending `serial` order. `LAG` therefore returns the previous *serial*. The files state that `serial` is the revision sequence but do not state that publication order follows it.
- *Assumption:* the `datetime` members arrive as RFC3339 strings and `TIMESTAMP BY` plus `CAST(... AS datetime)` accept them.
- *Assumption:* `magnitude IS NOT NULL` is a valid test for "this bulletin carries a determined source solution". The schema lists the same bulletin classes (震度速報 and the two commentary products) as the ones that omit `magnitude`, `latitude`, `longitude` and `epicenter_area_code`, which supports the equivalence but does not assert it.
- *Assumption:* the shindo enum's declared order is its severity order. The `altenums` descriptions run monotonically from "felt only by some people at rest indoors" to "people are thrown by the shaking", which is strong evidence, but the ordering itself is not declared as an ordering.
- *Assumption:* 0.5 magnitude units is a meaningful threshold for a "material" revision. It is an operator-chosen number, not a JMA-defined one, and should be tuned.
- *Assumption:* an earthquake's revision sequence completes within the 6-hour `LIMIT DURATION` on `LAG`, and one hour is a useful observation window for regional event rate. The files state no revision horizon.
- *Assumption:* `'UNLOCALISED'` is a safe sentinel for a missing `epicenter_area_code`. It is invented by this query for grouping and is not a JMA area code; those rows are bulletins issued before a hypocentre was determined.
- *Assumption:* an omitted member (`max_intensity`, `magnitude`, `epicenter_area_code`) surfaces as NULL to the query rather than as a missing column.
- *Assumption:* `COUNT(DISTINCT event_id)` is permitted inside a windowed `GROUP BY` in this dialect; if it is not, M4 needs a two-step pre-aggregation by `event_id`.


TRANSCRIPT C

# EarthquakeReport — five derived metrics

## 1. The five metrics

1. **Intensity escalation step** — the change in the ordinal rank of `max_intensity` between consecutive bulletins carrying the same `event_id`; a positive step means a revision raised the assessed shaking, which is the one change in this feed most likely to force a different downstream response.
2. **Bulletin latency**, decomposed — `DATEDIFF(second, origin_datetime, control_datetime)`, split into analysis lag (`origin_datetime`→`report_datetime`) and publication lag (`report_datetime`→`control_datetime`); it tells the operator how late the news is *and* which half of the producer's pipeline is responsible.
3. **Missed-bulletin count** — gaps in `serial` between consecutive observed bulletins of an event (`serial - prev_serial - 1`); a numbered sequence is the only thing in this record that lets you notice silent loss, and losing a bulletin means running on a superseded intensity.
4. **Magnitude revision drift** — `ABS(magnitude - prev_magnitude)` between consecutive bulletins of the same event; it measures how much the solution moves after first publication, i.e. how much an early bulletin can be trusted.
5. **Amendment share** — the fraction of an event's bulletins whose `info_type` is `CORRECTED` or `CANCELLED`, with a separate cancelled flag; a retraction rate is the cheapest available quality signal for the feed and for the individual event.

## 2. The query

```sql
-- Azure Stream Analytics / Fabric Eventstream SQL operator.
-- Event time is control_datetime (see assumptions). Aggregation window:
-- TumblingWindow(minute, 10), partitioned by event_id, which is the only
-- member that identifies an individual source (one earthquake, many bulletins).

WITH Bulletins AS (
    SELECT
        event_id,
        serial,
        info_type,
        magnitude,
        max_intensity,
        -- Metric 2: latency and its two additive halves.
        DATEDIFF(second, origin_datetime, report_datetime)   AS analysis_lag_sec,
        DATEDIFF(second, report_datetime,  control_datetime) AS publish_lag_sec,
        DATEDIFF(second, origin_datetime,  control_datetime) AS total_latency_sec,
        -- Ordinal rank taken from the order in which the max_intensity enum is
        -- declared. max_intensity is NOT in "required", so this is NULL whenever
        -- the member is absent, and every metric built on it is null-guarded.
        CASE
            WHEN max_intensity = '1'  THEN 1
            WHEN max_intensity = '2'  THEN 2
            WHEN max_intensity = '3'  THEN 3
            WHEN max_intensity = '4'  THEN 4
            WHEN max_intensity = '5-' THEN 5
            WHEN max_intensity = '5+' THEN 6
            WHEN max_intensity = '6-' THEN 7
            WHEN max_intensity = '6+' THEN 8
            WHEN max_intensity = '7'  THEN 9
            ELSE NULL
        END AS intensity_rank
    FROM input TIMESTAMP BY control_datetime
),

Sequenced AS (
    -- Reach the previous bulletin of the SAME earthquake. LIMIT DURATION is
    -- mandatory; 6 hours is an operational choice, not something the files state.
    -- LAG runs before the GROUP BY, so a comparison still works when the two
    -- bulletins land in different tumbling windows.
    SELECT
        event_id,
        serial,
        info_type,
        analysis_lag_sec,
        publish_lag_sec,
        total_latency_sec,
        intensity_rank,
        magnitude,
        LAG(intensity_rank, 1) OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_intensity_rank,
        LAG(magnitude, 1)      OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_magnitude,
        LAG(serial, 1)         OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_serial
    FROM Bulletins
),

Derived AS (
    SELECT
        event_id,
        intensity_rank,
        total_latency_sec,
        analysis_lag_sec,
        publish_lag_sec,
        -- Metric 1. Negative values are downgrades; NULL when either bulletin
        -- omitted max_intensity.
        CASE WHEN intensity_rank IS NULL OR prev_intensity_rank IS NULL
             THEN NULL
             ELSE intensity_rank - prev_intensity_rank
        END AS intensity_step,
        -- Metric 4. magnitude is optional and nullable, so guard both sides.
        CASE WHEN magnitude IS NULL OR prev_magnitude IS NULL
             THEN NULL
             ELSE ABS(magnitude - prev_magnitude)
        END AS magnitude_drift,
        -- Metric 3. Only detects gaps BETWEEN observed bulletins; if the first
        -- bulletin we see already has serial 2 (as the example does) we cannot
        -- tell whether 0 and 1 were lost or never existed, so we score 0.
        CASE WHEN prev_serial IS NULL THEN 0
             WHEN serial - prev_serial > 1 THEN serial - prev_serial - 1
             ELSE 0
        END AS serial_gap,
        -- Metric 5.
        CASE WHEN info_type = 'CORRECTED' OR info_type = 'CANCELLED' THEN 1 ELSE 0 END AS is_amendment,
        CASE WHEN info_type = 'CANCELLED' THEN 1 ELSE 0 END AS is_cancelled
    FROM Sequenced
)

SELECT
    System.Timestamp()                  AS window_end,
    event_id,
    COUNT(*)                            AS bulletins,               -- context / denominator
    MAX(intensity_rank)                 AS peak_intensity_rank,     -- context for metric 1
    MAX(intensity_step)                 AS max_intensity_step,      -- metric 1
    MAX(total_latency_sec)              AS worst_total_latency_sec, -- metric 2
    AVG(total_latency_sec)              AS avg_total_latency_sec,   -- metric 2
    AVG(analysis_lag_sec)               AS avg_analysis_lag_sec,    -- metric 2 (split)
    AVG(publish_lag_sec)                AS avg_publish_lag_sec,     -- metric 2 (split)
    SUM(serial_gap)                     AS missed_bulletins,        -- metric 3
    MAX(magnitude_drift)                AS max_magnitude_drift,     -- metric 4
    SUM(is_amendment) * 1.0 / COUNT(*)  AS amendment_share,         -- metric 5
    MAX(is_cancelled)                   AS cancelled_flag           -- metric 5
INTO output
FROM Derived
GROUP BY event_id, TumblingWindow(minute, 10)
```

Deliberate syntax choices, so that nothing here rests on a construct I cannot
check: searched `CASE` rather than the simple `CASE expr WHEN` form; `OR`
rather than an `IN` list; no `CROSS APPLY GetArrayElements`, no geospatial
functions, no `PERCENTILE_CONT`.

## 3. What I did not compute

* **Residual between `max_intensity` and `MAX(affected_prefectures[].max_intensity)`.** An internal-consistency check, and in the one example the two agree ("4"). Left out because nothing in the schema says the top-level member is *defined* as the maximum over that array — the array may enumerate only the prefectures the producer chose to list. Computing it would also need `CROSS APPLY GetArrayElements(affected_prefectures)`, which I cannot confirm the Fabric SQL operator accepts.
* **Epicentre drift between revisions, from `latitude`, `longitude` and `depth_km`.** A delta in degrees is not a distance (a degree of longitude shrinks with latitude), a real great-circle distance needs trigonometry or `ST_DISTANCE`/`CreatePoint` whose availability here I cannot verify, and all three members are optional so the per-event series is gappy.
* **Tsunami transition on `tsunami_possible`.** A false→true flip across revisions would be highly actionable, but the member is required *and* nullable and the files assign no meaning to null. A null→true step cannot be distinguished from "the earlier bulletin simply did not carry a value", and treating null as false would be inventing a fact.
* **Energy or seismic-moment aggregation from `magnitude`.** The schema gives `magnitude` no scale, no unit and no bounds. Any exponential energy conversion, or summing releases over a window, would be imported domain knowledge.
* **Depth banding of `depth_km`** into shallow / intermediate / deep. No thresholds are declared anywhere in the two files; only the range 0–700 is.
* **Feed-wide latency percentiles** — `PERCENTILE_CONT` over `total_latency_sec`. The statement is grouped by `event_id`, and a single event contributes too few bulletins for a percentile to be meaningful. A useful percentile needs a second output grouped only by the window, which a single statement cannot emit alongside this one.
* **Mix ratios over `bulletin_type` and `epicenter_area_code`.** The enum members `VXSE51`…`VYSE52` and the area codes have no stated meaning in either file, so a share-per-type figure would not be interpretable; `epicenter_area_code` is also optional and nullable.
* **Event-arrival rate as a seismicity rate, and aftershock-sequence clustering.** Both would require assuming the feed is complete and inventing a space/time threshold for "same sequence".
* **Inter-bulletin interval**, `DATEDIFF(second, prev_control_datetime, control_datetime)`. Dropped as largely redundant with `bulletins` counted over a fixed 10-minute window.
* **Parsing `event_id` as a timestamp.** Its 14 digits equal `origin_datetime` in the single example, but the schema declares only `^[0-9]{14}$`. It is used strictly as an opaque partition key.

## 4. Assumptions

* *Assumption:* `control_datetime` is the publication-side timestamp and is non-decreasing in the order records are produced, which is why it is the event time. The only support is the single example (14:38:12 ≥ 14:38:00 ≥ 14:32:07). `origin_datetime` was rejected because every revision of one earthquake repeats it, which would collapse a whole bulletin sequence onto one instant.
* *Assumption:* `event_id` is stable across revisions and identifies one earthquake. The schema never says so; the example's `report_id` of `20260729143207_2` = `event_id` + `_` + `serial` is what suggests it.
* *Assumption:* `serial` increments by exactly 1 per new bulletin of an event, so `serial - prev_serial - 1` counts missed bulletins. The schema states only `integer, minimum 0`.
* *Assumption:* the declaration order of the `max_intensity` enum (`1,2,3,4,5-,5+,6-,6+,7`) is ascending severity. The file declares the order; it does not declare that the order means severity. Ranks 1–9 are mine.
* *Assumption:* all revisions of one event arrive inside `LIMIT DURATION(hour, 6)`. Nothing states how long an event remains under revision.
* *Assumption:* `TumblingWindow(minute, 10)` is a reasonable reporting cadence. The files establish no cadence at all; this number is arbitrary and should be tuned.
* *Assumption:* an absent `max_intensity` or a null `magnitude` means "not carried in this bulletin", not zero. Both are outside `required`, so every metric touching them is null-guarded and simply yields no value rather than a false one.
* *Assumption:* records reach the query in approximately `control_datetime` order, within whatever out-of-order tolerance the job is configured with.
* *Assumption:* the input and output aliases are `input` and `output`.
* *Assumption / limitation:* latency is measured entirely inside the record's own clock domain. The record carries no ingestion or arrival timestamp, so true end-to-end delivery lag from producer to this query is not observable from these two files.


TRANSCRIPT D

# Five derived metrics for the JMA `EarthquakeReport` stream

## 1. The five metrics

1. **Solution latency** — `report_datetime` minus `origin_datetime`, in seconds, summarised per window as mean, p95 and max. The schema states that the report time is when the hypocentre and magnitude solution *became available* and that it is later than and independent of the origin time, so this difference is real production time between rupture and a usable answer. It is the feed's core service level, and the tail matters far more than the mean.
2. **Magnitude revision between successive bulletins of the same earthquake** — current `magnitude` minus the previous serial's `magnitude`, partitioned by `event_id`, reported as the largest upward and largest downward revision in the window and the number of bulletins that moved. `event_id` is explicitly shared across serials and `magnitude` is a computed solution, so revision is expected; an operator needs to know whether a number already acted on is still moving, and in which direction.
3. **Distinct-event rate** — count of distinct `event_id` per window. Seismic bulletin traffic is bursty; a jump in the number of separate earthquakes referenced per window is the aftershock/swarm signal and simultaneously the load signal for anything consuming the feed.
4. **Amendment share** — fraction of bulletins in the window whose `info_type` is not `ISSUED`, together with the outright `CANCELLED` count. `CANCELLED` retracts a bulletin, so downstream state built on it must be unwound; a rising amendment share is the trust indicator for the feed as a whole.
5. **Distribution latency** — `control_datetime` minus `report_datetime`, in seconds, mean and max per window. The schema goes out of its way to separate completion of the solution from handover into the distribution channel. Splitting this from metric 1 tells the operator whether a delay belongs to JMA's analysis or to the distribution path — different owner, different remedy.

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
--
-- Event time is report_datetime: the instant this bulletin's solution became
-- available, and the only one of the three timestamps that distinguishes the
-- serials of a single earthquake. origin_datetime is deliberately NOT the event
-- time -- every serial of one event repeats it, so a whole revision sequence
-- would collapse onto a single instant and LAG would have no ordering to work
-- with. control_datetime is a distribution-channel artefact, so using it would
-- fold channel delay into the window boundaries.
WITH Bulletins AS
(
    -- Record grain. Per-source partitioning happens here: event_id is the only
    -- member that identifies "one source" in the sense of a series of records
    -- describing the same thing over time. LIMIT DURATION is required on LAG.
    SELECT
        event_id,
        serial,
        info_type,
        magnitude,
        DATEDIFF(second, origin_datetime, report_datetime)  AS solution_latency_s,
        DATEDIFF(second, report_datetime, control_datetime) AS distribution_latency_s,
        LAG(magnitude, 1) OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_magnitude,
        LAG(serial,    1) OVER (PARTITION BY event_id LIMIT DURATION(hour, 6)) AS prev_serial
    FROM input TIMESTAMP BY report_datetime
),
Derived AS
(
    SELECT
        event_id,
        solution_latency_s,
        distribution_latency_s,
        -- Only a genuine forward revision counts. serial > prev_serial guards
        -- against a re-delivered or out-of-order bulletin being read as a
        -- magnitude change. NULL magnitudes (震度速報 and similar bulletins that
        -- carry no magnitude) yield NULL and drop out of the aggregate.
        CASE
            WHEN magnitude      IS NOT NULL
             AND prev_magnitude IS NOT NULL
             AND prev_serial    IS NOT NULL
             AND serial > prev_serial
            THEN magnitude - prev_magnitude
        END AS magnitude_revision,
        CASE WHEN info_type <> 'ISSUED'    THEN 1 ELSE 0 END AS is_amended,
        CASE WHEN info_type  = 'CANCELLED' THEN 1 ELSE 0 END AS is_cancelled
    FROM Bulletins
)
SELECT
    System.Timestamp()                          AS window_end,
    COUNT(*)                                    AS bulletin_count,

    -- Metric 3: distinct-event rate.
    COUNT(DISTINCT event_id)                    AS distinct_event_count,

    -- Metric 1: solution latency, origin -> report.
    AVG(solution_latency_s)                     AS avg_solution_latency_s,
    MAX(solution_latency_s)                     AS max_solution_latency_s,
    -- The prompt states PERCENTILE_CONT is available. In the product it is an
    -- analytic function taking an OVER clause; I am not certain this exact form
    -- composes with the tumbling GROUP BY in a single pass. If it is rejected,
    -- drop this line -- avg and max above still carry the metric.
    PERCENTILE_CONT(0.95) OVER (ORDER BY solution_latency_s) AS p95_solution_latency_s,

    -- Metric 2: magnitude revision across serials of the same event_id.
    MAX(magnitude_revision)                     AS largest_magnitude_upgrade,
    MIN(magnitude_revision)                     AS largest_magnitude_downgrade,
    SUM(CASE WHEN magnitude_revision IS NOT NULL THEN 1 ELSE 0 END)
                                                AS bulletins_with_magnitude_change,

    -- Metric 4: amendment share and cancellations.
    CAST(SUM(is_amended) AS float) / COUNT(*)   AS amended_share,
    SUM(is_cancelled)                           AS cancelled_count,

    -- Metric 5: distribution latency, report -> control.
    AVG(distribution_latency_s)                 AS avg_distribution_latency_s,
    MAX(distribution_latency_s)                 AS max_distribution_latency_s
INTO output
FROM Derived
-- Tumbling window, 15 minutes, non-overlapping. Tumbling rather than hopping or
-- sliding because metrics 3 and 4 are counts and shares that must not be
-- double-counted across overlapping windows.
GROUP BY TumblingWindow(minute, 15)
```

The window-level `GROUP BY` deliberately does **not** include `event_id`. Metrics 3 and 4 are cross-event by construction — grouping by `event_id` would make `COUNT(DISTINCT event_id)` identically 1. Per-earthquake identity is used where it belongs, in the `PARTITION BY event_id` of the two `LAG` calls, so metric 2 never compares across earthquakes.

## 3. What I did not compute

- **Great-circle relocation distance between successive serials, from `latitude` and `longitude`.** The obvious "has the hypocentre moved?" metric, and the one I most wanted. Left out because converting a degree difference to a distance needs either trigonometry or a degrees-to-kilometres constant, and the two files establish neither; a constant would be domain knowledge I imported. `depth_km` alone could be differenced safely, but a depth shift without the horizontal shift is a misleading half of the answer.
- **Escalation of `max_intensity` between serials, and any average of `max_intensity` or `affected_prefectures[].max_intensity`.** These are ordinal strings (`5-`, `5+`, `6-`), and the files establish only that a maximum is defined over them, not that the steps are equal. Subtracting or averaging encoded ranks would assert an interval scale the schema does not license. Metric 2 already gives a revision signal on a member that *is* numeric.
- **Mean or sum of `magnitude` over a window.** Each earthquake contributes a variable number of bulletins, so a window mean is weighted by revision churn rather than by seismicity, and `magnitude` is null for several bulletin types. Deduplicating to the latest serial per event first would fix the weighting but not the second problem: the files do not establish that JMA magnitudes are additively combinable, so the mean has no stated meaning.
- **Any inter-arrival interval or missed-report residual built on gaps between `origin_datetime` values.** The schema says outright that earthquakes are not scheduled and that successive origin times carry no period. A "time since last event" or an expected-arrival residual would present noise as a signal. Counting events per fixed window (metric 3) is a rate and is not the same claim.
- **A windowed rate over `tsunami_possible`.** The schema says the value is inferred from free-text comments by the bridge and is an estimate of the bulletin's intent, not a published coded field, and it is nullable. Aggregating it would turn an inference into a measurement.
- **Ranking `bulletin_type` as a solution-maturity ordinal.** The description calls it "the scale on which the maturity of the solution is expressed", which is tempting, but the enum (`VXSE51`, `VXSE52`, `VXSE53`, `VXSE5k`, `VXSE61`, `VYSE52`) is given without any stated order. I would have to invent the ranking.
- **Grouping any aggregate by `epicenter_area_code`.** It is nullable, and the bulletin types that omit it are named in the schema. Grouping on it would silently exclude exactly those bulletins and bias every count, and the files supply no mapping from code to region beyond the name.
- **Breadth of the felt footprint, `GetArrayLength(affected_prefectures)`.** Sound and computable, and it ranked sixth — it lost to the five above rather than being unsound. I am also not fully certain of the array-length function name in this dialect.

## 4. Assumptions

- **Assumption:** `report_datetime` is non-decreasing across the serials of one `event_id`, so `LAG` ordered by event time returns the immediately preceding revision. The `serial > prev_serial` guard limits the damage if it is not, but does not fully repair it.
- **Assumption:** all revisions of an earthquake arrive within 6 hours of one another, which is what `LIMIT DURATION(hour, 6)` encodes. The files state nothing about how long a revision sequence stays open.
- **Assumption:** the 15-minute tumbling window is arbitrary. The files establish no cadence for this feed — indeed they deny one — so the size must come from the operator's alerting interval, not from the data.
- **Assumption:** `origin_datetime <= report_datetime <= control_datetime`, so both latencies are non-negative. The schema states report is later than origin; for control it says only that it records handover of the *finished* bulletin, which implies but does not state ordering. A negative value in either column should be treated as a clock or pipeline fault, not as a fast solution.
- **Assumption:** the RFC3339 strings in `origin_datetime`, `report_datetime` and `control_datetime` are parsed into datetime values by the ingest, so `DATEDIFF` receives datetimes and not strings. If they arrive as strings an explicit `CAST(... AS datetime)` is needed on each.
- **Assumption:** `COUNT(DISTINCT event_id)` is supported inside a windowed aggregate in this dialect.
- **Assumption (semantic, and the weakest one):** the distinct-event count in a window counts earthquakes *referenced* in that window, not earthquakes that *ruptured* in it. Because the window is on `report_datetime`, a late revision of an older earthquake contributes to the current window. I chose not to filter to first bulletins because the files do not establish whether the first serial is 0 or 1 — `serial` has a minimum of 0, and the one instance available carries serial 2.
