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
