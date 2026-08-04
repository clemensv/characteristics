# 1. What this feed is

Each record is a one-shot telemetry sample taken by a public-transport vehicle in the Helsinki region while it is running a scheduled trip, published roughly once per second per vehicle over MQTT. A record answers: at instant *T*, this physical vehicle, operated by this operator, running this scheduled trip on this route and direction, was at this position, moving at this speed and heading, with its doors in this state, this far into its trip by odometer, and this far off its timetable.

The stream is therefore a set of interleaved per-vehicle trajectories, not a set of independent observations. The natural unit of analysis is not the record but the **vehicle-trip**: the run of consecutive records sharing the same operator, vehicle, route, direction and scheduled departure. Almost every useful quantity here is only meaningful inside that grouping.

The stream contains only position events. There are no explicit stop-arrival, stop-departure, or door-transition events in these records, so anything event-like — a dwell, a stop service, a door cycle — has to be *inferred* from consecutive samples, and inferred from a sampling process whose cadence is described only as "roughly" one per second.

# 2. Analytics

**Schedule adherence and punctuality.** The timetable deviation is carried on every sample and is anchored to a specific scheduled trip, so you can profile lateness along a trip, by route and direction, by time of day, and by operating day. This is the single strongest analysis the feed supports, because the producer has already done the schedule join for you.

**True running speed and trip distance.** The odometer accumulates from the actual start of the trip, so differencing it between two samples of the same vehicle-trip gives a distance travelled over a known elapsed time. This yields a defensible average speed. Averaging the instantaneous speed samples does not, and the two answers will differ.

**Congestion and delay geography.** Position plus instantaneous speed, filtered to satellite-fixed positions, lets you map where on a route vehicles slow down and where lateness accrues. Because lateness is carried per sample, you can locate *where* delay is accumulated rather than only observing that it exists at the terminus.

**Headway regularity and bunching.** Vehicles are individually identifiable and positions are frequent, so you can measure the time gap between successive vehicles passing a common point on the same route and direction. This is a genuinely different question from punctuality, and the timetable-deviation member does not answer it: two vehicles can both be equally late and be perfectly bunched.

**Dwell and stop-service inference.** Door state, near-zero speed, and the stop identifier together let you infer stop servicing. This is inference, not observation, and the strength of the conclusion depends on cadence, so treat it as a derived and lossy signal.

**Vehicle blocking and duty reconstruction.** Sequencing the distinct scheduled trips seen for one physical vehicle across an operating day reconstructs its block, which supports utilisation, layover and interlining analysis.

**Telemetry health.** The positioning-method member, the optionality of position, door state and deviation, and the gaps between consecutive sample timestamps together support a first-class data-quality analysis: what fraction of a fleet is reporting satellite fixes versus dead-reckoned or manually entered positions, and where coverage degrades. This is worth running *before* any of the above, because it determines which records are admissible into them.

**What the feed does not support.** Occupancy or crowding analytics are not supported for general vehicles: only Suomenlinna ferries report a measured value and everything else transmits a constant, so any fleet-wide occupancy chart is an artefact of that constant, not a measurement. Nothing here counts passengers. Acceleration is not a suitable basis for ride-quality, harsh-braking or energy analytics (see below).

# 3. Combination rules

**Vehicle number, operator, stop, route, and direction** are labels. Never sum, average, or difference them. Vehicle number is not unique on its own — the operator/vehicle pair is the identity of a physical vehicle, and grouping by vehicle number alone silently merges distinct vehicles across operators. Direction is carried as a string enumeration and neither value denotes a compass bearing; do not treat it as ordered or numeric.

**Route identifier versus displayed route number.** These are not interchangeable. The displayed number is a passenger-facing head-sign label; the other is the GTFS route key. Group and join on the GTFS identifier. Grouping on the display label will merge or split routes in ways that vary by route.

**Timetable deviation** may be compared, differenced, and averaged across records, with two conditions. First, the sign convention is inverted relative to normal practice: negative means *late*, positive means *early*. Any analysis that does not flip this reports the opposite of the truth. Second, it is comparable only against other records computed on the same basis; it is a producer-computed figure, not something these records let you recompute or audit.

**Odometer** may only be *differenced*, and only between two records of the same vehicle-trip. It must never be summed or averaged, and raw values must never be compared across vehicles or across trips: the counter is reset at the actual (not scheduled) start of each trip, so the same reading means different things on different trips, and a difference taken across a trip boundary is meaningless and may be negative. The maximum reading within one vehicle-trip approximates distance covered so far.

**Instantaneous speed** may be compared record to record. Averaging is conditional and usually wrong as performed: the arithmetic mean of speed samples is a *time*-weighted average only if samples are evenly spaced in time, and the cadence here is approximate and varies. It is never a distance-weighted average, so it does not equal distance divided by elapsed time. If you want average speed, use differenced odometer over differenced timestamp. Speed samples must not be summed.

**Acceleration must not be combined with anything, including other acceleration values.** It is not measured; it is a difference quotient over the interval between this sample and the previous one, and that interval's length varies between messages and is not carried by the record. Two acceleration values therefore describe periods of different and unknown duration, so they are not comparable, not averagable, and not integrable. It is also undefined for the first sample of a trip, and it is derived from the speed member, so speed and acceleration are not independent variables and must not be entered into a model as if they were. Threshold-based harsh-braking detection is unsound here, because the threshold's meaning depends on an interval length you do not have.

**Heading** is a circular quantity and must not be averaged arithmetically: the mean of 359 and 1 is not 0. Use vector or circular statistics. The permitted range includes both 0 and 360, which are the same bearing, so raw-value histograms and group-by operations split north across two buckets unless you normalise first. Heading is also not meaningful for a stationary vehicle; the files do not say what is reported at rest.

**Latitude and longitude** may be compared and, over a small area, averaged as a centroid — but never with equal weighting of the two axes. At this latitude a degree of longitude is roughly half the ground distance of a degree of latitude, so Euclidean distance or clustering computed directly on degree pairs is distorted by about a factor of two along the east–west axis. Project first, or use a proper geodesic distance.

**Position may only be combined across records whose positioning method matches the analysis.** Odometer-propagated, dead-reckoned and manually entered coordinates are not fixes; they are extrapolations or human input. The method changes without warning between consecutive samples of the same trip, so filtering has to be per-record, not per-trip. Mixing these into positional accuracy, dwell detection, or map-matching corrupts the result. Position is absent when unavailable, and absence is not the origin.

**Door state** is a state, not a quantity. It may be counted, and the fraction of samples with doors open approximates the *time* fraction only under the same uniform-cadence assumption that constrains speed averaging. It is absent when the onboard system cannot determine it, and absent must not be recoded as closed.

**Occupancy must not be summed, averaged, or compared across vehicles at all**, unless you have established externally that every vehicle in the set is a Suomenlinna ferry. For all other vehicles the value is a constant, and aggregating constants produces a number that looks like an occupancy statistic and is not one. The records carry no transport-mode member, so this precondition cannot be checked from the data itself.

**Timetabled arrival and timetabled departure** are planned instants, not observations. They may be compared with each other (departure never precedes arrival) and with the sample timestamp, since all three are UTC instants. They must never be averaged into observed-time statistics, and differencing them gives planned dwell, not actual dwell. They are present only while the vehicle is in a stop relation, so their absence is structural and must not be imputed.

**Scheduled-departure clock readings must never be sorted, compared or differenced as raw strings.** See below.

# 4. Time

The time axis of the thing described — the vehicle's state — is established by the sample timestamp. It is a UTC instant at millisecond precision, generated by the vehicle, and it is a civil instant: it can be compared and differenced directly against other sample timestamps and against the two timetabled instants, which the publisher has already normalised to UTC.

That axis is an *instant* axis for position, speed, heading, door state, positioning method, occupancy and deviation. It is not an instant axis for the odometer or for acceleration. Both of those characterise a *period* that closes at the sample timestamp and whose opening boundary the record does not carry: for the odometer it is the moment the vehicle actually began the trip, for acceleration it is the timestamp of the preceding message. Neither opening boundary is recoverable from a single record, and neither period has a stated length. The nominal one-second cadence is a statement about what the vehicle is expected to emit next; it does not bound either period.

The trip's scheduled departure sits on a **different axis entirely** and is the principal trap in this feed. It is an operating-day clock position, not a civil instant, and it must not be compared with one without converting through the operating-day regime. Two consequences follow that will silently corrupt naive work:

*The date-looking component is not a calendar date.* The operating day runs past midnight and ends around 04:30 the following calendar morning. A trip departing at 00:30 carries the *previous* date. Joining that component to a calendar-date dimension therefore assigns the post-midnight tail of every service day to the wrong day, and "all trips on 31 July" by calendar is not "operating day equals 31 July".

*The clock component wraps within a single operating day.* A departure of 00:30 occurs *after* every larger clock reading on the same operating day. Sorting or range-filtering on that raw clock string produces an ordering that is wrong precisely at the late-night boundary — the busiest place for headway and last-departure analysis. The fixed-width ordinal exists for exactly this reason: it renders the operating day and the minutes elapsed since 04:30 local, most significant first, so plain lexical ascending sort gives correct forward chronological order without implementing the regime. Sort and compare on the ordinal; use the other two members for display and for joining to schedule data.

Relating that axis to civil time requires the local UTC offset, which these records do not carry — see below.

# 5. Ambiguities

**The local UTC offset is not stated.** The operating-day boundary and the scheduled departure are both expressed in local time, and the sample timestamp is UTC, so converting between the two axes requires an offset the files never give. General knowledge of the region suggests EET/EEST, but the files do not establish it, and I am **declining to fix it** as a datum. Note that the single example record is only internally consistent — a positive odometer and a late-running deviation both imply the trip has already begun — if local time is roughly three hours ahead of UTC at that moment. That is an inference from one record, not a specification.

**Daylight-saving handling of the operating day is undetermined.** On transition days the operating day is not 24 hours, so minutes-elapsed-since-04:30 counts are not comparable across such days, and the boundary itself is described only as "approximately" 04:30. I am declining to decide how the producer handles this.

**The stop relation does not reconcile in the example.** The stop identifier is described as the stop most recently *departed from*, yet the timetabled arrival and departure attached to it fall *after* the sample timestamp while the deviation reports the vehicle as running late. Under a literal reading these cannot all hold. Something in the reading is wrong — either the stop reference is forward-looking in this state, or the deviation is trip-level rather than stop-local. **I am declining to decide which**, and the practical consequence is firm: do not derive stop-level punctuality by comparing the sample timestamp against the timetabled departure. Use the deviation member.

**The scope of trip identity is underdetermined.** The operating day and departure clock reading are asserted to identify the trip, but that cannot hold across the whole network, since many trips share a departure minute. **Guess:** the identifying key is unique only within a route and direction, so the practical trip key is route + direction + operating day + departure, and the vehicle-trip key adds operator and vehicle. Marked as a guess.

**Whether the ordinal is guaranteed consistent with the other two members is not stated.** It is consistent in the example — 07:15 is 165 minutes after 04:30 — but nothing rules out divergence, and the files do not say which member is authoritative if they disagree. Declining to decide; I would validate the invariant rather than assume it.

**The constant that non-ferry vehicles transmit for occupancy is not given.** The example carries zero, but one record does not establish the sentinel, and it is not stated whether the constant is uniform across operators or vehicle classes. Declining.

**Transport mode is not carried**, so the precondition for reading occupancy at all cannot be evaluated from these records. Neither the route identifier nor the display label is stated to encode mode.

**What the deviation is measured at is not stated.** It is anchored to the scheduled departure, but the files do not say whether it expresses deviation at the vehicle's current point on the trip or deviation accrued at departure. **Guess:** current-point deviation, since it is emitted on every sample and would otherwise be constant for the whole trip — and that is a testable prediction. Marked as a guess.

**Whether speed can be negative, and how it is derived**, are not stated; in particular it is not said whether the speed source tracks the positioning method. Declining.

**No accuracy or dilution-of-precision member accompanies position**, so positional uncertainty is not quantifiable from the record even for satellite fixes.

**Delivery semantics are undetermined.** The transport is MQTT and there is no sequence number or message identifier, so duplicates cannot be detected and dropped messages can only be inferred from timestamp gaps — which is indistinguishable from a vehicle that stopped transmitting. This matters directly, because every uniform-cadence assumption above depends on it.

**Which GTFS dataset the route and stop identifiers belong to is not stated**, nor is any version or validity window, so the join to schedule data is not fully specified by these files.

**Subcontracting cannot be observed from the records.** The operating operator is said to possibly differ from an owning operator carried on the MQTT topic, but the topic is not part of the record, so operator-level attribution from this data reflects the operating party only.

**Whether the operator/vehicle pair is stable over time** — that is, whether a vehicle can move between operators and retain its number — is not determined, which bounds any longitudinal per-vehicle analysis.
