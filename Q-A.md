# Hard Questions About This Specification

This document collects the most hostile questions that can reasonably be asked
about *JSON Structure: Semantic and Reference-System Annotations*, and answers
them. The questions were
written to be unfair; the answers try not to be defensive. Where the criticism
lands, it says so, and the final section lists every concession as a work item
rather than burying it.

Section references are to
[`draft-vasters-json-structure-characteristics.md`](draft-vasters-json-structure-characteristics.md).

---

## A. Why does this exist at all

### 1. Why does this exist when SOSA/SSN, ISO 19156, OGC SensorThings, and netCDF-CF already model observations — and you cite all of them as normative?

Because none of them annotate a schema. They are data models: to use SOSA you
restructure your payload into SOSA's shape, and to use SensorThings you adopt
its API and its entity graph. The overwhelming majority of real event streams
will never be restructured — the AIS, METAR, GBFS, BMRS, and HFP schemas in
`samples/real-world/` are the payloads their publishers actually ship, and no
publisher is going to reshape them into an observation ontology. This document
takes the opposite direction: leave the payload exactly as it is, and record
against it what the payload already means. It is a description mechanism for
schemas that exist, not a target model for schemas that do not.

### 2. If the answer is "those are too heavy," what exactly did you drop, and why is the residue still worth a spec rather than a convention document?

What was dropped is the object model — Observation, Sensor, FeatureOfInterest,
Datastream as *classes you must instantiate* — and the graph, the identity
system, and the entailment. What was kept is the small set of distinctions that
change how a number may be arithmetically handled: what it measures, against
which reference system, over which time semantics, produced how. It is worth a
specification rather than a convention because the attachment points, the closed
enumerations, and above all the prohibitions in §Processing Conformance are
only useful if they are normative. A convention that says "you may not infer a
coordinate binding from property names" is advice; a MUST NOT is a testable
requirement.

### 3. Why is this at the IETF? Observation semantics, CRSs, color spaces, and audio layouts are OGC, ISO, ICC, and ITU territory.

The document defines none of those things. It defines how a JSON schema
*cites* them, which is squarely an interchange-format concern. OGC owns what
EPSG:4326 means; this document owns the statement that members `lat` and `lon`,
in that order, are its axes. The venue question is fair to raise for a
Standards-Track document; for an Experimental one whose entire content is
citation form, the IETF is where the JSON Structure family lives and where the
core specification it extends is being processed. Cross-review by OGC and ICC
would improve it and should be sought.

### 4. Why is this bound to JSON Structure at all? Every keyword here is schema-language-agnostic.

The keyword *semantics* are language-agnostic; the *mechanism* is not. This
document relies on JSON Structure add-ins for attachment, on `$uses` for
activation, on the versioned meta-schema URI for versioning, on `$import` for
sharing meta-types, on Core's type system for the compatibility rules, and on
the Units extension for unit checking. Reproducing that machinery in a
language-neutral form would mean specifying an attachment model for every host
language. A neutral abstract vocabulary with per-language bindings is a
legitimate alternative design, and it is more work than it looks: the value of
the compatibility rules comes precisely from being able to say "this annotation
is invalid on this Core type."

### 5. Why not JSON-LD? You explicitly refuse prefixes, CURIEs, entailment, and node identity — so you've built a worse RDF.

The refusals are the point, not an omission. JSON-LD answers "what graph does
this document denote"; this document answers "how must a consumer handle this
number." Those need different machinery. A JSON-LD `@context` gives you term
identity but says nothing about axis order, quaternion component order, alpha
premultiplication, or A-weighting — and cannot, because those are not statements
about a graph. Conversely `concepts` deliberately stops at term identity and
delegates everything graph-shaped elsewhere. The two are complementary: a
schema can carry `concepts` bindings *and* have its instances serialized as
JSON-LD.

### 6. `category: exp`. Is this an experiment or a proposal? What result would falsify it?

Experimental, honestly labelled. The hypothesis is that a consumer — human or
machine — given an annotated schema and nothing else can correctly determine
whether two data streams may be combined, and can do so without prose. It is
falsified if independent implementers, reading the same annotations, reach
incompatible handling decisions; if the annotations turn out to be
systematically maintainable only by their original author; or if the set of
distinctions proves too small to cover real streams without constant extension.
The third is the live risk and the reason the sample corpus keeps growing.

---

## B. Is this one specification or five stapled together

### 7. What do river gauges, moment tensors, ICC color profiles, 5.1 audio beds, MODIS spectral bands, and ICD-10 diagnosis codes have in common?

One thing, and it is the thesis: in every case a number is meaningless until you
know the externally governed frame it is expressed in, and in every case that
frame is conventionally recorded in prose or in nothing. A component of a
magnetic field vector, a channel of a CIELAB triple, a band of a MODIS scene,
and a level in a 0+5+0 bed are all *the same problem* — an ordered set of
members resolved onto the ordered slots of a definition someone else maintains.
The keywords differ because the slot vocabularies differ (axes, channels, bands),
not because the problem does.

### 8. "Characteristics" of what? Is the title vague because the scope is?

**Accepted, and acted on.** The title was weak. "Characteristics" was chosen to
avoid promising an observation model, and it under-described the result. The
document has been retitled *JSON Structure: Semantic and Reference-System
Annotations*, with the short name `semantic-annotations` for the repository, the
meta-schema URI, and the `$uses` feature identifier.

### 9. Where does this stop? Why not geometry, provenance, licensing, calibration history?

**Accepted, and acted on.** The principle was applied consistently across the
keyword set but was nowhere written down, which is why the question was easy to
ask. It is now stated in the introduction: a quality of a value earns a keyword
when a consumer must know it to decide whether two values may be combined or
compared, and when it holds for the type rather than varying from one instance
to the next. Axis order, frequency weighting, and the register a code is drawn
from pass that test — get one wrong and an arithmetic result is wrong while
every value still validates. Licensing, retention, and endpoint addressing fail
it, because they do not change what may be computed. Per-observation
calibration history fails it, because it varies per record and belongs in the
payload. Geometry, provenance, and unit algebra fail it, because each is a model
in its own right that another specification defines.

### 10. Why is `measurementConditioning` here rather than in Units, given that dB(A) re 20 µPa is arguably a unit?

Because it is arguably a unit and demonstrably not one. UCUM has `B[SPL]`, but
frequency weighting is not part of the unit algebra: dB(A) and dB(C) are the
same unit and different quantities, and no unit system will convert between
them because no conversion exists. Putting weighting in the unit would make a
unit-aware processor believe two incomparable values are comparable, which is
the exact failure this document exists to prevent. Time weighting (fast/slow)
has the same property.

### 11. Why is `codedValues` here rather than in Validation or Alternate Names?

Validation constrains which values are permitted; Alternate Names states what a
symbol is called and means *in this schema*. `codedValues` does neither. It says
the permitted values are not this schema's to define — they are drawn from a
register maintained elsewhere, which may add codes tomorrow. That is a binding
to an external definition, which is what this document is about, and it is why
`codedValues` shares the `reference`/`kind` shape with everything else here.

### 12. Are `colorSpaces`, `audioChannels`, and `spectralBands` three copies of one keyword you failed to unify?

They share a shape, and they were considered for unification. They are separate
because their non-shared members carry the actual weight and do not generalize:
`illuminant`, `observer`, `transfer`, `alpha`, and `alphaMode` are meaningless
for audio; `levelReference` and `encoding` are meaningless for color;
`calibration` is meaningless for both. A unified keyword would be a shell around
three disjoint member sets, and a processor would need the discriminator anyway.
The honest cost of the decision is three near-identical `reference`/`kind`
sections, which is why §Semantic Binding states the shared shape once.

---

## C. Does it actually do anything

### 13. Everything is optional and absence establishes nothing. What does it mean to conform?

§Schema Conformance is explicit: a schema with zero annotations is
conforming, and conformance constrains only what is present. That is deliberate,
because the alternative — requiring annotations — would make the extension
unusable on the schemas that most need it. The teeth are elsewhere. Every
annotation that *is* present must sit at a permitted attachment point, have the
defined shape, use permitted values of the closed enumerations, be compatible
with the Core type, and satisfy the Units rules; and those checks are never
indeterminate. The stronger conformance target is the processor, not the schema
— see question 17.

### 14. `reference` need not be dereferenced and an unresolved one is "indeterminate rather than incorrect." How is that different from a comment?

Two ways. First, a comment cannot be compared; a URI can. Two schemas citing the
same reference are making the same claim, and a processor can determine that
without resolving anything — which is most of what interoperability needs.
Second, §Check Outcomes forbids treating indeterminate as valid: a processor
that cannot resolve a CRS is *prohibited* from performing the coordinate
transformation. A comment produces optimism; an unresolved reference produces a
required refusal.

### 15. Open enumerations where any string is legal and unknown values "establish nothing" — what did the enumeration buy?

It buys a defined subset that *does* establish something, plus a guarantee of
survival for everything else. The defined values are actionable; an undefined
value is an honest "this processor does not know," which a processor MUST
preserve and MUST NOT reject. The alternative designs are worse: a closed
enumeration makes the extension unusable in any domain not anticipated here, and
free text makes the known cases unactionable too. The real complaint is that the
open/closed split looks arbitrary — see question 36, where it is conceded.

### 16. Nothing validates an annotation against the data. What stops a schema claiming EPSG:4326 on a field carrying feet?

Partly, the Units rules do: coordinate properties must be numeric, and a `unit`
on a coordinate must be compatible with the corresponding axis, which a
processor with a CRS database can and MAY verify
(§Coordinate Reference Systems). Beyond that: nothing, and nothing can. No
metadata mechanism can detect a publisher who states something false, any more
than a type system detects a `double` holding a wrong measurement. The claim
here is not that annotations are true; it is that they are *checkable in
principle and comparable in practice*, which prose is not.

### 17. Name one decision a processor can make automatically, correctly, and safely, that it could not make before.

Refusal. Given two streams whose position members both carry
`coordinateReferenceSystem`, a processor can determine mechanically that one is
EPSG:4326 and the other EPSG:25832 and decline to join them on coordinates
without a transformation — and, per §Check Outcomes, must decline rather than
guess if it cannot resolve either. Same for `measurementConditioning`: two sound
levels with different `weighting` values must not be averaged. Same for
`vectorReferenceFrames`: components in two different spacecraft-local frames
must not be differenced, though their magnitudes may be compared. Automatic
correct refusal is the primary deliverable; automatic transformation is
explicitly not offered.

### 18. Do their data become interoperable, or do you merely make the incompatibility legible?

**Legible — and the abstract now says so.** It states that the annotations make
an incompatibility detectable by machine and do not resolve one, that the
document defines no conversion, that an unresolvable reference is reported as
indeterminate rather than assumed to agree, and that correctly declining to
combine two values is the outcome enabled while transforming them remains the
work of a tool holding the authoritative definitions.

Making incompatibility machine-visible is not a consolation prize — silent
incorrect combination is the failure mode that costs money and, in a few of
these domains, lives. §Security and Privacy Considerations reinforces the point
by forbidding temporal, coordinate, linear, and unit transformations without
validating authoritative definitions.

---

## D. The comparability premise

### 19. Annotating tide-gauge datum versus ellipsoidal height converts neither. You've moved the problem.

Correct, and moving it is the contribution. Today that information is not in the
schema at all, so the mismatch is invisible and the bad join happens silently.
With the annotation, the mismatch is detectable by a processor that holds
neither definition, and resolvable by one that holds both — using EPSG's
transformation machinery, which is EPSG's job and not this document's.

### 20. Interoperability depends on agreeing which vocabulary to cite, which you refuse to specify. Isn't the hard 90% out of scope?

The hard part is out of scope because it is already someone else's solved
problem. CF, EPSG, QUDT, WMO, and ICC exist, are maintained, and are agreed
within their communities. What did not exist is a way to say *in a schema*
which one you used. If this document also picked winners it would be wrong for
every domain it did not anticipate, and it would be a competing vocabulary
rather than a citation mechanism. What it does provide is
the informative Reference URIs appendix, which names resolvable URIs for the
registered kinds — a
recommendation without a mandate.

### 21. Two publishers cite equivalent-but-different terms. How does a consumer know they're the same? You forbid entailment.

It doesn't, from this document alone, and that is correct behavior rather than a
gap. Deciding that a CF standard name and a QUDT quantity kind denote the same
thing is a mapping judgement with real consequences, and
§Security and Privacy Considerations explicitly forbids treating an unreviewed
or non-exact mapping as approval. The mitigation available today is that `concepts`
takes a *list*, so a publisher who knows the correspondence can assert both
terms on one node and let consumers match on whichever they hold.

### 22. `concepts` is unordered with no primary entry. What does a consumer do with three terms it can't rank?

It matches on the one it recognizes. That is the intended and only use: the list
is not a ranking to be resolved but a set of synonymous handles, so that a
CF-based consumer and a QUDT-based consumer can each find their own without
either being privileged. Ranking would imply an authority this document does not
have.

---

## E. Meta-types

### 23. A meta-type is a convention you wrote yourself. How is that better than the undocumented local convention the introduction complains about?

Three ways, none of which is "it is as good as a registered definition."
It is written down in a machine-readable form rather than in a wiki; it is
addressable, so annotations across many schemas can point at one definition; and
it is reusable, because §Meta-Types expects it to live in its own document
and be brought in with `$import`. The document is candid that this is second
best: schema authors SHOULD use a registered definition where one exists
(§Coordinate Reference Systems). Meta-types exist because for spacecraft
frames, operating-day clocks, and TLE epochs, no register exists at all — the
alternative is not a registered definition, it is silence.

### 24. Two publishers each write a `PosixMillisecondEpoch` meta-type. They still don't interoperate.

They interoperate better than they did. Each has stated the regime, its sort
order, and which member carries the position, so a consumer can determine that
the two are describing the same regime by inspection rather than by assumption —
and, critically, can determine when two similar-looking integer timestamps are
*not* the same regime, which is the case that silently corrupts data today.
Full automatic equivalence needs a register, and the document's answer is that
publishing one is the community's job, not this specification's.

### 25. `referenceRole` is closed at four values. Why those four? Where are origin, epoch, scale, uncertainty, zone?

Because those four are the ones a keyword defined here actually maps:
`position` for `temporalReferenceSystem`, and `linearElement`, `measure`, and
`direction` for `linearReferenceSystem`. `referenceRole` is not a general
vocabulary of system parts; it is the mapping surface between an annotation and
a meta-type, and it is closed so that the mapping is decidable. Origin, epoch,
scale, and zone are properties *of the system*, stated in the meta-type's
descriptions, not members the annotation binds. A member with no
`referenceRole` is explicitly permitted and simply unmapped.

### 26. CRSs and vector frames take no roles because tuple order establishes the axes, but temporal and linear systems do. Why is the mechanism inconsistent?

Because the systems are. A coordinate system's parts are homogeneous and
ordered — axis 1, axis 2, axis 3 — so ordinal position is the natural and
sufficient identification. A linear reference system's parts are heterogeneous:
the route identifier, the distance along it, and the direction are different
kinds of thing and have no natural order. Using positional binding for the first
and named roles for the second follows the structure of the domain. Forcing one
mechanism on both would make one of them arbitrary.

---

## F. Binding by member name

### 27. Why are the mapping properties strings naming members rather than JSON Pointers?

Because their scope is deliberately one level. Every one of these keywords binds
*direct* members of the type it is attached to, so a pointer would always be
`#/properties/<name>` — the same information with more ceremony and an invitation
to point outside the type, which the design forbids. The constraint that a
coordinate is assembled from siblings is what makes the annotation checkable
against the effective schema.

### 28. What happens to those name strings under `$extends`, `$import` renaming, and Alternate Names? Do they refer to the schema name or the wire name?

**It was a genuine gap, and it is now closed.** §Annotation Model states
normatively that a member name stated by an annotation is the property name as
*declared in the schema*; that it resolves against the effective definition of
the annotated type, including members contributed by `$extends` and members of
an imported or shadowing definition; that a name not resolving to a direct
member of that effective definition is invalid; and that an alternate,
localized, or otherwise serialization-facing name — such as one assigned by JSON
Structure Alternate Names — changes how the member appears in an instance
document without changing the identity the annotation binds. A processor MUST
NOT resolve an annotation's member name against such a name. §Inheritance and
Imports carries a pointer to the rule, since that is where a reader is likely to
look for it.

### 29. If the annotated type is a tuple, the order is in the tuple. Why does `coordinates` restate it — and what if they disagree?

`coordinates` does not restate tuple order; it selects and orders a subset. A
tuple carrying `[time, lat, lon, quality]` has four elements of which two are the
coordinate, in an order that need not match. §Coordinate Reference Systems
also states that properties not named are not part of the coordinate, which is
what lets the annotation be applied to an existing record without restructuring
it. Disagreement is therefore not possible: `coordinates` is authoritative for
axis order, and the tuple is authoritative for serialization order.

### 30. Why can these keywords only sit on the containing type instead of on the members, like everything else?

Because they are statements about a *relationship among several members*, and
there is no single member to attach them to. An axis order exists between `lat`
and `lon`; putting "I am axis 2" on `lat` distributes one fact across n places
that can then disagree. The keywords that describe a single value —
`semanticRole`, `derivation`, `codedValues`, `measurementConditioning` — do sit
on the member. The split is not two attachment models chosen at random; it
follows arity.

---

## G. The closed enumerations are arbitrary

### 31. `statistic` has `mode` and `range` but no percentile or p95. Justify that on real telemetry.

**Accepted, and acted on.** The omission was real, and the design reason for it
was that quantiles are parameterized while every other value in the enumeration
is not — a closed enumeration of bare symbols has nowhere to put the parameter.
That was an argument for extending the design, not for the omission.

`statistic` now takes two forms. A function that takes no parameter stays a bare
string, unchanged, so every existing schema still validates. A function that
takes one is written as an object: `{ "function": "percentile", "percentile":
95 }`. Three parameterized functions are defined — `percentile`, `nthHighest`,
and `nthLowest` — and both enumerations remain closed, so the decidability
argument in question 15 is untouched.

The rank forms are there because a rank is not a percentile. The fourth-highest
value of 365 is the 99.18th percentile and of 90 is the 96.7th, so neither can
be rewritten as the other without the set size, which `statistic` deliberately
does not state. Both forms are what definitions in force actually specify: the
US ozone standard is the fourth-highest daily maximum eight-hour value, the EU
PM10 daily limit is evaluated as the 36th-highest daily mean, and a service
level objective is a percentile.

One meaning gets one spelling: an unparameterized function may not be written in
object form, percentile 0 and 100 must be written as `minimum` and `maximum`, a
rank of 1 must be written as `maximum` or `minimum`, and a quantile is written
as the equivalent percentile. Without that, two schemas could declare the same
statistic in ways no equality test would match. The meta-schema enforces the
shape, the closed function enumeration, and the parameter ranges; the checker
rejects an unknown function, an out-of-range percentile, a rank of one, and any
extra member.

`trimmedMean` was considered and left out: the parameter has no settled
convention across the sources that publish trimmed means. `exceedanceCount` was
left out because its parameter is a threshold carrying a unit and a reference,
which is a model rather than a parameter member.

### 32. Give me the operational test that distinguishes `calculated`, `estimated`, and `modeled`.

**Accepted, and acted on.** §The `derivation` Keyword now states the tests
instead of leaving them to the value names.

The first division is `measured` against everything else, and it is the one that
matters most to a consumer: a value is `measured` where it is what the procedure
read, and not `measured` where any function, fit, inference, or model stood
between the procedure and the value. That division was never ambiguous.

Among the rest, two tests decide. **Determinism** separates `calculated` from
`estimated` and `modeled`: where the same inputs must yield the same output and
the function could be written down, the value is `calculated` however elaborate
the arithmetic. A dew point from a measured temperature and humidity is
`calculated`. **Dependence on unobserved state** separates `modeled` from
`estimated`: an estimated value carries only what the observations carry,
arranged under an assumption about their error — an interpolated fill, or a
strike position from arrival times at several detectors — while a modeled value
carries information the observations do not contain, and the procedure would
produce a value for a place and time at which nothing was observed. A forecast
is `modeled`. A reanalysis or assimilated field is `modeled` too, because the
model supplies the state and the observations only constrain it.

The edge is still soft in places, and the document now says what to do there:
state the method in `description`, and never resolve the difficulty by falling
back on `measured`.

### 33. `semanticRole` includes `ingestionTime` and `scheduledTime`. Why are pipeline concerns in a closed IETF enumeration?

Because they are what the streams carry. A transit feed's entire purpose is
`scheduledTime` against `actualTime`; a Mode-S record has no phenomenon time at
all and only a ground-station decode instant. Excluding these as "not
observation semantics" would mean the annotation could not describe the
timestamps that real feeds actually publish, and consumers would go on guessing
which of four timestamps is the event time — the single most common and most
damaging ambiguity in event data. The role vocabulary follows the streams rather
than the ontology.

### 34. `AudioEncoding` is closed at `linear`, `aLaw`, `muLaw`. Float samples and every modern codec are un-annotatable.

**Accepted on the closure, and acted on; the codec half of the objection does
not stand.** A compressed codec bitstream is an opaque blob, not a set of
channel members, and is outside what this keyword annotates whatever its
encoding is called. That has not changed and the document now says so.

The closure has been removed. `encoding` is now an open enumeration, on the same
rule that governs every other open one here: a sample encoding is a definition
someone else maintains, as G.711 companding is, so a value outside the
enumeration is a URI identifying another encoding rather than an error. A
processor that does not know a value MUST preserve it and MUST NOT assume the
numbers are proportional to amplitude; the check is indeterminate.

`float` has been added, but not for the reason the question implies. Floating
point samples were already expressible — the old text said `linear` covers
numbers proportional to amplitude "whether stored as integers or as floating
point". What was missing was the *scale*. `linear` now means full scale is the
range the declared type permits; `float` means full scale is unit magnitude, so
a sample of `1.0` is at full scale and a magnitude above one is legal and is a
level above full scale rather than an error. That is a fact the declared type
cannot carry, since a `double` member may hold either convention, and getting it
wrong makes a decibel level or a channel sum come out wrong while every value
still validates. It is exactly the inclusion test the introduction states.

### 35. `AudioLevelReference` is closed at two values but `measurementConditioning.levelReference` accepts a URI. Same concept, two mechanisms.

**Fair hit, and acted on.** The divergence was historical: `audioChannels` was
specified against the two references that BS.1770 and BS.2051 actually use, and
`measurementConditioning` was specified later against acoustics practice, where
ISO 1683 defines many references and an open form was necessary. Two authoring
episodes produced two mechanisms for one question.

There is now one. `AudioLevelReference` is gone from the meta-schema, replaced by
a single `LevelReference` that both keywords reference. It is open, taking
`fullScale`, `soundPressure`, or an absolute URI — which is the resolution the
objection proposed, and it also gains `fullScale` for `measurementConditioning`,
which had no way to say it before although a digital meter reporting a
frequency-weighted level in dBFS plainly needs it. Opening the audio form
invalidates nothing, since every value that was legal remains legal. The
document states the values once, under `measurementConditioning`, and the audio
section refers to that definition rather than restating it, so the two cannot
drift apart again.

One difference survives, and it is now stated as a decision rather than left to
look like the same oversight in a new place. Absence still means `fullScale`
under `audioChannels`, because digital audio samples are referred to full scale
unless something says otherwise and making every schema say so would add noise
without adding information; absence under `measurementConditioning` still means
no reference is stated, because a conditioned measurement has no comparable
default. The §The Annotation Model inventory moves `audioChannels.levelReference`
from the closed list to the open one accordingly.

### 36. What rule decided which enumerations are open and which are closed?

**Accepted, and acted on.** The rule is: closed where the value selects a
behavior *this document defines*, open where the value names a definition
*someone else maintains*. It was defensible and it was unstated — §The Annotation
Model listed which enumerations were which without saying why. It now states the
rule first and the inventory second.

The inventory was also incomplete. It named eight enumerations and the document
has fourteen closed ones; `variance`, `symmetry`, the `encoding` and
`rotationSequence` of `frameTransforms`, and the `alphaMode` and `transfer` of
`colorSpaces` were all governed by a rule the reader could not find. The list is
now complete on both sides.

One further sentence was needed and is now there: closure states where a value's
meaning comes from, not that a list is finished. A later version may add values
to a closed enumeration, and the versioned meta-schema URI is what tells a
processor which set is in force.

Question 35 identifies a remaining place where the rule was misapplied;
question 34 identified another, and the audio sample encoding has since been
opened under this rule.

---

## H. Specific technical objections

### 37. `frameTransforms` fixes a quaternion component order that CCSDS, NAIF, ROS, and Eigen do not agree on. You've added a third-and-a-half convention.

The document fixes a convention *for the annotation*, not for the data, and that
is the opposite of adding a convention. `components` names the members in the
order this document fixes, so a message that stores the scalar last is annotated
by listing the scalar-carrying member first — sample
`22-ccsds-attitude-quaternion` does exactly this. The wire layout is untouched;
what is removed is the reader's need to guess which layout it is. Without a
fixed annotation order, `components` would itself be ambiguous and the keyword
would be pointless.

### 38. Twelve intrinsic Euler sequences only. Extrinsic is at least as common. Deliberate or oversight?

Deliberate and adequate, though under-explained. Every extrinsic sequence equals
an intrinsic sequence with the axis order reversed, so the twelve intrinsic
sequences cover the full space with no expressive loss — an extrinsic XYZ is
annotated as intrinsic ZYX. Fixing one convention avoids the failure mode where
a reader must determine which of two conventions a schema meant.

**Accepted on the explanation, and acted on.** The equivalence was in the
document, but in §Euler Angles, phrased as an observation about the intrinsic
reading, and stated in the direction an annotator does not need. An
annotator holding an extrinsic source arrives at §The `rotationSequence`
Property, finds twelve values none of which says extrinsic, and has to derive the
conversion. That section now gives it as a procedure, in the direction the work
actually runs, with a worked case: an extrinsic X-then-Y-then-Z rotation of 10,
20, and 30 degrees becomes a `rotationSequence` of `ZYX` with `components`
naming the 30-degree member first.

The worked case earns its place because the shorthand in the paragraph above —
"an extrinsic XYZ is annotated as intrinsic ZYX" — is the trap. It names only
half the operation. The angles reverse too, and reversing the letters while
leaving the angles in place produces a different rotation that will pass every
check a processor can perform. The document now says both halves reverse and
says outright that doing one without the other is the error being guarded
against. It also adds that a converting schema SHOULD record the conversion in
`description`, since nothing in the annotation preserves the source's
convention and a later reader comparing schema to source would otherwise see the
reversal as a bug.

### 39. `variance` per frame position, but no metric to raise or lower indices. Is the tensor support real or decorative?

Real but bounded, and the bound is intended. `variance` exists so that a
consumer knows whether components transform contravariantly or covariantly
under a change of frame — which is what determines whether a transformation is
legal, and is exactly the "may I combine these" question this document answers.
Actually performing index raising and lowering requires the metric tensor and is
a computation, which §The Annotation Model places outside scope along with every
other analytical procedure. Per-index variance on mixed tensors *is* expressible:
each entry in `frames` carries its own `variance`.

### 40. `symmetry` is permitted only when two frames name the same frame — is string equality your frame-identity test?

Yes, and it is the only test available to a processor that has not resolved
either reference. It is conservative in the safe direction: two spellings of the
same frame will fail the equality test and `symmetry` will be rejected, forcing
the author to state all components explicitly — which is correct but verbose.
The unsafe direction, two different frames passing as one, cannot occur.

### 41. `colorSpaces` lets `reference`, `kind`, `codePoints`, `illuminant`, `observer`, and `transfer` all be present. These can contradict. Which wins?

They address different questions and mostly cannot contradict: `reference`
identifies the space, `codePoints` gives the H.273 identification of the same
space for video pipelines that key off those integers, and `illuminant` and
`observer` apply to measurement-referred spaces such as CIELAB where the space
alone does not determine the numbers. `transfer` is not redundant at all — it
states whether the stored values carry the space's transfer function or are
linear-light, which is a property of *this data*, not of the space.

**Half accepted, and acted on; the other half rested on a misreading.** The
document did already settle `reference` against `codePoints`, in §The
`codePoints` Property: where they disagree the code points are the narrower
statement and a processor MUST prefer them, following PNG, which gives its
`cICP` chunk precedence over every other color declaration a file may carry. So
the objection's claim that the document says nothing was wrong, and its proposed
fix — that `reference` should prevail — would have reversed a rule that matches
deployed practice. A URI naming BT.2020 leaves the matrix coefficients and the
range flag open; the four integers do not.

What the objection got right is that the rule was undiscoverable and unexplained,
and that one pair was left open. Three things changed. The principle is now
stated once at the head of §The `colorSpaces` Keyword: `reference` identifies a
definition describing a *class* of data, while `codePoints`, `transfer`,
`illuminant`, and `observer` state what is true of *this* data, and the narrower
statement prevails — so the individual rules follow from something rather than
being three arbitrary facts. §The `reference` and `kind` Properties now carries a
forward pointer, so a reader arriving at `reference` is not left to discover the
precedence rule three subsections later. And `illuminant`/`observer` against the
identified definition, which genuinely had no rule, now has one in the same
direction: the declared members prevail, a processor SHOULD report the
disagreement, and the schema is not thereby invalid.

### 42. Since `reference` identifies the list, what does `codedValues.kind` add other than a taxonomy fight?

It tells a processor how a value *joins* to an entry before any resolution
happens — WMO codes, SNOMED concept identifiers, and IANA registry entries are
organized differently and are dereferenced differently. It also lets a processor
recognize a register family it supports without holding a list of every URI in
that family. The taxonomy is admittedly a judgement call, and the answer to "why
`snomed-ct` but not `naics`" is that the enumeration is open and adding a value
requires no permission — a schema may write `kind: "naics"` today, and a
processor MUST preserve it.

### 43. `cadence` is an expectation, not a constraint. How is an unenforceable expectation different from documentation?

It is documentation that a machine can act on, and the document is careful about
what that action may be. §Security and Privacy Considerations states that
cadence MUST NOT synthesize a missing `untilNext` successor, and §Processing
Conformance forbids inferring an `untilNext` end from cadence.
What remains is legitimate: sizing a window, setting a staleness threshold,
detecting a gap. Making cadence a constraint would be wrong — a stream that
misses a beat is late, not invalid, and a schema is not the place to declare a
runtime SLA.

**That reasoning was in the answer and not in the document, and it now is.** §The
`cadence` Keyword previously listed only what cadence is not. It now states the
expectation/constraint distinction normatively: a schema declaring a cadence
constrains no instance, an instance whose timing departs from it is not invalid
for that reason, and a processor MUST NOT reject an instance, a value, or a
schema on that ground. It also states the three legitimate consumer uses, so
that the keyword is not read as either enforceable or inert.

### 44. `cadence.period` is typed `any`. How does a processor validate it against a TRS it isn't required to resolve?

It validates what it can and reports the rest as indeterminate, which is the
general pattern of §Check Outcomes. `period` is `any` because the type of a
period depends on the temporal reference system: a Core duration for `datetime`,
`date`, and `time`, and a count of the system's own units for an ordinal regime
such as a sample clock or a TLE epoch. Constraining it to `duration` would make
the keyword unusable for exactly the non-civil regimes that most need it. A
processor that resolves the TRS can check the period against it; one that does
not, cannot, and must say so rather than guess.

### 45. Sample 28 had to invent a `sample_rate` because 1/48000 s isn't representable. Doesn't that show the cadence model is wrong below one second?

It shows the *civil-time* cadence model is wrong below one second, which is why
that sample does not use it. The frame counter is annotated against a sample-clock
`temporalReferenceSystem` meta-type with a period of one sample-clock unit — the
cadence is exact in the system the value is actually expressed in. The
`sample_rate` member is not a workaround for cadence; it is the conversion factor
from that system to seconds, which is information the record must carry anyway
and which no annotation could supply. The episode is evidence for meta-types
rather than against cadence.

**Accepted on the second point, and acted on.** A pattern that exists only in a
sample is a pattern most readers will not find, and the reader who most needs
this one is the reader who has just concluded the keyword cannot do the job.
§The `period` Property now carries it. It says why civil time fails — a duration
is written in seconds and their decimal fractions, and 1/48000 is not a
terminating decimal, so any duration written for it is rounded and the rounding
is in the period, which is the one place an error accumulates. It then gives the
construction: declare the clock as a meta-type, name it in
`temporalReferenceSystem`, and give `period` as a count of that clock's own
units, which for one value per tick is the integer 1. It separates the
conversion factor out as data rather than annotation, since a rate varies per
delivery while the schema does not, and states that a consumer MUST NOT assume a
conventional value for it. A worked example follows the civil-time one.

The drift is quantified rather than asserted, because the objection deserves a
number: `PT0.0000208333S` is short of a 48 kHz frame by about thirty-three
picoseconds, which is nothing in one frame and a full sample every thirteen
seconds of programme, and which keeps growing for as long as the recording runs.

---

## I. Contradicted non-goals

### 46. You define nineteen observation roles and five derivation categories. That is an observation model. Why deny it?

The denial was narrower than it read. What the document declines to be is a
*normative JSON encoding of ISO 19156* — it does not define Observation as a type
you instantiate, does not define the relationships among observation entities,
and does not require any record to be shaped like an observation. What it does
define is a role vocabulary that can be laid over a record someone else designed.
That is a description model, not a data model.

**Accepted, and acted on.** "Defines no observation model" appeared in a list of
things the document defines none of, alongside no vocabulary, no reference
system, no color space, no channel layout, and no code list. Every other item on
that list is true without qualification. That one was not, and putting it in the
same breath as the others made a defensible narrow claim look like an
indefensible broad one.

It has been struck from the list, and the qualification is now stated on its own
rather than buried in a series. The introduction concedes plainly that
`semanticRole` and `derivation` carry a vocabulary of observation concepts, then
says what is actually declined: no observation as a type to instantiate, no
classes for procedures or features, no relationships among observation entities,
and no requirement that a record be shaped like an observation. Two consequences
follow and are stated: a schema carrying none of these roles is not deficient for
that reason, and a processor MUST NOT reconstruct an observation entity from the
roles it finds. The README bullet, which already said "not a full ISO 19156 model
or a normative JSON encoding of that model," now says concretely what that
distinction amounts to.

### 47. `statistic: mean` over a stated window is an analytical claim. Where is the line?

**Accepted on the wording, and acted on.** The line is between describing an
operation that has already happened and specifying one to perform.
`statistic: mean` says this number was produced by taking a mean — a fact about
provenance that a consumer needs in order to avoid averaging averages. What the
document does not do is define what `mean` computes, how to handle gaps, whether
the window is inclusive, or under what conditions a consumer may recompute.
§Processing Conformance closes the loop by forbidding inference of permission to
aggregate.

The non-goal was overstated rather than wrong. "Does not define statistics" is
plainly contradicted by a keyword named `statistic` carrying a closed list of
them. Both the introduction and the README now say the document defines no
analytical *procedures*, and both spell out what that excludes: naming an
operation is not specifying it, and a processor MUST NOT read an instruction out
of an annotation that records one.

### 48. `derivation` + `observingProcedure` + `ingestionTime` is lineage with the word removed. Why the euphemism?

**Fair, and acted on.** These are lineage facts, and calling them something else
would be evasive. The non-goal now says the document defines no lineage *model*
and then says which part of the objection it is conceding: several annotations
plainly carry lineage facts, and what is declined is the graph of entities,
activities, and agents that PROV-O specifies, with its identity and its
derivation chains. What is here is flat and confined to one record — one
procedure identity, one derivation category, one ingestion instant, no chaining
and no activity. A schema that needs lineage in the modeled sense should use
PROV, which these annotations neither replace nor contradict; a record can carry
both, and the `concepts` example already does, mapping a publication instant
onto `prov:generatedAtTime`. The `derivation` section says the same thing
locally: the category does not identify the act that produced the value or
relate it to the values it was derived from. PROV-O is now a normative-adjacent
reference in the bibliography and appears in the vocabularies appendix.

### 49. You enumerate eleven blessed code-list registers and a handful of CRS registries. That is a vocabulary of vocabularies.

It is a taxonomy of register *models*, which is a weaker thing, and it is open —
§The Annotation Model requires a processor to preserve and not reject a `kind`
outside the enumeration, so nobody needs permission to add one. What the
enumeration provides is a shared spelling for the common cases so that two
publishers citing ICAO lists do not write `icao`, `ICAO`, and `icao-doc-7910`.
The maintenance question is real and is treated at question 51.

---

## J. Governance and rot

### 50. Where is the versioning of a referenced definition? EPSG deprecates, CF revises, ICD reissues.

**Rejected, and the reasoning is now in the document.** An earlier draft of this
answer called it a real weakness and put an optional version member up for
consideration. That was wrong, and the mechanism is not going to be added.

Versioning a definition is the job of the body that publishes the definition,
and every body named in the question already does it. The identifiers this
document uses throughout carry a version position by policy — a definition is
named `/def/{objectType}/{authority}/{version}/{code}`, so the `0` in
`http://www.opengis.net/def/crs/EPSG/0/4326` is not padding but an unfilled
version slot, and a schema that needs one edition rather than another fills it
in. An ICC profile goes further and is identified by a digest over its own
contents, so a revised profile is a different profile and cannot be confused for
its predecessor. Pinning is expressible today, by writing the identifier the
publisher supplies. A member here would duplicate an identifier that already
exists.

And it would cost more than it returned. This document would have to define what
a version *is*, across bodies that version by number, by date, by edition, and by
content digest — which is exactly the URI-layout question it declines in seven
other places. No processor could check the member against the reference without
resolving the reference, which none is required to do. Worst, the member and the
URI could disagree, manufacturing a precedence problem that does not otherwise
exist; the `colorSpaces` precedence rules are what that costs, and they are
there because two identifications of one thing were genuinely unavoidable. Here
they are avoidable.

The residual case is a publisher who revises without giving each revision an
identifier. A version member would not help there either, since there would be
nothing for it to carry. §The Annotation Model now says all of this, and directs
such a schema to record the situation in `description`, where it informs a
reader without inviting a processor to act on it. The pre-existing guidance
stands unchanged: §Coordinate Reference Systems defines no coordinate epochs for
dynamic CRSs, and §Security and Privacy Considerations treats deprecation
alternatives as migration advice rather than automatic substitutions and asks
that caching be version-aware.

### 51. `kind` is open with no registry and no collision rule. Two vendors both pick `sensor`. Now what?

Then two schemas use one token for two register models, and a processor that
knows neither treats both as unknown — which is the defined behavior and is
safe, if unhelpful. The document's position is that `reference` and not `kind`
establishes identity, so a collision degrades classification rather than
corrupting meaning.

**Decided, and acted on.** The policy is a registry, and a future revision is
expected to establish one. The URI-shaped convention was the other candidate and
was not taken: it would put a second identifier beside `reference`, which is the
arrangement that forces precedence rules — the cost paid in `colorSpaces` and
declined in question 50 — and it would do so to solve a classification problem
rather than an identification one.

No registry exists yet, so the limitation is now written down rather than left
for a reader to infer. §The Annotation Model states the containment normatively:
a processor MUST NOT treat `kind` as establishing identity, MUST NOT conclude
from two schemas carrying equal `kind` values that they draw on the same
register, and where `kind` agrees while `reference` does not, the references
govern and the agreement establishes nothing. A collision costs classification
and does not corrupt meaning; an unrecognized `kind` is reported indeterminate
and leaves a processor no worse placed than an absent one.

It then says outright that this is containment and not a solution, that a
registry is the remedy, and that until one exists a `kind` value outside those
defined here means something only to a processor that already knows it by an
agreement reached elsewhere. Two pieces of authoring guidance follow: use a
defined value where one fits, and do not coin a broad token such as `sensor` or
`registry` for a private arrangement, because the broadest tokens are the ones
most likely to be coined twice — which is precisely the collision the question
poses.

### 52. What is the deprecation story for the closed enumerations, given they cannot be extended without a new document?

The versioned meta-schema URI is the version identifier, so extending a closed
enumeration means publishing a new meta-schema version and schemas opting into
it by changing `$schema`. That is a deliberate trade: closed enumerations buy
decidable processing at the cost of requiring a version bump to grow. Questions
31 and 34 are exactly the cases where that cost is about to be paid, and it is
better paid now, at v0, than later.

### 53. Annotations aren't checked against data, so they rot silently while looking authoritative. Is confidently wrong metadata worse than none?

**Sometimes yes, and acted on.** This was the strongest criticism in the list and
the document was silent on it. The security considerations now say it in three
parts. First, what validation does and does not reach: it confirms that a named
member exists, that a closed enumeration holds, and that components and units
agree in number and kind, and it cannot confirm that a `reference` still
identifies the definition the values are actually expressed against. An
instrument is recalibrated, a station is resurveyed onto a new datum, a producer
reorders channels, a code list is superseded — and the schema goes on validating
while the annotation goes on reading as authoritative. Second, that stale
annotation is for that reason worse than absent annotation: the prohibitions in
§Processing Conformance guard the absent case, where a consumer knows it does
not know, and they do not guard the stale case, where nothing looks wrong. A
schema author MUST revise annotations in the same change that alters what the
schema describes, and a consumer MUST NOT treat an annotation as evidence more
current than the schema revision carrying it. Third, that the same property
makes annotations a target: a substituted CRS reference relocates every
coordinate, an `alphaMode` moved between `straight` and `premultiplied` alters
every composite, and none of it fails validation or signals anything, so schema
distribution needs the integrity protection the data needs.

### 54. Annotated schemas run twice the line count. Who pays that, and what's the evidence they'll keep paying?

The line-count comparison in
[`samples/real-world/README.md`](samples/real-world/README.md) is the honest
version of the cost, and the answer is that it is paid once by the schema author
and recovered many times by consumers who would otherwise each reconstruct the
same knowledge from documentation — or fail to. There is no evidence yet that
publishers will pay it, because no publisher has been asked. That is the
adoption question, and it is unresolved. See question 56.

---

## K. Evidence and adoption

### 55. Who has implemented this? Where are the two independent implementations?

There are none. There is a meta-schema, a validator that checks schemas and
instances against it, and an annotation checker used across all 43 samples —
all by the same author. The document is Experimental and has not been through
implementation review. This is a legitimate blocker for anything beyond
Experimental status and should not be spun as anything else.

### 56. Has any upstream publisher reviewed these annotations? If not, the samples are fan fiction about other people's schemas.

None has. The samples are retrofits, performed without the publishers'
involvement, and their evidentiary value is bounded accordingly. What they do
demonstrate is non-trivial: that 28 unrelated real payload schemas, none
designed with this extension in mind, can be annotated without restructuring
them, and that doing so surfaces specific ambiguities in each. What they cannot
demonstrate is that the annotations are *correct* in every domain detail, or
that any publisher wants them. Review by even two or three of these publishers
would be worth more than another ten samples.

### 57. The LLM evaluation is self-reported confidence, no control arm on 40 of 43, no blinding, one model. Would you accept that methodology from someone else?

**No. Acted on.** All four objections are correct and none of them is a
qualification — they are design defects. Two things were done.

The framing was pulled back. The README no longer leads with the confidence
ratings, says plainly that the result is an observation rather than evidence,
and lists the four defects before anything else. `EVALUATION.md` opens with the
same notice, records the ratings as self-ratings that carry the weight of
self-ratings, and keeps the run on record because it is what was actually done,
not because the method is sound.

Then the method was replaced. [`evaluation/`](evaluation/) contains a harness
that answers each defect with a mechanism rather than a caveat. `rubric.py`
derives from each annotated schema a list of claims the annotations entail, each
paired with the wrong reading it exists to rule out; nothing in it is written per
sample and nothing in it is a matter of taste. `run.py` runs every sample twice,
once against the schema as published and once against a control built at run
time by the same code that generates the committed unannotated companions — so
all 43 samples have a control and none can go stale. A separate supervisor model
grades the two transcripts, presented as A and B in a seeded random order,
without either schema and without being told there are arms, and every verdict
that is not `unaddressed` must carry a verbatim quote. `--subject-model` is
repeatable and the harness warns when the supervisor is also a subject, because
a model grading itself is not supervision.

The headline number it reports is not accuracy but *hazard*: the share of
claims a transcript got positively wrong. That is the quantity the document is
about. A silent reader is a nuisance; a reader that confidently states the wrong
reference frame is the harm.

One thing the harness does that is worth stating because it is uncomfortable:
blinding a control transcript is imperfect by construction, so the supervisor is
asked afterwards whether it could tell the two apart, and the share of times it
names the annotated arm correctly is reported. Near chance means the blinding
held. Near certainty means it did not, and the figures should be read as an
upper bound. That number is published either way.

### 58. An agent saying "the annotation helped" is not evidence its conclusion was correct. Which outputs were expert-checked?

**None, and acted on — but only the checkable half.** No domain expert reviewed
any of them. They were read by the author, who is not an expert in most of these
28 domains.

The distinction the question is pointing at is now stated in `EVALUATION.md` as
its own section and is enforced in code. A *schema-grounded* claim is one the
annotations entail — that `time_tag` carries phenomenon time, that components
resolved on a named frame are not comparable across frames, that the values are
in `nT`. Whether a transcript got such a claim right is decidable by anyone
holding the schema, and that is what the harness grades. A *domain-correct*
claim is whether an analysis is any good for its field: whether the proposed
fire-detection metric is the one a remote-sensing group would use, whether
something important was left out. Nothing here settles those.

So the harness emits exactly two claims per sample in an `expert` tier — domain
fitness and domain omission — marks them "not entailed by the schema; requires a
domain expert", shows them to a human, and excludes them from every score it
reports. A language model is not a domain expert, and the harness is written so
that one cannot be used as a substitute for the review questions 3 and 56 ask
for. The section in `EVALUATION.md` that describes annotation-driven reasoning
now says the same thing about itself: the claim being made is that the
annotation supplied the fact a proposal rests on, not that the proposal is what
a practitioner would do.

### 59. For METAR and AIS the model already knows the domain. Where's the ablation?

**There wasn't one. Acted on.** Six real-world samples ship an unannotated
companion and an earlier round compared four of them head to head; the 43-sample
run had no control at all. That is now fixed structurally rather than by adding
more companions to the repository: the harness generates the control arm into
the run directory by calling the same `derive()` the committed companions are
built with, so every sample has a control and the two can never drift apart.

Building it surfaced two problems worth recording, because both would have made
the ablation meaningless.

The first is that the control announced itself. The committed unannotated
companions carry a paragraph saying they are a stripped copy and inviting the
reader to compare them against the annotated version, and the annotated samples
carry the mirror-image paragraph explaining what their annotations are there to
show. Both are now cut from both arms, along with the differing `$id`, so the
two schemas a subject sees differ in the annotation keywords and in nothing
else.

The second goes to the heart of this question. A model that knows METAR will
guess right from member names alone, and crediting that as comprehension would
collapse the ablation to zero. So the subject is asked to mark its guesses, and
a transcript that states the correct answer while marking it a guess is scored
`declined`, not `correct`. Knowing that you do not know is a distinct outcome
from knowing, and `declined` is scored as neither success nor harm because it is
the behaviour an unannotated schema ought to produce.

What that still cannot catch is a right answer taken from priors and asserted
without hedging, which is indistinguishable from knowledge in the transcript.
That inflates the control arm, which is the conservative direction — it
understates the difference the annotations make — and it is stated as a limit in
the harness README rather than left for a reader to work out.

### 60. If the answer to "does this work" is an LLM's opinion of itself, is the real value "makes chatbots sound more confident"?

If the LLM evaluation were the only argument, that would be the fair reading of
it. It is not the argument. The argument is that a consumer of any kind cannot
correctly combine two data streams without knowing their reference systems, and
that this information is currently absent from the schema. That was true before
language models and remains true for the ordinary pipeline code that does most
of the world's data joining. The agent experiment is a convenient probe of
whether the annotations are self-describing; it is not the case for the
document, and the README should not lean on it as though it were.

---

## L. The uncomfortable summary question

### 61. Strip out everything that is a pointer to someone else's definition, and everything optional and unenforced. What's left?

Four things.

A **citation form** — one shape for "this member is expressed against that
definition," with defined attachment points and validity rules, so that
references can be compared without being resolved.

A **role vocabulary** for the distinctions that decide whether values may be
combined: which timestamp is the event time, what produced this number, over
what window it applies, at what expected rhythm.

A **mapping surface** that binds a definition's ordered slots — axes, channels,
bands, roles — onto members of a record its author never intended to annotate,
without restructuring it.

And the part that is neither optional nor a pointer: the **prohibitions** in
§Processing Conformance and §Check Outcomes. A processor may not infer a
role from a name, a frame from a sample, an alpha mode from a channel count, or
permission to aggregate from anything. It may not report an unresolved check as
valid. Those are the enforceable core, and they are what turns a set of optional
hints into a specification.

---

## Where the critique lands

The following are conceded above and should be treated as work items rather than
answered objections.

**Evidence and process**

| # | Item |
|---|---|
| 55 | No independent implementations exist. |
| 56 | No upstream publisher has reviewed the retrofitted samples. |
| 60 | Do not lean on the agent experiment as the case for the document. |
| 3 | Seek cross-review from OGC, ICC, and ITU. |
