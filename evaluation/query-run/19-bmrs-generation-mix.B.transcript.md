# GenerationMix — five derived metrics

## 1. The five metrics

All five are computed on a rolling six-hour window hopped every 30 minutes, so one row is emitted per settlement period and each row summarises the twelve periods up to it.

1. **Rolling 6-hour metered generation energy (MWh)** — `SUM` of the ten fuel members × 0.5 h, turning a stream of period *means* into the volume quantity; an operator needs the volume before any mix number means anything, and it is the denominator for metric 2.
2. **Rolling 6-hour wind share of metered generation (%)** — the mix headline this feed exists to carry; because every period is the same length the ratio of sums *is* the energy share, and it is a lower bound on GB wind because `wind_mw` covers only Balancing-Mechanism-metered units.
3. **Largest half-hour ramp of metered generation in the window (MW/min)** — how hard the system had to move between consecutive periods, which is what sizes response and reserve; computed from `start_time` differences rather than `settlement_period`, so it stays correct across a clock change.
4. **Rolling 6-hour net interconnector energy (MWh, signed, positive = import)** — how much of supply arrived across cables and in which direction; the seven `int*` members share one sign convention, so summing them with one another is the one cross-member sum the schema licenses.
5. **Standard deviation of `wind_mw` across the window (MW)** — dispersion of the uncontrolled component at a given mean, distinguishing a steady 6 GW of wind from a swinging one, which metric 1 and metric 2 cannot show.

## 2. The query

```sql
-- Event time is start_time: it is the only datetime member, and the feed
-- carries no end instant.  settlement_period is deliberately never used in
-- arithmetic (see section 3).
--
-- Dialect hedge: I am not certain COALESCE is available in this dialect.  If it
-- is not, replace each COALESCE(x, 0) with CASE WHEN x IS NULL THEN 0 ELSE x END.
-- ABS, STDEV, DATEDIFF and LAG ... LIMIT DURATION are assumed available.

WITH period AS (
    SELECT
        System.Timestamp()                    AS period_start,   -- = start_time
        COALESCE(ccgt_mw,    0)
      + COALESCE(ocgt_mw,    0)
      + COALESCE(coal_mw,    0)
      + COALESCE(oil_mw,     0)
      + COALESCE(nuclear_mw, 0)
      + COALESCE(wind_mw,    0)
      + COALESCE(biomass_mw, 0)
      + COALESCE(npshyd_mw,  0)
      + COALESCE(ps_mw,      0)
      + COALESCE(other_mw,   0)               AS gen_mw,         -- fuel members only
        COALESCE(wind_mw, 0)                  AS wind_mw,
        COALESCE(intfr_mw,   0)
      + COALESCE(intifa2_mw, 0)
      + COALESCE(intned_mw,  0)
      + COALESCE(intnem_mw,  0)
      + COALESCE(intelec_mw, 0)
      + COALESCE(intnsl_mw,  0)
      + COALESCE(intvkl_mw,  0)               AS net_import_mw   -- signed, + = import
    FROM input
    TIMESTAMP BY start_time
),

-- No member identifies an individual source, so there is no PARTITION BY here
-- or anywhere else in the query.  LIMIT DURATION is required on LAG.
lagged AS (
    SELECT
        period_start,
        gen_mw,
        wind_mw,
        net_import_mw,
        LAG(gen_mw,       1) OVER (LIMIT DURATION(hour, 2)) AS prev_gen_mw,
        LAG(period_start, 1) OVER (LIMIT DURATION(hour, 2)) AS prev_period_start
    FROM period
),

ramped AS (
    SELECT
        period_start,
        gen_mw,
        wind_mw,
        net_import_mw,
        CASE
            WHEN prev_period_start IS NOT NULL
             AND DATEDIFF(minute, prev_period_start, period_start) > 0
            THEN (gen_mw - prev_gen_mw)
                 / DATEDIFF(minute, prev_period_start, period_start)
            ELSE NULL
        END AS gen_ramp_mw_per_min
    FROM lagged
)

SELECT
    System.Timestamp()                                  AS window_end,

    -- 1. mean MW over a half-hour period -> MWh, summed over the window
    SUM(gen_mw) * 0.5                                   AS metered_generation_mwh_6h,

    -- 2. equal period lengths make the ratio of sums the energy share exactly
    CASE WHEN SUM(gen_mw) > 0
         THEN 100.0 * SUM(wind_mw) / SUM(gen_mw)
         ELSE NULL
    END                                                 AS wind_share_of_metered_pct_6h,

    -- 3. magnitude only; direction is discarded on purpose
    MAX(ABS(gen_ramp_mw_per_min))                       AS max_abs_gen_ramp_mw_per_min_6h,

    -- 4. signed, positive = net import to GB
    SUM(net_import_mw) * 0.5                            AS net_interconnector_mwh_6h,

    -- 5. dispersion of the uncontrolled component
    STDEV(wind_mw)                                      AS wind_stdev_mw_6h

INTO output
FROM ramped
-- HoppingWindow: 360-minute (6 h) window, 30-minute hop.  The hop matches the
-- declared half-hourly publication cadence, so one row is emitted per
-- settlement period and each window holds twelve periods.
GROUP BY HoppingWindow(minute, 360, 30)
```

## 3. What I did not compute

* **Total system supply as generation plus interconnectors** — the ten fuel members summed with the seven `int*` members. The schema says the interconnector values "may not be summed with the generation members without deciding how exports are to be treated", and the instance carries genuine negatives (`intnem_mw` = −412, `intelec_mw` = −184) which would silently cancel real generation. I kept the two sums apart as metrics 1 and 4 instead of deciding on the operator's behalf.
* **A combined gas total, `ccgt_mw` + `ocgt_mw`** — the schema states these are operationally unrelated fleets, bulk dispatched energy against minutes-at-a-time reserve. Their sum is a number nobody acts on.
* **A net or round-trip storage position from `ps_mw`** — the schema says the pumping load is metered as demand elsewhere and does not appear here as a negative, so `ps_mw` is not a net position and no storage balance is computable from this feed. It is included in metric 1 only as gross output.
* **A low-carbon or renewable share** (some combination of `nuclear_mw`, `wind_mw`, `npshyd_mw`, `biomass_mw`, `ps_mw`) — neither file establishes an emissions attribute for any member or a definition of "renewable", and where biomass and pumped storage fall is exactly the contested part. Writing it would be importing domain knowledge the files do not license.
* **Anything keyed on `settlement_period`** — no period-over-period differencing indexed by period number, and no settlement-day aggregate defined as periods 1..*n*. The schema says the count per day is 46, 48 or 50 and that arithmetic across a clock change is wrong; it also says periods are numbered from 1 at midnight UTC, and both cannot hold of a fixed 24-hour UTC day. I cannot delimit a settlement day soundly, so I did not attempt daily energy totals, and every time calculation in the query uses `start_time`.
* **Interconnector utilisation or capacity factor** — the schema notes that IFA and IFA2 have separate capacities but gives no capacity value for any cable and carries no capacity member, so `intfr_mw` / capacity and its siblings are not computable.
* **A true wind share of GB generation** — `wind_mw` omits distribution-connected wind and the files supply no figure for it, so I labelled metric 2 as a share of *metered* generation rather than presenting an understated number as the real one.
* **A feed-completeness counter** (`COUNT(*)` against the twelve half-hours a six-hour UTC window should contain) — this would be sound, since UTC is continuous through a clock change, but it ranks sixth and the brief is five.
* **`PERCENTILE_CONT` on any member** — twelve samples per window is too few for a stable percentile, so `STDEV` is the honest dispersion statistic here.

## 4. Assumptions

* **Assumption:** every record covers exactly half an hour, so a mean in MW multiplied by 0.5 is MWh. The schema states the period length; I rely on it for metrics 1 and 4.
* **Assumption:** consecutive `start_time` values are 30 minutes apart in UTC even across a GB clock change, and the publisher does not republish or restate a period. A restatement would be counted twice by the window sums and would produce a spurious zero-length interval in the ramp guard.
* **Assumption:** an absent optional member means zero output. Only `settlement_period` and `start_time` are required, so any fuel or cable may be missing, and the query cannot tell "not published" from "genuinely zero" — the instance carries real 0.0 values in `ocgt_mw`, `coal_mw` and `oil_mw`. If absence should instead void the total, remove the `COALESCE` wrappers so the sum becomes null.
* **Assumption:** the input is a single GB-wide stream. Nothing in the schema identifies an individual source, so there is no partition key; if several regions or publishers were multiplexed onto one input the query would silently mix them.
* **Assumption:** events arrive in or near event-time order and within whatever late-arrival tolerance is configured on the job. `LIMIT DURATION(hour, 2)` assumes the previous period is reachable within two hours; the out-of-order policy itself is job configuration, not part of this query.
* **Assumption:** the six-hour window and 30-minute hop are my choice, not something the files state. The hop is set to the declared half-hourly cadence so there is one output per settlement period; six hours gives twelve samples, enough for `STDEV` to mean something.
* **Assumption:** `System.Timestamp()` in the non-windowed step yields the event's own timestamp, i.e. `start_time`, and in the windowed `SELECT` yields the window end. Because `start_time` is the *start* of a period, `window_end` is the start instant of the newest period in the window and the underlying half hour runs 30 minutes past that stamp.
* **Assumption:** all seven `int*` members use the same sign convention, positive for import to GB. The schema states this for each of them individually, which is what makes their mutual sum in metric 4 legitimate.
* **Assumption (design choice, stated for clarity):** metric 3 reports ramp magnitude via `MAX(ABS(...))` and discards whether the swing was up or down, so that one column answers "how hard did the system have to move".
* **Assumption:** `COALESCE`, `ABS` and `STDEV` exist in this dialect. The query carries a comment with a `CASE`-based replacement for `COALESCE` in case it does not.
