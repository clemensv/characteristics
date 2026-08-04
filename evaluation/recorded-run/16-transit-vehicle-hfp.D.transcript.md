# 1. What this feed is

Each record is a single telemetry sample taken by a public-transport vehicle in the Helsinki region while it is operating a scheduled trip, published roughly once per second per vehicle. A record answers: at this instant, this physical vehicle — identified by the operator that is actually running the service plus the number painted on its side — was at this coordinate, moving at this speed on this heading, this far into the current trip on its odometer, this many seconds off its timetable, with its doors in this state.

The records are therefore not observations of a route, a stop, or a trip. They are observations of a vehicle, tagged with the trip it happens to be executing. Everything schedule-related in the record (`journey_start`, `ttarr`, `ttdep`, `dl`) is plan, not observation; everything position- and motion-related is observation, of varying and self-declared provenance. The stream is a moving-point time series with an attached, and only partially resolvable, planned-versus-actual comparison.

The stream is not self-contained. It carries GTFS route and stop identifiers but not the GTFS feed itself, not a trip identifier, not a transport mode, and not vehicle capacity. Several fields cannot be interpreted without those external facts, and the record gives no way to tell you that you are missing them.

# 2. Analytics

**Schedule adherence, and its distribution over time of day, route, direction, and operator.** `dl` gives the deviation directly, at ~1 Hz, anchored to a trip whose scheduled origin is on the record. This is the strongest analysis the feed supports, because the quantity is computed onboard against the same schedule the trip is running, so it does not require you to reconstruct the timetable. It is also where the feed is most likely to be read backwards: see §3.

**Delay propagation along a trip.** Because `dl` is sampled continuously rather than only at timepoints, you can see where in the run lateness is accrued and where it is recovered, rather than only the endpoint state. Pairing `dl` with `odo` gives delay against distance travelled, which is the shape you need to find the specific link or intersection that is costing time.

**Dwell time and door-cycle behaviour.** `drst` transitions, segmented by `stop`, give you the interval the doors were open at each stop. Combined with `spd` near zero, this separates a genuine passenger stop from a signal queue — a distinction that stop-arrival events alone cannot make.

**Running-time and speed profiles per link.** `spd` is an instantaneous measured value with a QUDT quantity kind and a real unit, and `lat`/`long` place it, so speed can be mapped to geography and aggregated per segment, per hour, per direction. This supports congestion mapping and timetable revision.

**Positioning-quality analysis.** `loc` names the procedure that produced each coordinate and is explicitly stated to change without warning mid-trip. That makes it possible — and necessary — to quantify how much of the feed is satellite-fixed versus propagated, and to measure how position error grows during `ODO`/`DR` runs by observing the jump when a satellite fix returns. Very few positional feeds expose this at all; here it is a first-class analysis.

**Headway and bunching.** Multiple vehicles on the same `route`/`dir` with different `journey_start` values can be ordered in space and time, giving observed headway rather than scheduled headway.

**Fleet and subcontracting analysis.** `oper` is the operating operator and may differ from the owning operator. Over a long window you can characterise which operators actually run which routes.

What the feed does *not* support, despite appearances: ridership or load analysis. See `occu` in §3.

# 3. Combination rules

**`veh`** — an identifier, not a quantity. Never compared, differenced, summed, or averaged. It is unique only in combination with `oper`; grouping by `veh` alone will silently merge distinct physical vehicles belonging to different operators.

**`oper`** — an identifier. No arithmetic. Usable only as a grouping key and as the other half of the vehicle key.

**`tst`** — a UTC instant. May be compared and differenced freely across any two records in the feed, without qualification: this is the one axis with no regime attached. Differences of `tst` are durations and may be summed and averaged. `tst` values themselves must not be summed; averaging them is meaningful only as a deliberate centroid-in-time.

**`journey_start`** — a position, not an instant. Compare and sort using `ordinal` only, and only lexically; that is what it is for. Do **not** sort or compare on `start`, because the clock reading wraps within a single operating day and `00:30` sorts before `23:00` while occurring after it. Do **not** compare any part of `journey_start` with `tst`, `ttarr`, or `ttdep`: those are civil UTC instants and this is not one. Differencing two `ordinal` minute components is a duration in minutes **only** when the `oday` components are equal; across different operating days it is not, because the length of an operating day is not established by these files (see §5). `oday` must not be treated as a calendar date — a trip departing after midnight carries the *previous* date, so bucketing by `oday` and bucketing by the calendar date of `tst` will disagree for early-morning trips, and the disagreement is systematically concentrated in night services.

**`desi`** — a display label. It may be grouped on and counted, but it must never be joined to GTFS route data and must never be used as a route key. The record shows `desi` `551` and `route` `2551`; they are different namespaces and their similarity here is a coincidence you cannot rely on.

**`route`** — a GTFS route identifier. Grouping and joining only, no arithmetic.

**`dir`** — nominal, despite being `"1"`/`"2"`. It must not be averaged, ranked, or treated as a bearing; neither value names a compass direction, and the mapping to physical direction differs per route. Only equality comparison is valid.

**`lat` / `long`** — degrees in EPSG:4326. Two coordinates may be compared and a geodesic distance computed between them, but **differences in degrees are not distances and must not be summed or Euclidean-combined**. At the latitude in the example (≈60.2°N) a degree of longitude is roughly half a degree of latitude on the ground, so naive planar distance in degrees overstates east–west movement by about a factor of two. Averaging coordinates gives an unweighted mean of *messages*, not a mean position over time, and is invalid across records whose `loc` differs (see next). Distance travelled should come from `odo`, not from summing coordinate deltas.

**`loc`** — nominal. Counts and proportions only. Its function in combination is as a gate: coordinates produced under `ODO`, `DR`, or `MAN` are not the same measurement as those produced under `GPS`, and mixing them into one positional aggregate combines quantities of different and undeclared accuracy. `N/A` means the procedure is unknown, not that the position is bad.

**`spd`** — instantaneous, m/s, ratio-scaled. May be compared, differenced, and averaged across records. But an unweighted mean over messages is a *message-weighted* mean, not a time-weighted one; the one-second cadence is a declared expectation of emission, not a guarantee of uniform sampling, so time-weight by successive `tst` deltas if you want a mean speed. Do not sum speeds.

**`hdg`** — a circular quantity. It must **not** be differenced, summed, or averaged with ordinary arithmetic: 359° and 1° are two degrees apart, not 358, and a plain mean of them is 180°, which is the exact opposite of the truth. Use circular statistics. Note also that the declared range is 0–360 inclusive, so 0 and 360 are two encodings of one direction and equality comparison on the raw integer will fail on them.

**`acc`** — calculated over an interval that closes at `tst` and opens at the previous message's timestamp, which this record does not carry. Two `acc` values may be compared as the same quantity kind, but they characterise intervals of *different and unknown length*, so they must not be averaged as if equally weighted and must not be integrated to recover a velocity change. The schema is explicit that the one-second cadence does not bound this interval; assuming it does is the specific error to avoid. Recovering the interval requires joining to the preceding record of the same vehicle, which is possible in a stored stream and impossible from a record alone.

**`odo`** — an accumulation from a reset at the vehicle's *actual* trip start, an instant not carried anywhere in the record. Consequences: absolute `odo` values are **not comparable** between two trips, between two vehicles, or against any fixed origin. `odo` must **never be summed** across records — that double-counts every metre once per message. The valid operation is a *difference* between two records that share the same `oper`, `veh`, and `journey_start`, with the later `tst` minus the earlier, which yields distance travelled between them. Differencing across a trip boundary is invalid because the counter resets in between. `journey_start` cannot be used to date the reset: it is the *scheduled* departure, and `dl` is precisely the measure of how far the actual departure diverged from it.

**`dl`** — seconds, signed, **with an inverted convention: negative is late, positive is early.** This is the single highest-risk quantity in the feed. Every standard tool, every GTFS-RT pipeline, and every analyst's instinct assumes the opposite sign, so a mean, a percentile, an "on-time performance" threshold, or a red/green map built without negating this will report the exact inverse of reality — a chronically late route will be reported as chronically early. Values may be compared, differenced, and averaged within a consistent schedule anchor. An unweighted mean over messages again weights by message count, which over-weights stationary and slow-moving vehicles precisely because they emit as many messages while covering less ground; aggregate per trip or per stop event instead.

**`stop`** — an identifier. No arithmetic. Its absence means the vehicle is between stop relations, not that no stop exists; treating absence as a value will create a spurious category.

**`ttarr` / `ttdep`** — planned UTC instants normalised by the publisher, so they *are* on the same axis as `tst` and may be compared with and differenced from it. `ttdep` never precedes `ttarr`, so `ttdep − ttarr` is a non-negative planned dwell. They must not be used as evidence that the vehicle was anywhere: they are plan. They are populated only during a stop relation, so any average over records where they are present is conditioned on that state and is not an average over the trip.

**`drst`** — nominal state encoded as 0/1. A mean of `drst` is the *fraction of messages* with a door open, which equals the fraction of *time* only under uniform sampling, which is not guaranteed. Its absence means the onboard system could not determine the state; treating absent as 0 will understate door-open time. Summing `drst` is meaningless.

**`occu`** — declared as a percentage with a QUDT-style observable property and a `measured` derivation, and it is nonetheless **not an observation for most of this feed**. Only Suomenlinna ferries report a measured value; every other vehicle class transmits a constant. The record carries no transport mode, so **from a record alone you cannot tell whether `occu` is data or filler**. It must not be averaged, summed, or compared across records until vehicle class has been established from outside this feed. In the example record `occu` is 0 with `drst` 0 and a vehicle moving at 8.42 m/s; a naive load model would read that as an empty bus, and there is nothing in these files that licenses that reading.

**Cross-record identity.** Any of the above per-trip or per-vehicle rules requires the right key. The physical vehicle is `(oper, veh)`. The trip is *not* `(oday, start)` alone despite the schema's wording — see §5.

# 4. Time

There are two time axes in this record, and they are not the same axis.

**`tst` is the phenomenon-time axis of the observations.** It is a UTC instant with millisecond precision, generated by the vehicle, marking when the vehicle sampled the state reported. Every observed value in the record — position, `spd`, `hdg`, `dl`, `drst`, `occu`, and the closing edge of `odo` and `acc` — is located at `tst`. Because it is UTC, positions on this axis map to civil time with no regime, no conversion, and no ambiguity, and instants from different vehicles, operators, days, and daylight-saving regimes are directly comparable. `ttarr` and `ttdep` are also normalised to UTC by the publisher and therefore sit on this same axis, which is what makes planned-versus-actual comparison possible at all.

**`journey_start` is a position on a different, non-civil axis: the operating-day regime.** Its coordinates are an operating day and a clock reading within that day. The operating day is not a calendar day — it runs past midnight and ends around 04:30 local time on the following calendar date. Two consequences follow, and both are traps.

First, `oday` looks like a date and is not one. A trip departing at 00:30 carries the *previous* calendar date as its `oday`. Any join, bucket, or partition that treats `oday` as the calendar date of the vehicle's activity will misfile every post-midnight trip by one day.

Second, `start` wraps within a single operating day. Because 04:30 is the origin, a `start` of `00:30` occurs *after* a `start` of `23:00` on the same operating day, so ordering on the raw `start` string, or on the `(oday, start)` pair lexically, is wrong at exactly the point where night service matters most.

The regime supplies its own remedy: `ordinal` renders the position at fixed width, most significant first, as `YYYY-MM-DD/MMMM`, where the minute component counts minutes elapsed since 04:30 local on the operating day. Because it is fixed-width and monotone, **lexical sort on `ordinal` is a correct chronological sort** without implementing the regime, and the ordering is forward — later positions sort later. The example is internally consistent: `2026-07-31/0165` is 165 minutes after 04:30, which is 07:15, matching `start`.

**Relating the two axes requires information not in these files.** The 04:30 origin and the `start` clock reading are stated to be *local* time. The files never name the local zone or its offset rules, so converting a `journey_start` position into a UTC instant — the thing you must do to compare a scheduled departure with `tst` — is not determined by the two files. Positions on the operating-day axis must not be compared with RFC 3339 instants until that conversion is supplied externally.

**Two members have periods with open lower boundaries.** `acc` characterises an interval closing at `tst` and opening at the previous message's timestamp, which is not carried. `odo` accumulates from the vehicle's actual trip start, which is also not carried and which `journey_start` does not supply, because `journey_start` is scheduled time and `dl` is precisely the size of the gap between schedule and actuality. Neither declares a support period, correctly, because neither has a length to declare. Both are therefore anchored at one end and floating at the other from the record alone; both become well-defined only by joining to neighbouring records in a stored stream.

Finally, the declared one-second cadence on `tst` is a statement about what the vehicle is expected to emit next. It is not a guarantee of uniform spacing and it explicitly does not bound the `acc` interval. Any time-weighted aggregate must use observed `tst` deltas, not the nominal cadence.

# 5. Ambiguities

**The local time zone is not named.** The operating-day origin of 04:30 and the `start` reading are "local time" and the zone is never stated. *This is a guess:* the description names the Helsinki region, so Europe/Helsinki (UTC+02:00 winter, UTC+03:00 summer) is the obvious candidate, and the example is consistent with a +03:00 offset — `tst` 05:12:44Z is 08:12:44 local, which is 57 minutes after the 07:15 scheduled first-stop departure, a plausible mid-trip position for a vehicle 95 seconds late. That is an inference from one record and a place name, not something the files establish.

**Daylight-saving behaviour of the `ordinal` minute count is not determined.** On a DST-transition day the operating day is 23 or 25 hours long, and nothing states whether the minute count reflects elapsed local clock minutes or elapsed real minutes, nor whether the 04:30 boundary itself shifts. I am declining to decide this. Lexical sorting still works; arithmetic on the minute component across such a day does not.

**The trip key is stated in a form that cannot be correct.** The schema says the `oday`/`start` pair "identifies the trip". Taken literally that is false — many trips on many routes depart at 07:15 on any given operating day. *This is a guess:* the intended key is `(route, dir, oday, start)`, possibly with `oper`. I am flagging the wording as an inconsistency rather than resolving it, because getting this wrong silently merges trips.

**`ttarr`/`ttdep` are attached to a stop whose relation to the vehicle's position is contradictory.** `stop` is documented on a `vp` event as the stop the vehicle *most recently departed from*, while `ttarr`/`ttdep` are the timetabled arrival and departure at "the stop named by `stop`" and are populated only during a stop relation. In the example both are `05:13:00Z`, sixteen seconds *after* `tst`, which is not consistent with a stop already departed. Either `stop` on this event names the upcoming stop, or the timetable values lead the position, or the vehicle is at the stop and `stop` is being populated on approach. I am declining to decide which. This matters directly: stop-level punctuality built on the wrong reading is offset by one stop.

**`dl` and `ttdep` are in tension in the example and the reconciliation is not stated.** `dl` is −95, meaning 95 seconds late, while the timetabled departure for the named stop is 16 seconds in the future. Nothing states which reference point `dl` is computed against — the trip origin, the current stop, the next timepoint, or a continuous interpolation of the schedule. Declining to decide; it changes how `dl` should be aggregated.

**`occu` is uninterpretable from a record alone.** The record carries no transport mode and no vehicle class, and the field is meaningful only for ferries. Whether the constant transmitted by other classes is `0`, and therefore whether the example's `occu: 0` is filler or a measurement, is not determined. Declining to decide. I would not publish any occupancy figure from this feed without an external vehicle-class mapping.

**Absence semantics are only partly specified.** `lat`/`long` are omitted when location is unavailable, and `loc` has an `N/A` member, but it is not stated whether `loc: "N/A"` implies the coordinates are absent, nor whether coordinates can be present with `loc: "N/A"`. Likewise `drst` is absent when undeterminable and `stop` is absent between relations, but nothing states whether these absences co-occur. Declining to decide.

**Ordering, duplication, and gaps in the stream are not addressed.** There is no sequence number and no statement about at-least-once delivery, out-of-order arrival, or replay. Since `tst` is generated by the vehicle rather than the broker, clock skew between vehicles is possible and unbounded by these files. This bears directly on `acc` and on `odo` differencing, both of which require correctly identifying the *adjacent* record. Declining to decide; I would treat de-duplication and reordering by `tst` within `(oper, veh)` as mandatory preprocessing.

**Authority between `ordinal` and `oday`/`start` is not stated.** They agree in the example. If a producer emitted an `ordinal` inconsistent with its own `oday`/`start`, nothing says which wins. Declining to decide.

**`odo` reset conditions beyond trip start are not enumerated.** The counter resets when the vehicle actually begins the trip. Whether it can also reset mid-trip — on a power cycle, a driver change, or a re-signon — is not stated. *This is an assumption:* any monotonicity violation in `odo` within a trip should be treated as a reset and the segment split, rather than as a negative distance.

**Subcontracting cannot be detected from the record.** `oper` is the operating operator and may differ from the owning operator carried on the MQTT topic, but the topic is not part of the record. Any analysis of subcontracting requires the transport envelope, which this feed as given does not preserve.

**`hdg` behaviour at rest is not specified.** Nothing states what heading a stationary vehicle reports — last known, zero, or held. Given `spd` can be zero, heading samples at rest may be meaningless and should probably be excluded from circular aggregates. Declining to decide; flagging so the exclusion is a conscious choice.

**`spd` provenance is not stated.** `loc` documents the procedure for `lat`/`long` only. Whether `spd` is derived from the same source — and therefore degrades in the same way during `ODO`/`DR` runs — is not determined, though `acc` is explicitly derived from `spd` and inherits its noise. Declining to decide.
