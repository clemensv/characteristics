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

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order centroid_latitude, centroid_longitude. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. The tensor components are expressed in frame `None` and the tensor is `symmetric`, which fixes how many components are independent.
   wrong reading: Treating the components as independent numbers in an unspecified frame.

3. `centroid_time` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `centroid_time` as the time the record was produced, received, or published, or using a different member for event time.

4. `centroid_time` is calculated rather than measured directly.
   wrong reading: Treating `centroid_time` as a direct measurement.

5. Successive `centroid_time` values are expected at cadence `irregular`. A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

6. `centroid_latitude` is calculated rather than measured directly.
   wrong reading: Treating `centroid_latitude` as a direct measurement.

7. `centroid_latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `centroid_latitude`.

8. `centroid_longitude` is calculated rather than measured directly.
   wrong reading: Treating `centroid_longitude` as a direct measurement.

9. `centroid_longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `centroid_longitude`.

10. `centroid_depth` is calculated rather than measured directly.
   wrong reading: Treating `centroid_depth` as a direct measurement.

11. `depth_type` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `depth_type` as an observed quantity.

12. `half_duration` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `half_duration` as a measured observation.

13. `scalar_moment` is calculated rather than measured directly.
   wrong reading: Treating `scalar_moment` as a direct measurement.

14. `mrr` is calculated rather than measured directly.
   wrong reading: Treating `mrr` as a direct measurement.

15. `mtt` is calculated rather than measured directly.
   wrong reading: Treating `mtt` as a direct measurement.

16. `mpp` is calculated rather than measured directly.
   wrong reading: Treating `mpp` as a direct measurement.

17. `mrt` is calculated rather than measured directly.
   wrong reading: Treating `mrt` as a direct measurement.

18. `mrp` is calculated rather than measured directly.
   wrong reading: Treating `mrp` as a direct measurement.

19. `mtp` is calculated rather than measured directly.
   wrong reading: Treating `mtp` as a direct measurement.


TRANSCRIPT A

# 1. What this feed is

Each record is one **source solution for one earthquake**: a centroid-moment-tensor
solution as published by the Global CMT catalogue, transcribed out of that
catalogue's fixed-column `ndk` text form into named members. The specification,
which uses this same catalogue as its worked example, describes the population as
"a source solution for every significant earthquake" and describes the six tensor
elements as giving "the orientation and the size of the movement on the fault, in
dyne-centimetres."

The record is not a seismogram, not a phase pick, and not a hypocentre. It is the
*result of an inversion*. Almost every number in it is annotated `derivation:
calculated` — including the position and including the time — which under the
specification means it was produced by a deterministic calculation, not read off
an instrument. One value, the half duration, is annotated `modeled`, which the
specification reserves for values carrying information the observations do not
contain.

Two things a reader coming from a general earthquake catalogue will get wrong
unless told:

- The position in this record is the **centroid** position, an inversion output.
  The schema states explicitly that it differs from the hypocentre position, which
  comes from a separate location catalogue and is **not carried here**. The same
  holds for the time: the centroid time is not the origin time of rupture, and the
  reference hypocentre time it was derived from is not in the record either.
- The record deliberately omits things the source `ndk` record carries: the
  per-component standard errors, the reference hypocentre line, and the scaling
  exponents (the values here already have the exponent applied). The absence of
  the standard errors is the single most consequential omission, for the reason
  given in §3 and §5.

The record's own type is bound by `concepts` to `dcterms:Event` as an
RDFS class, so the thing described is an event, not a station, a sensor, or a
time series sample.

# 2. Analytics

**Per-record frame-invariant functions of the tensor.** This is the analysis the
feed is built for and the one it fully supports. The schema declares the two index
positions of a rank-2 tensor, the axes each index ranges over, the index of each
of the six carried components, and `symmetry: symmetric`. The specification states
what that buys: "the six numbers alone determine nine components only once the
schema has stated the frame, the index of each, and the symmetry." So all nine
positions are recoverable from every record without appeal to any packing or
Voigt-style ordering convention, and any function of the full tensor can be
computed per record. Whether the resulting number is comparable to the same number
from another record is a separate question, answered in §3.

**Scalar-moment analysis across records, including across catalogues.** The schema
singles this out: the scalar moment "is invariant under a change of frame where the
six components are not, so it is the member to compare between catalogues that
disagree about the frame." It is required in every record, carries a declared UCUM
unit, and is bounded below at zero. This is the one cross-record comparison the
files positively endorse. Note the flip side, also stated by the schema: it "is a
function of the tensor and adds no independent information," so it must not be
treated as a second, independent measurement alongside the components in any fit,
weighting, or error propagation.

**Spatial and temporal distribution of events.** Centroid latitude and longitude
are bound to EPSG:4326 with the axis order stated explicitly as latitude first,
longitude second. The specification's own appendix confirms that is the
authoritative order for that identifier and that `CRS84` is the same datum in the
opposite order. This annotation prevents the most common error in the whole domain
— reading a geographic pair transposed — and it does so for a consumer that would
otherwise have guessed from member names. Combined with the phenomenon-time member
and the declared irregular cadence, event locations can be mapped and sequenced.

**Depth analysis, but only on a filtered subset.** The depth-type member is
annotated `resultQuality`, and the schema explains why it qualifies rather than
describes: "a depth that was held fixed carries no information from this
inversion." Any analysis of the depth distribution, or of depth against anything
else, must therefore be restricted to records whose depth type is `FREE`. Records
whose depth type is `FIX` or `BDY` carry a depth that this inversion did not
produce. Critically, the depth-type member is **not** in `required`, so it may be
absent; the specification is explicit that "omission does not imply acceptable
quality," so absent records must be excluded, not assumed free.

**Catalogue-composition analysis.** The event name encodes, in its leading letter,
which data types entered the inversion. That is a real and useful stratification —
but see §3 and §5 for why it may be used for display and must not be used as a
machine-established procedure identity.

**Analyses this feed does not support, and why it is worth knowing in advance:**

- *Uncertainty-weighted anything.* No member carries an uncertainty. The
  specification forbids inferring an uncertainty from a `derivation` value. The
  standard errors exist in the source catalogue and were dropped here.
- *Revision tracking or point-in-time reconstruction.* There is no `status`, no
  `resultTime`, and no `ingestionTime`. Nothing distinguishes a first publication
  from a later replacement, and the specification states plainly that it "defines
  no record-versioning axis."
- *Centroid-versus-hypocentre offset.* Both files say the hypocentre exists and
  comes from elsewhere; neither puts it in the record.
- *Procedure-controlled comparison against another catalogue.* No
  `observingProcedure` is declared anywhere, and the specification calls procedure
  identity "comparability-critical."
- *Regressing half duration on scalar moment.* The schema states that the half
  duration is assumed "from an empirical relationship with the scalar moment."
  Fitting one against the other recovers the catalogue's own assumption, not a
  fact about earthquakes. This is a trap that looks like a discovery.

# 3. Combination rules

The governing background rule from the specification: a processor "MUST NOT infer
… permission to aggregate, convert, transform, reject outliers, or infer
causality." Nothing in this schema grants such permission. There is no `statistic`
anywhere, no `derivation: statistic`, and no `phenomenonTimeRelation`, so no value
in the feed is a summary of a set and nothing declares that summation over records
is meaningful. Everything below is therefore about what may be done *without*
misreading the data, not about what the schema authorises.

**The six tensor components (`mrr`, `mtt`, `mpp`, `mrt`, `mrp`, `mtp`).**

- *Within one record*: freely combinable. All six carry the identical UCUM unit
  `dyn.cm`, which is what the specification requires of members bound by one frame
  entry. Together with the declared symmetry they give the complete nine-position
  tensor, so any tensor arithmetic on one record is well founded.
- *Across records*: **do not sum, average, or difference componentwise, and treat
  even comparison as unfounded.** The frame is a local one. The specification says
  of exactly this frame construction: "up, south, and east are directions only once
  a point on the Earth is given," and it adds that this document "defines no member
  that binds a frame to the position that orients it, and a processor MUST NOT
  infer such a binding from the presence of both keywords on one type." The
  schema's own meta-type description does not say which point orients the frame.
  Two records at different centroid positions therefore cite the same *definition*
  of the axes without that establishing the same *directions*. `mrr` from an event
  under El Salvador and `mrr` from an event under Japan are projections onto
  different physical directions, and their difference is not a difference of
  anything. This is the single most expensive mistake available in this feed, and
  the values give no sign of it: the units match, the member names match, and every
  arithmetic operation succeeds.
- Both frame entries omit `variance`, which the specification defaults to
  `contravariant`, and the change of frame is the passive one — the quantity does
  not move, the frame does. Anyone re-expressing a tensor must use that rule rather
  than the covariant one.
- Three further cautions on the components. First, the diagonal is constrained:
  the schema states that under the zero-trace constraint "the catalogue applies by
  default," the three diagonal components sum to zero, and in the sample instance
  they do so exactly. The six components are therefore not six free numbers, and
  any degrees-of-freedom count, covariance estimate, or dimensionality reduction
  that treats them as six independent quantities is wrong. Second, for very shallow
  earthquakes the catalogue **holds `mrt` and `mrp` at zero**, marking that by a
  standard error of zero — and this record does not carry standard errors. A zero
  in those two members is therefore indistinguishable from an estimate that came
  out near zero. Any mean, variance, correlation, or histogram over `mrt` or `mrp`
  across a population is silently contaminated, and no member of the record lets
  you detect or exclude the affected records. Third, `mtp` sits at index [1,2]; the
  declared symmetry puts the same value at [2,1]. Nothing in the instance says so,
  and a consumer reading the instance alone would produce a different — wrong —
  tensor.

**Scalar moment.** Comparable and differenceable across records, and the schema
names it the member to use when comparing across catalogues that disagree about
the frame, precisely because it does not depend on the frame. Summing or averaging
it is a different matter: nothing in either file establishes that a sum of scalar
moments over a set of events is a quantity of anything, no `phenomenonTimeRelation`
of `accumulation` is declared, no `statistic` of `sum` is declared, and the
specification is explicit that these relations "do not authorize summation or prove
complete coverage." Summation over events also presupposes that the record set is
complete for the period and region, which nothing here asserts. Separately: it must
not be combined *with* the components as though independent, because it is a
function of them. And note that it carries the same unit as the components, so
`scalar_moment + mrr` is dimensionally legal and semantically meaningless — equal
units do not license combination.

**Centroid latitude and longitude.** Comparable across records: same registered
CRS, same declared axis order, same declared unit. They may be plotted and sorted.
They may **not** be differenced or averaged as if they were metres. The
specification states that the axes of EPSG-style geographic systems are angles
rather than directions, that the annotations define "no CRS, datum, coordinate
operation, or transformation," and that a processor "MUST NOT perform temporal,
coordinate, linear, or unit transformations without validating authoritative
definitions." A distance, a bearing, or a centroid-of-centroids requires a geodetic
computation these files do not supply. (Assumption, flagged: naive differencing of
longitudes also fails across the antimeridian; that follows from the axis being
angular, but neither file states the wrap rule.) Across *feeds*: this position is
the centroid and the schema says it differs from the hypocentre position of a
separate catalogue, so the two must not be differenced, averaged, or joined as the
same quantity.

**Centroid depth.** Comparable and differenceable **only within this feed and only
on the assumption that one reference surface applies to every record**, which the
schema asserts in prose ("measured downwards from the surface") but binds to no
definition. The specification is emphatic that the vertical binding "is the binding
that makes a height or a depth interpretable, because the number and its unit do
not state what the value is measured from," and that the axis direction is a fact
about the identified system. Here there is no vertical coordinate reference system:
the schema names only latitude and longitude in the CRS binding, and the
specification states that "properties not named by `coordinates` are not part of
the coordinate." So the depth is a bare number with a unit. It must not be fed into
a three-dimensional CRS as a height, and must not be sign-flipped into one; the
schema says so directly, noting that depth increases in the opposite sense to
ellipsoidal height. Across catalogues, do not compare depths at all without
external information about the reference surface. And, per the point above, do not
mix `FREE` depths with `FIX` or `BDY` depths in one distribution.

**Half duration.** Comparable and differenceable in seconds. But it is a
deterministic function of the scalar moment, not an independent quantity, so it
must not be used as evidence about source duration, must not be correlated with
moment, and must not be averaged as though it were a measured population. It is
also optional; its absence means undeclared and must not be read as zero.

**Depth type.** A code, not a scale. The specification states that for
`resultQuality` it "defines no threshold, ordering, confidence model, or processing
effect." `FREE`, `FIX`, and `BDY` are therefore not rankable — you may partition on
them, you may not order them, and you may not compute anything numeric from them.
There is a further scoping subtlety: the specification says that where a record
carries more than one result, "a `resultQuality` on the record qualifies all of
them, and qualifying one result on its own requires modelling that result as a
nested object." This record carries many results, and the depth type is not nested.
So the machine-established reading is that it qualifies every result in the record,
while the schema's prose says it qualifies the depth alone. See §5.

**Event name.** Usable as a label. **Not** usable as an identity: the specification
forbids inferring "node identity" from a concept binding, and the binding to
`dcterms:identifier` is a concept binding. No `identity` is declared on the type,
so nothing establishes that the name is unique across records or that two records
sharing one name are one thing. The schema also calls it the identifier of *the
solution*, not of the earthquake. Its leading letter encodes which data types
entered the inversion, but the specification forbids inferring an
`observingProcedure` "from a name, label, description, type, unit, position, or
sample," so grouping or stratifying by that letter is a decision you take on your
own authority, not something the schema underwrites. Parsing it is unsafe in
another way too: the schema says *current* events use the fourteen-character form,
which implies older ones do not and does not say what they use.

**Across this feed and any other feed.** The observed-property reference points at
`catalog.example.org`, and the specification says such a reference is
"indeterminate" while unresolved and "MUST NOT be repaired from labels, mappings,
result schemas, units, descriptions, property names, or samples." There is also no
declared feature of interest and no declared procedure. So no annotation in this
schema establishes that another producer's moment tensors quantify the same
observable property, concern the same feature, or were produced by a comparable
procedure. Cross-catalogue work is possible — the schema tells you to reach for the
scalar moment — but it rests on your judgement, not on a check any processor could
perform.

# 4. Time

The time axis of the thing described is established by **one member, the centroid
time**, annotated `semanticRole: phenomenonTime`. That role is the specification's
"time during which the result applies to the observed property," as distinct from
the time a result became available or the time a system received it — neither of
which this record carries.

What that instant *is*, precisely, matters and the schema states it: it is the
instant about which moment release is centred. It is **not** the time rupture
began, and it is **not** the reference hypocentre time. It is annotated
`derivation: calculated` because the catalogue publishes an offset and this member
is the result of adding that offset to a reference time held on a different line of
the source record — a line this feed does not carry. So the number is arithmetic,
not observation, and its components are not recoverable from the record.

**Relation to civil time.** The member is Core `datetime` and carries no
`temporalReferenceSystem`. The specification states that "Core temporal types need
no annotation when their Core semantics are fully intended," and conversely that "a
non-Core or ambiguous encoding is indeterminate without one." So the omission is
correct rather than missing, and positions on this axis are ordinary civil-time
instants read under Core's own `datetime` semantics — in the sample, an RFC 3339
form with a `Z` offset and one decimal of a second. This is not a counted clock: no
meta-type, no epoch count, no `sortOrder`, no conversion required. Positions order
under the Core type's own ordering, and comparing two of them across records is
sound. What the two files in front of me do **not** do is name a time scale: no
`ogc-trs` binding to UTC, TAI, UT1, or GPS is present, although the specification
lists those as available. The exact scale is therefore whatever JSON Structure Core
fixes for `datetime`, and Core is not one of the files I have.

**What the axis does not give you.** No `phenomenonTimeRelation` is declared on any
result, and the specification says flatly that "omission is not `instant`." So the
schema does not state that the tensor applies *at* the centroid time. The schema
says the omission is deliberate: the half duration exists because "the solution
integrates moment release over a source duration." But no `supportPeriod` is
declared either — and it could not have been, since the specification prohibits
`supportPeriod` unless `phenomenonTimeRelation` is `interval` or `accumulation`.
The consequence is precise and worth stating to anyone building windows: **the
extent of the period each result characterises is undeclared.** The half duration
sits in the record as a separate result, and no keyword binds it as the support of
the tensor. Constructing an interval of twice the half duration centred on the
centroid time is an inference the annotations do not license; if you do it, do it
knowingly.

The cadence is declared `irregular`, with no period — the schema's justification is
that "earthquakes are not scheduled." The specification is clear about what a
cadence is and is not: an expectation about a producer, not a constraint on
instances, "not delivery time, a service-level objective, a completeness
assertion, or a phenomenon-time boundary," and no assertion that a successor
record exists. Under `irregular` there is nothing to sanity-check arrival timing
against, no basis for a staleness threshold, and no basis for calling an interval
without records a gap.

# 5. Ambiguities

**Which point orients the tensor frame.** *Declining to decide.* The frame's axes
are up, south, and east, which are directions only relative to a point on the
Earth. The meta-type's description states the axis order and its provenance but
never says which point orients it. The specification's own worked version of this
same frame says so explicitly in its meta-type description; this schema's does not,
and the specification forbids inferring the binding from the co-presence of the
coordinate annotation. *Guess, marked as a guess:* the intended orienting point is
almost certainly the centroid position carried in the same record. I am not
treating that as established, and §3 is written as if it is not.

**Whether the record-level observed property really applies to every result.** The
rule is not ambiguous — the specification says an `observedProperty` on a record
"identifies the observable property of every result in that record that does not
carry one of its own," and no member here carries one of its own. So the schema
formally asserts that the centroid latitude, the centroid depth, and the half
duration are all results quantifying the seismic-moment-tensor observable property.
*Guess, marked as a guess:* that is a modelling slip rather than an intention. I am
not repairing it, and a consumer joining on observed-property identity should know
that the assertion is broader than the prose reads.

**Whether the depth type qualifies the depth or every result.** *Declining to
decide.* The prose says the depth; the specification's scoping rule says every
result in a record with more than one. The two disagree, and only nesting the depth
in its own object would have settled it.

**What "the surface" is for the depth.** *Not determined.* No vertical reference
system is bound, and the prose names no datum, ellipsoid, or sea level.

**What "very shallow" means, for the components held at zero.** *Not determined.*
No threshold is stated, no flag is carried, and the standard errors that would have
marked the constrained values are not in the record. There is no way to identify
affected records from the data.

**Whether the zero-trace constraint was applied to any given record.** *Not
determined.* The schema says the catalogue applies it "by default," which implies
it is sometimes not applied, and nothing in the record says which case obtains.
The sample instance happens to satisfy it exactly.

**Whether a record is a first publication or a replacement.** *Not determined.* No
status, no result time, no ingestion time, no version member.

**The time scale.** *Declining to decide* on the evidence of these two files. The
absence of a temporal reference system is the correct encoding for full Core
semantics, but Core is not in front of me, so I will not name the scale.

**Absence of the two optional members.** *Not determined, and no default exists.*
Depth type and half duration may be absent. The specification says omission "means
undeclared unless stated otherwise" and "never implies compatible, successful, or
acceptable data." Do not default the depth type to `FREE`, and do not default the
half duration to zero.

**What entity the record is about.** *Not determined.* No `featureOfInterest` is
declared. The record's type is bound to `dcterms:Event`, which gives the domain
class of the record but no identity for the earthquake, and the specification
forbids inferring a feature "from a name, label, description, type, unit, position,
or sample."

**Whether the event name is a key.** *Not determined.* No identity is declared, and
node identity may not be inferred from the identifier concept binding.

**Older event-name formats.** *Not determined.* The schema says *current* events
use the fourteen-character form and does not describe any other, so name parsing
has an unspecified failure domain.

**The mixture of `unit` on the angles and `ucumUnit` elsewhere.** *Declining to
decide.* Both are keywords of JSON Structure Units, which the specification cites
normatively but which is not one of the two files I have. Whether they are two
spellings of one thing or two distinct registries is not decidable here, and it
matters to anyone writing a unit-checking consumer.

**Precision of the published values.** *Observation of one sample, not a schema
fact.* The single instance carries mantissas at three decimal places, consistent
with the fixed-column origin the schema describes. Nothing in the schema constrains
precision, and the specification explicitly forbids inferring anything from a
sample. Do not build a rounding or tolerance rule on this.

**One forward-looking hazard.** The schema activates the Alternate Names extension.
The specification states that a serialization-facing rename "changes how the member
appears in an instance document and does not change the identity the annotation
binds," and that a processor "MUST NOT resolve a member name stated in an
annotation against such a name." So if this feed ever ships localized or renamed
wire names, the tensor index bindings remain correct while a consumer joining on
wire member names silently breaks. At present the extension is used only to gloss
the three depth-type codes, so nothing is at risk today.


TRANSCRIPT B

# 1. What this feed is

Each record is one **solution**, not one measurement and not one earthquake. It is a centroid-moment-tensor result produced by an inversion, published by the Global CMT catalogue and transcribed here out of a fixed-column text format into named members. What the inversion produces is a symmetric second-rank tensor describing seismic moment release, together with the position and instant about which that release is centred and how deep the centroid sits.

Two things follow immediately and both are easy to get wrong. First, the position and time in a record are *inversion outputs*, not observations of where and when something was detected — the record's own material says the centroid latitude and longitude differ from the hypocentre coordinates, which come from a different catalogue entirely. If you join this feed to a location catalogue on event identity and difference the coordinates, the offset you get is a real difference between two different quantities, not a discrepancy to be reconciled. Second, the solution is not instantaneous: it integrates moment release over an assumed source duration, and the record says so explicitly as the reason its tensor members do not claim an instantaneous time relation.

A record is also a *statement about an inversion*, and the inversion's inputs vary between records. The leading letter of the event name records which data types entered it (body waves only, surface waves only, mantle waves only, or a combination). Records with different leading letters rest on different evidence and should not be pooled without stratifying.

# 2. Analytics

**Spatiotemporal mapping and depth cross-sections.** The centroid coordinates carry a declared geographic CRS and the centroid time is declared as the phenomenon time of the thing described on an absolute scale, so events can be placed on a map and on a timeline without further metadata. Depth is a separate downward-positive quantity and supports cross-sections, but see the caveat in §3 about which surface it is measured from.

**Depth distribution, restricted by provenance.** The record carries a qualifier saying whether the depth was inverted for, held fixed, or fixed from broad-band waveform modelling. This is what makes a depth histogram defensible: you can drop the depths that were held fixed, which by the record's own statement carry no information from this inversion and would otherwise pile up at whatever values the catalogue chose. Without that filter a depth distribution is partly a picture of the catalogue's fixing policy.

**Moment budgets by region and time window.** The scalar moment is frame-invariant and has a true zero with a stated minimum of zero, so it is a ratio-scale magnitude: ratios, geometric means, and binned totals are all defined on it. It is also the one quantity the record itself nominates for comparison against other catalogues, precisely because it survives disagreement about the tensor frame.

**Per-record source characterisation via frame-invariant quantities.** The six published components plus the declared symmetry determine all nine positions of the tensor, so a full tensor can be reconstructed from every record and decomposed. This is the correct route to any cross-record comparison of mechanism: compute rotation-invariant quantities (eigenvalues, invariants, any frame-independent decomposition) *per record first*, then compare those. See §3 for why comparing raw components across records is not equivalent.

**Inter-event interval statistics.** The time axis is declared irregular with no period, and the values are absolute instants, so successive differences are genuine elapsed times between events. This supports interval distributions, clustering-in-time tests, and burst detection.

**Structural quality control.** Three checks are available from the files alone: the three diagonal components should sum to zero under the catalogue's default constraint (the sample record satisfies this exactly — 0.838 − 0.005 − 0.833 = 0), depth and half-duration and scalar moment must be non-negative, and the tensor is symmetric by declaration so no independent check of the off-diagonal pairs is possible or needed. A non-zero trace is a flag worth raising but not automatically an error, because the constraint is described as a default rather than as invariant.

**Stratified comparisons.** Both the inversion data type (from the event name's leading letter) and the depth provenance are available as grouping variables. Any comparison of depths, durations, or mechanisms that does not stratify on both is comparing populations produced by different procedures.

**Analyses this feed does not support.** Anything requiring uncertainty: the record states that the catalogue publishes an estimated standard error beside each component and that this record does not carry them. So no uncertainty-weighted averaging, no chi-square or goodness-of-fit on components, no test of whether a component differs significantly from zero. Anything requiring catalogue completeness — no detection threshold, no reporting-coverage information, and nothing about which events are present — so event-rate trends and magnitude-frequency statistics cannot be defended from these files. And, specifically, do not regress half-duration on scalar moment: the record says half-duration is assumed from an empirical relationship with the scalar moment rather than derived from the analysis, so such a regression recovers the catalogue's own assumption and tells you nothing about earthquakes.

# 3. Combination rules

**Event name.** Equality only — it is the catalogue's stable identifier for the solution, so it is a join and de-duplication key. Do not order on it: the record says the fourteen-character form applies to *current* events, so lexical sort is chronological only over whatever subset uses that form, and the boundary is not given. Do not parse a timestamp out of it (see §5). Not summable, not averageable.

**Centroid time.** Differenceable across records — both endpoints are absolute instants on the same scale, so a difference is an elapsed duration between two events. Comparable and sortable. Averageable arithmetically after conversion to an epoch, though the mean of a set of event times is rarely the quantity anyone wants. **Not** resamplable to a fixed grid and **not** to be gap-filled or interpolated: the cadence is declared irregular with no period, so an absence of records over an interval is not a missing sample. Successive differences are inter-event intervals, never a sampling interval.

**Centroid latitude and longitude.** Comparable and combinable with each other and across records because they share one declared CRS. But they are *angular* coordinates: an arithmetic difference is a difference in angle, not a ground distance, and converting to distance requires a geodetic computation the files do not supply. Averaging them gives a mean in angle space, which is acceptable for coarse binning and wrong near the poles. The sample longitude is negative, so a signed convention is in use; any signed longitude convention is cyclic, so naive means and differences across the wrap point are wrong — I treat the exact range as an assumption, not something the files state. Do **not** combine these with hypocentre coordinates from another catalogue as if they were the same quantity; the record says they are not.

**Centroid depth.** Comparable, differenceable, summable and averageable across records **on two conditions**: that the depth provenance qualifier is the same or at least excludes the held-fixed cases, and that the depths share a common reference surface (not established — see §5). Depths from records where depth was held fixed must be excluded from any distributional analysis, because the record states such a depth carries no information from this inversion; including them creates artificial modes. Depth must **not** be combined arithmetically with any ellipsoidal or geodetic height, and must not be appended to the latitude/longitude pair to form a three-dimensional coordinate: the record explicitly refuses to bind depth to the declared CRS on the grounds that the CRS has no vertical axis and that depth increases in the opposite sense to height. Mixing the two without negating one of them produces sign errors that will not look like errors.

**Depth type.** Categorical. Equality and grouping only; no arithmetic of any kind. It is optional, so an absent value means the provenance was not stated — it must not be imputed as "inverted for".

**Half duration.** Dimensionally comparable, differenceable and averageable across records in seconds. But it is a *modelled* quantity, assumed from an empirical relationship with the scalar moment. Consequently: it is not an independent variable with respect to the scalar moment and must never be paired with it in a regression or correlation; variation in it across records is variation in scalar moment pushed through a fixed formula, not observed variation in source duration; and its mean over a set of records is a transform of that set's moments. It is optional, so it will be absent for some records.

**Scalar moment.** The most freely combinable quantity here. Comparable across records, across frames, and across catalogues — the record nominates it for exactly that role because it is frame-invariant where the components are not. Ratio-scale (true zero, stated minimum of zero), so ratios and geometric means are meaningful. Summing is arithmetically defined and is the natural way to build a released-moment budget over a region or window. But that sum must **not** be read as the scalar moment of a combined source. That follows from the files themselves: the trace of the tensor is zero by the catalogue's default constraint, so no non-trivial frame-invariant *linear* functional of the components survives, and a frame-invariant scalar moment therefore cannot be linear in the tensor. The scalar moment of a summed tensor is not the sum of the scalar moments. Separately: do not feed the scalar moment and the six components into the same model as independent inputs — the record states the scalar moment is a function of the tensor and adds no independent information, so they are collinear by construction.

**The six tensor components (mrr, mtt, mpp, mrt, mrp, mtp).** All share one unit, so they are dimensionally combinable, and within a single record they fully determine the tensor: the declared symmetry places each off-diagonal value at both of its index positions, and the zero-trace default makes the three diagonal values sum to zero. That last point means the six values are **not** six independent variables — under zero trace only five are free, and any statistical method that assumes independent inputs will misbehave on all six.

The important restriction is across records. The frame is defined by directions — radially outward from the Earth's centre, towards increasing colatitude, towards increasing longitude — and all three of those directions depend on where on the sphere you are standing. Two records at different centroid positions therefore resolve their components onto physically different axes even though the member names are identical. Componentwise differencing, summing, averaging, correlating, or clustering across records at different locations mixes quantities measured along different directions, and the files provide no rotation to a common frame. This is the single largest trap in the feed, and it fails silently: the arithmetic runs and produces plausible-looking numbers. The correct procedure is to reduce each record to frame-invariant quantities first and compare those. Componentwise aggregation is defensible only for records close enough together that the frame difference is negligible for your purpose, and the files give no basis for choosing that threshold.

Two further prohibitions on the components. They must not be compared against another catalogue's components unless that catalogue resolves on the same axes in the same order — again, the scalar moment is the safe cross-catalogue quantity. And no uncertainty-weighted combination is possible at all, because the per-component standard errors the catalogue publishes are not carried here.

**A specific hazard in mrt and mrp.** For very shallow earthquakes the catalogue holds these two components at zero rather than inverting for them, and marks that by a standard error of zero. This record does not carry standard errors. So a held-zero and a genuinely near-zero value are indistinguishable in this feed, and there is no member that lets you separate them. Any distribution, correlation, or mechanism classification that leans on these two components is contaminated by constrained values you cannot detect. The sample record has both non-zero and a centroid depth well away from the surface, so it is not such a case, but the files do not define "very shallow", so you cannot construct a depth filter that is known to be correct.

**Unit note (not from the files).** The moment members are annotated in dyne-centimetres, a CGS unit. Any comparison against values expressed in newton-metres needs a conversion; the conversion factor is unit-system knowledge, not something these two files establish, and I flag it rather than assert it as part of the feed's content.

# 4. Time

**The centroid time is the time axis**, and it is the only time in the record. It is declared as the phenomenon time — the time of the thing described — so it positions the earthquake, not the analysis, the publication, or the ingest.

Three properties of that axis matter for analysis.

*It is a centre, not an onset.* The record says plainly that this is the time about which moment release is centred and not the time rupture began. Combined with the assumed source duration carried in the half-duration member, the tensor describes release integrated over an interval, and the record explicitly declines to claim an instantaneous time relation for the tensor members. Treat each record as an interval-centred aggregate. Differences between this time and an origin time taken from any other catalogue are systematic and expected, not error.

*It is derived, not read off.* The catalogue publishes an offset, not an absolute instant; this member is the reference hypocentre time from one source plus that offset from another. Its accuracy is therefore inherited from two upstream quantities, and it is not independent of whatever hypocentre catalogue supplied the reference.

*It has no period.* The cadence is declared irregular. Events are not scheduled, so there is no sampling interval, no expected spacing, and no basis for resampling, interpolating, or gap-filling. An interval with no records is an interval with no earthquakes in the catalogue, not a dropout.

**Relation to civil time.** The sample value is written as an instant with an explicit UTC designator and one decimal place of seconds, so positions on the axis are absolute instants in UTC and no local-time, offset, or daylight-saving reasoning applies to them. Binning into local days or local hours requires a timezone rule you must supply from outside these files, and requires a decision about *which* place's local time — for a global feed, the sensible choice is the event's own longitude, but nothing in the files decides that. I have one instance, so "every value is UTC with a Z designator" is an assumption on my part, not something the schema constrains; the type permits an instant but I cannot see from here whether non-UTC offsets or varying sub-second precision occur.

**Do not take the time from the event name.** The name embeds a year, month, day, hour and minute, and in the sample they agree with the centroid time to the minute. But the record says the centroid time is a hypocentre time plus an offset, and does not say which of the two the name encodes; the sample cannot separate them because the offset there is only a few seconds. Parsing the name is also unsafe across the catalogue's history — see §5.

# 5. Ambiguities

**Declining to decide:**

- *Which surface centroid depth is measured from.* "Downwards from the surface" does not say whether that surface is the ellipsoid, a geoid, mean sea level, or local topography. This is not decidable from the files and it matters: under strong topography or bathymetry, depths from different regions are on different data and are not strictly comparable, and no three-dimensional point can be constructed without a vertical datum the files do not supply.
- *The threshold for "very shallow"* at which the two off-diagonal components are held at zero. Not given, and no flag in the record marks affected rows. There is no correct filter to write.
- *When the zero-trace constraint is relaxed.* It is described as applied "by default", which implies exceptions, but the conditions are not given. A non-zero trace is therefore uninterpretable: possibly a corrupt record, possibly a legitimate unconstrained solution.
- *The exact function relating the scalar moment to the six components.* The record says the scalar moment is a function of the tensor but does not give the function. You therefore cannot recompute it, cannot cross-validate it against the components, and cannot detect a transcription error in either.
- *The meaning of the event name's trailing character* (an "A" in the sample, shown as a placeholder in the stated form). Not explained. A plausible reading is disambiguation between solutions in the same minute, but that is speculation and I am not asserting it.
- *Which records use the fourteen-character name form.* The description says "current events" use it, which means older ones do not, but does not say what they use or where the boundary falls. Name-parsing code cannot be assumed safe over the whole catalogue.
- *Whether the event name is unique, and whether revised solutions reuse it.* It is called a stable identifier for the *solution*, which leaves open whether one earthquake can yield several records — and if it can, whether they are distinguished by the leading data-type letter. This directly affects de-duplication and, more seriously, independence: if the same earthquake appears more than once, records are not independent samples and any count-based or averaged statistic is inflated. I cannot resolve this from the files and I am not going to assume either way.
- *What absence of the two optional members means.* Neither the depth provenance qualifier nor the half-duration is required. Whether absence signals "not applicable", "not published", or a defaulted value is not stated. Do not impute.
- *Catalogue completeness and selection.* Nothing describes which events are included, a magnitude or moment threshold, or how coverage varies in space or time. Any analysis of event counts or rates rests on an unstated selection function.

**Marked as guesses or assumptions:**

- *(Assumption)* Every centroid time is UTC with the same designator and comparable sub-second precision. Based on one instance; the schema does not constrain it.
- *(Assumption)* Longitude runs on a signed range that wraps, so antimeridian handling is required. The sample's negative longitude establishes the sign convention; the range and wrap behaviour are my inference from that, not a statement in the files.
- *(Assumption)* The angular unit annotation on the coordinates and the unit annotations on depth, duration and moment are drawn from compatible unit vocabularies. They are expressed through different annotation keys, which is worth checking before turning automated unit conversion loose on this feed.
- *(Guess)* Because the tensor components are described as published against a scaling exponent and the sample carries them already multiplied out, I read the values in this record as absolute quantities in the annotated unit, with no exponent still to apply. The sample's diagonal summing exactly to zero and its scalar moment sitting at the same order of magnitude as the components are consistent with that reading, but neither confirms it.


TRANSCRIPT C

# 1. What this feed is

Each record is one published *solution* for one earthquake: a moment tensor obtained by inversion, together with the place, depth and time at which the moment release is centred. The records come from the Global CMT catalogue and are a transcription of that catalogue's fixed-column `ndk` records into named members.

The important framing point — and the one most likely to be missed — is that a record is **not an observation of an earthquake**. It is the output of a fitting procedure, and several of its members are results of that fit, not measurements: the location, the depth and the time are all inversion products, and they are explicitly stated to differ from the hypocentre location and time, which come from a *different* catalogue and are not carried here. The name is a stable identifier for the solution, and its leading letter encodes which data classes went into the inversion (body, surface, mantle, or a combination), so the identifier doubles as a method covariate.

The record is also a *reduced* transcription. The source catalogue publishes an estimated standard error beside every tensor component; none of them are here. It also publishes the hypocentre time and the centroid offset separately; only their sum is here. Anything that needs uncertainties, or needs the offset, has to go back to the `ndk` source.

# 2. Analytics worth running

**Where and how deep moment is released.** Centroid coordinates plus a scalar size measure support mapping and depth profiling directly. Depth has a stated true zero (the surface) and a stated positive sense (downwards), so depth differences and depth histograms are well defined — subject to the conditioning in the next section.

**Moment release totalled over time and space.** The time member is an absolute instant and the scalar moment is on a ratio scale with a true zero, so summing moment inside spatial or temporal bins is a meaningful aggregate. This is the natural way to turn an event list into a rate, and it is the only way, because the series has no period (see §4) and so cannot be differenced or interpolated as a regular time series.

**Size distribution.** Scalar moment is comparable across records without qualification, because it is stated to be frame-invariant. Counting events above moment thresholds, or fitting the upper tail, is supported by the data as given. What is *not* supported from these two files is any statement about detection completeness — nothing here establishes a threshold below which the catalogue stops being a census, so a threshold you choose is an assumption you are making, not one the data justifies.

**Mechanism comparison.** Dividing the six components by the scalar moment yields a dimensionless tensor that separates size from geometry — legitimate, since both are on the same unit. This is worth doing, but it is the analysis with the most traps in it (§3).

**Stratification by inversion input and by depth treatment.** The leading letter of the name and the depth-type member are the only quality/method covariates present. Any headline result should be recomputed within each stratum; if the answer moves with the inversion inputs or with whether depth was free, the result is partly an artefact of processing.

**Constraint audits as a data-quality screen.** Two cheap checks fall out of what the schema states. First, the three diagonal components should sum to zero, because the catalogue applies that constraint "by default" — the word *default* implies exceptions, and finding them tells you which records were treated differently. In the example record the sum is exactly zero (0.838 − 0.005 − 0.833 = 0.000, in units of 10²³). Second, the scalar moment is stated to be a function of the six components, so it should be recomputable; records that depart from whatever function you fit are worth inspecting. Note the caveat in §5 — I could not recover the function from these files, and the obvious candidate does not reproduce the published value.

**Detecting artificially-zeroed components.** Two of the off-diagonal components are held at zero for very shallow earthquakes, and the flag that marks this (a zero standard error) is absent from this record. Exact zeros in *both* of those members are therefore a usable heuristic for "this solution was constrained, not measured". I mark this as a heuristic, not a rule: the files do not say the constrained case is the only way those members can be exactly zero.

# 3. Combination rules

**The six tensor components — the critical case.** These must **not** be compared, differenced, summed or averaged across records at different centroid locations. The axes are named as *up*, *south* and *east*. Those are directions defined relative to a point on the Earth, so the frame rotates from event to event; two records at different coordinates express their tensors in different bases and their components are not commensurable. The schema corroborates this from the other side when it says the scalar moment "is invariant under a change of frame where the six components are not." (This conclusion is an inference — from the axis naming plus the presence of per-record coordinates — rather than a sentence the files state outright. It is the single largest failure mode for anyone stacking these records into a matrix.)

Component-wise arithmetic *is* valid between records at the same location, and is valid more generally only after an explicit rotation into a common frame. Such a rotation is computable in principle from the latitude and longitude each record carries, but see §5: the files do not fix whether "up" is the ellipsoid normal or the geocentric radial direction, and that choice changes the result.

Three further constraints on these six:

- The three diagonal components carry only two degrees of freedom under the imposed zero-trace constraint. Do not feed all three into a model as independent inputs; the design matrix is singular by construction. Equally, do not read a near-zero trace as an empirical finding — it was imposed, not measured.
- Only six values are published for nine positions because the tensor is symmetric. Reconstructing the full array requires mirroring the three off-diagonal values; loading six numbers into nine slots without mirroring silently produces a different tensor.
- The scalar moment is a function of these six. Do not use it as an independent feature alongside them.

**Scalar moment.** Comparable across records and, per the schema, the correct member to compare across catalogues that disagree about the frame. Ratio scale with a true zero, so ratios are meaningful. Summing is defensible as an aggregate of released moment; be aware that the sum of scalar moments is not guaranteed to equal the same scalar function applied to a summed tensor, and since the files do not state that function you cannot check. Averaging is arithmetically valid but the files establish nothing about the distribution, so report totals and quantiles rather than relying on a mean.

**Units.** The moment members are annotated dyne-centimetres, which is CGS. Combining these values with any source on newton-metres without conversion is wrong by seven orders of magnitude. The conversion factor is elementary unit arithmetic, not something these files supply; they supply only the unit annotation, which must be honoured. No magnitude scale is defined here, so do not convert to a magnitude — the relation is not in the files.

**Centroid depth.** Ratio scale, kilometres, positive downwards, floor at zero. Differences and averages are meaningful in kilometres. Two conditions. First, condition on the depth-type member: a depth that was held fixed is stated to carry no information from the inversion, so it must be excluded from, or flagged in, any depth statistic — otherwise the distribution acquires spikes at whatever preset values were imposed. Second, depth must **not** be differenced against ellipsoidal heights, elevations or terrain models: the schema states plainly that depth is outside the record's coordinate reference system, that that system has no vertical axis at all, and that depth runs in the opposite sense to ellipsoidal height. Which surface depth is measured from is not stated (§5), so there is no vertical datum here to align to.

**Latitude and longitude.** Comparable; equality and proximity tests are fine. Plain differencing and plain averaging are unsafe in the usual ways — longitude wraps, and the arithmetic mean of scattered angular coordinates is not a position on the sphere. Summing is meaningless. These two are the only members inside the stated coordinate reference system; do not assemble them with depth into a three-component coordinate.

**Centroid time.** Differences are meaningful and yield durations. Sums are meaningless. Comparison across records is unambiguous because the instants are absolute. See §4 for what the axis will and will not support.

**Half duration.** Seconds, ratio scale, arithmetically combinable — but analytically it is not data. The schema states it is *assumed* from an empirical relationship with the scalar moment rather than derived from the inversion. It is therefore a deterministic re-expression of the scalar moment and carries no independent information. Regressing it against moment recovers the assumed relation; correlating it with anything else is correlating moment with that thing under another name.

**Depth type.** Nominal. Group-by and filter only; no ordering, no arithmetic.

**Event name.** Nominal identifier; equality only. Do not sort by it to obtain time order — the leading character encodes the inversion inputs, not time, so a lexical sort orders by method first. Do not parse the embedded date-time out of it either; use the time member, and see §5.

**Missingness.** All members except depth type and half duration are required, so only those two need absent-value handling. Absence of the depth type should be treated as *unknown*, not as *free* — nothing in the files licenses that default.

# 4. Time

The centroid time member is the time axis. It is the instant about which moment release is centred, and it is formed by adding the catalogue's centroid offset to a hypocentre reference time that this record does not carry — so the offset itself, which is a quantity of interest, cannot be recovered from a record alone.

It is *not* the time rupture began. Differencing it against an origin-time catalogue produces a real physical offset, not a clock discrepancy or a data error.

Position on the axis relates to civil time directly: the instants are absolute and, in the example, carry a zero UTC offset, so they map onto civil time without any zone assumption. Local civil time at the epicentre is neither carried nor derivable — time zones are political boundaries and no zone information is present. (You could compute a local *solar* time from longitude; that is geometry, but it is an import from outside these files and it is not civil time.)

Two properties of the axis constrain what can be done on it:

*It is not a sampled series.* The schema is explicit that successive values carry no period. There is no sampling interval, so there is nothing to resample, interpolate or lag-difference. Rates must come from aggregation into bins or from point-process treatment. Nothing establishes that records arrive in time order.

*The values are not instantaneous.* The tensor is stated not to describe an instant: the solution integrates release over a source duration, whose scale is set by the half duration. The centroid time is a centre of that release, not a sample at a moment. Practically, treating an event as a point in time is safe at any bin width far larger than the half duration — 0.6 s in the example — and unsafe below it. That the release interval is symmetric about the centroid time, i.e. spans roughly the centroid time plus or minus one half duration, is a **guess**: it follows from combining "centred" with "half the duration", but the files do not state it, and for records where the half duration is absent the extent is simply unknown.

Finally, a gap on this axis is not interpretable from these files. Nothing here establishes a detection threshold or a completeness criterion, so an empty interval could mean no earthquakes or no solutions, and you cannot tell which.

# 5. Ambiguities

**Which function of the tensor produces the scalar moment — not determined; I decline to name it.** The schema says only that it is a function of the components. This matters because it is stated to add no independent information, which invites a consistency check. I ran the obvious candidate on the example record — the root-sum-of-squares over all nine positions, divided by the square root of two — and got 1.392 × 10²³ against a published 1.312 × 10²³, about six per cent apart. Either that is not the function, or something in this record is internally inconsistent. The files do not decide it, and I will not pick.

**The reference surface for depth — not determined; declining.** "Downwards from the surface" does not say which surface. The schema removes depth from the coordinate reference system explicitly, so there is no vertical datum to fall back on. This is inconsequential for the 162.8 km example and consequential for anything shallow or marine.

**Whether "up" means the ellipsoid normal or the geocentric radial direction — not determined; declining.** This is the missing piece needed to rotate tensors into a common frame, which is the operation §3 says you must perform before combining components across locations. Whatever you assume, document it; the assumption is yours, not the catalogue's.

**The meaning of the third depth-type category — not determined; declining.** The schema characterises only the free and fixed cases. Whether the third should be pooled with fixed, with free, or kept separate is not decidable here; keep it separate.

**How shallow "very shallow" is — not determined; declining.** This is the depth below which two off-diagonal components are held at zero rather than estimated. Without a number you cannot construct a depth filter, and because the affected records concentrate at one end of the depth range, the contamination is correlated with exactly the variable most depth-dependent analyses use. The exact-zero heuristic in §2 is a workaround, not a substitute.

**Whether the record can be trusted to distinguish a constrained zero from an estimated zero — it cannot.** The flag that does so upstream (a zero standard error) is stated to be absent from this record. This is not an ambiguity in the files so much as a known, stated loss.

**The trailing character of the event name — not determined.** *Guess:* it disambiguates solutions that would otherwise share the same minute. Marked as a guess; nothing in the files supports it.

**Which time is embedded in the name — not determined.** The digits agree with the centroid time to the minute in the example, but since the centroid time is a reference time plus an offset, the two can straddle a minute boundary. Use the time member and never the name.

**Whether older records use the current name form — the schema says "current events" use the fourteen-character form, which implies others do not.** Do not write fixed-width parsers against the name across a whole catalogue.

**Identity and revision semantics — not determined; declining.** Nothing says whether one physical earthquake can appear as more than one record, whether re-inversions replace or accompany earlier solutions, or how the catalogue version of a record could be established. There is no source, version or processing-time member. Deduplicating on the name is safe; concluding that two names are two earthquakes is not.

**Precision of the time values — not determined.** The example carries a tenth of a second; whether that resolution is uniform across the feed is not stated, so do not read it as an uncertainty.

**The coordinate reference system annotation.** The schema's prose refers to an EPSG:4326 annotation on the record, and I take the horizontal coordinates to be WGS 84 geographic degrees on that basis. I note that the annotation is asserted in prose rather than visible as a declared unit on the two coordinate members themselves, so the degree unit rests entirely on that reference — an **inference**, though a low-risk one, and consistent with the example's values.

**One thing that is *not* ambiguous, and is worth stating because sign errors are the classic failure here:** the axis triple as named — up, south, east — is right-handed, since up crossed into south gives east. There is no hidden reflection in the naming to compensate for.


TRANSCRIPT D

# Reading the GcmtMomentTensor feed

## 1. What this feed is

Each record is one **source solution for a single seismic event**: a named event, a
point in space and time called the *centroid*, a scalar magnitude of the source
expressed as a moment, and the six independent components of a symmetric
second-rank moment tensor in one consistent unit. A record is therefore not an
observation at a station and not a waveform — it is a *derived, inverted summary*
of an event's source: where the release was centred, when, how big, and what the
geometry of the release was.

Two members qualify how that summary was produced rather than describing the
source itself: a categorical depth-determination flag, and a source duration
scale. Both are optional, so some records will not carry them.

The critical thing about a record is that it mixes **directly reported
quantities** (the location, the time) with **quantities derived from a fit**
(the six components, and — see §3 — the scalar moment, which appears to be a
function of the six). Nothing in the record tells you how well the fit worked.

## 2. Analytics the stream supports, and why

**Space–time–size catalogue.** The record carries an absolute instant, a
three-dimensional location, and a magnitude-like scalar on a ratio scale with a
true zero and a declared unit. That is exactly the minimum for cumulative
moment-release curves, moment-release maps, depth histograms, and rate-change
detection. This is the analysis the feed is best suited to and the one that
needs the fewest assumptions.

**Source-geometry classification.** All six independent components of a
symmetric 3×3 tensor are present in a single common unit, so each record can be
eigen-decomposed. That supports principal-axis orientation, isotropic/deviatoric
splitting, and eigenvalue-ratio shape measures — per record, without needing any
other record. This is well supported *within* a record; see §3 for why it is not
well supported *across* records.

**Internal consistency QA.** The scalar moment and the six components are not
independent. On the single supplied record, the arithmetic works out as follows
(components in units of 10²³):

- Trace `mrr + mtt + mpp = 0.838 − 0.005 − 0.833 = 0.000` — traceless to the full
  reported precision.
- Eigenvalues ≈ `+1.581`, `−0.538`, `−1.043`.
- `(λ_max − λ_min) / 2 = 1.312`, which equals the reported `scalar_moment`
  to four significant figures.
- The root-sum-square norm `sqrt(ΣMᵢⱼ²/2) = 1.392`, which does **not** equal it.

So a cheap, high-value validator is: recompute the scalar from the components
and flag records where the two disagree. I am inferring the relation from *one*
record — it is a hypothesis, not something the schema states — but it is precise
enough to be worth testing across the corpus, and the negative result (it is not
the Frobenius-style norm) is the more important half, because that is the
formula an analyst is most likely to reach for.

**Depth-population analysis stratified by the depth flag.** The depth flag
clearly partitions records by how the depth was arrived at rather than by
anything about the event. Any depth histogram or depth-versus-anything
regression should be computed per stratum before being computed overall,
otherwise the shape of the distribution is partly an artefact of the inversion
procedure. (I decline to say what the three codes mean; see §5.)

**Duration versus size.** Both the duration scale and the scalar moment are
present with units on the same record, so their joint distribution is
computable. Because duration is optional, this analysis runs on a subset, and
that subset is not necessarily a random one — whether duration is missing at
random is not determined by the files, so the subset must be characterised
before it is used.

**What the feed cannot support.** There are no uncertainty, misfit, station-count,
or quality members of any kind, and the record is closed to additional members.
So: no error-weighted regression, no significance test on whether a small
component is distinguishable from zero, no filtering on solution quality beyond
the depth flag, and no way to attach provenance without a sidecar keyed on the
event name. Analysts routinely treat inverted tensors as exact; this feed gives
you no means to do otherwise, and that limitation should be stated in any result
derived from it.

## 3. Combination rules

**The six tensor components — the main trap.** Componentwise addition and
averaging of tensors is linear and therefore *arithmetically* valid, and all six
share one unit. But the component names index a coordinate basis, and the naming
(`r`, `t`, `p`) points to a spherical basis rather than a fixed Cartesian one.
**The files do not state whether that basis is global and fixed or local to each
event's own position.** If it is local — which is what a spherical basis normally
implies — then two records at different latitudes/longitudes express their
components in *different* bases, and adding, averaging, or even directly
comparing individual components across those records is meaningless without
first rotating both into a common frame. I am not deciding which it is; I am
flagging that this must be resolved before any cross-record component
arithmetic, and that the default assumption ("same member name, same meaning,
just add them") is unsafe here. Within a single record, all six are in one basis
and may be freely combined into invariants, eigenvalues, and traces.

The sign of each component is basis-dependent and the sign convention is not
stated. Signs are usable for comparison *within* this feed on the assumption of
internal consistency; they are not portable to another source without checking.

**Trace.** `mrr + mtt + mpp` is zero on the example record, and no constraint in
the schema enforces that. Do not assume tracelessness — compute it. If it is
identically zero across the corpus, the isotropic part of the source is not
carried by this feed at all and any "volumetric component" analysis is
impossible here rather than merely difficult. If it is non-zero on some records,
those records carry information the others do not.

**Scalar moment.** Non-negative, ratio scale, true zero, one unit — so ratios,
differences, and sums are all defined, and "total moment released by this set of
events" is a well-formed sum. The trap: **the sum of scalar moments is not the
scalar moment of the summed tensor.** Per §2 it is a function of the eigenvalues,
which is non-linear in the components. If you want a combined source, sum the
components (subject to the basis caveat) and re-derive the scalar; do not sum
the scalars. Arithmetic means deserve care for a second reason: the schema puts
no upper bound on the value and the example is written in exponent notation, so
the dynamic range is plausibly large and a plain mean would be dominated by a
few records. The distribution itself is not established by the files, so treat
this as a caution to check, not as a fact.

**Unit.** The declared unit is CGS (`dyn.cm`), not SI. `1 dyn·cm = 10⁻⁷ N·m`.
Any join against a source reporting newton-metres is silently wrong by seven
orders of magnitude if the unit is ignored. Because the scalar and all six
components share the unit, all *ratios* and all *dimensionless* shape measures
are unaffected by the choice — only absolute values are.

**Depth.** Kilometres, non-negative, one unit — differences and averages are
dimensionally fine. Two conditions: (a) the reference surface the depth is
measured from is not declared anywhere, so cross-source comparison is not
established, and (b) values determined under different depth-flag codes should
not be pooled without thought, because the flag is evidently about how the value
was obtained. The floor of zero also means the representation cannot express a
source above the reference surface; if such events exist they are clipped or
rejected upstream, which truncates the low end of any depth distribution.

**Latitude and longitude.** These are the only physical quantities carried with
**no declared unit at all**, while depth, duration, and moment all have one. A
unit-aware pipeline will convert the latter three and pass the angles through
untouched — a real and easily-missed asymmetry. The example values are only
consistent with degrees (13.76 cannot be radians), so degrees is a safe
inference, but it is an inference. Beyond that: no range constraints, no
wrap convention (the negative longitude is consistent with −180…180 but one
record does not establish it), and no datum or reference frame. Consequences:
longitude differences must be wrapped, arithmetic means of coordinates are not
valid centroids and break across the antimeridian, and the coordinates should be
treated as comparable within this feed but not as co-registered with any other
feed.

**Duration.** Seconds, non-negative, one unit — comparable, differenceable,
averageable. It is optional, and zero is a legal value, so **absent must not be
folded into zero**; they are different states and only one of them is a
measurement.

**Depth flag.** Nominal categorical. No ordering, no arithmetic, no interpolation.
Group by it; never average over it. Absent means unknown, not any of the three
codes.

**Event name.** Opaque string; equality only, no ordering. Nothing in the schema
declares it a key or asserts uniqueness, so deduplicating on it is an assumption
you are making, not a guarantee you are given. The example value visibly contains
digits matching a date and time, and those digits agree with the centroid time to
the minute but not to the second. Parsing the identifier to recover a timestamp
would therefore produce a value that is *close to but not equal to* the real one
— a silent, small, systematic error. Use the time member; treat the name as an
opaque label.

**Across the whole record.** There is no version, revision, or publication
member. Two records with the same event name cannot be ordered into "original"
and "revised", and there is no way to tell when a record was produced. The feed
is single-temporal: it supports as-of-event analysis and not as-of-knowledge
analysis. Any pipeline that needs to handle late corrections must carry that
information out of band.

## 4. Time

**The centroid time is the sole time axis, and it is the axis of the source
process — not of observation, not of detection, not of publication.** There is
no other temporal member, so the feed cannot answer "when did we learn this" at
all.

Positions on that axis relate to civil time directly and without a zone
assumption: the example value is an RFC-3339-shaped instant carrying an explicit
`Z` offset and a tenth-of-a-second fraction. Two such values are absolute
instants and may be differenced and ordered as-is. Two caveats: the schema does
not visibly guarantee that every record carries an explicit offset or that the
offset is always `Z`, so a consumer should *require* an offset rather than
assume one and default to UTC on absence; and the 0.1 s resolution of the example
is a property of that one value, not a declared precision.

There is a subtler point about what the instant means. The member is a
*centroid* time and the record separately carries a duration scale — which
together indicate the described process has real temporal extent and that the
time member is a single summarising point within it, not the moment the process
began. (This reading follows from the two members' names; the files do not spell
it out.) The practical consequence: ordering two records whose centroid times
differ by less than their duration scales is arithmetically well-defined but not
physically decisive, and binning events into intervals shorter than the typical
duration attributes an extended process to a single bin. Neither is wrong, but
neither should be read as more precise than it is.

Whether leap seconds are representable or how a `:60` value would be handled is
not determined.

## 5. Ambiguities

- **Whether the tensor basis is fixed or event-local.** *Declining to decide.*
  This is the single highest-consequence gap in the two files. It determines
  whether cross-record component arithmetic is valid without rotation. It must be
  resolved from outside these files before any stacking, averaging, or
  component-level clustering.
- **Sign convention of the components.** *Declining.* Internal consistency within
  the feed is a reasonable working assumption; portability to another source is
  not.
- **Meaning of the three depth-flag codes.** *Declining.* That the flag stratifies
  depth by determination method is a reading of its name and its position; which
  code means what, and which (if any) indicates a lower-confidence depth, is not
  in the files.
- **Definition of the scalar moment.** *Guess, and marked as such:* the reported
  value matches half the difference between the largest and smallest eigenvalue
  on this record to four significant figures. One record is one data point. The
  firmer, negative finding — that it is *not* the root-sum-square norm — is what
  should be acted on.
- **Units of latitude and longitude.** *Assumption:* degrees, because the example
  values are incompatible with radians. Not declared.
- **Longitude wrap convention and coordinate reference frame/datum.** *Declining.*
  One negative longitude is consistent with −180…180 but does not establish it,
  and no datum is named for either the horizontal coordinates or the depth's
  reference surface.
- **Whether the tensor is always traceless.** *Declining* — it is on this record,
  and nothing enforces it. Compute rather than assume.
- **Uniqueness of the event name, and its internal structure.** *Declining* on
  uniqueness (nothing declares it a key). The apparent embedded timestamp and the
  leading/trailing letters are *observations* from one value; their meaning is
  not established and the identifier should be treated as opaque.
- **Why the duration and depth flag are optional, and whether their absence is
  random.** *Declining.* This matters because any analysis using them runs on a
  self-selected subset.
- **Whether a magnitude can be derived.** The feed carries moment in CGS units
  and no magnitude member. The relation between the two is not in the files, so
  *I decline to supply one*; any magnitude produced downstream is an external
  convention, not something this feed determines.
- **Uncertainty on every reported quantity.** *Not determined and not
  representable* — the record is closed to additional members, so uncertainty
  cannot even be added in place.
