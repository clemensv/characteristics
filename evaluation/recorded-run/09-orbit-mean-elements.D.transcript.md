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
