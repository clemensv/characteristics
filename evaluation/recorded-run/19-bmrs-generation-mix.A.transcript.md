# 1. What this feed is

Each record is a cross-sectional snapshot of electricity supply on a single power system, broken down by production category and by cross-border link, tagged to a numbered half-hourly-style trading interval and to an instant. One record = one interval; the members within it are the simultaneous contributions of gas-fired plant (combined-cycle and open-cycle), coal, oil, nuclear, wind, biomass, non-pumped hydro, pumped storage, an unspecified residual, and seven named external interconnectors.

The category names and the interconnector names are strongly suggestive of the Great Britain transmission system, but nothing in the two files names a country, an operator, a market, or a source system. Treat the geography as an inference, not a given.

Two things the records are *not*: they are not energy, and they are not demand. The naming convention says megawatts, i.e. a rate; and there is no member for load, price, or emissions. Any statement about MWh, cost, or carbon requires a duration or a factor that this feed does not carry.

The single most consequential absence: **there is no solar member**. Whether solar is folded into the residual, sits outside the measurement boundary (e.g. because it is connected below the transmission system and never metered here), or simply is not published, is not determined. An analyst who sums these members and calls the result "total generation" will be wrong by whatever that boundary excludes, and will be wrong by a different amount at midday than at midnight.

# 2. Analytics

**Mix composition and share over time.** Every record is a complete simultaneous cross-section in one common unit, so within-record shares are computable directly, and the timestamp lets those shares be tracked as a series. Caveat carried from §3: shares are only well-defined once you have decided how to treat negative values and a possibly incomplete denominator.

**Ramp and volatility analysis.** Consecutive records differenced member-by-member give the change in output per interval — the raw material for wind ramp distributions, gas-plant following behaviour, and reserve sizing questions. This works because the member set is stable across records and the interval spacing is recoverable from the timestamps themselves.

**Displacement / correlation studies.** Wind against CCGT, or wind against net imports, over many records shows which technology absorbs variability. Supported because all categories are observed at the same instant, so contemporaneous correlation is not an alignment artefact.

**Net interconnector position.** The interconnector members are signed (the example carries two negatives), so import/export flipping, per-link utilisation, and aggregate net exchange are all directly derivable per interval.

**Storage cycling.** Pumped storage is carried as its own signed member, so charge/discharge alternation and cycle counts are observable. State of charge and round-trip efficiency are not.

**Diurnal and seasonal profiling.** The absolute instant on every record supports grouping by hour, day, month, or by the interval ordinal, and hence typical-day and duck-curve style profiles.

**Displacement-of-coal / retirement tracking.** Zero-run detection on coal and oil is trivially supported; the example shows explicit zeros, so a genuine zero is representable and distinguishable from absence.

**Data-quality surveillance.** Because two independent time indices are present, records can be cross-checked against each other, and gaps, duplicates, and off-grid timestamps can be detected. This is worth running *before* any of the above.

**Energy accounting** is supported only conditionally — see §3 and §4. **Emissions, prices, curtailment, capacity/availability, per-plant detail, and demand** are not supported at all from this feed alone; each needs data that is not here.

# 3. Combination rules

**The interval ordinal.** This is a label, not a measurement. It may be compared for ordering and differenced *only within a single day-frame*, and even then the difference is an interval count, not a duration, unless intervals are equal-length. It must never be summed, averaged, or used as a join key on its own: it is not unique across days, and two records with the same ordinal from different days are different things. Do not treat it as a quantity of any kind.

**The instant.** Ordering and differencing are valid; the difference is elapsed time and is the empirical way to establish interval length. Summing instants is meaningless. This is the only member suitable as a primary key — subject to the revision problem in §5. Records whose timestamps carry different UTC offsets must be normalised to a single reference before being ordered or differenced; the example carries an explicit `Z`, but the files do not establish that every record will.

**All power members (production categories, storage, interconnectors).** All are nominally the same unit, so:

- *Within one record*: they may be summed and differenced freely. That is the one unambiguously safe aggregation here.
- *Across records*: they may be **differenced** (ramp), and **averaged** to obtain mean power — but averaging is only an unweighted mean if every interval in the window has the same duration. If interval length varies (which the ordinal's upper bound of 50 implies it can), the average must be time-weighted or it silently over-weights short intervals.
- *Across records*: they may **not** simply be summed. Adding rates across time produces a number with no physical meaning. Energy requires multiplying each value by its own interval duration first, and that duration is not carried in the data.
- *Across records*: comparison is valid, with the caveat that a value from a long clock-change interval is not comparable like-for-like with a value from a normal interval if the value is an interval average rather than an instantaneous reading.

**Signed members must not be pooled with unsigned ones for share calculations.** Interconnectors and pumped storage may be negative — the example proves it for two interconnectors. A "percent of the mix" computed over a denominator that includes negative terms produces shares above 100% for some categories and negative shares for others. Decide explicitly: either exclude negative terms from the denominator, or split the record into a gross-supply side and a net-export side, and say which you did. Do not let a spreadsheet decide it for you.

**The residual category must not be treated as disjoint from the named ones.** Nothing establishes that the categories partition anything, and nothing establishes that the residual excludes what the named members already count. Adding it into a total risks double-counting; excluding it risks under-counting. There is no published total in the record against which either choice can be checked.

**Absence is not zero.** Only the interval ordinal and the instant are required; every power member may be missing. The example carries explicit `0.0` values, which proves that zero is expressible — so a missing member means "not stated", not "none". Any sum or mean that silently coerces missing to zero will understate totals and shift shares, without raising an error. This is the failure mode most likely to occur and least likely to be noticed.

**Validation will not save you.** Range constraints are applied only to the interval ordinal. The power members are unbounded, so implausible or wrongly-signed values pass schema validation cleanly. Plausibility checking is the analyst's job.

# 4. Time

The **instant** establishes the time axis. It is an absolute point, and in the example it is expressed with an explicit UTC designator, so it maps to civil time in any zone by applying that zone's offset rules — rules that are not in these files. The interval ordinal is a secondary index: it locates the record within some day-frame, but the files never define where that day begins.

The relationship between the two is under-determined, and the single example makes the problem visible rather than resolving it. **Guess:** intervals are thirty minutes and numbered from 1 at the start of the day. Under that guess, ordinal 12 begins 5h30m after the day boundary, and the example's instant of 05:30 UTC places the day boundary exactly at 00:00 UTC. But a day anchored to UTC always contains exactly 48 half-hours, which cannot produce the ordinal's permitted maximum of 50. A maximum of 50 only makes sense for a day-frame anchored to a local clock that shifts twice a year — and under a local anchor with a summer offset of one hour, this July record's ordinal 12 should begin at 04:30 UTC, not 05:30.

So one of these is true, and the files do not say which: the intervals are not half-hourly; or the numbering does not start where I assumed; or the day-frame is UTC-anchored and the bound of 50 is merely permissive; or the timestamp in this example is a local wall-clock time incorrectly labelled as UTC. That last possibility is the dangerous one, because it would silently shift the entire series by an offset that changes twice a year. **I am declining to decide this.** Resolve it empirically before analysis: pull the records spanning a clock-change day, count the intervals in it, and check whether the timestamp spacing stays constant across the transition. Until then, do not join this feed to anything else on wall-clock time.

Positions on the axis are interval *starts*, per the member's name. Each value therefore describes the interval that follows its stamp, not the one that precedes it. Whether the value is the mean over that interval or an instantaneous reading at its start is not determined, and this matters: only the mean interpretation makes value × duration a correct energy figure.

# 5. Ambiguities

**Units.** That these are megawatts rests entirely on a naming convention. Nothing declares a unit, a scale factor, or a magnitude. *Not determined* — verify against the publisher before reporting absolute numbers.

**Interval duration.** Not carried in the data. Required for every energy figure. *Guess:* thirty minutes, based on the ordinal's bound. Recoverable empirically from timestamp spacing; do that.

**Day-frame anchoring and the 50-interval maximum.** *Declining to decide* — see §4.

**Mean or instantaneous.** Whether each power value is the average over its interval or a spot reading at the start is *not determined*. Affects energy totals and affects whether ramp differences are true ramps or sampling artefacts.

**Measurement boundary.** Whether these figures cover only transmission-connected plant, or all plant including distribution-connected and behind-the-meter generation, is *not determined*. The absence of a solar member is evidence that the boundary is narrower than "everything", but the files do not say where it sits.

**What the residual contains,** and whether it overlaps the named categories: *not determined*.

**Sign convention.** *Guess:* positive means import (for links) and generating/discharging (for storage); negative means export and pumping. The negatives in the example establish that the members are signed, but not which direction each sign means. Getting this backwards inverts every net-exchange conclusion, so confirm it.

**Data vintage and revision.** There is no version, revision, publication-time, or provenance member. Consequently an initial estimate and a later restatement of the same interval are *indistinguishable* — same ordinal, same instant, different numbers, no tiebreak. If this feed is ever revised, deduplication by timestamp will keep whichever record happened to arrive last in your pipeline, and back-tests will not be reproducible. *Not determined* whether revisions occur; if they do, you need ingest-time metadata that this feed does not provide. Capture your own receipt timestamp at ingest.

**Whether the figures are metered, estimated, or forecast.** *Not determined.* A forecast feed and a settled-metering feed have identical shape here.

**Numeric resolution.** Every value in the example is integral despite a floating-point declaration. Whether the source publishes sub-MW resolution is *not determined*; do not report more precision than you can justify.

**Completeness of the category list.** Whether these are all the categories that will ever appear, or whether new ones (a solar member, a new interconnector) may be added later, is *not determined*. Since the record shape forbids unrecognised members, a new category would require a schema change — so pipelines built on this shape will reject, rather than ignore, an extended future record. Plan for that.
