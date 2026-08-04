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

1. Band values follow the band set `https://modis.gsfc.nasa.gov/about/specifications.php#thermal-anomaly-bands`, carried by the members ["brightness", "bright_t31"] in that order and are calibrated as `brightnessTemperature`.
   wrong reading: Treating raw band values as a physical quantity, or assuming which sensor band each member holds.

2. `latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `latitude`.

3. `longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `longitude`.

4. `brightness` is expressed in `K`.
   wrong reading: Assuming a different or conventional unit for `brightness`.

5. `bright_t31` is expressed in `K`.
   wrong reading: Assuming a different or conventional unit for `bright_t31`.

6. `frp` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `frp`.

7. `acq_datetime` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `acq_datetime` as the time the record was produced, received, or published, or using a different member for event time.


TRANSCRIPT A

# FIRMS MODIS fire detection — what an analyst needs to know

## 1. What this feed is

Each record is **one detection event at one pixel**, not one fire. The schema's own
description is precise about this and the precision matters: it is "one active-fire
pixel detection from a NASA FIRMS MODIS product," and the position is "the centre of
the nominal one-kilometre fire pixel." So a record asserts that a detection algorithm
flagged a particular pixel during a particular overpass, and it reports two
brightness temperatures in two spectral bands, sometimes a radiative power, where and
when the pixel was acquired, and which platform acquired it.

Three consequences follow immediately, and all three are routinely got wrong.

A record is not a fire. There is no fire identifier, no event identifier, no pixel
identifier, and no scene identifier. The schema declares no `featureOfInterest` at
all, which means the entity being observed is simply not stated. The specification is
explicit that feature identity "MUST NOT be inferred from observation identity,
location, property names, or transport metadata." Grouping detections into fires is
therefore an analysis you perform and own; it is not something the data asserts.

A record is not a location of burning. It is a location of a pixel *centre*. The
actual burning may be anywhere within the pixel, and the pixel's real footprint is
not carried in the record — "nominal one-kilometre" is a descriptive phrase about the
product, not a measured area. Nothing in these files gives you a pixel area, a scan
angle, or a footprint geometry.

Absence of a record establishes nothing. The specification states flatly that
"omission means undeclared unless stated otherwise. It never implies compatible,
successful, or acceptable data." Nothing in the two files describes what the feed does
when a pixel is observed and not flagged, when the sensor did not see the ground, or
when the algorithm suppressed a detection. A blank area on your map is not an area
without fire.

One further absence is load-bearing: there is no `resultQuality` anywhere in the
schema, and `additionalProperties` is `false`, so no confidence or quality value can
arrive in-band either. You cannot filter on detection confidence, and — per the
specification — the absence of quality "does not imply acceptable quality."

## 2. Analytics the stream supports

**Detection density in space and time.** Latitude, longitude and acquisition instant
are all required on every record, so every detection is placeable and datable without
imputation. Kernel density, gridded counts, and diurnal/seasonal detection profiles
are all computable from required fields alone. The caveat is the one above: these are
counts of *flagged pixels*, so the surface you are estimating is detection density,
not fire density, and it is confounded by whatever the product's detection threshold
and the platform's viewing geometry do. Neither is in the files.

**Band-difference screening and intensity gauging.** The schema binds `brightness` and
`bright_t31` as the two bands of one declared band set, with a stated calibration of
brightness temperature, and the description of `bright_t31` states its purpose
directly: paired with `brightness` "to screen false alarms and gauge fire intensity."
Both are required. This is the analysis the feed is shaped for, and it is the one
whose data support is strongest, because band identity and band order are asserted by
the schema rather than guessed from names.

**Radiative-power ranking and totals within an acquisition.** `frp` is a power in
megawatts and is the only intensity quantity on an absolute scale. Ranking pixels by
FRP within one overpass is well supported. Totalling FRP is supported only under a
condition the files do not supply — see §3.

**Stratified comparison by platform and product.** `satellite` carries
`semanticRole: observingProcedure`, and the specification says procedure identity is
"comparability-critical: different procedures can yield different biases or meanings
for the same property and feature." The schema is telling you, in machine-readable
form, that Terra-acquired and Aqua-acquired values are not interchangeable by default.
The analysis this enables — and effectively obliges — is stratification: build your
statistics per platform first, and pool only with a justification that comes from
outside these files. The same reasoning applies to `source`, which identifies the
product; a near-real-time product and a standard-quality product of the same nominal
quantity are different production paths.

**Latency analysis is not supported.** The description calls this a real-time feeder,
but the record carries only a phenomenon time. There is no `resultTime` and no
`ingestionTime`. You cannot compute how long a detection took to reach you from the
record alone.

**Fire radiative energy is not supported.** Integrating FRP over time to get energy
requires knowing the period each FRP value characterises. The schema declares no
`phenomenonTimeRelation` and no `supportPeriod`, and the specification is explicit
that "omission is not `instant`." The temporal support of an FRP value is undeclared,
so the integral has no defined width.

**Per-unit-area intensity is not supported.** There is no pixel area member, so FRP
density (MW·km⁻²) cannot be formed. Two pixels with equal FRP are not thereby equally
intense per unit ground area.

**Burned area, fire perimeter, spread rate, and fire tracking are not supported** by
what the record carries. They require feature identity or geometry, and the schema
declares neither.

## 3. Combination rules

A single rule from the specification governs all of the below and should be stated
first: a processor "MUST NOT infer … permission to aggregate, convert, transform,
reject outliers, or infer causality" from these annotations. Nothing in this schema
authorises an aggregation. Where an aggregation is defensible, it is defensible on
grounds you bring, and the conditions below are the ones you must satisfy.

**`brightness` and `bright_t31` (kelvin, two bands of one declared set).**

*Within a record:* differencing is the intended operation and is sound. But read the
result correctly — it is a **band-difference discriminant**, not a temperature rise of
anything. The arithmetic unit is kelvin; the meaning is not "the pixel is N kelvin
hotter." Two brightness temperatures in different bands describe the same pixel's
emission at different wavelengths, and their difference is an index.

*Across records:* comparable and differenceable **only where the band set is the
same**. The specification warns that "the bands of one sensor are not the bands of
another even where they are given the same colour name." Here the band set is asserted
once, at the record type, so all instances of this type share it — but records from
another feed, or from a schema carrying a different `spectralBands` reference, are not
comparable at the value level. Note also that equal `kind` values across two schemas
prove nothing: the specification says a processor "MUST NOT conclude from two schemas
carrying equal `kind` values that they draw on the same register, model, or
definition." Only equal `reference` values do that work.

*Across platforms:* stratify. `satellite` is a declared procedure, and equality of
procedure "is evidence for candidate grouping, not proof of statistical
interchangeability."

*Summing:* no. A brightness temperature is not an extensive quantity and summing has
no interpretation.

*Averaging:* not authorised by the schema. If you average anyway, you are averaging
across detections whose pixel footprints, view geometries, and platforms differ, none
of which the record reports. Report the platform stratification alongside any mean.

**`frp` (megawatts).**

*Optionality is the first trap.* `frp` is the only quantity absent from `required`.
Missing FRP means **undeclared**, and specifically it does not mean zero. The files do
not say why it can be absent — whether it was not retrieved, failed a threshold, or
is simply not carried for that product. Any FRP total or mean must report the count
of records lacking it, and must not impute a value.

*Comparing:* yes, within a platform and product. Across platforms, stratify for the
reason above.

*Differencing:* meaningful only between values of the same pixel or the same physical
region; the record supplies no identity to establish either, so the pairing is yours
to justify.

*Summing:* the standard construction — summing pixel FRP over an area — is defensible
**only if the summed records cover disjoint ground**. The files do not establish
disjointness. There is no pixel identifier, no acquisition identifier, and no
statement that two records cannot describe overlapping pixels, which is exactly what
you risk when consecutive overpasses or overlapping swaths land in the same query
window. Sum within a single acquisition of a single platform, or accept a double-count
risk you cannot bound from the data.

*Averaging:* an unweighted mean of FRP over pixels is a mean over footprints whose
areas are not reported, so it is not an intensity. Prefer sum with a stated disjointness
assumption, or report the distribution.

*Integrating over time:* no — the temporal support is undeclared (§2).

**`latitude` and `longitude` (degrees).**

The schema declares each of these as an `observationValue`. That is a stronger
statement than it looks: the specification says "multiple `observationValue`
properties in the same containing type represent multiple results, not one combined
act." So the schema declares five independent results per record, and **it does not
declare latitude and longitude to be a coordinate pair.** There is no
`coordinateReferenceSystem` annotation. The datum and axis interpretation appear only
in the human-readable description ("WGS-84 decimal degrees"), and the specification
forbids a processor from inferring "a coordinate, vector-frame, or linear reference
binding from names or samples." A human reader has WGS-84 from the prose; a toolchain
does not.

*Comparing:* equality of two coordinate values is equality of two numbers. It is
equality of place only under a reference system that is not machine-declared here.

*Differencing:* a difference of degrees is an angle, not a distance. A degree of
longitude at the sample's latitude of −13.25° subtends a very different ground
distance than one at 60°. Any distance, clustering, or nearest-neighbour computation
must go through a geodetic calculation on a stated ellipsoid, and the ellipsoid is
prose-only.

*Summing:* never meaningful.

*Averaging:* an arithmetic mean of longitudes is wrong across the antimeridian and
across the poles for latitude-weighted work, and in any case a mean of pixel *centres*
is a centroid of a sampling grid, not a centroid of fire. Use a proper spherical mean
if you need one, and label the result as a centroid of detections.

**`acq_datetime`.**

*Comparing and ordering:* see §4. Ordering is not machine-established by the schema.

*Differencing:* a difference of two positions is an elapsed duration only under a
metric temporal regime. The specification forbids inferring "metric intervals from
ordinal positions" and states that "a position whose definition establishes only order
MUST NOT be treated as a metric coordinate without additional authority." No regime is
declared here at all, so the metric reading rests entirely on the description.

*Summing or averaging:* not meaningful for instants.

**`source` and `satellite` (strings).**

Neither carries `codedValues`. The specification forbids inferring "a code-list
binding … from names, samples, units, or the number of members present." So these are
**opaque tokens**: exact string equality is the only defensible operation. Do not
order them, do not parse them, and do not assume that two spellings denote the same
product or platform, or that different spellings denote different ones. Both
descriptions say "such as," so the value sets are open — the schema does not establish
that `satellite` is confined to `A` and `T`, and you must handle unseen codes rather
than dropping them.

**A cross-quantity rule.** Because there is no `observedProperty` binding anywhere in
this schema, none of these quantities is bound to an external observable-property
definition. Joining this feed to another feed on the grounds that both measure "the
same thing" is not machine-supportable, and the specification says such a binding
"MUST NOT be repaired from labels, mappings, result schemas, units, descriptions,
property names, or samples." Unit agreement — two feeds both saying `K` — is not
agreement on quantity.

## 4. Time

`acq_datetime` establishes the time axis, and it does so as the **phenomenon time**:
the schema declares `semanticRole: phenomenonTime`, which the specification defines as
the "time during which the result applies to the observed property." So the axis is
the axis of the world being observed — the overpass acquisition instant — and not the
axis of processing, publication, or receipt. There is no second temporal member, so
the record offers no processing-time axis at all.

**How positions relate to civil time is not established by the schema.** This is the
most consequential gap in the two files, and it needs stating plainly.

The specification requires that a `phenomenonTime` used for an instant "MUST annotate
a value whose Core type and reference binding together encode a temporal position."
Here the Core type is `string` — not a Core temporal type — and no
`temporalReferenceSystem` is present. The specification's rule for exactly this case is
unambiguous: "Core temporal types need no annotation when their Core semantics are
fully intended. A non-Core or ambiguous encoding is indeterminate without one." And in
its conformance rules it forbids a processor from inferring "a temporal reference
regime from a non-Core or ambiguous encoding."

So: the description says UTC, ISO-8601; the single sample reads `2026-08-02T11:42:00Z`.
A human reader gets UTC from those. A conforming processor gets **indeterminate**, and
is specifically forbidden from recovering the regime from the sample. On a plain
reading this schema fails a `MUST` — I flag it as a probable conformance defect rather
than assert it, because the type-compatibility table elsewhere in the specification
does admit `string` for an RFC 3339 date-time, but only where a referenced definition
establishes that encoding, and no reference is present here. Declaring the member as
Core `datetime`, or adding a `temporalReferenceSystem`, would close this.

Two further temporal facts are undeclared and are commonly assumed:

**The temporal support of the values is not stated.** No `phenomenonTimeRelation` is
present, and the specification says "omission is not `instant`." So the schema does not
declare that the brightness temperatures or the FRP apply *at* the acquisition instant
rather than over some window around it. FRP is described as a rate, which suggests an
instantaneous reading, but that is a reading of prose, not a declaration.

**No revisit cadence is declared.** There is no `cadence` annotation, so nothing in the
schema states how often a given location is re-observed, or that successive records for
a location are regularly spaced. Do not build gap-detection or "missing overpass" logic
on an assumed revisit interval.

**Sort direction is not declared either.** `sortOrder` lives inside
`temporalReferenceSystem`, which is absent, so its `forward` default never engages.
In practice a zone-designated ISO-8601 string of fixed width sorts lexically in
chronological order, and I would sort on it — but that is my inference from the prose
form and the one sample, not something the schema asserts.

## 5. Ambiguities

Marked as *declining* where the files do not decide the matter, and as *guess* where I
am supplying something they do not.

1. **Temporal reference regime of `acq_datetime`.** *Declining to decide.* The prose
   says UTC and ISO-8601 and the sample carries `Z`; the schema declares nothing a
   processor may act on. I will not upgrade prose to a binding.
2. **Coordinate reference system, datum, and axis interpretation.** *Declining to
   decide.* Prose says WGS-84 decimal degrees; no `coordinateReferenceSystem` is
   declared, and the specification forbids inferring one from names or samples.
3. **Pixel footprint and area.** *Declining.* "Nominal one-kilometre" is a description
   of the product, not a per-record area. No area, scan angle, or geometry is present.
4. **What an absent `frp` means.** *Declining.* Not retrieved, below threshold, not
   carried by this product, and genuinely zero are all consistent with the files, and
   they have different analytical consequences. I will not impute.
5. **Whether records cover disjoint ground.** *Declining.* This is the condition that
   decides whether FRP may be summed, and nothing in the files supplies it.
6. **The closed sets of `source` and `satellite` values.** *Declining.* Both
   descriptions say "such as." No enumeration, no `codedValues` binding, no register.
7. **The relationship between `source` and `satellite`.** *Declining.* Both are
   present; whether the product identifier implies the platform, or whether they can
   disagree, is not stated.
8. **Whether the referenced band set really declares exactly these two bands, in this
   order.** *Indeterminate rather than undecided.* The specification makes band order
   an assertion by the schema author, never inferred from property order or names, and
   makes the band-count check indeterminate until the reference is resolved. I have
   not resolved it. The schema asserts `brightness` is band 1 and `bright_t31` is band
   2, and the description of `brightness` restates that; I take the assertion at face
   value and flag that it is unverified.
9. **Wavelengths.** *Declining.* The descriptions say "near four micrometres" and
   "near eleven micrometres," but the specification places wavelength ranges in the
   referenced band-set definition, not in the annotation. The prose is indicative, not
   a specification of band edges.
10. **Derivation of `frp`.** *Guess.* No `derivation` is declared, and the
    specification forbids inferring one from a name, description, type, or unit. My
    guess is that a radiative power is a retrieval rather than a direct reading, and
    so is not `measured` in the specification's sense — but this is a guess, the
    schema declares nothing, and you should not treat FRP as a raw sensor reading on
    my say-so.
11. **Temporal support of each value.** *Declining.* `phenomenonTimeRelation` is
    absent and "omission is not `instant`."
12. **Completeness of the record set.** *Declining.* Nothing states whether the feed
    is complete for a region and window, so neither absence of fire nor completeness
    of coverage can be read from the data.
13. **Whether `calibration: "brightnessTemperature"` is well-formed.** Not ambiguous —
    this is correct usage. `calibration` is an open enumeration, and the specification
    names brightness temperature as precisely the case an open value covers: "a
    quantity the values defined here do not name, such as brightness temperature, is
    carried as an open value." A processor must preserve it and must not reject the
    schema for it. I note it only because an unfamiliar token in an enumeration
    usually signals a problem, and here it does not.
14. **Schema identity.** The `$id` is a placeholder rather than a citable, resolvable
    identifier, so schema-identity-based joins or version pinning against this document
    are not available. *Observation, not a defect of the data itself.*


TRANSCRIPT B

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


TRANSCRIPT C

# FIRMS MODIS active-fire detections — analyst's briefing

## 1. What this feed is

Each record is **one observation of one pixel by one instrument on one overpass**, not one fire. The schema is explicit that the record is an "active-fire pixel detection" and that the geometry is "the centre of the nominal one-kilometre fire pixel" — so the unit of observation is a footprint on the ground that the sensor judged to contain fire at the moment it looked. A large fire produces many records in the same overpass; several unrelated ignitions inside one footprint produce one record; and a fire that burns for a week produces records only at the instants a satellite happened to be overhead.

The payload carries a location, two brightness temperatures (a ~4 µm channel and a ~11 µm channel), a fire radiative power in megawatts, the UTC instant of acquisition, a satellite platform code, and a product identifier. That is the whole record — the schema forbids additional properties, so there is nothing else arriving that you might key on.

The single most consequential property of this feed is that **it is a detections-only stream**. There is no record type meaning "looked here, saw nothing," and no record type meaning "did not look here." Absence of a record is therefore uninterpretable from the feed alone: it may mean no fire, no overpass, or an observation that failed some upstream screen. Every denominator you might want — fires per unit area, detection rate, fraction of a region burning — is unavailable, because the feed gives you numerators only.

## 2. Analytics worth running

**Spatio-temporal clustering of pixels into fire complexes.** Latitude, longitude and acquisition instant together support grouping co-located, contemporaneous detections into candidate fire objects, and then tracking those objects across successive overpasses. This is supported because the three fields fully locate each detection in space and time; it is *necessary* rather than optional, because per-record analysis will systematically mistake fire size for fire count.

**FRP-weighted intensity per cluster, per region, per overpass.** Fire radiative power is a rate of radiative energy release attributed to the pixel, and the schema states its unit. It is the only member on the record that is plausibly additive over disjoint footprints, which makes "total FRP observed in this region on this overpass" the natural intensity index. Note the qualifiers in section 3 before summing anything.

**The two-channel temperature contrast.** The schema states the ~4 µm and ~11 µm brightness temperatures are "paired ... to screen false alarms and gauge fire intensity." Their difference is therefore the intended discriminator and is worth carrying as a derived column alongside FRP. Whether upstream screening has *already* been applied to this feed is not stated; see section 5.

**Diurnal structure via local solar time.** Longitude is on every record and the timestamp is UTC, so local solar time is derivable arithmetically (UTC hour plus longitude ÷ 15). This is a genuine analysis the data supports without external inputs. It is also a trap: what you will actually be measuring is the *overpass* clock, not the fire's clock, unless you first establish the sampling cadence empirically from the timestamps themselves.

**Per-platform and per-product agreement and cross-check.** Because `satellite` and `source` are on every record, you can compare what different platforms and products report for the same place and near-same time. Do this as a *diagnostic* — to characterise how the streams differ — before doing it as a *measurement*, because the files do not establish that the streams are interchangeable.

**Persistence and re-detection.** Repeated detections near the same coordinates across overpasses give a duration-of-activity signal. Use a spatial tolerance, not coordinate equality: the schema gives pixel centres, not cells of a fixed named grid, and nothing establishes that the same ground location yields the identical coordinate pair on a later overpass.

**Feed-health monitoring.** `frp` is the one non-required member. Tracking its missing rate, and tracking gaps in acquisition times per platform, is worth doing continuously — both directly affect whether any of the above is valid on a given day.

## 3. Combination rules

**Fire radiative power (`frp`, megawatts).** A rate attached to a footprint, so it is extensive in area: **summable across distinct pixels observed in the same overpass**, and differenceable and comparable between records. Conditions and prohibitions:

- Do not sum across platforms or products for the same time window without deduplicating. Two satellites can see the same ground at nearby times; the files give no detection identifier and no linkage between records, so the feed cannot tell you whether two records are two fires or one fire seen twice. Deduplication must be positional and is therefore approximate.
- Do not sum FRP across time and call the result energy. FRP is a power; integrating it requires a duration per sample, and no member gives one. Summing a Monday value and a Tuesday value yields megawatts, not megawatt-hours, and it is not a bigger fire — it is the same fire counted twice.
- Averaging FRP is legitimate but answers a narrow question ("mean intensity of a detected pixel"), and is biased by the detection threshold, which is not described. Prefer medians and quantiles; the distribution's shape is not established by these files, so do not assume a mean is representative.
- Because `frp` is not required, a missing value is **not zero**. Sums must be reported alongside the count of contributing records, or they silently vary with completeness.

**Brightness temperatures (`brightness`, `bright_t31`).** Both are intensive — properties of the radiation from a footprint, not amounts of anything.

- **Never sum them.** A sum of brightness temperatures has no meaning.
- Differences and comparisons are valid *between records that are on the same scale*. Their **unit is not stated by the schema** — only the channel and wavelength are. The instance values (331.7, 295.4) are consistent with kelvin, but that is my inference, not something the files establish.
- The consequence: `brightness − bright_t31` **within a record** is safe, because a temperature difference is the same number in kelvin or degrees Celsius. Comparing that difference across records is safe for the same reason. But **ratios of these values, and any statistic that depends on where zero sits, are not safe**, because they change meaning depending on which scale is in use and the files do not fix the scale.
- Averaging brightness temperatures across pixels is arithmetically possible but should be area- or count-weighted deliberately and interpreted as "typical observed pixel temperature," never as the temperature of a fire. A radiometrically meaningful aggregate would require the pixel footprint areas, which are not on the record.
- Do not compare `brightness` against `bright_t31` as though they were the same measurement: they are different channels, and the schema treats them as a pair to be contrasted, not as interchangeable readings.

**Latitude and longitude.** Comparable, and differenceable as displacements with the usual spherical caveats.

- Arithmetic means of latitude and longitude are **not** a centroid. They fail across the antimeridian and distort near the poles; if you need a centre, average unit vectors and convert back.
- Any positional average is weighted by detection density, which is itself an artefact of sampling — so a "mean fire location" is a statement about where the satellite looked at least as much as where things burned.
- Do not treat the stated precision as accuracy. Four decimal places is roughly ten metres; the schema describes a **nominal one-kilometre** pixel and gives the *centre*, not the fire's position within it. Sub-kilometre spatial inference is unsupported. How much the true footprint departs from the nominal kilometre is not established here.
- Summing coordinates is meaningless.

**`satellite` and `source`.** Categorical labels; only equality comparison. They must be carried through every aggregation as grouping keys, because they are the only handle you have on which sampling regime produced a number. Pooling across them without first showing they agree is the most likely way to produce a wrong answer from this feed.

**Counts of records.** Countable, but they are counts of *detected pixels*, not of fires and not of area. Comparing counts between regions, days, or platforms compares observing opportunity as much as fire activity, and the feed supplies nothing with which to normalise that away.

## 4. Time

`acq_datetime` is the only temporal member and it establishes the axis. It is described as the **UTC acquisition instant of the overpass** — that is, the moment the *instrument observed*, not a property of the fire. This distinction is the whole of the section:

- The record carries **no valid-time interval** for the burning. There is no ignition time, no extinction time, no observation window, no duration. A fire's timeline can only be reconstructed as the envelope of the instants at which it happened to be detected, and that envelope is bounded by overpass opportunity, not by the fire.
- There is no ingest, receipt, or publication timestamp. **Latency is not measurable from the feed**, and you cannot distinguish "arrived late" from "detected late." If you need latency, you must stamp arrival yourself at the boundary.
- Positions on the axis are absolute UTC instants, so they are directly orderable and differenceable across all records regardless of platform or product — this is the one quantity that combines without qualification.
- Mapping to civil time requires a time zone you must supply from outside the feed; nothing on the record identifies one. For diurnal analysis, **local solar time** is preferable and is derivable in-feed from longitude, as noted above.
- The schema types this member as a plain string and describes it as "ISO-8601 form" in prose only. There is no format constraint and no declared pattern, so the serialisation is not guaranteed to be stable — trailing `Z` versus a numeric offset, presence or absence of fractional seconds. Parse defensively rather than by string slicing, and normalise to an instant before comparing.
- The example instant is at whole minutes with zero seconds. Whether the feed's timestamps are quantised to the minute, or that is a coincidence of one record, is not determined by a single instance — I would not build sub-minute logic on it.

## 5. Ambiguities

**Unit and scale of the two brightness temperatures — declining to decide.** The schema names the channels and wavelengths but never states kelvin or degrees Celsius, and the validation extension is declared without any constraint being used. My reading of the instance values as kelvin is a **guess** and I have kept every rule in section 3 robust to being wrong about it.

**Whether upstream false-alarm screening has already been applied — declining.** The schema says the temperature pair is used "to screen false alarms," but does not say whether this feed contains screened output, unscreened candidates, or a mixture. There is no confidence, quality, or version member, and additional properties are forbidden, so nothing on the record can settle it. This matters: it decides whether you may take a detection at face value.

**Detection threshold and minimum detectable fire — not determined.** Nothing in the files states what it takes for a pixel to appear here. Every distributional statement about FRP is therefore conditional on an unknown truncation.

**Actual pixel footprint — declining.** The schema's own word is "nominal." Whether footprints vary, and with what, is not established, and there is no scan/track dimension on the record. Consequently pixel *area* is unavailable, which rules out area-normalised intensities and any conversion of FRP to per-unit-area quantities.

**Comparability across `source` and across `satellite` — declining.** The schema gives `MODIS_NRT` as an example product and `T`/`A` as example platform codes but says nothing about calibration, threshold, or overpass-time equivalence between them. I will not assert they are poolable; I will not assert they are not. Treat this as a hypothesis to test empirically before pooling.

**The complete value domains — not determined.** "Such as `MODIS_NRT`" and "such as `T` ... or `A`" are illustrative. No enumeration is declared, so both fields must be handled as open sets and unknown values must not be silently dropped.

**Duplicate and revision semantics — declining.** There is no identifier, no sequence number, and no version. Whether the same detection can be delivered twice, and whether a later record ever supersedes an earlier one for the same pixel and instant, is unanswerable from these files. This is a real operational risk for any running FRP total; I would design the ingest to be idempotent on the tuple of product, platform, instant and coordinates, but that is a **defensive assumption**, not something the files license.

**Why `frp` is optional while the other measurements are required — not determined.** It could mean the retrieval sometimes fails, or that it is absent under some acquisition condition. The distinction matters for whether missingness is ignorable, and the files do not decide it. Treat missing FRP as informative until shown otherwise.

**Coordinate reference and datum details beyond WGS-84 — partially determined.** The datum is stated for both coordinates; nothing states whether coordinates are ever wrapped, normalised, or bounded, since no range constraints are declared. Validate ranges yourself.

**Geographic and temporal extent of the feed — not determined.** One record from one place on one day says nothing about whether this stream is global or regional, continuous or windowed. Do not infer coverage from the sample.


TRANSCRIPT D

# 1. What this feed is

Each record is a single **pixel-level thermal detection**, not a fire. It says that at one instant, one satellite instrument looking at one roughly one-kilometre patch of ground saw a thermal anomaly, and reports where that patch was, how hot it looked in two infrared channels, and how much radiative power was coming out of it.

The unit of observation is therefore *(pixel × overpass)*. A single wildfire burning for a week will appear as many records; a single record tells you nothing about how long anything has been burning, whether it burned before, or whether it will burn again. There is no fire identifier, no event identifier, no burn-area member, and no member that links one record to another. Any notion of "a fire" is something the analyst constructs downstream by clustering; it is not present in the data.

The records are also **presence-only**. There is no record for "this pixel was observed and was not burning", and no record for "this pixel was not observed at all". The absence of a detection is not evidence of absence of fire.

---

# 2. Analytics this stream supports

**Spatial clustering into fire complexes.** Coordinates are pixel centres in a stated geodetic reference (WGS-84), so detections from one overpass can be grouped by proximity into contiguous burning areas. This is the primary analysis the data supports, and it is supported because the geometry is unambiguous: a defined datum, a defined point semantics (centre, not corner), and a stated nominal footprint scale to calibrate the clustering radius against.

**Total radiative power of a fire complex at an instant.** Fire radiative power is a power, i.e. an extensive rate quantity attached to a pixel. Summing it over the pixels of one cluster in one overpass yields the radiative power of that complex. This is the one genuinely additive quantity in the feed.

**Intensity screening using the two-band pair.** The schema declares both temperature members as sensor bands under a single brightness-temperature calibration, and states explicitly that the pair exists to screen false alarms and gauge fire intensity. The difference between the short-wave band and the long-wave band is therefore a first-class derived quantity, not an incidental arithmetic result: it separates a genuinely hot sub-pixel source from a merely warm background.

**Comparison of the same region between platforms.** The platform code is marked as the observing procedure, which is the schema's way of saying that two records from different platforms are products of two different measurement processes. Because platforms differ, records from different platforms sample the same ground at different times, which supports looking at how a fire changed between two looks — provided the platform difference is treated as a stratification variable and not averaged away.

**Rate-of-change of a complex between consecutive overpasses.** Given clustering plus per-overpass FRP totals, the growth or decay of a complex can be tracked. The support here is weaker than the above and is conditional: it holds only where the same ground was actually observed in both overpasses, which this feed does not tell you.

**What the data does *not* support, despite looking like it does:**

- **Detection-count time series as a measure of fire activity.** Counts confound fire activity with observation opportunity. Nothing in the records states which ground was viewed, when, how often, or whether the view was obstructed. A drop in counts is equally consistent with rain, cloud, an orbital gap, or a feed outage. Any count-based trend line is a sampling artefact until an independent coverage record is joined in, and no such member exists here.
- **Burned area.** No area member, and detection is not extent.
- **Total energy released.** See §3.
- **Quality-filtered analysis.** There is no confidence, quality-flag, day/night, scan-geometry, or footprint-size member. Any workflow that assumes such filtering is available will have to source it elsewhere.

---

# 3. Combination rules, quantity by quantity

### Brightness temperatures (the two infrared bands)

**Comparable and differenceable, within the same band.** Both are on the kelvin scale, which is an absolute-zero-anchored ratio scale, so differences between two values of the *same* band are physically meaningful, and both bands share a declared common calibration basis.

**The cross-band difference is meaningful and intended.** Subtracting the long-wave value from the short-wave value within a single record is the designed use of the pair.

**Never average the two bands together.** The arithmetic mean of a four-micrometre brightness temperature and an eleven-micrometre brightness temperature is not a temperature of anything. The units match; the quantities do not. Matching units are not a licence to combine — this is the single most likely mistake with this feed, because a naive "average all the kelvin columns" pipeline will silently produce a number.

**Never sum brightness temperatures, across bands or within one.** A sum of temperatures is not a temperature and is not an energy. Temperatures are intensive; they do not accumulate over pixels.

**Averaging a single band across pixels is arithmetically valid and physically treacherous.** The mean is a mean of the reported quantity and nothing more. The files establish no linear relation between brightness temperature and radiated energy, so a mean brightness temperature must not be reported or reasoned about as a mean fire intensity or a mean energy. If you want energy-like aggregation, use FRP, which is the member that carries that meaning.

**Do not treat these as the temperature of the fire.** They are pixel-integrated brightness temperatures over a roughly one-kilometre patch that is mostly not on fire. Comparing one pixel's value to another compares two mixtures, not two flames.

### Fire radiative power

**Summable — under three conditions, all of which the analyst must enforce and none of which the data enforces.**

1. *Same acquisition instant.* Summing power values taken at different times adds instantaneous rates that never coexisted. The sum is not the power of anything at any moment.
2. *Same platform.* The platform is marked as the observing procedure. The files do not establish that the two platforms are mutually calibrated, so cross-platform sums mix measurement processes without a stated equivalence.
3. *Non-overlapping pixels.* The files describe a nominal one-kilometre pixel but do not state that pixel footprints tile the ground without overlap, and the word *nominal* signals that the real footprint is not fixed. Where two detections overlap on the ground, summing double-counts the shared radiance. This is an assumption you are making, not a fact the files grant.

**Averageable, but say which average you mean.** A mean FRP over the pixels of a cluster is a mean per-pixel intensity. It is not the intensity of the fire, and it moves in the opposite direction from the total when a fire spreads at constant per-pixel intensity: the total rises while the mean stays flat. Reporting the mean where the audience expects the total is a real and common error.

**Do not sum FRP over time to obtain energy.** Power integrated over time is energy, but integration needs a duration, and no member gives one. Each record is a rate at an instant; the interval it represents, the instrument dwell, and the gap to the next overpass are all absent. Multiplying FRP by an assumed interval is an assumption about orbital revisit that this feed does not supply, and it must be labelled as such if done.

**Missing FRP is not zero.** FRP is the only measurement member that is not required. Whether it is absent because it could not be retrieved, because it fell below a reporting threshold, or for some other reason is not stated. Consequently:

- A sum computed by coalescing missing FRP to zero is biased low by an unknown amount.
- A mean computed over only the records that have FRP is a mean over a self-selected subset, and if absence correlates with weak fires the mean is biased high.
- The correct handling is to report the number of records lacking FRP alongside any FRP aggregate, so consumers can see the size of the hole. Neither choice of imputation is defensible from these files alone.

### Latitude and longitude

**Comparable; usable for bounds, ordering, and distance.** They are on a stated datum, so they are mutually consistent across records.

**Differenceable only locally, and never as plain scalars.** A degree of longitude is not a fixed ground distance; it shrinks toward the poles. A difference in degrees is not a distance and must not be used as one. Distance requires a geodetic computation.

**Never summable.** Angular coordinates have no additive meaning.

**Averageable only with care, and the result is not what most people assume.** An arithmetic mean of coordinates gives an unweighted point that is not a centre of mass of the fire — it is a centre of the *detections*, so it is pulled toward whichever part of the fire happened to be resolved into more pixels. It also breaks across the antimeridian, where naive averaging of longitudes places the result on the opposite side of the planet. If a representative point is wanted, an FRP-weighted centroid is more defensible, but note that this silently discards every record with missing FRP.

**Areal densities are not computable.** Power per unit area needs a footprint, and no per-record footprint is given. Dividing by an assumed one square kilometre is an assumption, and the schema's own word *nominal* warns against it.

### Product source

**Not established as interchangeable.** The source identifies the product a detection came from. The files do not state that two different sources are mutually calibrated, share processing, or have the same detection sensitivity. Records should be pooled across differing sources only after a decision has been made externally to treat them as comparable, and that decision should be recorded. Pooling them by default is not supported by these files.

### Platform code

**A stratification key, not a payload value.** Because it is marked as the observing procedure, it identifies which measurement process produced the numbers. It should appear in every group-by that touches a measured quantity, and it should never be dropped on the grounds that the numbers "are all in kelvin anyway".

---

# 4. Time

The time axis is set by the acquisition instant, which is marked as the time of the phenomenon — that is, the time the world was in the reported state, not the time a record was written, ingested, or published.

**It is an instant, not an interval.** There is no start, no end, no validity window, no duration. Every record is a point sample. The thing described — a burning patch of ground — has a duration; the record does not. Nothing in the data tells you when a fire began, when it stopped, or whether it was burning between two records.

**The axis is irregular and instrument-driven.** Positions on it are determined by when a satellite happened to be overhead, not by any regular cadence. Consequently the sequence of records for a location is not a time series in the usual sense: it cannot be resampled, interpolated, or differenced as though the sampling were uniform, and a gap on the axis carries no information about the world.

**Relation to civil time.** Instants are given in UTC and are explicitly zone-anchored, so they are directly and unambiguously orderable and differenceable across records without any conversion — this is the one part of the feed with no hidden traps. But *local civil time at the fire* is **not derivable from these files.** Civil time depends on the political time zone and daylight-saving rules in force at that place on that date, and none of that is present. Deriving an offset from longitude is an astronomical approximation of solar time, not civil time, and it will be wrong by hours in many jurisdictions. I decline to give a rule for local time: it requires an external time-zone database, and that dependency should be stated explicitly wherever local-time reporting is required.

This matters because the analyses people most want — diurnal fire behaviour, "afternoon burning peaks", agricultural burning schedules — are all local-time analyses, and they cannot be done from this feed without joining external data.

**Precision is not stated.** The example instant lands on a whole minute with zero seconds. Whether that reflects true minute-level resolution, truncation, or a coincidence is not determined. Do not build logic that depends on sub-minute ordering.

**There is no record time.** With only a phenomenon time and no ingestion or publication time, latency is invisible, late arrivals are undetectable, and no bitemporal or as-of reconstruction is possible. If a record is ever revised or superseded, nothing here would let you tell.

---

# 5. Ambiguities

**Declining to decide:**

- **What a missing FRP means.** Not retrievable, below threshold, suppressed, or something else — the files do not say, and the three possibilities imply different and incompatible imputation strategies. This must be resolved from outside the feed before any FRP aggregate is trusted.
- **Whether the platform code set is closed.** Two codes are offered as examples. The phrasing is explicitly illustrative, so an unrecognised code is a live possibility and consumers must not fail on one.
- **Whether the two named product sources are intercalibrated.** Not stated.
- **Which of the two candidate short-wave channels supplied the value**, or whether that choice can vary between records. The schema names a channel pair for that member and does not resolve it. Whether the two channels are interchangeable for analysis is not determined here.
- **Whether records are unique.** There is no key, no identifier, and no stated uniqueness constraint. Whether the same pixel-overpass can arrive twice, and how a consumer should deduplicate if it does, is not determined. Deduplicating on the full value tuple is a workaround, not a documented guarantee.
- **Whether records are ordered or complete.** Neither delivery order nor completeness is addressed.
- **Whether pixel footprints overlap.** Bears directly on the validity of FRP summation, and is left open.
- **Local civil time**, as above.

**Guesses and assumptions, marked as such:**

- *Assumption:* the unit tokens carry their conventional meanings — arc degrees, kelvin, megawatts. The unit vocabulary is referenced by the schema but its definitions are not included in the material available to me, so I am reading the tokens conventionally rather than authoritatively.
- *Assumption:* the FRP value is the radiative power at the acquisition instant rather than an average over some retrieval window. The description calls it a rate and attaches it to an instantaneous acquisition, which supports this reading, but a dwell-averaged interpretation is not excluded by the text.
- *Guess:* the reason FRP is the only optional measurement is that its retrieval can fail where the two temperatures still succeed, i.e. it is a derived product downstream of them. This is inference from the required-set alone and should not be relied upon; it is offered only because it makes the missing-FRP handling question concrete.
- *Assumption:* records are additive event notifications rather than revisions of prior records, so a consumer can append rather than upsert. Nothing states this; nothing contradicts it either, and there is no key on which an upsert could be performed.

**Not ambiguous, and worth stating because it is often assumed to be:** the coordinates are unambiguously pixel *centres* on a stated datum, so no corner-versus-centre correction is needed and no datum shift should be applied. Extra members are prohibited by the schema, so a record carrying unexpected fields is invalid rather than merely unusual — a consumer that silently passes such records through is not conforming.
