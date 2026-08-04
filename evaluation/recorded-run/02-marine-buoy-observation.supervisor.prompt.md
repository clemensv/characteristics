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


TRANSCRIPT B

# 1. What this feed is

Each record is one dispatch from one fixed observing platform — a moored buoy, a
C-MAN station, or a partner platform — reporting the state of the sea and air
around it. `station_id` is the subject of the observation (`featureOfInterest`),
and every result in the record is about the surroundings of that platform and
nothing else. The platform's position is carried per record and is bound to
EPSG:4326 with the axes in the order that definition fixes: latitude first, then
longitude. Anything downstream that expects GeoJSON or CRS84 ordering must swap
them; nothing in the numbers themselves reveals the error.

The important thing about the record is not what it contains but that it is not a
snapshot. It reports one timestamp and three different kinds of temporal support
under it. Six members are instantaneous. Four wave members characterise the
twenty minutes ending at the timestamp. Pressure tendency characterises the three
hours ending at it. Three wind members characterise an interval whose length the
record does not carry at all. So a single record spans at least three hours of
phenomenon time, and treating the timestamp as the time of the whole record is
the first mistake available.

Only `station_id`, the two coordinates, and `timestamp` are required. Every
measurement is optional, and its absence is undeclared — not zero, not missing at
random. The instance omits visibility and tide, and the schema's own prose
explains why: those sensors are largely confined to particular platform types.
Missingness in this feed is therefore structured by platform capability, which
biases anything pooled naively across stations.

Two things the record does not carry are worth naming up front, because their
absence is easy to read as reassurance. There is no procedure or instrument
identifier anywhere, so the measuring arrangement behind any value is undeclared
and may not be inferred. There is no quality flag and no record status, so every
value arrives unqualified; absence of a quality declaration does not mean the
value passed anything.

Finally, the observed-property references on the individual results are QUDT
quantity kinds — Angle, Speed, Length, Period, Pressure, Temperature. These
classify; they do not identify a phenomenon. Wave height, visibility, and tide
all carry `Length`. Wind speed and gust both carry `Speed`. The two wave periods
both carry `Period`. Air and water temperature both carry `Temperature`. Any join
or grouping keyed on the declared observed property will conflate quantities that
must never be combined. Sameness of phenomenon in this feed rests on the member
position and its prose, not on the annotation.

# 2. Analytics

**Per-station time series of the instantaneous quantities.** Pressure, air
temperature, water temperature, and dewpoint all apply at the timestamp, at a
declared five-minute cadence, for a fixed subject. This is the one clean,
regularly sampled series the feed offers, and it supports trend, diurnal cycle,
and event detection directly.

**Air–sea temperature difference.** Both temperatures are instantaneous, share a
unit, share a timestamp, and share a feature, so their difference is well formed
within a single record without any alignment work. (No sensor height or depth is
carried, so the difference is between two unstated levels — see §5.)

**Dewpoint depression.** `air_temperature − dewpoint` is well formed for the same
reasons. Note that dewpoint was computed from air temperature and a humidity
channel the record does not carry, so the two are not independent measurements
and a correlation between them is partly definitional.

**Frontal and storm-passage detection from pressure tendency.** The three-hour
signed pressure change is supplied ready-made, with its sign convention stated
(negative falling, positive rising) and its window declared. It is directly
usable and must not be re-derived or accumulated (§3).

**Sea-state characterisation within a record.** The four wave members —
significant height, dominant period, average period, and mean direction — share
exactly the same twenty-minute window anchored at exactly the same instant. That
shared support is declared, not assumed, which makes derived sea-state indices
combining them internally consistent within one record. This is the strongest
combination licence the schema grants.

**Gust factor.** The schema states that the gust is the peak within the same
averaging window that produced the mean wind speed. Their ratio is therefore well
defined inside a record even though the window's length is unknown. It is
comparable across records only where the window length is the same, which the
record does not establish (§5).

**Spatial fields of the instantaneous quantities.** Position is machine-resolvable
against a named CRS, so gridding or interpolating sea-level pressure and the two
temperatures across stations at a common timestamp is supported. Pressure in
particular is reduced to sea level, which is what makes station-to-station
comparison meaningful at all. Wind statistics, tide, and visibility do not support
this (§3).

**Wave climate at a station.** Wave height and the two periods share a fixed
twenty-minute support that does not vary by platform type, so unlike the wind
members they are comparable across stations on support grounds. Distributions,
exceedance statistics, and inter-station comparison are supported subject to the
undeclared procedure.

**Wind–wave relationship, with a caveat.** Both are present, but they do not share
support: the wave window is twenty minutes and fixed, the wind window is short and
unknown. Any correlation is between quantities integrated over different and
partly non-overlapping stretches of time, and that mismatch must be carried
through the analysis rather than assumed away.

**Availability and gap analysis.** The declared five-minute cadence makes an
absent slot detectable as a gap. That is a legitimate consumer decision about
windowing and staleness. It does not license filling the gap, and it does not
assert that a record exists for every slot.

# 3. Combination rules

The gates that apply throughout: two values are like quantities only if they are
the same phenomenon, in a compatible unit, produced by the same summary function
where one applies, and over compatible temporal support. Different statistics of
one phenomenon are not like quantities. The procedure is undeclared for every
value here, so every cross-station combination below carries an undeclared
procedure difference that the data cannot expose.

**`station_id`** — not a quantity. Equality of `station_id` is the only grouping
key the schema licenses. Do not group by coordinate proximity.

**`latitude` / `longitude`** — a coordinate pair in EPSG:4326, latitude first.
Comparable only in that order. Degrees are angles, not distances: differencing
them does not yield a separation, which requires a geodetic computation on the
named CRS. Averaging positions across records of one station describes where the
platform sat; averaging across stations produces a centroid that is the location
of nothing. These members carry no `phenomenonTimeRelation`, so whether the
position applies at the timestamp is undeclared, and movement between consecutive
records must not be read as measured drift.

**`timestamp`** — comparable and orderable directly; differences are elapsed civil
time. Not summable or averageable as a quantity.

**`wind_direction`** — a circular quantity in degrees. Comparable within a station.
Differences must be taken modulo a full turn; a naive subtraction is wrong across
the north crossing. Never sum. Never average arithmetically — the arithmetic mean
of directions straddling north is meaningless, and even a proper circular mean
would be a mean of means over windows of unknown length. **Not combinable across
stations of different type**, because the averaging window differs by platform
type and the record does not say which it is. The reference direction is true
north by prose only; no frame is bound.

**`wind_speed`** — a mean over an interval whose length the schema deliberately
leaves indeterminate. Comparable and differenceable within one station.
**Must not be compared or pooled across stations without first establishing, from
station metadata outside this feed, that the two averaging windows are the same
length.** A two-minute mean and an eight-minute mean of the same wind are not the
same quantity. Never sum — a mean is not additive. Averaging consecutive records
is not a mean wind over the covering period: at a five-minute cadence an
eight-minute window overlaps its predecessor, so the values are not independent,
and a two-minute window leaves three minutes of every five unobserved.

**`gust`** — a maximum over that same unknown window. The maximum across a set of
records is a valid maximum over the union of their windows, provided you accept
that the union may have gaps. The mean of a set of gusts is a statistic of maxima
and is not a property of the wind; it may be computed but must be labelled as
what it is. Never sum. Gust and `wind_speed` are different statistics and are not
comparable as like quantities; their difference or ratio within one record is
nonetheless well formed, because the schema states they share a window and a unit.

**`wave_height`** — a mean of the highest third of the waves over twenty minutes.
Comparable, differenceable, and pooled across stations, since the support is fixed
and platform-independent. **Never sum**: the relation is `interval`, not
`accumulation`, and nothing here is additive. Averaging consecutive records
double-counts heavily — at a five-minute cadence, adjacent twenty-minute windows
share fifteen minutes — so an independent series requires subsampling to at least
twenty-minute spacing. Critically, **do not treat `wave_height` and
`average_wave_period` as comparable because they share derivation, statistic, and
support**: they are means over different populations (the highest third of wave
heights; all wave periods) and of different quantities. That distinction lives in
prose; the annotations alone do not carry it.

**`dominant_wave_period`** — read off a computed spectrum, not summarised from
readings. Comparable and differenceable across records and stations, sharing the
twenty-minute support. Never sum. It may be averaged arithmetically, but the mean
of a set of spectral peaks is not the peak of any mean spectrum, and the same
overlap caveat applies. Not a like quantity with `average_wave_period` despite the
shared unit, shared quantity kind, and shared window.

**`average_wave_period`** — mean of all wave periods over the same twenty minutes.
Same overlap caveat, same prohibition on summing.

**`mean_wave_direction`** — circular, and calculated from the spectrum at the
dominant frequency band only. All the circular rules for `wind_direction` apply.
Never sum, never average arithmetically. It describes the energy at the dominant
period, so pairing it with `average_wave_period`, which covers all waves, mixes
populations.

**`pressure`** — instantaneous, and already reduced to sea level, which is
precisely what makes it comparable and differenceable across stations and what
supports horizontal gradient analysis. Averaging over time within a station is
sound. Never sum. The reduction depends on a station elevation the record does not
carry, so a station with a wrong elevation carries a bias this feed cannot reveal,
and station pressure cannot be recovered.

**`air_temperature` / `water_temperature`** — instantaneous, measured, same unit.
Compare, difference, and average over time within a station freely. Cross-station
comparison is supported in principle but no measurement height or depth is
declared for either. Never sum. Do not average the two together; they are
different phenomena sharing a quantity kind.

**`dewpoint`** — instantaneous, calculated. Compare, difference, average over time.
Never sum. The formula is not machine-declared, so the humidity it came from may
not be reconstructed exactly.

**`pressure_tendency`** — already a difference over the three hours ending at the
timestamp. Comparable and differenceable across stations (fixed support, common
unit). **Never difference it again.** It may be summed only over a strictly
non-overlapping, contiguous, gap-free chain of three-hour steps, in which case the
sum telescopes to the net change; at a five-minute cadence that means taking every
thirty-sixth record. Summing consecutive records inflates the true change by
roughly a factor of thirty-six. Averaging consecutive records averages
overwhelmingly overlapping windows and yields a smoothed artefact, not a tendency.
It is not the derivative of the `pressure` member in this feed: that one is an
instantaneous value and the tendency was formed by the producer from its own pair
of readings, so cross-checking the two is a legitimate diagnostic but exact
agreement is not implied.

**`visibility`** — instantaneous, in nautical miles, from a sensor the schema says
ranges only to 1.6 nmi. The values are therefore right-censored at the top.
Treat 1.6 as a bound, not a measurement; means and variances computed over
censored values are biased. Comparable across stations only where the sensors
share that range, which the record does not state. Never sum.

**`tide`** — instantaneous, in feet, relative to Mean Lower Low Water. **No
vertical reference system is bound to this member.** A height means nothing
without a declared zero, and the schema names the datum in prose only, so what the
zero is — and whether two stations share one — is not established. **Compare,
difference, and average `tide` only within one station.** Do not compare,
difference, or average it across stations, and never sum it. (General knowledge,
not established by these files: MLLW is conventionally realised per station from
local tidal observations, which would make cross-station comparison actively wrong
rather than merely unsupported.)

**Across quantity kinds** — `wave_height`, `visibility`, and `tide` all declare
QUDT `Length`, in metres, nautical miles, and feet respectively, and describe three
unrelated phenomena. A shared quantity kind is a classification and never a licence
to combine. The same warning applies to the two `Speed` members, the two `Period`
members, and the two `Temperature` members.

# 4. Time

`timestamp` establishes the time axis. It carries the phenomenon-time role, so it
places the observed conditions rather than the record's publication or handling.

It is a plain Core `datetime` with no temporal reference system declared, which
means Core semantics are fully intended; the description states UTC and the
instance carries a `Z` offset. Positions on this axis therefore map onto civil UTC
directly — no epoch, no conversion, no local time, no reference-system lookup. The
value is built from year, month, day, hour, and minute fields, so the axis is
resolved to the minute and carries no sub-minute placement.

The axis is expected to advance in five-minute steps. That expectation describes
the producer, not the data: a record whose spacing departs from it is late, not
invalid; a missing slot is a detectable gap and nothing more; and the cadence
neither guarantees that a next record exists nor bounds any phenomenon time.

How results sit on the axis differs by member, and this is the part that governs
correct use. For the six instantaneous members the timestamp is the instant the
value applies. For every interval member the timestamp is the *closing* boundary:
the record carries no separate period boundaries, so `timestamp` anchors them all,
and each interval runs backwards from it, half-open. The wave quartet covers
[t − 20 min, t). Pressure tendency covers [t − 3 h, t). The three wind members
cover [t − L, t) for a length L that this feed does not carry and that must be
obtained from station metadata. Those three declare an interval relation with an
indeterminate extent — which is a deliberate, well-formed statement, not an
omission, and it must not be read as meaning the values are instantaneous.

Two consequences follow. First, the periods overlap one another inside a single
record and are not the same period, so a consumer that attributes all of a
record's content to its timestamp attributes three hours of pressure change to an
instant. Second, joining this feed to another on timestamp equality aligns the
instantaneous members and silently misaligns everything else unless the other
feed's support matches.

There is no result time, no ingestion time, and no effective time. The delay
between an observation applying and the record becoming available is therefore not
determinable from the data, and neither is any period for which a record is
intended to be acted on.

# 5. Ambiguities

**The wind averaging window length.** *Declining to decide.* The schema states
explicitly that the length follows the station type, that the record does not
carry the station type, and that the extent must be obtained from station
metadata. This is the single most consequential open item in the feed, and it is
open by design rather than by oversight.

**Which platform type any given record came from.** *Declining to decide.* Nothing
in the record declares it. One could try to read it off the shape of
`station_id` — the description offers a numeric example for a deep-ocean buoy and
an alphanumeric one for a C-MAN station — but the schema states no rule, two
examples are not a specification, and inferring semantics from the form of sample
values is exactly what should not be done here. If anyone does it anyway, it is a
guess and must be labelled one.

**Whether a station possesses a wave, visibility, or tide sensor.** *Declining to
decide.* All these members are optional and absence is undeclared. No capability
annotation exists, and presence or absence across a run of records is evidence
about the feed, not a declaration.

**The instrument or procedure behind any value.** *Declining to decide.* No
procedure is identified anywhere. This is comparability-critical and may not be
inferred from station identity, position, or the values themselves.

**The quality or verification state of any value.** *Declining to decide.* There is
no quality qualifier and no record status. Absence of these does not mean the data
are good, screened, or final, and nothing indicates whether records are ever
revised, superseded, or duplicated.

**Sensor heights and depths.** *Declining to decide.* No height is carried for the
anemometer or the air temperature sensor and no depth for the water temperature
sensor. *Assumption, from general knowledge rather than these files:* wind speed
varies substantially with measurement height, so cross-station wind comparison
carries an unquantified bias even when the averaging windows match.

**The tide datum and its sign convention.** *Declining to decide* on the datum: no
vertical reference system is bound, the realisation of MLLW is not identified, and
whether two stations share a zero is not established. *Guessing* on the sign: the
phrase "above or below" with "above" stated first suggests positive is up, but no
annotation establishes an axis direction, and this is a guess.

**The direction reference and encoding for the two direction members.** *Declining
to decide.* "Degrees true" appears in prose only; no reference frame is bound. The
admissible range, the treatment of the 0/360 boundary, and how a calm or an absent
direction is encoded are all undetermined.

**The circular-averaging convention used to produce `wind_direction`, and the
spectral method behind `wave_height`, `dominant_wave_period`, and
`mean_wave_direction`.** *Declining to decide.* The schema names the summary
function and the fact of a spectral computation but no method, and a method must
not be read out of a description. None of these values may be recomputed or
verified from the record.

**Whether the gust peak interval is five seconds or eight.** *Declining to decide.*
The description offers both and the record does not distinguish them.

**How missing measurements are encoded on the wire.** *Declining to decide.* The
instance omits two members, which is consistent with omission being the mechanism,
but one example does not establish it, and nothing rules out sentinel values
appearing in some deliveries.

**Whether the three-hour tendency window was actually complete.** *Declining to
decide.* The declared support states the extent of the period, not that readings
existed at both ends of it, and no quality annotation would reveal a partial one.

**The record-level observed property and every QUDT reference.** *Declining to
decide.* The catalogue behind `marine-surface-conditions` is not a real one and
none of these references is required to resolve. Unresolved is indeterminate, not
incorrect — but no equivalence, and no permission to combine, may be read from
them. In particular, the record-level property is overridden on every result
member, so it governs nothing in practice.

**Whether one record per station per five-minute slot is guaranteed.** *Declining
to decide.* The declared cadence is an expectation about a producer and asserts
neither completeness nor ordering nor the existence of a successor.


TRANSCRIPT C

# 1. What this feed is

Each record is a single timestamped snapshot from a fixed-identity marine
observing station: an identifier, a geographic position, an instant, and then a
mixed bag of surface meteorology (wind vector, gust, barometric pressure and its
tendency, air temperature, dewpoint, visibility) and sea state (wave height, two
wave periods, mean wave direction, water temperature, tide). Only the
identifier, position and time are guaranteed present. **Every measured quantity
is optional**, which means the feed is sparse by construction and the sparsity
carries information: the example record omits visibility and tide entirely, and
nothing in the data distinguishes "this station has no such sensor" from "the
sensor failed this cycle" from "the value was suppressed by quality control."
An analyst who treats absence as zero, or who back-fills it, will manufacture
signal.

The position travels *inside every record*, not alongside the station identity.
That is a deliberate shape and should be read as such: you may not assume that a
given `station_id` maps to one fixed coordinate pair. A moored buoy swings
around its anchor and can be re-deployed; the data model permits the position to
change from record to record and nothing constrains it not to. Join on identity
if you want a time series; join on position only if you have first checked
whether position is actually stable for that identity in your window.

The coordinates in the example put the station in the open western North
Atlantic — but that reading assumes the conventional sign and ordering of
latitude/longitude, which the files do not state (see §5).

# 2. Analytics

**Per-station time series and trend detection.** The identifier plus a
monotonic-comparable instant is the whole basis for this, and it is the analysis
the feed most directly supports. Pressure, temperature, wave height and wind
speed are all repeated scalar observations at one place, so run-length,
persistence, rate-of-change and threshold-crossing analyses are all sound
*within* one station.

**Gustiness.** `gust` divided by `wind_speed` is a dimensionless ratio. This is
the single most robust derived quantity in the feed, because it survives the
fact that the wind unit is never stated — the ratio is the same in knots, m/s or
mph. It is a usable turbulence/stability proxy and it is comparable across
stations even when nothing else is.

**Spectral narrowness of the sea state.** `dominant_wave_period` divided by
`average_wave_period` is likewise unit-free. A ratio near 1 indicates a narrow,
single-source sea; a large ratio indicates a mixed sea with swell arriving
separately from the locally generated wind waves. This is available without
knowing whether periods are in seconds.

**Air–sea temperature difference and dewpoint depression.** Both are
scientifically valuable (the first is a boundary-layer stability proxy, the
second a saturation/fog proxy). Both are *conditional*: they are only meaningful
if the two temperatures involved share a scale, and the files do not establish
that they do (see §3).

**Wind-driven versus swell-driven sea.** Comparing `wind_direction` to
`mean_wave_direction`, and `wind_speed` to `wave_height`, separates locally
generated wind sea from remotely generated swell. This is a genuinely useful
analysis but it is gated on a directional convention the files do not supply —
performing it naively is the most likely way to get a confidently wrong answer
from this feed.

**Cross-validating the reported tendency.** `pressure_tendency` is a change,
while `pressure` is a level. Differencing successive `pressure` values gives an
independent estimate of the same thing, which is a good data-quality check —
*provided* your differencing interval matches the (unstated) interval the
reported tendency is computed over. If they differ, the two will disagree
systematically and the disagreement means nothing.

**Availability and outage analysis.** Because members are optional, you can
profile sensor uptime per station per member over time. This is real and useful
and requires no unit knowledge at all.

**What the feed does not support well:** cross-station comparison of absolute
wind speed. Anemometer height is not carried, and wind speed is strongly
height-dependent, so two stations' wind speeds are not on the same footing
unless you know their sensor heights from outside this feed. Likewise extreme
value analysis is weakly supported, because there are no quality-control flags
— an outlier and a genuine extreme look identical here.

# 3. Combination rules

**`station_id`** is nominal. Group and join on it. Never order, difference or
average it, and do not infer proximity from numeric adjacency of identifiers.

**`latitude` / `longitude`** are angular coordinates on a sphere, not free
scalars. Within one station they may be averaged to estimate a mean mooring
position and differenced to measure watch-circle excursion. Across widely
separated stations a plain arithmetic mean is not a location. Longitude wraps at
the antimeridian; any differencing must be done modulo 360 or it will produce
errors of that magnitude for stations straddling the wrap.

**`wind_direction`, `mean_wave_direction`** are circular. They may be compared
only after reducing the difference to the shorter arc; they must **never** be
summed or arithmetically averaged. The mean of 350 and 10 is 180 under naive
arithmetic and 0 in reality. Vector-average (mean of unit vectors), or do not
average at all. Additionally, comparing `wind_direction` to
`mean_wave_direction` is only valid if both use the same convention (direction
*from* versus direction *toward*, and true versus magnetic north). The files
establish neither, and the two members could legitimately differ in convention.
Under one reading the example is a wind and sea in near-alignment; under the
other they are nearly opposed. **Do not difference these two members until the
convention is established externally.**

**`wind_speed`, `gust`** are non-negative magnitudes on a ratio scale. Within a
station they may be compared, differenced, averaged and ratioed. `gust` is a
*peak* statistic and `wind_speed` is a *mean* statistic; they are not
interchangeable and must not be pooled into a single "wind" series. Averaging
gusts produces a mean-of-maxima, which is not the maximum and not the mean —
label it as such or it will be misread. Cross-station combination is blocked by
the missing sensor height and by the missing averaging window.

**`wave_height`** may be compared, differenced and averaged within a station.
Note that a mean of wave heights is not the wave height of the mean sea state;
wave energy goes as the square, so if you want an energy-weighted aggregate you
must average the square and take the root, not average the height.

**`dominant_wave_period`, `average_wave_period`** are two different statistics
of the same underlying spectrum and **must not be combined with each other, nor
pooled into one series.** Each may be averaged within its own kind, but note
that period is a reciprocal quantity: the mean of periods is not the reciprocal
of the mean frequency. For physics that is frequency-linear, convert, average,
convert back.

**`pressure`** may be compared, differenced and averaged within a station.
Across stations it may be compared only if all values are reduced to a common
reference (typically sea level); the files do not say whether they are, and for
a marine surface station the distinction is smaller than for land stations but
not necessarily zero.

**`pressure_tendency`** is already a difference. It must **never** be added to
or differenced against `pressure` — they are not the same kind of quantity.
Tendencies may be averaged across records only if every record's tendency covers
the same window length, which the files do not guarantee. Tendencies over
adjacent, non-overlapping windows may be summed to give the total change; over
overlapping windows they may not, and nothing here tells you which case you are
in.

**`air_temperature`, `water_temperature`, `dewpoint`** are on an interval scale.
Differences are meaningful; sums are not; averages are meaningful only for
values on the same scale. Ratios are meaningless (a 20-degree reading is not
"twice as warm" as 10). Crucially, the files do not state that these three share
a unit — nothing prevents one being Celsius and another Fahrenheit — so
`air_temperature − water_temperature` and `air_temperature − dewpoint`, both
standard and valuable derivations, are **conditional on an assumption you must
make explicit and verify externally.** The example values are mutually plausible
on a single Celsius scale, but three plausible numbers do not establish a
convention.

**`visibility`** is a non-negative magnitude, comparable and differenceable, but
it is typically censored at a sensor maximum, and this feed carries no indicator
of censoring. Averaging censored values biases low.

**`tide`** is a signed displacement relative to a datum that the files do not
identify. Differences of tide *at the same station* are meaningful (change in
water level). Comparing or averaging tide *across* stations is meaningless
unless they share a datum, and nothing here says they do. Tide must not be
combined with `wave_height`, which measures a different thing about the same
water surface.

**Universally:** because no member carries a unit, any combination of two
different members into a physical formula (wave steepness, wind stress, relative
humidity, air density) is unsound from these files alone. Only unit-free
constructions — ratios of like to like — are safe.

# 4. Time

`timestamp` is the sole member establishing the time axis, and it is required,
so every record has a position on that axis. It is a date-and-time type, and the
example carries an explicit `Z` offset, which pins that value to UTC and
therefore to civil time anywhere via the ordinary offset rules. Ordering,
differencing and windowing across records are sound wherever the offset is
present.

Two cautions on the axis itself.

First, **what the timestamp denotes with respect to the measurement is not
determined.** Several of the members are unavoidably aggregates over an
interval: mean wind speed, mean wave period, mean wave direction and wave height
are all statistics over a sampling window, and `pressure_tendency` is explicitly
a change over some prior window. The record gives one instant and no window
boundaries. Whether the instant is the start, midpoint or end of the sampling
window is left open, and the answer shifts every derived rate by up to the
window length. When correlating this feed against another time series — radar,
satellite, model output — that offset is the dominant alignment error and you
cannot resolve it from these files.

Second, **the tendency's window is a second, invisible time axis.** It is
implied by a member but never represented, so it cannot be read, checked or
harmonised across stations from within the data.

There is no ingest or record-creation time, and no sequence or version member.
Consequently late-arriving, duplicated or corrected observations for the same
station and instant are indistinguishable from one another. If you deduplicate
on `(station_id, timestamp)` — which appears to be the natural key — you will
silently pick one of a duplicate pair with no basis for preferring either.

# 5. Ambiguities

**Units of every measured quantity — not determined; I decline to decide.** No
member carries a unit and neither file states one. Wind speed could be m/s,
knots, km/h or mph; pressure could be hPa/mbar, inHg or kPa; temperatures could
be Celsius or Fahrenheit; wave height metres or feet; periods seconds; distances
and tide any length unit. The example values are individually plausible under a
common metric reading, but plausibility is not specification, and this is
precisely the class of assumption that produces confident, silent, order-of-
magnitude errors. Resolve it from the feed's documentation before computing any
cross-member physical quantity.

**Whether all temperature members share one scale — not determined; I decline to
decide.** Even granting a metric reading overall, nothing forbids mixed scales
across the three temperature members.

**Directional convention (from/toward, true/magnetic) for wind and waves — not
determined; I decline to decide.** This is the highest-consequence gap in the
feed, because both readings yield a coherent-looking answer and the two answers
are 180° apart.

**Angular unit for directions — guess:** degrees rather than radians. Marked as
a guess; the values 212.0 and 205.0 exceed 2π, which rules out radians for these
particular values, so the guess is well-supported but is still an inference from
one record rather than a stated fact.

**Coordinate reference system and datum for position — not determined; I decline
to decide.** No CRS is named. A modern global datum is likely, but at the metre
scale the choice matters and cannot be read off.

**Sign convention for longitude — guess:** negative is west of the prime
meridian, and the ordering is the conventional one. Marked as a guess; the
single negative longitude in the example is consistent with it but does not
establish it.

**Vertical datum for `tide` — not determined; I decline to decide.** Sign,
zero-point and reference surface are all unstated, so absolute tide values are
uninterpretable and only within-station differences are usable.

**Sampling/averaging window for wind, waves and gust; gust duration — not
determined; I decline to decide.**

**Window length for `pressure_tendency` — not determined; I decline to decide.**
A three-hour convention is common in surface meteorology, but adopting it here
would be an unsupported import from outside these files.

**Sensor heights (anemometer, thermometer) and water-temperature measurement
depth — not determined; I decline to decide.** These block cross-station
comparison of wind and, to a lesser degree, temperature.

**Meaning of an absent member — not determined; I decline to decide.** No
sensor, transient failure, failed quality control and value-not-applicable are
all collapsed into the same absence.

**Whether `(station_id, timestamp)` is unique — guess:** it is the intended key.
Marked as a guess; nothing in the files declares a key or forbids duplicates.

**Whether position is constant per station — not determined.** The model permits
it to vary and gives no way to tell drift from redeployment from a correction.

**Nominal reporting cadence — not determined.** Only one record is available, so
no interval can be inferred. Gap detection therefore requires an externally
supplied expected cadence.

**Value ranges and quality control — not determined.** No bounds are declared,
no quality flags exist, and no member marks a value as estimated, interpolated
or suspect. Outliers and genuine extremes are indistinguishable from within the
feed.

**Whether the identifier in the example belongs to a known station network —
guess, and I decline to rely on it.** The identifier's form and the coordinates
are suggestive, but treating a recognised-looking identifier as authoritative
would be exactly the kind of external fact the files do not establish.


TRANSCRIPT D

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
