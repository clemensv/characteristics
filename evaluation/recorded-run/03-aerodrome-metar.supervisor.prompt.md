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

# 1. What this feed is

Each record is one decoded surface weather observation taken at a named aerodrome and identified by its ICAO location indicator. A record carries the atmospheric state at a single reported instant — temperature, dewpoint, wind, visibility, cloud layers, two pressure values, a coded present-weather field and a flight-category label — alongside fixed station metadata (position, elevation, name) and the original coded text of the observation.

The decisive structural fact for an analyst is that the record is a **derived** view of a text bulletin that is itself carried in the record. In the example, the coded text reports the altimeter setting as `A2999` (29.99 inches of mercury) while the structured member reports `1015.6`; that is 29.99 inHg converted to hectopascals. Likewise the coded body reports whole-degree temperatures (`26/22`) while the structured members carry tenths (`26.1`, `22.2`) taken from the remarks group `T02610222`. So the structured members are the output of a decoder that reformats, converts units, and prefers higher-precision remark groups when they exist. Everything downstream inherits that decoder's behaviour, and the schema documents none of it.

The second decisive fact is what is *absent*: the schema declares types only. There is no unit, no measurement scale, no reference datum, no value domain for any coded member, and no description of what a null means. Every unit statement below is inferred from one example record and the coded text inside it — not established by the schema.

# 2. Analytics

**Station climatology of temperature and dewpoint.** Each record pins a temperature and a dewpoint to a precise instant at a fixed, known location, so per-station distributions, diurnal cycles and seasonal cycles are all recoverable. This is the best-supported analysis in the feed. Two conditions apply: you must convert to local time before doing anything diurnal (§4), and you must handle the mixed routine/special reporting cadence (below).

**Dewpoint depression and humidity-driven phenomena.** Temperature and dewpoint are measured at the same instant and appear in the same record, so their difference is meaningful without any joining or interpolation. Fog and low-ceiling onset analysis, saturation timing, and cooling-to-saturation forecasts are all supported at record level.

**Wind climatology per aerodrome.** Direction, sustained speed and gust give a wind rose and a gust-factor distribution per station. Runway-alignment and crosswind work is *not* fully supported: it needs runway headings, which are not in the feed, and it needs the direction reference frame resolved (§5).

**Synoptic pressure fields and pressure tendency.** Sea-level pressure with a station position supports spatial interpolation across stations at a common time, and per-station differencing supports pressure tendency. The altimeter setting does not substitute for this (§3).

**Feed health and latency.** The gap between the observation instant and the report instant is directly measurable per record (two minutes in the example). Distributions of that gap by station, and per-station reporting completeness against the expected routine cadence, are supported and are worth running before any scientific analysis, because gaps in the observation series are the main source of silent bias.

**Weather-activity proxy from report type.** The routine/special distinction is itself a signal: special reports are emitted when conditions change through defined thresholds, so their rate per station per hour is a proxy for weather variability. This is only usable if the report-type member is populated, and it is nullable.

**Decoder-fidelity QC.** Because the original coded text accompanies every record, every derived member can be independently re-derived from the raw text and compared. Very few feeds permit this. It is worth doing systematically: it detects unit-conversion drift, silent precision changes (whole degrees vs. tenths), and members that were dropped rather than decoded. In the example record every derived member reconciles with the raw text.

**Flight-category work — with a caveat.** The flight category is a deterministic function of visibility and ceiling, both of which are also present. It therefore carries no independent information. Use it as a convenience label or as a QC target (recompute and compare), but never as a predictor alongside the visibility and cloud members — it is collinear with them by construction.

**What the feed does not support: areal averaging.** Aerodromes are sited where aviation needs them, not on a sampling grid. Averaging across stations produces a mean over an aviation-infrastructure-weighted sample, not over an area. Any "regional temperature" computed by pooling stations is an artefact.

**A cadence trap that affects every time aggregation.** The stream mixes routine observations at a fixed cadence with event-triggered special observations. Specials cluster during deteriorating weather. A naive mean over records therefore oversamples bad weather and biases temperature, visibility and ceiling statistics. Either filter to routine reports, or resample to a fixed grid, or weight by the interval each record represents. Do not take a simple mean over rows.

# 3. Combination rules

**Temperature, dewpoint.** Same scale, same instant, same instrument site. Compare freely; difference freely (the depression is the useful derived quantity); average over time at one station, or over stations, subject to the cadence caveat above. Do **not** sum them and do **not** take ratios: this is an interval scale with an arbitrary zero, so "twice as warm" is undefined and a sum has no referent. Do **not** average dewpoints and then compute a humidity from the mean — the relationship is non-linear, and the average of a humidity is not the humidity of an average. Averaging across stations is arithmetically valid but physically confounded, because station elevations differ and elevation is in the record for exactly that reason.

Also note a precision hazard when combining: the tenths in the structured members come from an optional remarks group. Records from stations that omit that group will carry whole degrees. Mixing the two changes the apparent quantisation of the series mid-stream and will show up as spurious structure in histograms and in any differencing at small lags.

**Wind direction.** This is a circular quantity. It may be compared only with a circular distance, and it must **not** be summed, differenced arithmetically, or averaged: the arithmetic mean of 350 and 010 is 180, which is the reciprocal of the correct answer. If you need a mean wind, form the vector mean using direction together with speed, and report it as a vector-mean wind — which is a different quantity from the mean of the speeds and will be smaller in magnitude whenever direction varies. Do not present the two interchangeably. Combining directions across stations additionally requires that all stations use the same reference frame, which the files do not establish (§5).

**Wind speed.** Ratio scale with a true zero: compare, difference, average, and take ratios. Do **not** sum as a proxy for run-of-wind unless the records are equally spaced in time — they are not, because of the mixed routine/special cadence. Averaging speeds across stations is arithmetically fine and physically weak, since anemometer exposure differs by site and is not described.

**Gust.** Gusts are a peak over an unstated window, and the member is present only when a gust was reported — the example's coded text contains a gust group, and there is no indication that a zero is emitted when there is none. Consequences: take the **maximum** freely; never impute zero for an absent gust; and if you take a mean gust, state that it is conditional on gusts occurring, because the underlying population is self-selected. Never merge gust and sustained speed into one "wind speed" series — they are different statistics of the same wind. The relationship gust ≥ sustained is expected but is not enforced anywhere, so check it rather than assume it.

**Visibility.** Delivered as text, and the example value `10+` is a **censored** observation: it means "at least 10", not "10". Nothing may be compared, differenced, summed or averaged until the text is parsed and the censoring is represented. Treating `10+` as the number 10 biases every mean downward and destroys the upper tail, which is precisely where most of the mass sits in fair weather. Use medians, quantiles, or survival/censored-data methods, or reduce to the categorical question you actually care about ("below threshold X or not"). Additionally, the unit is not declared in the schema; the example's coded text uses statute miles. If any producer emits metres, values from the two would be silently poolable and catastrophically wrong. Verify the unit per source before pooling across sources.

**Cloud layers.** Delivered as a string containing an embedded JSON array — a doubly-encoded value that no schema validates. Parse before use. Within a parsed layer, cover codes are categorical: count them, never average them. Layer bases are numeric and may be compared and differenced *within the same vertical reference*, but the reference is not declared. In the coded text the layer heights follow the convention of height above the aerodrome, not above sea level; if that holds, layer base and station elevation are measured from different data and **must not be added, differenced, or compared** without an explicit conversion. Ceiling — the quantity most analyses actually want — is not a member; it must be derived as the lowest broken-or-overcast layer, and that derivation is yours to define and document.

**Altimeter setting and sea-level pressure.** Both are pressures, both appear in the example in the same unit, and they differ by 0.2 in that example. They are **not the same quantity and must never be pooled, coalesced, or differenced against each other.** They are two different reductions of the same station pressure: one is the value that makes an altimeter read field elevation, computed against a standard atmosphere; the other is a reduction to sea level that accounts for the actual conditions. Their small difference is a property of the two reduction methods plus rounding, not a physical signal. Concretely: build a pressure series from one member only, and never fill gaps in one from the other. Within a single member, comparison across stations and differencing over time (pressure tendency) are both valid — that is what the sea-level reduction exists for.

**Position and elevation.** These are station metadata replicated into every record, not measurements. Never average them, and never treat their variation across records as signal. If they do vary for a given station across time, that is either a station relocation or a metadata correction; decide which before it silently moves your spatial joins.

**Flight category.** Categorical, with an implied ordering that the files do not define. Count and cross-tabulate; never average. Deterministically derivable from other members, so it adds no information to a model that already has them.

**Quality-control field.** An integer with no declared meaning and no declared value domain. It must not be summed, averaged, thresholded, or treated as ordinal. See §5.

**The two timestamps.** Their difference is meaningful and useful (message latency). They must not be averaged together, interchanged, or coalesced. See §4.

**Station identifier.** This is the grouping key for everything above; the station name is display text and is nullable, so never group by it.

# 4. Time

**The observation instant establishes the time axis of the thing described.** It is the instant the atmospheric state refers to, and it is the only member that should be used for binning, resampling, joining across stations, or plotting. The report timestamp belongs to a different axis entirely: it describes the *message*, not the atmosphere. Using it as the time axis silently shifts every observation forward by a variable, weather-dependent, station-dependent amount and will fabricate lags in any cross-station analysis. Keep it, but use it only to measure latency and feed health.

Positions on the axis are absolute instants expressed in UTC — the example carries an explicit `Z`, and the day-and-time group in the coded text (`301151Z`) corroborates it. Note that the coded text carries only a day of month; the full calendar date exists only in the structured timestamp, which is therefore authoritative for anything spanning a month boundary.

**Relation to civil time at the aerodrome is not derivable from the files.** The record gives a latitude and longitude, which yields mean solar time, not legal civil time. Time zone boundaries and daylight-saving rules are political, change over time, and cannot be computed from coordinates without an external time-zone database. Any diurnal, working-hours, or day/night analysis therefore requires an external lookup keyed on position or on the location indicator. Doing diurnal analysis in UTC across stations at different longitudes smears the diurnal cycle into noise; this is the single most common way this kind of data is analysed incorrectly.

**The instant is a label, not a duration, and the underlying quantities are not instantaneous.** Wind speed is a mean over some window, gust is a peak over some window, visibility is an assessment over some interval. None of those windows are stated anywhere in the files. So the timestamp identifies an interval of unknown width. This is harmless for hourly aggregation and matters a great deal for short-lag differencing, lead-lag correlation between stations, and anything claiming sub-hourly resolution.

**The series is irregular by design.** Routine reports arrive on a cadence, special reports arrive on events. Treat the data as an irregular event series and resample deliberately; do not assume a fixed step, and do not let a `diff` over adjacent rows stand in for a fixed-interval tendency. The example's observation minute (`:51`) is not on the hour; whether such a report is conventionally attributed to the hour it precedes is not established by the files, and if you bin by truncating to the hour you will attribute it to the preceding hour. Choose and document a binning rule rather than inheriting one from your date library.

# 5. Ambiguities

Items below are marked **[declining]** where the files do not decide the matter and I am not guessing, or **[guess]** where I am offering a reading that the files do not establish.

1. **No units are declared anywhere.** The schema carries types only, with no unit or semantic annotation vocabulary in use. Every unit in this answer is read off one example record and the coded text inside it: temperature and dewpoint in degrees Celsius, wind in knots, both pressures in hectopascals, cloud bases in feet, visibility in statute miles. **[guess]** — well-supported for this record, but a property of this record, not of the schema. A second producer could satisfy the schema with entirely different units and nothing would detect it.

2. **Elevation unit.** The value 3.4 for this aerodrome is consistent with metres and absurd as feet. **[guess]**: metres. The vertical datum for elevation is **[declining]** — not stated.

3. **Whether the altimeter member is always in hectopascals.** This record shows a conversion from the inches-of-mercury value in the coded text, so a conversion step demonstrably exists. Whether it is applied uniformly across producers, stations, and time is **[declining]** — not determined, and it is exactly the kind of thing that changes silently.

4. **Cloud base vertical reference.** **[guess]**: height above the aerodrome rather than above sea level, following the convention of the coded text. Not stated in the files. If you need absolute heights, resolve this before combining base with elevation.

5. **Wind direction reference frame — true north or magnetic north.** **[declining].** The files do not say. This does not affect a wind rose's shape but does affect any runway-relative or crosswind computation, and the error is a slowly varying function of location, so it will not look like noise.

6. **Encoding of calm and variable winds.** The direction member is a non-nullable integer, so a coded report of "variable" has no evident representation, and calm conditions may map to zero or to an omitted member. **[declining]** — not determined. Check for a spike at 0 in the direction histogram before trusting the low end.

7. **Absent gust vs. zero gust.** **[guess]**: the gust member is omitted when the coded report contains no gust group, and no zero is emitted. Not established. Verify, because the two readings give completely different gust statistics.

8. **The quality-control field.** **[declining], firmly.** An integer with no name-bearing semantics, no enumeration, no scale, and no documentation. The value 2 could be a bit mask, an ordinal confidence, a source code, or a decoder version. Do not filter on it, do not threshold it, and do not let it into a model. Carry it through and get it documented externally before using it.

9. **What null means, member by member.** Several members admit an explicit null distinct from omission, and the schema assigns no meaning to either. In the example, a null present-weather field most plausibly means "no significant weather was reported" — an *informative* absence — whereas a null station name would mean "metadata unavailable", a *missing* value. **[guess]** for that reading; **[declining]** on the general rule, because these two kinds of null demand opposite handling and the schema does not distinguish them.

10. **Record identity and duplicates.** Whether station plus observation instant is unique is **[declining]** — not stated. Corrected and amended reports are a normal feature of this kind of data and would collide on that key. The report-type member may carry the distinction, but only one value has been observed and its value domain is undeclared. Define a deduplication policy before aggregating.

11. **Value domains for every coded member.** Report type, present weather, cloud cover codes, and flight category each show at most one example value and declare no enumeration. **[declining]** on all of them. In particular the flight-category thresholds are not in the files, so a recomputed category cannot be checked against the supplied one without an external definition.

12. **Visibility text grammar.** The trailing `+` is legibly a lower bound. Whether fractional values, below-minimum markers, or metric values also occur is **[declining]** — one example does not establish a grammar. Write the parser defensively and fail loudly on unrecognised forms rather than coercing them.

13. **Cloud string inner grammar.** Two keys are visible in one example. Whether a base may be null for clear skies, whether vertical-visibility layers appear, and what the full cover-code set is are all **[declining]**. Nothing validates the inner content, so malformed entries will reach your parser intact.

14. **Averaging windows behind wind speed, gust and visibility.** **[declining]** — not stated. This bounds the meaningful time resolution of any analysis using them.

15. **Which layer is authoritative when the coded text and the derived members disagree.** **[declining].** They agree in this record. The presence of both means disagreement is detectable, which is a genuine strength; the resolution policy is yours to define.

16. **Precision provenance of temperature and dewpoint.** In this record the tenths come from an optional remarks group. Whether that group is present for all stations and all times is **[declining]**, and it directly controls whether your series has one decimal place or none.

17. **Whether station position and elevation are current as of the observation or as of publication.** **[declining].** Relevant only for long histories and station moves, but it silently invalidates spatial joins when it bites.

18. **Timestamp offset guarantees.** The example carries an explicit UTC designator; whether every record does is **[declining]**. Reject records without an offset rather than defaulting them to local time, which is what most date parsers will do for you.


TRANSCRIPT B

## 1. What this feed is

Each record is one surface weather report issued by one aerodrome reporting station, identified by its ICAO location indicator, for one moment. The station is the subject of the record — it carries the `featureOfInterest` role — and the record as a whole is bound to an aerodrome-surface-weather concept. The results are air temperature, dewpoint, wind direction, sustained wind speed, gust, prevailing visibility, altimeter setting, sea level pressure, present weather, cloud layers, and a flight category, plus a quality bitmask and the undecoded report text the values were parsed out of.

Two things about the shape of the feed matter more than the list of quantities. First, only the station identifier, the observation time, and the raw text are required; every decoded quantity may be absent from any given record, so no analysis may assume a rectangular table. Second, the record mixes report types: routine hourly reports and special off-cycle reports arrive on the same stream and are distinguished only by a status member. The stream is therefore not an equal-interval sample of the atmosphere.

The record identifies no observing procedure and no instrument. Nothing in the two files tells you whether two reports a year apart from the same station came from the same sensor package, and the specification is explicit that procedure identity is comparability-critical and must not be inferred from anything else. Long series from one station are, on this evidence, of unknown instrumental homogeneity.

## 2. Analytics the stream supports

**Operational availability by aerodrome.** Counting flight-category states per station over time is directly supported: there is a station identity, a phenomenon time, and a categorical operating condition on every record that carries one. This is the highest-value analysis here because it is what the feed's derived member exists for.

**Ceiling-and-visibility risk conditioned on temperature–dewpoint spread.** Temperature and dewpoint are both instantaneous, both in the same unit, and both apply at the same instant, so their difference is a well-posed per-record quantity and can be regressed against the flight category or the cloud content of the same record.

**Wind climatology and gust behaviour.** Sustained speed and gust are both summaries over the identical ten-minute window ending at the observation time. Because the windows coincide exactly, the gust-minus-sustained difference is a meaningful per-record quantity — the annotations establish co-support, which is the condition that makes the subtraction legitimate.

**Pressure-field analysis across stations.** Sea level pressure is described as reduced to a common surface, so values from stations at different elevations are referred to the same datum. That is what makes a cross-station pressure map or a pressure-gradient estimate meaningful.

**Observing-programme performance rather than weather.** The difference between report time and observation time is a publication latency; the frequency of special reports is a measure of how often conditions crossed a trigger. Both describe the programme, not the atmosphere, and both are worth tracking separately from any meteorological analysis.

**Spatial interpolation and station-network analysis.** Station latitude, longitude and elevation are carried with explicit reference-system bindings, so positions can be used for neighbour selection, gradient estimation, and elevation-aware comparison.

What the stream does **not** support: recomputing or auditing the flight category (the threshold set is named but not supplied); decoding the quality bitmask; decoding present weather to a defined meaning; any true time-averaged statistic over an hour, because nothing in an hour is observed except one instant and one ten-minute window.

## 3. Combination rules

**Air temperature and dewpoint.** Compare across records freely; both are direct measurements at an instant, in one unit. Difference is valid — within a record, temperature minus dewpoint is the depression; across records, a change in either is valid. Do **not** sum: these are interval-scale temperatures and their total is not a quantity. Averaging across records is arithmetically defined, but it yields the mean of the sampled instants, not a mean over elapsed time; the values are declared instantaneous and carry no support period, so nothing licenses reading an average as an hourly or daily mean. Do not pool temperature with dewpoint: they are declared as different observed properties.

**Sustained wind speed.** Compare and difference across records. Do not sum. Averaging is defined but produces a mean of ten-minute means sampled once per report — roughly one sixth of elapsed time — and must not be reported as a mean wind for the period.

**Gust.** Compare and difference against other gust values; average only with the understanding that a mean of gusts is a mean of maxima. Gust and sustained speed share a unit and an observed property but carry **different statistics**, and the specification states directly that two results with the same observable property and different statistics are not comparable as like quantities. So: gust minus sustained is a legitimate derived gust factor, because the two summarise the same window; but gust and sustained values must never be pooled into one wind-speed sample, and a maximum taken over sustained values is not the maximum wind. Absence of gust is described as "no gusts reported", which is a statement about reporting, not a measurement of zero. Do not impute zero, and do not treat the absence as missing-at-random.

**Wind direction.** This is a circular quantity in degrees true. It may be compared, but it must not be differenced, summed, or averaged by ordinary arithmetic — the naive mean of 350 and 010 is 180, which is the reciprocal of the truth. Use circular statistics. Before that, the value 0 must be removed: it is declared to mean variable or calm, so it is a sentinel and not a bearing, and including it drags every circular mean toward north. Wind direction and wind speed must **not** be assembled into a wind vector on the strength of these files: no vector frame is declared, and the specification forbids inferring that members sharing a unit or an observed property are components of one vector. The direction is also stated to be the direction the wind blows *from*, so any vector construction needs a reversal the schema does not perform.

**Altimeter setting and sea level pressure.** These carry the **same unit and the same observed property**, and they must not be combined. One is reduced to the aerodrome's own elevation, the other to mean sea level using station elevation and temperature history. They are two different reductions of one underlying station pressure. Do not pool them, do not substitute one for the other, and do not difference them — the difference is an artefact of the two reduction procedures, not a meteorological quantity. Sea level pressure may be compared, differenced, and averaged across stations, because the reduction refers every station to one surface. Altimeter setting may be compared and differenced within one station over time; comparing it across stations at different elevations confounds the pressure field with the elevation difference. Nothing in the schema would flag either mistake, because the machine-readable annotations on the two members are identical.

**Prevailing visibility.** A string carrying qualifiers, so the values are censored: a "10+" reading is a lower bound and not a number. It may be compared only as an ordinal after parsing. It must not be summed or averaged; averaging censored values understates the true mean systematically. It carries no machine-readable unit — the unit appears only in prose — and its observed property is a generic length, so it will not survive a unit check against another feed.

**Cloud layers.** An encoded string of layer objects. Not a quantity; only equality comparison and layer counting are safe. The base heights inside it carry no unit and no vertical datum: the record's vertical reference system binds the station elevation member only, and the specification says properties not named by a coordinate binding are not part of the coordinate. Cloud base heights may therefore not be combined with station elevation, nor with heights from any other feed, without information the files do not contain.

**Flight category.** Categorical. Count and cross-tabulate; never average or order arithmetically. Comparable across records and stations only under the assumption that one unchanging threshold set was applied throughout, which the files assert but do not supply.

**Present weather.** A coded string with no code-list binding. Equality comparison and frequency counts only. Do not decode by pattern-matching the description or the sample.

**Quality bitmask.** Flags, not a magnitude. Not summable, not averageable, not orderable — you cannot rank records by it. No register identifies the bits. The specification states that absent quality never implies acceptable quality, so a null here licenses nothing.

**Station position.** Latitude and longitude are bound with the axis order latitude-then-longitude declared explicitly. Feeding the pair into a pipeline expecting longitude-then-latitude transposes every station. Degree differences are not distances; converting to a metric separation is a geodesic computation the annotations neither perform nor authorise.

**Station elevation.** Bound to a mean-sea-level height system, so elevations may be compared and differenced across stations. It must **not** be joined with latitude and longitude as a single three-dimensional coordinate: they are two separate bindings, not one compound system. Note also that the elevation is additionally tagged with a general-purpose altitude vocabulary term; that tag is a vocabulary correspondence and does not establish a datum. Joining on it to a feed carrying ellipsoidal heights pools two quantities that differ by the geoid separation — tens of metres.

**Station identity, name, position, elevation.** These are station attributes repeated on every record, not observations. Aggregating them over records weights each station by its report count.

**Report time.** Differencing it against observation time gives publication latency and is valid. It is not a weather time axis.

## 4. Time

The observation time is the phenomenon-time axis: it is the position at which the reported conditions obtained, and it is the only member that places the described state of the world on a time line. It carries no temporal reference system annotation, which under the specification means the core datetime semantics are intended; the sample is an RFC 3339 instant with a `Z` offset, so positions are UTC instants. Relating them to local civil time at the aerodrome requires a time zone the files do not carry.

Positions on that axis are **not uniform in what they cover.** Temperature, dewpoint, both pressures, visibility, present weather, cloud layers, and flight category are declared instantaneous — they apply at the stated instant and nowhere else. The three wind quantities are declared to characterise an interval of ten minutes anchored at its end, which resolves to the half-open period from ten minutes before the observation time up to it. In the sample record the temperature applies at 11:51Z while the wind values describe 11:41Z to 11:51Z. These are different temporal supports on one record, and treating the wind as instantaneous, or the temperature as a ten-minute mean, is wrong in both directions.

Because no result is declared to hold until the next report, no value may be carried forward. Between two hourly reports the atmosphere is unobserved; the fifty minutes of each hour outside the wind window are unobserved even for wind.

The declared cadence is one hour. The specification is emphatic that cadence is an expectation and not a constraint: it does not assert that every hour has a record, does not assert ordering, does not prove that a successor exists, and does not make a stream that misses a beat invalid. It is useful for sizing a staleness threshold and for detecting gaps; it licenses no gap-filling. Two further facts cut against naive hourly binning. Routine reports are stated to fall near the end of the hour rather than on it, so a series of these is a sample at roughly fifty-one minutes past, not an hourly mean. And special reports arrive off-cycle on the same stream, so actual spacing is sometimes sub-hourly. Since specials are issued because conditions changed, an unweighted mean over records is biased toward changing conditions; any time-representative statistic needs explicit time weighting or a filter to routine reports only.

The report time is the result time — when the encoded report was issued, two minutes after the observation in the sample. It must not be used as the time axis for the weather, and it must not be used to order phenomena.

## 5. Ambiguities

- **Cloud base unit and datum.** Not determined by the files. The heights sit inside an opaque string with no unit and no vertical binding. Comparing the sample against the raw text suggests the values are feet expanded from the coded hundreds-of-feet groups — that is an inference from one record and I mark it a **guess**. Whether those heights are above ground or above sea level is not established at all; I decline to decide it. At this station, which is near sea level, the distinction is negligible; at an elevated aerodrome it is not.
- **Flight-category thresholds.** The rule set is referenced but not supplied. I decline to state the boundaries, and I decline to assert that one threshold set applied across any archive.
- **Quality bitmask semantics.** No register is identified. Bit meanings are not determined; I decline to guess them. Equality comparison is all that is available.
- **Present-weather code list.** Named in prose as standard METAR codes but bound to no register. I decline to decode individual codes.
- **Meaning of null.** For every nullable member, whether null means "not measured", "not applicable", or "phenomenon absent" is not determined. In particular, a null present-weather value does **not**, on these files, establish that the weather was clear. I decline to decide it. If pressed, my **guess** is that it means nothing was reported — but that is exactly the reading the specification warns against acting on.
- **The zero wind direction.** The value conflates variable and calm. Whether a zero sustained speed distinguishes calm from variable is a plausible **guess** and is not established. Whether north is encoded as 360 is not determined.
- **Which observation the flight category was computed from.** The description implies the ceiling and visibility of the same report. I read it that way but mark it a **guess**; nothing states that the derived category and the reported members are mutually consistent, or that the category was not recomputed later.
- **Observable-property identifiers.** The catalogue behind the aerodrome-weather, present-weather, cloud-layer and flight-category concepts is a placeholder domain and does not resolve. Under the specification an unresolved reference is indeterminate rather than valid, so these identifiers cannot be used to establish that this feed's concepts are the same as another feed's. I decline to treat them as equivalence evidence. The quantity-kind tags on the numeric members are classification hints and, by the specification, establish no equivalence either — as the two pressure members demonstrate.
- **Instrumental and station continuity.** No observing procedure, no automation indicator, no station-move history. Whether a station's series is homogeneous is not determined. I decline to assume it.
- **Consistency between the decoded members and the raw text.** The sample is internally consistent on every member I can check. Whether that holds generally is not determined, and the raw text carries content — remarks, precise temperatures, pressure remarks — that the decoded members do not expose. I decline to assume the decoded fields are authoritative over the text or vice versa.
- **Report completeness.** Only the identifier, time, and raw text are guaranteed. Which members a given station habitually populates is not determined, so absence must be modelled per station rather than assumed uniform.
- **Cadence and special reports.** The hourly cadence is declared on the time axis of a record type that also carries off-cycle reports. How special-report positions relate to the declared cadence is not stated, and I decline to decide it.


TRANSCRIPT C

# 1. What this feed is

Each record is one surface weather observation issued by a single aerodrome
reporting station, keyed by its ICAO identifier, and stamped with the instant
the conditions obtained. It carries the decoded surface state — air temperature,
dewpoint, wind, prevailing visibility, two different pressure reductions, present
weather, cloud layers — alongside the original coded observation text from which
all of those were decoded, plus one derived operational label (the flight
category) and an automated quality-check bitmask.

The critical framing point: this is not a sensor telemetry stream. It is the
output of an **observing programme**. Records exist because the programme's rules
say a report is due, and some records exist precisely because the weather
changed. The record set is therefore not a uniform sample of the atmosphere, and
several members describe the programme rather than the sky. Treating the feed as
an evenly-spaced instrument time series is the single largest source of error
available here.

# 2. Analytics worth running

**Flight-category availability and persistence per aerodrome.** Every record
carries a category label and an observation instant, so you can compute the
fraction of time an aerodrome sits in each category, the transition matrix
between categories, and the duration distribution of below-VFR spells. This is
the highest-value analysis in the feed because the label is already
authoritative — it is stated to be produced by applying published thresholds,
which means you should consume it, not recompute it (see §5).

**Gust structure.** Sustained speed and gust speed are stated to come from the
same ten-minute window, one as the mean and one as the peak. That shared window
is what makes the gust factor (peak minus mean, or peak over mean) a coherent
quantity rather than a comparison of two unrelated samples. Gust-factor
distributions by direction sector and by category are well supported.

**Fog and low-ceiling onset lead time.** Temperature and dewpoint are both on the
same scale at the same instant, so their spread is meaningful per record. You can
test how far ahead of a mist/fog present-weather code or a category degradation
the spread begins closing. The data support this because both values, the present
weather codes, the cloud layers and the resulting category all share one
timestamp.

**Latency and pipeline health.** The gap between when conditions obtained and
when the report was issued is directly measurable per record. Its distribution,
and its tail, tell you the usable freshness of the feed for any operational
consumer.

**Decode fidelity auditing.** The raw coded text is retained alongside every
decoded value, so every decoded member can be independently re-derived and
checked. In this example the decoded wind (210° / 12 kt / gust 18) reproduces the
coded wind group exactly, and the two pressure members reproduce the altimeter
group and the sea-level-pressure remark. Any systematic decoder drift is
detectable without external data.

**Observing-programme volatility.** The rate of special (non-routine) reports per
station per unit time is itself a signal of how fast conditions are changing.
This is a legitimate analysis *of the programme*; it is not a measurement of the
atmosphere, and it must not be mixed into atmospheric statistics.

**Pressure/density altitude.** Altimeter setting, station elevation and
temperature are all present, which is the input set such a computation needs. The
formulas themselves are not in the files; supply them from outside and say so.

**Not supported without external data:** anything requiring runway orientation
(crosswind and tailwind components, runway selection) — runway headings are
nowhere in this feed. Also anything requiring local civil time (§4).

# 3. Combination rules

**Air temperature and dewpoint.** Interval scale with an arbitrary zero.
*Comparable* across records and across stations. *Differenceable* — the
temperature-minus-dewpoint spread is the intended and meaningful difference, and
differences of the same quantity across time or stations are meaningful.
*Averageable* over records, with the caveat in the last paragraph of this section
about which records you average. **Never summed** — the sum of two Celsius
temperatures has no referent. **Never ratioed** — "20 °C is twice 10 °C" is
false on this scale. Cross-station comparison of raw temperature conflates
elevation differences; elevation is available per record, but the files supply no
lapse rate, so any elevation correction is yours and must be declared.

**Wind direction.** A circular quantity in degrees true. **Not** differenceable,
summable or averageable by ordinary arithmetic: the mean of 350 and 010 is not
180. Use vector or circular statistics only. Additionally, the value 0 is a
**sentinel**, not a bearing — it denotes variable or calm. Any record with
direction 0 must be excluded from, or separately handled in, every directional
aggregate; including it drags every mean toward north. Comparison of two
directions is meaningful only modulo 360.

**Sustained wind speed.** A ratio-scale quantity, so comparable, differenceable,
averageable, and formally summable. But each value is a **ten-minute mean ending
at the observation instant**, not an instantaneous reading and not an hourly
mean. Consequences: a series of these values is a once-per-cycle snapshot of a
ten-minute window, so integrating it over time to obtain run-of-wind or total
wind travel is invalid — the windows do not tile the interval. Averaging a set of
them yields "the mean of the sampled ten-minute means", which is a different
estimand from "the mean wind over the period"; the difference matters when
sampling is condition-triggered.

**Gust speed.** A maximum over the same ten-minute window as the sustained speed.
*Differenceable against the sustained speed of the same record* — that is the one
combination this pairing is built for. **Do not average gusts with sustained
speeds**, and **do not average gusts across records naively**: gust speed is
present only when gusts were reported, so absence is informative, not missing at
random. Substituting zero for an absent gust is wrong (it fabricates a calm
peak); dropping the absent records is also wrong for any question about typical
gustiness (it conditions on gusts existing). Decide and declare which estimand
you want.

**Altimeter setting and sea-level pressure.** Both are in hectopascals and they
are **different quantities**. One is reduced to the aerodrome elevation under a
standard-atmosphere assumption; the other is reduced to mean sea level using the
station elevation and its temperature history. They must not be pooled, averaged
together, or treated as interchangeable, and their difference is an artefact of
two reduction procedures, not a physical anomaly. For cross-station synoptic work
— pressure gradients, trough and ridge location — use the sea-level reduction
only; it is the one constructed to be comparable between stations of differing
elevation. The altimeter setting is comparable across stations only in the sense
that it is the value each aerodrome would set; differences in it partly encode
elevation differences. Within a single station, either may be differenced across
time to obtain a tendency, but do not mix the two series.

**Prevailing visibility.** Delivered as text with qualifiers, and at least one
qualifier ("10+") denotes a **censored** value: the true visibility is at or above
the stated figure, not equal to it. Parsing it to 10 and averaging biases every
visibility mean downward, and the bias grows as conditions improve. Fractional
forms will not parse as decimals. Visibility may be compared and ordered
(treating censored values as at-or-above the bound); it may be averaged only with
explicit censoring handling; it must never be summed.

**Cloud layer heights.** Delivered as an embedded encoded array, so they require a
second parsing step before any arithmetic. Within one record, layers may be
ordered and the lowest obscuring layer identified. Across records, bases may be
compared and differenced **only if the height reference is the same**, which the
files do not state (§5). Do not add a cloud base to the station elevation: the
units differ from elevation's units and the reference level is undetermined.

**Station elevation and position.** Fixed station metadata repeated on every
record, not measurements. Comparable across stations; averaging them across
records is meaningless (it just weights stations by report count). Latitude and
longitude are geographic degrees on the stated reference frame and must be
handled as such — degree differences are not distances, and longitude degrees do
not convert to distance at a fixed rate.

**Quality-control flag.** A **bitmask**. It is nominal, not ordinal and not
numeric. It must not be compared as a magnitude, differenced, summed or averaged.
Only per-bit prevalence counts are legitimate, and only if you know the bit
meanings, which the files do not give.

**Flight category, present weather, report type, station name, raw text.**
Categorical or free text. Only counts, proportions and transition frequencies.
Note that the flight category is a **deterministic function of the ceiling and
visibility already in the record**; using it as an explanatory variable alongside
visibility or cloud data in the same model is circular.

**The only legitimate summation in this feed is counting records** (reports per
station, hours in a category, number of gust events). Every measured quantity
here is intensive or instantaneous; none of them add.

**Governing all averaging:** records are of two kinds, routine and special, and
the special ones exist *because conditions were changing or had deteriorated*.
Any average taken over a mixed set is biased toward disturbed weather, and the
bias is worst exactly when the weather is worst. For climatological or
distributional work, restrict to routine reports, or weight by the time each
observation represents. State which you did.

# 4. Time

The time axis of the thing described is the **observation time** — the instant at
which the reported surface conditions obtained. Every measured member in the
record is anchored to that instant (the wind members to the ten-minute window
ending at it). All time-series construction, joining, resampling, and lag analysis
must key on that member.

The **report time** is the issuance instant of the encoded result — a property of
the dissemination process, not of the atmosphere. Using it as the time axis
shifts every value later by a variable latency and destroys any lead/lag analysis.
Its only correct use is as the endpoint of a latency measurement, or for
reconstructing what a consumer knew at a given moment (as-of / point-in-time
joins), which is a genuinely different and useful question from what the weather
was.

Both instants are absolute points on the UTC timeline. The observation time
originates as a count of seconds from the epoch, so it carries no zone or
daylight-saving ambiguity at all; the report time arrives as a UTC-qualified
string. Positions on the axis therefore relate to civil time **only through a UTC
offset for the aerodrome, which these files do not provide**. Longitude is not a
time zone and must not be used as one. Consequently any diurnal-cycle, local
business-hours, or day-boundary analysis requires an external zone mapping — I am
declining to supply one.

Axis spacing is irregular by construction. The routine cycle is stated to produce
about one report per station per hour, normally near the end of the hour, and the
example sits at :51 — so the natural "hourly" series is offset from the top of the
hour, and special reports insert additional, condition-triggered points between
them. Two consequences: methods that assume uniform sampling (spectral analysis,
naive fixed-lag correlation, differencing as a proxy for a rate) require explicit
resampling first; and the resampling rule you choose reintroduces the
special-report bias unless it is time-weighted. Whether a report near the end of
an hour should be labelled with that hour or the next one is a convention the
files do not settle — pick one and declare it.

# 5. Ambiguities

**Cloud base units and reference level — inference, flagged.** The schema states
only that each layer carries a coverage code and a base height; it gives no unit
and no reference. In the single example the decoded bases correspond to the coded
cloud groups multiplied by one hundred, which is consistent with feet. Whether
those heights are above ground or above mean sea level is **not determined**, and
it matters: station elevation here is small, so a single example cannot
distinguish the two. I am declining to decide it. Do not combine cloud bases with
station elevation until it is resolved.

**Ceiling definition and flight-category thresholds — declining.** The category is
stated to be derived from ceiling and visibility, but neither the rule that picks
the ceiling out of the cloud layers nor the numeric thresholds appear in the
files. Consume the supplied category; do not attempt to recompute it, and do not
assume any particular threshold set.

**Quality-control bit semantics — declining.** The mask is stated to be per-check
bits, but no bit is defined. You cannot filter on quality with this feed alone.
The observed value of 2 tells you one specific check fired or passed, and nothing
more.

**Temperature and dewpoint precision — inference, flagged.** In the example, the
decoded values carry tenths while the main coded body carries whole degrees; the
tenths appear to come from a supplementary group in the remarks. If that reading
is right, then precision varies between reports and between stations depending on
whether that group is present, and any analysis sensitive to sub-degree resolution
(dewpoint spread near zero, fog onset) will have heterogeneous resolution. I
cannot confirm this from one example — treat it as a hypothesis to test against a
larger sample.

**The direction-zero sentinel — partial inference, flagged.** Zero is stated to
mean "variable or calm", which conflates two physically different states. It is
plausible that the two can be separated by whether the sustained speed is also
zero, but the files do not say that, and they do not say whether a variable wind
might instead be reported with a nonzero mean direction. Declining to decide.

**Missing versus null.** Most measured members are optional rather than nullable,
while several textual members are explicitly nullable. Whether an absent member
and an explicit null carry different meanings for a given quantity is **not
established** by the files. Only the station identifier, the observation instant
and the raw text are guaranteed present; assume nothing else exists in any given
record.

**Visibility qualifier vocabulary — declining.** One censoring qualifier and the
existence of fractional forms are mentioned; the full set of forms that may appear
is not enumerated. Write the parser defensively and log unparsed forms rather than
coercing them.

**Reporting-station identity over time — not determined.** Nothing in the files
establishes whether a station's position, elevation or name are stable across the
history of the feed, or whether an identifier can be reassigned. For long-baseline
work, treat the station metadata as observed-per-record rather than as a static
dimension table until you have verified stability empirically.

**Multi-station scope — assumption.** Because position and elevation ride on every
record rather than being fixed, the feed can plainly carry more than one station,
but the files do not state the population of stations, its stability, or any
guarantee of completeness. Do not compute network-wide statistics as if the
station set were fixed.

**Duplicate, corrected and amended reports — not determined.** Nothing in the
files says whether a later record can supersede an earlier one for the same
station and observation instant. Until verified, do not assume that station plus
observation instant is a unique key; check for it, and decide a
last-report-wins or first-report-wins rule explicitly.


TRANSCRIPT D

# 1. What this feed is

Each record is one surface weather observation issued by one aerodrome reporting
station, identified by its ICAO code. The thing being observed is the station
site — not a grid cell, not an airspace volume — so every record is a point
observation anchored to a fixed piece of ground whose horizontal position and
mean-sea-level elevation travel with the record.

The payload mixes three different kinds of value that happen to sit side by side:
directly sensed atmospheric quantities (temperature, dewpoint, present weather,
cloud layers, visibility), wind statistics computed over a short window rather
than sampled at an instant, and quantities that are not observations at all but
reductions and classifications computed from other observations (altimeter
setting, sea-level pressure, flight category). It also carries the original
coded text of the report, which is a re-encoding of most of the decoded members
rather than an independent source of information.

The nominal rhythm is one routine report per station per hour, issued close to
the end of the hour, with off-cycle special reports interleaved when conditions
change enough to warrant one.

# 2. Analytics

**Per-station time series and climatology.** The observation time is explicitly
the time the conditions obtained, and a nominal hourly cadence is declared, so
temperature, dewpoint and pressure form a usable series per station. This is the
one family of analyses the data supports with no external inputs.

**Dewpoint depression and moisture regime.** Temperature and dewpoint are the
same unit, the same derivation, and both apply at the same instant, so their
difference is well defined within a record. That difference is the natural
driver for fog and low-ceiling work.

**Gust structure.** The gust value is a maximum over the same ten-minute window
that produced the sustained wind mean, which is exactly the condition needed for
a gust factor to mean anything. Ratios and differences between the two are
sound within a record.

**Wind roses and directional exposure.** Direction and speed share a support
window and an anchor, so they pair into a vector per record. Crosswind analysis
against specific runways is *not* supported by these files alone — runway
headings appear nowhere.

**Flight-category availability.** The category is a calculated classification, so
counting how often a station sits in each class, by hour or season, is a
legitimate and cheap operational summary.

**Reporting latency and observing-programme behaviour.** The record carries both
the time the conditions obtained and the time the encoded result was issued.
Differencing them measures the reporting pipeline. Separately, the routine/special
flag describes the observing programme rather than the atmosphere, so its rate is
a measure of how often conditions were changing — and a warning that the series
is not evenly spaced.

**Spatial fields across stations.** Positions are in a stated geographic CRS and
elevations in a stated vertical CRS, so multi-station interpolation and gradient
work is possible — but only for sea-level pressure among the pressure members
(see below).

Two analyses that look available and are not: anything requiring local civil
time, and anything requiring the quality-control flag's meaning.

# 3. Combination rules

**Temperature, dewpoint.** Same unit, same instant, measured. Differences within
a record (dewpoint depression) and across records or stations are valid.
Averages are defined. Sums are not meaningful — these are interval-scale
quantities, and neither is a ratio of two Celsius values. Averaging a run of
records is a sample mean of hourly snapshots, not a time-weighted mean of the
period, and it is biased whenever special reports thicken the sampling during
changing weather.

**Wind direction.** A bearing. Ordinary arithmetic is invalid: a naïve mean of
350° and 10° gives 180°, the opposite direction. Use circular statistics or
resolve to vector components. Before any of that, drop the zero values — zero is
a sentinel meaning variable-or-calm, not a bearing of due north, and the files
give no way to tell those two cases apart. Differencing two directions requires
wrapping to ±180°.

**Wind speed and gust.** Both are knots and both are statistics over a
ten-minute window ending at the observation time, so within a record they may be
compared, differenced and ratioed. Across records: the gust is a maximum, and
maxima do not average. A "daily maximum gust" taken from hourly reports is the
maximum over roughly sixty minutes of sampled window per day, not over the day —
it is a lower bound on the true peak, and it should be reported as one. Absence
of a gust value does not mean zero gust; it means no gust met the reporting
criterion, so imputing zero and averaging corrupts both the mean and the
variance. Both members are whole-knot integers, so a one-knot difference is at
the quantisation floor.

**The support-window trap that applies to all three wind members.** The values
summarise ten minutes, but the cadence is an hour. Averaging them yields a mean
over the sampled sixth of elapsed time, not a mean over the elapsed time.
Anything phrased as "average wind over the day" must be qualified accordingly.

**Visibility.** A string, in statute miles, and censored. "10+" means *at least*
ten, not ten. Parsing it to 10 and averaging biases the mean downward and
destroys the upper tail. Treat it as right-censored data, or reduce it to
threshold counts. Note also that this is the only imperial-length member in a
record whose elevation is metric — do not let a unit-inference routine mix them.

**Altimeter setting.** Reduced to the aerodrome's own elevation. Across records
from one station it may be differenced to obtain pressure tendency. Across
stations at different elevations it is **not** a comparable pressure field, and
differencing it between stations does not yield a pressure gradient. In the
example record the altimeter setting and the sea-level pressure agree almost
exactly, but that is an artefact of a station three metres above sea level and
must not be generalised.

**Sea-level pressure.** This is the member intended for cross-station comparison
and gradient work, because the reduction puts every station on a common surface.
Its accuracy degrades with the size of the reduction, so comparisons among
stations of very different elevation carry reduction error that the record does
not quantify. It may be absent.

**Altimeter setting versus sea-level pressure.** Same unit, different reference
surfaces. Never concatenate them into one series, never substitute one for the
other when one is missing, and never difference them expecting a physical
quantity.

**Elevation.** A fixed station attribute in a mean-sea-level vertical datum.
Differences between stations are valid within that datum. It must not be
combined with ellipsoidal (GNSS) heights without a geoid correction. It is not a
time series and should not be averaged over records.

**Latitude and longitude.** Degrees in a geographic CRS. Distances require a
geodesic computation, not Euclidean arithmetic on degrees, and longitude must
never be averaged naïvely across the antimeridian.

**Flight category.** A label, and one *computed from* ceiling and visibility.
Only counting and grouping are valid — no arithmetic, no averaging of an ordinal
encoding without saying so. Crucially, it is not independent evidence: using it
as a predictor alongside visibility and cloud in the same model is circular.

**Quality-control flag.** A bitmask. It is not ordered and not additive: a value
of 2 is not worse than 1 and not half of 4. Summing or averaging it is
meaningless. Without the bit definitions, the only defensible use is
zero-versus-nonzero grouping.

**Report type.** Categorical, and about the observing programme rather than the
air. Group by it; never treat it as a condition of the atmosphere.

**Present weather and cloud layers.** Strings; the cloud member is a nested
document carried as encoded text. Coverage codes are categorical. Layer base
values carry no declared unit anywhere in the record — see the ambiguities.

**Observation time versus report time.** Never mix the two axes. Ordering or
binning a series by report time places observations at the wrong point on the
phenomenon axis; their difference is only meaningful as pipeline latency.

**All cross-record combinations above assume a common station identifier**
unless explicitly stated as cross-station.

# 4. Time

The observation time is the time axis of the thing described: it is the instant
at which the reported conditions obtained. The report time belongs to the
publishing process, not to the atmosphere, and is a second, distinct axis.

Positions on the phenomenon axis are UTC instants. The upstream source delivers
them as epoch seconds, so the resolution is one second, though in practice the
value is the nominal observation minute rather than a precise sensor instant.

Nothing in the record carries a local offset or a timezone. Civil time at the
station is therefore **not determined** by these files. Any diurnal analysis must
either stay in UTC or bring in an external timezone-and-DST lookup keyed on the
station. Binning stations together by UTC hour-of-day silently mixes different
local times of day and will produce a smeared, meaningless diurnal curve for any
multi-station set.

Two further alignment points that are easy to get wrong. First, the record is not
internally simultaneous: temperature, dewpoint, pressure, visibility, present
weather and cloud all apply *at* the observation instant, while the three wind
members apply to the ten-minute interval *ending* at that instant. Treating them
as co-timed introduces up to ten minutes of offset. Second, routine reports fall
near the end of the clock hour — the example is at :51 — so the hour label of a
report is not the hour it characterises; its wind window lies in the last ten
minutes of that hour. The declared hourly cadence is nominal, and special
reports break it.

# 5. Ambiguities

- **Cloud layer base unit and datum.** Not stated anywhere. The example shows
  4500 and 25000 against raw codes of 045 and 250, which fixes the factor of one
  hundred but not the unit. My reading is feet above ground level, by METAR
  convention — **this is a guess** from general knowledge, not something the
  files establish. The datum relationship between cloud base and the station's
  mean-sea-level elevation is **not determined**; I decline to assume they share
  a reference.
- **Coverage codes and ceiling definition.** Which coverage codes constitute a
  ceiling, and the numeric thresholds that map ceiling and visibility onto the
  four flight categories, are **not determined**. I decline to supply them.
- **Quality-control bit meanings.** **Not determined.** Declining.
- **Visibility string grammar.** The unit is stated and two shapes are alluded
  to (a plus-qualified value and fractions), but no complete grammar is given. I
  decline to specify a parser.
- **Zero wind direction.** Conflates variable and calm with no discriminator
  provided. **Not determined.** Whether due north is encoded as 0 or 360 is also
  **not determined**.
- **Missing gust.** Described as omitted when no gust was *reported*, which is a
  statement about reporting, not about occurrence. Whether a missing gust means
  no gust occurred, none met threshold, or the sensor was unavailable is **not
  determined**.
- **Null versus absent.** Only the station identifier, observation time and raw
  text are mandatory; several members are additionally nullable. Whether an
  explicit null differs in meaning from an omitted member is **not determined**.
- **Per-record station geometry.** Position and elevation ride on each record
  rather than on a station table, and neither is mandatory. If two records for
  the same station disagree on coordinates, which is authoritative — and whether
  the disagreement signals a re-survey or an error — is **not determined**. No
  station registry is supplied.
- **Corrections and duplicates.** Whether reports are ever amended or
  retransmitted, and how two records sharing a station and observation time
  should be resolved, is **not determined**. The report-type member is an open
  string; values beyond the two named ones may occur.
- **Completeness.** Whether the feed contains every station and every cycle is
  **not determined**, so a gap cannot be distinguished from a station that did
  not report.
- **Temperature resolution.** The example carries tenths, and my general
  knowledge says that precision comes from an optional remark group and is
  absent from some reports, leaving whole degrees. Whether resolution varies
  across this feed is **not determined** from the files; treat mixed precision as
  a live possibility when computing small differences.
- **Concept definitions.** The observable-property and catalogue references point
  at placeholder hosts that cannot be dereferenced, and the schema's own
  identifier is likewise a placeholder. The precise definitions behind the
  aerodrome-surface-weather, present-weather, cloud-layers and flight-category
  concepts are therefore **not available**, and I decline to substitute my own.
- **Pressure back-conversion.** The altimeter setting is published in
  hectopascals while the raw text carries it in inches of mercury; the conversion
  and rounding have already happened. Back-converting will not reproduce the
  original figure exactly. This is an observation about the example, not a
  documented rule.
- **Who computes the derived members.** The reductions and the flight category
  are marked as calculated, but whether they are computed upstream or by this
  feed — and hence whether their conventions are stable over time — is **not
  determined**.
