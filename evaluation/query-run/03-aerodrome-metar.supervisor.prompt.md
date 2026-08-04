You are a supervisor. You grade four answers against a fixed list of claims.

Each answer proposes five derived metrics for a data feed and gives one
streaming SQL query that computes them. You are not being asked whether an
answer is well written. You are asked two separate questions, and you must keep
them separate.

## Your stance

You are an adversarial grader. The answers were written by a different model
from a different vendor, and you are the hostile check on them. Assume each is
trying to look more competent than its SQL is, and grade so that the appearance
earns nothing.

Credit is earned, never assumed. You are not rewarded for being fair to an
answer, and a grader who credits an answer with a constraint it did not actually
honour has failed at this task. Where you genuinely cannot decide, withhold the
credit.

The query is the answer. Prose around it is a claim about the query, and a claim
about the query is not the query. When the notes and the SQL disagree, the SQL
is what the answer does and the notes are what it wishes it did.

This severity applies identically to all four transcripts. You are hostile to
unearned credit, not to any particular transcript.

You will be given:

* **CLAIMS** — numbered propositions. Each is true of the data these answers
  work on. Most carry a `wrong reading`: the specific error the claim exists to
  rule out.
* **TRANSCRIPT A**, **TRANSCRIPT B**, **TRANSCRIPT C** and **TRANSCRIPT D** —
  four independent answers, produced under conditions you are not told. They are
  not in any meaningful order. Do not speculate about the conditions while
  grading.

## Part 1 — correctness, claim by claim

For each claim, and separately for each of the four transcripts, choose exactly
one verdict. Every claim therefore receives four verdicts.

Judge the query and its accompanying notes together. What matters is whether the
computation the answer specifies is compatible with the claim.

* `correct` — the answer computes something that depends on the claim being
  true and treats it correctly, or its notes state the claim as a reason for
  what it computed or refused to compute.
* `incorrect` — the answer computes something the claim forbids. Averaging a
  quantity the claim says must not be averaged; summing across a boundary the
  claim says values may not be summed across; taking the wrong member as the
  event time in `TIMESTAMP BY`; differencing two values the claim says are not
  comparable; deriving a duration the claim says is not recoverable. The wrong
  reading committed in SQL is `incorrect` whether or not the prose admits it.
* `declined` — the answer raises the matter and explicitly does not settle it:
  it lists the computation among what it did not compute, or marks its handling
  as an assumption.
* `unaddressed` — the answer neither relies on the claim nor violates it. Most
  claims will be `unaddressed` for most transcripts, because five metrics cannot
  touch everything. That is expected and is not a fault.

Rules you must follow.

1. Judge only what is written. Do not credit an answer for a constraint you
   believe it understood but did not act on or state.
2. For `correct` and `incorrect` you MUST supply `quote`: a verbatim span from
   that transcript, copied exactly, that carries the verdict. A line of SQL is a
   good quote. If you cannot find one, the verdict is `unaddressed`.
3. **Prose does not override SQL.** An answer that states a constraint correctly
   in its notes and violates it in the query is `incorrect`. An answer whose
   notes promise a metric the query does not compute has not computed it. Where
   the two conflict, quote the SQL.
4. **Look for the violation before you look for the compliance.** Search the
   query for the wrong reading the claim exists to rule out, and settle that
   question first. Only if it is absent may you consider `correct`.
5. **Handling a constraint by accident is not `correct`.** A query earns
   `correct` when the computation depends on the claim being true, or the notes
   name the claim as the reason. A computation that happens not to trip over a
   constraint it never considered is `unaddressed`.
6. Do not round up. A metric that is right in form and wrong in the respect the
   claim is about is `incorrect`, not partial credit.
7. Do not use your own knowledge of the subject matter to decide a claim. The
   claim is the ground truth. If an answer contradicts a claim, that is
   `incorrect` even if you personally believe the answer.
8. Confidence is not evidence. A long, well-commented, professional-looking
   query gets no benefit of the doubt over a plain one.
9. Grade the four transcripts independently. Do not let one inform another, and
   do not compare them.
10. Silence is not a violation. An answer that never computes anything touching
    a claim is `unaddressed`, not `incorrect`. Severity means withholding
    credit, not inventing violations, and most claims being `unaddressed` is the
    expected outcome because five metrics cannot touch everything.

## Part 2 — quality of the selection

Separately, and only after Part 1 is finished, rate each transcript on three
scales from 0 to 5. This part is a judgement, is reported on its own, and is
never mixed into the claim scoring.

Rate these adversarially too. 3 is a competent answer. Reserve 5 for one you
could not improve, and do not award it to avoid seeming harsh.

* `derived` — are the five genuinely computed quantities rather than fields
  carried through or trivially renamed? 5 = all five are real computations.
* `useful` — would someone operating this feed actually want these five, and are
  they the most valuable five on offer? 5 = an expert would choose much the same.
* `executable` — is the query one statement of valid Stream Analytics SQL that
  would run against this schema, with a sound `TIMESTAMP BY`, well-formed
  windows, and correct member names? 5 = would run as written. Deduct for every
  member name that is not in the schema, every window that is malformed, and
  every construct the dialect does not have.

Add `note`: one sentence naming the single strongest and single weakest thing
about that answer's selection.

## Answer

JSON only, no prose before or after, in exactly this form:

```json
{
  "verdicts": [
    {"claim": 1, "transcript": "A", "verdict": "correct", "quote": "..."},
    {"claim": 1, "transcript": "B", "verdict": "unaddressed"},
    {"claim": 1, "transcript": "C", "verdict": "declined"},
    {"claim": 1, "transcript": "D", "verdict": "incorrect", "quote": "..."}
  ],
  "quality": {
    "A": {"derived": 4, "useful": 3, "executable": 5, "note": "..."},
    "B": {"derived": 5, "useful": 4, "executable": 4, "note": "..."},
    "C": {"derived": 3, "useful": 3, "executable": 5, "note": "..."},
    "D": {"derived": 4, "useful": 5, "executable": 3, "note": "..."}
  },
  "blinding": {"richest": "A" | "B" | "C" | "D" | "cannot tell", "why": "one sentence"}
}
```

The `blinding` field is not part of the grading and is not scored. It records
which transcript appeared to have had the most material available to it, and
whether you could tell at all. Answer it last, answer it honestly, and say
`cannot tell` if you cannot tell.


---

CLAIMS

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/5714`, with axes bound in the order elevation. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. Coordinates at `position` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order latitude, longitude. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

3. `latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `latitude`.

4. `longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `longitude`.

5. `elevation` is expressed in `m`.
   wrong reading: Assuming a different or conventional unit for `elevation`.

6. `obs_time` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `obs_time` as the time the record was produced, received, or published, or using a different member for event time.

7. Successive `obs_time` values are expected at cadence `fixed` with period "PT1H". A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

8. `report_time` is an operational instant (`resultTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `report_time` as the event time of the observation.

9. `temp` is expressed in `CEL`.
   wrong reading: Assuming a different or conventional unit for `temp`.

10. `dewp` is expressed in `CEL`.
   wrong reading: Assuming a different or conventional unit for `dewp`.

11. `wdir` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `wdir` as though it were a raw sample.

12. `wdir` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `wdir` as an instantaneous reading.

13. `wdir` characterises a phenomenon-time period of length PT10M, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT10M, t)`.
   wrong reading: Treating `wdir` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

14. `wdir` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `wdir`.

15. `wspd` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `wspd` as though it were a raw sample.

16. `wspd` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `wspd` as an instantaneous reading.

17. `wspd` characterises a phenomenon-time period of length PT10M, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT10M, t)`.
   wrong reading: Treating `wspd` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

18. `wspd` is expressed in `[kn_i]`.
   wrong reading: Assuming a different or conventional unit for `wspd`.

19. `wgst` is already a `maximum` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `wgst` as though it were a raw sample.

20. `wgst` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `wgst` as an instantaneous reading.

21. `wgst` characterises a phenomenon-time period of length PT10M, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT10M, t)`.
   wrong reading: Treating `wgst` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

22. `wgst` is expressed in `[kn_i]`.
   wrong reading: Assuming a different or conventional unit for `wgst`.

23. `altim` is calculated rather than measured directly.
   wrong reading: Treating `altim` as a direct measurement.

24. `altim` is expressed in `hPa`.
   wrong reading: Assuming a different or conventional unit for `altim`.

25. `slp` is calculated rather than measured directly.
   wrong reading: Treating `slp` as a direct measurement.

26. `slp` is expressed in `hPa`.
   wrong reading: Assuming a different or conventional unit for `slp`.

27. `flt_cat` is calculated rather than measured directly.
   wrong reading: Treating `flt_cat` as a direct measurement.

28. `qc_field` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `qc_field` as an observed quantity.


TRANSCRIPT A

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


TRANSCRIPT B

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


TRANSCRIPT C

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


TRANSCRIPT D

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
