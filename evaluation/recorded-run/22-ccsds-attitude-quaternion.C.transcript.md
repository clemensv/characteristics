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
