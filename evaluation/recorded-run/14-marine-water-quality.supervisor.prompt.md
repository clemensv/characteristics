You are a supervisor. You grade four transcripts against a fixed list of claims.

You are not being asked whether a transcript is good, insightful, or well
written. You are asked, for each claim and each transcript, whether the
transcript got that specific matter right, got it wrong, declined to decide it,
or never touched it. Nothing else you think about the transcripts is wanted.

## Your stance

You are an adversarial grader. The transcripts were written by a different model
from a different vendor, and you are the hostile check on them. Assume each is
trying to appear more knowledgeable than it is, and grade so that appearance
earns nothing.

Credit is earned, never assumed. The default verdict is `unaddressed`, and a
transcript moves off it only by saying something specific enough that you can
point at the words. You are not rewarded for being fair to a transcript, and a
grader who credits an answer with something it did not quite say has failed at
this task. Being wrong in the direction of severity costs the evaluation far
less than being wrong in the direction of generosity, so where you genuinely
cannot decide, withhold the credit.

This severity applies identically to all four transcripts. You are hostile to
unearned credit, not to any particular transcript, and you must not go looking
for a transcript to punish.

You will be given:

* **CLAIMS** — numbered propositions. Each is true of the data the transcripts
  describe. Most carry a `wrong reading`: the specific error the claim exists to
  rule out.
* **TRANSCRIPT A**, **TRANSCRIPT B**, **TRANSCRIPT C** and **TRANSCRIPT D** —
  four independent readings of that data, produced under conditions you are not
  told. They are not in any meaningful order. Do not speculate about the
  conditions while grading.

For each claim, and separately for each of the four transcripts, choose exactly
one verdict. Every claim therefore receives four verdicts.

* `correct` — the transcript asserts the claim, or asserts something that
  entails it, as a statement it is standing behind.
* `incorrect` — the transcript asserts the wrong reading, or asserts anything
  else incompatible with the claim.
* `declined` — the transcript raises the matter and explicitly does not settle
  it: it says the files do not determine it, or it marks its answer as an
  assumption or a guess. **A transcript that states the correct answer but marks
  it as a guess or an assumption is `declined`, not `correct`.** Knowing that you
  do not know is a distinct outcome from knowing.
* `unaddressed` — the transcript never engages the matter at all.

Rules you must follow.

1. Judge only what is written. Do not credit a transcript for something you
   believe it meant, or for something a competent reader would obviously know.
2. For `correct` and `incorrect` you MUST supply `quote`: a verbatim span from
   that transcript, copied exactly, that carries the verdict. If you cannot find
   one, the verdict is `unaddressed`.
3. **The quote must carry the claim standing alone.** Read it with the rest of
   the transcript covered up. If someone who saw only those words would not
   learn the claim from them, the verdict is not `correct`, however clearly the
   surrounding paragraphs gesture at it. Naming the member, using the right
   technical term, or discussing the general area is not asserting the
   proposition.
4. **Look for the wrong reading before you look for the right one.** Search the
   transcript for the error the claim exists to rule out, and settle that
   question first. Only if the wrong reading is absent may you consider
   `correct`.
5. **A transcript that both asserts the claim and commits the wrong reading is
   `incorrect`.** Do not let a correct sentence elsewhere rescue it. Reciting a
   rule and then breaking it is worse than not knowing the rule, not better.
6. Do not round up. If a transcript gets part of a claim right and part of it
   wrong, and the wrong part is what the claim is about, that is `incorrect`. If
   the wrong part is incidental, it is `unaddressed`. It is not `correct`.
7. Do not use your own knowledge of the subject matter to decide a claim. The
   claim is the ground truth. If a transcript contradicts a claim, that is
   `incorrect` even if you personally believe the transcript.
8. Confidence is not evidence. Length is not evidence. A fluent, assured,
   well-organised transcript gets no benefit of the doubt over a terse one.
9. Grade the four transcripts independently. Do not let one inform another, and
   do not compare them. A matter that transcript C settles is still
   `unaddressed` in transcript A if transcript A never raises it.
10. Silence is not an error. A transcript that never touches a claim is
    `unaddressed`, and `unaddressed` is not a mark against it. Severity means
    withholding credit, not inventing violations.

Answer with JSON only, no prose before or after, in exactly this form:

```json
{
  "verdicts": [
    {"claim": 1, "transcript": "A", "verdict": "correct", "quote": "..."},
    {"claim": 1, "transcript": "B", "verdict": "unaddressed"},
    {"claim": 1, "transcript": "C", "verdict": "declined"},
    {"claim": 1, "transcript": "D", "verdict": "incorrect", "quote": "..."}
  ],
  "blinding": {"richest": "A" | "B" | "C" | "D" | "cannot tell", "why": "one sentence"}
}
```

The `blinding` field is not part of the grading and is not scored. It records
which transcript appeared to have had the most material available to it, and
whether you could tell at all. Answer it last, answer it honestly, and say
`cannot tell` if you cannot tell.


---

CLAIMS

1. `sampled_depth_m` is expressed in `m`.
   wrong reading: Assuming a different or conventional unit for `sampled_depth_m`.

2. `observation_time` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `observation_time` as the time the record was produced, received, or published, or using a different member for event time.

3. Successive `observation_time` values are expected at cadence `fixed` with period "PT15M". A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

4. `published_time` is an operational instant (`resultTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `published_time` as the event time of the observation.

5. `qc_flag` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `qc_flag` as an observed quantity.

6. `water_temperature_c` is expressed in `Cel`.
   wrong reading: Assuming a different or conventional unit for `water_temperature_c`.

7. `conductivity_s_m` is expressed in `S/m`.
   wrong reading: Assuming a different or conventional unit for `conductivity_s_m`.

8. `specific_conductivity_s_m` is calculated rather than measured directly.
   wrong reading: Treating `specific_conductivity_s_m` as a direct measurement.

9. `specific_conductivity_s_m` is expressed in `S/m`.
   wrong reading: Assuming a different or conventional unit for `specific_conductivity_s_m`.

10. `pressure_dbar` is expressed in `dbar`.
   wrong reading: Assuming a different or conventional unit for `pressure_dbar`.

11. `salinity_psu` is calculated rather than measured directly.
   wrong reading: Treating `salinity_psu` as a direct measurement.

12. `salinity_psu` is expressed in `PSU`.
   wrong reading: Assuming a different or conventional unit for `salinity_psu`.

13. `dissolved_oxygen_mg_l` is expressed in `mg/L`.
   wrong reading: Assuming a different or conventional unit for `dissolved_oxygen_mg_l`.

14. `dissolved_oxygen_saturation_pct` is calculated rather than measured directly.
   wrong reading: Treating `dissolved_oxygen_saturation_pct` as a direct measurement.

15. `dissolved_oxygen_saturation_pct` is expressed in `P1`.
   wrong reading: Assuming a different or conventional unit for `dissolved_oxygen_saturation_pct`.

16. `chlorophyll_ug_l` is expressed in `ug/L`.
   wrong reading: Assuming a different or conventional unit for `chlorophyll_ug_l`.

17. `chlorophyll_stddev_ug_l` is already a `standardDeviation` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `chlorophyll_stddev_ug_l` as though it were a raw sample.

18. `chlorophyll_stddev_ug_l` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `chlorophyll_stddev_ug_l` as an instantaneous reading.

19. `chlorophyll_stddev_ug_l` is expressed in `ug/L`.
   wrong reading: Assuming a different or conventional unit for `chlorophyll_stddev_ug_l`.

20. `turbidity_ntu` is expressed in `NTU`.
   wrong reading: Assuming a different or conventional unit for `turbidity_ntu`.

21. `turbidity_stddev_ntu` is already a `standardDeviation` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `turbidity_stddev_ntu` as though it were a raw sample.

22. `turbidity_stddev_ntu` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `turbidity_stddev_ntu` as an instantaneous reading.

23. `turbidity_stddev_ntu` is expressed in `NTU`.
   wrong reading: Assuming a different or conventional unit for `turbidity_stddev_ntu`.

24. `nitrate_umol` is expressed in `umol`.
   wrong reading: Assuming a different or conventional unit for `nitrate_umol`.


TRANSCRIPT A

# 1. What this feed is

Each record is one sampling cycle from a fixed marine monitoring mooring operated by King County, Washington, in Puget Sound. The mooring runs a CTD/optical/nutrient sonde package on a nominal fifteen-minute cycle, and each record carries the state of one water parcel at one depth at one instant: temperature, conductivity and salinity, pressure, dissolved oxygen, pH, chlorophyll, turbidity and nitrate, together with an automated QARTOD quality classification.

The critical structural fact — and the thing most consumers get wrong — is that a record names **three different entities, and they are not substitutes for one another**:

- the **mooring** (`station_id`), which is the programme's reporting unit;
- the **water parcel** at `sampled_depth_m`, which is what was actually measured;
- the **basin** (`basin`), which is the water body the result is interpreted *for*.

The measured values are properties of the parcel, not of the mooring and not of the basin. Attributing a reading to "the station" or "the basin" as though it were a property of either is a category error that the schema explicitly warns against, and `basin` must be read from the record, never inferred from the station.

A fourth identity carries equal weight: `sonde` is the measurement procedure. The schema states plainly that readings taken with a different package are not interchangeable even when the property and the station agree. The joining key for any comparative work is therefore the tuple **(station_id, sampled_depth_m, sonde)** — not `station_id` alone.

Finally, only the identity, time and QC members are required. Every measurement channel is optional. A conforming record may carry no measurements at all.

# 2. Analytics

**Continuous time-series characterisation at a fixed station/depth/sonde.** The regular fifteen-minute cadence and a single, explicit phenomenon-time axis support diel cycles, seasonal cycles, trend estimation, and spectral or harmonic decomposition. Fifteen-minute sampling puts the Nyquist limit at a thirty-minute period, which comfortably resolves the diel and semidiurnal tidal bands but aliases anything faster.

**Hypoxia and threshold-exceedance analysis.** Dissolved oxygen is present both as concentration and as percent saturation, on a regular grid, with an unambiguous instant attached. Exceedance frequency, onset and recovery timing, and event duration are all computable because the time axis is phenomenon time and the sampling interval is known.

**Bloom detection and nutrient drawdown.** Chlorophyll, nitrate, pH and oxygen saturation are all reported for the *same* water parcel at the *same* instant. That co-location is what makes the classic bloom signature — chlorophyll rise with nitrate drawdown, elevated pH and oxygen supersaturation — checkable within a single record rather than by risky cross-source alignment.

**Water-mass identification and stratification.** Temperature and salinity, with pressure and depth, support T–S characterisation. Stratification analysis specifically requires multiple depths; whether this feed delivers them is not determined (see §5).

**Internal-consistency auditing.** The schema names the derivation relations: salinity from conductivity/temperature/pressure, specific conductivity from conductivity normalised to 25 °C, oxygen saturation from concentration with concurrent temperature, salinity and pressure. Each can be recomputed and compared to the published value. Disagreement indicates a processing or calibration fault, not an environmental signal. This is one of the highest-value analyses available and requires no external data.

**Operational and data-quality analytics.** `published_time` minus `observation_time` gives per-record latency (23m41s in the example). Completeness is measurable against the expected quarter-hour grid. QC-flag rates, flag transitions, and sonde changeovers are all trackable, and sonde changeovers are worth detecting as *series break points*, since the schema declares readings across packages non-interchangeable.

**Burst-variability screening.** The two standard-deviation channels indicate within-cycle variability — patchiness or optical noise. Because burst length is not published, they are usable ordinally (this cycle was noisier than that one, same sonde) and not as calibrated dispersion.

**Turbidity event detection.** Storm, runoff and resuspension events are detectable, but NTU is a method-and-instrument-defined unit, so magnitude comparisons across different sondes are not supportable.

# 3. Combination rules

**Precondition governing everything below.** No two values may be compared, differenced or averaged unless `station_id`, `sampled_depth_m` and `sonde` match (or depths are binned deliberately and the binning is stated), and unless the `qc_flag` values are acceptable for the purpose. A `sonde` change invalidates the series continuity by the schema's own statement.

**Nothing in this feed may be summed.** Every measured quantity here is intensive — a concentration, a temperature, an index, a pressure, a depth. Adding two concentrations or two temperatures across records produces a number with no referent. Volumetric integration (e.g. oxygen inventory in a basin) would need water volumes, which the feed does not carry.

- **`station_id`, `station_name`, `basin`, `sonde`** — identity only. Equality tests and grouping keys. Never arithmetic. `basin` must not be derived from `station_id`; the schema says the ultimate feature of interest is stated, not inferred.
- **`sampled_depth_m`** — a coordinate, not an observed property. Differences are meaningful as vertical separation. Averaging describes where a group of samples sat, never a property of the water. Not summable.
- **`observation_time`** — differenceable (elapsed duration). Averaging is admissible only as the centroid of a window.
- **`published_time`** — combinable only by differencing against `observation_time` to obtain latency. Never a time axis, never a binning key.
- **`qc_flag`** — categorical. Countable, rate-computable. Never averaged, never numerically encoded and treated as a scale.
- **`water_temperature_c`** — interval scale. Differences and arithmetic means are valid within a matched group. Ratios are meaningless in Celsius: 13.8 °C is not "twice" 6.9 °C. Not summable.
- **`conductivity_s_m`** — ratio scale but temperature-confounded. It may be compared or differenced only among records at effectively equal water temperature. Across differing temperatures, use specific conductivity instead; otherwise a temperature change reads as a conductivity change.
- **`specific_conductivity_s_m`** — normalised to 25 °C, therefore comparable, differenceable and averageable across records of differing in-situ temperature within a matched group. **It must never be pooled with, differenced against, or substituted for raw conductivity.** In the example these read 4.0186 and 3.1274; the gap is a calculation artefact of the normalisation, not a physical difference, and mixing the two channels manufactures a step change out of nothing.
- **`pressure_dbar`** — ratio scale; differences valid; not summable. Whether it is absolute or surface-referenced is not determined (§5), so cross-source differencing is unsafe.
- **`salinity_psu`** — comparable, differenceable, averageable within a matched group. Not summable. **Not statistically independent** of conductivity, temperature and pressure: it is computed from them. Using salinity alongside conductivity and temperature as separate predictors in a regression, correlation matrix or PCA produces definitional, not physical, structure.
- **`dissolved_oxygen_mg_l`** — concentration; compare, difference and average within a matched group. Never sum.
- **`dissolved_oxygen_saturation_pct`** — a normalised index derived from concentration plus concurrent temperature, salinity and pressure. Comparable and averageable, but a difference between two saturation values taken under very different temperature and salinity corresponds to a different absolute oxygen difference, so do not read saturation deltas as oxygen deltas. Never sum. **Do not model it jointly with `dissolved_oxygen_mg_l`, temperature and salinity** — it is a deterministic function of them.
- **`ph`** — a logarithmic activity scale (general chemistry, not stated in the files). An arithmetic mean of pH is the mean of a logarithm, not the pH of the mean acidity; if a chemical mean is wanted, average hydrogen-ion activity and convert back, and label whichever you report. Differences are valid and express log-ratios. Never sum. The total scale is fixed for this feed, so cross-record scale mixing is not a hazard here, but comparison against external NBS- or free-scale data is invalid without conversion.
- **`chlorophyll_ug_l`** — concentration; compare, difference, average within a matched group. Never sum. Cross-sonde *absolute* comparison is unsafe both by the schema's procedure rule and because the channel may be raw fluorescence in equivalent units (§5). Relative and temporal use at a fixed station and sonde is sound.
- **`turbidity_ntu`** — same treatment. NTU is defined by the instrument and method, so cross-sonde magnitudes are not interchangeable; use ranks or within-series anomalies instead.
- **`nitrate_umol`** — if it is a concentration, treat as the other concentrations: compare, difference, average within a matched group, never sum. The analyte is stated as nitrate *or* nitrate-plus-nitrite, so records from different deployments may not carry the same analyte, and differencing against an external nitrate-only series is not supportable.
- **`chlorophyll_stddev_ug_l` and `turbidity_stddev_ntu`** — **must not be compared or differenced against their concentration counterparts.** They carry the same observable property but a different summary function; the schema says so explicitly, and treating 0.62 µg/L as a chlorophyll level rather than a dispersion is a straightforward error. They also **must not be averaged across records**: pooling dispersion requires variance-space arithmetic weighted by burst sample counts, and neither burst length nor sample count is published. They are usable ordinally within an identical deployment configuration, and the record does not tell you when that configuration changed.

# 4. Time

**`observation_time` is the time axis of the thing described.** It is phenomenon time — the instant at which the stated conditions applied to the sampled water parcel. All plotting, binning, resampling, event timing, lag and cross-correlation work must use this member and only this member. It is also the only correct chronological ordering; records may well arrive out of this order.

**`published_time` is a system availability axis, not a time axis for the data.** It is when the shore-side system released the reading after telemetry and automated QC, minutes to hours later. Its legitimate uses are latency measurement, arrival ordering and revision detection. Binning environmental values by publication time — a common default in stream-processing tools — misassigns readings to the wrong hour and, near a bloom or hypoxia onset, to the wrong event.

**Relation to civil time.** Both stamps are UTC in ISO 8601 form. Positions on the axis are therefore absolute instants: differences are true elapsed durations, with no daylight-saving discontinuities and no ambiguous or non-existent local times. This makes UTC the correct basis for duration, rate and spectral computation.

Local civil time is a separate matter. King County, Washington observes UTC−8 in winter and UTC−7 under daylight saving (general knowledge; the files state the location but not the zone). Anything indexed to the sun or to the working day — diel cycles, daylight-driven photosynthesis, day boundaries, tide-of-day patterns — must be converted to local civil or local solar time first. The example instant, 2026-07-27T19:15:00Z, is 12:15 in local daylight time: solar midday, not evening. Binning by UTC hour smears the diel cycle by one hour across each DST transition, and a "daily mean" computed on UTC day boundaries is not a local day.

**Cadence and grid.** One record per station per quarter-hour slot is expected. The example lands exactly on :15:00, which suggests the stamp is a scheduled slot label rather than the precise sensor trigger; that is a guess, but it means equality joins on `observation_time` across stations will probably work while sub-second accuracy should not be assumed. The expected grid also makes gaps detectable: absence of a record is informative, not merely missing.

**Support versus instant — the trap.** `observation_time` is an instant, but the two standard-deviation channels characterise a *burst* somewhere inside the sampling cycle whose length is configured per deployment and deliberately not published; the schema notes that no support period is declared and the extent is therefore indeterminate from the record. So the single point on the time axis under-describes the temporal support of those values. You cannot say what interval a standard deviation covers, and consequently you cannot correctly resample, aggregate or align it with anything.

# 5. Ambiguities

**Declining to decide** (the files do not determine these; do not resolve them by assumption):

1. **The unit of `nitrate_umol`.** "Micromoles" is an amount of substance, not a concentration. Whether the denominator is a litre, a kilogram of seawater, or something else is not stated, so absolute values cannot be safely compared to any external nutrient dataset.
2. **The nitrate analyte.** "Nitrate or nitrate-plus-nitrite" is two different analytes. Which one applies, and whether it is constant across deployments, is not determined.
3. **What `chlorophyll_ug_l` is.** "Chlorophyll fluorescence or chlorophyll concentration" leaves open whether this is a calibrated concentration or raw fluorescence expressed in equivalent units. This decides whether absolute cross-station comparison is meaningful.
4. **The temporal support of `chlorophyll_ug_l` and `turbidity_ntu`.** Whether these are burst means paired with their standard deviations, or single instantaneous reads, is not stated. If they are burst means, their support is the burst, not the instant, and the same indeterminacy that afflicts the standard deviations afflicts them.
5. **Burst length and burst sample count.** Explicitly not published. This is what forecloses correct pooling of the dispersion channels.
6. **The scope of `qc_flag`.** One flag covers the whole record. Which channel a `suspect` or `fail` condemns is not determined; a record may have sound temperature and unusable nitrate with no way to tell. Filtering the whole record is the conservative choice and discards good data; filtering nothing keeps bad data. The files do not decide this.
7. **Revision semantics.** There is no version, revision or supersession member. Whether a reading can be republished with a corrected value and a later `published_time` — and hence what the deduplication rule on (station_id, observation_time) should be — is undecided.
8. **Whether `sampled_depth_m` is fixed or varying.** The package is described as *profiling*, which suggests depth may vary per cycle, but the member is optional and no cast, profile or sequence identifier exists. Whether multiple depths can share a quarter-hour slot is likewise undetermined. A record carrying measurements but no depth leaves its proximate feature of interest unidentified, and such records cannot be pooled with anything.
9. **The meaning of an absent channel.** Not measured, removed by QC, or sensor not fitted — not determined. It must not be imputed as zero, and the distinction between an absent member and a `qc_flag` of `missing` is not explained.
10. **Depth reference under tide.** Depth is stated as below the sea surface, but the surface moves. Whether the sonde maintains constant depth below a moving surface or sits at fixed elevation above the bed is not determined, and the two describe different water parcels over a tidal cycle.
11. **pH reporting temperature.** The total scale is specified, but pH is temperature-dependent and the files do not say whether the value is at in-situ temperature or at a reference temperature.
12. **Station position.** No coordinates. Distance weighting, mapping, spatial interpolation and any advection or plume analysis are impossible from this feed alone.
13. **Measurement uncertainty.** No uncertainty, accuracy or detection-limit member exists anywhere, and `additionalProperties` is false with no extension point, so none can appear without a schema change. Error bars, significance tests and change-detection thresholds cannot be grounded in the data.
14. **Vocabulary control on `basin`.** "Puget Sound - Main Basin" is a free string. Grouping on it is a string match and is fragile to punctuation or naming drift.
15. **Calibration epochs.** Whether the `sonde` URI changes on recalibration or only on package substitution is not stated, so a stable URI does not guarantee an unbroken calibration history.

**Guesses**, marked as such:

- **Guess:** `nitrate_umol` is µmol/L, the conventional reporting unit for this measurement. Do not build on it without confirmation.
- **Guess:** `qc_flag` is record-level rather than per-channel, given there is one flag and many channels.
- **Guess:** `pressure_dbar` is surface-referenced rather than absolute. At 1.0 m depth the value is 1.04 dbar, roughly the water column alone; an absolute reading would include roughly ten decibars of atmosphere.
- **Guess:** `sampled_depth_m` is a nominal or rounded value (1.0 against 1.04 dbar) rather than an independently measured one, and may simply be derived from pressure.
- **Guess:** `observation_time` is a scheduled slot label aligned to :00/:15/:30/:45 rather than the exact sensor trigger instant.
- **Guess (general knowledge, not from the files):** the enum values map to the standard QARTOD codes — pass, not evaluated, suspect, fail, missing. `not_evaluated` is not an endorsement of quality and must not be pooled with `pass`.


TRANSCRIPT B

# 1. What this feed is

Each record is one sampling cycle of a fixed marine monitoring mooring operated by
King County, Washington, in Puget Sound. A cycle produces a bundle of CTD, optical
and nutrient channels — temperature, conductivity and its 25 °C-normalised
counterpart, pressure, salinity, dissolved oxygen as concentration and as
saturation, pH, chlorophyll, turbidity, and nitrate — plus two within-cycle
variability figures for the optical channels.

The record separates three subjects that a consumer will otherwise conflate. The
mooring is the programme-level feature the results are reported against. The water
parcel at the stated depth is the thing actually measured. The basin is the water
body the result is ultimately interpreted for. None of the three is derivable from
either of the others, and the schema says so; a query that groups by station and
calls the answer a basin figure, or that treats two stations in one basin as
observations of the same parcel, is combining different subjects.

One further identity carries the same weight: the sonde package URI is the
measurement procedure. Two readings of the same property at the same station and
depth are not interchangeable if they came from different packages.

# 2. Analytics

**Time series at a station and depth.** Every scalar channel is a point value
stamped with the instant it applied, at a declared quarter-hourly rhythm. That
supports trend, diel cycle, seasonal cycle, and threshold-crossing work at a
single station — provided the series is cut by depth and by sonde, not just by
station.

**Publication latency.** The record carries the instant the conditions applied and
the instant the shore system published, as two separate, distinctly-typed roles.
Their difference is a clean, per-record measure of telemetry-plus-QC delay (23 m
41 s in the example), and its distribution by station, by sonde and by quality
class is directly computable. Nothing else in the feed measures pipeline health.

**Quality-conditioned availability.** The QARTOD class is enumerated with its
codes' meanings attached, including one class that means "must not be used" and
one that means "never tested". Counting records by class per station per period
gives instrument-health and QC-coverage statistics, and is the necessary
precondition for every other analysis here.

**Within-cycle variability.** The two standard deviations are the only evidence in
the feed about behaviour *between* the quarter-hourly stamps. High chlorophyll or
turbidity variance within a burst is a usable signal of patchiness, resuspension,
bubbles or biofouling, and it is usable *relative to itself over time at one
deployment*. It is not usable as a variance in the statistical sense across
records, because the burst length is not published.

**Internal-consistency checking.** Three channels are declared calculated rather
than measured: specific conductivity from conductivity and temperature, salinity
from conductivity, temperature and pressure, and oxygen saturation from oxygen
concentration and the concurrent temperature, salinity and pressure. Recomputing
each from its stated inputs is a real QC test — a divergence indicates a
processing fault. What it is *not* is corroboration: agreement between salinity
and conductivity, or between oxygen concentration and oxygen saturation, is
arithmetic, not two independent instruments agreeing.

**Basin-level roll-up.** The programme's own interpretation target is the basin,
and each record declares its basin explicitly, so aggregation to basin is the
intended use. But the feed supplies no coordinates, no basin geometry and no
station weights, so any basin figure is an unweighted mean of whichever moorings
reported, and its representativeness is the consumer's assumption.

**What the feed cannot support.** Spatial interpolation or mapping of any kind:
there are no coordinates in the record. Stratification profiles: one depth per
record, and no guarantee that a station reports more than one. Flux or load
calculations: no discharge, no volume, and nothing here is an accumulated
quantity.

# 3. Combination rules

**The grouping key for any cross-record combination is station, sonde, depth, and
quality class.** Station identifies the feature; sonde identifies the procedure and
is comparability-critical; depth identifies the water parcel actually measured, and
a different depth is a different parcel, not a different reading of the same one.
Values whose quality class is `fail` must be excluded outright, and `not_evaluated`
must not be pooled with `pass` as though it were equivalent, since it asserts only
that nothing was checked.

With that key held fixed:

| Quantity | Compare | Difference | Sum | Average |
|---|---|---|---|---|
| water temperature | yes | yes | no | yes |
| conductivity (in situ) | yes | yes | no | yes |
| specific conductivity (25 °C) | yes | yes | no | yes |
| pressure | yes | yes | no | yes |
| salinity | yes | yes | no | yes |
| dissolved oxygen, mg/L | yes | yes | no | yes |
| dissolved oxygen, % saturation | yes | yes | no | yes |
| pH | yes | as a log ratio | no | not as a plain mean |
| chlorophyll | yes | yes | no | yes |
| turbidity | yes | yes | no | yes |
| nitrate | yes | yes | no | unit ambiguity first — see §5 |
| chlorophyll std. deviation | trend only | no | no | no |
| turbidity std. deviation | trend only | no | no | no |

Nothing in this feed may be summed. Every scalar channel is an intensive state
variable observed at an instant; none is an accumulation over a period, and a total
of temperatures, salinities or oxygen concentrations is not a quantity.

**Averages are averages of samples, not of time.** Every scalar channel is declared
to apply *at* the observation instant, not to hold until the next reading. A
consumer computing "mean daily oxygen" or "hours below a threshold" by treating
each value as valid for its fifteen-minute slot is asserting a step-function
semantics the feed explicitly does not declare. The declared cadence does not
license filling a gap either: an absent slot is absent, and an unweighted mean over
present records is biased toward whatever times the mooring was reporting.

**Pairs that must not be combined:**

- *Chlorophyll and its standard deviation; turbidity and its standard deviation.*
  Each pair shares a unit and the same observable-property reference and differs
  only in the summary function applied. They are not like quantities. They must not
  be differenced, ratioed as if commensurate, or fed into one series.
- *The two standard deviations across records.* The burst they summarise lies
  inside the cycle but its length is set per deployment and is not published, so
  the extent of the period each value characterises is indeterminate. Two such
  values may not be pooled, weighted, or combined into a longer-window variance,
  because the number of underlying samples is unknown. Watching one deployment's
  series rise or fall is legitimate; arithmetic across deployments is not.
- *Conductivity and specific conductivity.* They carry the same observable-property
  reference and the same unit, so a naive join will treat them as one quantity.
  They are referenced to different temperatures — in situ versus 25 °C — and are
  therefore different quantities. Do not difference them, do not substitute one for
  the other when the other is absent, and do not concatenate them into one series.
- *Anything across differing sonde values.* Turbidity in NTU and chlorophyll from a
  fluorometer are the clearest cases: both are instrument-defined optical scales,
  and equality of the declared property does not make two packages' numbers
  interchangeable. Even where the sonde URI is equal, that is grounds for grouping,
  not proof of statistical interchangeability across a recalibration.
- *Anything across differing depth, or with depth absent.* Depth is optional in
  this schema. A record without it cannot be placed in a depth-conditioned series
  at all, and must not be assumed to sit at the station's usual depth.

**pH** is a logarithmic quantity. Its differences are meaningful as log ratios of
activity; an arithmetic mean of pH is not the pH of the mean hydrogen ion activity.
That is chemistry rather than something the two files establish, so I mark it as
general knowledge, but the files give no unit and no basis for treating pH as an
ordinary linear scale either.

**Oxygen concentration and oxygen saturation** are not independent. Do not treat
their agreement as a cross-check, and do not build a model that regresses one on
the other; the second was computed from the first.

# 4. Time

The time axis of the phenomenon is the observation timestamp. It is the instant at
which the stated conditions applied to the sampled water parcel, and it is the only
member that places the *thing described* on a time line.

It is a Core datetime with no temporal reference system declared, which means it is
read under ordinary civil-calendar semantics; the description states it is
normalised to UTC and the example carries a `Z` offset. Positions on this axis are
therefore directly civil-time instants requiring no transformation, and they order
forward. Local solar or civil time for Puget Sound differs from these stamps by the
Pacific time offset, which the feed does not carry; a diel analysis must supply it
from outside. (The time zone is my general knowledge, not a fact these two files
establish.)

The publication timestamp is *not* the time axis. It records when the reading
became available after telemetry and automated QC, follows the observation by
minutes to hours, and must never be read as when the conditions held. Sorting or
windowing a series by publication time reorders the phenomenon.

The observation timestamp declares a fixed fifteen-minute cadence. That is an
expectation about producer behaviour, not a constraint on the data and not a
property of any value. It does not assert that every quarter-hour slot has a
record, that records arrive in order, that a successor exists, or that a value may
be interpolated where none was recorded. A stream that misses a beat is late, not
malformed. What the cadence legitimately does is size a window, set a staleness
threshold, and make an absent slot detectable as a gap rather than absorbed
silently — all consumer-side decisions.

Every scalar channel is a point on that axis. The two standard deviations are the
exception: they characterise an interval rather than an instant, and that interval
is stated to lie within the sampling cycle but is otherwise unlocated and of
unknown length. Their position on the time axis is therefore known only to within
the cycle.

The example stamp falls exactly on a quarter hour. Phase alignment is not
guaranteed by anything in the files; only the period is declared.

# 5. Ambiguities

**Which channel a non-`pass` flag refers to.** There is one quality value and it
qualifies every result in the record jointly. When a record is `suspect`, nothing
recovers which of the fifteen channels was suspect. *Declining to decide* — this
must be resolved with the producer, and until it is, a non-`pass` record has to be
excluded wholesale rather than partially.

**What `missing` means when values are present.** The class is documented as "no
value is present", but every value member is optional, so absence is already
expressible structurally. Whether `missing` means the whole cycle failed or one
channel did is *not determined*. Declining.

**Nitrate: unit and analyte.** Two separate defects. The declared unit is an amount
of substance, µmol, while the description calls the value a concentration; those
are not the same thing and the feed does not reconcile them. My *guess*, marked as
a guess, is that µmol/L is intended, since that is the common marine convention —
but I am not willing to rely on it, and nitrate values here cannot be compared with
any external dataset until the producer states the denominator. Separately, the
description says "nitrate or nitrate-plus-nitrite" while the property reference
names nitrate alone. Those are different quantities for any budget or ratio work.
*Declining to decide* which is published.

**Chlorophyll: fluorescence or concentration.** The same defect. The property
reference names a mass concentration; the description offers "fluorescence or
concentration" as alternatives. The value is declared *measured* rather than
calculated, which leans toward the raw fluorometer reading rather than a
calibration-fitted concentration — but that is my inference from the derivation
annotation, not something the files state. *Declining to decide.* The consequence
is real: raw fluorescence and calibrated chlorophyll are not comparable across
instruments even at identical stated units.

**Pressure: absolute or gauge.** Not stated; the description only says "as
published by the raw datasets". The example value of 1.04 dbar alongside a 1.0 m
depth is consistent with in-situ sea pressure rather than absolute pressure. That
is a *guess* from one sample and I mark it as such; a single instance is not a
definition.

**How depth is obtained, and whether it is stable.** Depth carries no derivation
annotation, so whether it is a nominal deployment depth, a measured value, or a
figure derived from the pressure channel is *not determined*. If it is derived from
pressure, then depth and pressure are not independent facts about the record and
must not be used as though they were. Nor does anything establish that a station's
depth is constant over time; the description explicitly scopes it to "this cycle".

**Identifier registers.** Neither the station identifier nor the basin is bound to
any code list. They are free strings — the basin in the example is a human label
with spaces and a hyphen. Grouping by basin is therefore string matching on a label
that can drift between releases, and joining the station identifier to any external
station registry is not licensed by the schema. *Not determined*; treat both as
opaque and pin them against a producer-supplied list.

**Record identity and revision.** There is no record identifier, no publication
status, and no ingestion time. If two records appear for the same station and slot,
nothing in the feed says whether the later supersedes the earlier or duplicates it.
*Declining to decide* — this is a question for the producer's delivery contract.

**Which temperature-compensation and which pH convention.** Specific conductivity
is said to use "the standard temperature-compensation relation", which is not
identified; different relations give different numbers. pH is stated to be on the
total scale but nothing says at what temperature it is reported. Both *not
determined*.

**Extensibility is closed.** The record forbids additional properties, so the
missing facts above — burst length, deployment identifier, coordinates, per-channel
flags, the nitrate denominator — cannot arrive in the payload. They must come from
a separate channel, and any consumer design should assume that.

**A provenance caution.** The schema's own description records that the upstream
description it derives from was a mis-copied text describing an unrelated service,
and that it was replaced. The prose in this feed has already been wrong once. Where
the descriptions here are the only source for something — the nitrate denominator,
the chlorophyll analyte, the pressure reference — that history is a reason to
confirm rather than to rely.


TRANSCRIPT C

# 1. What this feed is

Each record is one in-water observation made by a fixed instrument package at a named
monitoring station, reporting the physical, chemical and optical state of a parcel of
seawater at a stated depth, together with a quality-control verdict and the time the
record was made available. The station identity, the basin it sits in, the instrument
that produced the reading, and the two timestamps are always present; **every measured
quantity is optional.** The station is a mooring — a fixed platform sampling repeatedly
at the same place — so the series is a time series at a point, not a survey track.

The single most consequential thing to understand before using this data: the record
carries *one* quality flag for the *whole* record, not one flag per measurement. A
record marked `pass` is not a statement that each of its eighteen numbers is good, and a
record marked `suspect` or `fail` does not tell you which sensor was the problem. Any
pipeline that filters on the flag is making an all-or-nothing decision about a
multi-sensor package in which sensors fail independently. That is the default failure
mode of this feed.

# 2. Analytics worth running

**Publication latency and feed health.** The gap between when water was observed and when
the record was published is directly computable, per station and over time. This is the
one analysis the data supports cleanly and unconditionally, because both timestamps are
mandatory and both refer to the same record. Widening latency, or latency that becomes
bimodal, is the earliest visible symptom of telemetry or QC-pipeline trouble — visible
before any measured value looks wrong.

**QC-regime auditing.** The flag distinguishes *not yet evaluated* from *passed*. Tracking
the share of records in each state, per station and per week, tells you whether a
station's data has actually been reviewed or merely arrived. Series that silently mix
reviewed and unreviewed records are not comparable to themselves over time, and this feed
lets you detect that. Do it before any trend work.

**Water-mass characterisation (temperature–salinity structure).** Temperature and salinity
are reported together for the same parcel, so classic T–S analysis is available: which
water masses the station sees, when riverine or oceanic influence dominates, and when the
column is stratified. This works because the two values share a record and therefore share
a time, a place and a depth.

**Stratification and depth structure — only if depth is populated.** Depth is optional. Where
several records from one station at one time carry different depths, you have a profile
and can compute gradients. Where depth is absent you have a number with no vertical
position, and in a stratified estuary that number is close to meaningless for anything but
existence checks.

**Oxygen dynamics and hypoxia exposure.** Dissolved oxygen is reported both as a
concentration and as a percent of saturation. Concentration is what organisms experience;
saturation tells you whether the water is being drawn down biologically or merely warmed.
Both being present in the same record lets you separate thermal from biological causes of
low oxygen, which a single one of them cannot do.

**Bloom detection and nutrient drawdown.** Chlorophyll and nitrate arrive in the same record
from the same water. Their inverse excursions — chlorophyll rising while nitrate falls —
are the signature of a productive event, and this feed supports that correlation directly
because there is no cross-record joining involved and therefore no time-alignment error.

**Sensor-fouling and drift surveillance.** The two dispersion values (chlorophyll and
turbidity) describe how variable the measurement was *within* a single record's sampling
burst. Rising within-burst dispersion, especially in turbidity, is a classic biofouling and
bubble-entrainment signal, and it appears before the central value becomes obviously wrong.
Because the instrument is identified by a vocabulary URI, you can partition this analysis
by instrument type and separate genuine environmental patchiness from a behaviour peculiar
to one sensor model.

**Diel and seasonal cycling.** Oxygen and chlorophyll cycle on a day/night rhythm and a
seasonal one. The feed supports this, but see the time section: the binning must be done in
local solar time, and the files do not give you the coordinates needed to compute it
rigorously.

**What is *not* supported.** There are no coordinates anywhere in the record. You cannot map
stations, compute inter-station distances, interpolate spatially, compute a true solar
angle, or detect that a mooring was relocated. Basin is a free-text label, not a geometry
and not a controlled value, so grouping by it is exposed to spelling and renaming drift.
Carbonate-system work is also out of reach: pH alone does not constrain it, and no second
carbonate parameter is present.

# 3. Combination rules

**Everything measured here is intensive** — a property of a parcel of water, not an amount of
anything. **No quantity in this feed may be summed across records.** Adding two salinities or
two temperatures produces a number with no referent. The only summable thing is a count of
records. Say this out loud to anyone building aggregations, because SQL will happily do it.

**A precondition for averaging anything.** An average is only defined over a stated
population. Here that means: same station, same depth, same instrument type, same QC
status, and no duplicated observations. The files do not state that station identity plus
observation time is unique, so a restated or corrected record may coexist with the record
it supersedes, distinguishable only by publication time. Deduplicate to the latest
publication time per station-and-observation-time *before* aggregating, or accept
double-counting.

**Temperature (°C).** Differences and averages are valid within a coherent population.
Ratios are not — Celsius has an arbitrary zero, so one reading is never "twice as warm" as
another. Do not sum.

**pH.** Differences and averages are **not** valid in the ordinary way. pH is a logarithm of
hydrogen-ion activity; the arithmetic mean of two pH values is not the pH of the mixed
water, and a difference of 0.3 is a factor of two in acidity, not a small increment. If you
must average, convert to activity, average that, convert back — and even then the result
is only defensible over water of similar temperature and salinity. Never sum. Additionally,
the scale convention (total, free, or NBS) is not stated, and these differ by roughly a
tenth of a unit; **pH values from records produced under different conventions must not be
differenced at all**, and the files give you no way to tell them apart.

**Conductivity, specific conductivity, and salinity — treat as one measurement, not three.**
Salinity is derived from conductivity together with temperature and pressure; specific
conductivity is the same conductivity normalised to a reference temperature. They are three
presentations of one physical determination. **Do not correlate or regress them against each
other** — you will recover the conversion formula and mistake it for a finding. For
comparing ionic content across records taken at different temperatures, use the specific
(normalised) value; raw conductivity compared across records confounds temperature with
salt content. Salinity may be differenced and averaged over a coherent population; never
summed. The reference temperature behind "specific" is not stated in the files.

**Dissolved oxygen, concentration vs. saturation — likewise not independent.** Saturation
percent is the concentration expressed against a solubility that is itself a function of
temperature, salinity and pressure. They carry the same measurement. Concentration may be
differenced and averaged. Saturation percent is a normalised ratio: averaging it across
records at different temperatures and salinities produces a figure that corresponds to no
water sample, and summing it is meaningless. Cross-producer comparison of saturation is
further compromised because the solubility formulation used is not stated and the common
alternatives disagree by a small but non-negligible amount.

**Depth and pressure.** These are also very likely two expressions of one determination
rather than two independent facts; do not treat them as mutually corroborating. Neither the
vertical datum for depth (below the instantaneous surface? below a tidal datum?) nor whether
pressure is absolute or gauge-referenced is established. Depths from different records
should be differenced only within a single station.

**Chlorophyll and turbidity central values.** Differences and averages within a coherent
population are fine; sums are not. Turbidity in nephelometric units is defined by the
measurement method and optical geometry, so **turbidity from different instrument models is
not strictly comparable** — partition by the instrument URI before comparing. The same
caution applies with less force to chlorophyll.

**The two dispersion values are the sharpest trap here.** A standard deviation must never be
summed or averaged directly. Pooling dispersion requires combining *variances* weighted by
the number of subsamples behind each one, and **the subsample count is not reported**. You
therefore cannot correctly pool these across records at all. They are usable as a
per-record diagnostic and comparable between records only under the assumption that every
record's sampling burst has the same length and rate — which the files do not state. Report
them; do not aggregate them.

**Nitrate.** May be differenced and averaged within a coherent population; not summed. But
see the ambiguities: the unit is incomplete.

**Absent values.** A missing measurement is not zero and not a low value. Because every
measured member is optional and the quality flag is record-level, an absent value cannot be
distinguished from a measurement that was taken and withheld. Averages computed over
records where a member is sometimes absent are averages over a shifting population; carry
the count alongside every aggregate.

# 4. Time

**The observation time is the time axis of the thing described** — the moment the water was
in that state. The publication time is an axis of the *record*, describing when the
information became available; it is the right axis for latency, backfill and revision
analysis and the wrong axis for anything environmental. Ordering a series by publication
time will reorder the ocean.

Positions on the observation axis relate to civil time through the UTC offset carried in
the value itself. The example is expressed at zero offset, so it denotes an unambiguous
instant. Whether every record in the feed carries an offset is not established by these two
files; a value written without one would not be placeable on a global axis at all, and a
consumer should reject rather than assume such a value.

Two qualifications matter more than they appear to.

First, **the observation time is presented as an instant, but the record almost certainly is
not one.** The presence of within-record dispersion statistics means each record summarises a
burst of subsamples spanning some interval. The length of that interval is not given, and
neither is whether the stated time marks the start, the centre, or the end of it. Treat the
timestamp as an instant for coarse work; do not use it for anything at finer resolution than
the (unknown) burst length, and do not assume two records from different stations bearing
the same timestamp sampled the same window.

Second, **local civil time is not derivable from these files.** There are no coordinates and no
timezone member. Diel analysis — the day/night cycle in oxygen and chlorophyll, which is one
of the strongest signals in data like this — must be binned in local solar time, or the
cycle will smear and, across a season, drift. Binning in UTC is wrong here, and binning by a
fixed offset is wrong too wherever the location observes daylight saving, because the offset
changes mid-series.

Sampling cadence is not established. One record does not tell you whether the feed is
regular, and gap analysis, duty-cycle weighting, and any duration-based exposure metric
(e.g. hours below an oxygen threshold) all depend on knowing it. Until cadence is
established from the data itself, exposure must be reported as a count of records, not as a
duration.

# 5. Ambiguities

**Whether the quality flag applies per record or per measurement.** Declining to decide. The
evidence points to per-record, and that is what I have assumed throughout, but nothing here
states it, and the consequences differ enormously.

**What the "missing" flag state means.** Declining to decide. It may mark a placeholder for an
expected observation that never arrived, or a record whose values were all lost. Either way,
do not treat it as a low or zero reading.

**Whether "not evaluated" is safe to use.** Declining to decide. It is clearly distinct from
"pass", and folding the two together will bias any series; whether unevaluated data is
usable at all is a policy question these files do not answer.

**The denominator for nitrate.** The unit names an amount of substance with no volume. My
guess — **and it is a guess** — is micromoles per litre, which is the near-universal
convention for dissolved nutrients in seawater and is consistent in magnitude with the
example value. It could be micromoles per kilogram, which differs by roughly the density of
seawater, a few percent. This matters for absolute comparison against other datasets and not
much for internal trend work.

**The reference temperature behind "specific" conductivity.** Guess: 25 °C, the standard
convention. Not stated.

**The pH scale convention.** Declining to guess. Total, free and NBS scales are all in use for
seawater and differ by an amount comparable to a decade of acidification signal.

**The oxygen-saturation formulation.** Declining to guess. Several are in common use and they
disagree slightly.

**Whether the reported depth is a measurement or a conversion of pressure.** Guess: converted
from pressure, since the two are numerically consistent in the example. If so they are not
independent evidence.

**The vertical datum for depth, and whether pressure is absolute or gauge.** Declining to
decide, though the example's pressure value at the stated depth is consistent with a
gauge/in-water reading rather than an absolute one — **a guess.**

**The averaging window length behind each record, and where the timestamp sits within it.**
Not determined. This is the gap I would close first, because it bounds the temporal
resolution of everything else.

**The number of subsamples behind each dispersion value.** Not determined, and its absence
makes correct pooling of those values impossible rather than merely awkward.

**Whether station identity plus observation time is unique.** Not determined. There is no
revision counter or record version, so a corrected restatement would be detectable only as a
duplicate with a later publication time — and only if you look for it.

**Whether the station identifier is stable and whether the station has ever moved.** Not
determined. Without coordinates, a relocated mooring is invisible and would appear as a step
change in the environment.

**Whether the instrument reference identifies a model or an individual unit.** Guess: a model
or device *type*, since it points into a controlled vocabulary rather than carrying a serial
number. If so, you can partition by instrument type but cannot attribute drift to a specific
deployed unit or align it with calibration and servicing events.

**Units generally.** Units appear only inside member names; nothing in the schema declares them
in a form a tool could check, and no numeric bounds are enforced. The conductivity values are
internally consistent with siemens per metre as named, but a producer emitting the
also-common millisiemens per centimetre would be off by a factor of ten and **nothing here
would catch it.** Validate ranges yourself.

**Geographic location, and therefore basin membership.** Not determined. Basin is an
uncontrolled label; treat it as a hint, not a key.

**Whether chlorophyll is a direct measurement or a fluorescence proxy.** Declining to decide.
The distinction affects how much you trust absolute values versus relative change, and the
files do not address it.


TRANSCRIPT D

## 1. What this feed is

Each record is one sampling cycle from a fixed marine monitoring mooring operated in Puget Sound, Washington. A single cycle carries the CTD channels (temperature, conductivity, pressure, and the salinity derived from them), the optical channels (dissolved oxygen, pH, chlorophyll, turbidity), and a nitrate channel, all attributed to one water parcel at one stated depth at one instant.

The thing to understand before touching the data is that a record names three different physical things, and confusing them is the primary source of wrong answers. The mooring is the station the programme reports against. The water parcel at the stated depth is what was actually measured. The basin is the water body the result is meant to inform. A "station average" that silently pools parcels sampled at different depths is not an average of anything real, and a basin-level conclusion drawn from one mooring is a claim the record does not support on its own.

Cycles are nominally quarter-hourly, so the stream is a regular grid with detectable gaps rather than an irregular event log.

## 2. Analytics worth running

**Diel and seasonal cycling.** Temperature, oxygen, chlorophyll and pH at a fixed station and depth on a fifteen-minute grid resolve the daily light-driven cycle cleanly. The cadence is declared and fixed, so a missing slot is a genuine gap rather than a scheduling artefact, and you can quantify completeness rather than guess at it.

**Hypoxia exposure.** Both oxygen concentration and percent saturation are present, and both are timestamped to the instant the condition held for the sampled parcel. Threshold crossings and time-below-threshold are therefore computable — with the caveat in section 4 that these are point values, not fifteen-minute block means.

**Bloom detection with a confounder control.** Chlorophyll and turbidity are read concurrently from the same parcel. Elevated fluorescence accompanied by elevated turbidity is a different story from elevated fluorescence alone, and the concurrency is what makes the discrimination possible.

**Nutrient drawdown.** Nitrate and chlorophyll share a timestamp and a parcel, so uptake episodes can be examined without cross-feed alignment.

**Freshwater and stratification signals.** Salinity and temperature together characterise the parcel's water mass. True stratification analysis requires records at differing depths within the same cycle; whether the feed supplies those is not established (section 5).

**Patchiness and sensor health.** The two standard-deviation channels summarise within-cycle bursts and give a within-cycle variability signal that the instantaneous channels cannot. Their usefulness is bounded by the unpublished burst configuration.

**Pipeline latency and completeness.** The gap between the observation instant and the publication instant is directly measurable per record, giving a latency distribution, a basis for choosing a watermark in any streaming consumer, and a way to distinguish a genuinely absent reading from one that simply has not arrived yet. The example record shows roughly twenty-four minutes.

**Quality-flag epidemiology.** Flag prevalence over time at a station is a leading indicator of sensor fouling, drift or failure, independent of the physical signals themselves.

## 3. Combination rules

**Blanket gates that apply to every quantity below.** Two values are candidates for comparison, differencing or averaging only when the station agrees, the sampled depth agrees, the sonde agrees, and the summary function agrees. The sonde identity is comparability-critical and is stated to be so: readings from a different package are not interchangeable even when the property and the station match, so any recalibration or hardware swap that changes the sonde URI creates a seam in the series that must be handled as a seam, not smoothed over. Records flagged `fail` or `missing` must be excluded before any aggregate; `not_evaluated` means no test was applied and must not be treated as equivalent to `pass`; `suspect` should be carried through as a marked subset rather than silently kept or silently dropped. There is exactly one flag per record, not one per channel — see section 5.

**Water temperature.** Compare and difference freely within the gates. Average freely, but only as a time-weighted mean over an unbiased set of slots; a gappy day averages toward whatever hours survived. Never sum: Celsius has an arbitrary zero, so a sum of temperatures is not a quantity. Note that a *difference* of two Celsius values is a well-formed interval even though the values themselves are not on a ratio scale.

**Conductivity and specific conductivity.** These two must never be compared with each other, differenced against each other, pooled, or fed into the same series — despite carrying the same unit, the same symbol and the same standard-name reference. One is read at the in-situ temperature, the other is normalised to 25 °C. Identical units and identical property references here mean identical *dimension*, not identical *quantity*. This is the sharpest trap in the feed, because every naive check an analyst might run to confirm the two are compatible will pass.

Within its own series, in-situ conductivity may be compared, differenced and averaged, but any change in it conflates a change in ionic content with a change in temperature; if you want the ionic signal, use the specific conductivity or the salinity. Specific conductivity may be compared, differenced and averaged across records that differ in temperature — that is what it exists for. Neither may be summed.

**Pressure.** Compare, difference and average within the gates. Do not sum. The reference datum is not stated (section 5), which restricts differencing to within this feed.

**Salinity.** Compare, difference and average within the gates. Do not sum. The critical restriction is statistical rather than dimensional: salinity is a deterministic function of the conductivity, temperature and pressure in the very same record. It is not an independent observation. Placing salinity alongside temperature and conductivity as co-predictors in a regression, or reporting a correlation between salinity and conductivity as a finding, is degenerate — you are measuring the definition, not the ocean.

**Dissolved oxygen concentration.** Compare, difference and average within the gates. Never sum, and never attempt a mass or inventory total: this is an intensive concentration, and the feed carries no volume, no water-column geometry and no station coordinates with which to integrate it.

**Oxygen saturation percentage.** Compare, difference and average within the gates, and do not sum. Two further restrictions. It is computed from the oxygen concentration together with the concurrent temperature, salinity and pressure, so it is not independent of any of those and must not be treated as a separate observation in a joint statistical model. And because solubility is a nonlinear function of temperature and salinity, the mean of the saturation values is not the saturation computed from the mean concentration; pick one convention and do not mix results derived under both.

**pH.** Comparison and differencing are valid — a pH difference is a log ratio of hydrogen-ion activity and is meaningful. Arithmetic averaging is not valid if what you want is a mean hydrogen-ion activity, because the scale is logarithmic; convert, average, convert back, or state explicitly that you are reporting a mean of the logarithm. Never sum. Comparison against pH from any external source is valid only if that source is also on the total scale; the scale is stated here precisely because scale mismatch silently corrupts such comparisons.

**Chlorophyll.** Compare, difference and average within the gates. Do not sum. Cross-station and cross-instrument comparison is not supported, because whether this channel is raw fluorescence or a calibrated concentration is left open (section 5) — within one station and one sonde the series is internally consistent either way, which is why the ambiguity only bites when you widen the scope.

**Turbidity.** Same rules as chlorophyll. NTU is defined by the measurement geometry of the instrument, so the sonde gate is not a formality here: turbidity from a different optical package is a different quantity in practice even under the same unit.

**The two standard-deviation channels.** These carry the same observed property as their parent channels but a different summary function, and they are therefore not like quantities. Do not compare a standard deviation to a concentration, do not difference them, do not place them on the same axis as if they were the same measurement, and do not let them fall into the same aggregation as the parent channel. A ratio of standard deviation to mean is a legitimate derived index of within-burst variability, but it is a new quantity, not a comparison of the two.

Standard deviations must not be averaged across records, and must not be pooled into an aggregate spread. Pooling requires variances and per-burst sample counts; the burst length is configured per deployment and is not published, and no support period is declared. Even comparing one record's standard deviation to another's rests on the assumption that both bursts had the same configuration — an assumption the feed does not license. Treat cross-record comparison of these channels as provisional and say so.

**Nitrate.** Compare, difference and average within the gates; do not sum. Comparison against any external nitrate series is blocked until the unit question in section 5 is resolved.

**Across stations.** Different stations sample different places. Values may be compared at the level of the basin they are interpreted for, and only when the basin agrees and the procedure agrees. Nothing in a record licenses inferring the basin from the station or the parcel; the basin is stated independently precisely because it is not derivable.

**Across depths.** Different depths are different parcels. Differencing across depths within a cycle is the correct way to compute vertical structure. Pooling across depths into a single station mean is not an average of a physical quantity and should never be done implicitly.

## 4. Time

The observation timestamp is the time axis of the thing described: the instant at which the stated conditions held for the sampled water parcel. It is UTC, ISO 8601, and lands on quarter-hour slots under a declared fixed fifteen-minute cadence, so the series can be treated as a regular grid and an absent slot read as a real gap.

The publication timestamp is the instant the reading became available downstream, after telemetry and automated quality control. It trails the observation by minutes to hours and must never be used to bucket, bin, window or sort the physical signals. Its legitimate uses are latency measurement, late-arrival handling, watermarking, and as-of reconstruction of what a consumer could have known at a given moment. A dashboard that plots temperature against publication time is showing the behaviour of the data pipeline, not the water.

All sensor channels are instantaneous point values, not fifteen-minute averages. This matters for any integral: time below an oxygen threshold, cumulative exposure, or daily load must be obtained by interpolating between points, and treating each value as representative of the whole quarter-hour block is a modelling choice you are making, not something the data states. It also caps the resolvable frequency — anything varying on a timescale shorter than about half an hour aliases.

The two standard-deviation channels are the exception: they characterise an interval inside the cycle rather than an instant, and the extent of that interval is not published. They cannot be aligned to a known window and should not be plotted as though they applied to the full quarter hour.

Relating positions on the axis to civil time requires a conversion the record does not carry. The stations are described as being in King County, Washington, which places them in the US Pacific zone with summer time — an inference from the prose, not a declared member. Any diel analysis must convert to local time properly rather than applying a fixed offset, or the summer half of the year will be smeared by an hour against the solar cycle that drives the very signals being studied.

## 5. Ambiguities

**Whether the sampled depth is fixed or varies between cycles.** The measurement package is called a profiling sonde, which suggests the depth may change from cycle to cycle, while the example shows a single shallow depth. This is the single largest hazard in the feed: if depth varies, a naive time series "at the station" silently interleaves different water parcels and every trend derived from it is suspect. **Declining to decide.** Determine it empirically from the data before building anything, and treat depth as a grouping key until you have.

**Records without a depth.** The depth member is not required, so a record may arrive with no proximate feature identified. Such a record cannot be placed in the water column and cannot be pooled with records that carry a depth. What the producer intends by omitting it is **not determined**; excluding those records from depth-scoped analysis is the conservative course.

**Whether the quality flag covers the whole record or a single channel.** Only one flag is present, and it is described as classifying "this reading." **Guess: it applies to the record as a whole.** If it is in fact a roll-up of per-channel flags, then a `suspect` record may have exactly one bad channel and discarding it wholesale throws away good data — while a `pass` record could in principle hide an unevaluated channel. The distinction changes the yield of the dataset materially and cannot be settled from what is here.

**The nitrate unit.** The unit given is micromoles — an amount of substance — while the description calls the value a concentration. A concentration requires a volume or mass denominator. **Guess: micromoles per litre.** This is a guess and should not be relied on; the values cannot be compared with any externally sourced nitrate series, in µmol/L or µmol/kg, until the producer resolves it.

**The pressure datum.** Whether pressure is absolute or referenced to the sea surface is not stated. **Guess: sea-surface-referenced**, since the example shows roughly one decibar at roughly one metre, whereas absolute pressure at that depth would be about eleven. Differencing within the feed is unaffected; comparison to external pressure data is blocked until confirmed.

**Whether chlorophyll is raw fluorescence or calibrated concentration.** The description offers both readings of the same channel. **Not determined.** Within one station and one sonde this does not matter; it blocks absolute concentration claims, cross-station comparison, and any comparison to laboratory or satellite chlorophyll.

**Burst length and sample count behind the standard-deviation channels.** Explicitly unpublished and explicitly left indeterminate. **Declining to decide.** Consequences are set out in section 3: no pooling, no variance arithmetic, and cross-record comparison only under an assumption of stable deployment configuration.

**Revisions and duplicates.** There is no version, sequence or revision member. If a reading is reprocessed and republished, nothing distinguishes the correction from a duplicate except the later publication timestamp. **Guess: deduplicate on station and observation time, keeping the latest publication timestamp.** That is a plausible convention, not a stated one, and it will silently discard a genuine second reading if the producer ever emits two distinct parcels in one slot.

**Absence versus the `missing` flag.** Every measurement channel is optional, and the flag vocabulary also includes `missing`. Whether an omitted field and a `missing` flag mean the same thing, or whether one indicates a channel not fitted to this deployment and the other a channel that failed, is **not determined**.

**Station location.** There are no coordinates. No mapping, no spatial interpolation, no comparison against satellite products or circulation model output is possible without an external station registry, which is outside this feed.

**Trust in the descriptive text.** The schema records that it inherited a description from an upstream feeder that was outright wrong for this record and had to be replaced. That is a useful warning: the descriptive prose here is a corrected artefact of a chain of copies, and any single description should be treated as authoritative only where it is internally consistent with the units, roles and example values. The nitrate unit mismatch above is plausibly one such residue.
