You are a supervisor. You grade four transcripts against a fixed list of claims.

You are not being asked whether a transcript is good, insightful, or well
written. You are asked, for each claim and each transcript, whether the
transcript got that specific matter right, got it wrong, declined to decide it,
or never touched it. Nothing else you think about the transcripts is wanted.

## Your stance

You are an adversarial grader. The transcripts were written by a different model
from a different vendor, and you are the hostile check on them. Assume each is
trying to appear more knowledgeable than it is, and grade so that appearance
earns nothing.

Credit is earned, never assumed. The default verdict is `unaddressed`, and a
transcript moves off it only by saying something specific enough that you can
point at the words. You are not rewarded for being fair to a transcript, and a
grader who credits an answer with something it did not quite say has failed at
this task. Being wrong in the direction of severity costs the evaluation far
less than being wrong in the direction of generosity, so where you genuinely
cannot decide, withhold the credit.

This severity applies identically to all four transcripts. You are hostile to
unearned credit, not to any particular transcript, and you must not go looking
for a transcript to punish.

You will be given:

* **CLAIMS** — numbered propositions. Each is true of the data the transcripts
  describe. Most carry a `wrong reading`: the specific error the claim exists to
  rule out.
* **TRANSCRIPT A**, **TRANSCRIPT B**, **TRANSCRIPT C** and **TRANSCRIPT D** —
  four independent readings of that data, produced under conditions you are not
  told. They are not in any meaningful order. Do not speculate about the
  conditions while grading.

For each claim, and separately for each of the four transcripts, choose exactly
one verdict. Every claim therefore receives four verdicts.

* `correct` — the transcript asserts the claim, or asserts something that
  entails it, as a statement it is standing behind.
* `incorrect` — the transcript asserts the wrong reading, or asserts anything
  else incompatible with the claim.
* `declined` — the transcript raises the matter and explicitly does not settle
  it: it says the files do not determine it, or it marks its answer as an
  assumption or a guess. **A transcript that states the correct answer but marks
  it as a guess or an assumption is `declined`, not `correct`.** Knowing that you
  do not know is a distinct outcome from knowing.
* `unaddressed` — the transcript never engages the matter at all.

Rules you must follow.

1. Judge only what is written. Do not credit a transcript for something you
   believe it meant, or for something a competent reader would obviously know.
2. For `correct` and `incorrect` you MUST supply `quote`: a verbatim span from
   that transcript, copied exactly, that carries the verdict. If you cannot find
   one, the verdict is `unaddressed`.
3. **The quote must carry the claim standing alone.** Read it with the rest of
   the transcript covered up. If someone who saw only those words would not
   learn the claim from them, the verdict is not `correct`, however clearly the
   surrounding paragraphs gesture at it. Naming the member, using the right
   technical term, or discussing the general area is not asserting the
   proposition.
4. **Look for the wrong reading before you look for the right one.** Search the
   transcript for the error the claim exists to rule out, and settle that
   question first. Only if the wrong reading is absent may you consider
   `correct`.
5. **A transcript that both asserts the claim and commits the wrong reading is
   `incorrect`.** Do not let a correct sentence elsewhere rescue it. Reciting a
   rule and then breaking it is worse than not knowing the rule, not better.
6. Do not round up. If a transcript gets part of a claim right and part of it
   wrong, and the wrong part is what the claim is about, that is `incorrect`. If
   the wrong part is incidental, it is `unaddressed`. It is not `correct`.
7. Do not use your own knowledge of the subject matter to decide a claim. The
   claim is the ground truth. If a transcript contradicts a claim, that is
   `incorrect` even if you personally believe the transcript.
8. Confidence is not evidence. Length is not evidence. A fluent, assured,
   well-organised transcript gets no benefit of the doubt over a terse one.
9. Grade the four transcripts independently. Do not let one inform another, and
   do not compare them. A matter that transcript C settles is still
   `unaddressed` in transcript A if transcript A never raises it.
10. Silence is not an error. A transcript that never touches a claim is
    `unaddressed`, and `unaddressed` is not a mark against it. Severity means
    withholding credit, not inventing violations.

Answer with JSON only, no prose before or after, in exactly this form:

```json
{
  "verdicts": [
    {"claim": 1, "transcript": "A", "verdict": "correct", "quote": "..."},
    {"claim": 1, "transcript": "B", "verdict": "unaddressed"},
    {"claim": 1, "transcript": "C", "verdict": "declined"},
    {"claim": 1, "transcript": "D", "verdict": "incorrect", "quote": "..."}
  ],
  "blinding": {"richest": "A" | "B" | "C" | "D" | "cannot tell", "why": "one sentence"}
}
```

The `blinding` field is not part of the grading and is not scored. It records
which transcript appeared to have had the most material available to it, and
whether you could tell at all. Answer it last, answer it honestly, and say
`cannot tell` if you cannot tell.


---

CLAIMS

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order lat, long. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. `tst` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `tst` as the time the record was produced, received, or published, or using a different member for event time.

3. Successive `tst` values are expected at cadence `fixed` with period "PT1S". A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

4. `journey_start` is an operational instant (`scheduledTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `journey_start` as the event time of the observation.

5. Positions in `journey_start` are expressed in the temporal reference system `#/definitions/OperatingDayClockPosition` (kind `type`), not in an unqualified civil clock.
   wrong reading: Reading `journey_start` as ordinary UTC.

6. `journey_start` is on a clock of its own. Converting it to civil time requires a synchronisation relation that the schema does not supply, so a correct reader declines the conversion or states the external input it would need.
   wrong reading: Converting `journey_start` to UTC as though the mapping were given.

7. `lat` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `lat`.

8. `long` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `long`.

9. `spd` is expressed in `m/s`.
   wrong reading: Assuming a different or conventional unit for `spd`.

10. `hdg` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `hdg`.

11. `acc` is calculated rather than measured directly.
   wrong reading: Treating `acc` as a direct measurement.

12. `acc` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `acc` as an instantaneous reading.

13. `acc` is expressed in `m/s2`.
   wrong reading: Assuming a different or conventional unit for `acc`.

14. `odo` is accumulated over the phenomenon-time period, not an instantaneous reading, so it may be summed across adjacent periods but not averaged as a rate without dividing by duration.
   wrong reading: Treating `odo` as an instantaneous value at a timestamp.

15. `odo` is expressed in `m`.
   wrong reading: Assuming a different or conventional unit for `odo`.

16. `dl` is calculated rather than measured directly.
   wrong reading: Treating `dl` as a direct measurement.

17. `dl` is expressed in `s`.
   wrong reading: Assuming a different or conventional unit for `dl`.

18. `ttarr` is an operational instant (`scheduledTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `ttarr` as the event time of the observation.

19. `ttdep` is an operational instant (`scheduledTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `ttdep` as the event time of the observation.

20. `occu` is expressed in `%`.
   wrong reading: Assuming a different or conventional unit for `occu`.


TRANSCRIPT A

# 1. What this feed is

Each record is one instantaneous state sample taken *by a transit vehicle about itself* while it is running a scheduled trip. The subject — the feature of interest — is the physical vehicle, identified only by the pair (operator, vehicle number); the vehicle number alone does not identify anything. The record says where the vehicle was, how fast it was going and in what direction, how far it has run since it actually began the trip, how far off its timetable it is, whether a door was open, and, nominally, how full it is. Alongside that it carries the identity of the trip being run and, when the vehicle is in a stop relation, the timetabled arrival and departure for the stop it most recently left.

Sampling is per vehicle, at a nominal one message per second, so the volume is dominated by whichever vehicles are in service longest, not by whichever are most interesting. This is a *position* stream, not an event stream: there is no arrival event, no departure event, no cancellation, and no trip-completion marker in it. A trip's beginning and end have to be inferred, and the record does not carry the one instant that would make that inference safe (see §4).

One further point of shape matters. The record carries several independent results — position, speed, heading, acceleration, distance run, schedule deviation, occupancy — and these are separate observations that happen to share a carrier, not components of one combined measurement. None of them carries its own quality qualifier, and nothing in the feed states that any of them is good. Absence of a quality statement is not a statement of acceptable quality.

# 2. Analytics

**Schedule adherence and its evolution along a trip.** The deviation from timetable is carried directly, on every message, anchored to the trip's scheduled first departure, and it is stated in seconds. Because it arrives at ~1 Hz rather than once per stop, you can profile *where along a trip* lateness accrues and where it is recovered, which stop-event feeds cannot do. This is the strongest analysis the stream supports.

**Speed profiles and congestion location.** Speed is declared a directly measured, instantaneous quantity in m/s, and it arrives with a WGS 84 position on the same record. Binding speed to location over many trips gives per-link speed distributions and identifies where the network is slow, by time of day and direction.

**Trajectory reconstruction and distance run.** The odometer is a per-trip accumulator, reset when the vehicle actually starts the trip. Differences of it between two messages of the same trip give distance covered over that span, independent of position accuracy — which makes it the better basis for distance-based work than differencing coordinates, particularly during the intervals when the position is not satellite-derived.

**Dwell behaviour at stops.** The door-state flag plus the stop identifier let you bracket door-open episodes and attribute them to a stop. This is the only handle the feed gives on passenger service time.

**Positioning-quality auditing, and stratification of everything above by it.** The feed states, per message, the procedure that produced the coordinates, and states that this changes without warning within a single trip. That makes it possible to measure how much of the network is covered by dead-reckoned or odometer-propagated rather than satellite-fixed position, and — more importantly — to exclude non-satellite spans from any analysis whose conclusion depends on positional accuracy. Procedure identity is comparability-critical; equal procedure is grounds for grouping, not proof that two values are interchangeable.

**Headway and bunching between vehicles on a route.** Supportable in principle: multiple vehicles report against the same route and direction on a common UTC axis. It is the weakest of these, because the timestamps are generated by the vehicles themselves and nothing in the feed establishes that vehicle clocks agree.

**Schedule-versus-actual at the stop level.** The timetabled arrival and departure are normalised to UTC instants, so they can be compared against the observation instant. This yields a *different* quantity from the carried deviation figure, and the two must be kept apart (§3).

**Occupancy — only for one vehicle class.** See §3; for almost every vehicle this member is not an observation at all.

# 3. Combination rules

**Vehicle number and operator.** Identifiers, never arithmetic. The vehicle number is unique only in combination with the operator, so grouping, joining, or counting distinct vehicles on the number alone merges vehicles belonging to different operators. The operator carried here is the one actually running the trip and may differ from the owning operator when a service is subcontracted; the owning operator is not in the record, so subcontracting is not detectable from records alone.

**Observation instant.** Comparable, differenceable, and orderable across all records without qualification: it is a UTC instant with millisecond precision. Differences are elapsed seconds. The declared one-second cadence is an expectation about the producer, not a guarantee: it does not assert that every second has a record, does not license filling a gap, and does not bound any interval quantity. Do not integrate anything by assuming a fixed 1 s step; weight by the actual timestamp spacing.

**Trip anchor (operating day and departure clock reading).** Positions in this regime may be *ordered* — but only via the fixed-width ordinal rendering, under plain lexical order, increasing with time. Ordering on the raw clock reading is wrong, because it wraps within a single operating day: `00:30` on an operating day comes after `23:45` on the same operating day. The operating day is not a calendar day and must not be joined to a calendar-date column. A position in this regime must not be compared with a UTC instant without applying the regime, and the files supply no synchronisation relation to UTC. Within one operating day the ordinal's minute component is minutes since 04:30 local, so differences within one operating day are minutes; across operating days no metric difference is established.

**Route label versus route identifier.** The head-sign label is a display string and is explicitly not the GTFS route identifier. Group, join, and aggregate on the identifier. The files do not establish that the label is unique, so aggregating on it may merge distinct routes.

**Direction.** Equality only. It is not a bearing and carries no geometry. Its two values mean "the direction declared first in the GTFS feed for this route" and "the other one" — so direction "1" on one route bears no relation to direction "1" on another beyond that ordering accident. Never averaged, summed, or treated as numeric despite being carried as digits.

**Latitude and longitude.** Read them in the declared axis order — latitude first, longitude second — under WGS 84 as EPSG identifies it. They may be compared as positions and used to compute distances by an appropriate geodetic method. They must not be treated as ordinary numbers to average: an arithmetic mean of degrees is not a meaningful location, and no coordinate transformation is authorised by the schema. Both are optional; when the location is unavailable they are simply absent, and absence must not be read as (0, 0). Crucially, positions produced by different procedures are not interchangeable: mixing satellite fixes with odometer-propagated, dead-reckoned, or hand-entered coordinates in the same accuracy-sensitive computation is invalid without an external error model, which neither file supplies.

**Speed.** Comparable, differenceable, and averageable across records as a like quantity — same unit, same declared production, same phenomenon. But a mean over messages is a *sample* mean, not a time-weighted mean, and the two differ whenever message spacing varies, which the cadence expectation does not prevent. Time-weight by actual timestamp gaps. Speed does not sum across records.

**Heading.** Degrees clockwise from geographic north, in [0, 360]. This is a circular quantity: it may be compared, but it must not be linearly averaged or linearly differenced. The mean of 359 and 1 is not 180, and a naive difference between them is not 2 degrees. Circular statistics or vector averaging is required. The endpoints 0 and 360 denote the same direction, so equality tests on the raw number can fail for identical headings.

**Acceleration.** This is the one quantity that must essentially not be combined. It is a calculated difference between the current speed sample and the preceding one, divided by the interval between them; that interval closes at the observation instant and opens at a timestamp *the record does not carry*, and its length varies. The schema declares this explicitly and declares no support period, which means the temporal extent of what each value characterises is indeterminate from the record. Two acceleration values therefore characterise intervals of unknown and different length. They must not be summed, integrated, or averaged, and comparing two of them is comparing quantities over incomparable supports. The one-second cadence does not bound this interval — the schema says so directly, and cadence may not be used to supply a missing interval end in any case. The value is also undefined for the first message of a trip, and if you dropped an intervening message the interval is longer than you would suppose.

**Odometer.** An accumulator with a per-trip origin at the *actual* start of running. Differences within one trip of one vehicle, taken between two messages with no reset in between, are valid distances in metres. Absolute values must never be compared across trips or across vehicles, because each is measured from a different and unstated origin. It must never be summed across records — summing an accumulator counts the same distance repeatedly. Averaging it is meaningless. A decrease between consecutive messages of the same identified trip indicates a reset, not negative travel. Note that the scheduled departure does *not* give you the origin: the schedule anchor is a planned time, and the gap between plan and actual running is precisely what the deviation figure measures.

**Schedule deviation.** The sign convention is inverted relative to the usual one: **negative means late, positive means early**. This is the single most dangerous item in the feed, because every naive result stays plausible. The "worst" delay is the *minimum*, not the maximum; a percentile of lateness is the complementary percentile of this member; a mean that comes out negative means the service is late on average, not early. Values are comparable, differenceable, and averageable across records, trips, routes and operators as a like quantity, since each is the same declared quantity in seconds. They must not be *summed*: this is a level, not an extensive quantity, and adding lateness across messages of one trip counts the same lateness once per second. Beware sampling weight: because sampling is per vehicle per second, a mean over messages weights slow and long-running trips more heavily than short ones, so a message-mean is not a trip-mean and not a passenger-weighted mean.

**Schedule deviation versus timestamp-minus-timetable.** These are two different quantities and must not be pooled or used interchangeably. The deviation figure is computed onboard against the trip's schedule anchor; the difference between the observation instant and a timetabled stop time is a different construction against a different anchor, with the opposite sign sense. The example record demonstrates the divergence: it reports a deviation of −95 s, which under the declared convention is 95 seconds *late*, while the observation instant falls about 16 seconds *before* the timetabled arrival for the stop it carries. I do not attempt to resolve which is correct; the point is that a pipeline that computes lateness both ways and mixes the results is producing a mixture of two quantities.

**Stop identifier.** An identifier, equality only, never arithmetic and never ordinal. On these position records it names the stop most recently *departed* — not the next stop, and not an arrival. It is absent between stop relations, so a stream of records does not enumerate stops served; counting distinct values gives stops departed, and only those observed.

**Timetabled arrival and departure.** Planned times, not observed ones. They may be compared with each other — departure never precedes arrival, so their difference is planned dwell — and with observation instants, since all three are UTC. They must never be read as when the vehicle actually arrived or departed. They are populated only while the vehicle stands in a stop relation, so their absence carries no information about the vehicle's behaviour.

**Door state.** A state, not a quantity. Equality only; never summed or averaged as 0/1 without deciding what the denominator is. It is *absent* when the onboard system cannot determine it, and absence must not be collapsed to "closed". Door-open durations obtained by differencing observation instants across a state transition are bounded by the messages you actually received, and the cadence does not guarantee you received the transition promptly.

**Occupancy.** Do not combine at all without external information the feed does not carry. Only Suomenlinna ferries report a measured value; every other vehicle class transmits a constant. Nothing in the record states the transport mode, so from a record alone you cannot tell an observation from a placeholder. Averaging this member across a mixed fleet mixes measurements with constants and produces a number with no referent. The example record shows 0 on a bus-style service; that 0 is a filler, not evidence of an empty vehicle.

**Trip identity for any of the above.** Group by (route, direction, operating day, scheduled start) together with (operator, vehicle). The schema asserts that the operating-day/start pair "identifies the trip", which cannot hold across routes, since many routes have a 07:15 departure on the same operating day. Keying on the pair alone will merge unrelated trips.

**Missingness generally.** Only the vehicle, operator, observation instant, trip anchor, route label, route identifier, direction and position-source are guaranteed present. Every measured quantity may be absent, and absence means undeclared — never zero, never unchanged, never acceptable.

# 4. Time

The time axis of the thing described — the vehicle's motion — is established by the observation timestamp, which is declared the phenomenon time: the instant at which the vehicle sampled the state the record reports. It is a UTC instant with millisecond precision generated onboard, so positions on this axis relate to civil time directly and without a regime: it *is* civil time, in UTC, and converting to Helsinki local time is an ordinary time-zone conversion.

Three qualifications matter.

First, the trip anchor lies on a **different axis**, not on this one. It is a planned position in an operating-day regime whose day boundary falls at roughly 04:30 local, whose day label is not a calendar date, and whose clock component wraps within one day. It orders correctly only through its fixed-width ordinal rendering, and it increases with time. Nothing in the two files supplies a conversion from that regime to UTC. You can construct one — take the operating day, add the clock reading, roll to the next calendar date for readings before the day boundary, and convert from local time — but only by supplying the local time zone yourself, which the files do not name (see §5).

Second, two quantities reference **intervals whose opening boundary the record does not carry**. The acceleration figure characterises the gap back to the previous message, whose timestamp is not in the record and whose length varies. The odometer accumulates from the instant the vehicle actually began the trip, which is likewise not in the record and is not the scheduled departure. In both cases the extent is indeterminate from a single record; neither the scheduled anchor nor the declared cadence supplies it, and the schema says so explicitly for both.

Third, the timetabled stop times are UTC instants on the same civil axis as the observation timestamp, but they are *planned* positions. They locate a point on the axis where something was supposed to happen; they are not observations and give no boundary to any observed quantity.

The declared one-second cadence describes expected producer behaviour on the observation timestamp. It is not a completeness claim, not a delivery guarantee, and not an interval boundary: it does not assert a successor message exists, and a stream that misses a beat is late, not malformed.

Finally, the feed carries **no publication or ingestion time**. There is no way from a record to know how old it was when it reached you, so end-to-end latency and out-of-order arrival cannot be measured from the data.

# 5. Ambiguities

- **The local time zone is never named.** The operating-day regime is defined in "local" time, but which local time is not stated. Given the feed is stated to serve the Helsinki region, I *guess* Europe/Helsinki — marked as a guess. Every conversion of a trip anchor to UTC depends on it.
- **Daylight-saving behaviour of the operating day.** How the 04:30 boundary and the minutes-since-boundary count behave across a DST transition — whether a day gains or loses sixty minutes of ordinal — is not determined. I decline to decide it.
- **The exact day boundary.** The regime is described as ending "at approximately 04:30". "Approximately" leaves undetermined which operating day a departure near 04:30 belongs to, and whether a departure slightly before it yields a negative or wrapped minute count. Declining.
- **Trip identity.** The schema asserts the operating-day/start pair identifies the trip. Taken literally that is false across routes. I decline to decide what was meant; §3 gives the conservative key, which is an assumption on my part, not something the files state.
- **Vehicle clock agreement.** Timestamps are generated by the vehicles. Nothing establishes that two vehicles' clocks are synchronised, which is a precondition for headway and bunching work. Declining — this needs an external statement about the fleet.
- **Which vehicles are ferries.** The occupancy caveat requires knowing the transport mode, and no member carries it. Neither file maps any route identifier or head-sign label to a mode. Declining; this must come from a source the files do not reference.
- **The constant that non-ferry vehicles transmit for occupancy.** The example shows 0. I decline to conclude that the constant is always 0, or that it is the same for all vehicle classes.
- **Whether speed remains a direct reading under non-satellite positioning.** Speed is declared directly measured, but that declaration is a property of the type and does not vary per record, while the positioning procedure does vary per record. Whether speed is still a direct reading when the position is dead-reckoned or odometer-propagated is not determined. Declining.
- **What constitutes a "stop relation."** The stop identifier and the timetabled stop times are populated only while the vehicle is in one, but the geometric or logical criterion is not given, so you cannot reproduce the publisher's segmentation. Declining.
- **How timetabled stop times were normalised to UTC.** The publisher normalises them; the rule — in particular which calendar date is chosen for a trip that crosses midnight — is not stated. Declining.
- **Heading conventions at the edges.** Whether 0 and 360 are both emitted, and what value if any is emitted when heading is unknown, is not determined. The reference direction *is* determined: geographic, not magnetic, north.
- **Position present but source unhelpful.** The position source is required while the coordinates are optional, so a record may declare a satellite fix and carry no coordinates. What the source describes in that case is not determined. Declining.
- **Direction beyond two values.** Only two direction values exist. How circular routes, or routes with more than two GTFS directions, are represented is not addressed. Declining.
- **Head-sign label uniqueness.** Not established. I assume it is not unique and recommend against grouping on it; that is my assumption, not a fact from the files.
- **Deviation before the vehicle actually starts running.** The deviation is computed against the schedule anchored at the planned first departure, while the odometer resets at actual start. Whether deviation is meaningful, or emitted at all, before actual start is not determined.
- **Bounds and clamping of the deviation figure.** No range is stated, so an extreme value cannot be distinguished from a sentinel. Declining.
- **The observable-property definitions are unresolvable.** The record-level property, the schedule-deviation property and the occupancy-ratio property all cite an example catalogue that does not resolve. Their precise definitions are therefore unavailable — indeterminate rather than wrong. Anything that depends on the exact definition of "schedule deviation" or "occupancy ratio" beyond what the descriptions say cannot be settled from these files.
- **No quality and no provenance per result.** Nothing carries a result-quality qualifier and nothing identifies the act that produced a value. The absence is not evidence that the data is good.


TRANSCRIPT B

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


TRANSCRIPT C

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


TRANSCRIPT D

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
