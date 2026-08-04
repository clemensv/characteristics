# 1. What this feed is

Each record is a single telemetry sample emitted by one road vehicle operating a scheduled public-transport journey. It ties together three things that are usually kept apart: **who is reporting** (a vehicle, belonging to an operator), **what service they are currently running** (a route, a direction, a public-facing line designation, and a specific dated journey identified by its scheduled start), and **what the vehicle was doing at one instant** (position, positioning source, speed, heading, acceleration, an odometer reading, a schedule-deviation figure, the stop currently in context with its scheduled arrival and departure, door state, and an occupancy figure).

The stream is therefore a *vehicle-time* stream, not an event log, despite the shape of the payload. There is no member that says what kind of event a record represents — no "door opened", "arrived", "departed", "started journey" discriminator. Everything an analyst might want to treat as an event (a stop arrival, a door cycle, a journey start) has to be **derived from transitions between consecutive records of the same vehicle**, not read off a single record. Anyone who plans work on the assumption that arrivals or door events appear as distinct record types will build the wrong pipeline.

The service-identifying members are always present; almost everything measured is optional. A record is guaranteed to tell you which vehicle, which operator, which journey, which route and direction, at what instant, and from what positioning source — and is *not* guaranteed to tell you where the vehicle was. That asymmetry is deliberate and is the first thing to design around.

# 2. Analytics

**Schedule adherence.** The scheduled arrival and departure for the stop in context are absolute instants on the same axis as the observation timestamp, so actual-versus-scheduled is directly computable without any timezone reasoning. This is the strongest analysis the feed supports, because it needs no unit assumptions at all: it is instant minus instant.

**Headway and bunching.** Records carry route, direction, and a stop identifier alongside an absolute timestamp, so successive vehicle passages at a common stop on a common route and direction can be ordered and differenced. Bunching detection needs only ordering, which is safe here.

**Segment run times.** Because the stop in context changes over the life of a journey and every record carries the journey identity, the sequence of stop-context changes within one journey yields inter-stop traversal times from timestamps alone. Again, unit-free.

**Dwell time and door-cycle behaviour.** The door-state flag plus the timestamp gives door-open and door-closed intervals by transition. Scheduled dwell is separately available as the gap between scheduled departure and scheduled arrival — in the example that gap is zero, meaning the schedule models no dwell at that stop, which is itself worth profiling across the network.

**Telemetry quality and coverage.** The positioning-source member is required on every record even when there is no position, and one of its values explicitly denotes an unusable or absent fix. That makes it possible — and necessary — to measure where and when the fleet loses positioning, how much of each journey is dead-reckoned or odometer-derived, and which vehicles are chronically degraded. This is not a side analysis; it is the prerequisite that determines whether any position-derived result is trustworthy.

**Trajectory and speed profiling.** Position plus timestamp reconstructs a path per journey, and speed, heading and acceleration give a motion profile along it. Supported, but only within a single positioning source (see §3).

**Distance and utilisation.** The odometer is monotone within some epoch, so per-journey or per-vehicle distance is obtainable as a difference — conditional on knowing the reset epoch, which the files do not give.

**Occupancy profiling by time, route, and direction.** The occupancy member combined with route, direction and time supports loading curves, subject to a semantic ambiguity that materially changes the result (see §5).

**Journey completeness and fleet assignment.** Because journey identity is required on every record, you can find scheduled journeys with no telemetry at all, journeys served by more than one vehicle, and vehicles that switch journeys mid-stream. Operator identity supports fleet-versus-fleet comparison.

**Driving-behaviour flagging.** Signed acceleration supports harsh-braking and harsh-acceleration detection using empirically learned thresholds. It does *not* support reporting those thresholds in physical units.

# 3. Combination rules

**A rule that governs everything below.** These are samples from per-vehicle streams whose emission rate is not specified and is not guaranteed to be constant. Any unweighted mean taken over *records* is a per-sample mean, not a per-second, per-journey, per-vehicle or per-passenger mean. A vehicle that reports twice as often will dominate every naive average. Aggregate first to a natural unit — a stop visit, a journey, a vehicle-hour — and only then combine. Where a quantity is a *state* rather than an event (door state, occupancy, speed, positioning source), time-weight it by the interval to the next sample rather than counting records.

**Vehicle identifier, operator identifier.** Labels. Equality and grouping only; never differenced, summed or averaged. Whether the vehicle identifier is unique across operators or only within one is not determined; the presence of a separate operator member is a reason to key on the pair. Counting distinct vehicles on the vehicle identifier alone risks collapsing two operators' vehicles into one.

**Observation timestamp.** An absolute instant with an explicit UTC designator. Freely comparable and differenceable across every record in the feed regardless of vehicle, operator, route or day. Differences are true elapsed durations and may themselves be summed and averaged. Averaging the instants directly is meaningless. The example carries millisecond precision; that the underlying clock is *accurate* to a millisecond is not established, and clock skew between vehicles is not addressed anywhere.

**Journey identity.** A composite label, not a measure. Equality only. Its ordinal component embeds the operating-day date, so the ordinal and the operating-day member are not independent and can be cross-checked. The ordinal's four-digit tail is **not** the scheduled start rendered as HHMM — in the example the tail and the start disagree — so do not treat them as redundant encodings of one another. Whether the ordinal is unique network-wide or only within an operator or route is not determined; a journey key that is safe under all readings includes route and direction as well as the ordinal.

**Operating day.** A date *label* for a service day, not a calendar date derived from the timestamp. Do not join it to the calendar date of the observation timestamp — those two will legitimately disagree for late-night service. Differencing two operating-day values in days is only a duration under an operating-day rule the files do not state.

**Scheduled start.** A clock position on the operating-day clock, not an instant and not a time of day. The permitted format admits hour values that are not valid wall-clock hours, which is exactly how service continuing past midnight is normally represented; parsing it as a time of day will therefore fail or silently mis-order late journeys. Two start values may be compared for equality; differencing them as times is unsafe without the operating-day rule.

**Line designation and route identifier.** Two distinct labels that differ in value in the example, so they are not interchangeable grouping keys. Equality only. Which one is stable over time — a public-facing label can be reassigned between services in a way an internal identifier usually is not — is not determined.

**Direction.** A two-valued label carried as text, not a number. Equality only; never arithmetic. Its physical meaning is not established and is only interpretable relative to a route, so it must always be grouped *within* a route, never across routes.

**Latitude and longitude.** No coordinate reference system is stated. Comparability is conditional on the **positioning source**: positions derived from odometry, dead reckoning or manual entry have error characteristics that are different from, and unknown relative to, satellite fixes. Segregate by positioning source or carry it through every aggregate; mixing sources into one track silently changes what is being measured. Never impute a missing position as zero. Naive arithmetic means of coordinates are not valid centroids, and differences of coordinates are not distances without a projection.

**Positioning source.** A categorical provenance and status discriminator, required even where there is no position. It is a filter and a grouping key, never a quantity. Dropping records that lack a position is *not* random deletion — missingness correlates with terrain, tunnels and equipment faults, so listwise deletion biases every downstream result toward well-covered areas and healthy vehicles.

**Speed.** No unit is stated. Values may be compared and averaged **against each other within this feed** on the assumption that the producer is internally consistent, but must not be converted to any physical unit and must not be combined with any external speed series. Because it is an instantaneous state, an unweighted mean of samples is not an average speed; either time-weight it or compute distance over elapsed time instead. Never summed.

**Heading.** A circular quantity. Arithmetic means are wrong — the mean of 350 and 10 is not 180 — so use circular/vector statistics. Differences must be wrapped. The permitted range admits both endpoints, so two distinct encodings of the same direction exist and values must be normalised before equality comparison. The reference direction (true, magnetic, or grid) is not stated, so headings must not be combined with any external bearing data. Whether it is vehicle heading or course over ground is not determined, which matters for reversing vehicles and for stationary samples.

**Acceleration.** Signed, no unit. Same treatment as speed: internally comparable, not convertible, time-weighted if averaged, never summed. Whether it is a longitudinal component or a signed scalar of total acceleration is not determined; whether it is the derivative of the reported speed from the same source is not determined, so do not assume the two are consistent.

**Odometer.** A cumulative counter. **Differences only, and only between records from the same vehicle within an interval containing no reset and no rollover.** Never summed across records — summing a cumulative counter multiply-counts the same distance. Never averaged. Never compared across vehicles, since each vehicle's epoch is its own. The unit is not stated, so a difference is a distance in unknown units. Note also that odometry is one of the declared positioning sources, so where that source is in use the odometer and the reported position are not independent measurements and must not be used to cross-validate one another.

**Schedule deviation.** Signed integer, unit not stated and sign convention not stated. Critically, it is **not** reconstructible from the record's own timestamp and scheduled arrival: in the example the gap between them is about sixteen seconds while the deviation reads ninety-five in magnitude. So it references something other than this record's scheduled arrival, and any pipeline that derives one from the other, or that validates one against the other, is unfounded. Treat it as an opaque signed adherence index: comparable and averagable within the feed, not convertible to minutes, and not safe to describe as "early" or "late" until the sign convention is established externally. When averaging, aggregate per stop visit or per journey first — averaging over raw records weights vehicles by their reporting rate.

**Stop identifier.** A label. Equality only; never summed, averaged or differenced, and never treated as ordered even though it is numeric. Whether it denotes the stop just served or the stop being approached is **not determined**, and that choice changes the meaning of the scheduled arrival, the scheduled departure and any dwell derived from them. It is optional, so records between stops may carry none.

**Scheduled arrival and scheduled departure.** Absolute instants on the same axis as the observation timestamp, so actual-minus-scheduled is a valid duration — this is the one cross-axis bridge in the whole payload that is safe. But these values belong to a *(journey, stop)* pair, not to the record: the same pair repeats identically on every record emitted while that stop is in context. Deduplicate by journey and stop before counting stop visits or averaging anything derived from them, or high-frequency vehicles will be counted many times per stop. Their difference is scheduled dwell, which is zero in the example. They are stated to second precision while the observation timestamp is stated to millisecond precision; do not infer schedule knowledge finer than a second.

**Door state.** A two-valued state flag, not a quantity. Summing it counts samples, not door cycles, and the fraction of records showing the open state is not the fraction of *time* doors were open unless sampling is uniform in time. Derive durations from transitions against the timestamp. Which of the two values means "open" is not stated.

**Occupancy.** Bounded between zero and one hundred. Whether this is a percentage of capacity or a passenger count that happens to be capped is **not determined**, and the two readings do not combine the same way: a percentage averaged across vehicles of different capacity is a ratio of ratios and needs capacity weighting to mean anything, whereas a count sums and averages directly. Under either reading the upper bound censors the busiest observations, so means are biased low at peak. It is a state, so time-weight it. It is optional, and an absent value is not an empty vehicle. No capacity, vehicle type, or boarding/alighting members exist, and the record is closed to additional members, so occupancy cannot be converted into passenger counts from within this feed.

**Cross-record identity.** There is no record identifier and no sequence number, so duplicate delivery and out-of-order delivery cannot be detected except by assuming that vehicle plus timestamp is unique — an assumption the files do not confirm.

# 4. Time

There are **two distinct time axes**, and the most common way to get this data wrong is to treat them as one.

The **observation timestamp is the axis of the thing described.** It is an absolute instant carrying an explicit UTC designator, so it is globally ordered, directly differenceable across vehicles, operators, routes and days, and immune to timezone and daylight-saving complications. All true elapsed durations — headways, run times, dwell times, sampling gaps — must be computed on this axis and only on this axis. The scheduled arrival and departure are stated on the *same* axis, which is why schedule adherence is computable without any zone reasoning at all.

The **operating-day clock is a second, non-instant axis** used only to name the journey. Its date component labels a service day, and its start component is a position on a day-relative clock anchored to that date. A position on this axis does not become an instant without a timezone and an operating-day rule, **neither of which the files supply.** Concretely:

- The operating-day label is not the calendar date of the observation timestamp. Late-evening and post-midnight service will carry an operating day that differs from the UTC — and possibly from the local — calendar date of its own records. Grouping "by day" gives materially different answers depending on which of the two you use, and only one of them corresponds to a service day as an operator understands it.
- The scheduled start's format permits hour values beyond the wall-clock range, which is the normal way to express a journey that begins after midnight but belongs to the previous service day. Sorting or parsing it as a time of day will mis-order exactly the journeys that most need careful handling.
- If the applicable local zone observes daylight saving, an operating day may be twenty-three or twenty-five hours long. Durations computed on the operating-day clock are therefore not durations at all.

**Relating either axis to civil time requires a timezone the files do not name.** Nothing in the data identifies the jurisdiction or the offset. So no statement of the form "this occurred during the morning peak" is supportable from these two files alone; every time-of-day analysis rests on an externally supplied zone.

There is one piece of internal evidence, and it should be labelled for what it is. The example's journey has a scheduled start of 07:15 on the operating-day clock while the record itself is timestamped just after 05:12 UTC. If the record falls after its own journey's start — which is likely but not guaranteed, since a vehicle may report before beginning service — then the local civil clock the schedule uses runs at least about two hours ahead of UTC. That is an inference from one record, not a fact the files establish. What it does establish beyond doubt is the negative: **the operating-day date and the scheduled start are not UTC**, and concatenating them into a UTC instant produces a value roughly two hours wrong.

# 5. Ambiguities

**Units of speed, acceleration, odometer, and schedule deviation.** Not determined; **declining to decide.** The value ranges are consistent with several conventions and nothing in the data discriminates among them. All four are usable as internally comparable indices; none is usable as a physical measurement or safe to combine with any external series until a unit is supplied.

**Odometer reset epoch.** Not determined; **declining to decide.** Whether the counter resets per journey, per operating day, per shift, per maintenance event, or runs for the vehicle's life is the single most consequential undetermined fact in the feed. Under the per-journey reading, distance-per-journey is a direct read; under the lifetime reading it is a difference and the reported value is meaningless on its own. Any distance figure must therefore be validated against observed reset behaviour in the actual stream before it is published. As an illustration of the exposure: if the reset were per journey and the unit were metres, the example's counter combined with the elapsed time implied by the guessed local offset would give an implausibly low mean speed for scheduled road transport — which suggests at least one of those two assumptions is wrong, but does not tell us which. That chain rests on a guessed timezone and is offered only as a caution, not a finding.

**Sign convention of the schedule deviation.** Not determined; **declining to decide.** Negative could mean ahead of schedule or behind it. The example does not settle it, because the value cannot be reconciled with the record's own timestamp and scheduled arrival. Reporting punctuality with the sign guessed wrong inverts the entire result.

**Reference point of the schedule deviation.** Not determined; **declining to decide.** It is measured against something other than the scheduled arrival carried in the same record — possibly the current point along the route rather than the stop, possibly a different timing point. Until this is known, treat the deviation and the record's scheduled times as unrelated.

**Semantics of the occupancy figure.** Not determined; **declining to decide** between "percentage of capacity" and "capped passenger count". This changes both the interpretation and the legal aggregation rule, and no capacity member exists to disambiguate.

**Whether the stop identifier is the stop just served or the next stop.** Not determined; **declining to decide.** It changes what the scheduled arrival and departure refer to and therefore what any derived dwell or adherence figure measures.

**Coordinate reference system.** Not stated. **Guess:** the coordinate values are plausible as decimal degrees on a common global geodetic datum, and I would proceed on that basis for anything at street scale. Marked as a guess; any centimetre- or metre-critical work must confirm it.

**Heading reference and meaning.** Not determined; **declining to decide** between true, magnetic and grid north, and between vehicle heading and course over ground. Also unresolved is what heading means for a stationary vehicle.

**Door-state polarity.** Not stated. **Guess:** the non-zero value means doors open. Marked as a guess; it is cheaply falsifiable in real data by checking whether the non-zero state co-occurs with near-zero speed at stop context.

**Uniqueness scope of the vehicle identifier and of the journey ordinal.** Not determined; **declining to decide.** I would key vehicles on operator-plus-vehicle and journeys on route-plus-direction-plus-ordinal, since both are safe under every reading, at some cost in key width.

**Meaning of the journey ordinal's four-digit tail.** Not determined; **declining to decide.** It is demonstrably not the scheduled start expressed as HHMM. Treat it as an opaque token and do not parse it.

**Sampling rate and its stability.** Not determined. Nothing states how often a vehicle reports, whether the rate varies with speed or door state, or whether it differs by operator or equipment generation. This must be measured empirically before any average over records is trusted.

**Distinguishing the two identifiers for the line.** The public-facing designation and the route identifier differ in value. **Guess:** the shorter is the label presented to passengers and the longer an internal identifier, which would make the internal one the more stable grouping key. Marked as a guess.

**Relationship between speed, acceleration, and the positioning source.** Not determined. Whether these motion values come from satellite positioning, from the vehicle bus, or from whichever source the positioning-source member names is unstated, so their accuracy characteristics across positioning modes cannot be reasoned about.

**Timezone and operating-day rule.** Not determined; **declining to decide**, beyond the firm negative that the operating-day members are not UTC. Both must be supplied externally before any time-of-day or service-day analysis is meaningful.

**Duplicate and out-of-order delivery.** No record identifier or sequence number exists. **Guess:** vehicle plus timestamp is unique and suitable for deduplication. Marked as a guess; millisecond timestamp precision makes it plausible but does not guarantee it.

**Absence of an event-type member.** Firmly established as absent rather than ambiguous, and restated here because it is the most likely source of a wrong architecture: this is a sampled state stream, and every event of interest must be derived from transitions between consecutive samples.
