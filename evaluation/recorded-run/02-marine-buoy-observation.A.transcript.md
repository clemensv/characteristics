# 1. What this feed is

Each record is one observation cycle from one fixed marine observing platform — a moored ocean buoy, a coastal C-MAN station, or a partner platform — reporting the state of the atmosphere and sea surface in that platform's immediate surroundings. The platform is identified by a station code and located by latitude and longitude, and the cycle is stamped with a single UTC instant. Nominally one record exists per station per five-minute slot.

The critical thing to understand before touching the numbers: a record is **not** a snapshot of conditions at the stamped instant. It is a bundle of retrospective summaries computed over windows of *different lengths*, all ending (as far as the record tells us) at that instant. The wind fields summarise roughly the last two or eight minutes. The wave fields summarise the last twenty minutes. The pressure tendency summarises the last three hours. The temperatures and the pressure appear to be near-instantaneous readings, though nothing states this explicitly. Treating the record as a single-instant vector — which is what almost every downstream tool will do by default — silently mixes four different time scales.

A second structural point: the station's *type* is not carried in the record. Several definitions in this feed depend on station type, and none of them can be resolved from the data alone.

# 2. Analytics

**Synoptic and frontal analysis.** Sea-level pressure is reduced to a common datum, so it is directly comparable and differenceable across stations regardless of platform elevation. That makes horizontal pressure-gradient fields, trough and ridge tracking, and multi-station synoptic mapping valid without further correction. Pressure tendency gives the sign and magnitude of local pressure change directly, which is the classic short-range indicator of an approaching or departing system.

**Sea-state characterisation and wind-sea/swell separation.** Three independent wave descriptors are present: an energy-weighted peak period, a mean period over all waves, and a direction tied specifically to the peak band. A large gap between peak period and mean period, or a large angular separation between the peak-band wave direction and the wind direction, indicates a swell system arriving from a distant source rather than locally generated wind sea. The data supports this because the peak period and the mean period are genuinely different statistics of the same spectrum, not two estimates of one thing.

**Wave-growth and fetch relationships.** Significant wave height, mean wave period and wind speed together support empirical wave-growth checks and the detection of sea states inconsistent with local forcing. Caution: the wind and wave values in one record do not cover the same interval, so at short lag the pairing is approximate.

**Air–sea stability and fog potential.** Air temperature, water temperature and dewpoint are all on the same scale, so air-minus-sea temperature difference and dewpoint depression are both computable per record. Negative air-minus-sea difference indicates an unstable marine layer; small dewpoint depression over cold water is the classic advection-fog signature. Where visibility is present, it can be used to verify the inferred fog condition — but see the censoring caveat below.

**Gust structure.** Gust divided by mean wind speed gives a gust factor, usable as a turbulence/instability proxy and as a data-quality screen. This works only within a station, because both the averaging window and the gust interval vary by platform.

**Sensor-availability and outage monitoring.** Only four members are mandatory. Every measured quantity may be absent. Tracking which members appear per station over time distinguishes stations that never had a sensor from stations whose sensor has failed — and this is worth running as a first-class analysis, because a naïve availability-weighted average will otherwise drift as instruments drop out.

**Coastal water level.** Where tide is present, within-station water-level time series, tidal harmonic fitting, and residual (storm surge) extraction are supported, since the datum is fixed per station.

What the data does **not** support: anything requiring a vertical profile, sensor height, measurement uncertainty, or quality-control status. There are no QC flags, so good, suspect and failed readings are indistinguishable.

# 3. Combination rules

**Units are not uniform.** Everything is SI except water level, which is in feet, and visibility, which is in nautical miles. Any pipeline that treats all numeric members homogeneously will produce nonsense.

**Wind direction and mean wave direction** are angular coordinates in degrees true. They may not be arithmetically averaged, differenced, or summed. Differences must be taken modulo 360 and reduced to the ±180 range; means must be circular (vector) means. Averaging 350° and 10° arithmetically yields 180°, which is the opposite direction. Additionally, mean wave direction describes only the peak energy band, so it belongs with the dominant wave period, not with significant wave height, and it is not the mean direction of the whole sea state.

**Wind speed and wind direction** may be compared, differenced and averaged *within a single station*. Across stations they are only safely combined if the stations share a type, because the averaging window is either two or eight minutes depending on type and the type is not in the record. A two-minute mean and an eight-minute mean are different statistics of the same wind; comparing them across a station-type boundary compares unlike quantities. Wind speed must never be summed. Averaging wind speeds across records is valid as a mean-of-means only where the windows are of equal length and non-overlapping; with a five-minute cadence and an eight-minute window, consecutive buoy records overlap and the resulting mean is not an unweighted mean over elapsed time.

**Gust** is a maximum over a window, not a mean. Maxima may be compared and may be aggregated by taking the maximum over a set of records, and that result is a valid peak for the covered span (subject to window overlap). Gusts must never be summed, and averaging them produces a mean-of-peaks, which is a legitimate statistic only if labelled as such — it is not the peak of the pooled period. The gust interval is either five or eight seconds and the record does not say which, so gust factors are not comparable across stations.

**Significant wave height** is a mean taken over a restricted subpopulation — the highest one-third of waves — not over all waves. Consequently, averaging it across records yields the mean of significant heights, which is *not* the significant height of the pooled interval; the latter would require re-selecting the top third of the combined wave population, which the data does not permit. It may be compared and differenced across records and across stations, because the definition and the twenty-minute window are fixed and station-independent. It must never be summed.

**Dominant wave period** is read off an energy spectrum as a peak location — a mode, not a mean. It must not be averaged: the mean of peak locations is not the peak of the averaged spectrum, and in bimodal seas (wind sea plus swell) this value jumps discontinuously between two bands as the energy balance tips. Compare it, take medians or histograms of it, but do not treat it as an additive quantity. Differencing it between records is meaningful only as "the peak moved", not as a rate of anything.

**Average wave period** is a mean over all waves in the window and may be averaged across records, but strictly this is a weighted mean whose weights are the wave counts per window, and those counts are not carried. With equal-length windows the equal-weight approximation is reasonable. Not summable.

**Wave overlap.** The wave window is twenty minutes and the cadence is five minutes, so four consecutive records share fifteen minutes of the same underlying wave sample. Successive wave values are strongly autocorrelated by construction. Do not treat them as independent observations in any statistical test, and do not compute effective sample sizes from record counts.

**Pressure** is reduced to sea level, which is precisely what makes it cross-station comparable and differenceable — station elevation has already been removed. Averaging over a set of stations gives a valid field mean. Summing is meaningless.

**Pressure tendency** is *already a difference* over the preceding three hours. Do not sum tendencies across records: with a five-minute cadence, consecutive three-hour windows overlap by 98%, so a sum over a day would count each pressure change roughly thirty-six times. To get the pressure change over an arbitrary interval, difference the pressure values at the endpoints; never accumulate the tendency. Tendencies may be compared and mapped across stations, since the interval length is fixed and station-independent. Differencing tendencies to obtain a second derivative is possible in principle but the overlap makes it near-degenerate at short lags.

**Air temperature, water temperature and dewpoint** are on an interval scale in Celsius. Differences between them are meaningful and are the most useful derived quantities here (air-minus-sea, dewpoint depression). They may be averaged. They must never be summed. Two cautions: dewpoint is computed from air temperature and humidity, so it is *not statistically independent* of air temperature — do not enter both as independent predictors in a regression, and do not treat their correlation as a physical finding. And the sensor height for air temperature is not carried, so cross-station temperature comparison carries an unstated and unquantifiable height offset.

**Visibility** is censored. The sensor range is stated as 0 to 1.6 nautical miles, so any value at the ceiling means "at least 1.6", not "1.6". Averaging a mixture of censored and uncensored values biases the result low, and the bias grows as conditions improve. Use survival/censored-data methods, or reduce to a binary "below threshold" indicator. It is also generally only present on one class of station, so its absence is not evidence of poor visibility.

**Water level** is referenced to Mean Lower Low Water, which is a *local* datum specific to each station. Values are therefore comparable and differenceable only within a station. Differencing water level between two stations, or averaging it across stations, is meaningless — it measures the offset between two arbitrary local datums as much as anything physical. Within a station, differencing and averaging are valid; summing is not.

**Latitude and longitude** are coordinates. Averaging them across records is meaningful only as a check that a moored platform has stayed within its watch circle; it is not a measurement of anything. Nothing in the data establishes that they are constant per station, so do not assume they are.

**Across quantities:** no two members of this record may be combined on the assumption that they cover the same interval. Wind, waves and tendency each cover a different span ending at the same instant.

# 4. Time

The `timestamp` member is the sole time axis, and it is an instant in UTC with an explicit zero offset. Positions on the axis map to civil time directly: no offset table, no daylight-saving rule, and no ambiguous or skipped local times. Ordering, differencing and binning are all unproblematic.

The subtlety is what the instant *labels*. It is the end of the observation windows, not their midpoint and not their start. This is stated explicitly for the wind quantities and follows for the three-hour pressure tendency, whose interval ends at the observation time. The record is therefore right-labelled throughout. Anyone resampling, plotting, or joining this feed against a centre-labelled or left-labelled source will introduce a lag equal to half or all of the window length — up to ten minutes for waves and up to ninety minutes for the pressure tendency if it is mistaken for an instantaneous quantity.

The intended cadence is five minutes, following the refresh interval of the upstream composite file. This is an expectation about the producer, not a guarantee about the data: gaps, duplicates and irregular spacing must be handled. Because the wave window is four times the cadence and the tendency window is thirty-six times the cadence, consecutive records are not independent samples of the time axis.

There is no publication or ingestion time, and no version or revision member. Late-arriving data and corrected values are therefore undetectable from the record itself; a re-issued observation for the same station and instant cannot be distinguished from a duplicate.

Local solar or civil time at the station is not carried and would have to be derived externally; longitude gives solar time but not the station's civil time zone.

# 5. Ambiguities

**Station type is not carried.** This is the most consequential gap. It determines the wind averaging window (two versus eight minutes), the gust interval (five versus eight seconds), and whether visibility and water level sensors exist at all. *I am declining to decide it.* It cannot be inferred from the record; it must come from external station metadata.

**Sensor heights are not carried.** Anemometer height and air-temperature sensor height are unknown, so wind speeds cannot be reduced to a standard reference height and cross-station wind and temperature comparisons carry an unquantifiable offset. *Declining to decide.*

**Whether the wave window ends at the timestamp.** This is stated for the wind quantities and for the pressure tendency, but for the wave quantities the window is described without being anchored to the observation time. *I am assuming* it also ends at the timestamp, by analogy with the other quantities. Marked as an assumption; if the wave window is centred or lagged instead, wave-to-wind timing comparisons shift by up to twenty minutes.

**Mean wave direction convention.** For wind, the direction is explicitly "coming from". For waves, no convention is given, and both "coming from" and "going toward" are in use in oceanography. *This is a guess:* the value is most likely the direction waves are coming from, matching the wind convention used in the same record and making the wind/wave direction comparison direct. Marked as a guess — a 180° error here inverts every swell-source inference.

**Meaning of an absent member.** Only four members are mandatory and the example omits two. Nothing distinguishes "no such sensor on this platform", "sensor failed this cycle", "value failed quality control", and "value not yet available". *Declining to decide.* Related: it is not determined whether the producer omits missing values or emits a sentinel; the example omits, but one example does not establish a policy, and the upstream source is known to use numeric sentinels for missing data. Any consumer must guard against sentinel values appearing in a numeric member.

**Record identity.** No uniqueness constraint or key is declared. Station plus timestamp is the obvious candidate, but nothing forbids duplicates or contradictory records for the same station and instant. *Declining to decide;* deduplicate defensively.

**Value ranges.** No bounds are declared on any member, including latitude and longitude. Physically impossible values are not excluded by the data contract.

**Measurement uncertainty and quality control.** Neither is present. There is no way to distinguish a good reading from a suspect one, and no error bars for any quantity. *Declining to decide* — this cannot be recovered from the feed.

**Tidal datum epoch.** Mean Lower Low Water is defined over a specific multi-decade tidal epoch which is not stated, so water-level series spanning a datum re-definition would contain an undetectable step. *Declining to decide.*

**Whether platform position is static.** Not stated. Moored buoys move within a watch circle, and it is not determined whether the coordinates are a fixed nominal position or a per-cycle measurement. *Declining to decide.*

**Machine-readability of the window semantics.** Every statement about averaging windows, statistics, peak-versus-mean derivation, and interval anchoring exists only as prose. None of it is expressed in a form a tool can act on. Consequently no automated pipeline can enforce any of the combination rules in section 3; they must be applied by hand or encoded separately. This is the single largest practical risk in using this feed at scale.
