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
