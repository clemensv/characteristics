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

1. The transform is encoded as `quaternion` and carries coordinates out of `#/definitions/SpacecraftBodyFrame` into `#/definitions/TerrestrialFrame`, with components in the order ["qc", "q1", "q2", "q3"]. The direction and the component order are fixed by the annotation and are not conventions to be guessed.
   wrong reading: Assuming a component order or rotation sense from convention, or applying the transform in the opposite direction.

2. `creation_date` is an operational instant (`resultTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `creation_date` as the event time of the observation.

3. `epoch` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `epoch` as the time the record was produced, received, or published, or using a different member for event time.


TRANSCRIPT A

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


TRANSCRIPT B

# Spacecraft attitude quaternion feed — analyst's briefing

## 1. What this feed is

Each record is a single **orientation fix for one spacecraft at one instant**. It says how the spacecraft was turned in space at a stated moment — nothing about where it was, how fast it was turning, or how well the fix is known. The orientation is expressed as a quaternion relating the spacecraft's own structural frame to an Earth-fixed geocentric frame (the schema pins these as `SC_BODY_1` and `ITRF1997`, and writes both out because neither is citable as a resolvable definition).

Alongside the orientation, each record carries the spacecraft's identity (a common name and an international designator), the organisation that produced the message, the instant the attitude holds at, and the instant the message was produced. The example record is a fix for TRMM produced by GSFC.

Three things about the shape of the record matter more than anything else and are easy to get wrong:

- **The quaternion's storage order and its declared meaning order are deliberately different.** The frame-transform annotation lists the components scalar-first (`qc, q1, q2, q3`); the record stores them scalar-last. The schema states outright that the annotation states meaning and the record states storage. Anyone who reads the annotation's component list and then packs the JSON members in the order they appear will build a quaternion with the scalar in the wrong slot. This is the single most likely silent failure in this feed.

- **There is no member that records which convention the source message used.** The schema notes that the originating standard once made scalar position a producer-supplied field taking `FIRST` or `LAST`, and that the current issue removed the field and fixed the position at last. This record shape carries no such field and no message-version member. If historical messages are ever mapped into this shape, the information that would let you detect a scalar-first source has been discarded at ingest. The only vintage clue in the record is `creation_date`, and it is a weak one.

- **The frames are fixed by the schema, not stated per record.** The source standard permits a range of reference frame names in an annex; this shape can express exactly one pair. A message referenced to some other frame that was pushed through this shape would be silently relabelled as body-to-`ITRF1997`. Nothing in a record lets you check this. The same applies to time: the source message declared its time system in a keyword, and that keyword has no member here — the record asserts a UTC value and gives you no way to verify the conversion.

## 2. Analytics worth running

**Attitude history for one spacecraft.** Order records by `epoch` and derive, per record, the rotation angle and rotation axis from the quaternion. The schema gives you enough to do this: it states that the scalar component is the cosine of half the rotation angle and each vector component is a rotation-axis component times the sine of half that angle. For the example record this yields a rotation angle of about 150.2° — and usefully, the *magnitude* of that angle is independent of the unresolved direction-of-rotation convention discussed in §5, because conjugating a quaternion leaves the scalar part alone. The rotation axis is likewise convention-independent up to sign, because a rotation's axis has the same coordinates in both the frame it rotates from and the frame it rotates to.

**Angular rate between consecutive fixes.** Compose successive attitudes into a relative rotation and divide the resulting angle by the epoch separation. This is supported because `epoch` is the time the attitude holds at and the frames are constant across the feed. Two caveats bound the result, both serious: the target frame is Earth-fixed, so the derived rate is the spacecraft's rotation *relative to a rotating Earth*, not relative to inertial space — a spacecraft holding a fixed inertial orientation will show a steady non-zero rate in this feed. (That an Earth-fixed frame rotates relative to inertial space is knowledge I am bringing from outside the two files; the files say the frame is Earth-fixed and geocentric and say nothing about its motion.) And the rate is a mean over the interval, not an instantaneous rate; the feed carries no rate member.

**Pointing stability.** Dispersion of consecutive relative rotations about their central value gives a jitter or drift measure. Same frame caveat applies: what you measure includes the Earth-fixed frame's motion unless you remove it.

**Instrument boresight and nadir direction in Earth-fixed coordinates.** The body-frame definition describes its first axis as the primary instrument boresight and its third as the nominal nadir direction, so rotating those body unit vectors through the quaternion gives their Earth-fixed directions. This is the analysis most likely to be *wanted* and it is the one I would gate hardest: the schema explicitly says the physical directions of the body axes are a matter for each spacecraft's interface control document and that the descriptions given are a record of what such a document would state. Treat these axis meanings as illustrative until the actual ICD is in hand. Also note you get a *direction*, not a ground target — there is no position member in the record, so you cannot say what the boresight is pointed *at* without ephemeris this feed does not carry.

**Production latency and pipeline health.** `creation_date` minus `epoch` is a clean latency measure, and it is one of the few straightforward differences in this feed. For the example record it is 4 h 55 m 41.8828 s. Grouped by `originator` and tracked over time, this detects pipeline stalls and reprocessing campaigns. The schema is explicit that `creation_date` is not a property of the attitude, which is exactly why it works as a process metric.

**Record-level data quality screening.** Three checks are directly supported and all three are worth automating:
- *Norm.* Sum the four squares. The example record gives 0.9999957, i.e. a norm about 2.1 × 10⁻⁶ short of unity — consistent with values rounded at the fifth decimal, and not evidence of a defective quaternion. A record whose sum of squares departs from 1 by materially more than rounding can explain is either corrupt or built with components in the wrong slots. This check is the practical detector for the scalar-position trap in §1.
- *Hemisphere.* The sign of `qc` tells you which hemisphere the record sits in; the schema notes that a non-negative scalar corresponds to a rotation confined to a half turn either way. Track the sign distribution per originator.
- *Epoch integrity.* Duplicate epochs for one spacecraft, non-monotonic epochs, and gaps.

**Cross-originator agreement.** If two organisations ever publish an attitude for the same spacecraft at the same epoch, the relative rotation between the two reported attitudes is a direct disagreement measure. The schema supports this by treating `originator` as the observing procedure and explicitly declining to tie it to the spacecraft operator. Nothing in the two files establishes that such duplicate records exist.

**Coverage and provenance census.** Record counts and epoch coverage by spacecraft designator and by originator. Trivially supported and worth doing first, because it tells you whether the feed is one spacecraft or many and whether the sampling is regular — neither of which the two files settle.

## 3. Combination rules

### The four quaternion components

**They are not four scalars. They are one value in four slots, and almost every scalar operation on them is invalid.**

- **Do not sum them.** Nothing here is an extensive quantity. A sum of two attitude components has no referent.
- **Do not average them componentwise.** A componentwise mean of two unit quaternions is not a unit quaternion and does not represent the orientation "between" them. Averaging attitudes requires a rotation-aware method; the two files do not specify one, and I am not going to name one as though the files did.
- **Do not difference them componentwise.** The difference of two attitudes is a *relative rotation*, obtained by composing one with the inverse of the other, not by subtracting components. A componentwise difference is not an angular quantity and does not go to zero as the two attitudes converge — see the sign point below.
- **Do not interpolate them linearly.** Componentwise linear interpolation between two records puts the resulting four-tuple off the unit sphere, so it is not a rotation at all. A rotation-aware interpolation is required; the files do not specify one.
- **Do not take minima, maxima, or per-component distributions and read them as physics.** A single component is not an interpretable quantity on its own; only the four-tuple is. Per-component histograms are legitimate as crude data-quality diagnostics and as nothing else.

**The sign trap.** A quaternion and its negation describe the same orientation. Two records describing *identical* attitudes may have all four components opposite in sign. Any comparison, difference, statistic, or clustering performed on raw components will therefore report a large discrepancy where there is none. Before any cross-record numerical work, align records to a common hemisphere — the schema's remark that a non-negative scalar bounds the rotation to a half turn either way identifies non-negative `qc` as the natural canonical choice. The example record satisfies it, but one record does not establish that the producer enforces it, and I would not assume it does.

**When attitudes may legitimately be combined.** Composing two attitudes into a relative rotation is valid only when both records share the same from-frame *and* the same to-frame. Within this schema the frame pair is fixed, so that condition is met by construction for records of the same spacecraft — but see the next point, which is the one that actually bites.

**Never combine attitudes across different spacecraft.** The from-frame is the body frame of an individual spacecraft, and the schema says plainly that which physical directions its axes point in is settled by that spacecraft's own interface control document. Two records with different `object_id` therefore have different from-frames despite carrying the same frame *name*. Differencing them, averaging them, or comparing their components produces a number with no meaning. Group by spacecraft before any attitude arithmetic — always.

**Combining with attitudes referenced to a different terrestrial realization.** The schema names one specific realization. Whether attitudes referenced to a different realization of the same terrestrial system may be pooled with these is not addressed by the two files, and I decline to decide it here.

### `epoch` and `creation_date`

Both are timestamps and both may be compared, ordered, and differenced. Their difference within a record is meaningful (latency, §2). Differences *across* records are meaningful as elapsed time subject to the civil-time caveat in §4.

They must not be summed or averaged as instants — an average of two timestamps is only meaningful if you have decided it means the midpoint of an interval, which is a modelling choice, not something these files make for you. Averaging *differences* (mean latency) is fine.

**The two must not be substituted for one another.** `creation_date` is when the message was made; the schema states it is later than the attitude's epoch and is not a property of the attitude. Never use it as the time axis, never plot attitude against it, never bin attitudes by it. Its legitimate uses are latency measurement and vintage ordering — if the feed ever carries two records for the same spacecraft and epoch, the later `creation_date` is the more recent production, though whether that means it supersedes the earlier is a policy question the files do not answer.

### `object_name` and `object_id`

Identity keys. Comparable for equality only; not orderable in any meaningful sense, not summable, not averageable. Use `object_id` — the international designator — as the grouping key, not `object_name`. My reason for preferring the designator is an assumption, not something the files establish: designators are structured and issued, common names are not, so I would expect the name to be the less reliable key. The files do not say the name is non-unique or unstable.

### `originator`

A categorical label for the producing organisation, comparable for equality only. Two things follow that an analyst will otherwise get wrong. First, it is **not** a proxy for the spacecraft's operator — the schema says the standard does not require the two to coincide, so do not infer operatorship, ownership, or authority from it. Second, because it identifies distinct producers, it is the correct axis along which to check for convention drift, precision differences, and latency differences before pooling records from more than one source. Whether an originator change is a plausible cause of the historical scalar-position convention differing between records is a conjecture of mine, not something the files establish.

## 4. Time

**`epoch` is the time axis of the thing described.** It is the instant the attitude holds at — the schema marks it as the phenomenon time and states it explicitly. Every plot, every ordering, every rate calculation, every join to other attitude or ephemeris data must key on `epoch`. `creation_date` is the time the *message* was produced, is marked as the result time, and is explicitly stated not to be a property of the attitude; it belongs on a process-monitoring axis and nowhere else.

**How positions on that axis relate to civil time.** The source message declared its own time system in a dedicated keyword, and every time in that message was expressed in that system. This record shape carries the value **converted to UTC**, so the timestamps you see are civil times and the example values carry an explicit `Z`. Three consequences:

- **The original time scale is not recoverable.** No member records which system the message used. You cannot round-trip to the source, and you cannot verify the conversion from the record. If the conversion is wrong, the record gives you no signal.
- **The conversion statement is made about `epoch`.** Whether `creation_date` underwent the same conversion is asserted only by its `Z` suffix in the example, not stated anywhere. I decline to decide it. If precise production-time reasoning matters, confirm it with the producer.
- **UTC is not a uniform elapsed-time scale.** Differencing two UTC timestamps that straddle a leap-second insertion understates the true elapsed interval by that second, which corrupts any derived angular rate spanning such a boundary. *This is knowledge I am bringing from outside the two files* — the files name UTC and say nothing about its properties. For short-baseline rate work within a single day it does not arise; for long-baseline differencing it does.

**On sub-second precision.** In the example, `epoch` is given to a tenth of a millisecond while `creation_date` is given to whole seconds. That is an observation about one record, not a schema constraint — the type imposes no precision. Do not assume either precision holds across the feed, and in particular do not read the coarser `creation_date` resolution as meaningful quantisation of anything.

**On sampling.** Whether epochs are regularly spaced, whether the feed is a sampled series or event-triggered, and what the nominal cadence is are all undetermined from one record. Establish this empirically before treating the feed as a time series with a known rate.

## 5. Ambiguities

**Declining to decide — direction of the rotation.** This is the most consequential unresolved item in the two files. The transform is declared as going *from* the body frame *to* the terrestrial frame, but that phrasing does not distinguish between the quaternion that rotates a vector's coordinates from body components into terrestrial components and the quaternion that rotates the body axes onto the terrestrial axes — which is the conjugate of the first. The two differ by the sign of all three vector components. Adopting the wrong one transposes every derived direction and inverts every derived relative rotation, and because both interpretations produce perfectly well-formed unit quaternions, **no data-quality check in §2 will catch it**. Nothing in either file settles it, so I decline. Resolve it against the producer or against a record whose true orientation is independently known before deriving any pointing direction.

**Declining to decide — quaternion multiplication convention.** Composing attitudes requires a convention for the product's handedness. The files establish what each component *means* but not how two of these quaternions multiply. Undetermined.

**Declining to decide — whether the stored order can be trusted at ingest.** The schema resolves the meaning-versus-storage question for this shape: the annotation names the scalar first because it states meaning; the record stores it last. What it does not settle is what happens to records whose *source* used the older producer-selected scalar position, because this shape has no member preserving that choice and no version member. If the feed contains anything transcribed from older messages, the ordering of those records is not determinable from the record itself. The norm check will not help — reordering components of a unit quaternion leaves the norm at unity.

**Declining to decide — is the quaternion guaranteed normalised?** The schema imposes no norm constraint. The one example is unit to about 2 × 10⁻⁶, consistent with rounding at the fifth decimal. Whether that is a producer guarantee or a coincidence of this record is not determined. Renormalise defensively before use; that costs nothing and protects against the case where it is not guaranteed.

**Declining to decide — record uniqueness and revisions.** Whether more than one record can exist for the same spacecraft and epoch, and if so whether a later `creation_date` supersedes or supplements an earlier one, is not addressed.

**Declining to decide — cross-realization pooling.** As noted in §3.

**Declining to decide — the physical body axes.** The axis descriptions are explicitly flagged in the schema as a record of what an interface control document would state, for an individual spacecraft. They are not authoritative for TRMM or for any other specific craft. Any boresight or nadir analysis rests on obtaining the actual ICD.

**Guess — `qc` is probably not sign-normalised by the producer.** The one example has a positive scalar, which is consistent with a non-negative convention but equally consistent with chance. I would expect no enforcement and would test for it rather than assume it. Marked as a guess.

**Guess — the five-decimal precision is the source message's print precision rather than a genuine measurement resolution.** The values look like fixed-point transcription and the norm deficit is exactly what such rounding produces. Marked as a guess; the files say nothing about precision.

**Guess — the trailing digit in the body frame's name suggests a spacecraft may define more than one body frame.** If so, records for the same craft could in principle be referenced to different body frames, and this shape would not distinguish them. Purely inferential from the name; marked as a guess and worth confirming, because if true it weakens the "same spacecraft, therefore same from-frame" rule in §3.

**Not present at all, and worth stating so nobody goes looking.** There is no position or ephemeris, no angular rate, no uncertainty or covariance, no quality or validity flag, no manoeuvre or mode indicator, and no message-version member. The schema admits no optional or additional members, so records are structurally uniform and there is no missing-data handling to build — but equally, there is no quality field to filter or weight by. Any confidence attached to these attitudes must come from outside the feed.


TRANSCRIPT C

# 1. What this feed is

Each record states **the orientation of one named spacecraft at one instant** — nothing else. The orientation is given as the rotation that carries the spacecraft's own structural frame into an Earth-fixed geocentric frame, and it is carried by four numbers that are *one quantity*, not four independent measurements.

Three things about that are worth getting straight before anything else, because each of them is a way to be wrong while every value still validates.

**It is an attitude, not a position.** The transformation carries a rotation and no origin offset. The two frames it runs between do not share an origin — one is fixed to the spacecraft structure, the other runs from the geocentre — and no offset between them is carried. The record therefore lets you re-express *directions* between the two frames. It does not locate the spacecraft, and applying the transformation to a position vector silently assumes an origin coincidence the record does not establish.

**The target frame rotates with the Earth.** The orientation is reported against an Earth-fixed geocentric frame whose axes are tied to a reference meridian and a reference pole. A change in the four numbers between two epochs therefore mixes the spacecraft turning with the reference frame turning underneath it. Separating the two requires an Earth-rotation model, and neither file supplies one or names one.

**The record is closed.** Every member is required and no additional members are permitted, so this is the complete content of the feed forever. There is no uncertainty, no covariance, no angular rate, no attitude-determination method, and no time-system field, and none can appear without a schema change.

# 2. Analytics

**Pointing reconstruction and attitude history for a single spacecraft.** This is the primary use and it is fully supported, because the annotation resolves every choice that ordinarily has to be guessed: the scalar component is identified by name rather than by position, the three vector components are resolved onto the frames' declared axis order, the sense is fixed as *from*-frame coordinates into *to*-frame coordinates (`x' = M x`, the frame moves and the quantity does not), and positive angles are fixed to the right-hand sense. The specification also supplies a worked case for self-testing an implementation: a quarter turn in the right-hand sense about the third axis is the scalar 0.7071 with vector components 0, 0, 0.7071, and under it a vector reading 1, 0, 0 in the *from* frame reads 0, −1, 0 in the *to* frame. Any pipeline handling this feed should reproduce that before touching real data.

**Angular separation between two attitudes of the same spacecraft.** The half-angle parameterization is fixed — the scalar is the cosine of half the rotation angle and each vector component is the sine of half the angle times the corresponding axis component — so the rotation angle of each record and the angle between two records are both derivable. For the sample record the angle works out near 150°, i.e. the body and Earth-fixed frames are far from aligned, which is what you would expect against a rotating Earth-fixed target frame and is a useful sanity band.

**Production-latency analysis.** The message-production time and the time the attitude holds at occupy distinct declared roles, so their difference is a genuine, well-defined lag. In the sample it is a little under five hours. Grouped by originator this is a real operational metric, and it is one of the few things in this feed that can be summed and averaged freely.

**Producer-hygiene screening.** The four values should have unit norm and the scalar should be non-negative. Both are recommendations rather than requirements, so both are worth measuring rather than assuming. The sample passes: the sum of squares is about 0.9999957, a deficit of roughly two parts in a million, entirely consistent with the five-decimal rounding of the printed values, and the scalar is positive. A feed whose norms drift further than rounding explains, or whose scalars go negative, is telling you something about the producer.

**Detecting — not resolving — incompatibility with another feed.** If you pool this with attitude data from elsewhere, the declared frames and the declared transformation sense let a machine determine that the two disagree. They do not let it fix the disagreement. That is the deliberate limit of this annotation model, and it is the correct outcome to expect.

**What is *not* supported.** Angular rate by differentiation, interpolation between records, hold-last-value resampling, and uncertainty-weighted fusion are all unsupported as declared. See §3 and §5 for why.

# 3. Combination rules

**The four quaternion members, across records: never combine component-wise.** Do not sum, average, or difference the scalar or any vector component as if it were a scalar series. The parameterization itself forbids it: the components are trigonometric functions of half an angle times an axis, and a component-wise mean of two such quadruples is in general not of that form and not of unit norm, so it denotes no rotation at all. The composite quantity may be combined — you may compose two attitudes to get the rotation between them, and you may compute an angle between them — but only through rotation arithmetic, never through arithmetic on the members.

**And when you do that composition, do not reach for a library's quaternion product.** The specification fixes the parameterization and the transformation sense, which is enough to build each rotation matrix unambiguously; it does **not** fix a quaternion multiplication rule, and it records explicitly that the multiplication rule is exactly where conventions in circulation diverge. The safe path is: convert each record to a rotation matrix under the fixed parameterization, compose matrices, and validate against the worked quarter-turn case. Specifically noted: the SPICE convention carries the *negation* of the vector part carried here, so feeding these three vector components unchanged into a SPICE-convention routine yields the inverse rotation, and nothing in the four numbers reveals the error.

**Sign.** The scalar is only *recommended* to be non-negative, so a negative scalar is a legal record. Negating all four members denotes the same rotation — this follows from the parameterization the specification gives, since the same rotation can be written as its explementary angle about the negated axis — so two records may be numerically opposite and physically identical. Any comparison that works on the members rather than on the rotation must therefore normalize the sign first, or it will report a maximal difference between two identical attitudes.

**The three vector components are not a vector quantity.** The specification is explicit that a rotation-carrying quaternion is bound by neither the vector-frame nor the tensor-frame keyword, because three of its members lie along frame axes and the fourth does not. Do not rotate, project, or average them as a triple. One genuinely useful property does hold: because the rotation axis is unchanged by its own rotation, those three components read the same in both frames, so the question of which frame they are resolved in does not arise.

**Across different spacecraft: do not combine at all.** The body frame is a single named definition in the schema, but its own text says the physical directions of its axes come from the interface control document of the individual spacecraft and that the descriptions merely record what such a document would state. Two records for two different spacecraft therefore cite one written frame while meaning two different sets of physical directions. Attitudes from different spacecraft are not comparable, differenceable, or averageable, and the record set is not constrained to one spacecraft.

**Across feeds: do not match frames by name.** Neither frame carries a resolvable identifier — both are written out locally precisely because the source message names them by bare strings. A frame in another feed bearing the same string is not thereby the same frame, and the specification forbids inferring a shared frame from names, from classification tokens, or from samples agreeing.

**The two times.** The attitude time and the message-production time may be differenced against each other (that is the latency metric) and each may be compared and ordered against its own kind across records. They must not be pooled or averaged together as one series: they sit on the same axis but describe different things, one a property of the world and one a property of the message.

**The two spacecraft identifiers.** Use the international designator as the join key: it is the structured one, and its form is stated. Both identifiers are free strings with no binding to any external register, so neither should be resolved against a catalogue without an external agreement, and no code-list semantics may be assumed for either.

**The originator.** It fills the procedure slot, and procedure identity is comparability-critical — different procedures can bias the same quantity differently. But the schema itself says the originator need not be the operator, and the actual attitude-determination method is recorded nowhere. So equality of originator is at best weak evidence for grouping and is certainly not evidence of interchangeability, and *inequality* of originator tells you nothing either. This feed gives you no handle on determination-method bias at all.

# 4. Time

The time axis of the thing described is the **attitude epoch**, the member carrying the phenomenon-time role. The message-creation time is the result time; it belongs to the message, not to the attitude, and using it as the time axis would shift every record by an arbitrary production lag (nearly five hours in the sample).

Both are plain calendar date-times carrying no temporal-reference annotation, so ordinary core temporal semantics apply — RFC 3339 civil date-time — and both values in the sample carry an explicit `Z`. Positions on the axis are therefore UTC instants and relate to civil time directly, with no conversion needed by the consumer.

Two cautions.

**The conversion has already happened, and it is not auditable.** The schema states that the source message declares its time system in a field of its own, that every time in the source message is in that system, and that this record carries the value already converted to UTC. Which system that was is not stated in either file, no member carries it, and no reference-system annotation names it. You cannot verify the conversion, reverse it, or tell whether two producers converted alike. Anything that turns on the distinction between UTC and a continuous scale — most obviously behaviour around a leap second — is unresolvable from this data. I am flagging this as unresolvable rather than guessing what the source system was.

**Elapsed time between two UTC instants is not automatically physical duration.** Differencing two of these stamps gives calendar elapsed time; whether that equals elapsed physical time depends on leap-second handling, which neither file addresses. For latency figures at the scale seen here it is immaterial; for precise rate work it is not. Marked as a caveat, not as something the files decide.

Nothing establishes the *spacing* of records. No cadence is declared, so regular sampling must not be assumed, the existence of a successor record must not be assumed, and the record set must not be assumed ordered or complete.

Nothing establishes what the attitude does *between* stamps. No phenomenon-time relation is declared, and the specification is explicit that omission does not mean "instant". No support period is declared either. So it is not established that the attitude applies only at that instant, and it is equally not established that it holds until the next record. Interpolation and hold-last-value resampling are both unauthorized by the data as it stands. This is the single most likely place for a consumer to help themselves to a semantics the feed never granted.

# 5. Ambiguities

**Declining — the physical directions of the body axes for any particular spacecraft.** The schema hands this to each spacecraft's interface control document. The prose descriptions (boresight of the primary instrument; nominal nadir) are stated as what such a document *would* say, not as what any specific one does say. Without that document the four numbers are a well-formed rotation into a frame whose physical meaning is under-determined.

**Declining — which realization or epoch of the terrestrial frame is meant, beyond the bare name.** The schema says outright that the source names it by a bare string and offers no resolvable identifier, and that the axis order had to be written out because the source does not state it either.

**Declining — what phenomenon the record is declared to quantify.** The observable-property binding points at a placeholder catalogue and its classification token is the specification's own marker for a fictional catalogue; the schema identifier is likewise a reserved non-resolvable name. The binding is therefore indeterminate, and the specification forbids repairing it from descriptions, names, or samples. In practice you know from the prose what this is; formally, the binding resolves to nothing.

**Declining — the source time system, and who performed the UTC conversion.** As in §4.

**Declining — how the attitude was produced.** No derivation and no summary-function declaration. Measured, estimated, filtered, propagated, or smoothed are all consistent with the record, and the difference matters for anything statistical. Note this also means you must not treat successive records as independent samples.

**Declining — quality and uncertainty.** Nothing is carried, and absence of a quality declaration does not mean the quality is acceptable.

**Declining — whether a given stream is one spacecraft or many.** Not constrained.

**Flagging, with a recommended behaviour rather than a decision — the four-results reading.** Each of the four members individually carries the observation-result role, which on the face of it declares four separate results, and the record-level observed-property binding then attaches to each of them individually, so a generic role-driven tool will conclude the feed reports four independent attitude measurements per record. The frame-transformation binding says the opposite: the four members jointly carry one quantity. The files give no rule stating which reading governs a role-driven consumer. For arithmetic, the frame-transformation binding is the one to follow, unconditionally; the four-results reading is an artefact and must not be acted on. I am not claiming the files resolve this — I am telling you which side is safe.

**Assumption I am making explicit — that the two spacecraft identifiers denote the same feature.** Both carry the plain feature role, and the annotation model provides no mechanism that binds two feature members together as one entity. Their descriptions say they are the name and the designator of the spacecraft, and I am reading them that way, but nothing machine-checkable establishes it. Join on the designator.

**Guess — the resolution of the timestamps.** The sample shows the attitude epoch to four decimal places of a second and the creation time to whole seconds. That is one record. Nothing in the schema constrains either, and treating those as the feed's resolutions is a guess.

**Not an ambiguity, but a trap worth restating.** The order the four members are stored and declared in is not the order the annotation names them in, and the annotation order is the one that governs. The scalar is named first by the annotation and stored last in the record. Reading the members in declaration or serialization order, or handing them to a routine that expects scalar-first as a flat array, produces a rotation that is wrong in a way no norm check, no validation, and no visual inspection of the numbers will catch — a norm check in particular is invariant under any permutation of the four members and therefore cannot tell you which one is the scalar.


TRANSCRIPT D

# 1. What this feed is

Each record is a **single instantaneous orientation of one named space object**, published by a named producer. The orientation is carried as four numbers that together form one quaternion — a rotation. The record also carries the instant the orientation applies to, and separately the instant the record itself was produced.

The critical thing to understand before touching this data: a record contains **one physical quantity, not four**. The four numbers are components of a single rotation. Their sum of squares in the example record is 0.9999957 — unit to within rounding at five decimal places — which is what a rotation quaternion looks like and what an arbitrary 4-vector does not. Treat the four as an atomic value everywhere in your pipeline.

The record identifies the object two ways: a short human label and a longer identifier that follows a `YYYY-NNNL` shape. That shape is a common launch-designator pattern, but the files do not define it, and the files do not tell you what either identifier resolves to. You cannot learn from these files what object this is, what it does, or what it orbits.

# 2. Analytics this stream supports

**Attitude history per object.** You have a complete orientation stamped with a precise instant. Ordering records by that instant gives you the object's orientation as a function of time. This is the primary use and everything else derives from it.

**Slew and rate estimation.** For two records of the same object, the relative rotation between them, divided by the elapsed time, gives the average angular rate over that interval, and the rotation axis gives the direction of the slew. The data supports this because each record is a *full* orientation (not a partial or an angle), and the timestamps carry sub-second resolution — in the example, four decimal places on the seconds field. That precision is what makes short-baseline rate estimates viable. Two caveats that the files do not let you discharge: the estimate is only valid if consecutive records use the same rotational convention (see §5), and if the frames involved are themselves rotating, the number you compute is not an inertial rate.

**Maneuver and event detection.** Large relative rotation over a short interval, or a discontinuity in an otherwise smooth attitude history, is detectable from the same relative-rotation computation. Nothing external is needed.

**Pointing stability / jitter.** Dispersion of relative rotations at short time baselines characterizes how steadily the object holds attitude. This requires a sampling cadence dense enough to resolve it; the cadence is not established by a single record.

**Integrity checks that need nothing but the record itself.** The strongest one is the norm: the sum of squares of the four components must be 1. Any record where it is not is truncated, corrupted, or not actually a rotation, and should be quarantined rather than renormalized silently — renormalizing hides upstream damage. Other checks: duplicate or non-monotonic instants per object, coverage gaps, and records where the production instant precedes the state instant (see §5, prediction vs. determination).

**Producer latency profiling.** Production instant minus state instant is a well-defined duration and is worth tracking per producer. In the example it is about 4 hours 56 minutes. Understand what this measures: it characterizes the *publishing process*, not the object. It is an operations metric, not a physics metric.

**Cross-producer disagreement detection.** If two producers publish the same object at the same instant, comparing them is worth doing — **as an alarm, not as a merge.** See §3.

**What this stream does not support.** There is no position, so you cannot compute where the object is pointing at anything: no ground-target geometry, no sun angle, no nadir angle, no field-of-view coverage. Attitude without position answers "which way is it turned," never "what is it looking at." There is also no angular velocity member, no uncertainty or covariance, and no quality flag — so every derived rate is unweighted and carries no error bar you can defend, and you cannot distinguish a high-confidence record from a poor one.

# 3. Combination rules

## The four quaternion components — one quantity, `q1`/`q2`/`q3`/`qc` jointly

Treat these as a single value `Q`. The rules below apply to `Q`; the rule for the individual components is that there is no valid operation on an individual component at all.

- **Compare:** Yes, but only between records of the **same object**, from a context where the rotational convention is known to be identical, and only using a rotation-aware metric — the angle of the relative rotation. Do not compare component by component.
- **Difference:** Never component-wise. The meaningful "difference" between two attitudes is the relative rotation, obtained by composing one with the inverse of the other. Component subtraction produces a number with no physical meaning.
- **Sum:** Never, under any condition. The sum of two rotations is not a rotation; the result is off the unit sphere and corresponds to nothing.
- **Average:** Not arithmetically. A mean attitude is a defined concept but requires a rotation-aware estimator. A component-wise mean is wrong for two independent reasons: it leaves the unit sphere, and it is corrupted by the sign ambiguity below. It is only meaningful at all within a single object and a single convention.

**The sign trap — the single most likely way to get this data wrong.** A quaternion and its negation represent the *identical* rotation. Nothing in the files constrains which of the two a producer emits, and nothing forbids it from changing between records. Consequences you must design around:

- A per-component time series can show four enormous simultaneous jumps while the physical attitude did not move at all.
- Component-wise means, standard deviations, thresholds, and change-detection are all corrupted by this and will fire on non-events.
- Any comparison or interpolation must be sign-normalized first (align the second quaternion to the same hemisphere as the first) or must use a metric that is invariant to the flip.

**Never plot, threshold, trend, alert on, or aggregate a single component.** `q1` alone is not a physical quantity. It is one coordinate of a representation that is not unique.

## `epoch` (the state instant)

Differences between two state instants are durations and are meaningful and additive. Ordering is meaningful. Summing instants is meaningless. Averaging instants is arithmetically defined but rarely means anything useful; a midpoint of an interval is defensible, a "mean epoch" over a heterogeneous set is not.

One condition: durations are only exact if both records sit on the same underlying time scale. See §4 — this is not established.

## `creation_date` (the production instant)

Same instant algebra as above, but it lives on a **different axis**. It describes the producer's workflow, not the object's state. Never substitute it for the state instant when building a time series; never treat records as ordered by it. The one legitimate cross-axis combination is production-minus-state as a latency figure, and that figure describes the producer.

## Object identifiers

Nominal. Equality only — no ordering, no arithmetic, no distance. **Group and join on the longer structured identifier, not the short label.** Nothing in the files guarantees the short label is unique across objects or stable over time for a given object, and nothing guarantees the two identifiers stay in a fixed correspondence. Keying on the label risks silently merging two objects or splitting one. This is a reasoned choice about which identifier is more likely stable, not something the files decide — treat it as an assumption, but the failure mode of the alternative is worse.

## `originator`

Categorical; equality only. **Do not pool records across producers into one attitude series.** Because the rotational convention is nowhere declared (§5), two producers can describe the exact same physical orientation with different quaternions, and the data gives you no way to detect that they differ. Merging them produces a series with phantom slews at every producer changeover. Compare across producers only to raise a disagreement flag; resolve it out of band.

# 4. Time

**The time axis of the thing described is `epoch`** — the instant at which the stated orientation held. That is the only member that positions the *object's state* in time. `creation_date` positions the *record* in time and belongs to a provenance axis. Conflating them is the second most likely way to get this data wrong.

The two axes are not aligned. In the example the record was produced roughly five hours after the state it describes, which means this record is retrospective. Two consequences:

- **Records will not necessarily arrive in state-time order, and arrival order tells you nothing.** Sort by the state instant, always, at the point of use.
- Nothing in the files forbids a record whose production instant *precedes* its state instant — that would be a prediction rather than a determination. There is no member that labels a record as predicted, determined, filtered, or smoothed. Check the sign of the interval per record and segregate accordingly; do not assume the whole stream is one kind.

**Relation to civil time.** Both instants in the example carry a `Z` designator, placing them at zero offset — so read at face value they are directly civil time in UTC, with no local-offset conversion needed and no ambiguity about which day or hour is meant. Two practical points:

- Do not assume `Z` on every record. If a record arrives with a non-zero offset it denotes the same instant expressed differently, so *instant* comparisons remain correct, but **lexical string sorting silently breaks**. Parse to instants before ordering or deduplicating.
- Sub-second precision is present and load-bearing. The state instant in the example carries four decimal places on the seconds. A parser or store that truncates to whole seconds destroys the basis for short-baseline rate estimation. Preserve it end to end.

**What is not determined:** the files establish the *offset* is zero; they do not establish the *time scale*. Whether the producer's internal timekeeping was UTC, or another scale converted (or not converted) before serialization, is nowhere stated. At the four-decimal precision on offer, a scale confusion would be a tens-of-seconds error — orders of magnitude larger than the stated resolution. I decline to decide this from the files. If you are doing anything precision-sensitive, it must be confirmed out of band.

# 5. Ambiguities

**The reference frames are absent, and the schema forecloses their ever appearing.** A quaternion is a rotation *from* one frame *to* another. Neither frame is given. Without both, the four numbers do not denote a physical orientation — they denote a rotation between two unnamed things. You cannot say which way the object is facing; you can only say how its orientation changed between two records, and even that only if you assume both records use the same unnamed pair. This is not an oversight you can wait out: every member is required, no additional members are permitted, and there is no frame member. **The frame information can only ever come from outside these files.** Obtain it before publishing any derived orientation. I am declining to guess the frames — a wrong guess here produces confidently wrong answers rather than obviously wrong ones.

**The direction of the rotation is undetermined.** Even given two frames, whether the quaternion maps A onto B or B onto A is not stated. The conjugate is equally consistent with everything in the files. Getting this backwards inverts every orientation and reverses the sign of every derived slew axis. Declining to decide.

**Which component is the scalar part is inferential, not established.** The naming of the fourth component sets it apart from the three numbered ones, and the conventional reading is that it is the scalar (cosine) part with the numbered three as the vector part. **That is my inference from the name, and I mark it as such.** The numbers cannot settle it: the norm is symmetric in all four, so the unit-norm check passes under any assignment. The stakes are concrete — if the fourth component is the scalar, the example encodes a rotation of roughly 150 degrees; if the second component were instead the scalar, it encodes roughly 58 degrees. Same record, entirely different physical claim.

**Component-to-axis ordering is undetermined.** Which of the three numbered components corresponds to which axis is not stated, and would be meaningless anyway without knowing whose axes. This is downstream of the frame gap.

**Sign convention is undetermined and may vary within the stream.** Discussed in §3. Not a defect to be fixed in the data — it is inherent to the representation — but it must be handled explicitly in code.

**Nothing establishes what the identifiers denote.** Assuming the structured identifier follows a launch-designator convention is a **guess** based on its shape. The files define neither identifier's namespace, uniqueness, or stability.

**Sampling behaviour is unknown.** One record establishes nothing about cadence, regularity, burstiness, whether multiple producers cover the same object, or whether one state instant can appear more than once. All of these determine whether rate estimation, gap analysis, and deduplication are viable. Declining to characterize; measure it on real volume before designing around it.

**Revision semantics are undetermined.** There is no version, sequence, or supersession member. If two records share an object and a state instant but differ, you cannot tell a correction from a duplicate from a genuine producer disagreement. Using the later production instant as a tiebreaker is a reasonable operational default, but it is **my assumption**, not something the files support.

**Whether the quaternion describes the object's body relative to something, or something relative to the body, is undetermined** — a restatement of the frame and direction gaps, but worth calling out separately because it is the question an analyst will actually ask first and the files answer it not at all.
