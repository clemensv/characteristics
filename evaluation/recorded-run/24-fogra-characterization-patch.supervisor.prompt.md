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

1. Channel values are in color space `https://registry.color.org/cmyk-registry/fogra51`, carried by the members ["cyan", "magenta", "yellow", "black"] in that order. Values must not be treated as linear-light or as sRGB unless that is what is declared.
   wrong reading: Assuming sRGB, assuming values are linear in radiometric quantity, or compositing premultiplied and straight alpha alike.

2. Channel values are in color space `https://cie.co.at/publications/colorimetry-part-4-cie-1976-lab-colour-space-1`, carried by the members ["l_star", "a_star", "b_star"] in that order, where `illuminant` is `D50`; `observer` is `cie-1931-2`. Values must not be treated as linear-light or as sRGB unless that is what is declared.
   wrong reading: Assuming sRGB, assuming values are linear in radiometric quantity, or compositing premultiplied and straight alpha alike.


TRANSCRIPT A

# 1. What this feed is

Each record is one **colour patch from a printing characterization target**: a
four-component ink recipe expressed as percentage coverage of cyan, magenta,
yellow and black, paired with the three-coordinate colour measurement that
resulted from printing that recipe, plus a free-text description of the
conditions under which the measurement was taken.

The record therefore has two halves with very different natures, and the whole
of the analytical risk in this feed comes from confusing them:

- The four ink percentages are the **independent variable** — the input asked
  for. They are a specification of the patch.
- `l_star` / `a_star` / `b_star` are the **dependent variable** — an
  observation, the result of a physical measurement of the printed patch.

Nothing in the two files states this split explicitly; I infer it from the
schema name (`FograCharacterizationPatch` — "characterization" and "patch") and
from the fact that only the three colour coordinates have an associated
`instrumentation` description of how they were obtained. Treat that split as an
inference, but a load-bearing one.

The example record — cyan 100 %, everything else 0 % — is a **solid primary**:
the single-ink extreme of the cyan channel. Its measured coordinates
(L\* 56.12, a\* −34.9, b\* −52.52) are a dark, strongly green-and-blue-leaning
colour, which is consistent with the patch being cyan-only, but the files do not
label it as such; that reading is mine.

I read `l_star`, `a_star`, `b_star` as **CIE L\*a\*b\*** coordinates. That is an
inference from the member names and from the measurement condition text
(illuminant, standard observer, measurement geometry, backing). **The schema
itself nowhere declares a colour space, an illuminant, an observer, or a white
point for these three members, and gives them no unit annotation at all** — see
§5. That absence is the single most consequential fact in this feed.

The feed as a whole is a *lookup* — a sampled mapping from a 4-dimensional ink
space onto a 3-dimensional colour space, for one printing process under one set
of measurement conditions.

# 2. Analytics worth running

**Fit a forward device model (CMYK → colour).** This is the primary purpose the
data structure supports and the reason the feed exists. Every record pairs a
complete ink coordinate with a complete colour coordinate, so the set of records
is a sampled function that can be interpolated, fitted, or turned into a lookup
table. Supported because both sides of the mapping are present and complete in
every record (all seven are required).

**Invert it (colour → CMYK) for separation.** The same sample set run backwards
gives ink recipes for target colours. This is supported by the same pairing, but
only over the region of colour space actually covered by the samples — and one
record does not tell you what that coverage is (§5).

**Gamut characterization.** The cloud of measured coordinates across all records
bounds what this process can reproduce: convex hull, hull volume, extremes per
axis, and the lightness range between the paper (all four inks at 0 %) and the
darkest overprint. Supported because the colour coordinates share a single
coordinate system, so geometric operations on the point cloud are well defined —
*provided* every record in the set was measured under the same conditions (§3).

**Primary and overprint audit.** Records where exactly one ink is at 100 % and
the rest at 0 % give the solid primaries; records with two or three at 100 %
give the secondary/tertiary overprints; all-zero gives the substrate. These are
the standard reference points for judging whether an ink set and substrate match
an intended reference. Supported because the ink coordinates are explicit
numbers rather than patch labels, so these special cases are selectable by
filtering rather than by convention.

**Tone response curves.** Select records where three inks are at 0 % and one
varies; the resulting relation between coverage and measured lightness describes
how that channel behaves from paper to solid. Supported because coverage is a
continuous quantity in the record rather than a step index.

**Grey balance and neutrality.** For black-only records, the departure of `a_star`
and `b_star` from zero measures the colour cast of the black ink and substrate;
for three-colour combinations, the same test measures how far a nominally
neutral recipe actually lands from neutral. Supported because the two chromatic
coordinates are signed and share an origin.

**Dataset-to-dataset comparison.** If the same patch identifiers appear under two
different `instrumentation` descriptions, per-patch colour differences quantify
the effect of the measurement condition (or of a re-print, or of ageing). This is
the most valuable analysis available *and the least safe*: it depends on
`sample_id` being a stable patch key across the two sets, which the files do not
establish (§5).

**What this feed cannot support:** anything about time, drift, repeatability
across sessions, print run stability, or process control over a shift. There is
no time axis (§4). Also nothing about spectral behaviour, metamerism, or
re-computation under a different illuminant — the record carries reduced
tristimulus-style coordinates, not spectra, so the measurement cannot be
recomputed for other viewing conditions. That is a permanent loss, not a gap you
can fill downstream.

# 3. Combination rules

**`sample_id`.** A label, not a quantity, despite being an integer. Never sum,
difference, or average it. Comparison is limited to equality. Two further
cautions: the schema declares no uniqueness or key constraint, so identifier
collisions within a set are not excluded; and nothing establishes that the
integer ordering is meaningful, so do not sort by it and read the order as a
sequence of anything (not of position on a target, not of ink level, not of
time). Use it for joining, and only where the join is otherwise justified.

**`cyan`, `magenta`, `yellow`, `black`.** All four carry the same unit
annotation, so they are mutually unit-compatible.

- *Comparable and differenceable* within a channel across records: "this patch
  has 20 percentage points more cyan than that one" is well formed.
- *Comparable across channels* only in the weak sense that both are percentages;
  20 % cyan and 20 % magenta are the same coverage fraction but of different
  colourants, so equality of the numbers is not equality of anything perceptual.
- *Summable across the four channels within one record*: the sum is
  unit-consistent and yields the total coverage the patch demands. I read that
  as the total ink laid down for the patch, which is a standard printing
  quantity; the files do not name it, so treat that reading as an assumption.
- *Averageable* across records only as a description of how the sample set is
  distributed — the mean coverage of a target says something about the target,
  not about any colour.
- **Do not sum the same channel across records.** Adding the cyan of patch 12 and
  the cyan of patch 73 produces a number with no referent; each percentage is
  relative to its own patch area, and there is no area, count, or weight in the
  record to make the sum extensive.
- The schema places no bounds on these values, so 0–100 is *not* enforced.
  Negative coverage and coverage above 100 % are schema-valid. Range-check on
  ingest rather than trusting the type.

**`l_star`, `a_star`, `b_star`.** These are **coordinates in a space, not
amounts of anything**. This is where analysts go wrong.

- *Comparable and differenceable* per axis between two records — ΔL\*, Δa\*, Δb\*
  — **but only if both records were measured under the same conditions.** See the
  condition rule below; it is not optional.
- The three per-axis differences form a displacement vector, and its Euclidean
  length is the conventional single-number colour difference between two
  patches. That interpretation depends on my inference that this is CIE L\*a\*b\*
  (§1); the schema does not say so. If that inference is wrong, the Euclidean
  norm is not justified.
- **Never sum them.** Not across axes within a record (the three axes are not
  commensurable — one is a lightness axis and two are chromatic, and the schema
  gives none of them a unit), and not across records. Adding the L\* of two
  patches does not model printing them together, overlaying them, or viewing them
  side by side. There is nothing additive here.
- **Averaging is defined arithmetically but is not the operation people think it
  is.** An unweighted mean of `l_star`, `a_star`, `b_star` over a set of records
  gives the centroid of a point cloud. It is *not* the colour of a mixture of
  those patches, *not* the colour of a patch printed with the average ink
  recipe, and *not* the colour you would get by averaging the underlying
  measurements before they were reduced to these coordinates — because the
  reduction is not linear. (That last point rests on the CIELAB inference.)
  There is no mass, area, or count member in the record to weight such an
  average by, so even a weighted mean has nothing to key on. Report a centroid
  only when you mean "the middle of this cloud of samples", and say so.
- **Do not compare a colour coordinate to an ink percentage.** They are
  different kinds of thing, and only one of them carries a declared unit.

**The condition that governs every comparison of colour coordinates.**
`instrumentation` records the circumstances of the measurement — illuminant,
observer, geometry, filtering, backing, and the standard the measurement follows.
The record carries that description precisely because the coordinates are
*conditional on it*: a value obtained under one set of conditions is not the same
observable as a value obtained under another. Therefore:

- Colour coordinates may be compared, differenced, or pooled **only across
  records whose measurement conditions agree.**
- Where they differ, the values must not be combined, and the difference between
  them must not be attributed to the print. The difference confounds print
  variation with measurement-condition variation, and this record gives you no
  way to separate the two.
- `instrumentation` is **optional**. A record may arrive with no stated
  conditions at all. Such a record's colour coordinates cannot be safely pooled
  with anything — not even with another condition-less record, since silence is
  not evidence of agreement. Do not default a missing condition to the most
  common one in the set.
- `instrumentation` is **free text with no enumeration or pattern**. Equality
  testing on the raw string is fragile: spelling, word order, spacing, and
  abbreviation may all vary between records that mean the same thing, and two
  records with byte-identical strings may still have been produced casually.
  Normalize before grouping, and treat the grouping as provisional.
- **`additionalProperties` is false**, so there is no member for a substrate, a
  print run, a press, a dataset identifier, or a batch. Records from two
  different print runs measured the same way are **indistinguishable** in this
  format. Pooling across runs is therefore possible and undetectable. If your
  ingest path can receive more than one run, carry the provenance outside the
  record; you cannot recover it from inside.

# 4. Time

**No member establishes a time axis, and no position in these records can be
related to civil time.** I am not declining this question — the files decide it,
and they decide it in the negative:

- There is no timestamp, date, sequence number, or duration member, and
  `additionalProperties: false` forbids one being added by a producer.
- `sample_id` is an integer, but nothing declares it monotone, sequential, or
  ordered in acquisition; reading it as a measurement order is unfounded.
- **The "2009" in the instrumentation text is a trap.** It is the edition year of
  the standard the measurement follows. It is not when the patch was printed, not
  when it was measured, and not when the record was written. Do not parse a date
  out of that string; a record written today and a record written a decade ago
  would both carry it.

The practical consequences are worth stating plainly, because they are what
someone would get wrong: this feed cannot support drift analysis, repeatability
over time, press stability monitoring, before/after comparison of a calibration,
or any ordering of records in acquisition sequence. If two records disagree, the
data cannot tell you which is later. If you need any of that, the time must be
attached outside the record at ingest, and once records are pooled without it,
it is unrecoverable.

# 5. Ambiguities

**The colour space, illuminant, and white point of the three coordinates are not
declared in the schema.** Only the four ink percentages carry a machine-readable
unit; the three colour members are bare numbers with no annotation, no space, no
reference white, and no range. A units-aware consumer will treat them as
dimensionless scalars and will happily perform arithmetic on them that is
meaningless. The only place the colorimetric context exists is a free-text,
*optional* string that no tool can interpret. **I am guessing** that these are
CIE L\*a\*b\* under the illuminant and observer named in that string; the
guess is well supported by the member names and the condition text but is not
established by the schema, and every distance and difference computation in §3
inherits it.

**Whether `sample_id` is unique, and what it is unique within.** No key,
identity, or uniqueness declaration exists. **My guess** is that the true natural
key is the pair (`sample_id`, measurement condition) rather than `sample_id`
alone, since the same physical patch would plausibly be measured more than once;
but the files do not settle it. Do not deduplicate on `sample_id` alone and do
not assume a join on it is one-to-one.

**Whether the ink percentages are the requested values or measured values.**
I read them as requested (nominal) coverage — the recipe — because that is what
makes the record a characterization sample. **This is an assumption.** If they
were instead measured coverages, the whole record becomes two measurements and
the modelling task changes shape. Nothing in the files distinguishes the two.

**The reference of the percentage.** Percent is a ratio and the files do not say
of what — area coverage, tint value, screen dot percentage, or a transfer-curve
value. **I am declining to decide this.** It does not affect the combination
rules in §3, but it does affect whether the four values can be interpreted
physically or only as device control values.

**The sampling grid and coverage of the set.** One record tells you nothing about
which combinations are present, at what step size, how many records constitute a
complete set, or whether the set is a regular grid. Interpolation quality,
gamut-hull validity, and inversion all depend on this. **Declining** — it is a
property of the collection, not of the record, and cannot be inferred from a
single instance.

**Whether repeats exist.** Nothing declares whether a patch appears once or many
times. Without repeats there is no measurement-uncertainty estimate available
from the data at all, and outlier detection has to rely on smoothness assumptions
about the device model rather than on replication. **Declining.**

**The substrate, ink set, press, screening, and print condition.** Absent, and
`additionalProperties: false` means they cannot be carried. Two records that
differ only in substrate are identical in this format. **Declining** — this is a
genuine gap in the format, not something to be inferred.

**Whether the measurement conditions are constant across the feed.** The
condition text is per-record and optional, which suggests it *can* vary;
whether it does in practice is not determined. **Declining**, but plan for
variation: group by normalized condition text before any pooled analysis, and
quarantine records with the field absent.

**Bounds.** Validation is declared as in use, but no minimum, maximum, or range
is applied to any numeric member. Out-of-range coverage and physically
implausible colour coordinates are schema-valid, so schema validity is not a
data-quality signal here. That is a fact, not an ambiguity — but it is one people
assume away.


TRANSCRIPT B

# FOGRA characterization patch feed — analyst's briefing

## 1. What this feed is

Each record is a **matched stimulus–response pair from a printing press**. The stimulus is the four ink amounts commanded to the press for one small rectangle of a printed test sheet; the response is the colour that was subsequently read off that printed rectangle with a measuring instrument. One record is one rectangle ("patch"). A complete set is 1617 patches making up a single test target, and the schema states this transcription comes from the FOGRA51 file in the ICC's characterization data registry.

The consequence that matters: **the two halves of the record are not the same kind of number.** The ink amounts are *inputs* — what was asked for, exact by construction, carrying no measurement error. The L\*a\*b\* values are *outputs* — what a physical sheet of paper actually did, carrying instrument error, press variation, and substrate effects. Anyone treating all seven numbers as "columns of measurements" will draw wrong conclusions, because four of them are a designed grid and three of them are observations.

The example record is the cyan solid: 100 % cyan, nothing else, reading L\* 56.12, a\* −34.9, b\* −52.52. That is a data point about *this printing condition*, not about cyan ink in general.

## 2. Analytics worth running

**Fit a forward device model (ink amounts → colour).** This is the primary purpose the data structurally supports: every record is a controlled input paired with its observed output, and 1617 of them sample the four-dimensional ink space. Nothing else in the record is needed.

**Invert that model for separation, and derive the reproducible gamut.** The measured L\*a\*b\* points, taken as a cloud in three-space, delimit what this condition can actually produce. Supported because the response side is a coordinate triple in a common colour space, so the set of achievable colours is directly the set of observed triples (plus whatever interpolation you can justify — see §3).

**Per-channel tone reproduction.** Records where exactly one ink is non-zero form a ramp for that ink; the observed L\*a\*b\* along that ramp is the channel's response curve. Supported because the ink amounts are stated per channel independently, so single-channel records are identifiable by inspection.

**Overprint and trapping behaviour.** Records with two or three non-zero inks let you compare the observed colour of an overprint against what the individual inks did alone. Supported for the same reason.

**Grey balance and black generation.** Locate CMY combinations whose a\* and b\* sit near zero, and compare the black-only ramp against composite neutrals of the same lightness. Supported because a\* and b\* have a defined neutral origin and L\* is a separable lightness coordinate.

**Total ink coverage against appearance.** The four ink amounts share one unit and one full-scale reference, so their sum per record is a well-defined device-side quantity; you can study how it relates to observed L\*. Note this is a coverage statistic, not a colour statistic (§3).

**Cross-condition comparison.** Given a second characterization set, comparing colour at identical ink amounts quantifies how two printing conditions differ. **Strictly gated** on the measurement-condition text matching exactly — see §3 and §5.

**Sampling-design audit.** You can check how the target covers the ink space and where it is sparse, which tells you where any fitted model will be least trustworthy.

What this data does **not** support: anything about time, drift, repeatability, or process stability (§4); and any uncertainty statement, because no record carries a tolerance, a repeat count, or a standard deviation.

## 3. Combination rules

### `sample_id`

A **label**, not a magnitude. It identifies a position within the target. Never sum it, average it, difference it, or use it as a regressor; the gap between patch 73 and patch 74 is not a quantity of anything. Its only legitimate uses are equality, grouping, and joining.

It is safe as a join key **only between files built on the same target**. These files establish the target size (1617) for *this* dataset; they do not establish that any other file uses the same layout. Joining on the four ink amounts is the safer key, because that is a statement about the stimulus rather than about a file's row ordering.

The files do not declare whether the index is 0-based or 1-based, nor that it is unique within a file. Do not assume either.

### Ink amounts (cyan, magenta, yellow, black)

All four are percentages of full coverage on a common scale with a real zero.

- **Within one channel:** compare, difference, sum, and average freely. These are exact commanded values, so an average is an average over the design grid, not over noise — interpret it accordingly.
- **Across the four channels of one record:** summing is arithmetically valid (shared unit, shared reference) and yields total ink coverage. But it is a *material* quantity, not a *colour* quantity: it tells you how much ink went down, and it predicts nothing about appearance. Do not let a units-aware pipeline present it as if it described the patch's colour.
- **Averaging one channel across records:** valid arithmetic, but it is a property of the target's design, not of the press. The files do not establish that the target samples the ink space uniformly, so an unweighted mean over patches is not a mean over anything anyone prints.
- **Ink amounts and colour coordinates must never be combined arithmetically with each other.** One side is unit-bearing (%) and commanded; the other is an unlabelled coordinate on a colour scale. Their relationship is the object of study, not an operand.

### `l_star`

Lightness on a scale running from zero at black to one hundred at the diffuse white established by the illuminant and geometry.

- **Differences are the meaningful operation.** The scale is described as perceptually near-uniform, so equal L\* differences are approximately equal perceptual steps — approximately, and only approximately.
- **Ratios are not supported.** "Twice as light" is not a statement this scale licenses, notwithstanding the defined zero, because uniformity is stated as near, not exact.
- **Averaging** is arithmetically fine and is the right move when you want the mean lightness of a defined set of patches. It is the wrong move if you intend the result to be "the colour of the average" — see the joint rule below.

### `a_star` and `b_star`

Signed bipolar coordinates. Positive a\* toward red, negative toward green; positive b\* toward yellow, negative toward blue.

- **Differences are meaningful. Sums are not.** Adding two a\* values produces nothing.
- **The zero is a convention fixed by the illuminant, not by the sheet.** This is the single most consequential fact in the record. Sign is meaningful only relative to that illuminant-defined neutral; it does not mean "the paper is neutral there". A substrate whose unprinted patch reads a\* ≠ 0 is not an error, and a\* = 0 does not mean "no colourant". Ratio statements are meaningless because the origin is a chosen reference rather than an absence of the quantity.

### The colour triple taken jointly

`l_star`, `a_star`, `b_star` are **three coordinates of one reading**, not three independent measurements. Never sum or average them across each other; a mean of {56.12, −34.9, −52.52} is a nonsense number.

The natural joint operation is a distance in the three-space, used as a colour-difference measure — and the "perceptually near-uniform" characterization is what makes a Euclidean distance approximately interpretable. **Assumption flagged:** the files supply no difference formula, no weighting, and no tolerance thresholds. Any specific ΔE formulation and any pass/fail limit must come from outside these files.

**Coordinate-wise averaging of colour across records is not a colour operation.** The mean of two patches' L\*a\*b\* is not the colour of their mixture, of their overprint, or of their average spectrum. It is a centroid of a point cloud and should only be reported as such.

**Interpolation between records is not licensed here.** Nothing in these files establishes that observed colour is a linear function of ink amount, so you may not average the readings at 0 % and 100 % cyan and call the result the reading at 50 %. Fitting an interpolating model is a legitimate analysis (§2); asserting linearity as a combination rule is not.

### Across measurement conditions — the hard gate

**No colour value may be compared, differenced, or pooled with a colour value taken under different measurement conditions.** The instrumentation text is the identity of the condition under which every reading in the file was taken: illuminant, observer, geometry, filter state, backing, and the standard and mode invoked. Change any of those and the numbers are no longer on the same footing, even though they look like the same three columns.

Operationally: **exact string equality is the only condition-match test these files support.** If two feeds carry byte-identical instrumentation text, pooling is defensible. If the strings differ, these files give you no basis whatever to decide whether the two conditions are equivalent — decline, or resolve it from a source outside this data.

The instrumentation value is a **file-level constant repeated onto every record**. It therefore carries zero per-record information: do not group by it within a file, do not count distinct values as if they varied, and do not treat its presence as evidence of per-patch provenance. Its job is to survive the record leaving its file.

## 4. Time

**No member establishes a time axis, and no position in this data relates to civil time.**

There is no timestamp, no measurement date, no sequence time, and no room for one — the record is closed to additional members. The one member with an ordering, `sample_id`, indexes *position on a physical target*, which is spatial, not temporal; these files do not establish that patches were measured in index order, so it cannot be pressed into service as a proxy clock.

The only date-like tokens anywhere are edition identifiers embedded in prose — the standard year named in the instrumentation text, and the dataset name itself. Those identify *which document* and *which published dataset*, not *when a sheet was printed or read*. Do not parse them as observation times.

Consequences you must accept:

- No trending, no drift detection, no before/after, no time-series methods of any kind.
- Records cannot be ordered in time, and two records cannot be said to be contemporaneous.
- Any "as-of" reasoning — when this characterization was produced, whether it is still current, whether a later re-measurement exists — must come from external provenance carried alongside the feed. Nothing in the record supports it.
- If you ever pool this with a re-measurement of the same target, you will have no field that distinguishes the two. Retain the file-level provenance separately before the records are flattened.

## 5. Ambiguities

**Two annotations the schema's own prose promises are absent from it.** The black-channel text says the channel ordering "has to be stated by the annotation"; the instrumentation text says the illuminant and observer "are also declared on the colorimetric space so that a processor need not parse the sentence." Neither declaration appears in what I was given. So: a machine cannot obtain the illuminant or observer without parsing English prose, and there is no file-supplied authority for a canonical channel order. *I am declining to supply either.* If you must serialize the inks as a positional tuple, the column names quoted in the descriptions suggest cyan-magenta-yellow-black order — **that is a guess from naming, not something the files decide.**

**Whether a record without the instrumentation text is usable.** That member is optional. The files do not say whether its absence means "unknown condition" or "inherit from the file". *Declining.* Treat an absent value as unknown and refuse to pool such a record with anything.

**No dataset identifier lives on the record.** The dataset's identity sits in the schema's description, not in the data, and the record admits no additional members. Two different characterization datasets sharing an identical instrumentation string would be **indistinguishable record by record** after they leave their files. This is a live pooling hazard, not a theoretical one. *Declining to propose a workaround from these files;* it must be solved by keeping records with their schema/provenance.

**What printing condition FOGRA51 denotes.** Press, substrate, screening, tone-value characteristics — none of it is established here. The name is a label whose meaning lives in the registry these files point at but do not contain. *Declining.*

**What the mode named at the end of the instrumentation text entails.** The string names a standard and a mode. These files do not define the mode. I am treating it as an opaque identity token that must match before any cross-file comparison, and *declining to interpret it further.*

**Value ranges.** L\*'s 0–100 span and the polarity of a\* and b\* are stated in prose but nothing constrains the numbers; a\* and b\* have no stated bounds at all, and the ink amounts have no stated maximum. Whether a value above 100 % or below 0 % is possible, erroneous, or meaningful is *not determined.* Do not silently clamp.

**Index base and uniqueness.** Whether `sample_id` starts at 0 or 1, and whether it is unique within a file, are *not determined.* Uniqueness is strongly implied by the words "index of the patch within the target" — **treat that as an assumption and verify it in the data before joining on it.**

**Which record is the substrate.** Analysis of this kind usually needs the unprinted paper. There is presumably a record with all four inks at zero, but these files do not establish that such a patch is present in the target. *Declining;* look for it, do not assume it.

**Measurement uncertainty is entirely absent.** No tolerance, no repeat count, no dispersion, no indication whether a reading is a single measurement or an average of several. Every colour difference you compute will therefore have unknown uncertainty. *Declining to estimate one.* Do not report differences with implied precision the data cannot support.

**Precision of the readings.** The example shows two decimals, but nothing in the files fixes a precision or a rounding rule. *Not determined.*


TRANSCRIPT C

# 1. What this feed is

Each record is one calibration point of a printing press: a specific combination of four ink amounts that was **commanded** to the press, paired with the colour that was **measured** off the sheet where that combination landed. The records are transcribed from a published characterization file (FOGRA51) held in the ICC's characterization data registry, and the whole set of them — 1617 patches — constitutes a description of what colours that particular printing condition can produce and how ink requests map onto them.

The single most important thing to understand before touching this data: the record contains two different kinds of number that the schema does not structurally distinguish. The four ink values are an *instruction*, not an observation. The three colour coordinates are an *observation* of the result. Both are tagged with the same role in the schema, so nothing but the prose descriptions tells you which is stimulus and which is response. Any pipeline that treats all seven values as measurements of the same thing is wrong from the first line.

The second thing: the colour readings are only meaningful relative to a stated set of measurement conditions, and those conditions are attached to the record as a free-text sentence with no internal structure. They are not decoration. They are the precondition for the readings meaning anything at all.

# 2. Analytics

**Forward device characterization — modelling ink request → resulting colour.** This is what the data is built for. Every record is an exact input/output pair under one fixed measurement condition, and the target sweeps 1617 combinations, so the relation can be fitted, interpolated, or tabulated across the ink space. The files support this because the ink values are stated as exact commanded amounts (not recovered estimates) and every colour reading in the file shares one declared colorimetric space and one measurement condition.

**Gamut extent.** The set of measured colour coordinates across all patches bounds what this printing condition can reach. Supported because all readings share illuminant, observer, and measurement conditions, so they are points in one common space and their extent is a coherent object.

**Colour difference between patches.** The schema states the colour scale is perceptually near-uniform, which is exactly the property that licenses treating distance between two patches as a difference magnitude. Supported for any pair of patches sharing the measurement condition. Note the limit: the files license *a* distance interpretation on this scale; they do not name or specify any particular difference formula, so anything beyond a plain distance in the three coordinates is your choice, not theirs.

**Per-channel tone response.** Records in which three of the four inks are zero isolate one ink's behaviour across coverage. The example record is such a case — full cyan alone. Supported because the ink amounts are exact and independently specified per channel.

**Neutrality analysis.** The schema states that the zero of the two chromatic coordinates is fixed by the illuminant, not by the sheet. That makes "how close is this patch to neutral" a well-posed question with a fixed reference, so grey-axis behaviour across the black-ink patches is analysable. This would *not* be well-posed if the zero were sheet-relative, and the schema is explicit that it is not.

**Total commanded coverage.** The four ink values share a unit and a basis (percentage of full coverage), so their sum within a record is arithmetically well-defined and its distribution across the target is computable. Whether that sum is a meaningful or constrained quantity in printing is not established by these files.

**Conformance comparison against another dataset.** Possible in principle, but only under the gate described in §3 — and see §5, because the gate cannot be evaluated mechanically.

**Analyses this data does not support.** Nothing temporal: there is no time member, so no drift, trend, repeatability, or run-to-run comparison is available (see §4). Nothing about measurement uncertainty: no uncertainty, replicate count, or tolerance is carried. Nothing spectral: only three colorimetric coordinates are present per patch, and the files carry no member that would let the readings be restated under a different illuminant or observer than the one declared. Whether such restatement is possible at all from these members is outside what the files decide; what is decided is that the inputs for it are not here.

# 3. Combination rules

**Patch index.** An identifier of position within the target, not a magnitude. Never difference, sum, or average it. The only valid operation is equality — matching the same patch across datasets, if you have another dataset built on the same target. Whether the index is unique, dense, or one-based is not established. Whether adjacent indices are adjacent on the physical sheet is also not established; do not read spatial locality into the ordering.

**The four ink amounts.** All four carry the same unit and the same basis, so within a single record they may be summed. Across records they may be compared and differenced, but only between records whose CMYK space resolves to the same registry entry — these are device coordinates for one specific printing condition, and an ink percentage from a different printing condition is a different quantity wearing the same name. Do not compare or difference them across printing conditions.

Averaging ink values across records is arithmetically defined but analytically misleading, and this is worth stating plainly: the population of patches is a *target design*, chosen to sample the ink space. A mean ink amount across records therefore describes how the target was laid out, not anything about the press, the ink, or the paper. It is a property of the questionnaire, not of the answers.

**Lightness.** Differences between patches are the licensed combination, because the schema states the scale is perceptually near-uniform — that is precisely a claim that equal differences mean equal amounts. Comparison and differencing are valid only between readings taken under identical illuminant, observer, and measurement conditions. Ratios are not licensed by anything in the files: the scale's upper end is fixed by the illuminant and the measurement geometry, which is a convention, and nothing here establishes that the scale is proportional to any underlying physical quantity. Treat it as an interval scale and do not compute ratios or percentage changes on it.

**The two chromatic coordinates.** The schema is explicit that their zero is set by the illuminant and not by anything in the sheet. That makes them interval quantities with a conventional origin. Consequences, each of which is a common error:

- Differences are valid; ratios are not. A patch with twice the chromatic coordinate value of another is not "twice as red."
- A value of zero does not mean the ink has no red–green or yellow–blue character. It means the patch sits on the neutral axis *as defined by D50*. Under a different illuminant the same sheet would not sit at zero.
- Summing these coordinates across records is meaningless. There is no aggregate they add up to.
- Sign carries direction and must not be discarded before averaging; averaging magnitudes and averaging signed values give different and non-interchangeable results.

**The three colour coordinates together.** They are the three components of one point, not three independent measurements. Never sum or average them with each other. The combination the files license across the triple is distance between two patches.

Componentwise averaging of the triple across records yields a centroid in the perceptual space. That is a defensible object, but it is the centroid of a *set of patches*, not the colour of any mixture of inks and not a summary of the press — and, as with the ink values, the set was chosen by the target designer, so the centroid describes the target's sampling plan.

**Ink amounts and colour coordinates must never be combined arithmetically with one another.** They differ in kind (instruction versus observation) and in unit (one carries a percentage unit, the other carries no unit at all — which also means the colour coordinates must not be fed through any unit conversion or auto-scaling machinery).

**Channel ordering.** When assembling the four ink values into a tuple for any downstream model, take the order from the declared channel list — cyan, magenta, yellow, black. Do not derive it from the member names. The schema warns about this explicitly, and the warning is real: the fourth channel is named for the printing term rather than for the letter it is conventionally abbreviated with, so alphabetical or naive ordering produces a silently wrong tuple that will still typecheck and still run.

**The gate on all cross-record colour combination.** The measurement-condition text is stated to apply to every patch in this file, so within one file all colour readings are mutually comparable and differenceable. Across files, they are comparable only if both the colorimetric space declaration *and* the measurement-condition text agree. Illuminant and observer are machine-comparable. The geometry, the filter state, the backing, and the measurement standard are only present as prose, so this gate cannot be evaluated by a program. See §5.

**Records lacking the measurement-condition text.** That member is not required. A record without it retains illuminant and observer from the space declaration, but geometry, filter, backing, and standard are then unknown. Do not pool such records with records whose conditions are known, and do not assume they share the conditions of the record next to them in the stream.

# 4. Time

**No member establishes a time axis, and I decline to assign one.** The question presupposes something these files do not provide.

Specifically:

- There is no timestamp, date, epoch, duration, or timezone anywhere in the record.
- The patch index is an index into a target's patch inventory. It is a position in a *layout*, not a position in time. Nothing states that patches were printed or measured in index order, and even if they were, no origin or spacing is given, so the index cannot be converted into a position on any time axis.
- The measurement-condition text names a standard with a year attached. That is the edition year of a document. Treating it as a measurement date, an acquisition date, or a validity window would be a serious error, and I want to name it because it is the one number in the record that looks like a date and is not one.

The consequences are worth stating, because they determine what you can and cannot build. These records cannot be time-joined to anything. They cannot be trended, aged, windowed, or ordered chronologically. Two records carrying the same patch index cannot be distinguished, ordered, or reconciled — nothing here identifies a printing occasion, a measurement session, or a run. If you are pooling data from more than one source, you have no way to detect that you have mixed occasions together.

If your platform requires an event time for ingestion, you must supply it from outside this data and you must record that you did so. Do not synthesise one from the patch index.

*Guess, marked as such:* the source file this was transcribed from very likely carries dating information in header lines that were not brought across, since only one header line was preserved. I have no evidence for this beyond the fact that one header line was explicitly carried and the schema admits no other members. Treat it as a lead for recovering provenance, not as a fact.

# 5. Ambiguities

**The measurement condition cannot be compared mechanically.** *Declining to decide.* The schema itself says the geometry, filter, backing, and standard have no keyword of their own and survive only as text. So the precondition for pooling colour readings across datasets is a free-form sentence, and two datasets that are genuinely equivalent may state it differently, while two that differ materially may differ in a way a string comparison misses. I am not going to rule on how to normalise it. What I will say is that this comparison must be treated as requiring human adjudication, and a pipeline that silently pools on illuminant and observer alone — the two things that *are* machine-readable — will pool data it should not.

**The measurement-condition designation appearing at the end of that sentence.** *Declining.* It names a defined measurement condition, but nothing in these files defines it or states what it implies about the readings. I will not guess at its meaning. What follows regardless: two datasets differing in it must not be assumed poolable.

**Value ranges.** *Not determined.* No bounds are declared on any numeric member. Whether ink amounts are confined to 0–100, whether lightness can exceed 100, and whether the chromatic coordinates have any practical envelope are all open. Do not build validation on assumed ranges.

**Whether the mapping is invertible.** *Not determined, and not decidable from one record.* Whether distinct ink combinations can produce indistinguishable measured colour is a property of the full set, not of the schema, and the files say nothing about it. If you are building a separation (colour → ink), you must establish this empirically from the full 1617 patches; do not assume a unique inverse exists.

**Whether each reading is a single measurement or an aggregate.** *Declining.* No replicate count, no uncertainty, no aggregation method is present. I could offer a plausible convention here and I am deliberately not doing so, because the answer changes how you would weight or de-noise the data and guessing it would be worse than leaving it open. Treat the readings as of unknown replication.

**Patch index semantics.** *Not determined.* Uniqueness, base (0 or 1), density over 1..1617, and any relationship to physical sheet position are all unstated. Do not assume the index is a usable spatial coordinate.

**What the identifiers point at.** *Not determined.* The observed-property reference and the schema identifier are placeholder addresses that do not resolve, so the formal definition of "printed colour" behind them is unavailable. The CMYK space reference looks like a real registry entry but its contents are not available here — which means the substrate, ink set, press, and screening that define this printing condition are named by reference only and are not present in the data. Anyone comparing this to another dataset is comparing two registry keys, not two described conditions.

**What was dropped in transcription.** *Not determined.* The record admits no members beyond those defined, and one header line was carried through explicitly. Whatever else the source file held — further headers, further columns — is absent, and nothing here says what it was.

**The role tagging does not separate stimulus from response.** *Not an ambiguity so much as a hazard, and I am flagging it as one.* All seven numeric members carry the same semantic role. The distinction between the four commanded inputs and the three measured outputs exists only in the prose descriptions. Any consumer that routes on the role annotation alone will treat the press instruction as a measurement of the sheet. This is the failure mode most likely to occur and least likely to announce itself.

**What "sent to the press" means precisely.** *Not determined.* Whether the stated ink amount is the value before or after any device-side transform is not established. This matters if you intend to reproduce the condition rather than merely model it.


TRANSCRIPT D

# 1. What this feed is

Each record is one **paired** fact: a set of ink amounts that were *sent to a
press*, and the colour that was then *read off the printed result*. It is not a
colour, and it is not a set of ink values. It is the correspondence between the
two, for one patch, under one printing condition.

The pairing is the whole content. The ink amounts are inputs chosen by whoever
built the test target; the L\*a\*b\* triple is what the press and paper actually
did with them. Neither half means anything on its own: the ink numbers are
device control values whose meaning is fixed entirely by the device, medium and
process they drive, and the specification is explicit that such a set is *not a
colour space in the colorimetric sense* — its meaning "is precisely the
measurement it is paired with." Strip the measurement away and four percentages
remain that denote nothing.

A complete file is a lattice of 1617 such pairs covering the device's input
space, which taken together is an empirical characterization of one printing
condition. A single record is one cell of that lattice.

The colorimetric half is anchored: the schema declares the space, the illuminant
(D50) and the standard colorimetric observer (CIE 1931 2°) as annotations, and
under the specification those declarations *prevail* over anything the cited
definition would otherwise establish. That anchoring is not decoration. The
1976 L\*a\*b\* definition applies to tristimulus values computed under either
the 1931 or the 1964 observer, values computed under the two differ, and nothing
in the numbers records which was used. Without the declaration these three
numbers would be uninterpretable, and a consumer who assumed a default would be
wrong roughly half the time by construction.

# 2. Analytics

**Forward device characterization.** The supported analysis is the mapping from
ink amount to measured colour. It is supported because both sides are present in
one record, the channel-to-member mapping is asserted explicitly for both spaces
rather than left to be guessed from member names, and the colorimetric side
carries a fixed illuminant and observer so that every record's measured triple
lives in one and the same space.

**Single-ink and two-ink behaviour.** Records in which three ink channels are
zero and one is not isolate the behaviour of that one ink; records with two
non-zero channels isolate an overprint. This is supported because the ink
amounts are explicit, exact, per-channel inputs rather than something inferred
from the measurement.

**Extent of the reproducible colour set.** Taking the measured triples of a
complete file as a point cloud describes what this printing condition can
produce, under D50 and the 1931 observer. Supported for the same reason as
above: all records share one declared colorimetric space.

**Neutrality.** For patches driven by black alone, the measured a\* and b\*
values can be examined against zero, because the description fixes the zero of
a\* by the illuminant rather than by anything in the sheet. That gives a
well-defined reference point; a scale whose zero were set by the paper would not.

**Comparison of two characterizations.** Two files can be compared patch by
patch *only* if they share the target, the printing condition and the
measurement conditions. The data supports the comparison arithmetically; see
§3 and §5 for why the files give you almost no machine-readable way to check
that the precondition holds.

What the feed **does not** support, and this is worth stating because each of
these is a plausible thing to attempt:

- Any time-based analysis at all — drift, stability, before/after, ordering,
  batch effects. There is no time axis (§4).
- Any per-sheet, per-run or per-instrument analysis. Nothing identifies the
  printing occasion, the sheet, the operator or the device.
- Any uncertainty-weighted or quality-filtered analysis. No quality, status or
  uncertainty is carried, and the specification states plainly that omission of
  quality "does not imply acceptable quality."
- Any conversion of the measured values to another illuminant or observer. The
  files supply no transformation, and the specification forbids performing one
  without an authoritative definition.
- Any recomputation or inversion presented as authorized by the schema. The
  annotations describe what the values *are*; the specification states that a
  processor "MUST NOT read an instruction out of them."

# 3. Combination rules

## The patch index

An identifier, not a magnitude. Equality is the only admissible operation:
differences between indices are not distances, sums and means are meaningless,
and index 74 is not "one more colour" than index 73.

Even equality is conditional. The index locates a patch *within the target*, so
two equal indices denote the same patch only once you know both records describe
the same target. The schema carries no target identifier, no dataset
identifier and no record key, so that condition cannot be established from the
data. Joining two files on the index alone is an assumption, and the
specification is explicit that feature identity must not be inferred from
identifiers, position or transport metadata.

Counting distinct indices is meaningful, and is the one way to tell whether a
file is complete against the stated 1617.

## The four ink amounts

**Compare and difference:** admissible between records that cite the same
device-value set. Every record under this schema does, so within one feed the
comparison is sound.

**Never across characterizations.** A cyan value here and a cyan value from a
different characterization are not the same quantity, even at the same numeric
value and the same unit, because the meaning of a device control value is fixed
by the device, medium and process it drives. This is the single easiest mistake
to make with this data: the unit agrees, the member name agrees, and the
quantity does not.

**Never across channels.** All four carry the same unit and are still four
different quantities. 100 % cyan minus 100 % magenta is not zero of anything; it
is a subtraction of two unlike things that the unit system will not catch.
Unit agreement is not comparability, and the four are distinguished only by
their declared position in the space's channel order — an order the
specification says is an assertion by the schema author and is *never* to be
inferred from property names or property order. The schema's own note on the
black channel exists precisely because its name would mislead an inferring
reader.

**Sum:** arithmetically admissible across the four channels of one record, since
they share a unit and one control-value set. Whether the sum denotes anything
about the process — a coverage limit, an ink load — is **not established by
these files**, and I decline to assert that it does.

**Average across records:** arithmetically possible and analytically almost
always wrong to interpret. These are amounts *sent* to the press. Their
distribution over a file is a property of how the target was designed, not an
observation of any press, any sheet or any ink. A mean ink amount over a
characterization file describes the test chart.

**Never with the measured values.** The ink amounts and the measured triple are
components of two different spaces declared as two separate elements. No
arithmetic crosses between them.

## The three measured coordinates

**They are one value, not three.** They are declared as the components of a
single point in one space. Analysing L\*, a\* and b\* as three independent
scalars discards the space that makes them mean anything, and mixing components
across axes — differencing an L\* against an a\* — is the same category error as
mixing ink channels.

**Compare and difference across records:** admissible only where the illuminant
and the observer agree. Within this feed they agree, because both are declared
once on the schema and therefore hold for every record. Against any other
source, the condition is that the other source declare D50 and the 1931 2°
observer, or that its cited definition establish them; where it declares
neither, the comparison is indeterminate and must be reported as such rather
than performed.

**There is a second condition, and you cannot check it.** Comparability also
requires the same measurement geometry, filter, backing and measurement
standard. Those are present here only inside a free-text sentence. They have no
keyword of their own, the schema says so, and the specification forbids a
processor from inferring measurement conditioning from names, text or samples.
So two records can be compared on illuminant and observer by machine, and on
everything else only by a human reading prose.

**Sum:** not defined. Nothing in the files gives a sum of lightness values, or
of a\* values, any meaning. Do not compute one.

**Average:** arithmetically possible; interpret with care. The files establish
no relation between L\* and any radiometric quantity — they say only that the
scale is perceptually near-uniform. A mean of L\* values is therefore a mean of
L\* values and nothing else. It is not the lightness of the average stimulus,
and no statement in either file licenses that reinterpretation.

**Colour difference.** The files define **no** distance metric, no ΔE formula
and no tolerance. The specification defines no analytical procedure at all, and
states that naming an operation is not specifying one. Treating the three
coordinates as a Euclidean space because the description says "perceptually
near-uniform" is an inference *I am declining to make on the files' authority*;
it may well be the right thing to do, but it comes from outside these two
documents.

**Do not treat any of the three as a percentage.** L\* running from zero to one
hundred is not a percentage, carries no unit, and is not commensurable with the
ink amounts despite the shared numeric range. a\* and b\* have no stated range
at all and are signed about a zero that the illuminant fixes.

## The instrumentation sentence

Not a quantity; it identifies the procedure. The only admissible machine
operation is exact string equality, and equality is weak evidence: the
specification says procedure identity is comparability-critical but that
equality is "evidence for candidate grouping, not proof of statistical
interchangeability." Two producers stating the same conditions in different
words will not compare equal, and nothing here normalizes them.

Critically, this member is **optional**. A record that omits it has *undeclared*
measurement conditions — not "the same conditions as the record next to it."
Omission means undeclared and never means compatible.

# 4. Time

**No member establishes a time axis, and I am not going to invent one.**

Nothing in the record carries a temporal role — not phenomenon time, not result
time, not ingestion or scheduled or actual time — and no temporal reference
system or cadence is declared anywhere. Under the specification, omission means
undeclared. The consequence is not that the time is unknown to a processor; it
is that these records are **not placed on a time axis at all**, and no position
in them relates to civil time.

The things that look like time and are not:

- `ISO 13655:2009` inside the instrumentation sentence is the edition year of a
  measurement standard. It is prose, it is a property of the method, and the
  specification forbids reading a temporal regime out of a non-Core or ambiguous
  encoding, let alone out of a sentence.
- The `v1` in the observable-property URI and the `fogra51` in the registry URI
  are *edition* identifiers. The specification is explicit that a reference
  identifies its revision and that publishers put the revision in the
  identifier. That fixes which definition is meant. It says nothing about when
  anything was printed or measured.

What this costs the consumer: records cannot be ordered, two records cannot be
told to have come from the same measurement session, no drift or stability
analysis is possible, and there is no basis for deciding that one record
supersedes another. Since the record is closed to additional properties, that
information cannot be smuggled in either — supplying it requires changing the
schema.

# 5. Ambiguities

**Whether a measured triple is one reading or a summary of several.** No
derivation and no statistic are declared, so it is undeclared whether each
L\*a\*b\* value is a single instrument reading or a mean over repeats or over
sheets. This matters: the specification states that two results carrying the
same observable property but different summary functions are not comparable as
like quantities. **Declining to decide.** A consumer must not assume either.

**Whether all records in one file share the instrumentation string.** The
description asserts the file states these conditions "for every patch it holds,"
but the schema does not enforce it: the member is optional and is pinned by no
constant or enumeration. So prose promises a file-level constant that the
schema permits to vary or vanish per record. **Declining to decide** which
governs; a consumer should verify rather than assume.

**Whether the ink amounts really are results of observing "printed colour."**
The record-level observable-property declaration reaches every result that does
not carry its own, and none of the seven values carries its own. Read strictly,
the four ink amounts are declared to be observations of printed colour, which
would put device inputs and measured outputs in one bucket for anything that
groups by observable property. **My guess** — and I mark it as a guess — is that
this is not intended, and that the declaration was meant for the colorimetric
half only. The files do not say so.

**What "printed colour" actually means.** The observable-property reference
points at a catalogue the specification itself uses as its stand-in for a
fictional one, and the schema's own identifier is under a domain reserved for
things that do not resolve. The binding will therefore always come back
indeterminate. **Declining** to substitute a meaning for it; the specification
requires that an unresolved reference be reported as indeterminate and never
repaired from names, descriptions or samples.

**Whether the declared channel orders are correct.** The schema asserts that the
registry entry declares its channels in the order cyan, magenta, yellow, black,
and that the colorimetric space declares L\*, then a\*, then b\*. Those are
assertions about external definitions. Neither is checkable without resolving
them, and the same goes for whether each space defines exactly the number of
channels supplied. **Indeterminate**, in the specification's own sense — not
wrong, just unverifiable from here.

**Whether the prose and the annotations agree.** The sentence says D50 and 2
degree; the annotation says D50 and the 1931 2° observer. They agree, which is
lucky, because if they disagreed the annotation would win under the
specification and nothing would flag the contradiction. The specification's rule
about reporting disagreement covers annotation-versus-definition, not
annotation-versus-prose. **Determined, and worth knowing:** the sentence is
documentation, not a cross-check.

**Ranges and validity.** Nothing constrains the ink amounts to 0–100 or forbids
values outside it; nothing constrains a\* or b\* at all; L\*'s stated range lives
only in prose. Whether a value of, say, 105 % would be a data error or a
legitimate encoding is **not determined**.

**What the percentage is a percentage of.** Only the cyan description says "as a
percentage of full coverage"; the other three inherit that by position in the
text rather than by any statement. **My assumption**, marked as such, is that all
four mean the same thing.

**Identity and joinability.** There is no record key, no target identifier, no
press-run identifier and no dataset identifier, and additional properties are
forbidden. Two records from two different printings of the same target are
indistinguishable. **Declining to decide** how records should be identified or
joined; the files provide no basis for it.
