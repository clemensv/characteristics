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
