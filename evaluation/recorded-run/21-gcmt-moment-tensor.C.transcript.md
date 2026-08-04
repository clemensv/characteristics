# 1. What this feed is

Each record is one published *solution* for one earthquake: a moment tensor obtained by inversion, together with the place, depth and time at which the moment release is centred. The records come from the Global CMT catalogue and are a transcription of that catalogue's fixed-column `ndk` records into named members.

The important framing point — and the one most likely to be missed — is that a record is **not an observation of an earthquake**. It is the output of a fitting procedure, and several of its members are results of that fit, not measurements: the location, the depth and the time are all inversion products, and they are explicitly stated to differ from the hypocentre location and time, which come from a *different* catalogue and are not carried here. The name is a stable identifier for the solution, and its leading letter encodes which data classes went into the inversion (body, surface, mantle, or a combination), so the identifier doubles as a method covariate.

The record is also a *reduced* transcription. The source catalogue publishes an estimated standard error beside every tensor component; none of them are here. It also publishes the hypocentre time and the centroid offset separately; only their sum is here. Anything that needs uncertainties, or needs the offset, has to go back to the `ndk` source.

# 2. Analytics worth running

**Where and how deep moment is released.** Centroid coordinates plus a scalar size measure support mapping and depth profiling directly. Depth has a stated true zero (the surface) and a stated positive sense (downwards), so depth differences and depth histograms are well defined — subject to the conditioning in the next section.

**Moment release totalled over time and space.** The time member is an absolute instant and the scalar moment is on a ratio scale with a true zero, so summing moment inside spatial or temporal bins is a meaningful aggregate. This is the natural way to turn an event list into a rate, and it is the only way, because the series has no period (see §4) and so cannot be differenced or interpolated as a regular time series.

**Size distribution.** Scalar moment is comparable across records without qualification, because it is stated to be frame-invariant. Counting events above moment thresholds, or fitting the upper tail, is supported by the data as given. What is *not* supported from these two files is any statement about detection completeness — nothing here establishes a threshold below which the catalogue stops being a census, so a threshold you choose is an assumption you are making, not one the data justifies.

**Mechanism comparison.** Dividing the six components by the scalar moment yields a dimensionless tensor that separates size from geometry — legitimate, since both are on the same unit. This is worth doing, but it is the analysis with the most traps in it (§3).

**Stratification by inversion input and by depth treatment.** The leading letter of the name and the depth-type member are the only quality/method covariates present. Any headline result should be recomputed within each stratum; if the answer moves with the inversion inputs or with whether depth was free, the result is partly an artefact of processing.

**Constraint audits as a data-quality screen.** Two cheap checks fall out of what the schema states. First, the three diagonal components should sum to zero, because the catalogue applies that constraint "by default" — the word *default* implies exceptions, and finding them tells you which records were treated differently. In the example record the sum is exactly zero (0.838 − 0.005 − 0.833 = 0.000, in units of 10²³). Second, the scalar moment is stated to be a function of the six components, so it should be recomputable; records that depart from whatever function you fit are worth inspecting. Note the caveat in §5 — I could not recover the function from these files, and the obvious candidate does not reproduce the published value.

**Detecting artificially-zeroed components.** Two of the off-diagonal components are held at zero for very shallow earthquakes, and the flag that marks this (a zero standard error) is absent from this record. Exact zeros in *both* of those members are therefore a usable heuristic for "this solution was constrained, not measured". I mark this as a heuristic, not a rule: the files do not say the constrained case is the only way those members can be exactly zero.

# 3. Combination rules

**The six tensor components — the critical case.** These must **not** be compared, differenced, summed or averaged across records at different centroid locations. The axes are named as *up*, *south* and *east*. Those are directions defined relative to a point on the Earth, so the frame rotates from event to event; two records at different coordinates express their tensors in different bases and their components are not commensurable. The schema corroborates this from the other side when it says the scalar moment "is invariant under a change of frame where the six components are not." (This conclusion is an inference — from the axis naming plus the presence of per-record coordinates — rather than a sentence the files state outright. It is the single largest failure mode for anyone stacking these records into a matrix.)

Component-wise arithmetic *is* valid between records at the same location, and is valid more generally only after an explicit rotation into a common frame. Such a rotation is computable in principle from the latitude and longitude each record carries, but see §5: the files do not fix whether "up" is the ellipsoid normal or the geocentric radial direction, and that choice changes the result.

Three further constraints on these six:

- The three diagonal components carry only two degrees of freedom under the imposed zero-trace constraint. Do not feed all three into a model as independent inputs; the design matrix is singular by construction. Equally, do not read a near-zero trace as an empirical finding — it was imposed, not measured.
- Only six values are published for nine positions because the tensor is symmetric. Reconstructing the full array requires mirroring the three off-diagonal values; loading six numbers into nine slots without mirroring silently produces a different tensor.
- The scalar moment is a function of these six. Do not use it as an independent feature alongside them.

**Scalar moment.** Comparable across records and, per the schema, the correct member to compare across catalogues that disagree about the frame. Ratio scale with a true zero, so ratios are meaningful. Summing is defensible as an aggregate of released moment; be aware that the sum of scalar moments is not guaranteed to equal the same scalar function applied to a summed tensor, and since the files do not state that function you cannot check. Averaging is arithmetically valid but the files establish nothing about the distribution, so report totals and quantiles rather than relying on a mean.

**Units.** The moment members are annotated dyne-centimetres, which is CGS. Combining these values with any source on newton-metres without conversion is wrong by seven orders of magnitude. The conversion factor is elementary unit arithmetic, not something these files supply; they supply only the unit annotation, which must be honoured. No magnitude scale is defined here, so do not convert to a magnitude — the relation is not in the files.

**Centroid depth.** Ratio scale, kilometres, positive downwards, floor at zero. Differences and averages are meaningful in kilometres. Two conditions. First, condition on the depth-type member: a depth that was held fixed is stated to carry no information from the inversion, so it must be excluded from, or flagged in, any depth statistic — otherwise the distribution acquires spikes at whatever preset values were imposed. Second, depth must **not** be differenced against ellipsoidal heights, elevations or terrain models: the schema states plainly that depth is outside the record's coordinate reference system, that that system has no vertical axis at all, and that depth runs in the opposite sense to ellipsoidal height. Which surface depth is measured from is not stated (§5), so there is no vertical datum here to align to.

**Latitude and longitude.** Comparable; equality and proximity tests are fine. Plain differencing and plain averaging are unsafe in the usual ways — longitude wraps, and the arithmetic mean of scattered angular coordinates is not a position on the sphere. Summing is meaningless. These two are the only members inside the stated coordinate reference system; do not assemble them with depth into a three-component coordinate.

**Centroid time.** Differences are meaningful and yield durations. Sums are meaningless. Comparison across records is unambiguous because the instants are absolute. See §4 for what the axis will and will not support.

**Half duration.** Seconds, ratio scale, arithmetically combinable — but analytically it is not data. The schema states it is *assumed* from an empirical relationship with the scalar moment rather than derived from the inversion. It is therefore a deterministic re-expression of the scalar moment and carries no independent information. Regressing it against moment recovers the assumed relation; correlating it with anything else is correlating moment with that thing under another name.

**Depth type.** Nominal. Group-by and filter only; no ordering, no arithmetic.

**Event name.** Nominal identifier; equality only. Do not sort by it to obtain time order — the leading character encodes the inversion inputs, not time, so a lexical sort orders by method first. Do not parse the embedded date-time out of it either; use the time member, and see §5.

**Missingness.** All members except depth type and half duration are required, so only those two need absent-value handling. Absence of the depth type should be treated as *unknown*, not as *free* — nothing in the files licenses that default.

# 4. Time

The centroid time member is the time axis. It is the instant about which moment release is centred, and it is formed by adding the catalogue's centroid offset to a hypocentre reference time that this record does not carry — so the offset itself, which is a quantity of interest, cannot be recovered from a record alone.

It is *not* the time rupture began. Differencing it against an origin-time catalogue produces a real physical offset, not a clock discrepancy or a data error.

Position on the axis relates to civil time directly: the instants are absolute and, in the example, carry a zero UTC offset, so they map onto civil time without any zone assumption. Local civil time at the epicentre is neither carried nor derivable — time zones are political boundaries and no zone information is present. (You could compute a local *solar* time from longitude; that is geometry, but it is an import from outside these files and it is not civil time.)

Two properties of the axis constrain what can be done on it:

*It is not a sampled series.* The schema is explicit that successive values carry no period. There is no sampling interval, so there is nothing to resample, interpolate or lag-difference. Rates must come from aggregation into bins or from point-process treatment. Nothing establishes that records arrive in time order.

*The values are not instantaneous.* The tensor is stated not to describe an instant: the solution integrates release over a source duration, whose scale is set by the half duration. The centroid time is a centre of that release, not a sample at a moment. Practically, treating an event as a point in time is safe at any bin width far larger than the half duration — 0.6 s in the example — and unsafe below it. That the release interval is symmetric about the centroid time, i.e. spans roughly the centroid time plus or minus one half duration, is a **guess**: it follows from combining "centred" with "half the duration", but the files do not state it, and for records where the half duration is absent the extent is simply unknown.

Finally, a gap on this axis is not interpretable from these files. Nothing here establishes a detection threshold or a completeness criterion, so an empty interval could mean no earthquakes or no solutions, and you cannot tell which.

# 5. Ambiguities

**Which function of the tensor produces the scalar moment — not determined; I decline to name it.** The schema says only that it is a function of the components. This matters because it is stated to add no independent information, which invites a consistency check. I ran the obvious candidate on the example record — the root-sum-of-squares over all nine positions, divided by the square root of two — and got 1.392 × 10²³ against a published 1.312 × 10²³, about six per cent apart. Either that is not the function, or something in this record is internally inconsistent. The files do not decide it, and I will not pick.

**The reference surface for depth — not determined; declining.** "Downwards from the surface" does not say which surface. The schema removes depth from the coordinate reference system explicitly, so there is no vertical datum to fall back on. This is inconsequential for the 162.8 km example and consequential for anything shallow or marine.

**Whether "up" means the ellipsoid normal or the geocentric radial direction — not determined; declining.** This is the missing piece needed to rotate tensors into a common frame, which is the operation §3 says you must perform before combining components across locations. Whatever you assume, document it; the assumption is yours, not the catalogue's.

**The meaning of the third depth-type category — not determined; declining.** The schema characterises only the free and fixed cases. Whether the third should be pooled with fixed, with free, or kept separate is not decidable here; keep it separate.

**How shallow "very shallow" is — not determined; declining.** This is the depth below which two off-diagonal components are held at zero rather than estimated. Without a number you cannot construct a depth filter, and because the affected records concentrate at one end of the depth range, the contamination is correlated with exactly the variable most depth-dependent analyses use. The exact-zero heuristic in §2 is a workaround, not a substitute.

**Whether the record can be trusted to distinguish a constrained zero from an estimated zero — it cannot.** The flag that does so upstream (a zero standard error) is stated to be absent from this record. This is not an ambiguity in the files so much as a known, stated loss.

**The trailing character of the event name — not determined.** *Guess:* it disambiguates solutions that would otherwise share the same minute. Marked as a guess; nothing in the files supports it.

**Which time is embedded in the name — not determined.** The digits agree with the centroid time to the minute in the example, but since the centroid time is a reference time plus an offset, the two can straddle a minute boundary. Use the time member and never the name.

**Whether older records use the current name form — the schema says "current events" use the fourteen-character form, which implies others do not.** Do not write fixed-width parsers against the name across a whole catalogue.

**Identity and revision semantics — not determined; declining.** Nothing says whether one physical earthquake can appear as more than one record, whether re-inversions replace or accompany earlier solutions, or how the catalogue version of a record could be established. There is no source, version or processing-time member. Deduplicating on the name is safe; concluding that two names are two earthquakes is not.

**Precision of the time values — not determined.** The example carries a tenth of a second; whether that resolution is uniform across the feed is not stated, so do not read it as an uncertainty.

**The coordinate reference system annotation.** The schema's prose refers to an EPSG:4326 annotation on the record, and I take the horizontal coordinates to be WGS 84 geographic degrees on that basis. I note that the annotation is asserted in prose rather than visible as a declared unit on the two coordinate members themselves, so the degree unit rests entirely on that reference — an **inference**, though a low-risk one, and consistent with the example's values.

**One thing that is *not* ambiguous, and is worth stating because sign errors are the classic failure here:** the axis triple as named — up, south, east — is right-handed, since up crossed into south gives east. There is no hidden reflection in the naming to compensate for.
