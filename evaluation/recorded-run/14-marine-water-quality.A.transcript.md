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
