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
