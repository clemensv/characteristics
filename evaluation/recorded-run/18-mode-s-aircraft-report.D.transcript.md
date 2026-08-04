# Mode-S / ADS-B downlink feed — analyst's briefing

## 1. What this feed is

Each record is **one reception event at one ground station**, not one state of one
aircraft. A radio transmission left an airframe, a particular receiver heard it,
a decoder turned it into fields, and the result was forwarded. The airframe is
named by its 24-bit ICAO address; the station that heard it is named as well,
and the schema is explicit that the station is *the procedure that produced every
value in the record*.

Two consequences follow immediately, and they are the two things most likely to
be got wrong:

- **The feed is a census of receptions, not of aircraft.** The same transmission
  heard by two stations becomes two records that legitimately disagree — in
  signal level, in timestamp, and sometimes in the decoded position itself,
  because position is reconstructed from a *pair* of messages and two stations
  may have caught different pairs. Any count, rate, or density computed without
  first collapsing on aircraft identity measures receiver coverage, not air
  traffic.
- **The records are heterogeneous by construction.** The downlink-format family
  governs which members carry meaning. There is no single "aircraft state" row
  here; there are position rows, identity rows, velocity rows, altitude replies,
  all-call replies, and Comm-B replies, flattened into one shape. Treating the
  shape as a uniform observation table will silently mix quantities that were
  never measured together.

The values themselves are decoder *outputs*, not sensor readings. Position is a
solution to an ambiguous encoding. The Comm-B register code is an inference from
a bit pattern and can be inferred wrongly. Altitude is a pressure-derived
quantity, not a height. Nothing here is a raw measurement of the world.

## 2. Analytics this stream supports, and why

**Trajectory reconstruction per airframe.** Grouping on the ICAO address and
ordering by the decode timestamp gives a track, because the address is present in
every format and is the only identifier that is. Positions come only from the
subset of records that carry them, so the track is irregularly sampled and its
sampling rate is a property of the receiver's luck, not of the aircraft.

**Receiver coverage and station performance.** The station identifier plus the
signal level make it possible to characterise each station separately: message
volume, the altitude and bearing distribution of what it hears, and where in its
own dynamic range the receptions sit. The schema states that signal level is
comparable *within* a station, which is exactly what a coverage study needs and
exactly what a cross-station comparison must not assume. Note that the station's
own location is not in the data, so range-based coverage requires an external
source.

**Multi-station reconciliation and de-duplication.** Because the same
transmission can appear more than once, the data supports measuring the
redundancy of the network, and — as a side effect — cross-checking decodes: two
stations reporting materially different positions for the same aircraft at
effectively the same instant indicates a decode problem, not aircraft motion.
This analysis is a prerequisite to almost every other one.

**Emergency and special-condition detection.** The squawk carries three reserved
values whose meaning, per the schema, *overrides* the assignment. Alerting on
these is directly supported and needs no inference.

**Flight-leg segmentation.** The callsign is the flight identity and changes
between legs while the airframe address does not. The pair therefore supports
splitting a continuous airframe history into legs — with the caveat, stated in
the schema, that the callsign is crew-entered and frequently wrong or blank, so
segmentation must tolerate absent and bogus values.

**Vertical-profile and level-occupancy analysis.** Barometric altitude over time
per airframe yields climb, cruise and descent structure, and occupancy of
pressure surfaces. Vertical rate corroborates the direction of change. This is
supported for *shape*; it is not supported for geometric height (see §3).

**Data-quality and decoder-health monitoring.** Signal level, per station, marks
messages decoded near the noise floor, which the schema identifies as the origin
of bit errors that survive the parity check. Cross-tabulating implausible values
(impossible position jumps, absurd rates) against signal level gives a defensible
quality filter. Likewise, the distribution of Comm-B register codes is worth
monitoring precisely because that code is inferred and can be inferred wrongly.

**Field-population profiling by message family.** Because the message family
determines which members are populated, deviations from the expected population
pattern are themselves a signal about the feeder — and this feed's own example
record shows such a deviation (see §5).

## 3. Combination rules, quantity by quantity

**ICAO address.** Equality only. Groups records into airframes; never arithmetic.
It identifies the *airframe*, not the flight, so grouping by it spans legs, and
not the *operator* either. Whether an address is ever reassigned to a different
airframe over time is not established here.

**Station identifier.** Categorical. It must appear in the grouping key of any
count, rate or density, because a count aggregated over stations counts
receptions, not events. It may not be averaged over, and it may not be dropped
before de-duplication.

**Message family, downlink format, type code.** These are numeric-looking labels,
not quantities. Never sum, average or difference them. A mean downlink format is
meaningless. They may be compared for equality and used to partition.

**Comm-B register code.** Categorical, and inferred rather than transmitted.
Counts by register code carry an unknown misclassification rate; do not present
them as ground truth.

**Timestamp.** Differences *within a single station* are meaningful and are the
basis of all rate and interval work. Comparisons and differences *across
stations* silently assume the stations' clocks agree; the files do not establish
that they do, nor what clock discipline is used. Summing timestamps is
meaningless; averaging them is defensible only as a deliberate midpoint. Crucially,
a difference of two timestamps is a difference of *decode* instants, not of the
instants at which the reported states were true — see §4.

**Callsign.** String equality after trimming, since the schema states it is padded
to eight characters (the padding character itself is not stated — assuming spaces
is a guess). Not a stable join key: it is per-leg, crew-entered, and may be wrong
or blank. Do not use it to identify an airframe, and do not treat two records with
the same callsign as necessarily the same flight without corroboration.

**Squawk.** Octal digits held as text. Never arithmetic — the codes are not
magnitudes and octal text will mis-sort or mis-parse if coerced to a number.
Compare for equality; treat the three reserved values as a separate, dominating
category.

**Barometric altitude.** May be compared and differenced *as a pressure surface*.
Two records with the same value are on the same pressure surface; they are **not**
at the same geometric height, and the schema says so explicitly. Therefore:

- Differencing two aircraft's values gives vertical separation on the pressure
  reference — legitimate, and the intended use.
- Differencing one aircraft's values over time gives change on that reference,
  which is not exactly a change in geometric height, because the offset varies
  with the state of the atmosphere and is not transmitted.
- **Do not** combine these values with any geometric or ellipsoidal height, nor
  with terrain, nor convert to height above ground. The correction term is not in
  this data.
- Averaging across different aircraft yields a mean pressure surface, which is
  rarely the quantity anyone actually wants.

**Latitude and longitude.** Comparable and differenceable as coordinates.
Longitude differences must be scaled by the cosine of latitude before being
treated as distances, and averaging raw degrees to obtain a centroid is invalid
across the antimeridian; both are properties of the coordinate system the schema
names, not domain facts imported from elsewhere. More important here: these are
*solutions*, not readings. Two stations decoding the same aircraft may resolve
slightly different positions; that difference is decoder disagreement, not motion,
and must not be turned into a velocity. There is no accuracy or integrity
indicator in this feed, so position uncertainty cannot be quantified from it.

**Speed.** Knots — but the schema states the subtype bit distinguishing ground
speed from airspeed has been discarded. This is a hard barrier: two speed values
may not be differenced, averaged, or compared unless you have independently
established that they are the same kind of speed, and this data cannot establish
that. In particular, do **not** validate this value against a speed derived from
successive positions, and do not mix it into a single distribution — such a
distribution is a blend of two different physical quantities. Any aggregate over
speed should be reported with that contamination stated.

**Angle.** Two independent hazards. First, it is circular: the arithmetic mean of
degrees is wrong across the 0/360 wrap, and 0 and 360 are both permitted for the
same direction, so equality tests must normalise. Circular statistics are required.
Second — and this is the one that will not show up as an obvious outlier — the
same discarded subtype bit means the value is track over the ground in some
records and magnetic heading in others, and the schema states these differ by
drift angle and by magnetic variation. Differencing two angle values from
different records is therefore not defined. Do not compute turn rates from it
without first establishing the subtype from outside this feed.

**Vertical rate.** Feet per minute, positive upward; may be compared and averaged
*within* one airframe and one assumed source. It cannot be reconciled with the
altitude member, because the bit stating whether it was computed barometrically
or geometrically is not forwarded. Concretely: integrating vertical rate and
expecting it to reproduce the altitude series is unsound, and any discrepancy you
find is uninterpretable — it may be the source mismatch rather than an error.

**Signal level.** Decibels relative to each receiver's own full scale.
**Never compare, difference or average across stations** — the schema says the
scale is receiver-specific, so a cross-station mean is a number without a
referent. Within one station the values are meaningful and ordinal, and are the
right tool for identifying marginal decodes. Because they are logarithmic,
summing them is meaningless and a mean of decibel values is not the decibel value
of the mean power; if you want an average power, convert out of the log domain
first. Whether that is the right thing to want is a modelling decision this data
does not make for you.

## 4. Time

The single timestamp member is the time axis of **the observation**, not of the
thing observed. It is the instant the ground station decoded the transmission,
expressed as milliseconds since the POSIX epoch, and it therefore lands directly
on civil UTC. The example record's value corresponds to
**2026-07-31 05:12:44.316 UTC**. (POSIX counts do not represent leap seconds; that
is a property of the encoding rather than something these files assert, so treat
sub-second alignment across a leap second as undetermined.)

The critical point: **the reported aircraft state has no time axis in this feed.**
The schema states plainly that Mode-S transmissions carry no timestamp, so the
instant at which the state was true aboard the aircraft is unavailable and can
only be *bounded* by the transmission interval of the format concerned — and that
interval is not given anywhere in these two files. So:

- The latency between "state was true" and "state was decoded" is **not
  determined** by this data. You can order events; you cannot date the states.
- Interpolating a track between two position records assumes the decode times are
  a faithful proxy for the sample times. That assumption is not supported here,
  only unrefuted.
- Because position is resolved from a *pair* of messages, a position record's
  timestamp is the decode instant of the later message of a pair whose span is
  unknown to the consumer. The effective position epoch is therefore earlier than
  the timestamp by an unstated amount.
- Ordering records from *different* stations on one axis requires their clocks to
  be mutually disciplined. Nothing here says they are. Within a station, ordering
  is sound.

## 5. Ambiguities

**The example record is internally inconsistent with the schema's own population
rule, and this is the most consequential open question.** The record is declared
as an extended-squitter position message whose type code means airborne position,
yet it also carries a callsign (identification messages), a squawk (identity
replies), and speed, angle and vertical rate (velocity messages). The schema says
the message family "determines which members of this record are populated". Two
readings are possible: the feeder maintains per-aircraft state and stamps each
outgoing record with the most recent known value of every member; or the example
is a synthetic composite that no real record resembles. **I decline to decide
which.** The choice matters enormously: under the first reading, most members in
a record are *stale* by an unknown amount and do not share the record's timestamp,
which invalidates any analysis that treats a record as a simultaneous
observation. An analyst must settle this against the feeder before proceeding.

**Altitude for geometric-reference position messages.** The type code member says
codes 20–22 carry airborne position referenced to a *geometric* altitude, while
the altitude member is described unconditionally as barometric. What the altitude
member contains in a type-20-to-22 record is **not determined**. Do not assume it
is barometric there.

**Timestamp encoding.** The example carries the timestamp as a JSON string while
the schema types it as a 64-bit integer. The numeric value is unambiguous; which
form is normative on the wire is **not determined**, and a consumer should accept
both.

**Surface and other type codes.** The type-code description accounts for
identification, airborne position, velocity, and geometric-reference position. It
says nothing about the remaining codes, so how surface-position or status
messages appear in this feed — or whether they appear at all — is **not
determined**. There is also no air/ground indicator anywhere, so distinguishing
airborne from surface records is not possible from this data alone.

**Absence semantics.** Only five members are mandatory. Whether an absent member
means "the message did not carry it" or "the decoder failed on it" is **not
determined**, and the two have opposite implications for quality metrics.

**Completeness and gaps.** There is no sequence number, no message counter and no
gap indicator, so a quiet interval cannot be distinguished from a missed
reception. Any duty-cycle or "aircraft last seen" metric therefore conflates
aircraft behaviour with receiver performance. This is a limitation, not an
ambiguity — but it is one analysts routinely fail to state.

**Station clock discipline and station location.** Neither is given. Cross-station
time alignment and range-based coverage both require external information.

**Signal-level reference.** The full-scale reference is per-receiver and its value
is not published in the feed, so signal levels cannot be normalised into a common
scale even in principle from this data.

**Whether upstream de-duplication has already occurred.** Not determined. The
schema's language implies duplicates are expected, but it does not say the
consumer receives them un-collapsed. Verify before counting anything.

**Callsign padding character.** Not stated. That it is spaces is a **guess**.

**Address stability.** That an ICAO address maps one-to-one and permanently to an
airframe is not asserted; only that it is assigned by the state of registry.
Treating it as a durable primary key across long time spans is an **assumption**.
