# 1. What this feed is

Each record is a marine surface-conditions report from one fixed observing platform — a moored ocean buoy, a coastal C-MAN station, or a partner installation — describing the atmosphere and sea immediately around that platform. The platform identifier is the feature of interest: the record does not describe the buoy, it describes the patch of ocean and air the buoy sits in. Position accompanies every record in WGS 84 (EPSG:4326), so the feed is self-locating and can be joined to other geospatial data without a station registry, though a registry is still needed for everything about the platform itself.

The critical structural fact is that a record is **not a snapshot**. It is a bundle of quantities with three different temporal footprints that happen to share an end point: instantaneous readings (pressure, air and water temperature, dewpoint, visibility, tide), quantities summarising a 20-minute wave-sampling window, quantities summarising a short wind-averaging window whose length the record does not carry, and one quantity summarising the preceding three hours. Treating the record as a single-instant observation is the first and most damaging mistake available here.

The second structural fact is that records are emitted far more often than most of these windows are long. The publication slot is five minutes; the wave window is twenty minutes and the pressure-tendency window is three hours. Consecutive records therefore describe **heavily overlapping** windows and are not independent samples.

# 2. Analytics

**Storm and frontal tracking across stations.** Pressure is reduced to sea level by a standard-atmosphere correction, so absolute pressure is directly comparable between platforms at different elevations — an isobaric field can be built from a multi-station slice at a common timestamp. Pressure tendency strengthens this: it is a signed three-hour change, which is datum-free and elevation-free, so it is the cleanest cross-station quantity in the feed. Mapping tendency across stations identifies deepening/filling centres and frontal passage without any calibration assumptions.

**Sea state characterisation and wave climate.** Significant wave height, dominant period, average period and mean wave direction all share the same 20-minute window ending at the record timestamp, so within a record they are mutually consistent and describe one sea state. Wave steepness (height against period) and the separation between dominant and average period — a spread indicator distinguishing a narrow swell-dominated spectrum from a broad wind-sea — are computable per record with no external input.

**Wind–wave coupling.** Wind direction and mean wave direction are both in degrees true, so their angular separation is meaningful and diagnoses locally generated wind sea versus remotely generated swell. Wind speed against wave height over a station's history yields an empirical fetch/duration relationship for that site.

**Gust structure.** The peak gust and the mean wind speed are drawn from the *same* window, so their ratio (gust factor) is well posed within a single record and is a usable turbulence/instability indicator and a marine-safety threshold input.

**Air–sea thermal contrast and fog potential.** Air temperature, water temperature and dewpoint are all instantaneous, co-located and in the same unit at the same timestamp. Water-minus-air gives the stability sign for the surface layer; air-minus-dewpoint gives the dewpoint depression. Warm water under cool moist air, or a dewpoint at or above the water temperature, are the classic advection-fog and sea-smoke signatures, and the feed supports flagging them directly.

**Data-availability and integrity monitoring.** The stream declares a fixed five-minute cadence, which gives an expected slot grid. Missing slots, duplicate (station, timestamp) pairs and stalled values are all detectable without domain knowledge, and this is worth running first because everything downstream depends on it.

**What the feed does not support.** Anything requiring sensor height, platform type, quality flags, or spectral detail beyond the four summary wave numbers. There is no wave spectrum, no relative humidity, no current, and no station metadata.

# 3. Combination rules

**Identity and keying.** Two records with different platform identifiers describe different features of interest and must never be differenced as if they were one time series. Deduplicate on identifier plus timestamp before anything else.

**Position.** Latitude and longitude locate the observation; they are not measurements. Averaging them produces a centroid, which is a legitimate summary of a station set but is not an observed value. Do not difference positions across records as if that were platform motion unless you have separately established that the platforms are moored and that reported position varies only by watch-circle drift — the files do not establish this.

**Directions (wind direction, mean wave direction).** These are angles on a circle. They may be compared and they may be differenced, but only modulo 360 with the result folded into ±180. They may **not** be summed, and they may **not** be arithmetically averaged — the wrap at 0/360 makes the linear mean wrong, and for a northerly wind it is catastrophically wrong. Use vector/circular statistics. If you want a mean wind direction that is physically meaningful, resolve speed and direction into components and average the components; the unweighted circular mean of direction alone is a different quantity and should be labelled as such. Wind direction and wave direction may be differenced against each other **only after** the wave-direction convention is settled (see §5).

**Wind speed and gust.** Within one record the two share a window, so their ratio and difference are valid. **Across records or across stations they are not automatically comparable**, because the averaging window is 8 minutes for buoys and 2 minutes for land stations and the record does not say which it is. A 2-minute mean and an 8-minute mean are different quantities: the shorter window has higher variance and a systematically higher expected maximum. Comparing them, or pooling them into one distribution, requires resolving platform type from external station metadata. Wind speeds may be averaged within a station once the window length is known and the records chosen are non-overlapping; they may not be summed.

Gust is a maximum. Maxima may be compared, and taking the maximum across records is valid. The **mean of gusts across records is a mean of block maxima**, which is a legitimate but different statistic from "average gust" and must be labelled that way; it is not an estimate of the mean wind. Gusts may never be summed.

**Overlapping windows — the dominant hazard.** With a five-minute publication slot and a 20-minute wave window, four consecutive records share window content; with an 8-minute wind window, roughly two do. Consecutive wave and wind values are therefore autocorrelated by construction. Any running mean, variance, trend test, or confidence interval that assumes independent observations is invalid on consecutive records. To get independent wave samples, select records at least 20 minutes apart; for wind, at least the window length apart.

**Pressure tendency — never sum.** This is already a difference over the preceding three hours, republished every five minutes. Summing tendencies across consecutive records would count the same pressure change roughly thirty-six times over. Tendencies may be compared across stations and across times, and may be averaged over a set of records to describe a typical rate. They may be **accumulated only over strictly disjoint three-hour windows**, i.e. by selecting records exactly three hours apart; that reconstructs total pressure change legitimately. Differencing tendency between records gives a second derivative of pressure, which is well defined but is a different quantity from tendency and should be named as such.

**Pressure.** Because it is sea-level reduced, it may be compared, differenced and averaged across stations freely. It must **not** be used as the barometric pressure at the platform — it is not the raw reading, so it cannot be fed into air-density, altimetry or gas-law calculations for the site.

**Temperatures (air, water, dewpoint).** All three are instantaneous and in the same unit, so within a record they may be differenced against each other. Across records at one station, or across stations, they may be compared, differenced and averaged. They may **not** be summed — a sum of Celsius temperatures has no meaning. A difference of two Celsius values is a temperature *interval*, not a Celsius temperature, and must not be re-injected anywhere expecting an absolute temperature. Dewpoint is computed from air temperature and humidity, so it is **not statistically independent** of air temperature: do not treat the pair as independent regressors or report their correlation as an empirical finding. Note also that the water sensor is at the waterline and the air sensor is not — the air–sea difference is a contrast between two unspecified heights, not a gradient at a defined level.

**Significant wave height.** This is the mean of the highest third of waves, not the mean wave height. It therefore does **not** pair with average wave period as two summaries of the same population — one describes the top third, the other describes all waves. Significant wave heights may be compared and differenced. They may be averaged only over disjoint windows, and the result is a mean of a derived statistic, not the significant height of the longer period. Because wave energy scales with the square of height, the mean of heights is not proportional to the mean energy; square first if energy is what you want. Wave heights may not be summed.

**Wave periods.** Dominant and average period may be compared, differenced and averaged over disjoint windows; they may not be summed. The two are different quantities and must not be pooled into one distribution.

**Visibility.** Buoy sensors saturate at 1.6 nautical miles, and the sensor is mostly absent from buoys entirely. Values from such platforms are therefore **right-censored**, and the record does not say which platform it came from. A mean of visibility across a mixed platform population is biased low and is not interpretable. Restrict visibility analysis to platforms whose type and sensor range you have established externally, and treat the ceiling as censoring, not as an observation of "1.6".

**Tide.** Water level is referenced to Mean Lower Low Water, which is a **station-specific vertical datum**. Absolute tide values from different stations are therefore not comparable and must never be differenced or averaged across stations — the difference would be dominated by the datum offset, not by water level. Within one station, differences, averages and trends are valid. It is also the only quantity in feet, alongside visibility in nautical miles and everything else metric; convert before any joint computation.

**Absence.** Only the identifier, position and timestamp are guaranteed. Every measurement is optional, and the example record omits visibility and tide entirely. Absence means "not reported"; it must never be imputed as zero, and denominators in any aggregate must count present values, not records.

# 4. Time

The timestamp is the phenomenon time — the time of the thing observed, not the time it was processed or published — and it carries an explicit UTC offset. Positions on the axis are therefore absolute instants with no local-time or daylight-saving ambiguity; ordering, differencing and joining across stations are unproblematic. Mapping to a station's *civil* time requires that station's political time zone, which is not in the record and cannot be reliably derived from coordinates alone, so any "local hour of day" analysis needs external input.

The essential subtlety: the timestamp is the **end** of every interval-valued quantity in the record, not the middle and not the start. A record stamped 11:50 UTC reports temperatures and pressure *at* 11:50, wave conditions over 11:30–11:50, wind over a short window ending at 11:50, and a pressure change over 08:50–11:50. When aligning this feed with model output, satellite passes, or another sensor stream, the instantaneous quantities align on the instant but the interval quantities must be aligned on their windows. Assigning a 20-minute significant wave height to the instant 11:50 introduces a systematic ten-minute lag against anything centred on its window.

The declared cadence is a fixed five-minute period, which sets the expected slot grid. It describes the refresh rate of the upstream composite; it is a producer expectation, not a delivery guarantee, and gaps should be expected. There is no result time or publication time anywhere in the record, so **observation latency is not determined** and cannot be measured from this feed. Nor is there any indication of whether a record for a given station and timestamp may later be revised.

# 5. Ambiguities

- **Wind averaging window length.** Eight minutes or two minutes depending on platform type, and the platform type is not carried in the record. The files explicitly decline to fix it. *I am declining to decide this.* It must come from station metadata, and until it does, wind speed, gust and wind direction are not safely comparable across stations.

- **Gust peak interval.** Stated as "5-second or 8-second"; which applies to any given record is not determined. *Declining to decide.*

- **Wave direction convention.** Wind direction is explicitly the direction the wind comes *from*. The wave direction's sense is never stated. This matters: get it backwards and every wind–wave alignment result inverts. *Guess:* it follows the same meteorological "coming from" convention as the wind field, since both are in degrees true and the feed originates from a meteorological producer. **Marked as a guess** — verify before using it.

- **Sensor heights.** Anemometer height above water is not carried, and wind speeds are not stated to be normalised to a standard reference height. Cross-platform wind comparison and any drag/flux calculation therefore rest on an unstated assumption. *Declining to decide;* treat cross-station wind magnitude comparisons as approximate.

- **Platform type per record.** Buoy versus C-MAN versus partner platform is undetermined, which is what makes the wind window, the visibility censoring, and the presence of tide unresolvable from the record alone. *Declining to decide.*

- **Meaning of a missing member.** Sensor not fitted, sensor failed, value failed quality control, or transmission gap — these are indistinguishable. *Declining to decide.* Treat all as unknown rather than assigning any of them.

- **Quality control status.** No flags, no confidence, no version. Whether values have been screened at all is not determined. *Declining to decide.*

- **Platform mobility.** Whether reported position is fixed, drifts within a mooring watch circle, or can change materially is not stated. *Guess:* these are moored or fixed installations and position is effectively constant per station. **Marked as a guess** — check by inspecting position variance per identifier before relying on it.

- **Whether every station truly reports every five minutes.** The cadence is declared as fixed at five minutes, yet the example timestamp falls on a ten-minute boundary. Whether each station genuinely produces a distinct observation per five-minute slot, or whether the five minutes is only the refresh rate of the upstream file with stations reporting less often and values repeating, is not resolved. *Declining to decide* — this must be established empirically from the data, and it directly determines whether consecutive records carry new information.

- **Tidal datum epoch.** Mean Lower Low Water is defined against a specific tidal epoch, which is not given, and no station-to-station datum relationship is provided. *Declining to decide.* This reinforces that tide is a within-station quantity only.

- **The catalogue reference for the overall observed property** cannot be resolved without network access, so whatever additional semantics it carries are unavailable. *Declining to decide* what it adds.
