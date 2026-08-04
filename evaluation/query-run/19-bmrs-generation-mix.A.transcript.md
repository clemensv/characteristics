# GenerationMix — five derived metrics

## 1. The five metrics

1. **`total_mw` — the summed level across the whole closed member set.** The schema is `additionalProperties: false`, so the seventeen `_mw` members *are* the record; their sum is the only complete level the feed carries, and it is the denominator every other proportional metric needs.
2. **`ramp_mw_per_min` — signed change in `total_mw` between successive records, divided by the elapsed wall time between their `start_time` values.** An operator acts on rate of change, not level: a large negative ramp is the shape of a loss, a large positive ramp the shape of a pick-up, and both are invisible in the raw record.
3. **`net_int_mw` and `int_share_pct` — the signed sum of the seven `int`-prefixed members, and that sum as a percentage of `total_mw`.** The instance shows `intnem_mw` and `intelec_mw` negative while `intfr_mw`, `intifa2_mw`, `intned_mw`, `intnsl_mw`, `intvkl_mw` are positive, so this subgroup is the one part of the record demonstrated to reverse sign; its net and its weight tell the operator how much of the level is coming from a direction that can flip.
4. **`stdev_total_mw` and `range_total_mw` — dispersion of `total_mw` within the window.** Two records can share a mean and differ entirely in how settled they were; volatility is what distinguishes a steady window from one that was chased, and it is the natural threshold on which to alarm.
5. **`avg_member_completeness_pct` and `period_breaks_in_window` — the share of the seventeen optional `_mw` members actually present, and the count of `settlement_period` steps that were not `+1`.** Only `settlement_period` and `start_time` are required, so a record missing twelve members still parses and still produces a `total_mw` that is silently too low; this metric says whether the other four are computed on a whole record and an unbroken sequence, or not.

## 2. The query

```sql
-- Single statement.
--
-- PARTITIONING: nothing in GenerationMix identifies an individual source.
-- There is no id, station, region or unit member; `settlement_period` is a
-- bounded cycle index (1..50), not an identity. So there is no PARTITION BY
-- anywhere in this query and the feed is treated as one series.
--
-- DIALECT NOTE: COALESCE, ABS and CASE are used below and were not named in
-- the dialect notes I was given. I believe all three are supported here, but
-- I am flagging them as the one place I could not check. If COALESCE is
-- unavailable, each `COALESCE(x, 0)` becomes `CASE WHEN x IS NULL THEN 0
-- ELSE x END`; if ABS is unavailable, `MAX(ABS(r))` becomes
-- `MAX(CASE WHEN r < 0 THEN -r ELSE r END)`.

WITH Levels AS (
    SELECT
        System.Timestamp()  AS event_time,
        settlement_period,

        -- METRIC 1. Sum over the closed member set. `additionalProperties` is
        -- false, so these seventeen members are exhaustive for this type and
        -- the sum is complete by construction. COALESCE because every _mw
        -- member is optional -- only settlement_period and start_time are
        -- required -- and one NULL would otherwise null the whole total.
          COALESCE(ccgt_mw,    0) + COALESCE(ocgt_mw,   0)
        + COALESCE(coal_mw,    0) + COALESCE(oil_mw,    0)
        + COALESCE(nuclear_mw, 0) + COALESCE(wind_mw,   0)
        + COALESCE(biomass_mw, 0) + COALESCE(npshyd_mw, 0)
        + COALESCE(ps_mw,      0) + COALESCE(other_mw,  0)
        + COALESCE(intfr_mw,   0) + COALESCE(intifa2_mw, 0)
        + COALESCE(intned_mw,  0) + COALESCE(intnem_mw,  0)
        + COALESCE(intelec_mw, 0) + COALESCE(intnsl_mw,  0)
        + COALESCE(intvkl_mw,  0)                             AS total_mw,

        -- METRIC 3 (part). Signed net of the seven int-prefixed members.
        -- Deliberately NOT wrapped in ABS: the instance carries intnem_mw and
        -- intelec_mw negative alongside five positive siblings, so the sign of
        -- this sum is information, and the cancellation inside it is real.
          COALESCE(intfr_mw,   0) + COALESCE(intifa2_mw, 0)
        + COALESCE(intned_mw,  0) + COALESCE(intnem_mw,  0)
        + COALESCE(intelec_mw, 0) + COALESCE(intnsl_mw,  0)
        + COALESCE(intvkl_mw,  0)                             AS net_int_mw,

        -- METRIC 5 (part). How many of the seventeen optional _mw members this
        -- record actually carried. Conditions the trustworthiness of total_mw.
          (CASE WHEN ccgt_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN ocgt_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN coal_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN oil_mw     IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN nuclear_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN wind_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN biomass_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN npshyd_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN ps_mw      IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN other_mw   IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intfr_mw   IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intifa2_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intned_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intnem_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intelec_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intnsl_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intvkl_mw  IS NOT NULL THEN 1 ELSE 0 END) AS members_present

    -- start_time is the only datetime member in the schema, so it is the only
    -- candidate for event time. No PARTITION BY: see header note.
    FROM input TIMESTAMP BY start_time
),

Deltas AS (
    -- Reach the previous record. No PARTITION BY, for the reason above.
    -- LIMIT DURATION(hour, 2) is required by the dialect; two hours is four
    -- times the assumed 30-minute cadence, so it survives up to three
    -- consecutive dropped periods before LAG returns NULL.
    SELECT
        event_time,
        settlement_period,
        total_mw,
        net_int_mw,
        members_present,
        LAG(total_mw, 1)          OVER (LIMIT DURATION(hour, 2)) AS prev_total_mw,
        LAG(settlement_period, 1) OVER (LIMIT DURATION(hour, 2)) AS prev_period,
        DATEDIFF(second,
                 LAG(event_time, 1) OVER (LIMIT DURATION(hour, 2)),
                 event_time)                                     AS gap_seconds
    FROM Levels
),

Rates AS (
    SELECT
        event_time,
        total_mw,
        net_int_mw,
        members_present,

        -- METRIC 2. Signed MW per minute. NULL rather than 0 on the first
        -- record and on any non-positive elapsed time, so that a missing
        -- comparison never masquerades as a flat ramp in the AVG below.
        CASE
            WHEN prev_total_mw IS NULL OR gap_seconds IS NULL OR gap_seconds <= 0
                THEN NULL
            ELSE (total_mw - prev_total_mw) * 60.0 / gap_seconds
        END AS ramp_mw_per_min,

        -- METRIC 3 (part). Share is only defined against a positive
        -- denominator; the schema places no lower bound on any _mw member, so
        -- total_mw is not guaranteed positive and the share is nulled when it
        -- is not.
        CASE
            WHEN total_mw > 0 THEN 100.0 * net_int_mw / total_mw
            ELSE NULL
        END AS int_share_pct,

        -- METRIC 5 (part). settlement_period is declared 1..50 and is assumed
        -- to advance by exactly one per record. A step to 1 is treated as a
        -- cycle reset, not a break, because the schema fixes only the upper
        -- bound (50) and not the cycle length, so the value the sequence
        -- resets *from* is not knowable here.
        CASE
            WHEN prev_period IS NULL                       THEN 0
            WHEN settlement_period = prev_period + 1       THEN 0
            WHEN settlement_period = 1                     THEN 0
            ELSE 1
        END AS period_break
    FROM Deltas
)

-- Window: HoppingWindow(minute, 180, 30) -- a 180-minute window advancing in
-- 30-minute hops. Size chosen to hold six records and hop chosen to emit once
-- per record, both under the assumed 30-minute cadence (assumption 3). Six
-- samples is the smallest window on which STDEV is worth reading; the hop
-- keeps the alarm latency down to one settlement period rather than one
-- window.
SELECT
    System.Timestamp()                                  AS window_end,
    COUNT(*)                                            AS records_in_window,

    -- 1. level
    AVG(total_mw)                                       AS avg_total_mw,
    MIN(total_mw)                                       AS min_total_mw,
    MAX(total_mw)                                       AS max_total_mw,

    -- 2. rate of change
    AVG(ramp_mw_per_min)                                AS avg_ramp_mw_per_min,
    MAX(ABS(ramp_mw_per_min))                           AS peak_abs_ramp_mw_per_min,

    -- 3. int-prefixed subgroup, signed
    AVG(net_int_mw)                                     AS avg_net_int_mw,
    MIN(net_int_mw)                                     AS min_net_int_mw,
    AVG(int_share_pct)                                  AS avg_int_share_pct,

    -- 4. dispersion
    STDEV(total_mw)                                     AS stdev_total_mw,
    MAX(total_mw) - MIN(total_mw)                       AS range_total_mw,

    -- 5. integrity of the four above
    AVG(CAST(members_present AS float)) * 100.0 / 17.0  AS avg_member_completeness_pct,
    SUM(period_break)                                   AS period_breaks_in_window
INTO output
FROM Rates
GROUP BY HoppingWindow(minute, 180, 30)
```

Sanity check against the one instance: `total_mw` = 22 871 (the ten non-`int` members) + 5 588 (the seven `int` members) = 28 459; `net_int_mw` = 5 588; `int_share_pct` = 19.64; `members_present` = 17, so completeness = 100 %.

## 3. What I did not compute

* **Per-member share of `total_mw` for each of the seventeen `_mw` members.** A share presumes the parts partition a whole. `intnem_mw` is −412.0 and `intelec_mw` is −184.0 in the instance, so the members do not partition `total_mw`; percentages over a set containing negatives sum to 100 % only by accident and are not comparable between records. I compute a share only for the aggregated `net_int_mw`, and interpret it as signed.
* **A Herfindahl or any concentration/diversity index over the members.** It requires squaring non-negative shares. `intnem_mw` and `intelec_mw` are negative; dropping them to force non-negativity would silently change the denominator, so the index would not be comparable record to record.
* **Any grouping of `ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw` as one class, or of `wind_mw`, `npshyd_mw`, `biomass_mw`, `ps_mw` as another.** The schema declares no such taxonomy — no enum, no annotation, no grouping construct — and the instance does not imply one. That classification is domain knowledge these two files do not carry, so no "thermal", "renewable", "low-carbon" or "dispatchable" aggregate appears above. The one grouping I did make, the seven `int`-prefixed members, rests on the shared name prefix alone and is flagged as assumption 2.
* **A reconciliation residual: reported total minus computed total.** This is the metric an operator of a summed feed most wants, and the feed cannot support it. There is no total member, and `additionalProperties: false` means one cannot arrive later. Nothing declares a reference for `total_mw` to be checked against, so no residual is computed.
* **Capacity factor, utilisation, or headroom for any member.** No nameplate, capacity, availability or limit member exists in the schema. Every such ratio would require a denominator I would have to invent.
* **A negative-value error flag on `ccgt_mw`, `coal_mw`, `nuclear_mw` and the other non-`int` members.** The schema author declared `minimum: 1` and `maximum: 50` on `settlement_period` and declared no bounds at all on any `_mw` member. They demonstrably knew how to constrain a value and chose not to constrain these, so a negative `coal_mw` is not licensed as an anomaly and I do not flag it.
* **Any charge/discharge, state-of-charge or round-trip treatment of `ps_mw`.** Nothing in the schema or the instance establishes that `ps_mw` is a store or that it is bidirectional; it is +742.0 in the one record available. It is summed into `total_mw` like every other member and given no special handling.
* **`SessionWindow` for outage detection.** Considered as the mechanism for metric 5. Rejected because `settlement_period` gives a direct, schema-licensed sequence test (`prev_period + 1`) that needs no timeout parameter, whereas a session timeout is a number I would have had to invent.
* **`PERCENTILE_CONT` on `total_mw`.** Available in the dialect and sound here, but over the six records a 180-minute window holds it adds nothing `MIN`, `MAX` and `STDEV` do not already say. Omitted as padding.
* **Suppressing the ramp across a `settlement_period` reset to 1.** Not done deliberately: `ramp_mw_per_min` divides by elapsed wall clock from `start_time`, which is well defined across a cycle boundary. Only the `period_break` flag treats the reset specially.

## 4. Assumptions

1. **Assumption — the `_mw` suffix means megawatts, and all seventeen members share that unit, so they may be added.** The schema declares no unit anywhere. Its `$uses` list names only `JSONStructureValidation`, so no units extension is in play; the unit exists solely in the member names. Every sum, ramp and share above fails if the members are not commensurable.
2. **Assumption — the `int` prefix marks a coherent subgroup**, so that `intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`, `intelec_mw`, `intnsl_mw` and `intvkl_mw` are the same kind of thing and their signed sum is meaningful. This rests on the shared prefix and on the observation that these are the only members negative in the instance. Nothing in the schema declares the group.
3. **Assumption — the cadence is one record per 30 minutes.** Inferred from a single instance: `settlement_period` 12 with `start_time` 2026-07-31T05:30:00Z is consistent with period *n* beginning (*n* − 1) × 30 minutes after midnight, and `maximum: 50` is consistent with a cycle of roughly a day at that spacing. One record is weak evidence. The `HoppingWindow(minute, 180, 30)` hop, the window size, and the `LIMIT DURATION(hour, 2)` on both `LAG` calls all depend on this; if the cadence differs, all three need re-sizing, though the metrics themselves do not change.
4. **Assumption — `settlement_period` advances by exactly one between consecutive records and resets to 1 at the start of each cycle.** The schema bounds it 1..50 but says nothing about its progression. `period_break` is built on this, and treats a step to 1 as a legitimate reset rather than a break.
5. **Assumption — `start_time` is the start of the interval the record describes, not the time the record was produced.** Taken from the member name. Consequence: `TIMESTAMP BY start_time` stamps each record at the opening of its interval, so a window closing at *T* includes a record whose interval is still running past *T*. Every windowed figure is therefore aligned on interval starts, not on interval coverage.
6. **Assumption — records are not revised or republished.** If the feed restates a settlement period, `LAG` compares the restatement against the record before it and `ramp_mw_per_min` is wrong for two consecutive outputs. Nothing in the two files establishes revision behaviour, and there is no version, sequence or revision member to detect it with.
7. **Assumption — a missing optional `_mw` member means the quantity is absent, and substituting 0 is the right null policy.** Every `_mw` member is optional; the alternative — nulling `total_mw` whenever any member is missing — would blank the whole metric on one absent value. `avg_member_completeness_pct` exists precisely to expose the resulting understatement, but it is an assumption that 0-substitution is preferable.
8. **Assumption — `total_mw` is positive whenever a share is meaningful.** No `_mw` member has a declared `minimum`, so a non-positive total is possible; `int_share_pct` is nulled in that case rather than returning a signed or infinite ratio.
9. **Assumption — the stream carries a single source.** The schema has no identifying member, which is why there is no `PARTITION BY`. This further assumes the feed does not multiplex several sources into one stream distinguished by something outside the record body, such as a partition key or a transport header; if it does, `LAG` interleaves unrelated series and metric 2 and metric 5 are both invalid.
10. **Assumption — `COALESCE`, `ABS` and `CASE` are supported in this dialect.** They were not named in the notes I was given. Substitutions for the first two are given in the query header comment.
