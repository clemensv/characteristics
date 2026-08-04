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

2. `origin_datetime` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `origin_datetime` as the time the record was produced, received, or published, or using a different member for event time.

3. Successive `origin_datetime` values are expected at cadence `irregular`. A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

4. `report_datetime` is an operational instant (`resultTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `report_datetime` as the event time of the observation.

5. `control_datetime` is an operational instant (`ingestionTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `control_datetime` as the event time of the observation.

6. `latitude` is calculated rather than measured directly.
   wrong reading: Treating `latitude` as a direct measurement.

7. `latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `latitude`.

8. `longitude` is calculated rather than measured directly.
   wrong reading: Treating `longitude` as a direct measurement.

9. `longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `longitude`.

10. `depth_km` is calculated rather than measured directly.
   wrong reading: Treating `depth_km` as a direct measurement.

11. `depth_km` is expressed in `km`.
   wrong reading: Assuming a different or conventional unit for `depth_km`.

12. `magnitude` is calculated rather than measured directly.
   wrong reading: Treating `magnitude` as a direct measurement.

13. `max_intensity` is already a `maximum` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `max_intensity` as though it were a raw sample.

14. `bulletin_type` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `bulletin_type` as an observed quantity.

15. `tsunami_possible` is `estimated` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `tsunami_possible` as a measured observation.

16. `max_intensity` is already a `maximum` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `max_intensity` as though it were a raw sample.


TRANSCRIPT A

# Reading the EarthquakeReport feed

## 1. What this feed is

Each record is **a bulletin about an earthquake, not an earthquake**. That distinction is the single most consequential fact here, and it is carried by the annotations rather than by the shape: the record is bound as a class to `dcmitype:Event`, and at the same time it is declared an observation record (it carries `observedProperty`), with a phenomenon time, a result time, and an ingestion time all distinguished from one another. A bulletin is a statement issued at one moment about a rupture that began at an earlier moment.

Many bulletins describe one earthquake. `event_id` is stated by the schema to be shared by every bulletin for the same rupture, and `serial` to be that rupture's revision sequence. So the natural key of a row is `report_id`, and the natural key of a physical event is `event_id`. **The row is the revision, not the earthquake.** Any count, average, or distribution computed over rows without collapsing to events is a count of *publishing activity*, not of seismicity.

What each bulletin can carry is a computed hypocentre (latitude, longitude, depth), a computed magnitude, a maximum observed shaking intensity for the whole report and a per-prefecture breakdown of the same, a source-region identifier, and the standing of the bulletin itself. Almost none of that is guaranteed to be present. Only the identity, the three timestamps, the Japanese title, the product code, the detail URL, the prefecture array, and the tsunami flag are required. The hypocentre, the magnitude, the intensity, and the source region are all omissible, and the schema itself states that whole classes of product omit them.

There are two additional facts that shape everything downstream. Every scientific quantity in the record is **declared as derived, never as measured** — no member carries `derivation: measured`, and no `observingProcedure` is declared anywhere in the schema. And the product code is declared as `resultQuality`, meaning the record itself tells you that the results it carries are qualified by which product issued them.

## 2. Analyses this stream supports

**Publication latency, and the pipeline behind it.** This is the best-supported analysis in the feed and the one that needs nothing external. Three timestamps are given three *different* declared roles — origin as `phenomenonTime`, publication as `resultTime`, distribution handover as `ingestionTime` — and all three are Core `datetime` with no separate temporal reference system, so they sit in one binding and their differences are meaningful. `report_datetime − origin_datetime` is time-to-solution; `control_datetime − report_datetime` is time-to-distribution. The specification is explicit that operational times such as `ingestionTime` describe the handling of the record and must not be read as the phenomenon or result time, which is exactly why the two differences measure two different stages and must not be merged into one "latency".

**Solution convergence across revisions.** Because bulletins for one event share `event_id` and are sequenced by `serial`, and because the product code qualifies the maturity of each solution, you can trace how the hypocentre, depth, magnitude, and intensity change as an event is re-reported. This is supported precisely because the schema separates the identity of the event from the identity of the bulletin, and because it declares the product code as a quality qualifier of the results rather than as a result.

**Product-mix and field-availability analysis.** The optionality pattern is not incidental: the schema states that particular products omit hypocentre, magnitude, and intensity. Cross-tabulating presence of each field against `bulletin_type` characterises the feed's own coverage and is a prerequisite for every other analysis, because it tells you which strata you are silently dropping when you filter on a non-null magnitude.

**Spatial plotting of hypocentres.** Supported, and safely so, because the coordinate pair carries an explicit CRS binding with an explicit axis order rather than leaving it to be guessed. Plotting is supported; *measuring* is not (see §3).

**Depth-against-magnitude, and depth-against-intensity, as reported.** Supported as relationships among declared values within this feed, with the depth caveat in §3.

**Revision-count and correction-rate analysis.** `info_type` distinguishes issuance, correction, and withdrawal as a closed set with a declared `status` role, so "how often are bulletins corrected or withdrawn, and for what kinds of event" is answerable from the feed alone.

**Analyses this stream does not support.** Event *rates* and catalogue completeness: the cadence is declared `irregular`, and the specification states that cadence is not a completeness assertion and does not assert that every position has a record. Nothing here licenses "N earthquakes per month". Intensity-against-distance or attenuation: the prefectures are identified only by codes whose register the schema does not name, so they cannot be placed on the ground. Anything requiring the tsunami field as ground truth: it is declared `estimated` and described as an inference from free text.

## 3. Combination rules

**`event_id`.** Equality only. It groups bulletins into events, and that is its whole analytic value. Do not order it, difference it, or parse it as a time — it carries no temporal role and no temporal reference system, and the specification forbids inferring a temporal regime from an encoding that does not declare one. Its fixed 14-digit form would sort lexically, and the specification even provides the machinery for declaring exactly that (a `temporalReferenceSystem` with a `position` member rendered at fixed width); the schema does not use it, so the ordering is undeclared.

**`serial`.** Equality, and — as an assumption — ordering *within one `event_id`*. That it sequences revisions is asserted in the schema's prose only; no `sortOrder` and no temporal binding declares it. Never compare serials across different events, never sum them, never average them. A "mean serial" is a number about nothing.

**`report_id`.** Equality only. Do not parse it; it restates two other members and the schema gives no parse rule that a processor is permitted to act on.

**`info_type`.** Equality and grouping only. It is a status, not a grade: the specification states that status qualifies the record rather than the phenomenon, that a change of status does not change what was observed, and that status and result quality are distinct conditions that must not be read as each other. There is no ordering among the three values. **Filter on this before any aggregate**, or withdrawn bulletins will be counted as observations.

**The three timestamps.** Within one role, positions are comparable and differenceable, and the resulting durations may be summed, averaged, and summarised across records. Across roles, a difference is meaningful only *within a single record*, as the latency of that record; differencing one record's origin time against another record's publication time produces arithmetic without a referent. Absolute instants themselves are not summable or averageable — nothing in either file puts them on a scale where addition means anything. And any latency distribution must first fix its unit of analysis: averaging over bulletins over-weights events that were re-reported many times.

Nothing in the schema constrains these three to be monotonic with respect to one another. Do not assume publication follows origin or that handover follows publication; the instance shows that ordering, one instance establishes nothing, and the schema does not enforce it.

**`latitude` and `longitude`.** Comparable across records, because all records declare one CRS (EPSG:4326) with one axis order. The axis order is **latitude first, longitude second** — this is an assertion by the schema author, which the specification says is not to be inferred from names, and it happens to match the authoritative order for that CRS. A consumer that assumes the longitude-first convention common in web mapping will place every point in the wrong hemisphere-pair.

They may **not** be differenced into a distance and may **not** be averaged. A degree of longitude and a degree of latitude are not the same length on the ground; the specification defines no coordinate operation or transformation and requires that transformations not be performed without validating authoritative definitions. Great-circle distance between two hypocentres therefore requires the ellipsoid definition, which is outside these two files, and Euclidean arithmetic on degrees is simply wrong. The mean of a set of angular coordinates is not defined here either, and the declared range crosses the antimeridian.

There is no positional uncertainty in the record, and no per-result quality, so you cannot weight or filter hypocentres by how well constrained they are.

**`depth_km`.** This is the trap in the spatial data. The CRS annotation names only latitude and longitude, and the specification is explicit that properties not named by `coordinates` are not part of the coordinate. Depth therefore has **no vertical reference system at all** — no datum, no axis direction. The specification says in as many words that a height or depth is made interpretable by such a binding, because the number and its unit do not state what the value is measured from. So: comparing and differencing depths is defensible only under the assumption that every record uses one datum and one sign convention, which neither file establishes. Do not concatenate latitude, longitude, and depth into a three-dimensional position as though they belonged to one compound system; they do not, and the specification requires a single compound definition for that.

The schema's prose adds that the sign of the source value is discarded before conversion. That is a lossy step stated in prose, not in any annotation, and it means the encoding cannot distinguish the two sides of whatever surface the source measured from.

**`magnitude`.** Comparable and differenceable *within a stratum*, and the strata matter. Two magnitudes are alike only if they share the product code that qualifies them, because that code is declared `resultQuality` and the specification states that result quality qualifies the result value. It also states that omission of quality never implies acceptable quality, and defines no ordering over any quality scale — so you may group magnitudes by product code but you may not rank the codes, however suggestive their descriptions are.

**Do not sum magnitudes, and treat any average as an average of the reported numbers rather than of the underlying quantity.** The concept binding here says the value is *dimensionless*; dimensionlessness removes the unit obstacle to arithmetic but does not license it. Neither file states that the scale is additive or that it is on a ratio scale, and the schema's own prose names a formula over amplitudes and a comparison to the Richter scale. I am declining to assume additivity.

Two further constraints. No `observingProcedure` is declared anywhere, so you cannot establish that two magnitudes were produced by the same procedure; the specification calls procedure identity comparability-critical and says omission means undeclared. And because bulletins for one event each carry a magnitude, any distribution over rows counts revised solutions repeatedly — collapse to one row per event first, choosing the row by an explicit rule you state.

`null` magnitude and absent magnitude are two different encodings that the schema permits and neither file distinguishes. Neither is zero.

**`max_intensity`, at both the report and prefecture level.** This is **ordinal at best, and not numeric under any reading.** Never average it, never sum it, never difference it. Two values may be compared for equality; ranking them relies on the English labels ("Lower", "Upper"), which are author-supplied glosses — the specification forbids inferring identity or equivalence from labels, and no ordering is declared by any annotation. I mark treating it as ordinal as an **assumption**.

If you do so, sort it with an explicit lookup table. **A lexical string sort is wrong**: `+` precedes `-` in code-point order, so naive string comparison places `5+` below `5-` and `6+` below `6-`, inverting the Upper/Lower pairs. A naive string `MAX` over the prefecture array of the example record would return the wrong element for any event reaching 5 or 6.

Both intensity members are declared as `maximum` over a set of values. The specification says the set is scoped by the record's other annotations — its temporal roles and its feature and procedure roles. Here the declared feature of interest is the *epicentral area*, not the stations, so the set the maximum ranges over is described only in prose. Two maxima are comparable only if their sets are; the report-level maximum and a prefecture-level maximum range over different sets and are **not** like quantities.

Critically, **do not recompute the report-level maximum from the prefecture array**. The specification states plainly that a processor must not recompute a result from a `statistic` declaration, and nothing in either file asserts that the prefecture list is exhaustive or that the two maxima are consistent. They agree in the one example; one example establishes nothing.

**`bulletin_type`.** Equality and grouping only. It is a quality qualifier, and because a record here carries more than one result, it qualifies *all* of them — both the magnitude and the intensity. The specification defines no threshold, ordering, or processing effect for quality. Stratify by it; do not rank by it.

**`epicenter_area_code` and the prefecture `code`.** Equality only, and **you cannot resolve either to a place from these files.** The specification defines a keyword for exactly this purpose — `codedValues`, which binds a coded property to the register that gives its codes meaning — and the schema uses it on neither. So the registers are unidentified, and the specification forbids repairing an unidentified register from labels, property names, descriptions, or samples. `epicenter_area_jp` gives a human-readable name for the epicentral area only; the prefecture codes have no accompanying name at all.

**`affected_prefectures` as a whole.** Counting entries per bulletin is legitimate. Counting across bulletins is not, without collapsing to events, because the set may be restated with each revision. The array is required but nothing declares a minimum length, so it may be empty. Nothing declares it ordered — do not treat the first element as the worst-affected — and nothing declares the codes unique within it.

**`tsunami_possible`.** Three-valued and **not a hazard statement.** It is declared `estimated`, which the specification defines as inferred from incomplete, indirect, or uncertain evidence, and the schema describes it as a text inference made by the bridge rather than a coded field from the source. The three values are not two: `false` is stated to mean an explicit negative in the source text, while `null` means the source text was unavailable or not fetched. **`null` is a state of the pipeline, not a state of the world, and folding it into `false` fabricates negative findings.** Use this field only to characterise the bridge's own behaviour. It carries no semantic role at all, so even its function within the record is undeclared.

**`title_jp`, `title_en`, `detail_url`.** Not analytic quantities. The URL identifies the upstream document; the specification notes that remote resources of this kind are untrusted input and that dereferencing discloses interest, so fetching them at scale is a decision, not a detail.

## 4. Time

**The time axis of the thing described is `origin_datetime`.** It is the only member carrying `phenomenonTime`, and every quantity that declares a relation to phenomenon time — latitude, longitude, depth, magnitude — declares that relation as `instant`, meaning the value applies *at* that position. That is what makes the hypocentre and the magnitude attributable to a moment rather than to a window.

`report_datetime` and `control_datetime` are on the record's axis, not the phenomenon's. The specification states directly that operational and result-time positions describe the handling of the record and must not be read as phenomenon time. Ordering the feed by publication time orders the *bulletins*; ordering by origin time orders the *earthquakes*, with revisions collapsed onto the instant they describe.

**Relation to civil time.** All three are Core `datetime` and carry no `temporalReferenceSystem`. Under the specification that is the correct and complete declaration when Core semantics are fully intended, and the specification's own compatibility table binds that case to an RFC 3339 date and time. The instance renders all three with a `Z` offset, and the schema's prose says the source values are converted to UTC. So positions are civil-time instants, comparable directly, with no reference-regime translation required.

Two limits on that. Whether the schema permits a non-UTC offset on these members is governed by JSON Structure Core, which is not among the files I hold — **I decline to decide it**. And nothing in the schema pins the offset to `Z`, so a consumer should normalise on read rather than assume.

**The timestamp-shaped strings are not on the time axis.** `event_id` is a 14-digit identifier bound to `dcterms:identifier` and given no temporal role; the detail URL embeds two more digit strings. None of these carries a temporal reference system, and the specification forbids reading a temporal regime out of an undeclared encoding. Treat all three as opaque.

There is a live inconsistency here that I flag and do not resolve. The schema states that the source publishes with a local offset and that the control timestamp is converted *from JST* to UTC. In the one instance, the identifier digits and the two digit strings in the URL are numerically identical to the UTC-labelled fields. Either those source-native strings were already UTC — in which case the stated conversion is a relabelling — or the instance was not produced by the conversion the schema describes. **The two files do not decide which, and I decline to guess.** The operational consequence is the same either way: never derive a time from `event_id` or from the URL, and never assume the identifier and the origin timestamp agree.

**Cadence.** `origin_datetime` declares an `irregular` cadence. The specification is emphatic about what that does *not* mean: cadence is an expectation and not a constraint, it is not a completeness assertion, it does not assert that every position has a record, and no instance is invalid for departing from it. There is therefore no basis in this feed for a rate, a frequency, or a "we saw everything in this window" claim. Note also that successive values of `origin_datetime` across the stream are not successive earthquakes, because revisions repeat the same origin time.

`max_intensity` — at both levels — carries **no** phenomenon-time relation, no boundary roles, and no support period. The specification says explicitly that omission is not `instant`. So the temporal extent of the intensity maximum is **indeterminate**: you cannot say it applies at the origin instant, and you cannot say what window it summarises. Any statement of the form "maximum intensity during period X" is unsupported by these files.

## 5. Ambiguities

Marked as **declining** where the files do not decide, and as **guess/assumption** where I have taken a position anyway.

- **Whether `serial` orders revisions.** Asserted in prose; no `sortOrder` or temporal binding declares it. Using it as an ordering is an **assumption** — a well-founded one, but not one a processor is entitled to make from the annotations.
- **Which bulletin for an event is authoritative, and what supersedes what.** Not determined. **Declining.** The files give no "latest wins" rule; you must state your own selection rule explicitly.
- **What `CANCELLED` implies for previously issued bulletins of the same event.** Not determined. **Declining.** The specification says a status change does not change what was observed, but it does not say whether a withdrawal invalidates its predecessors. This must be settled outside the data before any aggregate is trusted.
- **Whether `ISSUED` implies the first bulletin for an event.** The gloss says "first publication of *this bulletin*", and the example carries `ISSUED` at serial 2. So the scope is the revision, not the event. That reading is a **guess** from the label wording; labels are not binding under the specification.
- **Whether the identifier strings encode UTC or local time.** Not determined, and, as described in §4, the descriptions and the instance appear to disagree. **Declining.**
- **Whether absent and `null` differ in meaning** for the four members that are both optional and nullable. Not determined. **Declining** — treat them as distinct signals of unknown meaning rather than collapsing them.
- **Whether a record may carry a latitude without a longitude.** The schema does not forbid it, and the CRS binding names two optional members. A half-coordinate validates. Guard for it.
- **What register the area and prefecture codes come from.** Not identified; the keyword for identifying it is unused. **Declining** to resolve any code to a place.
- **Whether the shindo scale is ordinal in the order the labels suggest.** Not declared by any annotation. Treating it as ordinal is an **assumption**; treating it as numeric or interval-scaled would be an error under any reading.
- **Whether the report-level maximum equals the maximum over the prefecture array, and whether that array is exhaustive.** Not established. **Declining**, and recomputation is forbidden by the specification regardless.
- **The depth datum, sign convention, and axis direction.** Not established — there is no vertical reference binding. **Declining.**
- **What the observed property actually is.** The reference points at a placeholder catalogue on a non-resolvable domain, and the specification says an unresolved reference is indeterminate and must not be repaired from names, descriptions, units, or samples. **Declining.** This blocks any join to another feed on observed-property identity.
- **Whether the record-level observed property covers the intensity result.** By the specification's own scoping rule it does, since that result declares none of its own — which would attribute a hypocentre-and-magnitude observable property to a shaking-intensity value. I read this as a **modelling defect** rather than a claim about the domain, and I flag it rather than act on it.
- **Whether the record-level observed property covers the coordinates.** They carry derivation and a phenomenon-time relation but are not given a result role, so the scoping rule may or may not reach them. Not determined. **Declining.**
- **The declared derivation of the hypocentre.** It is `calculated`, which under the specification asserts determinism. The schema's own description says the position is obtained by inverting arrival times across a network — and the specification's worked example of that exact situation classifies it as `estimated`. A processor must act on the declared value; a human analyst should not read `calculated` here as "reproducible with no inferential error". I flag the discrepancy and **decline** to decide which is right.
- **Procedure identity.** No `observingProcedure` is declared anywhere. Under the specification, omission means undeclared, so you cannot establish that any two values in this feed were produced the same way. This is a hard limit on pooling, not a detail.
- **The `altenums` construct.** It comes from the alternate-names extension, whose specification is not among the files I hold, so I cannot state its normative effect. I have treated its contents as author-supplied labels only, which is the conservative reading and consistent with the specification's prohibition on inferring equivalence from labels.
- **The `symbol` annotation on the coordinates.** Governed by the units specification, which I do not hold. **Declining** to say anything about it.
- **The trailing `_1` in the detail URL of the example, against `serial` 2.** Unexplained by either file. **Declining.** It is a reason not to derive anything from the URL's structure.
- **The identifiers throughout use non-resolvable placeholder domains.** Nothing in this feed can actually be dereferenced from what is given, so every external check the specification defines is indeterminate here, and the specification requires that an indeterminate check never be reported as valid.


TRANSCRIPT B

# Reading the EarthquakeReport feed

## 1. What this feed is

**These records are bulletins, not earthquakes.** That is the single most important
thing to understand before touching the data.

Each record is one published revision of a Japan Meteorological Agency report
about a seismic event. The unit of the row is the report; the unit of the
phenomenon is the earthquake. They are related many-to-one: a stable event
identifier is shared by every bulletin describing the same earthquake, a serial
number orders the revisions within that event, and a composite report identifier
is the actual primary key of a row. A single earthquake will therefore appear
several times in the stream, with progressively refined values, and the record
that says a bulletin was *cancelled* is itself a row.

What each row carries is a **solution**, not a measurement. The hypocentre
coordinates, the depth and the magnitude are all marked as calculated: they are
the output of inverting arrival times and displacement amplitudes across a
national network, not readings taken off an instrument. The maximum intensity
values — both at report level and per prefecture — are marked as statistics,
specifically maxima over the set of stations that had reported by the time the
bulletin was cut. The tsunami flag is marked as *estimated*, and its description
is explicit that it was inferred from free-text commentary by the ingestion
bridge rather than read from a coded field published by JMA.

So the feed mixes three provenance classes in one row: values computed by the
publishing authority, statistics summarised by the publishing authority, and one
value guessed by the pipeline. They should not be trusted equally.

A fourth thing sits alongside the results: the bulletin product code carries the
role of *result quality*. It is not a category for faceting a chart, it is the
maturity grade of the solution in that row. One of its values is documented as a
flash issued before the source parameters have been determined at all. Rows of
that kind are structurally incapable of carrying a hypocentre or magnitude.

## 2. Analytics worth running

**Solution latency.** The two published time members are declared with distinct
roles — one is the time the rupture began, the other the time the solution became
available — and a third records handover into the distribution channel. Their
differences are therefore well-defined and meaningful: report-minus-origin is how
long JMA took to produce a solution; control-minus-report is how long the
distribution system took to move it. Stratified by bulletin product code, this
directly measures the timeliness contract of each product class. This is the
cleanest analysis in the stream because the schema does the hard part — telling
you which instant means what — that a raw feed would leave you to guess.

**Revision convergence.** Group by event identifier, order by serial, and watch
magnitude, coordinates, depth and maximum intensity move. Because the source
parameters are explicitly calculated quantities and the intensity is explicitly a
maximum over a growing station set, the drift between serials is *solution
refinement and reporting completeness*, not physical change. This tells you how
much an early bulletin can be trusted, how much magnitude typically moves between
first and final, and how long it takes to stabilise. It is also the analysis most
often destroyed by people who treat rows as events.

**Catalogue construction and seismicity statistics.** Collapse to one row per
event — latest serial that is not a cancellation and that actually carries a
determined hypocentre — and you have a usable catalogue for event rates,
magnitude distributions, depth distributions and spatial patterns. The
identifier/serial/status triple is exactly what makes this deduplication
possible, and its presence is the reason this feed can be used for catalogue work
at all.

**Source-region profiling.** The epicentre area code is a stable coded identifier
for a seismic source region, and a coordinate reference system is declared for the
coordinate pair, so grouping by region and characterising its depth and magnitude
distribution is supported.

**Shaking versus source.** Within the product class that carries both, you can
relate maximum intensity to magnitude and depth. This is supported because both
appear in the same row for the same event, at the same phenomenon instant.
Intensity must be handled as an ordered category throughout.

**Pipeline and data-quality monitoring.** The rate of corrections and
cancellations, the rate at which the English title is absent, the rate at which
the tsunami flag is null, and the rate at which coordinates are omitted broken
down by product code, are all directly measurable and are genuinely diagnostic
because the schema distinguishes authority-published values from bridge-inferred
ones.

**What is not supported.** Total energy release (see §3 on magnitude). Anything
about whether a tsunami occurred — the flag is an estimate of a bulletin's
*intent*, not an observation. Intensity at any specific place: there are no
station-level values and no prefecture geometry. Rupture duration or extent:
every computed quantity is tagged as relating to an *instant*, so the record
describes a point in time and nothing in it bounds an interval.

## 3. Combination rules

| Quantity | Compare | Difference | Sum | Average | Condition |
|---|---|---|---|---|---|
| Event identifier | equality only | no | no | no | Nominal. Digits, but an identifier. |
| Serial | yes, **within one event only** | within one event only | no | no | Ordinal revision index; has no cross-event meaning. |
| Report identifier | equality only | no | no | no | The true row key. |
| Information type | equality only | no | no | no | Categorical status; counts by category are fine. |
| Origin time | yes | yes, **after deduplicating to one row per event** | no | no | Instants. Differencing two bulletins about the same quake yields zero and is a bug, not a result. |
| Report time, control time | yes | yes | no | no | Different axes from origin time. |
| Latency (report − origin, control − report) | yes | yes | yes | **yes** | Durations. This is the derived quantity that *is* safe to average. |
| Latitude, longitude | yes | see below | **no** | **no** | Angular; see below. |
| Depth | yes | yes | rarely meaningful | yes, within a defined population | Kilometres, ratio scale. |
| Magnitude | yes | yes, with care | **no** | **only with a caveat** | See below. |
| Maximum intensity (both levels) | **order only** | **no** | **no** | **no** | Ordered categories, not numbers. |
| Prefecture count per record | no | no | no | no | Reflects reporting completeness, not the earthquake. |
| Epicentre area code, prefecture code | equality only | no | no | no | Nominal, and **not the same code space**. |
| Tsunami flag | equality only, three-valued | no | no | no | Estimated, not published. |
| Bulletin product code | equality only | no | no | no | A quality grade, not a result. |

**Coordinates must not be arithmetically averaged.** Degrees of latitude and
longitude are angular coordinates on a declared geodetic reference system. Their
plain arithmetic mean is not a centroid, their plain difference is not a
distance, and longitude wraps. Any spatial aggregation must be done geodesically
or in a projection. Latitude, longitude and depth are also documented as coming
out of one joint inversion: their errors are correlated and they must not be
treated as three independent measurements.

**Magnitude.** Comparison and ordering are safe; so are counts above a threshold
and quantiles. Summing is never meaningful. Whether the arithmetic mean is
meaningful depends on whether the scale is logarithmic in the underlying physical
quantity — the two files say only that it is dimensionless, computed from
displacement amplitudes by the published JMA formula, and "similar to Richter
magnitude for shallow events". *I am assuming, from outside these files, that it
is logarithmic; the files do not state it.* On that assumption a mean magnitude
must never be read as an energy average. Independently of that assumption,
magnitudes here are on the JMA scale only and must not be pooled with magnitudes
from any other catalogue.

**Intensity must never be arithmetised.** The scale includes "5-" and "5+" as
distinct values. There is no numeric interpretation under which these behave. A
mean intensity, a sum of intensities, or a difference of two intensities are all
meaningless. Ordering is available, and *maximum* is available and composes
correctly — the maximum over a set of prefecture maxima is a valid maximum. The
mean of a set of maxima is not a mean of anything. Note also that the scale is
closed at 7: it cannot distinguish among the most severe events, so 7 is a
ceiling category and any distribution is censored at the top.

**Do not count the report-level maximum and the prefecture maxima as separate
observations.** The report-level value is a maximum over a station set that
includes the stations behind the prefecture values. Pooling them double-counts.

**Do not mix the three time axes.** Binning by report time or control time and
calling the result seismicity is wrong: the source parameters are attached to the
origin instant, and the report time reflects the operations of the agency, not
the behaviour of the Earth.

**Do not pool across bulletin product codes without stratifying.** Product codes
denote different solution maturities, including one issued before source
parameters exist. A magnitude distribution computed over an unstratified mix is a
mixture of populations of different quality.

**Absence is not random, and absence is not null.** Two different missingness
mechanisms are in play. Some members are nullable and will carry an explicit
null; others are neither required nor nullable and will simply *not be present*.
Code that treats a missing key and a null value as the same thing will
mis-handle one of the two. More importantly, the omissions are documented as
systematically tied to the bulletin product class — flashes, commentary bulletins
and source-element update notices are the ones that lack coordinates, magnitude
and intensity. Dropping incomplete rows therefore silently filters by product
maturity. That is usually the right thing to do, but it must be a decision, not
an accident. A missing intensity means "this product carries no intensity
summary", not "no shaking".

## 4. Time

The time axis of the thing described is the **origin time** — the instant at which
rupture began. It is the only member carrying the phenomenon-time role, and it is
the instant to which the hypocentre, depth and magnitude are attached; all of
those are tagged as relating to an instant rather than to an interval. The report
time is the result time (when the solution became available) and the control time
is the ingestion time (handover to distribution). Both are properties of the
publishing process, not of the earthquake. Report time is later than and
independent of origin time by the schema's own statement, so the two must never
be substituted for one another.

The origin-time axis is declared to have **irregular cadence with no period**.
Consequences: there is no expected spacing, so nothing may be resampled,
interpolated or gap-filled as though it were a regular series; and the absence of
a record in an interval is not a zero-valued sample, it is simply no bulletin.

All three timestamps are RFC 3339 and are stated to have been normalised to UTC;
the example carries a `Z` offset on each. The upstream feed is described as
publishing in Japanese local time with a local offset, so **rendering these back
to civil time for a Japanese audience requires converting out of UTC**. The files
do not state the numeric offset. *I am assuming, from outside these files, that
it is UTC+9.*

There is a discrepancy here that anyone building on this feed will hit. The event
identifier is documented as JMA's rendering of the origin time in
`YYYYMMDDHHMMSS` form, and the origin time is documented as having been converted
to UTC. If the identifier is copied unchanged from a local-time source and the
timestamp has been shifted, the two should disagree by the offset. In the example
they agree digit for digit, and the digits embedded in the detail URL follow the
same convention. Either the identifier was rebuilt after conversion, or the
timestamps are local-time values wearing a `Z`. **I am declining to decide which.**
The operational rule that holds either way: do not parse the event identifier as a
UTC timestamp, do not assume the identifier and the origin time agree, and treat
the identifier strictly as an opaque key.

## 5. Ambiguities

**Origin time versus the identifier digits.** As above. *Declining to decide.*
Consequence stated above.

**Whether the coordinate is a precise hypocentre or a representative point for a
named source region.** The member is described as a hypocentre coordinate, but the
source path it is drawn from is the coordinate of the hypocentre *Area*. These are
not the same thing, and the difference matters for anything distance-based.
*Declining to decide.* Until resolved, do not compute epicentral distances and
present them as precise.

**No uncertainty is published for any computed value.** No error ellipse, no depth
uncertainty, no magnitude standard error. Not determined by these files.
Consequence: no weighting, no confidence intervals, no principled outlier test on
the source parameters.

**Scope of a cancellation.** Whether a cancelled bulletin retracts only that
serial or invalidates the event entirely is not determined. *Declining.* The
conservative reading — exclude the event from a catalogue until a later
non-cancelled bulletin appears — is a choice, not something the files license.

**Whether the serial is per event or per event-and-product.** An event may
plausibly produce a flash and then a full hypocentre-and-intensity bulletin under
one identifier. If the serial is shared across products, "take the highest serial"
may select a different product than intended. *Declining.* Deduplicating by
identifier *and* product code is the safer construction.

**The trailing integer in the detail URL.** In the example it is `1` while the
serial is `2`. What it denotes is not determined.

**Whether the prefecture list is complete, and whether it may be empty.** The array
is always present, but nothing establishes that it enumerates every prefecture
that felt the event, nor what an empty array would mean. Not determined.

**Prefecture codes and epicentre area codes appear to be different code spaces** —
the example uses `290` for the source region and `400`/`410`/`300` for
prefectures. *This is a guess* based on one record and on the differing
descriptions; the files publish neither code list. Do not join the two on code
equality without confirming.

**Sign information in depth is discarded.** The transformation is documented as
taking the absolute value of a signed source figure. Whether that sign ever
carried meaning is not determined; if it did, it is not recoverable from this
feed.

**The observable-property and schema identifiers are placeholders** pointing at
non-resolvable hosts, so the authoritative definition of the observed property
cannot be consulted. Not determined.

**The record's declared concept is a generic "Event", while the record is in fact a
report about an event.** I read this as a modelling looseness rather than a claim
that one row equals one earthquake — everything else in the two files points the
other way — but *that reading is my inference*, not something the files state.

**The annotation vocabulary itself** — the meanings of the derivation, statistic,
cadence, semantic-role and phenomenon-time-relation keywords — is referenced but
not available to me. I have read them from their names and from the surrounding
descriptions, which are consistent, but I have not verified them against their
defining specification.


TRANSCRIPT C

# Earthquake bulletin feed — analyst's briefing

## 1. What this feed is

Each record is **a bulletin about an earthquake, not an earthquake**. The pairing of
an `event_id` with a monotonic `serial`, plus an `info_type` drawn from
`ISSUED` / `CORRECTED` / `CANCELLED`, means one seismic event generates a *chain*
of records over time, each one a revised or withdrawn statement about the same
event. The example is `serial: 2` — already a second statement about that event —
and its `report_id` is the event key and the serial glued together.

Each bulletin carries a full restatement of the event parameters: where it
happened (coordinates, depth, and a named source region), how big it was
(magnitude), how strongly it was felt (an intensity grade, both overall and
broken out by prefecture), whether a tsunami is in play, and a URL to a
per-bulletin detail document. It also carries three distinct timestamps and a
product-type code (`bulletin_type`) identifying which of several bulletin
products this is.

The single most consequential thing to understand before touching this data:
**the row count is a count of bulletins, not of earthquakes**, and later rows
supersede earlier ones. Any analysis that does not first collapse the chain to
one row per `event_id` will over-count events, over-count tsunami flags,
double-count prefectures, and mix preliminary estimates with revised ones.

## 2. Analytics worth running

**Dissemination latency.** Three absolute instants are present on *every*
record, and they are required, so `report_datetime − origin_datetime` and
`control_datetime − report_datetime` are computable with no missingness and no
imputation. This supports a well-founded latency distribution: time from the
event itself to a public statement, and the further processing delay after that.
It can be cut by `bulletin_type`, by `serial` (first bulletin vs. follow-ups), by
`max_intensity`, and by epicenter area. This is the analysis the data supports
*best*, because it depends only on fields that are mandatory and absolute.

**Revision behaviour.** Because the event parameters are restated in full on
every bulletin, and the bulletins are ordered within an event by `serial`, you
can measure how the picture of an event changes as it matures: how much the
coordinates move, how the depth and magnitude estimates shift, whether the
intensity grade is revised up or down, and how long after the origin the
parameters stop changing. You can also measure how often a first bulletin is
followed by a `CORRECTED` or `CANCELLED` one — an operational quality signal for
the feed itself.

**Shaking footprint versus source parameters.** Each bulletin lists the
prefectures that reported shaking and the strongest grade in each. That supports
a study of how far and how strongly shaking is reported as a function of
magnitude, depth, and source region — count of prefectures reporting, highest
grade reported, and the drop-off in grade across the affected set. The response
variable here is an *ordinal grade*, not a number, so this must be done with
ordinal methods (rank correlation, proportional-odds style models, contingency
tables). Treating the grade as a number will produce results that look fine and
are not.

**Source-region climatology.** After collapsing to one row per event, the
coordinates, depth, magnitude, and named area support the usual descriptive
work: event counts and depth/magnitude distributions per named source region,
and depth-versus-location structure. Note that the schema caps depth at 700 km,
which tells you the feed is expected to cover deep events, not only crustal ones.

**Tsunami-flag conditioning.** `tsunami_possible` is mandatory on every bulletin,
so you can measure how the flag co-varies with magnitude, depth, and source
region, and how often it is revised between serials. This is only sound if nulls
are handled explicitly (see §5) and if you dedupe to the *final* bulletin, since
an early flag may be withdrawn.

**Feed-quality monitoring.** Serial gaps, events whose chain never reaches a
terminal state, records missing an epicenter name or a magnitude, and
prefecture codes that appear or disappear over time are all directly observable
and are worth a standing dashboard. Missingness here is not random — it is a
statement about how mature the bulletin is.

## 3. Combination rules

**Intensity grades** (`max_intensity`, at both the record level and inside
`affected_prefectures`). These are labelled `1`…`4`, `5-`, `5+`, `6-`, `6+`, `7`.
They may be **compared and ranked**; they may **not** be differenced, summed, or
averaged. The `+`/`-` variants at 5 and 6 make it plain that the labels are
category names, not measurements — there is no quantity for which "5+" minus
"5-" has a value. The mean of a set of grades is undefined; the *maximum* of a
set of grades is well defined, because a maximum only needs an ordering. So
max-of-max across prefectures is legitimate; mean-of-max is not. Ranking rests
on the assumption that the enumeration is listed in increasing severity, which
the files do not state in words — I treat it as established by the label forms
themselves, but flag it in §5.

**Prefecture intensities specifically.** Each entry is already an aggregate — the
strongest grade observed somewhere in that prefecture. Aggregates of that kind
cannot be re-aggregated into a total: three prefectures at grade 4 do not make
anything "greater" than one prefecture at grade 4. You may count how many
prefectures reached a given grade; you may not add or average the grades. Also,
**absence from the list is not a zero**. There is no grade below `1` in the
scale, so a prefecture that felt nothing and a prefecture that was never
assessed are represented identically — by omission. Do not fill omitted
prefectures with a floor value.

**Magnitude.** The files give a bare number with no unit, no named scale, and no
statement of what physical quantity it is linear in. Two magnitudes may be
compared and ranked **only under the assumption that all records use one and the
same scale**, which the files do not assert — and `bulletin_type` shows that
several distinct bulletin products feed this stream, so the assumption is not
free. Summing magnitudes is meaningless under any reading. Averaging magnitudes
across events is a decision I decline to bless from these files alone: whether
an arithmetic mean of these numbers means anything depends on what the scale is
linear in, and the files do not say. Averaging the *successive magnitude
estimates for one event* across its own serials is separately wrong — those are
revisions of one quantity, and the correct summary is the last one, not the mean.

**Depth.** A length in kilometres, bounded 0–700, and the only unambiguously
ratio-scaled quantity in the record. It may be compared, differenced, averaged,
and binned across records. One caveat: the files do not state the reference
surface the depth is measured from, so depth is comparable *within* this feed
but not automatically against depths from any other source.

**Latitude and longitude.** Comparable and mappable. They may **not** be
differenced as if degrees were a distance: a degree of longitude is not a fixed
ground distance and shrinks toward the poles, so coordinate deltas are not
displacements. Averaging coordinates across events yields a rectangular centroid
that is not a spherical mean and that will sit in the wrong place for any
spatially spread set; use it only as a rough label, never as a location. The
files name no geodetic datum or reference frame, so these coordinates should be
treated as internally consistent and not as interchangeable with coordinates
from another source without a stated datum.

**Timestamps.** All three are absolute instants and may be differenced freely,
both within an event and across events, in either direction — this is what makes
the latency analysis sound. They may be ordered and binned. Averaging instants
is meaningful only as "mean time of day/date" and is rarely what you want;
averaging *differences* of instants (mean latency) is the well-formed operation.
Never difference a timestamp on one record against a timestamp on another record
*of a different kind* without saying so — `control_datetime` on one bulletin
minus `origin_datetime` on another bulletin of a different event is a number
with no referent.

**Serial.** An ordinal position **scoped to its `event_id`**. It may be compared
only against other serials carrying the same `event_id`, where it establishes
which bulletin is later. Across events it means nothing: serial 5 of one event
and serial 5 of another are not comparable, are not "the same stage", and their
difference is not a quantity. Never sum or average serials. The maximum serial
per event is a legitimate derived count ("how many bulletins this event
required"), subject to the gap question in §5.

**Identifier and category strings** — `event_id`, `report_id`,
`epicenter_area_code`, prefecture `code`, `info_type`, `bulletin_type`,
`detail_url`. All nominal. Equality and grouping only; no ordering, no
arithmetic, no averaging. `epicenter_area_code` (`290`) and prefecture `code`
(`400`, `410`, `300`) are digit strings that will silently coerce to integers in
most tools — do not let them, and do not compute on them. Whether those two code
sets even inhabit the same namespace is not determined by the files, so do not
join one to the other.

**`tsunami_possible`.** A three-valued field: true, false, and null. Counting
true is fine after deduplication; treating null as false is a substantive
decision the files do not authorise. Within one event the flag may change
between serials, so the event-level answer is the value on the surviving
bulletin, not the disjunction over the chain.

**Cross-record combination in general.** Before *any* aggregate over this stream,
collapse each `event_id` to a single bulletin — normally the highest serial —
and decide explicitly what to do with `CANCELLED` chains, which appear to
withdraw rather than update. Aggregating the raw stream weights events by how
many bulletins they happened to generate, which correlates with severity, and
therefore biases every result in a direction that looks plausible.

## 4. Time

Three timestamps are present, and they are not interchangeable.

**`origin_datetime` is the time axis of the thing described.** It is the instant
of the earthquake itself. Every question about seismicity — rates, inter-event
intervals, time-of-day patterns, clustering, before/after comparisons — must be
placed on this axis. It is also the only one of the three that is stable across a
revision chain in principle: the other two advance with each new bulletin, so
plotting events on them will smear a single earthquake across the timeline.

`report_datetime` and `control_datetime` are the time axis of the *bulletin* —
when the statement was made and when it was handled. They are the right axis for
studying the feed's own behaviour (latency, revision cadence, operational load)
and the wrong axis for studying earthquakes.

**Relation to civil time.** All three are absolute instants carrying an explicit
UTC offset in the example (`Z`), so each denotes an unambiguous point on the
global timeline and converts to any civil clock by applying that zone's offset
rules. They are not floating local times and must not be read as wall-clock
readings in some implied local zone. Consequently, differences between them are
true elapsed durations and are unaffected by daylight-saving transitions or zone
choice.

The files do **not** establish the local civil zone in which these events occur
or in which the bulletins are authored. Any "time of day" analysis therefore
requires you to choose and declare a zone; the data will not choose one for you,
and a time-of-day histogram built directly on the UTC values is a histogram of
UTC, not of local day and night. Whether the offset is always `Z` or merely
happens to be so in this one example is not established either.

Within the single example the three timestamps are ordered
origin ≤ report ≤ control, which is the only ordering that makes sense given what
they denote — but the files impose no constraint enforcing it, so validate rather
than assume, and expect the occasional inversion.

## 5. Ambiguities

**Whether a later bulletin fully supersedes an earlier one or amends it.**
Not determined, and this is the highest-stakes gap in the pair of files. Every
bulletin restates every parameter, which *suggests* full replacement, but
nothing says so. If bulletins were ever partial, "take the highest serial"
would silently drop fields. I am declining to decide this; it must be resolved
before building any event-level table.

**What `CANCELLED` withdraws.** Whether it retracts the whole event or only the
preceding bulletin is not determined. I decline to decide it. It changes event
counts directly.

**The ordering of the intensity grades.** The files never state that the
enumeration is ordered by severity. I am treating `1 < 2 < 3 < 4 < 5- < 5+ <
6- < 6+ < 7` as established by the label forms and their listed order — that is
a *strong inference*, not something the files assert, and I mark it as such. If
it is wrong, every ranking and every "maximum" in this document is wrong with it.

**Whether the record-level `max_intensity` is the maximum over
`affected_prefectures`.** In the example it is (top level `4`; prefectures `4`,
`3`, `2`). One example does not establish a rule. **Guess:** it is the maximum,
and the two are redundant. Do not rely on it — if you need the relation, verify
it across the corpus, because a mismatch may be meaningful (e.g. an intensity
observed outside the listed prefectures) rather than an error.

**Three different ways of saying "missing", with no stated distinction.**
Some fields may be absent but never null; `magnitude` may be absent *or* null;
`tsunami_possible` must be present but may be null. The files do not say whether
absent and null mean different things — "not yet determined" versus "not
applicable" versus "withheld". I decline to decide; treat the distinction as
unknown and preserve it rather than normalising nulls and absences together.

**What the magnitude scale is.** Not determined — no unit, no scale name, no
stated bounds. This blocks any principled averaging (see §3) and blocks
comparison against magnitudes from any other source.

**Whether all bulletin types report on the same scales.** `bulletin_type` has six
values, implying six distinct products, and the files say nothing about whether
they populate magnitude and intensity identically. I decline to assume they do.
Segment by `bulletin_type` before pooling.

**The `bulletin_type` value `VXSE5k`.** Its siblings all end in a digit; this one
ends in a letter. Whether it is a literal code, a wildcard, or a family
placeholder is not determined. I decline to decide.

**Code namespaces.** Whether `epicenter_area_code` and prefecture `code` share a
scheme, what the codes denote, and whether the code sets are stable over time
are all undetermined. There is no lookup table in the material, so codes cannot
be resolved to places at all — only the epicenter's *name* is given, and only in
one language, and only when present.

**Reference frames.** No geodetic datum for the coordinates and no reference
surface for depth. Both are undetermined; both matter the moment you join to
anything external.

**Serial semantics.** Whether serials start at 0 or 1, increment by exactly one,
and never repeat is not determined. The example jumps straight to 2 with no
serial-1 record present in the material. Do not infer "number of bulletins" from
the maximum serial without checking.

**Uniqueness.** Nothing states that `report_id` is unique, that `(event_id,
serial)` is unique, or that a prefecture code appears at most once in
`affected_prefectures`. Deduplicate defensively.

**Empty and absent prefecture lists.** The list is mandatory but may evidently be
empty, and no minimum is imposed. Whether "empty" means "no shaking reported"
or "not yet assessed" is not determined — and given that revision chains exist,
both readings are plausible at different serials.

**Granularity floor.** The record is closed and carries intensity only at
prefecture level. Sub-prefecture or station-level analysis is not possible from
this feed; the per-bulletin `detail_url` may carry more, but nothing in the
material describes what is behind it, so I decline to assume it does.

**Feed completeness and delivery order.** Nothing establishes that the stream
contains every bulletin, arrives in order, or arrives at all for every event.
Treat gaps as unexplained rather than as absence of events.

**Retention of the event key across time.** `event_id` is 14 digits and in the
example equals `origin_datetime` rendered as `YYYYMMDDhhmmss`; `report_id` is
that key with `_2` appended. Both are single-example observations, not stated
rules. **Guess:** the composition is as it appears. Do not parse a time out of
`event_id` in production code on the strength of it — use `origin_datetime`,
which is typed as a timestamp and means what you need it to mean.


TRANSCRIPT D

# Earthquake report feed — analyst's briefing

## 1. What this feed is

Each record is a **bulletin about an earthquake, not an earthquake**. It is one revision of an official Japanese seismological report: a statement, issued at a particular moment by a publishing agency, of where and how large an earthquake was and how strongly the ground shook in the places that observed it.

The same earthquake generates many records. They are tied together by a stable event identifier and ordered by a serial number that marks the revision sequence. A record also declares its own standing in that sequence — a fresh issue, a correction of an earlier issue, or a cancellation.

The physical content of a record is a *computed solution*, not a set of instrument readings. The hypocentre (latitude, longitude, depth) is obtained by inverting arrival times across a national seismograph network. The magnitude is obtained by applying a published formula to displacement amplitudes across that network. The headline shaking value, and each per-prefecture shaking value, is a **maximum taken over the stations that contributed** — a statistic over observations, not a reading. Nothing in a record is a direct measurement of anything.

One further piece of the physical content is not published at all but *inferred*: the tsunami flag is the bridge's reading of free-text commentary, described in the source material as an estimate of the bulletin's intent. Tsunami-specific products are explicitly excluded from this feed.

## 2. Analytics worth running

**Solution convergence within an event.** Group by event identifier, order by serial, and watch the hypocentre and magnitude move. This is the single most defensible analysis here, because the event identifier is stated to be stable across bulletins and the serial is stated to define the revision sequence. It answers: how far does an epicentre migrate between the first and final bulletin? How much does magnitude move? Does depth move more than the horizontal position?

**Publication latency, decomposed.** Three distinct instants are recorded, with three stated and different meanings: when the rupture began, when the solution became available, and when the finished bulletin was handed to the distribution channel. Their differences are two separate latencies — *time to solution* and *time to distribution* — and confusing them is a common error. Both are worth tracking by revision number and by product code.

**Revision and retraction behaviour.** How often does an event receive a correction? How often a cancellation? At which serial does that usually happen? Supported directly by the standing field's three-valued meaning.

**Magnitude–depth–shaking relationship.** The strength of shaking against magnitude and depth is a classic attenuation question, and this feed carries all three per event. It must be modelled as **ordinal** in the shaking variable (see §3), which means ordered-categorical methods, not regression on a numeric shindo.

**Shaking footprint breadth.** The number of prefectures that reported shaking, and the distribution of their per-prefecture maxima, is a crude but real proxy for how far the shaking propagated. It supports comparison against magnitude and depth. It is a count of reporting units, not an area and not a population.

**Spatial and depth clustering of seismicity.** Coordinates are stated to be WGS84 decimal degrees with depth in kilometres, so hypocentres are directly plottable and inter-hypocentre distances are computable. Cluster by source region, stratify by depth band.

**Feed quality monitoring.** A substantial and named class of bulletins arrives with no hypocentre, no magnitude, and no English title. Measuring the share of such records, and the share where the tsunami inference came back unknown, tells you how much of the feed is actually usable for the analyses above.

**Event rate as a point process.** Legitimate, but only as a point process — see §4 on why it is not a time series.

## 3. Combination rules

**Shaking intensity — headline and per-prefecture.** This is an **ordinal scale with tied-but-distinct steps**: consecutive levels include lower and upper subdivisions of the same numeral. Values **may be compared and ordered**, and maxima and minima are meaningful — the feed itself is built on taking maxima over stations, which presupposes a total order. Values may **not** be summed, differenced, or averaged, under any condition. The gap between adjacent levels is not a defined quantity, so a "mean intensity" or an "intensity delta" is not a number about the world. Use medians, modes, maxima, and rank methods. Do not encode the levels as 1…9 and then do arithmetic on the encoding.

**Magnitude.** Values are on one named agency scale and **may be compared** across records — subject to the maturity condition below. They may **not be summed**, and the files do not establish that the numeric spacing is uniform, so **differences and averages are not licensed either**. The scale is described as the output of a formula that is not given here; without knowing that formula's structure you cannot claim that a step from 4.0 to 5.0 is the same quantity of anything as a step from 6.0 to 7.0. Treat magnitude as an ordered scale value, not an interval quantity. The material also hedges that the scale resembles the familiar one *for shallow events*, which means any cross-scale intuition you carry should not be applied uniformly across depths.

**Latitude, longitude, depth.** These three are **components of one joint solution** and must move together. You may not take the horizontal position from one bulletin and the depth from another, nor from a different revision of the same event — they are outputs of a single inversion and mixing them yields a point that no solution ever asserted. Across records, coordinates share a stated datum, so **distances and differences between hypocentres are meaningful**. Averaging coordinates across revisions of *one* event is not an improvement of the estimate; the later revision supersedes the earlier one, and the mean of a superseded and a current solution is neither. Averaging coordinates across *different* events yields a centroid, which is a legitimate summary of a cluster but is not a place where anything happened.

**Depth specifically.** Depth is derived by taking an absolute value, so it carries no sign and cannot express elevation above datum. It is bounded and non-negative by construction.

**The maturity condition, which governs magnitude and hypocentre alike.** The product code is described as *the scale on which the maturity of the solution is expressed* — it qualifies the results rather than being a result. Two solutions carried under different product codes are therefore **not on the same footing**, and pooling them without stratifying mixes preliminary and refined estimates into one distribution. Always stratify by product code, or restrict to a single code, before summarising magnitudes or hypocentre scatter. Note carefully: the files establish *that* maturity is expressed there but **do not establish the ordering** — you can group by it, you cannot rank by it. Ordering of revisions comes from the serial number, which is explicitly a revision sequence.

**Timestamps.** All three are instants on a single common absolute axis, so **any two of them may be differenced**, and those differences are durations in the ordinary sense. But they are **not interchangeable**, and substituting one for another silently changes what your analysis is about. Averaging timestamps across records is not meaningful; averaging *differences* between them is.

**Serial number.** Ordinal within one event identifier only. Comparing serial numbers across different events is meaningless — a serial 3 of one earthquake and a serial 3 of another share nothing.

**Region and prefecture codes.** These are **two different code spaces**. The source-region code names the seismic source area; the prefecture codes name administrative units that observed shaking. They come from different source fields and must not be joined to each other, matched against each other, or pooled into one dimension — in the sample record the source region is an offshore area whose code appears in neither of the prefecture code values. Both are opaque without an external lookup table; counting distinct codes is fine, interpreting them is not.

**The tsunami flag.** Three-valued, and the third value means *unknown*, not *no*. Collapsing unknown into false will systematically understate. Because the value is an inference over free text rather than a published coded field, it may be **counted and cross-tabulated with the appropriate caveat, but must never be treated as authoritative** and must never drive an operational or safety decision. The feed also excludes the dedicated tsunami products entirely, so it is structurally incapable of being a tsunami source.

**Counting.** Do not count records to count earthquakes. Deduplicate to one record per event identifier — normally the highest serial — before any per-earthquake statistic. Every record-level count is a count of bulletins.

**Missingness.** Absence is encoded two different ways in this feed: some quantities are set to a null value when unavailable, others are simply left out of the record. A consumer that only tests for null will silently mis-handle the omitted ones, and one that only tests for presence will treat null as a value. Test for both.

## 4. Time

**The time axis of the thing described is the origin time** — the instant at which rupture began. That is the phenomenon time, and it is the correct axis against which the hypocentre, magnitude, and intensity results should be read, because those results are all statements about the event that started then.

The other two instants belong to the **observing and publishing system**, not to the phenomenon: one records when the solution became available, the other when the finished bulletin was handed into the distribution channel. Plotting seismicity against either of these gives you the behaviour of the agency's pipeline, not the behaviour of the earth.

**Positions on the axis are instants, not intervals.** The origin time marks the *beginning* of rupture; no duration or extent is carried, so an earthquake in this feed has a start and no modelled end.

**There is no period and no sampling rate.** The material states plainly that earthquakes are not scheduled and that successive origin times carry no period. Consequences: this is a point process, not a time series. Do not resample it onto a regular grid, do not interpolate between events, do not treat a quiet stretch as missing data, and do not compute a "rate" by averaging inter-arrival times without a point-process treatment. Gaps are the signal.

**Relation to civil time.** All three timestamps are recorded on an absolute, offset-free basis, having been converted from Japanese local time at ingest. This makes them directly comparable and differenceable without any timezone reasoning — which is exactly what you want for latency work.

It also means that **any analysis involving time of day is not directly supported.** Diurnal patterns, working-hours effects, day-versus-night response — all of these are questions about Japanese civil time, and the files establish that the source was a local clock but **do not state the numeric offset from it**. To go back to civil time you must supply that offset from outside these files. I am not deriving it here; treating it as a fixed nine-hour shift is an assumption I am flagging as coming from outside the material, and it additionally assumes the offset is constant, which is also not established.

**Ordering between the three instants is expected but not guaranteed.** The stated meanings imply origin precedes availability precedes distribution, and the sample record is consistent with that, but no constraint in the material enforces it. Check it rather than assume it, and treat violations as data-quality events.

**Do not parse the event identifier as a timestamp.** See §5.

## 5. Ambiguities

**Which clock the event identifier is on — declining to decide.** The identifier is described as the origin time in compact form, while the origin timestamp is described as a conversion to an offset-free absolute time. If the identifier is on the local clock these two should disagree by the local offset; in the sample record they agree exactly, digit for digit. One of the two readings must be wrong and the material does not say which. **Practical instruction: do not parse the identifier as a time. Use the origin timestamp.**

**The trailing sequence number in the detail link does not match the serial** in the sample record — the link ends in 1 where the serial is 2. Whether the link embeds a different counter, a different product's serial, or is simply inconsistent here, the files do not say. **Declining to decide.** Do not use the link to recover the revision number.

**Whether the report identifier is globally unique.** It is formed from the event identifier and the serial, and is described as distinguishing bulletins for one event. Nothing establishes that two *different product codes* for the same event cannot both carry the same serial, which would collide. **Declining to decide** — verify uniqueness empirically before using it as a primary key, and be prepared to key on event, serial, and product code together.

**Whether the headline shaking value always equals the maximum of the per-prefecture values.** They are drawn from different source fields, described independently. The sample record is consistent, but consistency is not asserted. **Declining to decide.** Do not derive one from the other; carry both and treat a disagreement as informative.

**What a cancellation implies for the data it carries and for prior bulletins.** The standing field is described only as the bulletin's position in the revision sequence. Whether a cancelling bulletin still carries a hypocentre, and whether it retracts the preceding solution or supersedes it with nothing, is not stated. **Declining to decide** — but exclude cancelled events from seismicity statistics until you know, since including a retracted event is the more damaging error.

**The ordering of the product codes by maturity.** Established that they express maturity; not established which is more mature than which. One code in the permitted set has a different prefix from the rest, and its relation to the others is unexplained. **Declining to decide.** Stratify, do not rank.

**The meaning of every code value** — source region and prefecture alike. These are opaque identifiers with no accompanying table. **Declining to decide.** Do not assume they correspond to any standard national or international code list; obtain the authoritative table or leave them as opaque keys.

**Uncertainty on every computed quantity.** No error ellipse for the hypocentre, no depth uncertainty, no magnitude uncertainty, no indication of whether depth was free or fixed in the inversion. **Not determined.** This is the most consequential gap: you can measure how much a solution *moved* between revisions, but you cannot say whether any two solutions *differ significantly*, and you cannot put a confidence region on any epicentre.

**Whether serial numbers are monotonic and gapless.** Described as a revision sequence with a lower bound of zero. **Guess, marked as a guess:** they increase within an event and may skip values. Do not rely on "serial equals count of prior bulletins", and select the latest revision by maximum serial rather than by an assumed final value.

**Whether the prefecture list can be empty.** It is a required member. **Guess, marked as a guess:** an empty list is emitted for bulletins with no observed shaking, which is the same class of bulletin that omits the hypocentre. Code defensively for the empty case regardless.

**Feed completeness.** Tsunami products are stated to be excluded, so the feed is not a complete record of the agency's output. Whether it is a complete record of *earthquake* bulletins, whether there is a magnitude or intensity threshold below which nothing is published, and what the retention window is, are all **not determined**. Without a completeness threshold you cannot compute a magnitude–frequency distribution or claim any catalogue is complete above a given magnitude.

**Whether the shaking scale's lowest published level is a floor or a threshold.** The permitted levels begin at 1, with no level for imperceptible shaking. Whether events felt below that level are reported with the member absent, or not reported at all, is **not determined** — which matters directly for any attenuation or footprint analysis, since it decides whether an absent prefecture means "no shaking" or "not observed".

**Precision and rounding of magnitude and coordinates.** Not stated. Do not infer significant figures from the sample.
