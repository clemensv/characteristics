# 19 — BMRS Generation Mix: five derived metrics

## 1. The five metrics

1. **`total_metered_generation_mw`** — the sum of the ten fuel-type means
   (`ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw`, `nuclear_mw`, `wind_mw`,
   `biomass_mw`, `npshyd_mw`, `ps_mw`, `other_mw`) for the settlement period.
   The record carries the mix but never the level; an operator needs the level to
   read any of the parts, and every share below divides by it.
2. **`wind_share_of_metered_generation`** — `wind_mw` divided by
   `total_metered_generation_mw`. One dimensionless number for the composition of
   the mix, and the one an operator watches because it is the part of the fleet
   that is not dispatched.
3. **`generation_ramp_mw_per_hour`** — the change in
   `total_metered_generation_mw` since the previous record, divided by the elapsed
   time between the two `start_time` values. The rate the fleet actually moved at,
   which is what sizes the flexibility a system operator must hold.
4. **`net_interconnector_mw`** — the signed sum of the seven cable flows
   (`intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`, `intelec_mw`,
   `intnsl_mw`, `intvkl_mw`), positive when GB is on balance importing. Whether
   the system is drawing on or supplying its neighbours, in one number, kept
   arithmetically apart from generation because these values are signed.
5. **`cadence_departure_flag`** (with `seconds_since_previous_period`) — the
   residual of the observed gap between successive `start_time` values against the
   `PT30M` cadence the schema declares on `start_time`. A silently missing
   half-hour corrupts metrics 1–4 without changing their type; the specification
   says a declared cadence is what "makes an absent value detectable as a gap
   rather than absorbed silently", and this is that flag.

`generation_members_present` and `interconnector_members_present` also appear in
the output. They are counters, not metrics, and are not among the five: only
`settlement_period` and `start_time` are `required`, so any `*_mw` member may be
absent, the sums go `NULL` when one is, and these counters are what make that
`NULL` interpretable.

## 2. The query

```sql
-- Grain: one row per settlement period, the grain of the feed.
-- No PARTITION BY: nothing in the record identifies a source. No member carries
--   semanticRole "featureOfInterest"; the fleet a value belongs to lives only in
--   the member name and its description. `settlement_period` is annotated
--   dcterms:identifier and identifies the period within the settlement day, not
--   a source, so it is not a partition key.
-- No windowed aggregation: see section 3.
WITH
periods AS
(
    -- TIMESTAMP BY start_time: the only member with a temporal semanticRole
    -- ("phenomenonTimeStart"), and the position on which every value member's
    -- supportPeriod (PT30M, anchor "start") is anchored.
    SELECT
        start_time,
        settlement_period,
        wind_mw,

        -- Metric 1. Ten members that share one observedProperty reference
        -- (qudt Power), one unit (MW), one statistic (mean), one
        -- phenomenonTimeRelation (interval) and one supportPeriod
        -- (PT30M, anchor start), so the sum of the means is the mean of the sum
        -- over the same half hour. NULL if any member is absent: nothing here
        -- licenses substituting zero for a value that was not recorded.
        (   ccgt_mw + ocgt_mw + coal_mw + oil_mw + nuclear_mw
          + wind_mw + biomass_mw + npshyd_mw + ps_mw + other_mw
        ) AS total_metered_generation_mw,

        (   CASE WHEN ccgt_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN ocgt_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN coal_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN oil_mw     IS NULL THEN 0 ELSE 1 END
          + CASE WHEN nuclear_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN wind_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN biomass_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN npshyd_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN ps_mw      IS NULL THEN 0 ELSE 1 END
          + CASE WHEN other_mw   IS NULL THEN 0 ELSE 1 END
        ) AS generation_members_present,

        -- Metric 4. Seven signed net flows, every one declared positive for
        -- import to GB, so they add on a common convention. Deliberately not
        -- added to the generation members.
        (   intfr_mw + intifa2_mw + intned_mw + intnem_mw
          + intelec_mw + intnsl_mw + intvkl_mw
        ) AS net_interconnector_mw,

        (   CASE WHEN intfr_mw   IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intifa2_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intned_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intnem_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intelec_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intnsl_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intvkl_mw  IS NULL THEN 0 ELSE 1 END
        ) AS interconnector_members_present

    FROM input TIMESTAMP BY start_time
),

transitions AS
(
    -- LIMIT DURATION is two hours: four beats of the declared PT30M cadence,
    -- so the previous record is still reachable across a missed beat or three.
    SELECT
        start_time,
        settlement_period,
        wind_mw,
        total_metered_generation_mw,
        generation_members_present,
        net_interconnector_mw,
        interconnector_members_present,
        LAG(start_time, 1)
            OVER (LIMIT DURATION(hour, 2)) AS prev_start_time,
        LAG(total_metered_generation_mw, 1)
            OVER (LIMIT DURATION(hour, 2)) AS prev_total_metered_generation_mw
    FROM periods
),

timed AS
(
    SELECT
        start_time,
        settlement_period,
        wind_mw,
        total_metered_generation_mw,
        generation_members_present,
        net_interconnector_mw,
        interconnector_members_present,
        prev_total_metered_generation_mw,
        DATEDIFF(second, prev_start_time, start_time)
            AS seconds_since_previous_period
    FROM transitions
)

SELECT
    -- carried, for identification only
    start_time,
    settlement_period,

    -- 1
    total_metered_generation_mw,

    -- 2. Share of the metered generation this feed reports. Not a share of GB
    -- generation: wind_mw covers only Balancing-Mechanism-metered units and the
    -- schema states it understates GB wind.
    CASE
        WHEN total_metered_generation_mw > 0
        THEN wind_mw / total_metered_generation_mw
    END AS wind_share_of_metered_generation,

    -- 3. Divided by the elapsed time actually observed, not by an assumed half
    -- hour: cadence is an expectation, not a constraint. Over a longer baseline
    -- this is still a mean rate of change, and the flag below says which.
    CASE
        WHEN seconds_since_previous_period > 0
        THEN (total_metered_generation_mw - prev_total_metered_generation_mw)
             * 3600.0 / seconds_since_previous_period
    END AS generation_ramp_mw_per_hour,

    -- 4
    net_interconnector_mw,

    -- 5. Residual against the declared PT30M cadence. A flag, not a rejection:
    -- a record whose timing departs from a declared cadence is late, not invalid.
    seconds_since_previous_period,
    CASE
        WHEN seconds_since_previous_period IS NULL THEN NULL
        WHEN seconds_since_previous_period = 1800  THEN 0
        ELSE 1
    END AS cadence_departure_flag,

    -- qualifiers on metrics 1 and 4, not metrics
    generation_members_present,
    interconnector_members_present

INTO output
FROM timed
```

## 3. What I did not compute

**Any total combining generation with interconnectors, and any demand or
net-supply figure.** `intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`,
`intelec_mw`, `intnsl_mw` and `intvkl_mw` are signed, and `intfr_mw` states
outright that it may not be summed with the generation members without first
deciding how exports are treated. Separately, `ps_mw` is not a net position — its
pumping load is metered as demand elsewhere and is absent here — so no quantity
in this record is a supply-side total against which demand could be inferred.

**Carbon intensity, or a low-carbon / fossil split.** That needs an emission
factor per fuel. Neither file states one, and the specification is explicit that a
fact an annotation does not carry must not be repaired from property names,
descriptions, labels or samples. It would have involved `coal_mw`, `oil_mw`,
`ccgt_mw`, `ocgt_mw` and `biomass_mw`, and `biomass_mw` is the member on which
the answer would actually turn.

**A combined gas figure, `ccgt_mw + ocgt_mw`.** Arithmetically unobjectionable
and semantically misleading: the schema says these are operationally unrelated
fleets, bulk energy against minutes-long reserve, and a reader given one number
would treat them as one dispatchable fleet.

**A combined hydro figure, `npshyd_mw + ps_mw`.** The schema says they are
disjoint and says why they are reported apart — only one of them is a store.
Adding them presents released stored energy as natural inflow.

**Energy in MWh, from the MW means and the `PT30M` `supportPeriod`.** The most
tempting omission. The support period is declared, so the interval length is
known; but `statistic: mean` states no weighting, no sample count and no
treatment of missing values, and the specification says a processor MUST NOT
recompute a result from it. Multiplying by half an hour is only correct if the
mean is time-weighted, which nothing here says. One line to add if the publisher
confirms it.

**Anything keyed on `settlement_period`.** No arithmetic across it, no grouping
by it, no use of it as a partition key. It is annotated `dcterms:identifier`, its
description says a settlement day holds 46, 48 or 50 of them so arithmetic across
a clock change is wrong, and it identifies a period rather than a source.

**Cross-record aggregation of any kind: no `TumblingWindow`, `HoppingWindow`,
`SlidingWindow` or `SessionWindow` appears.** A mean of the half-hourly means over
a window, or a `STDEV` of `wind_mw` across one, is the mean or dispersion of the
window only if every period in it is present, and the specification forbids
inferring complete coverage from `phenomenonTimeRelation: interval`. It also
states that no annotation confers permission to aggregate. Such a metric is
computable — `AVG(wind_mw)` with `COUNT(*)` beside it over, say,
`TumblingWindow(hour, 6)`, where twelve is the count the declared `PT30M` cadence
implies for six UTC hours — but it sits at a different grain from metrics 1–5 and
one statement has one output, so I left the output at the grain of the feed.

**Filling absent members with zero.** `required` names only `settlement_period`
and `start_time`, so every `*_mw` member is optional. `COALESCE(ccgt_mw, 0)` and
the like would supply a value where none was recorded, which the specification
prohibits. The sums propagate `NULL` instead and the presence counters expose why.

**Capacity factors, headroom, or margin.** No member carries a capacity,
availability or registered-output figure.

**Per-cable import/export flags.** Computable and sound, but seven flags say less
to an operator than the one net position already in metric 4.

## 4. Assumptions

* **Assumption.** The ten fuel-type members are mutually disjoint and together
  cover what the feed reports as metered generation, so their sum double-counts
  nothing and is a level rather than an arbitrary total. The schema states
  disjointness only for the `npshyd_mw` / `ps_mw` pair, and implies the rest by
  defining `other_mw` as plant "whose fuel type BMRS does not report separately".
  Everything in metrics 1, 2 and 3 rests on this.
* **Assumption.** That the sum is meaningful at all. The member annotations
  establish that the ten values are *commensurable* — one `observedProperty`
  reference, one `unit`, one `statistic`, one `phenomenonTimeRelation`, one
  `supportPeriod` — and the specification says explicitly that a processor must
  not infer permission to aggregate from annotations. The licence to add them
  comes from the prose: the record-level `observedProperty` names a generation
  *mix*, and `other_mw` is defined as its residual category.
* **Assumption.** The input carries a single series. Nothing in the record has
  `semanticRole: featureOfInterest`, so if two publishers or two regions were ever
  multiplexed into one input the query would silently interleave them, and there
  is no member on which to partition to prevent it.
* **Assumption.** The "BM-metered" scope stated explicitly on `wind_mw` and
  `other_mw` applies to all ten fuel members, so that the denominator in metric 2
  is drawn on the same basis as its numerator. If it does not, the share is still
  well defined but is not a share of a coherent population.
* **Assumption.** A two-hour `LIMIT DURATION` is enough lookback. Beyond four
  missed beats of the declared cadence the ramp and the gap flag return `NULL`
  rather than reaching further back.
* **Assumption.** Late arrival and out-of-order tolerance for `start_time` are
  configured on the job, not expressed here. `TIMESTAMP BY` places the event; it
  does not state how long the query waits for a straggler.
* **Assumption.** `total_metered_generation_mw > 0` is the right guard for the
  share. No member declares a `minimum` and all are `double`, so the schema does
  not exclude a zero or negative total; the metric yields `NULL` rather than a
  ratio if one occurs.
* **Assumption.** `LAG(..., 1) OVER (LIMIT DURATION(hour, 2))` is accepted without
  a `PARTITION BY` clause. I believe it is, but I could not check, and if it is not
  the two `LAG` calls need a constant partition key.
* Not an assumption, for the record: `start_time` being UTC, the period being half
  an hour, the interconnector sign convention, and the `PT30M` cadence are all
  stated in the schema.
