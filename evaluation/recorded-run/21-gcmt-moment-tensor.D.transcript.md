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
