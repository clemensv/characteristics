# Reading the feed

## 1. What this feed is

Each record is a **point-in-time report of where one identified mobile unit was and how it was moving**, as received by whatever collected the feed. A record binds an integer identity to a coordinate pair, a reception instant, a small set of quality/validity flags, and — when present — a speed, a course, and a heading. A further group of booleans describes the *reporting device and its operating mode* rather than anything about the world.

The stream is therefore a **sequence of independent samples, not a continuous track**. Nothing in the material says a record's state holds until the next record, and nothing states a reporting cadence. A track is something you reconstruct by grouping on the identity and ordering on the reception instant; it is not something the feed gives you.

Only six things are guaranteed to be present: the identity, the reception instant, the undocumented integer `Timestamp`, the `Valid` flag, and the two coordinates. **Everything about motion — speed, course, heading — is optional and may simply be absent.** Any pipeline that assumes motion data is present will silently drop or mis-handle records.

The schema's name and the abbreviations used are strongly suggestive of maritime AIS Class B position reporting. *That is a guess from naming alone.* The files establish no domain, no vessel, no sensor, no platform type, and no issuing authority. I use no domain knowledge below; everything in sections 2–4 stands on the two files.

## 2. Analytics worth running, and why the data supports them

**Track reconstruction per unit.** The identity, a typed instant, and a coordinate pair are all *required*, so every record can be placed on a per-unit timeline without loss. This is the only analysis fully supported by the required members alone. It rests on one unverified assumption: that the identity is stable and unique per physical unit (see §5).

**Spatial occupancy, density, and dwell.** Coordinates are required and never missing, so heat maps, cell counts, and "how many distinct units entered region R" are computable over the whole stream with no coverage bias from optional fields. Note that *density is report-weighted, not unit-weighted*: a unit reporting ten times as often contributes ten times the mass. Deduplicate to distinct identities per cell if you want an occupancy measure rather than a chattiness measure.

**Presence, gaps, and reporting behaviour.** Grouping by identity and differencing consecutive reception instants gives inter-report intervals. This supports gap detection, session/voyage segmentation by silence threshold, and per-unit reporting-rate profiles. It is well supported because both inputs are required. What it does *not* support is calling a gap a real outage: the files do not establish whether this stream is complete or a sample, so a gap may be a collection artefact.

**Data-quality profiling.** The proportion of records with each boolean set, cross-tabulated by unit and by time, is fully supported. The single instance shows `Valid` true while `PositionAccuracy` is false, which demonstrates these are not the same flag and must be profiled separately. This is worth running *first*, because the polarity of these flags is undetermined (§5) and their empirical joint distribution is the only evidence available for interpreting them.

**Presence/absence analysis of the optional members.** Because absence is permitted and `additionalProperties` is closed, the pattern of which optional members appear is itself a signal — it may distinguish device classes, firmware, or upstream decoders. This is supported and cheap. It is also a prerequisite for every motion analysis, since missingness is likely to be non-random.

**Speed distributions and motion-regime segmentation** (stopped / slow / underway), *within this feed only*. Supported for relative comparison and for clustering, because all records in one feed plausibly share one unit of measure. Not supported for any statement in physical units, and not supported for comparison against any external speed source — the unit is not established anywhere.

**Course and heading behaviour**: turn detection, course-change rate, steadiness. Supported provided you treat these as circular quantities (§3). Circular variance of course over a window is a good, well-founded manoeuvre detector here.

**Heading-versus-course divergence** is the analysis analysts most want and the one this material least supports. It requires that the two angles share a reference direction and rotational sense. Only one of them is named "True"; the other's reference is unstated. The single instance has them 2.3 apart, which is consistent with a shared reference but a single record cannot establish it. Treat any drift/set computation as an assumption, and validate it against the population before using it.

**Not supported by these files:** anything about what the units *are* (no type, size, class, name, or voyage data); any latency or end-to-end delay measurement (requires knowing what `Timestamp` is and whose clock `TimeReceived` uses — neither is established); any absolute-speed or absolute-distance claim in named physical units; any fusion with an external positional dataset without first resolving the coordinate reference.

## 3. Combination rules, quantity by quantity

**Identity (`UserID`).** Equality and grouping only. It is a label that happens to be stored as an integer. **Never sum, average, difference, or order it**, and never treat numeric adjacency as relatedness — no numbering scheme is established. Its use as a grouping key assumes uniqueness and temporal stability, neither of which the files state.

**Reception instant (`TimeReceived`).** Compare and order freely. **Difference two of them** to get an elapsed duration — this is the one arithmetic operation on time that is sound here. **Never sum instants.** Averaging is meaningful only as a midpoint, not as a quantity. Differences are trustworthy as *reception* spacing; treating them as the spacing of the underlying events assumes constant delay, which is not established. If more than one receiver contributes to the stream, differences across records from different receivers may not reflect real event spacing at all.

**`Timestamp`.** **Do not combine it with anything.** No unit, no epoch, no origin, no range, no monotonicity, and no wrap behaviour is established. It must not be differenced against `TimeReceived`, summed, or averaged; it must not be used to order records. The instance actively rules out the obvious reading: as seconds since the Unix epoch, the value 7 would place the record in 1970, irreconcilable with the accompanying instant. So the epoch interpretation is *excluded by the material itself*. Equality comparison is the only defensible operation, and even that has no established meaning.

**Coordinates (`Latitude`, `Longitude`).** These are **two components of one quantity and must always travel as a pair**; never combine the latitude of one record with the longitude of another. Within one reference system they may be compared and differenced — but a difference in degrees **is not a distance**. Euclidean distance on raw degrees is wrong everywhere except trivially near the equator, because a degree of longitude shrinks with latitude. Use a geodesic or a projection.

**Do not take a component-wise arithmetic mean to get a "mean position."** Longitude is cyclic and wraps; an arithmetic mean is catastrophically wrong across the wrap and distorted elsewhere. Use a unit-vector (Cartesian) mean, or work in a projected system.

Summing coordinates is meaningless. Comparing or differencing coordinates against *any other data source* requires that both use the same geodetic reference — the files establish none, so cross-source fusion carries an unquantified datum offset. The `double` type also permits far more precision than the source plausibly carries; do not read trailing digits as resolution.

**`Sog` (speed).** Within a single feed it may be compared, differenced, and averaged — **on the assumption that all records share one unit**, which the files do not state but which is the natural reading of a single feed under one schema. It may **not** be combined with speed from any external source without reconciling units; the plausible candidates differ by factors of roughly 1.9 to 3.6, so the error is large and silent.

Two further traps. First, **a plain mean of `Sog` across records is not mean speed over time** unless reports are equally spaced — and spacing is not established. Weight by the interval to the next report if you want a time-average. Second, no "unavailable" sentinel value is documented; if the encoding uses one, it will be an ordinary-looking number that poisons every mean and maximum. Profile the distribution before aggregating.

**`Cog` (course) and `TrueHeading`.** Both are **circular quantities and must not be treated as ordinary numbers.** Specifically:

- **Never take an arithmetic mean.** 350 and 10 average to 180 — the exact opposite of the correct answer. Use the vector mean of unit vectors, or circular statistics.
- **Never sum them.**
- **Difference only modulo the circle**, wrapping to the shortest signed arc in (−180, 180]. A raw subtraction produces spurious 350-unit jumps at every wrap.
- **Ordering comparisons ("greater than") are not meaningful** on a circle. "Within an arc of X" is meaningful; "above 300" is not, unless you mean it as an arc.
- Standard deviation, min, max, median, and linear interpolation are all invalid without circular treatment.

Additionally these two must not be differenced against each other unless you accept the unverified assumption that they share a reference direction and rotational sense. They also differ in stored precision — one integral, one fractional — so their difference inherits the coarser resolution. And the integral one admits values outside a compass range with no documented sentinel; screen for out-of-range values before any circular aggregation, because a single sentinel will drag a vector mean anywhere.

**The boolean flags — `Valid`, `PositionAccuracy`, `Raim`.** These are predicates about a record, not measurements. Use them to filter, and aggregate them only as *proportions over a stated denominator*. Never sum them together — they are not commensurable with one another. Their polarity is not established (§5), so a filter written in the wrong direction will silently keep exactly the records you meant to drop. The single instance shows `Valid` and `PositionAccuracy` disagreeing, so they must never be conflated or used interchangeably.

**The device/mode flags (`AssignedMode` and the `ClassB*` group).** These describe the reporting equipment, not the world. If they are constant per unit — which is plausible but **not established** — then averaging them across *records* produces a report-weighted statistic that says more about which units are chatty than about the population. **Deduplicate to one row per identity before computing any fleet-level proportion over these.** Comparing them record-to-record is fine; summing or averaging over raw records is a trap. As a group they are also not commensurable with each other and must not be summed into a score.

**Absence, across all optional members.** **Do not impute a missing boolean as `false`, and do not impute a missing number as zero.** The schema permits absence and states nothing about its meaning; a missing speed is not a speed of zero, and a missing flag is not a cleared flag. Missing and false must remain distinguishable through the whole pipeline, and every proportion must state whether its denominator is all records or only records where the member was present.

## 4. Time

**`TimeReceived` is the only member that establishes a time axis.** It is the sole member with a temporal type, and the instance carries a UTC designator, so its values are absolute instants — orderable, differenceable into elapsed durations, and convertible to civil time in any zone given that zone's rules.

The critical point, and the thing an analyst will get wrong: **this axis is a reception axis, not an observation axis.** The member's own name places it at the point of receipt. The files nowhere state the delay between the described state holding and the record being received, nor whether that delay is constant, nor whose clock stamped it. Consequences that follow directly:

- Ordering records by this member is ordering by *arrival*. If delays vary — different receivers, different paths, buffering, replay — arrival order need not match the order in which the states actually occurred.
- Interpolating a position between two consecutive instants assumes constant delay across that interval. That assumption is unstated and unverified.
- Cross-unit synchrony ("these two were close at the same moment") is only as good as the assumption that both records suffered the same delay.

**`Timestamp` does not establish a time axis** and must not be used as one. It carries no epoch, unit, origin, or range, and as noted the instance excludes the epoch-seconds reading outright.

On the relation to civil time: with a UTC anchor, each instant maps unambiguously to civil time in any zone. Durations obtained by differencing are **elapsed UTC durations, not wall-clock differences** — across a daylight-saving transition the two disagree by an hour, so bucketing by local hour-of-day requires an explicit zone conversion and must not be done by string slicing. The schema guarantees only that values are instants; it does not guarantee that every record carries the same offset designator as this one, so normalise to UTC on ingest rather than assuming.

Finally, **a record marks an instant, not an interval.** No validity duration or "state held until" is expressed. Any resampling, gap-filling, forward-fill, or "last known position" logic is an interpretation layered on top of the data, and the choice of hold-time is yours, not the feed's.

## 5. Ambiguities

**Declining to decide** — the files do not settle these, and I will not manufacture an answer:

- **The domain.** Nothing states what is being tracked, on what medium, by whom, or under what standard. *Guess, marked as such:* the schema name and the abbreviations suggest maritime AIS Class B position reporting. Nothing in the two files establishes this and I have not used it anywhere above.
- **The unit of `Sog`.** Undetermined. *Guess: knots.* Do not act on that guess; the plausible alternatives differ by nearly a factor of four.
- **The angular unit and reference of `Cog` and `TrueHeading`.** *Guess: degrees,* on the weak evidence that both instance values fall below 360. The reference direction of `Cog` and the rotational sense of both are undetermined; only one member's name asserts a reference at all. Whether the two share a reference — the precondition for any divergence computation — is undetermined.
- **The geodetic reference and unit of the coordinates.** *Guess: decimal degrees.* The datum is entirely undetermined, which is the blocker for fusing this feed with any other spatial dataset. Sign conventions (north-positive, east-positive) are likewise unstated; I assume the conventional ones and flag that as an assumption.
- **The meaning of `Timestamp`.** Undetermined, and I decline to use it. *Guess, marked and not relied upon:* a coarse sub-minute field, given the small value and the presence of a full instant alongside it. That guess is not sufficient to justify any arithmetic.
- **The polarity and referent of every boolean.** Does `PositionAccuracy` true mean *high* accuracy or *low*? Does `Valid` qualify the position, the whole record, or a decode step? What does each `ClassB*` flag assert? All undetermined. Written the wrong way round, these filters invert your dataset without erroring.
- **Identity uniqueness and stability.** Whether one identity maps to exactly one unit, whether it persists over time, and whether it can be reassigned or spoofed. Every per-unit analysis assumes all three. Also unstated: whether identity values can exceed the signed 32-bit range, and what happens if so.
- **The meaning of absence** for the optional members, and whether missingness is random or systematic.
- **Sentinel / "unavailable" encodings** in the numeric members. This is the highest-risk unknown here, because a sentinel is indistinguishable from a real value and will corrupt means, extremes, and circular aggregates without any error surfacing.
- **Reporting cadence, and whether the stream is complete.** Undetermined. Every time-weighted statistic and every gap-based inference depends on it.
- **Whether `TimeReceived` is stamped by a receiver or by the unit, and the delay distribution.** Undetermined; see §4.
- **Deduplication.** Whether one underlying report can appear more than once — for instance via multiple receivers. Undetermined. Undetected duplicates inflate density maps and bias every unweighted aggregate toward whatever is best-covered.
- **Effective coordinate resolution.** The storage type permits far more precision than the source plausibly carries. *Guess:* true resolution is coarser than the stored digits. Do not report positions to full stored precision.
- **Ordering guarantees.** Whether records arrive in reception order, and whether late arrivals occur. Undetermined; sort explicitly rather than trusting arrival order.

**What I would need to resolve these:** a units declaration for the speed and the two angles, a geodetic reference for the coordinates, a definition of `Timestamp`, the polarity and referent of each flag, and a statement of which clock stamps `TimeReceived`. None of it is inferable from one schema and one record, and inferring it would be guessing dressed as analysis.
