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
