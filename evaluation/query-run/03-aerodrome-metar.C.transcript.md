# Five derived metrics over the METAR stream

## 1. The five metrics

1. **Flight-category transitions** — count, per station per window, of observations whose `flt_cat` differs from that station's previous observation. The category is the field the feed itself uses to summarise conditions; a *change* in it is the event worth alarming on, and it is the cheapest high-value signal here because it needs no unit, scale or ordering knowledge — only equality.
2. **Peak gust spread** — the window maximum of `wgst - wspd`. Both are integers reported in the same wind group of `raw_ob` (`21012G18KT`), so the difference is dimensionally sound; it measures how unsteady the wind is rather than how strong it is, which mean wind speed alone cannot show, and the peak (not the mean) is the operationally binding number over a period.
3. **Minimum temperature–dewpoint spread** — the window minimum of `temp - dewp`. The two are reported as a single slash-separated pair in `raw_ob` (`26/22`), so they share a unit and the difference is sound; the smallest spread reached in the window is the tightest margin the station got to the point where the two members coincide.
4. **Maximum absolute rate of pressure change** — `|slp - previous slp|` per station, normalised to a per-hour rate by the actual elapsed `obs_time`, then maximised over the window. A rate of change of a repeatedly reported scalar is well defined from the files alone, and normalising by elapsed time makes it comparable across stations that report on different cadences.
5. **Maximum report latency** — the window maximum of `report_time - obs_time`. This is the only metric that needs no domain reading at all: it measures the feed's own delay between when a station observed and when the observation was published, and it bounds how stale every other metric above can be.

`observations` (a plain `COUNT(*)`) is also emitted. It is **not** one of the five; it is the denominator that tells you whether a MIN/MAX in a window rests on one sample or six.

## 2. The query

Event time is `obs_time`: it is one of the three required members, it is the time the measurement refers to, and unlike `report_time` it is non-nullable. Aggregation is a **HoppingWindow of 6 hours, hopping every 1 hour**, partitioned by `icao_id`, which is the only member that identifies a source. `LAG` is limited to `DURATION(hour, 3)`; when the previous observation is older than that, the successive-record metrics return NULL instead of a stale comparison.

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL
WITH Observations AS
(
    SELECT
        icao_id,
        CAST(obs_time    AS datetime) AS obs_ts,
        CAST(report_time AS datetime) AS report_ts,
        temp,
        dewp,
        wspd,
        wgst,
        slp,
        flt_cat
    FROM input TIMESTAMP BY obs_time          -- event time: obs_time, and nothing else
),

-- Per-event step: successive-record reach-backs, each capped by LIMIT DURATION (3 hours).
Successive AS
(
    SELECT
        icao_id,
        obs_ts,
        temp,
        dewp,
        wspd,
        wgst,
        slp,
        flt_cat,
        report_ts,
        LAG(slp)     OVER (PARTITION BY icao_id LIMIT DURATION(hour, 3)) AS prev_slp,
        LAG(obs_ts)  OVER (PARTITION BY icao_id LIMIT DURATION(hour, 3)) AS prev_obs_ts,
        LAG(flt_cat) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 3)) AS prev_flt_cat
    FROM Observations
),

-- Per-event step: the five derived quantities, before aggregation.
Derived AS
(
    SELECT
        icao_id,

        -- (1) categorical state change; equality only, no ordering assumed
        CASE
            WHEN flt_cat IS NULL OR prev_flt_cat IS NULL THEN 0
            WHEN flt_cat <> prev_flt_cat                 THEN 1
            ELSE 0
        END AS flt_cat_changed,

        -- (2) gust spread; NULL when either member is absent, never coerced to 0
        CASE
            WHEN wgst IS NULL OR wspd IS NULL THEN NULL
            ELSE wgst - wspd
        END AS gust_spread,

        -- (3) temperature-dewpoint spread
        CASE
            WHEN temp IS NULL OR dewp IS NULL THEN NULL
            ELSE temp - dewp
        END AS dewpoint_spread,

        -- (4) pressure rate of change, normalised to one hour by actual elapsed time
        CASE
            WHEN prev_slp IS NULL OR slp IS NULL OR prev_obs_ts IS NULL THEN NULL
            WHEN DATEDIFF(second, prev_obs_ts, obs_ts) <= 0             THEN NULL
            ELSE ABS(slp - prev_slp) * 3600.0 / DATEDIFF(second, prev_obs_ts, obs_ts)
        END AS abs_slp_rate_per_hour,

        -- (5) publication delay; NULL when report_time is absent
        CASE
            WHEN report_ts IS NULL THEN NULL
            ELSE DATEDIFF(second, obs_ts, report_ts)
        END AS report_latency_s

    FROM Successive
)

SELECT
    icao_id,
    System.Timestamp()               AS window_end,
    COUNT(*)                         AS observations,              -- context, not a metric
    SUM(flt_cat_changed)             AS flt_cat_transitions,       -- metric 1
    MAX(gust_spread)                 AS peak_gust_spread,          -- metric 2
    MIN(dewpoint_spread)             AS min_dewpoint_spread,       -- metric 3
    MAX(abs_slp_rate_per_hour)       AS max_abs_slp_rate_per_hour, -- metric 4
    MAX(report_latency_s)            AS max_report_latency_s       -- metric 5
INTO output
FROM Derived
GROUP BY icao_id, HoppingWindow(hour, 6, 1)   -- 6-hour window, 1-hour hop, per station
```

I used only `COUNT`, `SUM`, `MIN`, `MAX`, `ABS` and `DATEDIFF`. I deliberately avoided `PERCENTILE_CONT` for latency: I am not certain it is usable as a `GROUP BY` aggregate in this dialect rather than only as an `OVER (...)` analytic, and a metric I cannot be sure will parse is worth less than `MAX`.

## 3. What I did not compute

* **`visib`** — declared `string`, and the one observed value is `"10+"`, which is not a number. Any threshold, trend or window minimum would require me to invent a parse rule for `+` that the files do not state. No visibility metric.
* **`clouds`** — a `string` carrying an encoded array (`[{"cover":"FEW","base":4500},…]`). Deriving a ceiling means (a) parsing a JSON string, which I am not confident this dialect can do, and (b) knowing which `cover` values constitute a ceiling and how `FEW`/`SCT` rank, which neither file establishes. No ceiling height, no lowest-base metric.
* **`altim` minus `slp`** — tempting, because the two are on the same numeric scale (1015.6 and 1015.4) and a stable residual per station would make a good sensor cross-check. Left out: nothing in the two files says they are the same physical quantity reduced by different conventions, nor what role `elevation` plays in relating them. The difference would be a number with no established meaning, so a drift in it could not be interpreted.
* **`wdir`** — no mean, no standard deviation, no shift magnitude. `AVG(wdir)` and `STDEV(wdir)` over a compass-like integer are unsound wherever the series crosses the 0/360 boundary, and the files establish neither that it wraps at 360 nor how a calm or variable wind is encoded. A crosswind component was also not computed: that needs a runway heading, which this feed does not carry.
* **`flt_cat` severity** — only *whether* the category changed, never whether it improved or deteriorated. Only one value (`"VFR"`) is observed and no ordering over the category strings is declared, so "deterioration" is not computable from these files.
* **`qc_field`** — value `2`, no legend. I did not filter, threshold or weight anything by it, because I do not know whether higher is better.
* **`wx_string` presence rate** — the non-null fraction is derivable without decoding the string, and I considered it. Left out because the files do not establish whether `null` means "no significant weather" or "not reported", so the ratio would not be interpretable either way.
* **Station silence** — a station that stops reporting emits no events, so no window fires for it and no query over this stream alone can detect it. Detecting a dark station needs a roster of expected `icao_id` values, which the files do not provide. The inter-observation gap appears here only as the denominator of metric 4, not as an outage alarm.
* **Anything spatial** — `position.latitude` / `position.longitude` and `elevation` are present, but grouping stations into regions or computing a gradient between them requires a grouping rule and a distance function that neither file supplies.
* **Re-parsing `raw_ob`** — it evidently duplicates the decoded members, but extracting anything from it means assuming a grammar the files do not state. I used it as *evidence of shared units* (see assumptions), not as a data source.
* **Temperature tendency** — `(temp - previous temp)` per hour is as computable as the pressure rate. Dropped rather than added: one rate-of-change metric is enough, and I judged pressure the more informative of the two. This was a ranking decision, not a soundness one.

## 4. Assumptions

* **Assumption** — `obs_time` and `report_time` are on the same clock and in the same zone, so their difference is a publication delay and not a clock offset. If they are not, metric 5 is meaningless.
* **Assumption** — the job's late-arrival tolerance is configured to exceed the typical report latency. The single instance was observed at 11:51Z and reported at 11:53Z, so events reach the pipeline after their event time; with `TIMESTAMP BY obs_time` and too small a tolerance they would be dropped or clamped.
* **Assumption** — `wspd` and `wgst` share a unit. My evidence is the `21012G18KT` group in `raw_ob`, where `012` and `G18` sit inside one `KT`-suffixed token and match the two members; that the decoded members correspond to those tokens is itself an assumption. The output column is left unit-less for this reason.
* **Assumption** — `temp` and `dewp` share a unit, evidenced by the single `26/22` pair in `raw_ob`. No unit is declared anywhere.
* **Assumption** — `slp` is one quantity in a fixed unit, reported repeatedly per station, so successive differences are meaningful. Only one value exists in the files.
* **Assumption** — `wgst` is absent, not zero, when no gust is reported. The schema types it `int32` (not nullable) but does **not** list it in `required`, so it may be missing; the query yields NULL rather than treating a missing gust as a spread of `0 - wspd`.
* **Assumption** — `wgst >= wspd`. If a record violates it, metric 2 is still a signed difference and simply goes negative; nothing breaks.
* **Assumption** — `icao_id` identifies one physical source and is stable over time. It is required by the schema and is the only plausible key, but the files show exactly one value.
* **Assumption** — `flt_cat` is a categorical label whose change between successive observations is meaningful rather than cosmetic (e.g. not whitespace or case variation).
* **Assumption** — the reporting cadence. The files show a single observation at :51 past the hour and establish no interval. The 6-hour window, the 1-hour hop and the 3-hour `LIMIT DURATION` are therefore judgement calls, not facts. They are chosen so that a gap longer than 3 hours produces NULL for the successive-record metrics rather than a comparison across a hole.
* **Assumption (interpretive)** — that a large `|Δslp|/hour` and a small `temp - dewp` are operationally significant. The files establish that these quantities exist and can be differenced; they do not establish what the results mean. Metrics 3 and 4 are sound as arithmetic and interpreted only by this assumption.
* **Assumption** — the input stream is named `input` and the sink `output`.
