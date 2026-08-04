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

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order latitude, longitude. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. `latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `latitude`.

3. `longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `longitude`.

4. `timestamp` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `timestamp` as the time the record was produced, received, or published, or using a different member for event time.

5. Successive `timestamp` values are expected at cadence `fixed` with period "PT5M". A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

6. `wind_direction` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `wind_direction` as though it were a raw sample.

7. `wind_direction` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `wind_direction` as an instantaneous reading.

8. `wind_direction` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `wind_direction`.

9. `wind_speed` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `wind_speed` as though it were a raw sample.

10. `wind_speed` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `wind_speed` as an instantaneous reading.

11. `wind_speed` is expressed in `m/s`.
   wrong reading: Assuming a different or conventional unit for `wind_speed`.

12. `gust` is already a `maximum` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `gust` as though it were a raw sample.

13. `gust` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `gust` as an instantaneous reading.

14. `gust` is expressed in `m/s`.
   wrong reading: Assuming a different or conventional unit for `gust`.

15. `wave_height` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `wave_height` as though it were a raw sample.

16. `wave_height` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `wave_height` as an instantaneous reading.

17. `wave_height` characterises a phenomenon-time period of length PT20M, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT20M, t)`.
   wrong reading: Treating `wave_height` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

18. `wave_height` is expressed in `m`.
   wrong reading: Assuming a different or conventional unit for `wave_height`.

19. `dominant_wave_period` is calculated rather than measured directly.
   wrong reading: Treating `dominant_wave_period` as a direct measurement.

20. `dominant_wave_period` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `dominant_wave_period` as an instantaneous reading.

21. `dominant_wave_period` characterises a phenomenon-time period of length PT20M, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT20M, t)`.
   wrong reading: Treating `dominant_wave_period` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

22. `dominant_wave_period` is expressed in `s`.
   wrong reading: Assuming a different or conventional unit for `dominant_wave_period`.

23. `average_wave_period` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `average_wave_period` as though it were a raw sample.

24. `average_wave_period` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `average_wave_period` as an instantaneous reading.

25. `average_wave_period` characterises a phenomenon-time period of length PT20M, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT20M, t)`.
   wrong reading: Treating `average_wave_period` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

26. `average_wave_period` is expressed in `s`.
   wrong reading: Assuming a different or conventional unit for `average_wave_period`.

27. `mean_wave_direction` is calculated rather than measured directly.
   wrong reading: Treating `mean_wave_direction` as a direct measurement.

28. `mean_wave_direction` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `mean_wave_direction` as an instantaneous reading.

29. `mean_wave_direction` characterises a phenomenon-time period of length PT20M, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT20M, t)`.
   wrong reading: Treating `mean_wave_direction` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

30. `mean_wave_direction` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `mean_wave_direction`.

31. `pressure` is calculated rather than measured directly.
   wrong reading: Treating `pressure` as a direct measurement.

32. `pressure` is expressed in `hPa`.
   wrong reading: Assuming a different or conventional unit for `pressure`.

33. `air_temperature` is expressed in `CEL`.
   wrong reading: Assuming a different or conventional unit for `air_temperature`.

34. `water_temperature` is expressed in `CEL`.
   wrong reading: Assuming a different or conventional unit for `water_temperature`.

35. `dewpoint` is calculated rather than measured directly.
   wrong reading: Treating `dewpoint` as a direct measurement.

36. `dewpoint` is expressed in `CEL`.
   wrong reading: Assuming a different or conventional unit for `dewpoint`.

37. `pressure_tendency` is calculated rather than measured directly.
   wrong reading: Treating `pressure_tendency` as a direct measurement.

38. `pressure_tendency` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `pressure_tendency` as an instantaneous reading.

39. `pressure_tendency` characterises a phenomenon-time period of length PT3H, stated by the schema rather than carried in the record. The period closes at the anchoring position and runs back to it. The anchoring position is the sibling annotated `phenomenonTimeEnd`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t - PT3H, t)`.
   wrong reading: Treating `pressure_tendency` as an instantaneous reading at the record timestamp, running its period forward from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

40. `pressure_tendency` is expressed in `hPa`.
   wrong reading: Assuming a different or conventional unit for `pressure_tendency`.

41. `visibility` is expressed in `[nmi_i]`.
   wrong reading: Assuming a different or conventional unit for `visibility`.

42. `tide` is expressed in `[ft_i]`.
   wrong reading: Assuming a different or conventional unit for `tide`.


TRANSCRIPT A

# Five derived metrics for the `BuoyObservation` stream

## 1. The five metrics

1. **Pressure-tendency divergence (hPa/h).** The pressure rate observed between
   two consecutive records, minus the mean rate the record already declares
   (`pressure_tendency / 3`, since the schema defines that member as the signed
   change over the *preceding 3 hours* ending at the observation time). Both
   terms are signed hPa per hour, so the difference says whether the pressure
   change right now is faster or slower than the three-hour average it is being
   folded into. An operator wants this because the carried tendency is a
   three-hour smoother and therefore lags: a system that has begun to deepen
   shows up in the divergence long before it dominates the tendency. It is a
   residual against a reference the schema itself declares, which is the
   strongest kind of derived value this feed supports.

2. **Gust factor (dimensionless).** `gust / wind_speed`, reported as window mean
   and window maximum. The schema states that `gust` is the greatest
   short-interval speed *within the same averaging window that produced*
   `wind_speed`, so the ratio is well defined even though the length of that
   window is left indeterminate — the unknown length cancels. An operator wants
   it because absolute wind speed does not distinguish a steady 7 m/s from a
   squally 7 m/s with 15 m/s peaks, and it is the peaks that part mooring lines
   and knock down small craft.

3. **Cadence completeness and longest gap.** Records received per station per
   window against the number the schema says to expect (one per five-minute
   slot), plus the longest interval between consecutive observations in the
   window. The schema declares the publication cadence explicitly, so a
   shortfall is measurable rather than guessed. An operator wants it first
   because it is the metric that tells them whether to trust the other four:
   every window mean here silently degrades when the platform or the ingest
   thins out, and nothing else in the record reveals that.

4. **Sea-state build rate (m/h).** Signed change in significant wave height per
   hour between consecutive observations, reported as window mean, fastest build
   and fastest decay. The height says how big the sea is; the rate says whether
   it is building or laying down, which is the quantity a departure-or-hold
   decision actually turns on.

5. **Spectral period ratio (dimensionless).** `dominant_wave_period /
   average_wave_period`. The schema defines DPD as the period of the band
   carrying maximum energy and APD as the mean of all wave periods in the
   sampling window; a ratio well above 1 therefore means the energy peak sits at
   periods substantially longer than the typical wave, i.e. long-period energy
   coexisting with shorter ones. An operator wants it because a 1.8 m sea at
   ratio ≈ 1 and a 1.8 m sea at ratio ≈ 2 are different sea states for the same
   reported height.

## 2. The query

```sql
-- Dialect: Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
--
-- Event time   : [timestamp] -- the only temporal member the schema carries.
-- Source key   : station_id  -- the only member that identifies an observing platform.
-- Aggregation  : TumblingWindow(minute, 30), non-overlapping, one row per station
--                per window. 30 minutes is six of the five-minute slots the schema
--                says the producer emits, which gives the cadence metric an integer
--                denominator and gives the pressure-rate mean six samples to average.
-- Event-to-event reach: LAG(..., 1) OVER (PARTITION BY station_id
--                LIMIT DURATION(minute, 30)). The LIMIT DURATION is required by the
--                dialect; 30 minutes doubles as the cut-off beyond which no rate of
--                change is emitted at all, so nothing is differenced across an outage.

WITH Observations AS
(
    SELECT
        station_id,
        CAST([timestamp] AS datetime) AS obs_time,
        wind_speed,
        gust,
        pressure,
        pressure_tendency,
        wave_height,
        dominant_wave_period,
        average_wave_period
    FROM input TIMESTAMP BY [timestamp]
),

-- Reach this station's previous observation.
Previous AS
(
    SELECT
        station_id,
        obs_time,
        wind_speed,
        gust,
        pressure,
        pressure_tendency,
        wave_height,
        dominant_wave_period,
        average_wave_period,
        LAG(obs_time,    1) OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_time,
        LAG(pressure,    1) OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_pressure,
        LAG(wave_height, 1) OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_wave_height
    FROM Observations
),

PerEvent AS
(
    SELECT
        station_id,
        obs_time,

        -- Elapsed time since this station's previous record. NULL if there was none
        -- inside the LAG reach, which correctly nulls every rate below.
        DATEDIFF(second, prev_time, obs_time) AS gap_seconds,

        -- METRIC 2. gust and wind_speed share one averaging window per the schema,
        -- so the ratio needs no knowledge of that window's length. Undefined at calm.
        CASE WHEN wind_speed > 0 THEN gust / wind_speed END AS gust_factor,

        -- METRIC 5. Both periods are seconds over the same record's sampling of the sea.
        CASE WHEN average_wave_period > 0
             THEN dominant_wave_period / average_wave_period
        END AS period_ratio,

        -- METRIC 1, first half: pressure rate observed between consecutive records.
        CASE WHEN DATEDIFF(second, prev_time, obs_time) > 0
             THEN (pressure - prev_pressure) * 3600.0
                  / DATEDIFF(second, prev_time, obs_time)
        END AS pressure_rate_hpa_per_h,

        -- METRIC 1, second half: that rate minus the declared 3-hour mean rate.
        -- pressure_tendency is a signed 3-hour change in the same sea-level-reduced
        -- quantity as `pressure`, so /3.0 puts both terms in hPa per hour.
        CASE WHEN DATEDIFF(second, prev_time, obs_time) > 0
             THEN ((pressure - prev_pressure) * 3600.0
                   / DATEDIFF(second, prev_time, obs_time))
                  - (pressure_tendency / 3.0)
        END AS tendency_divergence_hpa_per_h,

        -- METRIC 4. Signed change in significant wave height, per hour.
        CASE WHEN DATEDIFF(second, prev_time, obs_time) > 0
             THEN (wave_height - prev_wave_height) * 3600.0
                  / DATEDIFF(second, prev_time, obs_time)
        END AS wave_rate_m_per_h

    FROM Previous
)

SELECT
    station_id,
    System.Timestamp() AS window_end,

    -- METRIC 1. Averaged over the 30-minute tumbling window to lift the signal above
    -- the quantisation of a five-minute pressure difference (see Assumptions).
    AVG(tendency_divergence_hpa_per_h) AS tendency_divergence_hpa_per_h,
    AVG(pressure_rate_hpa_per_h)       AS observed_pressure_rate_hpa_per_h,

    -- METRIC 2.
    AVG(gust_factor) AS gust_factor_mean,
    MAX(gust_factor) AS gust_factor_max,

    -- METRIC 3. Denominator 6 = 30-minute window / declared 5-minute slot.
    COUNT(*)         AS observations_received,
    COUNT(*) / 6.0   AS cadence_completeness,
    MAX(gap_seconds) AS longest_gap_seconds,

    -- METRIC 4. MAX is the fastest build, MIN the fastest decay; both are signed.
    AVG(wave_rate_m_per_h) AS wave_rate_mean_m_per_h,
    MAX(wave_rate_m_per_h) AS wave_rate_fastest_build_m_per_h,
    MIN(wave_rate_m_per_h) AS wave_rate_fastest_decay_m_per_h,

    -- METRIC 5.
    AVG(period_ratio) AS period_ratio_mean

INTO output
FROM PerEvent
GROUP BY station_id, TumblingWindow(minute, 30)
```

## 3. What I did not compute

* **Angular separation of `wind_direction` and `mean_wave_direction`** (a
  wind-against-sea alignment metric). The schema states that `wind_direction` is
  the direction the wind is coming *from*. It states no convention at all for
  `mean_wave_direction` — from or towards. A separation of 0° therefore means
  either "wind and waves aligned" or "wind and waves exactly opposed", depending
  on a fact the files do not supply. The number would be uninterpretable, so I
  left it out.
* **Any window mean of `wind_direction` or `mean_wave_direction`.** They are
  degrees on a circle: `AVG()` over 350° and 10° returns 180°, which is the
  opposite of the truth. A correct circular mean needs a sine/cosine
  decomposition, and I preferred to omit the value rather than publish a scalar
  average that is wrong precisely at the wrap point.
* **Reconstructing the true three-hour change, `pressure` minus `pressure` three
  hours earlier**, to check `pressure_tendency` directly. `LAG` reaches the
  immediately preceding event, not the event three hours back, and pulling the
  first and last `pressure` out of a three-hour `HoppingWindow` would need
  `FIRST`/`LAST`/`TopOne`, whose availability in this dialect I could not
  confirm from what I was given. Comparing *rates* gets at the same divergence
  using only constructs I was told exist.
* **Threshold flags** on `wind_speed`, `gust`, `wave_height` or
  `pressure_tendency` (gale warning, storm-force, dangerous sea). The files
  declare units but no thresholds, no station class and no climatology; any
  cut-off would be a number I invented.
* **Wave steepness** from `wave_height` and `dominant_wave_period`. Converting a
  period to a wavelength requires the deep-water dispersion relation and a value
  of *g*. Neither is in the two files, and the ratio without that conversion is
  not steepness.
* **`air_temperature − water_temperature` and `water_temperature − dewpoint`.**
  Both are arithmetically sound — same units, same platform, same record. I
  ranked them below the five above, and the second one's value rests on
  `dewpoint` being the saturation temperature of the air, which the schema names
  but never states.
* **Anything over `visibility` and `tide`.** Neither is required, neither
  appears in the one example record, and the schema says visibility is generally
  only available on C-MAN stations — a class the record does not carry. A window
  aggregate would be taken over an unknown, station-dependent sample.
* **Position change from `latitude`/`longitude` between records** (mooring watch
  circle, drift). Nothing in the files says the platform moves, and nothing
  gives a position accuracy, so a non-zero displacement could not be told apart
  from sensor jitter.
* **Any cross-station aggregate.** The files establish no region membership, no
  spacing, and no way to tell a deep-ocean buoy from a C-MAN station or a
  partner platform. A mean pressure or wave height across an arbitrary set of
  stations in one window is not a quantity.

## 4. Assumptions

Each of the following is an assumption; the two files do not establish it.

* **Assumption:** `timestamp` is the correct event time for windowing and is
  populated on every record. (The schema does make it required; that it is the
  intended event time rather than, say, a publication time, is my reading.)
* **Assumption:** the producer actually meets the declared cadence closely
  enough that six records per 30-minute window is the right denominator, and
  there are no duplicates or replays. Duplicates would push
  `cadence_completeness` above 1, which is why the raw `observations_received`
  is emitted alongside it.
* **Assumption:** the five-minute gaps are near-uniform, so the mean of
  per-event rates approximates the rate over the whole window. Where gaps are
  irregular the mean is weighted by record count rather than by elapsed time.
* **Assumption:** `pressure` is reported at about 0.1 hPa resolution — I infer
  this from the single value `1016.4` in the one example record. If so, a
  five-minute difference is quantised at roughly ±1.2 hPa/h, and only the
  30-minute mean makes the divergence in metric 1 readable. A finer or coarser
  resolution would change the window size I would choose.
* **Assumption:** `wave_height`, `average_wave_period` and
  `dominant_wave_period` in one record describe the same stretch of sea, ending
  at the observation time. The schema gives 20 minutes for the first two, gives
  no window at all for `dominant_wave_period`, and never says any of these
  windows end at the observation time.
* **Consequence of the above, not an assumption:** consecutive records are ~5
  minutes apart while `wave_height` summarises ~20 minutes, so successive values
  share most of their sampling window. `wave_rate_m_per_h` is therefore a
  smoothed derivative of an already-smoothed quantity, not an independent
  difference. It is still directional and still useful; it is not a measurement
  of how much the sea changed in five minutes.
* **Assumption:** `station_id` is stable and unique per platform for the life of
  the stream, and a station does not change type mid-stream. The schema says it
  identifies the platform; persistence is my reading.
* **Assumption:** the aggregate functions ignore NULLs, so a window mean may be
  taken over fewer rows than `observations_received` when an optional member
  such as `wave_height` or `pressure_tendency` is absent. The count is emitted
  so a consumer can see that the denominators may differ.
* **Not an assumption, stated by the schema and relied on:** `gust` and
  `wind_speed` share one averaging window (metric 2), and `pressure_tendency` is
  a signed change in the same sea-level-reduced pressure over the three hours
  ending at the observation time, negative for falling (metric 1). Both metrics
  would be unsound without those two sentences.
* **Assumption about the dialect:** that multi-step `WITH ... AS` feeding a
  single `SELECT ... INTO`, `LAG` with `LIMIT DURATION`, `DATEDIFF(second, …)`
  and `CASE` inside a windowed `SELECT` are all accepted as written. I stayed
  inside the constructs I was told exist and avoided `FIRST`/`LAST`/`TopOne`,
  `COUNT(DISTINCT …)` and any trigonometric function for that reason.


TRANSCRIPT B

# BuoyObservation — five derived metrics

## 1. The five metrics

1. **Gust factor** — `gust / wind_speed`, emitted both for the newest record in the window and as the window maximum. The schema states that `gust` is the peak short-interval speed *within the same averaging window that produced* `wind_speed`, so the ratio is a like-for-like comparison and is dimensionless: it is the one wind metric that stays valid even though the schema refuses to fix the length of that averaging window (8 min for buoys, 2 min for land stations, and the record does not say which). An operator wants it because it separates a steady blow from a gusty, squally one at the same mean speed, which is the difference that matters to anything floating or lifting.

2. **Pressure rate of change, hPa per hour** — the signed change in `pressure` between the first and last record of the window, divided by the *actual* elapsed seconds between those two records. `pressure_tendency` is carried and describes the preceding 3 hours; this is computed and refreshes every 5 minutes, so an operator sees a pressure fall developing without waiting for the three-hour figure to catch up.

3. **Cadence completeness** — `COUNT(*)` over the window against the count the declared `cadence` (`fixed`, `PT5M`) implies. This is a residual against a reference the schema itself declares. An operator wants it because a station that has stopped reporting, or is reporting off-slot, is invisible in every other metric here — they simply go quiet — and because it tells you whether to trust metrics 2 and 4, both of which depend on the window being fully populated.

4. **Pressure-tendency residual** — the observed 3-hour change in `pressure` reconstructed from the stream, minus the declared `pressure_tendency` for the same interval. The schema defines `pressure_tendency` as the signed change in sea-level pressure over the preceding 3 hours, and the stream carries `pressure`; therefore the stream can reproduce that quantity, and a non-trivial disagreement is a defect in the barometer, in the reduction to sea level, or in the producer's encoding. An operator wants it as a self-contained quality check that needs no external reference.

5. **Wave period spread** — `dominant_wave_period - average_wave_period`, and its maximum over the window. Both are seconds, both share the same `supportPeriod` of `PT20M` anchored at the end, so the subtraction is between two summaries of the same 20 minutes. The schema says `dominant_wave_period` is the period of the band carrying maximum energy while `average_wave_period` is the mean of all wave periods; a large positive spread therefore means the energy peak sits well away from the bulk of the field, i.e. a long-period component coexisting with a shorter-period one. An operator wants it because a single significant wave height hides that structure entirely.

## 2. The query

```sql
-- Event time is the member the schema marks semanticRole=phenomenonTime.
-- Source identity is station_id, the member the schema marks
-- semanticRole=featureOfInterest; everything is partitioned by it.
WITH observations AS (
    SELECT
        station_id,
        [timestamp] AS observed_at,
        pressure,
        pressure_tendency,
        -- guard: the ratio is undefined at zero wind
        CASE WHEN wind_speed > 0 THEN gust / wind_speed END AS gust_factor,
        -- NULL if either period member is absent, which is the wanted behaviour
        dominant_wave_period - average_wave_period AS wave_period_spread
    FROM input
    TIMESTAMP BY [timestamp]
),

-- Window type: HoppingWindow. Size 185 minutes, hop 5 minutes, per station.
-- The size is 185 and not 180 deliberately: at the declared PT5M cadence a
-- full window holds 37 records whose first and last are exactly 36 x 300 s
-- = 3 hours apart, which is the interval pressure_tendency declares. A
-- 180-minute window would span only 175 minutes of observations and the
-- residual in metric 4 would compare mismatched intervals. The 5-minute hop
-- makes the output refresh at the cadence of the feed.
station_window AS (
    SELECT
        station_id,
        System.Timestamp() AS window_end,
        COUNT(*) AS record_count,
        MAX(gust_factor) AS gust_factor_max,
        MAX(wave_period_spread) AS wave_period_spread_max,
        -- TopOne() OVER (ORDER BY ...) returns the whole record; I am
        -- reasonably but not fully confident of this exact form and of the
        -- dotted field access on its result in every version of this dialect.
        -- It is used instead of LAG(pressure, 36) so that the endpoints are
        -- found by time rather than by counting records, which would break
        -- silently whenever the station drops a slot.
        TopOne() OVER (ORDER BY observed_at DESC) AS newest,
        TopOne() OVER (ORDER BY observed_at ASC) AS oldest
    FROM observations
    GROUP BY station_id, HoppingWindow(minute, 185, 5)
),

spans AS (
    SELECT
        station_id,
        window_end,
        record_count,
        gust_factor_max,
        wave_period_spread_max,
        newest.gust_factor AS gust_factor_latest,
        newest.pressure AS pressure_newest,
        oldest.pressure AS pressure_oldest,
        newest.pressure_tendency AS pressure_tendency_declared,
        DATEDIFF(second, oldest.observed_at, newest.observed_at) AS span_seconds
    FROM station_window
)

SELECT
    station_id,
    window_end,
    record_count,

    -- 1. Gust factor: newest record, and the worst seen in the window.
    gust_factor_latest,
    gust_factor_max,

    -- 2. Pressure rate of change, hPa/hour, over the actual observed span.
    --    Suppressed below an hour of span: too short to be a trend.
    CASE
        WHEN span_seconds >= 3600
        THEN (pressure_newest - pressure_oldest) * 3600.0 / span_seconds
    END AS pressure_rate_hpa_per_hour,

    -- 3. Cadence completeness against the declared PT5M cadence.
    --    37 = 185 minutes / 5 minutes. Below 1.0 means dropped slots;
    --    above 1.0 means duplicate or off-slot records, equally informative.
    CAST(record_count AS float) / 37.0 AS cadence_completeness,

    -- 4. Residual of the reconstructed 3-hour pressure change against the
    --    declared pressure_tendency. Only evaluated when the window endpoints
    --    really are 3 hours apart (+/- 5 minutes), so a gapped window
    --    produces NULL rather than a false alarm.
    CASE
        WHEN ABS(span_seconds - 10800) <= 300
             AND pressure_tendency_declared IS NOT NULL
        THEN (pressure_newest - pressure_oldest) - pressure_tendency_declared
    END AS pressure_tendency_residual_hpa,

    -- 5. Wave period spread, worst in the window.
    wave_period_spread_max

INTO output
FROM spans
```

## 3. What I did not compute

* **Wind-versus-wave misalignment**, `wind_direction` against `mean_wave_direction`. The schema states the convention for `wind_direction` explicitly — "the direction the wind is coming from" — and pointedly states no convention for `mean_wave_direction`. The difference is therefore ambiguous by 180 degrees, and a misalignment metric that may be inverted is worse than none. Separately, the two members do not describe the same interval: `mean_wave_direction` carries `supportPeriod` `PT20M`, while `wind_direction` carries none at all because its averaging period depends on station type that the record does not transmit.
* **Any mean or standard deviation of a direction member** — `wind_direction`, `mean_wave_direction`. These are circular quantities; arithmetic `AVG` over them is wrong across the 0/360 discontinuity, and the dialect offers no circular-mean aggregate. `MAX(gust_factor)` is safe in a way `AVG(wind_direction)` is not.
* **Wave steepness**, e.g. `wave_height / (dominant_wave_period * dominant_wave_period)`. Turning a height and a period into a steepness requires the deep-water dispersion relation. The two files supply no such relation, no water depth, and no constant; the ratio would be a number with no defined meaning.
* **Windowed mean of `wave_height`, `average_wave_period` or `dominant_wave_period`.** Records arrive every 5 minutes but each of these carries a `supportPeriod` of `PT20M` anchored at the end, so four consecutive records describe overlapping 20-minute intervals. A mean over them is a mean of non-independent, overlapping samples. `wave_height` compounds this: it is already the mean of the highest third of the waves, so averaging it again produces a statistic of a statistic whose meaning the schema does not define. I accepted the same overlap objection for `MAX(wave_period_spread)` in metric 5 because a maximum over overlapping supports still answers "did the spread reach this value", whereas a mean answers nothing definite.
* **Windowed aggregate of `pressure_tendency` itself.** It already summarises a `PT3H` interval; averaging values whose supports overlap by 2 hours 55 minutes is not interpretable. Its value in the query is as a reference to subtract against, not as something to aggregate.
* **`water_temperature - air_temperature`, and `air_temperature - dewpoint`.** Both subtractions are clean — same unit `CEL`, same `phenomenonTimeRelation` of `instant`, same platform — and I nearly used one of them. I left both out because everything that would make them *actionable* to an operator (sea fog, boundary-layer stability, approach to saturation) is meteorology the two files do not state. A bare signed temperature difference is not worth one of five places.
* **Anything derived from `visibility` or `tide`.** Both are absent from the only instance and neither is in `required`. The schema says `visibility` is "generally only available on C-MAN stations" with a range capped at 1.6 nmi, and `tide` is a coastal and C-MAN measurement; the record carries nothing that says which kind of platform it came from, so a metric over either would be null for most sources and could not distinguish "sensor not fitted" from "sensor failed". A tidal rate of change would additionally require separating astronomical tide from surge, which needs a harmonic prediction not present here.
* **Platform drift from `latitude` and `longitude`.** Nothing in the schema says whether the platform is moored or free-drifting, so there is no basis for deciding that a change in position is an anomaly rather than the normal behaviour of the source.
* **Any cross-station aggregation**, e.g. a regional mean `pressure`. `station_id` is the declared `featureOfInterest`; the files define no grouping of stations, and `latitude`/`longitude` under EPSG:4326 do not by themselves license a spatial bucket without a declared tessellation.
* **A named alert threshold on the gust factor or the pressure rate.** Both metrics are emitted as numbers rather than as boolean flags because the files supply no threshold for either, and any constant I chose would be imported from outside them.

## 4. Assumptions

* **Assumption:** the input stream is named `input` and the sink `output`.
* **Assumption:** absent measurements arrive as SQL `NULL`. The files state that only `station_id`, `latitude`, `longitude` and `timestamp` are required, and the instance omits `visibility` and `tide` entirely, but they do not say how an absent value is represented on the wire. If the producer instead passes through a numeric fill value for a missing reading, every metric above is corrupted and no guard in this query would catch it.
* **Assumption:** the declared `cadence` of `PT5M` is the intended publication rate for *every* station, so a shortfall in `record_count` is a gap rather than a legitimate slower rate. The schema says the producer "is expected to publish one record per station per five-minute slot", which is the basis for this, but it is an expectation and not a constraint.
* **Assumption:** records land on aligned 5-minute slots. This is what makes a 185-minute window span exactly 3 hours of observations and therefore what makes metric 4 an interval-matched comparison. The `+/- 300 s` guard limits the damage if it is false, at the cost of suppressing the residual instead.
* **Assumption:** `station_id` is stable over time and not reassigned between platforms; the schema calls it an identifier assigned by NDBC but says nothing about reuse.
* **Assumption:** `timestamp` is an acceptable event time for the whole record. The schema marks it `phenomenonTime`, but the record's members do not all describe that instant: the wave members summarise the preceding `PT20M`, `pressure_tendency` the preceding `PT3H`, and the wind members an interval of undeclared length. Aligning all of them on their common end anchor is the only choice the schema supports, but it means the window boundaries cut through the support periods of most members.
* **Assumption:** a `wind_speed` of exactly zero is a genuine calm rather than a placeholder; the query emits `NULL` for the gust factor in that case rather than treating it as an infinite ratio.
* **Assumption:** the sign convention for `pressure_tendency` is applied consistently by the producer — the schema states negative means falling — since the residual in metric 4 is a signed subtraction and a producer that inverted the sign would show as a residual of twice the tendency rather than as an obvious error.
* **Assumption about the dialect, not the data:** `TopOne() OVER (ORDER BY ...)` as a windowed aggregate, and dotted field access on the record it returns, are supported. The alternative, `LAG(pressure, 36) OVER (PARTITION BY station_id LIMIT DURATION(hour, 3))`, is syntax I am more confident of but is semantically worse, because a fixed record offset silently means something other than "3 hours ago" the moment a station drops a slot.
* **Design note, not an assumption:** metrics 2 and 4 share the same two pressure endpoints. They are kept separate because one is the magnitude and sign of a trend and the other is a consistency check on a carried member; a reader should treat metric 4 as meaningful only when metric 3 shows the window was fully populated.


TRANSCRIPT C

# BuoyObservation — five derived metrics

## 1. The five metrics

1. **Gust factor** — `gust / wind_speed` per report, then the window maximum and mean. It is a ratio of two members the schema types identically, so it is dimensionless and survives the fact that no unit is declared anywhere in the schema; an operator watching for squalls wants the peak-to-sustained ratio, and neither member alone shows it.
2. **Pressure rate of change per hour** — signed change in `pressure` between successive reports from the same `station_id`, normalised to an hour by the actual gap between reports. Even without knowing the unit of `pressure`, the sign and the magnitude relative to the same station's own history are the earliest warning this record set contains.
3. **Wave-height rate of change per hour** — the same successive-difference treatment of `wave_height`. `wave_height` itself is carried; whether the sea is building or decaying, and how fast, is not, and that is the part an operator acts on.
4. **Wind/wave misalignment** — the circular difference between `wind_direction` and `mean_wave_direction`, folded into 0–180°. This is the only cross-member relation the record licenses between the wind block and the wave block: it separates a wave field lying with the local wind from one running across it, which no single member reveals.
5. **Measurement completeness** — fraction of the 14 optional measurement members actually present, averaged over the window per station. The schema requires only `station_id`, `latitude`, `longitude` and `timestamp`; the one example record already omits `visibility` and `tide`, so partial reports are normal and silent channel loss is otherwise invisible.

The query also emits `reports` and `max_report_gap_seconds`. Those are diagnostics that make metrics 2 and 3 interpretable (a rate is meaningless without knowing the interval it was measured over) and are **not** claimed as part of the five.

## 2. The query

```sql
-- Azure Stream Analytics / Fabric Eventstream SQL. Single statement.
-- Event time member: timestamp. Source identity: station_id.
WITH
Observed AS (
    SELECT
        station_id,
        System.Timestamp()                  AS obs_time,   -- outside a window, this is the event time
        pressure,
        wave_height,
        wind_speed,
        gust,
        wind_direction,
        mean_wave_direction,
        -- previous report from the SAME station; LIMIT DURATION is mandatory on LAG
        LAG(pressure, 1)           OVER (PARTITION BY station_id LIMIT DURATION(hour, 3)) AS prev_pressure,
        LAG(wave_height, 1)        OVER (PARTITION BY station_id LIMIT DURATION(hour, 3)) AS prev_wave_height,
        -- I am not certain LAG accepts System.Timestamp() as its expression; if it does not,
        -- substitute LAG(CAST([timestamp] AS datetime), 1) OVER (...)
        LAG(System.Timestamp(), 1) OVER (PARTITION BY station_id LIMIT DURATION(hour, 3)) AS prev_obs_time,
        -- every member except station_id / latitude / longitude / timestamp is optional
        (CASE WHEN wind_direction       IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN wind_speed           IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN gust                 IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN wave_height          IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN dominant_wave_period IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN average_wave_period  IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN mean_wave_direction  IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN pressure             IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN air_temperature      IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN water_temperature    IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN dewpoint             IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN pressure_tendency    IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN visibility           IS NULL THEN 0 ELSE 1 END) +
        (CASE WHEN tide                 IS NULL THEN 0 ELSE 1 END)   AS members_present
    FROM input TIMESTAMP BY [timestamp]
),
PerReport AS (
    SELECT
        station_id,
        obs_time,
        members_present,
        DATEDIFF(second, prev_obs_time, obs_time) AS gap_seconds,

        -- (1) gust factor: dimensionless, guarded against a calm report
        CASE WHEN wind_speed > 0
             THEN gust / wind_speed
             ELSE NULL END AS gust_factor,

        -- (2) pressure change, normalised to declared-units-per-hour
        CASE WHEN DATEDIFF(second, prev_obs_time, obs_time) > 0
             THEN (pressure - prev_pressure) * 3600.0
                  / DATEDIFF(second, prev_obs_time, obs_time)
             ELSE NULL END AS pressure_rate_per_hour,

        -- (3) wave height change, normalised to declared-units-per-hour
        CASE WHEN DATEDIFF(second, prev_obs_time, obs_time) > 0
             THEN (wave_height - prev_wave_height) * 3600.0
                  / DATEDIFF(second, prev_obs_time, obs_time)
             ELSE NULL END AS wave_height_rate_per_hour,

        -- (4) circular difference folded into [0, 180]
        CASE WHEN ABS(wind_direction - mean_wave_direction) > 180
             THEN 360.0 - ABS(wind_direction - mean_wave_direction)
             ELSE ABS(wind_direction - mean_wave_direction) END AS wind_wave_misalignment_deg
    FROM Observed
)
SELECT
    station_id,
    System.Timestamp()                          AS window_end,   -- end of the tumbling window
    COUNT(*)                                    AS reports,      -- diagnostic
    MAX(gust_factor)                            AS gust_factor_max,              -- (1)
    AVG(gust_factor)                            AS gust_factor_avg,              -- (1)
    AVG(pressure_rate_per_hour)                 AS pressure_rate_per_hour,       -- (2)
    AVG(wave_height_rate_per_hour)              AS wave_height_rate_per_hour,    -- (3)
    AVG(wind_wave_misalignment_deg)             AS wind_wave_misalignment_deg,   -- (4)
    SUM(members_present) * 1.0 / (COUNT(*) * 14.0) AS measurement_completeness,  -- (5)
    MAX(gap_seconds)                            AS max_report_gap_seconds        -- diagnostic
INTO output
FROM PerReport
GROUP BY
    station_id,
    TumblingWindow(minute, 60)   -- tumbling, 60 minutes, one row per station per hour
```

Window summary: one **TumblingWindow of 60 minutes**, partitioned by `station_id`; the successive-difference metrics use `LAG` over a **3-hour LIMIT DURATION** partitioned by `station_id`.

## 3. What I did not compute

* **A residual of `pressure` change against `pressure_tendency`.** This is the one declared reference in the record and the obvious candidate, and I left it out. `pressure_tendency` has no declared averaging period, no declared unit, and no declared sign convention. Without the period I cannot difference it against an observed change over a known interval. The only unit-free version is a sign-agreement flag, and that is unsound too: pressure genuinely reverses direction, so at every turning point the observed short-interval change and a tendency computed over a longer period would legitimately disagree, and the flag would fire on correct data. A check that alarms on normal behaviour is worse than no check.
* **Wave steepness from `wave_height` and `dominant_wave_period`.** Relating a period to a wavelength requires the deep-water dispersion relation and consistent units for both members. The files establish neither. That is imported physics, not something these two files license.
* **The ratio `dominant_wave_period / average_wave_period`.** Arithmetically it is safe — both are periods and the ratio is dimensionless. I dropped it because the files do not say what distinguishes "dominant" from "average", so I could not state what the ratio means or which direction of departure from 1 is the one an operator should care about. A number I cannot interpret is not a metric.
* **Dewpoint depression, `air_temperature - dewpoint`.** The subtraction is sound if both share a scale, but its entire value rests on the relationship between dewpoint and saturation, which the files never state. I would be asserting meteorology the schema does not carry.
* **Air–sea temperature difference, `air_temperature - water_temperature`.** Ranked sixth. Sound under the same-scale assumption and I would add it if I had a sixth slot, but I judged the two rate metrics and the completeness metric more directly actionable, and the brief was five.
* **Arithmetic mean or `STDEV` of `wind_direction` or `mean_wave_direction` themselves.** These are circular quantities; the arithmetic mean of 350 and 10 is 180, which is the opposite of the right answer. Only the folded difference between them is averaged, and that is a magnitude in [0, 180], for which the arithmetic mean is valid.
* **`STDEV(wave_height)` within the window.** Sound, but largely redundant with metric 3, and with an undeclared reporting cadence the spread would mix genuine sea-state change with sampling density.
* **Anything using `latitude` and `longitude`** — drift from a home position, distance between stations, regional averages. There is no declared reference position to form a residual against, great-circle distance needs an earth model the files do not provide, and a single example record does not establish that more than one station exists or that a station's position is meant to be fixed.
* **Anything using `tide` or `visibility`.** `tide` is a level relative to a datum, and no datum is declared, so no residual or threshold is possible. Both are absent from the only example record. They are counted in the completeness metric and otherwise untouched.
* **Threshold flags in absolute units** — sea-state or wind-force classification, storm-pressure alarms. Every such threshold needs a unit, and no unit is declared for any member.

## 4. Assumptions

Each of the following is an **assumption**; none is established by the schema or the instance.

1. **Assumption:** `timestamp` is the observation time and is the correct event time. It is the only `datetime` member, which is why it is the one named in `TIMESTAMP BY`. I also assume its lexical form (`"2026-07-30T11:50:00Z"` in the instance) is parsed as an instant by the runtime.
2. **Assumption:** `station_id` identifies one physical source and is stable over time, making it a valid `PARTITION BY` key and a valid `LAG` partition.
3. **Assumption:** `gust` and `wind_speed` are expressed in the same unit, so their ratio is dimensionless. No unit is declared for either.
4. **Assumption:** `wind_direction` and `mean_wave_direction` are in degrees on [0, 360) and use the *same* reference convention — both "from" or both "toward". The schema declares them only as `double`. If the conventions differ, metric 4 is offset by 180° and the folded value is wrong.
5. **Assumption:** the rate metrics are in "declared-unit per hour". Since no unit is declared for `pressure` or `wave_height`, their magnitudes are comparable only to other reports from this same feed, not to any external scale.
6. **Assumption:** reports arrive more often than once per hour, so a 60-minute tumbling window contains several of them, and more often than once per 3 hours, so the `LAG` `LIMIT DURATION` reaches the previous report. The files contain exactly one record and establish no reporting cadence; both window sizes are guesses and should be re-tuned once the real interval is known.
7. **Assumption:** an absent member means the channel did not report, not that its value is zero. This drives metric 5 and the `IS NULL` guards. The schema makes all 14 measurement members optional and the instance omits `visibility` and `tide`, which is consistent with this reading but does not prove it.
8. **Assumption:** `gust >= wind_speed` is *not* guaranteed. The schema declares `$uses: ["JSONStructureValidation"]` but carries no validation keywords at all — no ranges, no units, no descriptions — so nothing constrains the values. A gust factor below 1 is therefore not treated as an error by the query.
9. **Assumption:** out-of-order and late arrivals are handled by the job's late-arrival policy, which is not part of the query and is not declared anywhere in the two files. `LAG` semantics depend on it.
10. **Assumption:** `AVG`, `MAX` and `SUM` ignore NULL inputs as in standard SQL, so partial reports reduce the sample size of a metric rather than poisoning it.


TRANSCRIPT D

# Five derived metrics over the BuoyObservation stream

## 1. The five metrics

1. **Sea-level pressure rate of change, in hPa per hour, per station.** The
   signed difference between `pressure` in this record and in the previous
   record from the same station, divided by the *measured* elapsed seconds
   between them and scaled to an hour. `pressure` is declared
   `phenomenonTimeRelation: instant`, so two readings from one station are two
   points on one curve and their difference is a rate. An operator wants the
   fastest fall in the hour: a deepening low is the single most consequential
   thing this feed can show, and the record's own `pressure_tendency` only
   resolves it over three hours.

2. **Gust factor, `gust / wind_speed`, per record, and its hourly maximum and
   mean.** Dimensionless: both members are `m/s`. The schema states that `gust`
   is "the greatest short-interval wind speed observed within the same averaging
   window that produced `wind_speed`" — so the ratio is a ratio of two summaries
   of *one* set of samples, and it remains sound even though the length of that
   window is not declared. An operator wants gustiness because a high ratio
   distinguishes a squall or a convective downdraught from a steady blow at the
   same mean speed, and because a ratio drifting toward 1.0 or toward absurdity
   points at the anemometer rather than the weather.

3. **Wave-height change between two non-overlapping 20-minute supports, per
   station.** `wave_height` carries `supportPeriod {length: PT20M, anchor: end}`,
   and `timestamp` carries `cadence {fixed, PT5M}`, so consecutive records
   describe periods that overlap by fifteen minutes. This metric compares the
   current record against the record whose support *closes twenty minutes
   earlier* — i.e. `[t-40m, t-20m)` against `[t-20m, t)` — and emits nothing
   when the elapsed time is not actually about twenty minutes. An operator wants
   the build or decay rate of the sea state, and this is the only wave
   difference in the feed that is a difference between disjoint periods.

4. **Dewpoint spread, `air_temperature - dewpoint`, and its hourly minimum.**
   Both are `CEL` and both are `phenomenonTimeRelation: instant`, so the
   subtraction is between like quantities at one instant. Its value is that the
   record carries no humidity member: the schema states `dewpoint` is computed
   from air temperature and relative humidity by a deterministic formula, so at
   a fixed `air_temperature` the spread varies only with the humidity channel,
   and the spread is the only way to see that channel at all. An operator
   watching for a closing spread is watching the one input the feed hides.

5. **Reporting completeness and worst gap against the declared cadence, per
   station.** `timestamp` declares `cadence {kind: fixed, period: PT5M}`, so a
   one-hour window expects twelve records; the metric reports the observed count
   as a percentage of that, plus the longest observed interval between
   successive `timestamp` values. An operator wants a station that has gone
   quiet to be visible as a gap rather than as a flat line, and wants to know
   the denominator before reading metrics 1–4 for that hour. Per
   {{cadence}} in the specification this is a decision the consumer makes about
   its own processing; it is reported, never enforced, and a shortfall does not
   make any record invalid.

## 2. The query

```sql
-- Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
-- Event time is `timestamp` (semanticRole: phenomenonTime). The source is
-- `station_id` (semanticRole: featureOfInterest); everything partitions by it.
-- `timestamp` is bracket-quoted throughout in case it collides with a
-- reserved word in this dialect.

WITH Observation AS
(
    SELECT
        station_id,
        [timestamp]                          AS phenomenon_time,
        pressure,
        wind_speed,
        gust,
        wave_height,
        air_temperature,
        dewpoint,

        -- Immediately preceding record from this station. The timestamp is
        -- carried so that elapsed time is measured, not assumed from cadence.
        LAG([timestamp], 1)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_time,
        LAG(pressure, 1)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_pressure,

        -- Fourth record back. At the declared PT5M cadence that record closes
        -- the 20-minute wave support immediately preceding the current one.
        -- Its timestamp is carried so the 20-minute assumption is *verified*
        -- below rather than trusted.
        LAG([timestamp], 4)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prior_support_time,
        LAG(wave_height, 4)
            OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prior_support_wave_height

    FROM input TIMESTAMP BY [timestamp]
),

PerRecord AS
(
    SELECT
        station_id,
        phenomenon_time,

        -- METRIC 5a: observed interval between successive phenomenon times.
        DATEDIFF(second, prev_time, phenomenon_time) AS gap_seconds,

        -- METRIC 1: signed pressure change normalised to hPa/hour by the
        -- measured elapsed time, so a missed beat lengthens the denominator
        -- instead of corrupting the rate. Intervals longer than one hour are
        -- discarded rather than extrapolated.
        CASE
            WHEN pressure IS NULL OR prev_pressure IS NULL THEN NULL
            WHEN DATEDIFF(second, prev_time, phenomenon_time) <= 0 THEN NULL
            WHEN DATEDIFF(second, prev_time, phenomenon_time) > 3600 THEN NULL
            ELSE (pressure - prev_pressure) * 3600.0
                 / DATEDIFF(second, prev_time, phenomenon_time)
        END AS pressure_rate_hpa_per_hour,

        -- METRIC 2: gust factor. Dimensionless; both members are m/s and the
        -- schema states they summarise the same averaging window.
        CASE
            WHEN gust IS NULL OR wind_speed IS NULL OR wind_speed <= 0 THEN NULL
            ELSE gust / wind_speed
        END AS gust_factor,

        -- METRIC 3: wave-height change across two NON-OVERLAPPING PT20M
        -- supports. Emitted only when the two anchoring positions really are
        -- about 20 minutes apart (1200 s, +/- 60 s), otherwise the two supports
        -- overlap or are disjoint by an unknown amount and the difference is
        -- not a 20-minute change.
        CASE
            WHEN wave_height IS NULL OR prior_support_wave_height IS NULL THEN NULL
            WHEN DATEDIFF(second, prior_support_time, phenomenon_time)
                 BETWEEN 1140 AND 1260
                 THEN wave_height - prior_support_wave_height
            ELSE NULL
        END AS wave_height_change_20min,

        -- METRIC 4: dewpoint spread, in degrees Celsius of DIFFERENCE.
        CASE
            WHEN air_temperature IS NULL OR dewpoint IS NULL THEN NULL
            ELSE air_temperature - dewpoint
        END AS dewpoint_spread
    FROM Observation
)

SELECT
    station_id,
    System.Timestamp() AS window_end,

    -- METRIC 1: most negative rate is the fastest fall; the absolute maximum
    -- catches a rapid rise behind a front as well.
    MIN(pressure_rate_hpa_per_hour)      AS min_pressure_rate_hpa_per_hour,
    MAX(ABS(pressure_rate_hpa_per_hour)) AS max_abs_pressure_rate_hpa_per_hour,

    -- METRIC 2
    MAX(gust_factor)                     AS max_gust_factor,
    AVG(gust_factor)                     AS avg_gust_factor,

    -- METRIC 3: order statistics only. See section 3 on why no mean is taken
    -- over the raw wave members.
    MAX(wave_height_change_20min)        AS max_wave_height_rise_20min,
    MIN(wave_height_change_20min)        AS max_wave_height_fall_20min,

    -- METRIC 4
    MIN(dewpoint_spread)                 AS min_dewpoint_spread,

    -- METRIC 5: 12 = one hour divided by the declared PT5M cadence. This is
    -- an expectation, not a guarantee; the value is reported, not asserted.
    COUNT(*)                             AS records_in_window,
    COUNT(*) * 100.0 / 12.0              AS reporting_completeness_pct,
    MAX(gap_seconds)                     AS max_gap_seconds

INTO output
FROM PerRecord
-- Window: TumblingWindow, 60 minutes, non-overlapping. Sixty is an integer
-- multiple of both the declared PT5M cadence and the PT20M wave support, so a
-- window holds a whole number of each.
GROUP BY station_id, TumblingWindow(minute, 60)
```

## 3. What I did not compute

* **Wave steepness, or any combination of `wave_height` with
  `dominant_wave_period` or `average_wave_period`.** Relating a height to a
  period requires the deep-water dispersion relation. Neither file states it,
  and the specification forbids repairing a missing fact from units,
  descriptions or property names.

* **Wind–wave misalignment, `wind_direction` minus `mean_wave_direction`.**
  `wind_direction` is explicitly "the direction the wind is coming from".
  `mean_wave_direction` states no from/toward convention at all. A convention
  mismatch is a 180-degree error and every value would still validate. Their
  supports differ as well: `mean_wave_direction` has `supportPeriod` PT20M and
  `wind_direction` has none.

* **Any window mean of `wind_direction` or `mean_wave_direction`.** Degrees
  wrap at 360 and an arithmetic mean of angles is wrong near north. Beyond
  that, `wind_direction` is already `derivation: statistic, statistic: mean`
  and `mean_wave_direction` is `derivation: calculated` from spectral
  directional moments; the specification states that `statistic` does not
  authorise recomputation and that a processor must not read an instruction out
  of these keywords. A vector mean would require the energy weighting the
  record does not carry.

* **A residual of `pressure_tendency` against a three-hour difference of
  `pressure`.** `pressure_tendency` declares `supportPeriod {PT3H, end}`, so
  the reference exists and the residual is exactly the shape the task calls
  valuable. Reconstructing the comparison term requires locating the record
  three hours back, which means either a fixed `LAG` offset of 36 or a trust in
  `cadence`. The specification is explicit that cadence is an expectation and
  not a constraint, that it does not assert a record exists for any position,
  and that a processor must not act as though it does. A fixed offset would
  silently compare the wrong interval on any hour that dropped a beat, and the
  error would be invisible in the output. Metric 1 measures its elapsed time
  instead of assuming it, which is why it is a short-interval rate rather than
  this residual.

* **Any mean, sum or standard deviation of `wave_height`,
  `dominant_wave_period`, `average_wave_period` or `mean_wave_direction` over a
  window.** Their `supportPeriod` is PT20M anchored at `end` and the cadence is
  PT5M, so consecutive records overlap by fifteen minutes. A windowed mean
  would weight the middle of the window roughly four times over, and a sum
  would count the same water four times. Only order statistics over published
  values and the disjoint-support comparison of metric 3 survive that overlap.

* **Cross-station aggregation of `wind_speed`, `gust` or `wind_direction`, and
  any treatment of them as a fixed-length average.** The schema declares no
  `supportPeriod` for these three and says so deliberately: the averaging
  length follows the station type, which the record does not carry. Per the
  specification the extent is then indeterminate and a nominal length must not
  be substituted. So an eight-minute mean from a buoy and a two-minute mean
  from a C-MAN station may not be pooled. The gust factor of metric 2 survives
  only because the ratio is taken within one record, where the schema states
  both members share one window.

* **Anything derived from `tide` or `visibility`.** Neither is in `required`
  and neither appears in the instance. `tide` is stated relative to Mean Lower
  Low Water, a station-specific datum, and no vertical
  `coordinateReferenceSystem` binds it — the schema's only CRS annotation binds
  `latitude` and `longitude` to EPSG:4326. Differencing tide across stations is
  therefore unsound, and the specification is clear that a datum stated in
  prose is not a binding a processor may act on. `visibility` is stated to be
  generally available only on C-MAN stations, which the record cannot identify.

* **Publication latency or feed freshness against arrival.** The schema
  declares `phenomenonTime` and nothing else temporal: there is no `resultTime`
  and no `ingestionTime`, and the specification forbids reading an operational
  time out of a phenomenon time. Metric 5 measures the interval between
  successive phenomenon times, which is a different quantity and is not a
  delivery-delay metric.

* **Anything from `latitude` and `longitude`** — drift of a moored buoy,
  station separation, spatial clustering. The CRS binding is present and
  unambiguous (EPSG:4326, `["latitude","longitude"]`, authoritative axis
  order), but neither file establishes whether the position is fixed per
  station or updated per record, and the specification explicitly declines to
  define coordinate operations or transformations, so a distance computation
  would rest on an ellipsoid model neither file supplies.

* **Air–sea temperature difference, `water_temperature - air_temperature`.**
  This one is sound — same unit `CEL`, both `derivation: measured`, both
  `phenomenonTimeRelation: instant`, same station and same phenomenon time —
  and I ranked it sixth and dropped it to keep to five. I note it here rather
  than in section 1 because the two files establish nothing about what the
  difference *means*, so its operator value is confined to cross-checking two
  independent sensors.

* **Any threshold flag, quality gate or "good data" indicator.** The schema
  carries no member with `semanticRole: resultQuality` and none with
  `semanticRole: status`, and it declares no `enum`, minimum or maximum on any
  numeric member. The specification states that omission never implies
  acceptable quality. I therefore raise no flag anywhere, including the
  otherwise obvious one on a negative dewpoint spread: that dewpoint cannot
  exceed air temperature is a fact about the atmosphere, not a fact these two
  files state.

## 4. Assumptions

* **Assumption.** `timestamp` is the correct event time for windowing. The
  schema gives it `semanticRole: phenomenonTime` and the record carries no
  other temporal member, so this follows; what does not follow, and is assumed,
  is that phenomenon time is an acceptable proxy for arrival ordering. Late and
  duplicate arrivals are left to the job's late-arrival and out-of-order
  policy, which is configuration and not part of this query.

* **Assumption.** `station_id` identifies one physical platform, that
  identifiers are not reused across platforms, and that one station emits at
  most one record per five-minute slot. The schema says the identifier is
  assigned by NDBC and identifies the observing platform; uniqueness over time
  and non-duplication in the stream are not stated.

* **Assumption (dialect).** `LAG` accepts an offset argument greater than 1 in
  this dialect. If it does not, metric 3 must be rewritten — the offset of 4 is
  load-bearing there. I could not verify this, as instructed.

* **Assumption (dialect).** `timestamp` needs bracket-quoting to avoid a
  reserved-word collision, and `ABS` is available. Neither is established by
  the files.

* **Assumption.** The ±60-second tolerance on metric 3's twenty-minute
  comparison is my choice. The files establish the PT20M support and the PT5M
  cadence but no tolerance for jitter; `timestamp` is stated to be constructed
  from minute-resolution columns, which is what makes a one-minute band
  plausible rather than principled.

* **Assumption.** The one-hour discard threshold in metric 1, and the
  suppression of the metric across gaps longer than that, are my choices. The
  files state no interval beyond which two `pressure` readings stop being
  usefully comparable.

* **Assumption.** The denominator 12 in `reporting_completeness_pct` treats the
  declared `cadence` of PT5M as the expected delivery rate for a full hour. The
  specification states this is an expectation and not a constraint; the query
  reports the ratio and draws no conclusion from it.

* **Assumption.** `dewpoint_spread` and the wave-height change are differences,
  not values on the underlying scale. A difference of two `CEL` values is a
  temperature interval and a difference of two `m` wave heights is a length
  change; the output column names say so but no unit annotation travels with
  them, and a downstream consumer that treats
  `min_dewpoint_spread` as a temperature will be wrong.

* **Assumption.** Successive `pressure` values from one station are comparable
  to each other. The schema states the value is reduced to sea level by the
  standard atmosphere from the station elevation, and I assume that elevation
  is constant for a given station over the window, so the reduction is a fixed
  transform and cancels in the difference. Nothing in the two files states that
  station elevation is fixed.

* **Assumption.** Every member other than `station_id`, `latitude`,
  `longitude` and `timestamp` may be absent from any record, since `required`
  lists only those four. Every metric is guarded for NULL on that basis, and
  each aggregate is therefore computed over an unstated and varying number of
  contributing records. The output does not report those per-metric counts.
