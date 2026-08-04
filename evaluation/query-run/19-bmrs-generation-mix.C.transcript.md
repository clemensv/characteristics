# GB generation mix — five derived metrics

## 1. The five metrics

1. **Total metered generation output (MW).** The sum of the ten fuel members (`ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw`, `nuclear_mw`, `wind_mw`, `biomass_mw`, `npshyd_mw`, `ps_mw`, `other_mw`), interconnectors deliberately excluded. No member carries it and every share below is measured against it, so it is the first number an operator reads and the denominator for the rest.
2. **Half-hour wind ramp (MW per settlement period).** `wind_mw` minus its value in the immediately preceding period, emitted only when the two `start_time` values are exactly 1800 seconds apart. This is the swing the rest of the fleet had to absorb between one period and the next, and it is the single quantity that decides whether the coming period is comfortable.
3. **Wind share of metered generation output (fraction).** `wind_mw` divided by metric 1. The headline mix number — and the one whose denominator must be named, because `wind_mw` covers only Balancing-Mechanism-metered units and the denominator excludes imports, so this is a share of the metered mix and not of GB generation.
4. **Net interconnector position (MW, positive = net import to GB).** The signed sum of the seven cable members (`intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`, `intelec_mw`, `intnsl_mw`, `intvkl_mw`), kept out of metric 1. It tells the operator how much of supply is arriving over cables and, because the sign convention is declared, when GB has flipped to net export.
5. **Six-hour wind ramp volatility (MW).** `STDEV` of metric 2 over a six-hour hopping window. A regime measure rather than an event measure: it says how much reserve the recent past has been demanding, and a step change in it is a weather front arriving.

## 2. The query

```sql
-- Azure Stream Analytics / Fabric Eventstream SQL.
-- Event time is start_time, the member tagged semanticRole "phenomenonTimeStart"
-- and the only datetime in the record. settlement_period is emitted for
-- reference but is never used in arithmetic: the schema states that the count
-- of periods per settlement day is not constant, so differencing or ordering on
-- it is wrong across a clock change.
WITH base AS (
    SELECT
        start_time,
        settlement_period,
        wind_mw,

        -- METRIC 1 - total metered generation output, fuel members only.
        -- Interconnectors are excluded: the schema states they are signed net
        -- flows on cables, not fuels, and may not be summed with generation
        -- without a decision on exports. The decision taken here is to keep
        -- them out entirely and report them separately as metric 4.
        -- ps_mw is included as OUTPUT; this total is not net of pumping demand,
        -- which the schema says is metered elsewhere and is absent from the feed.
        -- Strict '+' is intentional: only settlement_period and start_time are
        -- required, so a member may be absent, and an absent member yields NULL
        -- here rather than a silently understated total. Absence is not zero -
        -- the publisher emits explicit 0.0 (see ocgt_mw, coal_mw, oil_mw).
        ccgt_mw + ocgt_mw + coal_mw + oil_mw + nuclear_mw
            + wind_mw + biomass_mw + npshyd_mw + ps_mw + other_mw
            AS total_metered_generation_mw,

        -- METRIC 4 - net interconnector position. All seven members share the
        -- declared convention "positive for import to GB", so they are additive
        -- with each other even though they are not additive with generation.
        intfr_mw + intifa2_mw + intned_mw + intnem_mw
            + intelec_mw + intnsl_mw + intvkl_mw
            AS net_interconnector_mw

    FROM input TIMESTAMP BY start_time
),

stepped AS (
    SELECT
        start_time,
        settlement_period,
        wind_mw,
        total_metered_generation_mw,
        net_interconnector_mw,

        -- METRIC 3 - wind share of the metered generation output above.
        CASE
            WHEN total_metered_generation_mw > 0
            THEN wind_mw / total_metered_generation_mw
            ELSE NULL
        END AS wind_share_of_metered_generation,

        -- METRIC 2 - half-hour wind ramp. No PARTITION BY: nothing in the
        -- record identifies an individual source (see the note below), so LAG
        -- reaches the previous event of the single stream. The ramp is emitted
        -- only when the previous record's start_time is exactly one declared
        -- support period (PT30M = 1800 s) earlier, so a missed, duplicated or
        -- out-of-order publication produces NULL instead of a fabricated rate.
        CASE
            WHEN DATEDIFF(
                     second,
                     LAG(start_time, 1) OVER (LIMIT DURATION(hour, 2)),
                     start_time) = 1800
            THEN wind_mw - LAG(wind_mw, 1) OVER (LIMIT DURATION(hour, 2))
            ELSE NULL
        END AS wind_ramp_mw_per_period,

        -- validity guard, not a metric: observed spacing against the declared
        -- cadence of PT30M.
        DATEDIFF(
            second,
            LAG(start_time, 1) OVER (LIMIT DURATION(hour, 2)),
            start_time) AS observed_gap_seconds

    FROM base
),

wind_vol AS (
    -- METRIC 5 - HoppingWindow, 6 hours long, hopping every 30 minutes
    -- (expressed in one unit as minute, 360, 30 to stay in the three-argument
    -- same-unit form). At the declared cadence a full window holds 12 ramps;
    -- ramp_samples_6h is emitted as a validity guard so a consumer can reject
    -- the statistic when the feed has gapped.
    SELECT
        System.Timestamp() AS window_end,
        STDEV(wind_ramp_mw_per_period) AS wind_ramp_stdev_6h_mw,
        COUNT(wind_ramp_mw_per_period) AS ramp_samples_6h
    FROM stepped
    GROUP BY HoppingWindow(minute, 360, 30)
)

SELECT
    s.start_time,                          -- carried, not a metric
    s.settlement_period,                   -- carried, not a metric
    s.total_metered_generation_mw,         -- metric 1
    s.wind_ramp_mw_per_period,             -- metric 2
    s.wind_share_of_metered_generation,    -- metric 3
    s.net_interconnector_mw,               -- metric 4
    v.wind_ramp_stdev_6h_mw,               -- metric 5
    s.observed_gap_seconds,                -- guard on metric 2
    v.ramp_samples_6h                      -- guard on metric 5
INTO output
FROM stepped s
-- Attaches the six-hour window ending at this record's own event time. The hop
-- is 30 minutes, so BETWEEN 0 AND 29 selects exactly one window per record.
-- I am not certain a LEFT OUTER JOIN between a per-event step and a windowed
-- step is accepted on every compatibility level; if it is not, run the wind_vol
-- step to its own output sink and join downstream, or drop to an inner JOIN and
-- accept that the first six hours after start produce no rows.
LEFT JOIN wind_vol v
    ON DATEDIFF(minute, s, v) BETWEEN 0 AND 29
```

**Event time.** `TIMESTAMP BY start_time`, and no other member. `start_time` is the only datetime in the record and carries `semanticRole: phenomenonTimeStart`.

**Windows.** One aggregating window: `HoppingWindow(minute, 360, 30)` — a six-hour hopping window advancing every 30 minutes, one hop per declared publication. Metrics 1–4 are per-record and use no window; metric 2 uses `LAG` with `LIMIT DURATION(hour, 2)`, which is a lookback bound and not a window.

**Partitioning.** None, because nothing in the record identifies an individual source. Every member is a whole-system quantity; there is no unit, BMU, zone or publisher identifier. `settlement_period` is tagged `dcterms:identifier`, but it identifies the half-hour inside a settlement day, not a source, and the schema warns against arithmetic on it. The stream is therefore treated as a single source and `LAG` is written without `PARTITION BY`.

## 3. What I did not compute

* **A combined gas total, `ccgt_mw + ocgt_mw`.** The schema states these describe operationally unrelated fleets — CCGT is the bulk fleet dispatched for energy, OCGT runs for minutes at a time as reserve. Summing them names a fleet that does not exist operationally, and it destroys the signal that matters most in `ocgt_mw`, which is that it is non-zero at all.
* **Any net or round-trip position for pumped storage from `ps_mw`.** The schema states the pumping load does not appear as a negative value here and is metered as demand elsewhere, so `ps_mw` is not a net position and no storage balance can be formed from this feed. For the same reason I did not add `ps_mw` to `npshyd_mw` into a "hydro" total: the schema separates them precisely because only one of them is a store.
* **A total supply figure or a demand proxy, generation plus interconnectors.** The schema explicitly says the cable members may not be summed with the generation members without deciding how exports are to be treated, and a demand figure would additionally need station load, distribution-connected generation and pumping demand — none of which are in the feed.
* **A per-settlement-day energy total.** Converting a member to MWh is licensed (a mean over a stated `supportPeriod` of PT30M is `mw * 0.5` MWh), but I cannot delimit a settlement day from this feed: the schema says periods are numbered from 1 at midnight UTC and also that a day may hold 46 or 50 periods. I cannot reconcile those two statements, so I cannot say which records constitute one day, and I did not use a `settlement_period` rollover to 1 as a day boundary either.
* **Carbon intensity, or a low-carbon / renewable share.** That requires emission factors and a classification of `biomass_mw`, `other_mw` and the imported members that the two files do not establish. `other_mw` is defined only as plant whose fuel type is not reported separately, which makes it unclassifiable by construction.
* **Capacity factors, headroom, or availability.** No capacity, unit count or availability appears anywhere in the schema.
* **Per-cable flow reversal flags** (a sign change on `intnem_mw`, `intelec_mw` and the rest between consecutive periods). This is sound and computable, but without capacity or outage data a reversal cannot be told apart from a trip, so the flag would raise alerts an operator cannot act on; metric 4 already carries the aggregate direction. Left out to stay at five.
* **A synthesised period end.** The feed carries no end instant, and I did not manufacture `start_time + 30 minutes` as a second timestamp nor treat any mean as an instantaneous value at a point inside its period.

## 4. Assumptions

* **Assumption: the input carries one system and one publisher.** Nothing identifies a source, so `LAG` and the window are written unpartitioned. If two feeds were ever merged onto the same input, both the ramp and the volatility would be wrong.
* **Assumption: a settlement period is published once and never restated.** The schema says nothing about revisions or corrections. `LAG` and the hopping window assume at most one record per `start_time`; a republished period would be read as a duplicate and, because its `start_time` gap would not be 1800 seconds, would null the ramp rather than corrupt it.
* **Assumption: labelling a value by the start of its support is acceptable.** Event time is `start_time`, so a window whose end is `T` contains the values that *begin* in the preceding six hours and therefore covers phenomenon time out to `T + 30 minutes`. The feed carries no end instant, so there is no alternative anchor; the offset is stated rather than corrected.
* **Assumption: records arrive within the job's late-arrival tolerance and roughly in event-time order,** and the previous period is within the `LIMIT DURATION(hour, 2)` lookback.
* **Assumption: an absent member means "not reported", not zero.** The instance carries explicit `0.0` for `ocgt_mw`, `coal_mw` and `oil_mw`, which suggests absence and zero are distinguishable, so the totals use strict addition and go NULL rather than coalescing to zero. If the publisher in fact omits members it means to be zero, metric 1 and metric 3 will be NULL more often than they should.
* **Assumption: the ten fuel members are mutually disjoint.** The schema states disjointness only for `npshyd_mw` against `ps_mw`. If any other pair overlaps, metric 1 double counts.
* **Assumption: including `ps_mw` in metric 1 is what an operator wants.** It makes the total a gross output total. Anyone wanting a total net of storage cannot get one from this feed.
* **Assumption: the hopping window boundaries coincide with publication instants** (on the hour and half hour), which is what makes `DATEDIFF(minute, s, v) BETWEEN 0 AND 29` select exactly the window ending at the record's own time. If publication is offset from the half hour, the join must be widened and the metric-5 column will lag by one hop.
* **Assumption: a standard deviation over at most twelve ramp samples is informative enough to publish.** It is a small-sample statistic; `ramp_samples_6h` is emitted so a consumer can decide.
* **Assumption about the dialect: `LEFT OUTER JOIN` between a windowed step and a per-event step is accepted,** as flagged in the query comment.
