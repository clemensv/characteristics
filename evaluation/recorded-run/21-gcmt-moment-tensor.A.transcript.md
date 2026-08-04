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
