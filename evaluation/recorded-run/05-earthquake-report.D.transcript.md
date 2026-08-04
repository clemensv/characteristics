# Earthquake report feed — analyst's briefing

## 1. What this feed is

Each record is a **bulletin about an earthquake, not an earthquake**. It is one revision of an official Japanese seismological report: a statement, issued at a particular moment by a publishing agency, of where and how large an earthquake was and how strongly the ground shook in the places that observed it.

The same earthquake generates many records. They are tied together by a stable event identifier and ordered by a serial number that marks the revision sequence. A record also declares its own standing in that sequence — a fresh issue, a correction of an earlier issue, or a cancellation.

The physical content of a record is a *computed solution*, not a set of instrument readings. The hypocentre (latitude, longitude, depth) is obtained by inverting arrival times across a national seismograph network. The magnitude is obtained by applying a published formula to displacement amplitudes across that network. The headline shaking value, and each per-prefecture shaking value, is a **maximum taken over the stations that contributed** — a statistic over observations, not a reading. Nothing in a record is a direct measurement of anything.

One further piece of the physical content is not published at all but *inferred*: the tsunami flag is the bridge's reading of free-text commentary, described in the source material as an estimate of the bulletin's intent. Tsunami-specific products are explicitly excluded from this feed.

## 2. Analytics worth running

**Solution convergence within an event.** Group by event identifier, order by serial, and watch the hypocentre and magnitude move. This is the single most defensible analysis here, because the event identifier is stated to be stable across bulletins and the serial is stated to define the revision sequence. It answers: how far does an epicentre migrate between the first and final bulletin? How much does magnitude move? Does depth move more than the horizontal position?

**Publication latency, decomposed.** Three distinct instants are recorded, with three stated and different meanings: when the rupture began, when the solution became available, and when the finished bulletin was handed to the distribution channel. Their differences are two separate latencies — *time to solution* and *time to distribution* — and confusing them is a common error. Both are worth tracking by revision number and by product code.

**Revision and retraction behaviour.** How often does an event receive a correction? How often a cancellation? At which serial does that usually happen? Supported directly by the standing field's three-valued meaning.

**Magnitude–depth–shaking relationship.** The strength of shaking against magnitude and depth is a classic attenuation question, and this feed carries all three per event. It must be modelled as **ordinal** in the shaking variable (see §3), which means ordered-categorical methods, not regression on a numeric shindo.

**Shaking footprint breadth.** The number of prefectures that reported shaking, and the distribution of their per-prefecture maxima, is a crude but real proxy for how far the shaking propagated. It supports comparison against magnitude and depth. It is a count of reporting units, not an area and not a population.

**Spatial and depth clustering of seismicity.** Coordinates are stated to be WGS84 decimal degrees with depth in kilometres, so hypocentres are directly plottable and inter-hypocentre distances are computable. Cluster by source region, stratify by depth band.

**Feed quality monitoring.** A substantial and named class of bulletins arrives with no hypocentre, no magnitude, and no English title. Measuring the share of such records, and the share where the tsunami inference came back unknown, tells you how much of the feed is actually usable for the analyses above.

**Event rate as a point process.** Legitimate, but only as a point process — see §4 on why it is not a time series.

## 3. Combination rules

**Shaking intensity — headline and per-prefecture.** This is an **ordinal scale with tied-but-distinct steps**: consecutive levels include lower and upper subdivisions of the same numeral. Values **may be compared and ordered**, and maxima and minima are meaningful — the feed itself is built on taking maxima over stations, which presupposes a total order. Values may **not** be summed, differenced, or averaged, under any condition. The gap between adjacent levels is not a defined quantity, so a "mean intensity" or an "intensity delta" is not a number about the world. Use medians, modes, maxima, and rank methods. Do not encode the levels as 1…9 and then do arithmetic on the encoding.

**Magnitude.** Values are on one named agency scale and **may be compared** across records — subject to the maturity condition below. They may **not be summed**, and the files do not establish that the numeric spacing is uniform, so **differences and averages are not licensed either**. The scale is described as the output of a formula that is not given here; without knowing that formula's structure you cannot claim that a step from 4.0 to 5.0 is the same quantity of anything as a step from 6.0 to 7.0. Treat magnitude as an ordered scale value, not an interval quantity. The material also hedges that the scale resembles the familiar one *for shallow events*, which means any cross-scale intuition you carry should not be applied uniformly across depths.

**Latitude, longitude, depth.** These three are **components of one joint solution** and must move together. You may not take the horizontal position from one bulletin and the depth from another, nor from a different revision of the same event — they are outputs of a single inversion and mixing them yields a point that no solution ever asserted. Across records, coordinates share a stated datum, so **distances and differences between hypocentres are meaningful**. Averaging coordinates across revisions of *one* event is not an improvement of the estimate; the later revision supersedes the earlier one, and the mean of a superseded and a current solution is neither. Averaging coordinates across *different* events yields a centroid, which is a legitimate summary of a cluster but is not a place where anything happened.

**Depth specifically.** Depth is derived by taking an absolute value, so it carries no sign and cannot express elevation above datum. It is bounded and non-negative by construction.

**The maturity condition, which governs magnitude and hypocentre alike.** The product code is described as *the scale on which the maturity of the solution is expressed* — it qualifies the results rather than being a result. Two solutions carried under different product codes are therefore **not on the same footing**, and pooling them without stratifying mixes preliminary and refined estimates into one distribution. Always stratify by product code, or restrict to a single code, before summarising magnitudes or hypocentre scatter. Note carefully: the files establish *that* maturity is expressed there but **do not establish the ordering** — you can group by it, you cannot rank by it. Ordering of revisions comes from the serial number, which is explicitly a revision sequence.

**Timestamps.** All three are instants on a single common absolute axis, so **any two of them may be differenced**, and those differences are durations in the ordinary sense. But they are **not interchangeable**, and substituting one for another silently changes what your analysis is about. Averaging timestamps across records is not meaningful; averaging *differences* between them is.

**Serial number.** Ordinal within one event identifier only. Comparing serial numbers across different events is meaningless — a serial 3 of one earthquake and a serial 3 of another share nothing.

**Region and prefecture codes.** These are **two different code spaces**. The source-region code names the seismic source area; the prefecture codes name administrative units that observed shaking. They come from different source fields and must not be joined to each other, matched against each other, or pooled into one dimension — in the sample record the source region is an offshore area whose code appears in neither of the prefecture code values. Both are opaque without an external lookup table; counting distinct codes is fine, interpreting them is not.

**The tsunami flag.** Three-valued, and the third value means *unknown*, not *no*. Collapsing unknown into false will systematically understate. Because the value is an inference over free text rather than a published coded field, it may be **counted and cross-tabulated with the appropriate caveat, but must never be treated as authoritative** and must never drive an operational or safety decision. The feed also excludes the dedicated tsunami products entirely, so it is structurally incapable of being a tsunami source.

**Counting.** Do not count records to count earthquakes. Deduplicate to one record per event identifier — normally the highest serial — before any per-earthquake statistic. Every record-level count is a count of bulletins.

**Missingness.** Absence is encoded two different ways in this feed: some quantities are set to a null value when unavailable, others are simply left out of the record. A consumer that only tests for null will silently mis-handle the omitted ones, and one that only tests for presence will treat null as a value. Test for both.

## 4. Time

**The time axis of the thing described is the origin time** — the instant at which rupture began. That is the phenomenon time, and it is the correct axis against which the hypocentre, magnitude, and intensity results should be read, because those results are all statements about the event that started then.

The other two instants belong to the **observing and publishing system**, not to the phenomenon: one records when the solution became available, the other when the finished bulletin was handed into the distribution channel. Plotting seismicity against either of these gives you the behaviour of the agency's pipeline, not the behaviour of the earth.

**Positions on the axis are instants, not intervals.** The origin time marks the *beginning* of rupture; no duration or extent is carried, so an earthquake in this feed has a start and no modelled end.

**There is no period and no sampling rate.** The material states plainly that earthquakes are not scheduled and that successive origin times carry no period. Consequences: this is a point process, not a time series. Do not resample it onto a regular grid, do not interpolate between events, do not treat a quiet stretch as missing data, and do not compute a "rate" by averaging inter-arrival times without a point-process treatment. Gaps are the signal.

**Relation to civil time.** All three timestamps are recorded on an absolute, offset-free basis, having been converted from Japanese local time at ingest. This makes them directly comparable and differenceable without any timezone reasoning — which is exactly what you want for latency work.

It also means that **any analysis involving time of day is not directly supported.** Diurnal patterns, working-hours effects, day-versus-night response — all of these are questions about Japanese civil time, and the files establish that the source was a local clock but **do not state the numeric offset from it**. To go back to civil time you must supply that offset from outside these files. I am not deriving it here; treating it as a fixed nine-hour shift is an assumption I am flagging as coming from outside the material, and it additionally assumes the offset is constant, which is also not established.

**Ordering between the three instants is expected but not guaranteed.** The stated meanings imply origin precedes availability precedes distribution, and the sample record is consistent with that, but no constraint in the material enforces it. Check it rather than assume it, and treat violations as data-quality events.

**Do not parse the event identifier as a timestamp.** See §5.

## 5. Ambiguities

**Which clock the event identifier is on — declining to decide.** The identifier is described as the origin time in compact form, while the origin timestamp is described as a conversion to an offset-free absolute time. If the identifier is on the local clock these two should disagree by the local offset; in the sample record they agree exactly, digit for digit. One of the two readings must be wrong and the material does not say which. **Practical instruction: do not parse the identifier as a time. Use the origin timestamp.**

**The trailing sequence number in the detail link does not match the serial** in the sample record — the link ends in 1 where the serial is 2. Whether the link embeds a different counter, a different product's serial, or is simply inconsistent here, the files do not say. **Declining to decide.** Do not use the link to recover the revision number.

**Whether the report identifier is globally unique.** It is formed from the event identifier and the serial, and is described as distinguishing bulletins for one event. Nothing establishes that two *different product codes* for the same event cannot both carry the same serial, which would collide. **Declining to decide** — verify uniqueness empirically before using it as a primary key, and be prepared to key on event, serial, and product code together.

**Whether the headline shaking value always equals the maximum of the per-prefecture values.** They are drawn from different source fields, described independently. The sample record is consistent, but consistency is not asserted. **Declining to decide.** Do not derive one from the other; carry both and treat a disagreement as informative.

**What a cancellation implies for the data it carries and for prior bulletins.** The standing field is described only as the bulletin's position in the revision sequence. Whether a cancelling bulletin still carries a hypocentre, and whether it retracts the preceding solution or supersedes it with nothing, is not stated. **Declining to decide** — but exclude cancelled events from seismicity statistics until you know, since including a retracted event is the more damaging error.

**The ordering of the product codes by maturity.** Established that they express maturity; not established which is more mature than which. One code in the permitted set has a different prefix from the rest, and its relation to the others is unexplained. **Declining to decide.** Stratify, do not rank.

**The meaning of every code value** — source region and prefecture alike. These are opaque identifiers with no accompanying table. **Declining to decide.** Do not assume they correspond to any standard national or international code list; obtain the authoritative table or leave them as opaque keys.

**Uncertainty on every computed quantity.** No error ellipse for the hypocentre, no depth uncertainty, no magnitude uncertainty, no indication of whether depth was free or fixed in the inversion. **Not determined.** This is the most consequential gap: you can measure how much a solution *moved* between revisions, but you cannot say whether any two solutions *differ significantly*, and you cannot put a confidence region on any epicentre.

**Whether serial numbers are monotonic and gapless.** Described as a revision sequence with a lower bound of zero. **Guess, marked as a guess:** they increase within an event and may skip values. Do not rely on "serial equals count of prior bulletins", and select the latest revision by maximum serial rather than by an assumed final value.

**Whether the prefecture list can be empty.** It is a required member. **Guess, marked as a guess:** an empty list is emitted for bulletins with no observed shaking, which is the same class of bulletin that omits the hypocentre. Code defensively for the empty case regardless.

**Feed completeness.** Tsunami products are stated to be excluded, so the feed is not a complete record of the agency's output. Whether it is a complete record of *earthquake* bulletins, whether there is a magnitude or intensity threshold below which nothing is published, and what the retention window is, are all **not determined**. Without a completeness threshold you cannot compute a magnitude–frequency distribution or claim any catalogue is complete above a given magnitude.

**Whether the shaking scale's lowest published level is a floor or a threshold.** The permitted levels begin at 1, with no level for imperceptible shaking. Whether events felt below that level are reported with the member absent, or not reported at all, is **not determined** — which matters directly for any attenuation or footprint analysis, since it decides whether an absent prefecture means "no shaking" or "not observed".

**Precision and rounding of magnitude and coordinates.** Not stated. Do not infer significant figures from the sample.
