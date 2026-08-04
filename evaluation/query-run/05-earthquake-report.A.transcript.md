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
