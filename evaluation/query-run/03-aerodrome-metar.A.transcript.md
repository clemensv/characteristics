# METAR stream — five derived metrics

## 1. The five metrics

Ordered by value, most valuable first.

1. **Gust excess over sustained wind, kt** — `wgst - wspd`, reported as the
   greatest value in the window. The schema states that `wgst` is the `maximum`
   and `wspd` the `mean` of the *same* ten-minute window (both carry
   `supportPeriod` `{ "length": "PT10M", "anchor": "end" }` and the same
   `observedProperty`), so the difference is the spread of one declared set, not
   a comparison of two unrelated readings. An operator wants it because gust
   spread — not mean wind — is what aircraft crosswind and gust limits are
   written against, and a station can sit at a benign mean wind while gusting
   well past a limit.

2. **Flight-category transition count** — number of reports in the window whose
   `flt_cat` differs from the previous report's `flt_cat` for the same
   `icao_id`. A category change is the event that moves an aerodrome between
   approach procedures and triggers diversion and alternate-minima decisions;
   the steady-state value is already carried, the *change* is not. Counting
   changes requires only inequality, so it needs no ordering over the four
   category values (see §3).

3. **Pressure tendency, hPa per hour, greatest fall and greatest rise** —
   `(altim - prev_altim) * 3600 / elapsed_s`, where `elapsed_s` is the
   *measured* interval between the two reports. `altim` is `calculated`,
   `instant`, in `hPa`, so successive values at one station are on a common
   footing and their rate of change is well defined. Rate of pressure change is
   the earliest indication in this feed that a front is crossing the aerodrome,
   and it leads the wind and category changes above. Sign is preserved (a fall
   and a rise are not the same event), so the window reports both extremes.

4. **Report dissemination latency, s** — `DATEDIFF(second, obs_time,
   report_time)`, greatest value in the window. `obs_time` is `phenomenonTime`
   (when the conditions obtained) and `report_time` is `resultTime` (when the
   encoded result was issued); their difference is exactly how stale a report is
   at the moment it becomes available. A rise in this number is a fault in the
   collection and encoding path, not in the weather, and it is invisible in any
   member taken alone.

5. **Cycle gap, s, and missed-cycle flag** — elapsed time since the same
   station's previous report, and a flag when it exceeds the declared cycle.
   `obs_time` carries `cadence` `{ "kind": "fixed", "period": "PT1H" }`. The
   specification says a consumer may use a declared period to size a window and
   to make "an absent value detectable as a gap rather than absorbed silently"
   (§ *The `cadence` Keyword*), which is precisely this metric. It tells the
   operator a station has gone quiet, which no field in a record that never
   arrives can tell them.

## 2. The query

```sql
WITH Stamped AS
(
    -- Event time is obs_time and nothing else. obs_time carries
    -- semanticRole = phenomenonTime: the instant the surface conditions
    -- obtained. report_time carries semanticRole = resultTime, i.e. when the
    -- result became available; it is deliberately NOT the event time, and is
    -- used below only to derive latency.
    SELECT
        icao_id,
        obs_time,
        report_time,
        wspd,
        wgst,
        altim,
        flt_cat
    FROM input TIMESTAMP BY obs_time
),

Deltas AS
(
    -- icao_id carries semanticRole = featureOfInterest and is the only member
    -- that identifies an individual source, so it is the partition key
    -- throughout. LIMIT DURATION is required on LAG; 6 hours bounds how far
    -- back a previous report may be found.
    SELECT
        icao_id,
        wspd,
        wgst,
        altim,
        flt_cat,
        DATEDIFF(second, obs_time, report_time) AS latency_s,
        DATEDIFF(
            second,
            LAG(obs_time, 1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)),
            obs_time
        ) AS elapsed_s,
        LAG(altim,   1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)) AS prev_altim,
        LAG(flt_cat, 1) OVER (PARTITION BY icao_id LIMIT DURATION(hour, 6)) AS prev_flt_cat
    FROM Stamped
),

PerReport AS
(
    SELECT
        icao_id,
        latency_s,
        elapsed_s,

        -- Metric 1. NULL when wgst is absent (the schema says wgst is omitted
        -- when no gusts were reported). Not coerced to 0: absence does not
        -- state that the gust equalled the mean.
        wgst - wspd AS gust_excess_kt,

        -- Metric 3. Normalised by the measured interval, never by the declared
        -- cadence, which is an expectation and not a constraint. The 1800 s
        -- floor keeps a short off-cycle interval from amplifying a small
        -- pressure difference (see Assumptions).
        CASE
            WHEN elapsed_s >= 1800
                 AND altim IS NOT NULL
                 AND prev_altim IS NOT NULL
            THEN (altim - prev_altim) * 3600.0 / elapsed_s
        END AS pressure_tendency_hpa_per_h,

        -- Metric 2. Inequality only; no ordering over the category values is
        -- assumed. A NULL on either side is not a transition, because an
        -- absent category is not a category.
        CASE
            WHEN prev_flt_cat IS NOT NULL
                 AND flt_cat IS NOT NULL
                 AND flt_cat <> prev_flt_cat
            THEN 1 ELSE 0
        END AS flt_cat_changed,

        -- Metric 5. Long side only: a gap longer than the declared PT1H cycle
        -- is evidence of a missing report, whereas a short gap is evidence of
        -- nothing (a SPECI is issued off-cycle by design).
        CASE WHEN elapsed_s > 5400 THEN 1 ELSE 0 END AS missed_cycle
    FROM Deltas
)

-- Window: TumblingWindow, size 1 hour, partitioned by icao_id.
-- The size is taken from the cadence declared on obs_time (fixed, PT1H), so a
-- window holds one routine cycle for a station plus any off-cycle reports
-- issued within it, and emits one row per station per cycle.
SELECT
    icao_id,
    System.Timestamp() AS window_end,
    MAX(gust_excess_kt)                 AS max_gust_excess_kt,
    SUM(flt_cat_changed)                AS flt_cat_changes,
    MIN(pressure_tendency_hpa_per_h)    AS fastest_pressure_fall_hpa_per_h,
    MAX(pressure_tendency_hpa_per_h)    AS fastest_pressure_rise_hpa_per_h,
    MAX(latency_s)                      AS max_report_latency_s,
    MAX(elapsed_s)                      AS max_cycle_gap_s,
    MAX(missed_cycle)                   AS missed_cycle_flag
INTO output
FROM PerReport
GROUP BY icao_id, TumblingWindow(hour, 1)
```

## 3. What I did not compute

* **Any average, or successive difference, of `wdir`.** Two reasons, either
  sufficient. It is a circular quantity, so an arithmetic mean and a plain
  subtraction both wrap incorrectly at 360°, and nothing in either file
  licenses circular arithmetic. Worse, the description states that a value of 0
  "indicates variable or calm" — 0 is a sentinel, not a direction, so any
  numeric treatment mixes a flag into an angle. A wind-shift or veer/back
  magnitude is therefore not available from this feed as declared.

* **Any numeric aggregate of `visib`.** It is typed `string` precisely because
  it carries qualifiers such as `"10+"`. `"10+"` is a bound, not a value, and
  the files define no grammar for parsing the string form. A mean or minimum
  visibility would require inventing that grammar and inventing a value for the
  bound.

* **A ceiling, or anything else, from `clouds`.** It is a JSON-encoded string of
  layer objects with a coverage code and a base height. The files neither define
  the coverage code list nor state which coverages constitute a ceiling, so
  "lowest broken-or-worse base" is not derivable from what is here.

* **A severity ranking or "deterioration" flag over `flt_cat`.** The description
  lists VFR, MVFR, IFR and LIFR but states no order among them, and the member
  carries neither `enum` nor a `codedValues` binding — its `observedProperty`
  points at a catalogue the files do not include. The specification's processing
  conformance rules forbid inferring a code-list binding or its ordering from
  names or samples. So metric 2 counts changes and refuses to say which
  direction is worse.

* **A "bad report" rate from `qc_field`.** It carries
  `semanticRole: resultQuality` and is described as a bitmask of automated
  check outcomes. The specification states that the quality scale is defined
  outside it, that it defines "no threshold, ordering, confidence model, or
  processing effect", and that omission does not imply acceptable quality. The
  files do not say which bit means what, nor that non-zero means failure. The
  instance value `2` is uninterpretable here, so no threshold was raised on it.

* **A spatial pressure field, or any cross-station aggregate of `altim`.**
  `altim` is described as reduced to *aerodrome elevation*, so values from
  stations with different `elevation` are not on a common surface and averaging
  them is meaningless. `slp` is reduced to mean sea level and would be the
  candidate, but it is declared omissible and its reduction consumes station
  elevation and a temperature history the record does not carry. More
  generally, `icao_id` is the `featureOfInterest`: combining different features
  is combining different subjects, and no annotation here licenses it.

* **A SPECI issuance rate from `metar_type`.** This was the strongest sixth
  candidate — `metar_type` carries `semanticRole: status` and the description
  gives the two literal values — but the specification requires a `status`
  member to constrain its states with `enum` or to identify the set defining
  them, and this schema does neither. The value set exists only in prose, so I
  did not branch the query on it. It is noted in §4 as the reason short cycle
  gaps are not flagged.

* **Dewpoint depression, `temp - dewp`.** Arithmetically this one is sound:
  both are `measured`, both `instant` against the same `phenomenonTime`, both
  in `CEL`, both for the same `icao_id`. I left it out because its *value* to an
  operator rests on a meteorological relationship — spread as a proxy for
  humidity, fog or icing risk — that neither file states, and I have five
  metrics whose value the files do establish. Included only as a note, not
  padded into the five.

* **Rate of change of `temp` between reports.** Sound on the same grounds as
  the pressure tendency, and omitted only because I judged pressure tendency
  the more valuable of the two and the brief allows five.

* **Pooling `wspd` and `wgst` into one wind-speed series.** The specification
  states that two results carrying the same observable property and different
  `statistic` values "are not comparable as like quantities". Metric 1 does not
  pool them; it takes the difference between the maximum and the mean of one
  set that the schema explicitly declares to be the same set.

* **Anything reconstructed from `raw_ob`.** Re-parsing the raw text would
  re-derive members the schema has already decoded, and the files define no
  grammar for it. `name`, `position`, `elevation` and `wx_string` are carried
  identity, location and text; nothing is derived from them, and copying them
  would not count towards the five in any case.

* **Filling a missing cycle.** The declared `cadence` is not used to synthesise
  a report, a value, or a successor. The specification is explicit that cadence
  must not do this, and metric 5 only reports that the gap occurred.

## 4. Assumptions

* **Assumption:** `obs_time` and `report_time` lie on the same time line and are
  directly differenceable. Neither carries a `temporalReferenceSystem`, so I
  read both as Core `datetime` in UTC; the descriptions support this (`obs_time`
  delivered as Unix epoch seconds, `report_time` as an ISO 8601 UTC string) but
  no annotation states it.

* **Assumption:** the job's out-of-order and late-arrival tolerance is
  configured to exceed the observed latency. `TIMESTAMP BY obs_time` means every
  report reaches the job after its own event time, by the amount metric 4
  measures (120 s in the sample instance). This is job configuration, not SQL,
  and if it is set too tight the windows will drop late reports.

* **Assumption:** the missed-cycle threshold of 5400 s (1.5 × the declared
  `PT1H`) is my choice. The specification is explicit that a cadence is an
  expectation and not a constraint, that an instance departing from it is not
  invalid, and that the threshold is a decision the consumer makes about its own
  processing. Any other tolerance is equally defensible.

* **Assumption:** the 1800 s floor on `elapsed_s` before computing a pressure
  tendency is my choice, not a rule from the files. Its purpose is to stop a
  short off-cycle interval — the schema's description of `metar_type` implies
  SPECI reports arrive between routine cycles — from multiplying a small `altim`
  difference into a large apparent hourly rate.

* **Assumption:** `LIMIT DURATION(hour, 6)` is an adequate reach for `LAG`. A
  station silent longer than six hours yields NULL for `elapsed_s`,
  `prev_altim` and `prev_flt_cat`, so the deltas are NULL rather than wrong;
  the trade-off is that a very long outage stops being measured by metric 5
  rather than being reported as an enormous gap.

* **Assumption:** an absent `wgst` should propagate as NULL rather than as a
  zero gust excess. `wgst` is typed `int32` and is not in `required`, and its
  description says it is omitted when no gusts were reported. Reading absence
  as "gust equalled the mean" would be an inference the files do not license,
  so `MAX` simply skips those reports.

* **Assumption:** `altim` may be absent from a report even though its type is
  non-nullable, since it is not listed in `required`. The tendency guards for
  this explicitly.

* **Assumption:** no unit conversion is performed anywhere. Knots (`[kn_i]`),
  hectopascals (`hPa`) and degrees Celsius (`CEL`) pass through unchanged, and
  the output columns are in those units. The specification forbids inferring
  permission to convert, and nothing here needs it.

* **Assumption:** window alignment. Azure Stream Analytics aligns a
  `TumblingWindow(hour, 1)` to the clock hour, whereas routine METARs are issued
  near the end of the hour (11:51Z in the instance). Consecutive reports for one
  station therefore fall in different windows. This does not affect the metrics,
  because every difference is computed per event in `PerReport` before any
  window is applied; it affects only which window a given difference is reported
  in.

* **Assumption:** a station with no reports in an hour produces no output row —
  Stream Analytics emits nothing for an empty group. Absence is therefore
  detected by metric 5 on the *next* report to arrive, not by a missing row at
  the time the cycle is skipped. A downstream consumer that needs the alert
  sooner needs a separate reference-data join against a station list, which the
  files do not provide.
