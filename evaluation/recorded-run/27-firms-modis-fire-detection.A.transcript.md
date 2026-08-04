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
