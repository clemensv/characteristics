# Spacecraft attitude quaternion feed — analyst's briefing

## 1. What this feed is

Each record is one **attitude fix for one spacecraft at one instant**: the orientation of the vehicle, expressed as a unit quaternion, tagged with the instant it holds at and with the organisation that produced the message. The records are transcriptions of a CCSDS Attitude Parameter Message, so each one is a *point sample of orientation*, not a state valid over a span, and not a trajectory.

Two things this feed is **not**, and both are easy to assume wrongly:

- It carries **no position, orbit, or ephemeris**. Attitude tells you which way the vehicle is turned, not where it is. Ground tracks, look angles, target visibility, and "what is it pointing at on Earth" cannot be computed from this feed alone.
- It carries **no rates, no covariance, and no uncertainty**. Any angular rate you produce is a finite difference you computed yourself, and any error bar you quote comes from the printing precision, not from the producer.

There is also a decisive gap, discussed under Ambiguities: **the record never says which two reference frames the rotation relates.** A quaternion without a from-frame and a to-frame is a rotation with no referent. Since the schema forbids additional members, that information can never arrive in this feed; it must come out of band.

## 2. Analytics worth running

**Attitude history and manoeuvre detection.** Ordering records for one spacecraft by their epoch gives a sampled orientation history. The angular separation between consecutive samples is a well-defined scalar (see §3), so step changes, slews, and settling behaviour are detectable as excursions in that scalar. This works because the epoch is an instant on a real time axis and the four components fully determine a rotation.

**Angular rate estimation by finite difference.** Divide the angular separation between consecutive records by the epoch difference. This is the principal derived product the feed supports. Two limits apply. First, the separation is only recoverable **modulo a full turn** — if the vehicle rotated 370° between samples you will read 10°, and nothing in the record lets you detect the missing revolution. For any spinning or fast-slewing object, the sampling cadence must be known to be fast enough, and the feed does not tell you the cadence. Second, the component precision (§3) puts a floor of roughly two arcseconds on any angle you derive, so the rate floor is two arcseconds divided by your sampling interval.

**Producer latency and pipeline monitoring.** The message creation time minus the attitude epoch is a genuine production-latency measurement. In the single example it is about 4 h 55 m 42 s, i.e. this is a retrospective, after-the-fact product, not a real-time telemetry stream. Tracked over a population and grouped by originator, this distribution is a direct health metric for the producing pipeline. Nothing about the spacecraft is measured by it.

**Revision and disagreement analysis.** When two records share a spacecraft and an epoch, they are competing statements about the same physical fact. If they differ only in creation time, the later one is presumably a reprocessed solution and supersedes the earlier. If they differ in originator, they may be independent determinations, and the angular separation between them is a direct measure of inter-producer disagreement — one of the more valuable things this feed can yield, since it is the only internal handle on accuracy the feed offers at all.

**Ingest integrity checking.** Three cheap checks catch most corruption. (a) The four components must sum in squares to one; the example does so to 2.1×10⁻⁶, exactly the residue you expect from rounding to five decimals, so a deviation materially larger than that indicates truncation, a dropped component, or a reordering. (b) The scalar component should be non-negative under the producer's stated convention; a negative one is legal but flags a record that will silently poison naive comparisons. (c) Epoch monotonicity and gap detection per spacecraft gives coverage and dropout statistics.

**Fleet coverage.** Counting distinct spacecraft, and epoch coverage and gaps per spacecraft, is straightforward and requires no interpretation of the quaternion at all.

**What is not supported.** Pointing-target analysis, boresight geometry, sun/eclipse conditions, slew efficiency against a commanded profile, and any comparison against a reference attitude all require the frame definitions and a body-axis convention that this feed does not carry. Also undetermined is whether these are *determined* attitudes, *estimated* attitudes, or *planned/commanded* attitudes — that distinction changes the meaning of every one of the analyses above, and the files do not settle it.

## 3. Combination rules

### The four quaternion components — read this before doing anything else

**They may not be compared, differenced, summed, or averaged component by component. Ever.** They are not four measurements. They are one point on a unit sphere in four dimensions, carrying three degrees of freedom, subject to the constraint that their squares sum to one. Componentwise arithmetic leaves that sphere and produces something that is not a rotation. The arithmetic mean of two of these records is not an attitude. The componentwise difference of two of them is not a rotation, and its magnitude is not an angular separation. Treating the four as independent columns in a statistics package — computing per-column means, standard deviations, correlations, or regressions — is meaningless output that will look plausible.

Three specific traps:

**The sign trap.** A quaternion and its exact negation denote the *same* orientation. The schema fixes a convention (the scalar non-negative, which confines the rotation angle to at most a half turn either way) but states it as a conditional, not a requirement, and nothing in the schema enforces it. So a record with a negative scalar can legitimately appear. If it does, componentwise comparison against a sign-normalised record will show a maximal difference for two attitudes that are identical. **Canonicalise on ingest: if the scalar is negative, negate all four components.** This changes nothing physical and removes the trap permanently.

**The ordering trap.** The record stores the three vector components first and the scalar last. The schema warns that the accompanying semantic annotation names the scalar *first* — that annotation is not in this directory, so any consumer driven by it will reorder. The schema further records that an earlier issue of the standard let the producer choose scalar-first or scalar-last via a field that has since been removed, meaning historical or third-party data in the same shape may be scalar-first with no field to declare it. You cannot detect the ordering from a record's values: in the single example the scalar (0.25678) is *not* the largest component (0.87543 is), so the common "the scalar is usually biggest" heuristic gives the wrong answer on this very record. Ordering must be established out of band per source.

**The interpolation trap.** Linear interpolation between two records' components is wrong: it leaves the unit sphere and produces a non-uniform angular rate. Interpolation must be done along the sphere. Likewise, holding a value forward between epochs asserts that the attitude was constant, which the feed nowhere states.

### What you *can* safely do with the components

Two operations are legitimate and convention-independent:

- **Rotation magnitude within one record**: twice the inverse cosine of the absolute value of the scalar component. For the example this is about 150.2°. The absolute value handles the sign convention. This scalar is invariant to which coordinate basis the vector part is written in — but it still describes the angle between one *specific pair* of frames, so comparing it across records is only meaningful if those records relate the same frame pair. The feed cannot confirm that.
- **Angular separation between two records**: twice the inverse cosine of the absolute value of the four-component dot product. This is the geodesic distance on the unit sphere. It is immune to the sign convention (because of the absolute value) and immune to the multiplication convention the files never state (because a distance has no handedness). This is the one safe cross-record comparison, and it requires only that both records express the same frame pair in the same coordinates.

Anything beyond these — composing rotations, transforming vectors, deriving a rotation *direction* rather than a magnitude — requires the multiplication convention and the frame pair, neither of which the files supply. Those operations should be deferred, not guessed at.

**Precision floor.** The components are printed to five decimals, so roughly 5×10⁻⁶ absolute. That propagates to about 10⁻⁵ radians, or **about 2 arcseconds**, in any angle you derive. Pointing analyses below a few arcseconds are not supported by the data as printed. Note also that the first vector component in the example, 0.00005, sits *at* the printing resolution — its relative uncertainty is of order 100%, so no trend, ratio, or statistic built on that one component alone means anything, even though its contribution to the derived axis and angle is perfectly well bounded in absolute terms. And because of rounding, no record is exactly unit-norm; renormalise before use.

### The identifiers

**Spacecraft name.** Equality comparison only. It is free text carried from a message keyword; the files do not say it is unique, controlled, or stable, so grouping by it is an assumption. Do not use it as a join key.

**International designator.** Equality comparison only, and this is the better join key of the two. It has internal structure (launch year, launch number, trailing letter), which means lexical sort happens to order by launch epoch given fixed-width fields — but that is inferred from a single example and the meaning of the trailing letter is not established by the files. It is not a quantity; it is not summable or averageable in any sense.

**Originator.** Equality comparison only, and it carries a specific warning: the schema states the originator **need not be the operator** of the spacecraft. So do not treat it as ownership, do not partition the fleet by it, and do not infer mission affiliation from it. Its correct use is as a **provenance discriminator**: it must be retained when deduplicating, because two records for the same spacecraft and epoch from different originators are independent statements, not duplicates, and collapsing them destroys the disagreement signal described in §2.

### The two times

**Message creation time.** Comparable and differenceable across records, and orderable. Its legitimate uses are provenance and workflow: latency against the epoch, and supersession ordering among competing records for the same epoch. Averaging it is meaningful only as a pipeline statistic. It must **never** be used as the time axis of the attitude and never plotted against the quaternion as if it were when the attitude held — the schema is explicit that it is a property of the message, not of the attitude.

**Attitude epoch.** Comparable, orderable, and differenceable, subject to the caveats in §4. Averaging epochs is only meaningful as the midpoint of an interval, and only if every record in the set went through the same time-system conversion — which no record can confirm.

**Difference between the two.** Meaningful as latency provided both are on the same scale. The instance labels both as UTC, which supports that; the schema's prose is less clear (see §5).

## 4. Time

**The epoch establishes the time axis of the attitude.** It is the instant the orientation holds at. Records must be ordered, differenced, and rate-differentiated on this member and no other. The message creation time is a second, unrelated axis belonging to the production pipeline; in the example it falls about five hours *after* the epoch, and the schema states this ordering as a general property, confirming the feed is retrospective rather than live.

**Relation to civil time.** The epoch is carried as a UTC instant with a zero offset, so it *is* civil time at the zero meridian, directly comparable to a wall clock without further conversion. Rendering it as local civil time anywhere else requires a zone offset the record does not carry. Positions on this axis are therefore civil-time positions, not proper elapsed time: differences of UTC labels across a leap-second insertion under-count the true elapsed interval by the inserted seconds. The files say nothing about this, so for short intervals it is immaterial and for long ones it is your problem to handle; I am flagging it, not resolving it from these files.

**The conversion is not auditable.** The original message declared its own time system in a keyword, and that keyword is **not carried into this record**. What you receive is a value the producer already converted to UTC. You therefore cannot verify the conversion, cannot reverse it, and cannot detect a producer that got it wrong or that changed its source time system mid-stream. A silent offset of tens of seconds — the typical scale of the difference between a spacecraft time scale and UTC — would be invisible in this feed and would look like a real timing shift in any rate you derive. Since the schema forbids additional members, the source time system can never appear here; it must be established per producer out of band.

**Resolution is not uniform.** The example's epoch carries sub-millisecond resolution while its creation time carries whole seconds. Nothing guarantees resolution across records, so do not assume a fixed timestamp granularity when binning or joining.

## 5. Ambiguities

**Reference frames — declining to decide.** Neither file states the frame the rotation goes *from* nor the frame it goes *to*. This is not a detail; it means no record in this feed can be interpreted as an absolute attitude on its own. I am not guessing at a default. Because the schema forbids members beyond those defined, this cannot be repaired within the feed.

**Rotation sense — declining to decide.** Whether the quaternion rotates vectors or rotates frames, and which of the two frames is the source, is not stated. Consequently the *direction* of any relative rotation you compute is undetermined, even though its magnitude is not.

**Multiplication convention — declining to decide.** The files define what the components mean individually but never state the composition convention. Composing two records, or applying one to a vector, therefore requires an assumption from outside the files. The angular-separation formula in §3 is deliberately chosen because it does not need this.

**Nature of the attitude — declining to decide.** Determined, estimated, filtered, predicted, or commanded — the files do not say. This materially changes whether inter-originator disagreement is an accuracy measure or a plan-versus-actual comparison.

**Whether both timestamps went through the same conversion — guess.** The schema says every time in the source message is in the declared system and that "the value" was converted to UTC, without making clear whether that covers the creation time as well. The instance labels both with a zero offset. **My guess** is that both are UTC as labelled and the latency difference is a real elapsed duration; I flag the residual risk that the creation time is nominal.

**Non-negative scalar — decided, and not in the reassuring direction.** The schema phrases the half-turn bound as conditional on the scalar not being negative, which entails that negative scalars are possible. Nothing enforces the convention. Treat sign canonicalisation as mandatory, not defensive.

**Nothing is machine-enforced.** A validation vocabulary is declared but no constraint is attached to any member. Unit norm, non-negative scalar, and creation-after-epoch are all prose claims made by the schema author, not checks a validator will perform. They are assertions to be tested on ingest, not guarantees.

**Five-decimal precision — assumption.** One example is not a convention. I am assuming the precision floor of about two arcseconds generalises; a producer emitting more digits would raise it and one emitting fewer would lower it, and this should be measured over real traffic rather than assumed.

**Cadence, ordering, and duplication — not determined.** Whether records arrive in epoch order, at fixed cadence, at all, or more than once per spacecraft-epoch is nowhere stated. Since the aliasing limit on rate estimation (§2) depends entirely on cadence, this must be characterised empirically before any rate product is trusted.

**Identifier semantics — partly guessing.** That the international designator is the more reliable join key than the free-text name is **my judgement**, based on the designator having declared structure and the name having none. The meaning of the designator's trailing letter is not established by the files and I am not supplying one.

**The referenced annotation is absent.** The schema points to an accompanying annotation that names the scalar component first, and that annotation is not in this directory. Any consumer wired to it will see a different component order than the record stores. That reordering is real and must be handled; its details cannot be checked from what is here.
