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

1. `CREATION_DATE` is an operational instant (`resultTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `CREATION_DATE` as the event time of the observation.

2. Successive `CREATION_DATE` values are expected at cadence `irregular`. A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

3. `EPOCH` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `EPOCH` as the time the record was produced, received, or published, or using a different member for event time.

4. Positions in `EPOCH` are expressed in the temporal reference system `#/definitions/TleEpochPosition` (kind `type`), not in an unqualified civil clock.
   wrong reading: Reading `EPOCH` as ordinary UTC.

5. `EPOCH` is on a clock of its own. Converting it to civil time requires a synchronisation relation that the schema does not supply, so a correct reader declines the conversion or states the external input it would need.
   wrong reading: Converting `EPOCH` to UTC as though the mapping were given.

6. `day_of_year` is expressed in `d`.
   wrong reading: Assuming a different or conventional unit for `day_of_year`.

7. `MEAN_MOTION` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `MEAN_MOTION` as a measured observation.

8. `MEAN_MOTION` is expressed in `rev/day`.
   wrong reading: Assuming a different or conventional unit for `MEAN_MOTION`.

9. `ECCENTRICITY` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `ECCENTRICITY` as a measured observation.

10. `INCLINATION` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `INCLINATION` as a measured observation.

11. `INCLINATION` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `INCLINATION`.

12. `RA_OF_ASC_NODE` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `RA_OF_ASC_NODE` as a measured observation.

13. `RA_OF_ASC_NODE` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `RA_OF_ASC_NODE`.

14. `ARG_OF_PERICENTER` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `ARG_OF_PERICENTER` as a measured observation.

15. `ARG_OF_PERICENTER` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `ARG_OF_PERICENTER`.

16. `MEAN_ANOMALY` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `MEAN_ANOMALY` as a measured observation.

17. `MEAN_ANOMALY` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `MEAN_ANOMALY`.

18. `BSTAR` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `BSTAR` as a measured observation.

19. `BSTAR` is expressed in `1/ER`.
   wrong reading: Assuming a different or conventional unit for `BSTAR`.

20. `MEAN_MOTION_DOT` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `MEAN_MOTION_DOT` as a measured observation.

21. `MEAN_MOTION_DOT` is expressed in `rev/day^2`.
   wrong reading: Assuming a different or conventional unit for `MEAN_MOTION_DOT`.

22. `MEAN_MOTION_DDOT` is `modeled` and is not a measurement. It must not be presented as observed fact or used as ground truth against which measurements are validated.
   wrong reading: Treating `MEAN_MOTION_DDOT` as a measured observation.

23. `MEAN_MOTION_DDOT` is expressed in `rev/day^3`.
   wrong reading: Assuming a different or conventional unit for `MEAN_MOTION_DDOT`.

24. `epochDayOfYear` is expressed in `d`.
   wrong reading: Assuming a different or conventional unit for `epochDayOfYear`.


TRANSCRIPT A

# Orbit mean-element feed — analyst's briefing

## 1. What this feed is

Each record is one **fitted orbit state for one tracked object, valid at one instant**. It is not a measurement of that object. The record declares its own production route: an orbit-determination procedure named `SGP4` produced every element in it, and every element carries `derivation: modeled`, which in this annotation vocabulary means the value carries information the observations do not contain, supplied by the model's own representation of the system. Nothing in the record is an observed position, velocity, or physical property.

The subject of the record — the feature of interest — is a catalogue-numbered resident space object, identified by exactly one member. The record also declares a publication instant distinct from the instant the elements describe, so a record has two times with different meanings, and they are not in the same time regime.

The practical shape of the stream is: an object is re-fitted whenever new tracking data warrants, and each re-fit emits a fresh, complete, self-contained state. Records are therefore a **sequence of independent snapshots of a model estimate**, not a time series of readings and not an incrementally updated state.

The single most consequential fact for anyone consuming it: the numbers are *inputs to a propagator*, not *outputs about the world*. They are only meaningful when fed to an implementation of the declared theory. The record declares the theory precisely because the same object fitted under a different theory yields different element values.

## 2. Analytics the stream supports

**Per-object orbital decay and re-entry watch.** Track mean motion and its first derivative across successive epochs of one object. Supported because epochs are totally ordered (see §4), every element is declared to apply at an instant rather than over a window, and the theory that produced them is declared and can be checked for constancy across the series. Rising mean motion over a series of epochs is the signal; it is a *model* signal, not an observation of altitude.

**Ephemeris generation.** Feed the elements plus the epoch to an SGP4 implementation. Supported because the record names the mean-element theory as the observing procedure and states that the elements are only meaningful when consumed by a propagator implementing it. The record contains no position or velocity — producing those is the consumer's work.

**Fit-refresh behaviour and freshness monitoring.** The record separates the instant the state describes from the instant the fit became available, so you can measure how far a published fit lags its own epoch, and how often an object is re-fitted. This analysis is *wanted* and *partially obstructed*: the two instants are in different time regimes and cannot be subtracted without an authoritative conversion (§4). The feed also declares its publication rhythm as irregular with no period, so you cannot derive a staleness threshold from the schema — you must set one from your own operational judgement.

**Population structure of the catalogue.** Distribution of inclination, eccentricity, and mean motion across many objects at one time. Supported because all objects in the feed are fitted by the same declared procedure, which makes cross-object grouping defensible. Two caveats bound it, both material: each record carries *its own* epoch, so a cross-object cut is never a simultaneous snapshot, and a QUDT quantity-kind classification shared by two members does not make them the same quantity (§3).

**Constellation / launch cohort grouping.** The launch designator gives launch year, launch number, and piece, so pieces of one launch can be grouped. This is a grouping key, not a feature identity — see §3 and §5.

**Cross-object anomaly screening on drag behaviour.** Weak. The drag term is declared to be a free parameter of the fit rather than a physical property of the object, and the record carries nothing about the object's mass or area. You can screen for *change* in an object's own drag term over time; you cannot rank objects against each other by it and call the result physics.

An analysis that is **not** supported and that people will attempt: interpolating between two consecutive element sets to obtain a state at an intermediate time. Each set is an independent fit; the record declares no covariance, no quality, and no relationship between one fit and the next. Interpolation between them is not licensed by anything in the files.

## 3. Combination rules

Three conditions gate almost everything below. State them once:

- **C1 — same object.** Records may be combined only when the catalogue identifier agrees. That member is the declared feature of interest; the object name and the launch designator are *not*, and the annotation model forbids inferring feature identity from a name or a description.
- **C2 — same procedure.** The mean-element theory is declared as the observing procedure, and procedure identity is comparability-critical: differing procedures can give different biases and meanings for the same property and feature. Records with differing theory values are not comparable as like quantities. Equality of theory is grounds for *candidate* grouping, not proof of statistical interchangeability.
- **C3 — same time regime.** Positions may be compared, ordered, or combined only within one binding, or through an authoritative transformation. The epoch and the creation date do not share a binding.

| Quantity | Compare | Difference | Sum | Average | Governing condition |
|---|---|---|---|---|---|
| Mean motion | Yes, under C1+C2; across objects only as a population statistic | Yes, under C1+C2 | No | Only as a population statistic, never as "the orbit" | A difference across epochs mixes real decay with re-fit noise; the record publishes no uncertainty by which to separate them |
| Eccentricity | Same as mean motion | Same | No | Population only | Dimensionless and bounded, so arithmetic is well-formed; interpretation still needs C1+C2 |
| Inclination | Yes, under C2 (cross-object comparison is meaningful) | Under C1+C2 | No | See below — **not** by naive arithmetic | Angular; reference frame undeclared (§5) |
| RAAN, argument of pericentre, mean anomaly | Yes, under C1+C2 | Only with wrap handling | No | **No** by naive arithmetic | Bounded 0–360 angles measured from a fixed direction; see below |
| Drag term | Only against the same object's own history, under C1+C2 | Under C1+C2, as a change in a fit parameter | No | No | Declared a free parameter of the fit, not a property of the object; may be zero or negative; declared physically meaningful only for low-Earth orbits |
| First and second derivatives of mean motion | Under C1+C2 | Under C1+C2 | No | No | Distinct units from mean motion; never add a rate to a value |
| Revolution count at epoch | Under C1 only | Yes, under C1 — gives revolutions elapsed between two epochs | No | No | Cumulative since launch, so cross-object comparison compares launch dates, not orbits |
| Element set number | No | No | No | No | Declared a modulo-1000 counter with a frequently-emitted placeholder value; unusable as a sequence key |
| Ephemeris type, classification | Equality only | No | No | No | Categorical |
| Epoch, creation date | Order and compare *within* one of them | See §4 | No | No | C3 |

**Angles.** The three orbital orientation angles and the anomaly are bounded on 0–360 and are described as angles measured from a fixed reference direction, so 0 and 360 denote the same direction. Arithmetic that treats them as ordinary reals — a mean, a standard deviation, a naive difference — is wrong near the wrap point and produces plausible-looking garbage. *This is an inference, not something the files state:* the files give the bounds and the geometric description, and state no wrap convention, no branch cut, and no circular-statistics rule. Treat wrap handling as your responsibility and document the convention you choose.

**The four angles are not one quantity.** Inclination, RAAN, argument of pericentre and mean anomaly all carry the *same* quantity-kind reference. The annotation model is explicit that this establishes nothing: a processor must not infer identity or semantic equivalence from quantity-kind classification, and a quantity-kind mapping is a compatibility hint, not evidence of sameness. Any pipeline that keys on the observed-property reference to decide what may be aggregated will silently pool four unrelated orbital angles into one bucket. This is the highest-probability automated failure in this feed.

**Never average element sets together.** Averaging the elements of two records for one object at two epochs, or of two objects, does not produce a valid orbit. Each set is a jointly-fitted parameter vector consumed as a unit by the propagator; the record publishes no covariance and the annotations grant no permission to aggregate. Population statistics over a *collection* of objects are legitimate — they describe the population, not an orbit, and should be labelled as such.

**Never mix a fitted element with a value from another source.** The elements are model outputs of one declared procedure. Comparing an inclination here with an inclination from a different determination process violates C2 unless you have external authority that the two procedures are interchangeable.

**Do not attach error bars.** The record carries no result-quality member. The annotation model states plainly that the absence of a quality declaration does not imply acceptable quality. It means unknown.

## 4. Time

Two members carry time, with different roles, and confusing them is the second-most-likely failure here.

**The epoch is the time axis of the thing described.** It is the record's phenomenon time: the instant to which every element applies and from which the propagator integrates. Every element additionally declares that it applies *at an instant*, not over a window and not until the next record. Two consequences follow directly: there is no interval over which these values may be accumulated or averaged, and holding a value forward in time is not licensed — extending the state in time is what the propagator does, and that is a computation, not a data operation.

**The epoch is not civil time.** It is expressed in a declared regime that locates a position by calendar year and fractional day of that year, counting uniform 86400-second days with no leap-second correction, because that is what the propagator assumes. The regime's definition states, in terms, that a position in it is not an RFC 3339 civil instant and **must not** be compared with one without an authoritative conversion, with the discrepancy bounded by the leap seconds accumulated in the year in question.

**Ordering is safe; arithmetic is not.** The epoch carries a fixed-width, most-significant-first string rendering, and the regime declares forward sort order. You can therefore sort and compare epochs correctly with plain lexical string ordering, without implementing the regime and without any conversion. That covers ordering, sequencing, deduplication by position, and "latest record wins". It does **not** cover elapsed time: a lexical ordinal supports order, not metric intervals, and the annotation model forbids inferring metric intervals from ordinal positions. Elapsed time between two epochs must be computed from the year and fractional-day components under the regime's own rules.

**The convenience UTC rendering is not authoritative.** The record carries a best-effort normalisation of the epoch to an RFC 3339 timestamp, and explicitly disclaims it as non-authoritative: a consumer propagating the elements must use the regime's own components. It is also *optional* — only the ordinal, year and day-of-year are required — so a pipeline built on it will fail on records that omit it. Use it for display and approximate bucketing. Do not use it for propagation, and do not use it to reconstruct the epoch.

**The creation date is a different axis.** It is the record's result time: when the fit became available. It is an ordinary civil UTC timestamp. It follows the epoch in time, because the fit consumes observations taken up to and around the epoch. Its recurrence is declared irregular with no period — several times a day for low orbits, less for deep space.

**The two axes must not be subtracted.** Computing publication lag as creation date minus epoch crosses two time bindings and requires an authoritative conversion the files do not supply. If you need the lag, either obtain a leap-second-aware conversion from outside these files, or compute it from the non-authoritative UTC rendering and label the result as approximate, bounded in error by that year's accumulated leap seconds.

**No cadence is declared for the epoch axis at all.** Cadence is declared only on the publication instant, and it is irregular. So the schema licenses no expected epoch spacing, no gap detection on epochs, and no staleness rule. Separately, the annotation model states that a declared cadence is an expectation and never a constraint: a record whose timing departs from it is late, not invalid, and cadence must never be used to synthesise a record that does not exist.

## 5. Ambiguities

**No record identity is declared.** The schema names no key. *Guess:* the catalogue identifier together with the epoch ordinal is the natural candidate. *Declining to decide:* whether that pair is actually unique. Whether the publisher can emit two different fits at the same epoch for the same object — a re-fit that lands on the same instant — is not determined by the files. If you deduplicate on that pair, you may be discarding a genuinely newer fit; the publication instant is the only tiebreak available, and the files do not say it is a valid one.

**No supersession or lifecycle signal.** The only status member in the record is a security classification, which the annotation model treats as a statement about how the *record* is to be handled and not about the phenomenon. There is no "superseded" or "withdrawn" state. Whether a later epoch or a later publication instant retires an earlier record is not determined. Declining.

**The reference frame of the angles is undeclared.** The inclination is described relative to Earth's equatorial plane and the RAAN relative to the vernal equinox, but no reference-frame or coordinate-reference-system annotation is present, and the annotation model forbids inferring a frame from member names, descriptions or samples. Comparing these angles with angles from any other source therefore has no established basis. Declining — this must come from the propagator specification, not from these files.

**Which propagator branch to use.** The record declares one theory and one ephemeris type, and the ephemeris-type description mentions a deep-space variant alongside the near-Earth one. Nothing in the record indicates which branch applies to a given object. Selecting on mean motion is a domain convention the files do not state. Declining.

**The Earth-radius basis of the drag term.** The drag term's unit is inverse Earth radii; which Earth radius value is meant is not determined. Consumers converting it must obtain that from the propagator definition. Declining.

**Whether the derivative terms are pre-scaled for the propagator.** The record states that the first derivative member holds one half of the true derivative and the second holds one sixth. *Assumption:* the values are stored in that pre-scaled classical form and should be handed to the propagator unmodified, since the record describes them as the classical terms the theory consumes. Anyone using them for independent physics rather than for propagation must undo the scaling; the files do not say which convention a downstream tool expects.

**Whether a revolution counter can roll over.** A difference of the counter across two epochs of one object gives revolutions elapsed — *under the files*, which declare no maximum and no wrap. If the underlying encoding wraps, the files do not say so, and a naive difference would go negative. I am not asserting either way; guard for a negative difference.

**Whether quantity-kind references are appropriate observed properties.** The annotation model expects an observed-property reference to identify one immutable observable-property definition and to deep-link to a concrete definition entry; the element members instead cite broad quantity-kind classifications, and the model separately says quantity-kind classification does not establish equivalence. Whether this is a modelling weakness in the schema or a deliberate use of an open catalogue kind is not determined. I flag it because it changes what a conforming processor may do with these references — which is: very little. Declining to decide the intent; the operational consequence in §3 stands either way.

**The record is closed.** No additional members are permitted, so covariance, uncertainty, or provenance detail cannot arrive in-band later without a schema change. That is a fact, not an ambiguity, but it bounds every "we'll add error bars later" plan.

**Validity of the unit strings.** The unit tokens for revolutions per day, its derivatives, and inverse Earth radii are governed by a units specification that is not among the files I was given. Whether they are well-formed under it, and whether any of them is convertible by an automated unit engine, is not something I can decide here. Declining.


TRANSCRIPT B

# Orbit mean-element feed — analyst's briefing

## 1. What this feed is

Each record is one **orbit solution for one catalogued space object at one instant**: a set of mean orbital elements (mean motion, eccentricity, inclination, and three angles), plus drag-like terms and bookkeeping fields, tagged with the object's catalogue number and the instant the elements describe.

The critical property, and the one that governs everything else, is stated explicitly in the record: the elements are **mean elements under a named theory** (`MEAN_ELEMENT_THEORY`, `"SGP4"` in the example). They are not an observed position or an osculating state vector. They are fitted parameters whose only defined meaning is "the numbers you feed to that particular propagator to reproduce the object's motion." A record is therefore a *model fit*, not a measurement, and it is only interpretable in the context of the theory named in the same record.

A stream of these records for one object is a sequence of successive re-fits produced by an originator (`ORIGINATOR`) as new tracking data arrives. Consecutive records are not independent samples of a physical quantity; they are revisions of an estimate.

Each record also carries **two distinct timestamps**: the instant the elements describe (`EPOCH`) and the instant the record was produced (`CREATION_DATE`). Confusing them is the most common way to get this data wrong.

## 2. Analyses the feed supports

**Per-object element time series and orbital decay.** Grouping records by `NORAD_CAT_ID` and ordering by `EPOCH` gives a trend line for each element. Because `MEAN_MOTION` and its derivatives are present in every record and the epoch is carried at sub-millisecond resolution, the rate of change of mean motion — the decay signature — is directly observable both as a differenced series and as the producer's own `MEAN_MOTION_DOT` estimate. Comparing those two is itself worthwhile (see §5 on the derivative convention).

**Maneuver and event detection.** A maneuver appears as a step or slope break in an element series that natural drift cannot explain. The feed supports this because it gives all six elements at a common epoch, so a discontinuity in one element can be checked against the others for corroboration. Note that a change of `ELEMENT_SET_NO` or `CREATION_DATE` with the same `EPOCH` is a *re-fit*, not an event — that distinction has to be enforced or every re-issue looks like a maneuver.

**Drag and space-weather response.** `BSTAR`, `MEAN_MOTION_DOT`, and `MEAN_MOTION_DDOT` are per-record fitted quantities. Their evolution across many low-orbit objects over the same epoch range is a population-level signal. The data supports this because the same three quantities are required in every record, so no object is silently missing from the population.

**Production latency and cadence.** `CREATION_DATE` minus the epoch instant gives per-record latency; the gap between successive epochs for one object gives refresh cadence. Both are computable from required fields alone. This is the analysis that tells you how stale the feed is at any moment, which conditions the validity of everything else.

**Population and constellation structure.** `INCLINATION`, `RA_OF_ASC_NODE`, `MEAN_MOTION`, and `ECCENTRICITY` across the catalogue at a common epoch window support clustering — objects sharing an orbital plane, objects in similar shells. The data supports this because those four fields are required and range-bounded, so a catalogue-wide snapshot is dense.

**Nodal regression.** For one object, the drift of `RA_OF_ASC_NODE` against `EPOCH` is measurable directly. Across many objects it can be studied against `INCLINATION` and `MEAN_MOTION`. This works only if the angular differencing is done modulo the full turn (§3).

**Fragmentation-event cohorts.** `OBJECT_ID` follows a launch-designator pattern (`YYYY-NNN` plus up to three letters), so records sharing a `YYYY-NNN` stem plausibly share a launch. This is a structural inference from the declared pattern, not something the files state. It is also unusable as a *primary* grouping because the field is both optional and nullable.

**Data-quality auditing.** Three independent representations of the epoch are carried in each record with no cross-consistency constraint, and `REV_AT_EPOCH` is a counter that should be predictable from elapsed time and mean motion. Both give cheap, self-contained integrity checks that require no external reference.

**What is *not* supported by these two files alone:** producing a position or velocity. Propagation requires an implementation of the named theory and the physical constants it assumes; neither is in the data. Likewise anything needing uncertainty — weighted fits, gating, covariance-based screening — is out of reach, because no record carries any error estimate at all.

## 3. Combination rules

The universal precondition, applying to every element below: **records may only be combined if they carry the same `MEAN_ELEMENT_THEORY` value.** The elements are parameters of a specific propagation model. A mean motion under one theory and a mean motion under another are different quantities that happen to share a name and a plausible magnitude. `MEAN_ELEMENT_THEORY` is an unconstrained string, so this must be checked per record, not assumed from the feed as a whole. A second precondition applies almost as widely: elements from different `ORIGINATOR` values are independent solutions, and interleaving them into one series manufactures apparent jitter that is producer disagreement, not physics. Keep originators in separate series unless you have specifically established they agree.

| Quantity | Compare | Difference | Sum | Average |
|---|---|---|---|---|
| `MEAN_MOTION` | Yes, same theory | Yes, same object | No | Yes, over a window short enough that decay is negligible |
| `ECCENTRICITY` | Yes, same theory | Yes, same object | No | Yes, same caveat |
| `INCLINATION` | Yes | Yes, ordinary subtraction | No | Yes, ordinary mean |
| `RA_OF_ASC_NODE` | Only modulo the turn | Only modulo the turn | No | Circular mean only |
| `ARG_OF_PERICENTER` | Only modulo the turn | Only modulo the turn | No | Circular mean only |
| `MEAN_ANOMALY` | Rarely meaningful | Only with revolution count restored | No | No |
| `BSTAR` | Yes, same theory | Yes | No | Yes |
| `MEAN_MOTION_DOT` / `_DDOT` | Yes, same theory | Yes | No | Yes |
| `REV_AT_EPOCH` | Yes, same object | Yes, same object | **No** | No |
| `ELEMENT_SET_NO` | Equality only | No | No | No |
| `EPHEMERIS_TYPE` | Equality only | No | No | No |
| `NORAD_CAT_ID` | Equality only | No | No | No |

Notes on the entries that carry real risk:

**The three angles bounded to a full turn** (`RA_OF_ASC_NODE`, `ARG_OF_PERICENTER`, `MEAN_ANOMALY`) wrap. The files declare only the numeric bounds, not the wraparound — treating them as cyclic is an assumption on my part, but it is the safe one, because the failure mode is silent: an arithmetic mean of 359.9 and 0.1 returns 180, a value on the opposite side of the orbit, with no error raised. Differences must be reduced into the half-turn on either side of zero; averages require a circular mean. The same applies to any linear regression against time — a naive least-squares fit of `RA_OF_ASC_NODE` versus epoch across a wrap point produces a nonsense slope.

**`INCLINATION` is the exception among the angles.** Its declared range is a half-turn, not a full one, so it does not wrap within its own domain and ordinary arithmetic is correct.

**`MEAN_ANOMALY` deserves separate treatment.** It is the object's phase within its orbit and it advances through a full turn many times per day at the mean motions this feed carries. Differencing two records' mean anomalies gives the phase difference modulo one revolution, which is almost never what an analyst wants; the whole-revolution count between the epochs has to be reconstructed from the mean motion and the epoch gap before the difference means anything. Averaging it across records is meaningless in every case I can construct. Treat it as a phase to be propagated, never as a state to be smoothed.

**`REV_AT_EPOCH` is a cumulative counter, not a measurement.** Differences between two records of the same object are meaningful — revolutions completed between the epochs, and a good cross-check against elapsed time times mean motion. Sums are meaningless. Differences *across objects* are meaningless because each object's counter has its own origin. The files do not state whether the counter ever wraps or resets; if it does, a difference across the discontinuity will be large and negative, and I would guard for that.

**Angles across objects.** Comparing `RA_OF_ASC_NODE` between two objects is only meaningful if they share a reference frame and the values are taken at the same epoch, because the node regresses. The files never name a reference frame; frame identity is implied only by shared `MEAN_ELEMENT_THEORY`, and that is my inference, not a statement in the files. Node comparisons at different epochs will show separation that is pure precession.

**Averaging elements at all.** Because successive records are revisions of a fit rather than repeated measurements, averaging them does not reduce noise in the way an analyst may expect, and it smears real secular drift. Where I have written "yes" for averaging above, I mean it is arithmetically defensible over a short window, not that it is statistically principled. With no uncertainty field in the record there is no way to weight an average correctly.

**Never sum anything in this record.** No quantity here is extensive. There is no aggregation over records for which addition is the right operator.

## 4. Time

**`EPOCH` establishes the time axis of the thing described.** It is the instant the elements are valid for. `CREATION_DATE` is the time the record was manufactured; it belongs to a processing axis, not a physical one. Two records with identical `EPOCH` and different `CREATION_DATE` describe the same instant and are competing solutions for it, not two points in a series. Plotting elements against `CREATION_DATE`, or joining two feeds on it, is the single most damaging mistake available here.

The epoch is carried in three forms. Only two of them are guaranteed present: the ordinal string and the year/day-of-year pair. The plain UTC timestamp is **optional** and may be missing from any record, so any pipeline that reads only that field will silently drop rows. The ordinal string is the field to treat as canonical: it is required, and its declared shape fixes the resolution at eight decimals of a day, roughly 0.86 ms.

Position on the axis relates to civil time as: **the instant is `day_of_year − 1` days after 00:00 on 1 January of `year`**, i.e. the day number is one-based and the fractional part is the time of day. I verified this against the single available record: day 211.76644861 of 2026 resolves to 30 July, 18:23:41.16, matching the record's own UTC field to the millisecond. That is confirmation from one example, not a rule the files state.

Two consequences of that arithmetic:

The optional UTC field is **rounded** relative to the ordinal — the ordinal in the example carries about 0.9 ms of resolution and the UTC field is truncated to whole milliseconds. They are therefore not interchangeable as join keys, and equality tests on the UTC string will fail against the ordinal-derived value.

Nothing in the files enforces agreement between the three representations. They can disagree, and if they do the files give no rule for which wins. Pick one, derive the others, and audit the disagreement rate.

The time scale of the day-of-year value is **not stated**. Its agreement with the UTC field in the one available record is consistent with it also being UTC, but that is one sample. If it is UTC, then day fractions in days containing a leap second do not map linearly to wall clock, because such days do not contain the nominal number of seconds; the files say nothing about how the producer handles this.

Two further gaps: `day_of_year` has a declared lower bound but no upper one, so a value past the end of the year is schema-legal and would silently roll into the following year under the arithmetic above. And nothing guarantees that records arrive in epoch order, or that a later `CREATION_DATE` implies a later `EPOCH` — sort explicitly, and do not assume the feed is append-only in time.

## 5. Ambiguities

**Units are entirely absent — declining to decide, and this is serious.** The schema declares numeric types and ranges but no units for any physical quantity. For the three full-turn angles and inclination, degrees are strongly implied by the declared bounds, and I would proceed on that basis; I am flagging it as an inference. For `MEAN_MOTION`, `BSTAR`, `MEAN_MOTION_DOT`, and `MEAN_MOTION_DDOT`, the files do not determine the units and I decline to state them. The example value of mean motion is consistent with revolutions per day, which would make the orbital period its reciprocal — that is a guess from one number and should be confirmed against the producer before any period, altitude, or decay-rate figure is published.

**The derivative convention is undetermined — declining.** Whether `MEAN_MOTION_DOT` is the plain first time derivative of mean motion or is scaled by a convention-dependent constant is not stated anywhere in the files. This matters because an analyst will naturally compute the derivative themselves by differencing consecutive records and will get a number differing from the published field by exactly that factor, then spend a long time looking for a bug. Determine which is which empirically against a long series before trusting either. `MEAN_MOTION_DDOT` has the same problem and is zero in the only example, so the example gives no help.

**`BSTAR` sign — resolved, and worth stating because it surprises people.** The field has no lower bound, so negative values are schema-legal. Do not filter them as corrupt. What a negative value *means* physically is not established by the files; I decline to say.

**The reference frame for the angles is not named — declining.** It is implied by the theory named in `MEAN_ELEMENT_THEORY` but never written down. Records with differing theory strings must be assumed to be in possibly different frames.

**`EPHEMERIS_TYPE` — declining entirely.** An integer with a lower bound of zero and the value zero in the example. Its semantics are not established. Do not filter, group, or branch on it without external documentation.

**`CLASSIFICATION_TYPE` values — guess.** The three permitted single letters look like classification markings, with the example's value presumably meaning unclassified. That is a guess from the letters alone. What the other two mean, and whether a consumer is obliged to handle them differently, is not determined. The operationally relevant fact, which *is* established, is that the enum permits three values, so a stream can contain a mix and any pipeline must decide what to do with the non-example ones rather than assuming uniformity.

**`ELEMENT_SET_NO` semantics — declining.** It is a non-negative integer; the example carries 999. Whether it increments per revision, whether it is unique within an object, whether it wraps, and whether a higher value supersedes a lower one are all undetermined. My working assumption would be that it distinguishes successive element sets, so it is a candidate tiebreaker between records sharing an epoch — but that is an assumption and I would validate it before deduplicating on it. Using `CREATION_DATE` as the tiebreaker instead relies only on what the files establish about that field's meaning.

**Whether `CREATION_DATE` always follows `EPOCH` — declining.** In the one example it does, by under two hours. Nothing forbids a record whose epoch lies in the future relative to its creation, and such records would be predictions rather than fits. Do not build latency monitoring that assumes a non-negative difference without checking.

**Absent versus null.** Both the name and the launch designator are optional *and* nullable, so each has two distinct forms of "no value" and the files give no rule distinguishing them. Whether an explicit null carries different meaning from omission is not determined; I would treat them identically and record that as a decision.

**Identity and joins.** The catalogue number is the only required identifier and is therefore the join key. The object name is neither required nor non-null, and nothing in the files says it is stable across records for the same object — so keying, grouping, or labelling on the name will produce wrong or fragmented results. Whether the catalogue number is stable over an object's lifetime is itself not established by the files, though nothing in them suggests otherwise.

**No uncertainty anywhere — established, not ambiguous, but easy to miss.** No record carries any error estimate, residual, or covariance. Every trend line drawn from this feed is unweighted, and no result derived from it can carry a defensible confidence interval without information from outside these files.

**The record is closed.** Extra members are forbidden at both the top level and inside the epoch object. This means no producer can smuggle in additional context, and it also means any pipeline that expects to receive uncertainty or frame information in a future revision is expecting a schema change, not a field addition.


TRANSCRIPT C

# Orbit mean-element feed — analyst's briefing

## 1. What this feed is

Each record is one **fitted orbit solution for one tracked space object**, valid at one instant. It is not a measurement and not a position report. An orbit-determination process at 18 SPCS consumed surveillance observations taken around a reference instant and solved for a parameter set that, when fed to the SGP4 propagator, reproduces the object's motion. What you receive is the solved parameter set.

Two consequences follow immediately and govern everything below.

First, **the numbers are outputs of a model, not observations of the sky.** Every element carries `derivation: modeled`. The schema says the theory "is the procedure that produced this record" and that the same object fitted under a different theory yields different values. So an element value is only meaningful relative to the theory that produced it, and only when consumed by a propagator implementing that theory. There is no sense in which these are "the object's true orbit" that the feed makes available to you.

Second, **each record is an independent refit, not the next sample of a continuous trace.** New records appear whenever fresh tracking data warrants a refit — several times a day for low-orbit objects, less often for deep-space ones, at no fixed period. The difference between two consecutive records therefore contains both real physical change and fit-to-fit variation, and the feed gives you nothing with which to separate them.

The stream is keyed on `NORAD_CAT_ID`, which the schema marks as the feature of interest and describes as the globally-recognised unique identifier. That is your join key and your only one.

## 2. Analytics worth running

**Per-object element histories.** Group by `NORAD_CAT_ID`, order by epoch, and you have a time series per object. This is the primary structure the feed supports, because the identity key is stable and the epoch is orderable.

**Orbital decay tracking.** `MEAN_MOTION` rises as an orbit lowers — the schema states the correspondence directly (≈15.5 for a low-Earth object, ≈1.0 for geostationary). A monotone rise in `MEAN_MOTION` across a per-object history, corroborated by `BSTAR` and `MEAN_MOTION_DOT`, is the decay signal. Supported because all three are present in every record and referenced to the same epoch.

**Refit-cadence analysis.** `CREATION_DATE` is a plain UTC timestamp and is safely differenced between records. The gap distribution per object is itself informative: the schema ties refit frequency to orbital regime, so cadence is a usable proxy for how closely an object is being tracked. Also supported: fit latency, the interval between the epoch a record describes and the moment it was published — but see the precision caveat in §4.

**Population segmentation at a snapshot.** `MEAN_MOTION`, `INCLINATION` and `ECCENTRICITY` are each referenced to a common external frame (the solar day, Earth's equatorial plane, and a dimensionless ratio respectively), so their distributions across objects are comparable and will separate orbital regimes.

**Launch-cohort grouping.** `OBJECT_ID` decomposes into launch year, launch number within that year, and a piece designator. Records sharing the `YYYY-NNN` prefix came from the same launch. This is the only structure in the feed that relates distinct objects to one another, and it is derivable purely from the stated format.

**Analyst-object segregation.** The `7995xxxxx` catalog-number range identifies analyst objects, which also carry null name and designator. Segregating them matters because they are, per the schema, uncatalogued and have no associated launch — so any analysis keyed on launch metadata must exclude them rather than treat them as missing data.

**Change detection against the model's own prediction.** `MEAN_MOTION_DOT` is the mean motion's first derivative, so the change in `MEAN_MOTION` between two epochs can be compared to what the earlier record predicted. A large residual flags something the fit did not anticipate. The files do **not** let you say what caused it — a manoeuvre, a drag event, and a revised fit are indistinguishable here.

## 3. Combination rules

**Two conditions gate every cross-record comparison of an element.** Records must share a `NORAD_CAT_ID` (they describe the same object), and they must share `MEAN_ELEMENT_THEORY` and `EPHEMERIS_TYPE` (they were produced by the same procedure). Elements from different theories are different quantities that happen to share a name; the schema says so explicitly. Public data is expected to be uniformly SGP4, but that is a property of the source, not a constraint in the schema — check, do not assume.

**Every element is instantaneous** (`phenomenonTimeRelation: instant`). None is an accumulation over an interval. Nothing here may be **summed**, ever. An "average" over a per-object history is a sample mean of irregularly-spaced model outputs, weighted by however often refits happened — it is not a time-average of anything physical, and dense refit periods will dominate it.

**The elements are a coupled set.** The schema says they locate the object jointly and are meaningful only when consumed together by the propagator. Averaging or interpolating element-wise across records yields a tuple that corresponds to no state the model ever produced. Do not do it.

Quantity by quantity:

- **`MEAN_MOTION`** — differenceable and comparable within one object's history (this is the decay signal); comparable in magnitude across objects, since it is a rate against a common day. Not summable. Averaging is a sample mean only.
- **`ECCENTRICITY`** — dimensionless and bounded 0–1, so arithmetically well-behaved. Differenceable within an object. Cross-object aggregation is arithmetically valid but I decline to endorse a physical reading of a population mean; the files supply no basis for one.
- **`INCLINATION`** — 0–180° against Earth's equatorial plane, which is a shared reference, so cross-object comparison is sound. **Not cyclic**: 0° and 180° are distinct states (the schema notes >90° is retrograde), so ordinary subtraction and ordinary arithmetic means are correct here.
- **`RA_OF_ASC_NODE`, `ARG_OF_PERICENTER`, `MEAN_ANOMALY`** — all three are **cyclic on 0–360°**. Plain subtraction is wrong across the wrap: 359° and 1° differ by 2°, not 358°. Differences must be reduced modulo 360 and wrapped to ±180. Arithmetic means are invalid; use a circular mean or do not average at all. This is the single most likely thing to be got wrong.
- **`MEAN_ANOMALY` additionally** — it is a phase that advances a full turn every revolution, and `MEAN_MOTION` tells you the revolution rate. For the example object at ≈15.5 rev/day, consecutive daily epochs are separated by roughly fifteen full wraps. A difference between two mean anomalies is therefore only interpretable **modulo whole revolutions**, and the wrap count is not recoverable from the angle alone. `REV_AT_EPOCH` is what resolves it.
- **`BSTAR`** — the schema calls it a free parameter of the fit rather than a physical property of the object, and says it is physically meaningful only for low-orbit objects and may be zero or negative. Within one object it is a legitimate fit-parameter series, but a change in it means the fit changed, not necessarily that drag changed. Cross-object comparison is not a comparison of a physical property, and pooling zeros contributed by deep-space objects into a population statistic is meaningless. Never summed.
- **`MEAN_MOTION_DOT` / `MEAN_MOTION_DDOT`** — **these are scaled**. The schema states the first is *one half* of dn/dt and the second is *one sixth* of d²n/dt². Using either directly as the derivative introduces a factor-of-two or factor-of-six error. Differenceable within an object; never summed. `MEAN_MOTION_DDOT` is described as almost always zero, so it will usually carry no signal.
- **`REV_AT_EPOCH`** — referenced to each object's own launch, so it is meaningless across objects: never summed, never averaged, never compared between objects. Within one object, the **difference** between two epochs is the revolutions elapsed, and that is the quantity that disambiguates the mean-anomaly wrap.
- **`CREATION_DATE`** — differenceable against another `CREATION_DATE`, both being ordinary UTC timestamps. Comparing it against `EPOCH` crosses time regimes; see §4.
- **`NORAD_CAT_ID`** — an identifier. No arithmetic of any kind. Critically, **do not zero-pad or width-constrain it**: the schema says the five-digit range was exhausted in July 2026 and analyst objects sit in a nine-digit range. Any pipeline assuming five digits will corrupt or drop records.
- **`OBJECT_NAME`, `OBJECT_ID`** — never keys. The schema says the name is mutable and not globally unique, so grouping by name will split one object across a rename and merge distinct objects that share a name. Both may be null, and neither is required, so absence and null-ness are two different signals you may have to distinguish.
- **`ELEMENT_SET_NO`** — a counter modulo 1000 that frequently carries the placeholder 999. It is unusable for ordering, unusable for deduplication, and must not be differenced.
- **`CLASSIFICATION_TYPE`, `ORIGINATOR`, `EPHEMERIS_TYPE`** — categorical. Partition and filter keys only.

The record is closed (`additionalProperties: false`), so no uncertainty or covariance information will ever arrive alongside these values.

## 4. Time

There are two distinct time members with two distinct roles, and conflating them is a standing hazard.

**`EPOCH` is the time axis of the thing described.** It carries the phenomenon time: every element is stated *at* that instant and an SGP4 propagator integrates *from* it. All temporal analysis of the orbit itself is on this axis.

**`CREATION_DATE` is the time axis of the record's availability** — the result time, when the fit became publishable. It follows the epoch, because the fit consumes observations taken up to and around the epoch. It is an ordinary UTC timestamp and behaves normally.

**The epoch axis is not civil time.** It is a year plus a fractional day of that year, with day 1.0 at 00:00 on 1 January, where the fractional part measures a uniform 86400-second day. The regime applies **no leap-second correction**, because that is what the propagation theory assumes. The schema states outright that a position on this axis is not an RFC 3339 civil instant and must not be compared with one without an authoritative conversion, with the discrepancy bounded by the leap seconds accumulated in that year. No such conversion is supplied by these files.

Practical consequences:

- **Order by `ordinal`.** It renders year then zero-padded day at fixed width, most significant first, and the ordering is forward, so lexical string sort is correct across the whole regime without implementing the day arithmetic. Use it.
- **`day_of_year` resets each year.** Differencing it across a year boundary yields a negative number. Elapsed time between epochs must be computed year-aware; within a single year the difference is a count of uniform days, which is the count the theory wants, but is *not* a count of elapsed UTC seconds if a leap second fell between them.
- **The `utc` member is convenience only.** The schema calls it best-effort and explicitly non-authoritative, and it is **not in the required list**, so it may be absent. Never propagate from it and never treat it as the epoch.
- **Publication latency is only approximate.** `CREATION_DATE − EPOCH` crosses the two regimes. At the scale of minutes and hours the answer is usable; at second-level precision it is unsound, and the files do not give you the correction.
- **Cadence is declared irregular.** There is no sampling period. Do not resample, do not assume even spacing, and do not compute rates as if the series were uniform.
- **Epoch order and publication order are not the same ordering** and the files do not guarantee the stream arrives epoch-monotone. Sort explicitly on whichever axis your question is about.

## 5. Ambiguities

**Reference frame for the orientation angles.** `RA_OF_ASC_NODE` is measured from the vernal equinox, but which equinox — of date, or a fixed reference — is not stated. This matters: under an of-date convention the value drifts for reasons unrelated to the orbit, contaminating any long-baseline trend. **Declining to decide.** Resolve it against the propagator implementation before trusting multi-year RAAN trends.

**Exact epoch-to-UTC conversion.** Not supplied. The error bound is characterised only qualitatively. **Declining.** If you need sub-second civil alignment, you must obtain the conversion elsewhere.

**"Solar day" versus "uniform 86400-second day".** `MEAN_MOTION` is defined per *solar* day; the epoch regime counts *uniform 86400-second* days. The files never reconcile the two. For most purposes they are presumably the same day, but the schema does not say so. **Declining** — flagging it because anyone doing precise revolution accounting will need the answer.

**Duplicate records.** Emission is triggered by "a new or refreshed element set," which leaves open whether the same epoch can be republished. If it can, you need a deduplication rule, and `ELEMENT_SET_NO` cannot supply one because of the 999 placeholder. **Declining** — the files do not decide it, and this needs a source-side answer before you build ingestion.

**Whether `REV_AT_EPOCH` ever wraps or resets.** Declared as a non-negative integer with no wrap statement. **Declining.** Do not assume monotonicity across a long history without checking.

**No uncertainty anywhere.** No element carries an accuracy figure, and the record is closed against extra members. You therefore cannot tell whether a difference between two records is a real change or fit noise. **Declining** — this is a hard limit of the feed, not something to estimate from within it.

**Feed completeness.** Whether this covers the whole catalogue or a subset is not stated. **Declining.** Absence of an object is not evidence of anything.

**What counts as "low-Earth orbit"** for the purpose of `BSTAR` being physically meaningful. No threshold is given. **Declining.**

**Whether `MEAN_ELEMENT_THEORY` and `EPHEMERIS_TYPE` are constant in practice.** The prose says public data always carries SGP4 and 0, but the types are an open string and an open integer. **Guess:** they are constant in this feed. Marked as a guess — partition on them anyway, because the cost of the guess being wrong is silently mixing incomparable quantities.

**Whether the null name / null designator and the `7995xxxxx` range identify exactly the same set of objects.** The descriptions point both ways but never state the equivalence. **Guess:** they coincide. Marked as a guess — if you need the analyst/catalogued split to be exact, test it against the data rather than relying on either signal alone.

**Whether `MEAN_MOTION_DOT` and `MEAN_MOTION_DDOT` are actually consumed by the propagator** or are carried forward vestigially. The files describe what they are but not that SGP4 uses them. **Declining.**


TRANSCRIPT D

# Orbit Mean-Element Sets (GP / OMM) — what an analyst needs to know

## 1. What this feed is

Each record is one **fitted orbit solution for one catalogued space object, valid at one instant**. It is not a position, not a measurement, and not a description of the object. It is the output of an orbit-determination process run by the 18th Space Defense Squadron: a set of mean elements that, fed into an SGP4 propagator, reproduces where that object is expected to be.

Three consequences dominate everything else:

- **The numbers are model parameters, not observations.** The schema says so for every element, and for `BSTAR` it goes further — a free parameter of the fit rather than a physical property. A change in a value between two records may be a change in the orbit, a change in the tracking data, or a change in the fit. The feed gives you no way to distinguish these; it carries no covariance, no fit span, no observation count, and it is closed (`additionalProperties: false`), so that information will never arrive in-band.
- **The numbers are only meaningful inside one theory.** `MEAN_ELEMENT_THEORY` is not a label, it is the procedure that produced the record. The schema states plainly that the same object fitted under a different theory yields different element values. Theory is therefore a partition key, not a descriptive field.
- **The feed is a stream of revisions, not a stream of objects.** Records are emitted whenever a new or refreshed element set appears, several times per day for LEO objects, less often for deep-space ones, at no fixed period. The same object appears repeatedly. Any analysis that treats one record as one object will silently over-weight the objects that are re-fitted most often.

## 2. Analyses this stream supports

**Per-object element time series (decay, drift, orbit evolution).** Every element is stamped to an epoch and the object has a stable identifier, so successive records for a fixed `NORAD_CAT_ID` form a genuine time series. Rising `MEAN_MOTION` corresponds to a lowering orbit (the schema gives the qualitative direction and two anchor points, ~15.5 for ISS-class LEO and ~1.0 for geostationary). This is the strongest analysis the feed supports.

**Discontinuity / manoeuvre detection.** Because consecutive element sets for one object are fitted under the same theory to the same reference frame conventions, step changes in the elements between adjacent epochs are detectable. What you *cannot* do from these two files is attribute a discontinuity: the feed contains no manoeuvre flag and no fit-quality indicator, so a step is equally consistent with a burn, a re-fit on sparse data, or an epoch far from the observation arc.

**Fit latency and refresh-cadence monitoring.** Every record carries both the instant it describes (`EPOCH`) and the instant it was produced (`CREATION_DATE`), and the schema states the second follows the first because the fit consumes observations up to and around the epoch. The difference is an operational latency you can chart per object and per orbital regime. Likewise, gaps between successive epochs for one object measure how often the catalogue is refreshing it — which is itself a proxy for tracking coverage.

**Staleness of the catalogue.** For each object, the age of its most recent epoch relative to now is directly computable and is the quantity that decides whether a propagated position is worth trusting. (That a stale epoch degrades propagation accuracy is standard practice but is *not* asserted by these files — treat the accuracy claim as outside assumption; the age itself is fully supported.)

**Population and regime census.** `INCLINATION` and `MEAN_MOTION` together partition the catalogue into recognisable orbital regimes; `OBJECT_ID` encodes launch year, launch number within that year, and piece, so records can be grouped into launches and launch cohorts without any external table. **Precondition:** deduplicate to one record per `NORAD_CAT_ID` first (latest epoch), or the census counts element sets, not objects.

**Catalogue-hygiene and identity analytics.** Null `OBJECT_NAME` / null `OBJECT_ID` marks analyst and unlaunched-provenance objects, and the `7995xxxxx` range of `NORAD_CAT_ID` marks analyst objects. These let you separate the tracked, attributed catalogue from the analyst population — a split that materially changes any population statistic.

**Revolution accounting.** `REV_AT_EPOCH` differenced between two epochs of the same object gives revolutions elapsed, which can be cross-checked against `MEAN_MOTION` integrated over the same interval. Disagreement is a useful integrity signal on either the feed or your own epoch arithmetic.

**What this feed cannot support.** Element-set quality ranking, uncertainty propagation, conjunction screening with error bounds, or any inference about the object's physical properties (size, mass, area) — none of the required inputs are present, and `BSTAR` is explicitly disclaimed as a fit parameter rather than a physical property.

## 3. Combination rules

**Preconditions that gate everything below.** Two records may be compared or differenced element-wise only if they share the same `MEAN_ELEMENT_THEORY` and the same `EPHEMERIS_TYPE`. Mixing theories is not a precision loss, it is a category error — the schema states the values themselves differ under a different theory. Cross-object aggregates additionally require de-duplication to one record per object, for the reason in §2.

**Identifiers — equality only, never arithmetic.**

- `NORAD_CAT_ID` is an integer by encoding, not by meaning. Compare for equality; group by it. Never sum, average, or difference it. Never assume a fixed width: the schema states regular objects passed 100000 on 2026-07-11 and analyst objects live at `7995xxxxx`, up to nine digits. Any five-character parse, `int16`, or zero-padded key format is a live bug. Range membership is meaningful only for the one analyst range the schema names; inferring other ranges is guesswork.
- `OBJECT_NAME` is mutable and not globally unique. It must never be a join key, a grouping key, or a stable label across time. Two records with the same name may be different objects; the same object may change name between records.
- `OBJECT_ID` is a structured identifier. Its launch-year and launch-number fields may be parsed out and grouped or compared; the string as a whole is an identity, not a magnitude. It is nullable, so grouping by launch silently drops analyst objects unless you handle null explicitly.

**Categoricals — partition keys, not data.** `CLASSIFICATION_TYPE`, `ORIGINATOR`, `MEAN_ELEMENT_THEORY`, `EPHEMERIS_TYPE`. Compare for equality; use to filter and partition. Not summable or averageable in any sense beyond counting.

**`ELEMENT_SET_NO` — do not use it as a counter.** It increments modulo 1000 and the originator frequently emits the placeholder `999` (the sample record does exactly this). It therefore cannot be differenced to count how many element sets were issued, cannot be used to order records, and cannot be assumed unique or even informative. Any "did we miss an update?" logic must be built on `EPOCH`, not on this.

**Scalar elements — `MEAN_MOTION`, `ECCENTRICITY`.** Within one object and one theory: comparable, differenceable, and a legitimate time series; a rate of change may be formed by dividing by the epoch interval. Across objects: comparable and rankable (both have the same definition and units for every object), and distributional summaries — median, quantiles, histograms — are meaningful for a de-duplicated population. **Never sum them**: neither has additive semantics, so a total mean motion or total eccentricity is a number with no referent. A cross-object *mean* is arithmetically defined but describes a heterogeneous population, not an orbit; report it only as a population statistic, never as "the average orbit".

**Angles — three of the four wrap; one does not.**

- `RA_OF_ASC_NODE`, `ARG_OF_PERICENTER`, `MEAN_ANOMALY` are cyclic on 0–360°. Plain subtraction is wrong across the wrap: 359° and 1° differ by 2°, not 358°. Differences must be reduced modulo 360 into (−180, 180]; averages require circular statistics, because the arithmetic mean of 359 and 1 is 180 — the diametrically opposite answer. Summing them is meaningless.
- `INCLINATION` is bounded on 0–180° but the files do not describe it as wrapping; treat it as an ordinary bounded linear quantity, differenceable and averageable across a de-duplicated population. Note that inclination alone does not identify an orbital plane — two objects at equal inclination with different `RA_OF_ASC_NODE` are in different planes — so clustering on inclination alone will merge unrelated populations.
- **`MEAN_ANOMALY` deserves a separate prohibition.** It is a phase at epoch that sweeps the full circle once per revolution. Differencing it between two records with different epochs tells you nothing about the orbit; it tells you where in its cycle the object happened to be at each instant. It is usable only after accounting for elapsed time and completed revolutions, i.e. only through the propagator.

**All elements are epoch-referenced.** The schema states that every mean element applies at `EPOCH`. Therefore comparing *any* element across records with different epochs is comparing two states at two different times, and the difference confounds real change with the passage of time. This is acute for `MEAN_ANOMALY`, real for `RA_OF_ASC_NODE` and `ARG_OF_PERICENTER`, and mild-but-present for the rest. The files do not quantify how fast any of these evolve, so the size of the confound is not determined here.

**`BSTAR`.** Dimensioned (inverse Earth radii), may be zero, may be negative — **do not filter zero or negative values as data errors**, the schema declares both legitimate. Because it is a fit parameter and not a property of the object, cross-object comparison compares fits, not drag environments, and a cross-object average is not a meaningful physical quantity. Within one object, its change across epochs is a fit-stability diagnostic. The schema also says it is physically meaningful only for LEO objects, so any interpretation applied to deep-space records is unsupported. Not summable.

**`MEAN_MOTION_DOT` and `MEAN_MOTION_DDOT` — the scale-factor trap.** These are *not* the derivatives. The schema states `MEAN_MOTION_DOT` is one half of dn/dt and `MEAN_MOTION_DDOT` is one sixth of d²n/dt². Anyone plotting them as decay rates, or substituting them into a Taylor expansion, without multiplying by 2 and 6 respectively will be wrong by exactly those factors. Units are rev/day² and rev/day³. Differenceable and comparable within an object and theory; not summable; cross-object averaging is a fit statistic only. Separately: the fitted `MEAN_MOTION_DOT` and a finite difference of `MEAN_MOTION` across two epochs are two different estimates of related quantities — do not treat them as interchangeable or validate one against the other as if they must agree.

**`REV_AT_EPOCH`.** A monotone count for a given object since its own launch. Differencing two epochs of the same object yields revolutions elapsed and is the one arithmetic use that is meaningful. Never compare, sum, or average it **across** objects — objects launched at different times have unrelated counts, so a cross-object statistic measures launch age, not anything about orbits. Whether the counter wraps at some width is **not determined by these files**; validate any difference that comes out negative rather than assuming a wrap size.

**`CREATION_DATE`.** A civil UTC timestamp. Orderable and differenceable against other `CREATION_DATE` values without qualification. Do **not** use it to order the states themselves — it orders publication, not the instants described. Subtracting `EPOCH` from it to get fit latency crosses a time-regime boundary (see §4) and is therefore approximate; that is fine for latency monitoring and not fine for anything fed to a propagator.

**`EPOCH` members.**

- `ordinal` is a string built for lexical sorting, and that is its only combination use — sort with it, never do arithmetic on it. It sorts correctly only among values in the same regime and format.
- `year` and `day_of_year` must be combined **as a pair**. `day_of_year` is only comparable within a single year; differencing day numbers across a year boundary without adding the intervening year length is a straightforward off-by-365 error.
- Intervals computed from `year`/`day_of_year` are in **uniform 86400-second days with no leap-second correction**. This is exactly what SGP4 wants, and it is the correct basis for propagation intervals. It is *not* identical to an elapsed UTC interval if a leap second falls inside the span.
- `utc` is declared best-effort and explicitly non-authoritative, and it is **not in the required set** — a record may legally omit it. Code that reads `EPOCH.utc` unconditionally will fail on a conforming record. Use it for display and for loose joins to civil-time data; never for propagation, and never as the basis of a propagation interval when `year`/`day_of_year` are available.

## 4. Time

The feed carries **two independent time axes, and they answer different questions.**

The time axis **of the thing described** — the orbit state — is `EPOCH`. Every element in the record is a value *at* that instant, and it is the instant from which a propagator integrates. Its authoritative representation is the `(year, day_of_year)` pair, where day 1.0 is 00:00 on 1 January and the fractional part is the elapsed fraction of a uniform 86400-second day. The `ordinal` string is the same position rendered most-significant-first at fixed width so that it can be ordered lexically without implementing the regime.

`CREATION_DATE` is the time axis **of the record**, not of the state. It answers "when did this become available", and the schema notes it follows `EPOCH` because the fit consumes observations taken up to and around the epoch. Ordering a per-object series by `CREATION_DATE` is not guaranteed to produce the same order as ordering by `EPOCH`, and only the latter is the physical timeline. In the sample record the creation is roughly an hour and three-quarters after the epoch.

**How epoch positions relate to civil time.** They relate *only* through the feeder's normalisation in `EPOCH.utc`, and that link is explicitly declared best-effort and non-authoritative. The epoch regime counts uniform days and applies no leap-second correction, so it is not an RFC 3339 civil timestamp and must not be read as one. The practical rule:

- **Ordering, interval arithmetic, propagation** → use `ordinal` (ordering) and `year` + `day_of_year` (arithmetic).
- **Display, and joining to civil-time data such as ground events or telemetry** → use `utc`, accepting an approximation, and handle its absence.

The magnitude of the discrepancy between the two axes is **not stated by these files** and I decline to quantify it. What the files do establish is the direction of the hazard: the divergence is a property of leap seconds inserted within the relevant span, so a naive UTC-based propagation interval will be wrong by a small, discrete, era-dependent amount rather than drifting continuously.

One consistency observation from the single record available: `2026/211.76644861` converts, on a plain uniform-day reading, to 30 July 2026 at 18:23:41.160 — which is exactly what `utc` carries. So in this instance the normalisation is a straight uniform-day conversion, agreeing to the millisecond. **One record cannot establish that this holds in general**, and the schema's disclaimer stands; treat the agreement as a data point, not a rule.

## 5. Ambiguities

**Reference frame of the angles — declining to decide, and this is the most consequential gap.** The schema says `RA_OF_ASC_NODE` is measured from the vernal equinox and `INCLINATION` from Earth's equatorial plane, but never states *which* equator and equinox — of date, of a standard epoch, or the propagator's own working frame. Nothing in the two files determines it. Anyone converting these elements to inertial or Earth-fixed coordinates needs this and must obtain it elsewhere; getting it wrong produces a plausible-looking answer that is quietly rotated.

**Record identity and duplicate handling — declining.** `NORAD_CAT_ID` identifies the *object*, not the element set, and nothing in the files supplies a key for the record. `(NORAD_CAT_ID, EPOCH.ordinal)` is the obvious candidate and is my **assumption**, but the files do not state that two element sets for one object cannot share an epoch, and `ELEMENT_SET_NO` cannot break the tie because of the `999` placeholder. Relatedly, the phrase "new or refreshed element set" leaves open whether an identical record can be re-emitted, whether records can arrive out of epoch order, and whether an element set can be superseded or retracted. All three are undetermined; a consumer should be built to be idempotent on the assumed key.

**Whether the feed is ever anything but public SGP4 data — declining.** `MEAN_ELEMENT_THEORY` and `ORIGINATOR` are open strings, `EPHEMERIS_TYPE` is an open integer, and `CLASSIFICATION_TYPE` permits `C` and `S` while the description says public data is always `U`. The descriptions state what public GP data *carries*; the types permit more. Treat all four as variable and partition on them rather than asserting constants — but which other values actually occur is not determined.

**Whether `REV_AT_EPOCH` wraps, and at what width — declining.** Not addressed. Difference computations should validate rather than assume.

**Fit provenance and quality — determined to be absent.** No covariance, no fit span, no observation count or arc length, no manoeuvre flag, no data-source indicator. Combined with `additionalProperties: false`, this is not a gap that a richer producer could fill in-band. Any quality-weighted analysis is out of scope for this feed.

**Derived quantities.** Orbital period is derivable definitionally — `MEAN_MOTION` is revolutions per solar day, so the period is 1440 / `MEAN_MOTION` minutes (≈92.9 minutes for the sample record). Altitude and semi-major axis are **not** derivable: the conversion needs a gravitational parameter and an Earth-radius convention that the files do not supply. The schema gives only a qualitative direction and two anchor values. Treat any altitude figure computed from this feed alone as importing an outside constant.

**`BSTAR` normalisation — noted, undetermined.** Units are inverse Earth radii, but which Earth-radius value defines that unit is not stated. This matters for cross-tool comparison, not for internal time-series work.

**Analyst-object detection — partly a guess.** The schema names `7995xxxxx` for analyst objects and says `OBJECT_NAME` and `OBJECT_ID` may be null for analyst / unlaunched-provenance objects, but it does not say the two nulls always co-occur, nor that the named range is the only analyst range. Any classifier built on these is a **heuristic**, not a determined rule.

**`OBJECT_ID` shape.** The declared pattern permits a zero-length piece designator, so a value like `1998-067` would validate. Whether such values actually occur is not determined; parsers should tolerate it rather than assume at least one trailing letter.

**"The bridge".** The schema attributes emission to a bridge component whose latency, ordering, and loss characteristics are nowhere described. Delivery-order and at-least-once/at-most-once semantics are undetermined.
