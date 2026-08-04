# FirmsModisFireDetection — analyst briefing

## 1. What this feed is

Each record is a single **observation event**: a place, a moment, two numeric readings whose names begin with "bright", one further numeric reading, and two labels identifying which producing stream and which platform the observation came from. The schema is named `FirmsModisFireDetection` and the sole example carries `source: "MODIS_NRT"`, so the feed is presented as fire detections from MODIS. That is the extent of what the files assert about the domain.

The single most important thing to get right before touching this data: **a record is an observation, not a fire.** There is no fire identifier, no event identifier, no cluster identifier, and no per-record unique key of any kind. Nothing in the files lets you decide whether two records refer to the same burning thing seen twice or to two different burning things. Counting records therefore counts *detections*, not fires, not events, and not distinct locations. Any headline of the form "N fires" derived from this feed is unsupported by what the files establish.

The second thing: the record is **closed** (`additionalProperties: false`). No conforming record will ever carry a confidence score, a footprint or pixel size, a viewing geometry, a day/night flag, a processing version, or an identifier. The absences noted throughout this briefing are structural, not accidental — you cannot wait for a richer record to show up.

The third thing: the files say nothing about **completeness**. There is no statement that the feed is a census, no statement about detection thresholds, no statement about coverage in space or time. Absence of records is therefore *not* evidence of absence of fire. Do not build any analysis whose conclusion rests on a region or interval being empty.

## 2. Analytics worth running, and why the data supports them

**Spatial distribution and hotspot mapping over time.** Every record is *required* to carry both coordinates and a timestamp — none of the three can be missing in a conforming record. That guarantee is what makes space–time aggregation safe here: you never have to decide how to handle a positionless or timeless detection, because the schema forbids one. Binning detections into a grid and watching bins change over time is well supported.

**Detection-rate time series.** Counting records per time bucket is supported for the same reason, subject to the timestamp caveats in §4 and to the count-is-not-fires caveat above. This is a measure of *observation activity*, and it confounds real activity with observing opportunity, since the feed carries nothing describing when or where the platform was looking.

**Stratified comparison and per-stratum distributions.** `source` and `satellite` are both required, so every record can be assigned to a `(source, satellite)` stratum with no missing-key handling. Distributions, quantiles, and trends of the numeric readings are defensible *within* a fixed stratum. Across strata they are not (see §3).

**Reporting-completeness analysis of the one optional quantity.** `frp` is the only member the schema permits to be absent. Whether it is present is therefore itself a recorded fact about every record, and the presence rate — by stratum, by time, by region — is a legitimate and useful analysis. It is also a prerequisite for any aggregate over `frp`, because you must know your denominator.

**Co-variation between the two "bright" quantities.** Their joint distribution, rank correlation, and scatter within a fixed stratum are computable and interpretable as "these two readings move together this way." Note that rank correlation is safe under the scale uncertainty in §3, whereas anything requiring a common origin or unit is not.

**Analyses this feed does not support**, and why — each of these will look computable and will be wrong:

- **Burned area, or anything per unit area.** No footprint, no resolution, no pixel geometry, and the schema is closed. A detection count per grid cell is a count, not a density of burning.
- **Fire duration, persistence, spread, or growth.** These all require linking records into the same fire across time. There is no identity member to link on. Spatial-proximity linking is a modelling choice you would be importing, not something the data establishes.
- **Confidence-filtered subsets.** There is no confidence or quality member.
- **Severity or intensity ranking across platforms or across sources.** No calibration statement exists in the files; see §3.
- **Viewing-geometry normalisation.** No observation-geometry member exists and none can be added.
- **Day/night stratification.** No flag exists. Local solar time could in principle be approximated from longitude and timestamp, but only under the unit assumption in §5 — and local *solar* time is not local *civil* time (see §4).

## 3. Combination rules

The governing fact: **the files declare no units, no measurement scales, and no calibration relationship between strata.** They do, however, hand you `source` and `satellite` as required discriminators. The presence of those two members is the files' own signal that records are not all alike; treat crossing them as an act requiring external justification, not a default.

**Latitude and longitude.**
- *Compare / order:* yes, within an assumed common reference frame. The frame is not stated, so combining these coordinates with positions from any other dataset is not warranted by the files.
- *Difference:* yields an angular difference only. Converting a coordinate difference to a ground distance requires a datum and ellipsoid, neither of which is given. Do not report kilometres without importing that assumption explicitly.
- *Average:* **do not** naively average. Averaging longitudes across the ±180 seam produces a point on the opposite side of the world, and the componentwise mean of latitude/longitude pairs is not a correct centroid on a sphere in general. If you need a representative point, use a method appropriate to angular coordinates and state it.
- *Sum:* meaningless. Coordinates are positions, not amounts.

**`brightness` and `bright_t31`.**
- *Scale:* not established. Whether these sit on an interval scale (a shifted zero, like a temperature) or a ratio scale (a true zero) is the decisive question and the files do not answer it. **Adopt the interval treatment as the conservative default** (this is an assumption, stated as such). Under it: differences and means are meaningful; **sums are not**, and **ratios are not**. A "total brightness" or a "brightness is 12% higher" statement is unsupported.
- *Compare and difference across records:* yes, **within a fixed `source` and a fixed `satellite`**. Different platforms are different instruments and different `source` values are different processing streams; nothing in the files says their readings are on a common scale, so cross-stratum comparison of these numbers is not warranted. If you must pool, say plainly that you are assuming cross-calibration the feed does not assert.
- *Average:* yes, within a stratum, under the interval treatment. An average across strata inherits the same unwarranted-calibration problem.
- *`brightness` minus `bright_t31`:* arithmetically available and a natural thing to want. But the files do not state that these two are in the same unit or share a zero, so the difference is only interpretable under that assumption. Mark it as an assumption wherever the derived value appears; do not let it propagate silently into a downstream product.

**`frp`.**
- *Optionality is the first-order concern.* It may be absent, and the files **do not define absence as zero**. Never coalesce a missing `frp` to 0 — that silently converts "not reported" into "reported as none" and biases every sum and mean downward. Every aggregate over `frp` must state its denominator policy: sum-over-present, mean-over-present, or excluded-record count.
- *Compare / difference / average:* within a fixed stratum, yes. Across strata, the same missing-calibration objection applies as for the brightness quantities.
- *Sum:* summing is only defensible if the records being summed are **distinct, non-duplicated observations of non-overlapping things**. The feed gives you no way to establish that. There is no identifier, no footprint, and two records at nearly the same place and time from different platforms may well be the same physical thing observed twice. **Summing across `satellite` values, or across `source` values, risks double counting and the files provide no mechanism to detect or prevent it.** A total that pools platforms should be treated as an upper bound at best, and labelled as such.
- Whether `frp` has a true zero (and so whether summing is meaningful at all) is a guess; see §5.

**`source` and `satellite`.**
- Nominal labels. Equality and grouping only. No ordering, no arithmetic, no interpolation, no "average satellite."
- Their value domains are **not enumerated** by the schema. You cannot know the full set of strata in advance. Any hard-coded list of expected values will silently drop records carrying an unanticipated value — build the stratification from the data and alert on unseen values rather than filtering to a fixed list.

**`acq_datetime`.**
- It is typed as an unconstrained string. **Do not sort or compare records by the raw string.** Lexicographic order coincides with chronological order only if every value is same-format, same-width, and same-offset, and the schema requires none of that. Parse to an absolute instant first, and fail loudly on anything that does not parse rather than falling back to string order.

**Record counts.**
- Countable, and the count is exact for records. It is *not* a count of fires, events, or locations, for the identity reasons in §1.

**A note on defensive validation.** The schema declares that it uses the validation extension but imposes no ranges, no enumerations, and no string format. Nothing constrains latitude to ±90, longitude to ±180, or `frp` to non-negative values. A conforming record can therefore carry values that are nonsense for the domain. Validate ranges yourself at ingest; schema conformance will not do it for you.

## 4. Time

**`acq_datetime` is the only member carrying time and is therefore the time axis.** No other member is temporal. In particular, the `NRT` fragment inside the example's `source` value is not defined by the files as a latency or timeliness statement, and I decline to read it as one.

**How positions on that axis relate to civil time.** The member is typed as a plain string with no format constraint, so the *schema* fixes nothing. The one example value is `2026-08-02T11:42:00Z`. If that shape holds across the feed, the trailing `Z` designates UTC, which means each position is an **absolute instant**, directly readable as civil time in UTC, and instants from different records are directly ordered and differenced once parsed.

Three consequences an analyst will otherwise get wrong:

1. **UTC is not guaranteed.** Because the format is unconstrained, a conforming feed may mix offsets, or omit an offset entirely. An offset-less timestamp is not an instant at all — it is a local wall-clock reading whose position on the absolute axis is undetermined. Normalise on ingest; do not assume `Z`.

2. **Local civil time is not derivable from the record.** The record locates the observation geographically, but geographic position does not determine a civil time zone — zone boundaries are political and daylight-saving rules are jurisdictional, and neither is present in the record. Any "local time of day" analysis requires an external zone lookup, and any *solar* time approximation from longitude is a different quantity from civil time and should be labelled as such.

3. **Resolution and semantics are unstated.** The example shows zero seconds and a whole-minute value, which is consistent with minute granularity but does not establish it. More importantly, the files do not say whether the timestamp marks the instant of observation, the start of an acquisition or aggregation interval, or a rounded/binned value. Two records bearing equal `acq_datetime` values are therefore not necessarily simultaneous, and you should not build sub-granularity ordering or sequencing logic on this member.

The record carries **no duration, no end time, and no validity interval**. Whether the record denotes a point on the axis or an interval anchored at that point is not established by the files.

## 5. Ambiguities

**Not determined — declining to decide:**

- **Measurement scale of `brightness` and `bright_t31`** (interval vs. ratio). This decides whether sums and ratios are legitimate. I recommend the interval treatment as a conservative default, and I flag that recommendation as an *assumption*, not a finding.
- **Whether `brightness` and `bright_t31` share a unit and a zero.** Their difference is only meaningful if they do. Declining.
- **Whether readings are comparable across `satellite` values or across `source` values.** No calibration statement exists. Declining.
- **Coordinate reference system and datum.** Declining. This blocks safe joins with any other geospatial dataset.
- **Whether the coordinates denote a point measurement or a representative point for an areal footprint.** Declining. This blocks all area-normalised analysis.
- **Meaning of the `satellite` value `"A"`, and the domain of that member.** The example is a single character; whether the domain is single characters or arbitrary strings is unconstrained. Declining.
- **Meaning of `source`, and specifically whether different `source` values can carry revisions or supersessions of the same underlying observation.** If they can, pooling sources double counts. The files neither establish nor exclude it. Declining — and treat cross-source pooling as unsafe until resolved externally.
- **Semantics of an absent `frp`.** Not-computed, not-applicable, below-threshold, and dropped-in-transit are all consistent with the files. Declining — and in the meantime, do not impute zero.
- **Record identity and deduplication key.** None exists. Declining to propose a surrogate; note that any proximity-based dedup you invent is a modelling assumption that will change your totals.
- **Whether records are ever updated, corrected, or retracted**, and whether the feed is append-only. Declining. This determines whether a stored history can be trusted.
- **Whether the feed is complete, sampled, or thresholded.** Declining. Consequence restated because it is the easiest error to make: empty is not zero.
- **Timestamp resolution and whether it marks an instant or an interval start.** Declining.
- **Any authoritative external definition.** The schema's `$id` is a non-resolvable placeholder, so there is no retrievable definition to appeal to from within what I was given.

**Guesses — marked as guesses, and not relied on anywhere above:**

- **Guess:** `latitude` and `longitude` are in decimal degrees, latitude positive north and longitude positive east. The example values fall inside ±90 and ±180, which is *consistent* with degrees but does not prove it, and consistency with a range is weak evidence.
- **Guess:** `brightness` and `bright_t31` are temperatures in kelvin, and `frp` is a radiative power in megawatts. This is inferred from the member names and the magnitudes of the example values, and it is exactly the kind of inference the files do not license. If it is right, the interval treatment I recommended for the two brightness quantities is the correct one and summing them is indeed invalid. If it is wrong, nothing above breaks, because no rule in §3 depends on it.
- **Guess:** `frp` has a true zero and may therefore legitimately be summed, subject entirely to the duplication and denominator cautions in §3. Do not treat this guess as clearing those cautions — they are the binding constraint, not the scale question.
