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
