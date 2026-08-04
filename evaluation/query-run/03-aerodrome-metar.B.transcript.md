# Five derived metrics from the METAR stream

## 1. The five metrics

1. **Gust spread** — `wgst − wspd`, in knots, maximised and averaged over the
   window. The schema states that both values come from *the same* ten-minute
   window ending at `obs_time`, one as the mean and one as the maximum, so their
   difference is a licensed within-report residual rather than a comparison of
   unrelated samples. An operator wants it because the two members are
   individually unremarkable and only their separation says how unsteady the
   wind was; `wgst` is also omitted when no gusts occurred, so the spread
   doubles as the gustiness indicator.
2. **Dewpoint depression** — `temp − dewp`, in degrees Celsius, minimised and
   averaged over the window. Both members are `observationValue`, `measured`,
   `instant`, unit `CEL`, at the same station and the same `obs_time`, so the
   difference is dimensionally and temporally sound. An operator wants the
   window minimum because it is the single number that collapses two curves that
   are almost always tracked together.
3. **Altimeter tendency** — `(altim − previous altim) × 3600 ÷ elapsed seconds`,
   in hPa per hour, reported as the window minimum (steepest fall) and maximum
   (steepest rise). This is a rate of change over successive reports from the
   same station, normalised by the actual elapsed time rather than by the
   nominal cycle, so an interleaved `SPECI` or a missed cycle does not distort
   it. An operator wants a tendency because a single QNH value carries no
   information about direction of change and the feed carries no tendency member
   of its own.
4. **Report latency** — `DATEDIFF(second, obs_time, report_time)`, maximised and
   averaged over the window. The schema separates `phenomenonTime` from
   `resultTime` explicitly, which is exactly what makes their difference
   meaningful: it is the delay between the conditions obtaining and the encoded
   result being issued. An operator wants it because it is the only member pair
   that measures the health of the observing and publishing chain rather than
   the atmosphere.
5. **Routine-cadence completeness** — the count of `metar_type = 'METAR'`
   reports in the window against the count the declared `PT1H` cadence predicts,
   plus a shortfall flag. `SPECI` reports are excluded from the numerator
   because the schema states the routine cycle produces one report per station
   per hour and that `SPECI` is a special issuance; counting them would let a
   burst of special reports mask a dead routine cycle. An operator wants it
   because a station that has gone silent produces no records at all, and
   silence is invisible unless it is counted against a declared expectation.

## 2. The query

```sql
-- Event time is obs_time: semanticRole phenomenonTime, required, and the time
-- at which the reported conditions obtained. report_time is resultTime and is
-- nullable, so it is not used as the event time.
WITH PerEvent AS
(
    SELECT
        icao_id,
        metar_type,
        obs_time,
        altim,
        temp - dewp                                                       AS dewpoint_depression_c,
        wgst - wspd                                                       AS gust_spread_kt,
        DATEDIFF(second, obs_time, report_time)                           AS report_latency_s,
        -- Previous report from the same station. LIMIT DURATION is sized from
        -- the declared PT1H cadence with slack for two missed cycles.
        LAG(altim, 1)    OVER (PARTITION BY icao_id LIMIT DURATION(hour, 3)) AS prev_altim_hpa,
        LAG(obs_time, 1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 3)) AS prev_obs_time
    FROM input TIMESTAMP BY obs_time
),
WithTendency AS
(
    SELECT
        icao_id,
        metar_type,
        dewpoint_depression_c,
        gust_spread_kt,
        report_latency_s,
        CASE
            WHEN prev_altim_hpa IS NOT NULL
             AND DATEDIFF(second, prev_obs_time, obs_time) > 0
            THEN (altim - prev_altim_hpa) * 3600.0
                 / DATEDIFF(second, prev_obs_time, obs_time)
        END                                                               AS altim_tendency_hpa_per_h
    FROM PerEvent
)
SELECT
    icao_id,
    System.Timestamp()                          AS window_end,

    -- 1. Gust spread (kt)
    MAX(gust_spread_kt)                         AS max_gust_spread_kt,
    AVG(CAST(gust_spread_kt AS float))          AS avg_gust_spread_kt,

    -- 2. Dewpoint depression (degC)
    MIN(dewpoint_depression_c)                  AS min_dewpoint_depression_c,
    AVG(dewpoint_depression_c)                  AS avg_dewpoint_depression_c,

    -- 3. Altimeter tendency (hPa/h), signed: MIN is the steepest fall
    MIN(altim_tendency_hpa_per_h)               AS min_altim_tendency_hpa_per_h,
    MAX(altim_tendency_hpa_per_h)               AS max_altim_tendency_hpa_per_h,

    -- 4. Report latency (s)
    MAX(report_latency_s)                       AS max_report_latency_s,
    AVG(CAST(report_latency_s AS float))        AS avg_report_latency_s,

    -- 5. Routine-cadence completeness against the declared PT1H cadence.
    --    6 routine reports are expected across the 6-hour window.
    SUM(CASE WHEN metar_type = 'METAR' THEN 1 ELSE 0 END)            AS routine_reports,
    SUM(CASE WHEN metar_type = 'METAR' THEN 1 ELSE 0 END) / 6.0      AS routine_cadence_completeness,
    CASE WHEN SUM(CASE WHEN metar_type = 'METAR' THEN 1 ELSE 0 END) < 6
         THEN 1 ELSE 0 END                                           AS routine_cadence_shortfall_flag
INTO output
FROM WithTendency
-- Hopping window, 6 hours long, advancing every 1 hour. Length is six declared
-- PT1H cycles so the aggregates have something to aggregate; the 1-hour hop
-- means output is emitted once per nominal report cycle.
GROUP BY icao_id, HoppingWindow(hour, 6, 1)
```

Partitioning is by `icao_id` throughout, in the `LAG` window and in the
`GROUP BY`: it carries `semanticRole: featureOfInterest` and is the only member
that identifies an individual source. `position` and `elevation` are station
constants and add nothing to the key.

## 3. What I did not compute

* **Any statistic over `wdir`.** `AVG(wdir)` is wrong across the 0/360
  discontinuity, and the schema states that `0` means "variable or calm", so a
  documented sentinel is mixed into the same numeric range as a real bearing due
  north. Nothing in the two files tells me how to tell those two cases apart,
  so I cannot filter the sentinel out before decomposing the bearing into
  components. For the same reason I did not combine `wdir` with `wspd` into a
  wind vector or compute directional shear against `LAG(wdir)`.
* **Anything numeric from `visib`.** The schema says the value is a string
  because it may carry qualifiers such as `10+` or fractions, and the instance
  confirms it with `"10+"`. No grammar for those qualifiers is given, so any
  `CAST` or substring rule would be a guess, and `10+` is a bound rather than a
  measurement in any case.
* **Ceiling height from `clouds`.** The member is a JSON array of `cover`/`base`
  pairs, but the files enumerate no cover codes and establish no ordering over
  them, so I cannot say which layer constitutes a ceiling. Without that, neither
  `MIN(base)` nor any layer count is interpretable.
* **A `flt_cat` deterioration or severity metric.** The schema names VFR, MVFR,
  IFR and LIFR but does not order them, so ranking them by severity would be
  imported knowledge. A pure change count — `flt_cat <> LAG(flt_cat)` — needs no
  ordering and is sound; I considered it and ranked it sixth, and dropped it
  rather than write a sixth metric.
* **A pass rate from `qc_field`.** The schema says it is a bitmask in which each
  bit records the outcome of one automated check, but it does not say which bit
  is which check, nor whether a set bit means pass or fail. The instance value
  `2` is therefore uninterpretable. No arithmetic on it is defensible.
* **`altim − slp`.** Both are hPa and both are `calculated`, but they are
  reductions to different data — aerodrome elevation under the standard
  atmosphere versus mean sea level using elevation and temperature history — and
  the files give neither reduction formula. Their difference is a number, not an
  interpretable residual. `slp` is also optional, so the difference would vanish
  intermittently. I did compute a tendency on `altim` rather than `slp` because
  `altim` is non-nullable in the schema.
* **Any cross-station aggregation, spatial gradient, or nearest-neighbour
  comparison** from `position` and `elevation`. The feed declares no relationship
  between stations and supplies no distance function, and a pressure or
  temperature gradient without one is meaningless.
* **Gust *ratio* `wgst / wspd`** in place of the difference. `wspd` can be zero
  when calm, which makes the ratio undefined exactly where gusts are most
  notable. The difference has neither problem and keeps the declared unit.
* **Threshold alarms on wind, temperature or pressure.** The files declare no
  operational limits for any of those members, so every threshold would be
  invented. The one threshold in the query — six routine reports per six hours —
  is read directly off the declared `cadence: {kind: fixed, period: PT1H}`.

## 4. Assumptions

* **Assumption:** the input stream alias is `input` and the sink alias is
  `output`. The files name neither.
* **Assumption:** `obs_time` reaches the job as a value the runtime can
  `TIMESTAMP BY`. The schema types it `datetime` but says the API delivers it as
  Unix epoch seconds, while the instance shows an ISO-8601 string; I assume the
  connector materialises it as a datetime. If it arrives as an integer it needs
  conversion before `TIMESTAMP BY`, which that clause does not permit, so the
  conversion would have to happen upstream.
* **Assumption:** the job's late-arrival and out-of-order tolerance is at least a
  few minutes. The instance shows a two-minute gap between `obs_time` and
  `report_time`, so events necessarily arrive after their event time; if the
  tolerance were tighter than that, records would be adjusted or dropped before
  `LAG` and the window ever saw them.
* **Assumption:** consecutive reports from one station are no more than three
  hours apart, which is what `LIMIT DURATION(hour, 3)` allows. This is derived
  from the declared PT1H cadence plus slack for two missed cycles, but the files
  do not bound the outage length, so a longer gap silently yields a null
  tendency rather than a spanning one.
* **Assumption:** it is acceptable for the altimeter tendency to be measured
  against whatever the previous report was, routine or `SPECI`. The files do not
  say `SPECI` reports carry a `altim` value of different provenance, and the
  tendency is normalised by actual elapsed seconds, so the rate stays comparable
  — but the interval it covers is then not a whole cycle.
* **Assumption:** `metar_type` is populated on routine reports. It is nullable in
  the schema, and a null is not counted as routine by the completeness metric,
  so a station that omits the member would read as permanently silent.
* **Assumption:** one record per station per `obs_time`, with no duplicate
  republication of the same observation. Only one instance is supplied, so
  neither uniqueness nor a deduplication key is established. A republished
  record would inflate the routine count and inject a zero-elapsed-time pair
  into the tendency, which the `> 0` guard drops.
* **Assumption:** a warm-up period is tolerated. The first hopping windows after
  a job start cover fewer than six real cycles and will raise the shortfall flag
  spuriously.
* **Assumption:** reading the dewpoint depression as a proxy for nearness to
  saturation, fog or cloud-base formation is domain knowledge the two files do
  not supply. The query computes only the arithmetic spread between two
  temperatures; any operational meaning attached to a small value is the
  reader's, not the schema's.
