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
