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
