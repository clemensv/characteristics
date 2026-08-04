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
