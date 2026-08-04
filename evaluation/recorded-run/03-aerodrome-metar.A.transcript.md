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
