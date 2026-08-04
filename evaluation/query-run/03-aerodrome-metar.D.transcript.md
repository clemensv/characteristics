# METAR stream — five derived metrics

## 1. The five metrics

1. **Gust factor and gust spread** — `wgst / wspd` and `wgst - wspd` per report, reduced to the per-station maximum in the window. The schema states that `wspd` is the *mean* anemometer speed over the ten-minute window ending at the observation time and `wgst` is the *greatest short-interval speed observed within that same ten-minute window*. The two are therefore the max and the mean of one population over one interval in one unit (knots), which is the strongest licence for a ratio anywhere in this record. An operator wants it because it separates a steady 12 kt wind from a 12 kt wind that is peaking at 18 kt — the second is a different thing to land in, and it is invisible in either member alone.
2. **Altimeter tendency (hPa per hour)** — the change in `altim` between consecutive reports from the same station, normalised by the actual elapsed observation time. The schema establishes the unit (hectopascals), the per-station identity (`icao_id`), and the cadence (one routine report per station per hour), so a first difference over time is well-founded. An operator wants the rate rather than the level: a falling altimeter setting is the leading indicator in the record, and it is the only member here whose *derivative* carries more information than its value.
3. **Dewpoint spread and its closure rate** — `temp - dewp` per report, and the change of that spread per hour. Both members are stated to be temperatures at the same station in degrees Celsius at the same instant, so the difference is arithmetically sound without further licence. The minimum spread in the window and the fastest closure rate tell an operator that two curves are converging and how fast, which is the earliest numeric warning the feed offers of a change in the low-level moisture state. *(The interpretation of a narrowing spread — fog, lowering cloud base — is domain knowledge; see Assumptions. The number is not.)*
4. **Flight-category change count** — the number of reports in the window whose `flt_cat` differs from that station's previous report. `flt_cat` copied out is not a metric; the *transition* is. It is the record's own summary of ceiling and visibility, and a station that changed category three times in six hours is unstable in exactly the dimension that governs whether aircraft can operate, whatever the categories themselves mean.
5. **Issue latency (obs → report)** — `DATEDIFF(second, obs_time, report_time)`, mean and max per station per window. The schema goes out of its way to distinguish the time the conditions obtained from the time the encoded result was issued, which is a direct licence to difference them. An operator wants it because everything downstream is acting on conditions that are already this many seconds old, and a station whose latency drifts is degrading before it fails.

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
--
-- Event time  : obs_time  (the time the conditions obtained, per the schema;
--                report_time is when the encoded result was issued, so it is a
--                payload member here, not the clock).
-- Partition   : icao_id   (the schema states it identifies the reporting aerodrome).
-- Window      : TumblingWindow(hour, 6) on the final aggregate — the schema states
--                the routine cycle is one report per station per hour, so a 1-hour
--                window would hold a single report and every aggregate in it would
--                be degenerate. Six hours gives roughly six samples per station.
-- Lookback    : LIMIT DURATION(hour, 6) on every LAG — this is the required bound
--                on the lookback, not a window; it is sized to match the aggregate
--                window so a report can always reach its predecessor.

WITH Reports AS
(
    SELECT
        icao_id,
        obs_time,
        report_time,
        temp,
        dewp,
        wspd,
        wgst,
        altim,
        flt_cat
    FROM input TIMESTAMP BY obs_time
),

Lagged AS
(
    -- Previous report from the same station. LAG is isolated here so that the
    -- arithmetic below reads as plain column references.
    SELECT
        icao_id,
        obs_time,
        report_time,
        temp,
        dewp,
        wspd,
        wgst,
        altim,
        flt_cat,
        LAG(obs_time, 1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)) AS prev_obs_time,
        LAG(temp,     1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)) AS prev_temp,
        LAG(dewp,     1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)) AS prev_dewp,
        LAG(altim,    1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)) AS prev_altim,
        LAG(flt_cat,  1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)) AS prev_flt_cat
    FROM Reports
),

PerReport AS
(
    SELECT
        icao_id,

        -- (1) Gust factor and gust spread. wgst is the max and wspd the mean of the
        --     same ten-minute window, both in knots. NULL when no gust was reported
        --     (the schema says wgst is omitted then) or when wspd is absent or zero.
        CASE WHEN wgst IS NOT NULL AND wspd > 0
             THEN CAST(wgst AS float) / CAST(wspd AS float)
        END AS gust_factor,
        CASE WHEN wgst IS NOT NULL AND wspd IS NOT NULL
             THEN CAST(wgst AS float) - CAST(wspd AS float)
        END AS gust_spread_kt,

        -- (2) Altimeter tendency, hPa per hour, normalised by the real interval
        --     rather than assuming the hourly cycle held.
        CASE WHEN prev_altim IS NOT NULL
              AND DATEDIFF(second, prev_obs_time, obs_time) > 0
             THEN (altim - prev_altim) * 3600.0
                  / DATEDIFF(second, prev_obs_time, obs_time)
        END AS altim_hpa_per_hour,

        -- (3) Dewpoint spread, and the rate at which it is closing (negative = closing).
        temp - dewp AS dewpoint_spread_c,
        CASE WHEN prev_temp IS NOT NULL AND prev_dewp IS NOT NULL
              AND DATEDIFF(second, prev_obs_time, obs_time) > 0
             THEN ((temp - dewp) - (prev_temp - prev_dewp)) * 3600.0
                  / DATEDIFF(second, prev_obs_time, obs_time)
        END AS spread_change_c_per_hour,

        -- (4) Flight-category transition. Change only: the files never establish an
        --     ordering over VFR / MVFR / IFR / LIFR, so no direction is claimed.
        --     Both sides must be non-null, otherwise an absent value would read as a change.
        CASE WHEN flt_cat IS NOT NULL
              AND prev_flt_cat IS NOT NULL
              AND flt_cat <> prev_flt_cat
             THEN 1 ELSE 0
        END AS flt_cat_changed,

        -- (5) Issue latency: conditions obtained -> encoded result issued.
        CASE WHEN report_time IS NOT NULL
             THEN DATEDIFF(second, obs_time, report_time)
        END AS issue_latency_s

    FROM Lagged
)

SELECT
    icao_id,
    System.Timestamp()                  AS window_end,
    COUNT(*)                            AS reports_in_window,

    -- (1)
    MAX(gust_factor)                    AS max_gust_factor,
    MAX(gust_spread_kt)                 AS max_gust_spread_kt,
    COUNT(gust_factor)                  AS reports_with_gust,

    -- (2)
    AVG(altim_hpa_per_hour)             AS mean_altim_tendency_hpa_per_h,
    MIN(altim_hpa_per_hour)             AS steepest_altim_fall_hpa_per_h,

    -- (3)
    MIN(dewpoint_spread_c)              AS min_dewpoint_spread_c,
    MIN(spread_change_c_per_hour)       AS fastest_spread_closure_c_per_h,

    -- (4)
    SUM(flt_cat_changed)                AS flt_cat_changes,

    -- (5)
    AVG(issue_latency_s)                AS mean_issue_latency_s,
    MAX(issue_latency_s)                AS max_issue_latency_s

INTO output
FROM PerReport
GROUP BY icao_id, TumblingWindow(hour, 6)
```

## 3. What I did not compute

* **Numeric visibility, or a visibility trend, from `visib`.** The schema declares it a string precisely because it carries qualifiers such as `'10+'` and fractional values, and gives no grammar for them. `'10+'` is a bound, not a measurement; averaging bounds and measurements together is meaningless, and I have no parse rule.
* **A ceiling, or a ceiling trend, from `clouds`.** Two things are missing, not one. The files do not say which coverage codes constitute a ceiling (the instance shows `FEW` and `SCT` only), and they do not state the unit of `base` (4500 and 25000 are consistent with feet, but nothing says so). A ceiling metric would be two guesses stacked.
* **Any statistic over `wdir` — mean, standard deviation, or a veering/backing rate.** Two disqualifiers. It is a circular quantity, so the arithmetic mean of 350 and 010 is 180, which is the reciprocal of the truth; and the schema states that 0 means *variable or calm*, so 0 is a sentinel and not a point on the circle. Both problems would need a convention the files do not supply.
* **Ranking `flt_cat` into a severity order to flag deterioration versus improvement.** The schema lists VFR, MVFR, IFR, LIFR and says they come from published thresholds, but never states that this list is ordered or which end is worse. I count transitions of `flt_cat` and claim no direction. This is the single largest piece of value I left on the table, and it is one word of schema text away from being computable.
* **A QC failure rate from `qc_field`.** It is declared a bitmask in which "each bit records the outcome of one automated consistency check", but no bit is named, and the polarity — set means passed, or set means failed — is unstated. The one example value, 2, establishes nothing. Any rate I computed would have an unknown sign.
* **The residual `altim - slp`.** Tempting, because both are hectopascals derived from the same station pressure reading. But the schema says they are reduced by *different* methods to *different* references: `altim` to the aerodrome elevation under the ICAO standard atmosphere, `slp` to mean sea level using station elevation and temperature history. Their difference is therefore dominated by station elevation and is not comparable across stations, and the files give no expected magnitude against which a residual could be judged. It looks like a consistency check and is not one.
* **A SPECI rate from `metar_type`.** The schema explicitly says this member "reports the state of the observing programme rather than a property of the atmosphere". A SPECI fraction would measure how a station's reporting policy is configured as much as it measures weather, and I cannot separate the two.
* **Missed-cycle or gap detection from successive `obs_time` values.** The schema says a routine cycle produces one report per station per hour "normally near the end of the hour". *Normally* is not a guarantee, and `metar_type` establishes that SPECI reports legitimately arrive off-cycle, so any gap threshold would fire on both real outages and correct behaviour.
* **Relative humidity or absolute humidity from `temp` and `dewp`.** This needs a saturation-vapour-pressure relation (Magnus, Tetens, Goff–Gratch — they disagree at the edges). No such formula appears in the files. The spread is a subtraction the files license; humidity is physics they do not.
* **Anything spatial from `position` and `elevation`** — inter-station pressure gradients, nearest-neighbour comparison, area means. A neighbour or distance relation is required and the files establish none; the example carries exactly one station.
* **Re-deriving anything from `raw_ob`.** Every value I would extract already has a decoded member, and parsing it needs a METAR grammar the files do not contain. Note the trap: the instance's `raw_ob` shows `A2999`, which is not 1015.6 — the raw text and the decoded `altim` member are in different units.
* **Threshold flags of any kind** — "gust factor above X", "tendency steeper than Y hPa/h", "spread below Z °C". The prompt lists a threshold flag as a legitimate derived metric, but no threshold for any member appears in the files, and an invented one is a domain claim wearing a number. I emit the continuous quantities and leave the threshold to whoever is entitled to set it.

## 4. Assumptions

* **Assumption:** `obs_time` is the right event-time member. The schema's description supports it directly, but note that the instance's `report_time` is two minutes later, so events necessarily arrive after their event time; the job's late-arrival tolerance must exceed the issue latency plus transport delay or reports will be dropped or reordered. The correct tolerance is not derivable from the files.
* **Assumption:** `icao_id` identifies one physical source, is stable over time, and there is exactly one observing installation per aerodrome. The schema says it identifies the aerodrome; it does not say a station cannot be relocated, retired, or duplicated.
* **Assumption:** an omitted `wgst` surfaces as SQL `NULL`. The schema says the member is "omitted if no gusts were reported", which is a statement about JSON absence; that absence maps to `NULL` in the ingestion layer is an assumption about serialisation, not about the schema.
* **Assumption:** only `icao_id`, `obs_time` and `raw_ob` are required, so `temp`, `dewp`, `wspd`, `altim` and the rest may be absent from any given report. The query is written so that each metric independently degrades to `NULL` and the aggregates skip it; this means the window count and the count of reports contributing to any one metric can differ, which is why `reports_in_window` and `reports_with_gust` are both emitted.
* **Assumption:** the *interpretation* of a narrowing dewpoint spread as approaching saturation is domain knowledge and is not established by the files. The subtraction is sound — same station, same instant, same unit, both declared temperatures — but its meaning is my import, and metric 3's operational value rests on it.
* **Assumption:** comparing a maximum (`wgst`) against a mean (`wspd`) is legitimate here because the schema states both are taken over the *same* ten-minute window from the same instrument. If that co-window claim were wrong the gust factor would be meaningless. I am relying on it heavily and it is the reason metric 1 ranks first.
* **Assumption:** `altim` is in hectopascals as the schema declares, notwithstanding that the instance's `raw_ob` encodes the altimeter as `A2999` (inches of mercury). I take the schema's stated unit for the decoded member as governing.
* **Assumption:** events for a given station reach the `LAG` in non-decreasing `obs_time` order within the six-hour lookback. Out-of-order delivery inside the tolerance would make the first differences in metrics 2 and 3 negative-interval; the `DATEDIFF(...) > 0` guard suppresses those rather than emitting a wrong rate, so the effect is silent under-counting, not corruption.
* **Assumption:** six hours is an operationally useful aggregation period. It follows from the schema's stated hourly cadence that it yields roughly six samples, but nothing in the files says an operator wants six-hourly summaries. A shorter window collapses to one report and makes `MAX`/`AVG` trivial; per-report emission would mean dropping the `GROUP BY` entirely.
* **Assumption about the dialect:** I have used `LAG(... ) OVER (PARTITION BY ... LIMIT DURATION(...))`, `DATEDIFF(second, ...)`, `CAST(... AS float)`, `System.Timestamp()` and `TumblingWindow(hour, 6)` as documented in the prompt's notes. I deliberately avoided `PERCENTILE_CONT` for the latency distribution — it is listed as available, but I believe it is an analytic function requiring an `OVER` clause rather than a `GROUP BY` aggregate, and I cannot verify that form, so I used `AVG` and `MAX` instead. `COUNT(<column>)` counting only non-null values is standard SQL semantics that I assume holds in this dialect.
