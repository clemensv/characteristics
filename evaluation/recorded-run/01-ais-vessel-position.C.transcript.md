# Reading the feed

## 1. What this feed is

Each record is one self-reported position-and-motion observation transmitted by a
single shipborne station, decoded from an AIS radio message and relayed by a
third-party aggregator. The station is identified by a nine-digit MMSI, which the
schema names as the feature of interest: the thing being observed is the
*station*, and only by implication the vessel carrying it.

The class of equipment matters for how the stream behaves. These are Class B
units — the schema says so, and says the message type carries no navigational
status field. So the feed tells you *where a station was, how fast it was moving,
which way it was going, and which way its bow pointed*, plus a handful of
integrity flags and a description of what the radio can do. It does not tell you
the vessel's name, type, size, draught, destination, or whether it is under way,
anchored or moored. Those are simply absent, not implied.

Two further facts shape everything downstream. Reception is via a **terrestrial**
receiver network, per the description of `TimeReceived` — so the spatial extent of
the feed is the extent of that shore-based network, not the world's oceans. And
the reporting cadence is declared **irregular**, so this is an event stream, not a
sampled time series.

## 2. Analytics worth running

**Per-station track reconstruction.** The schema designates `UserID` as the
feature of interest and gives position, speed, course and heading as observation
values sharing one phenomenon time. That is exactly the shape needed to group by
`UserID`, order in time, and reconstruct a trajectory.

**Cross-validation of reported motion against inferred motion.** `Sog` and `Cog`
are both marked `derivation: measured` — they come from the station's own
position-fixing system, not from differencing successive reports. That makes them
*independent* of the speed and bearing you can compute from consecutive
positions. Disagreement between the two is therefore informative: it flags decode
errors, gaps you did not notice, duplicate or colliding identities, or
implausible reports.

**Drift / crab angle.** `Cog` and `TrueHeading` are both in degrees *true* and are
co-observed at the same instant on the same station. Their signed circular
difference is a physically meaningful quantity — the angle between where the hull
points and where it actually travels. This is one of the few genuinely derived
quantities the feed supports without external data.

**Ingest latency characterisation.** `TimeReceived` is explicitly the aggregator's
receipt instant and `Timestamp` the fix instant; the difference is the
propagation-and-queueing delay of the receiver network. You can profile that
delay by region and by hour. This is worth doing for its own sake *and* because
the whole time reconstruction in §4 depends on that delay staying below one
minute.

**Data-quality surveillance.** Three members carry `semanticRole: resultQuality`
(`Valid`, `PositionAccuracy`, `Raim`). Rates of decode failure, of low-accuracy
(non-differential) fixes, and of RAIM-disabled receivers are directly measurable
and are the correct filter to apply before any positional analysis.

**Equipment census of the Class B population.** The four `ClassB*` capability
flags and `ClassBUnit` describe the transponder, not the observation. Aggregated
over *distinct* stations they give a picture of what hardware is actually in the
water. See §3 for the de-duplication requirement that makes or breaks this.

**Traffic density and dwell.** Position plus speed supports occupancy maps and
stationarity detection — with the heavy caveat, below, that record counts are not
vessel counts.

## 3. Combination rules

**`UserID`** — nominal identifier. Compare for equality only. Never differenced,
summed, averaged, ranged or binned as a number; the arithmetic is meaningless.
The schema says "nine-digit identity" but stores it as `int32`, so any value with
fewer than nine digits has lost leading zeros. Zero-pad to nine characters before
joining against any external identity list, or the join will silently miss rows.

**`Latitude` / `Longitude`** — angular coordinates in EPSG:4326, with axis order
explicitly declared as Latitude-then-Longitude. Comparable and, over short local
extents, differenceable. **Not** to be summed. Arithmetic means of latitude and
longitude are not the centroid of a set of positions on a sphere, and a mean
longitude is outright wrong for any set straddling the antimeridian; use a
geodetic aggregation if you need a centre. Distances must be computed
geodesically — a Euclidean distance in degrees is not a distance, and one degree
of longitude is not one degree of latitude except at the equator. Because the
declared axis order is the opposite of GeoJSON's, expect a transposition bug at
any hand-off to mapping tooling.

**`Sog`** — a ratio-scale quantity in knots; comparable, differenceable,
averageable. Two conditions. First, records are irregularly spaced, so a plain
mean over records is a *sample* mean weighted by reporting rate, not a mean over
time; time-weight it if you want mean speed over a passage. Second, each value is
instantaneous at its fix, not an interval average, so integrating speed to obtain
distance requires an explicit assumption that speed persisted between samples.
Converting to SI requires the knot-to-metre-per-second constant, which is not in
these files.

**`Cog` and `TrueHeading`** — circular quantities. They must **not** be averaged,
summed or differenced with ordinary arithmetic: the mean of 359° and 1° is 0°, not
180°, and a naive difference of those two values gives 358° instead of 2°. Use
circular statistics for aggregates and the smallest signed angular difference for
comparisons. They also must **not** be pooled with each other or with
`Latitude`/`Longitude` merely because all four carry the unit `deg`: course over
ground, compass heading and geographic coordinates are three different things
that share a unit symbol. `Cog` and `TrueHeading` *may* be differenced against
each other, because both are referenced to true north and both are observed at
the same instant on the same station — that difference is the drift angle above.

**`Timestamp`** — this is the trap. It is a **second of the minute**, not an
instant. Differencing two `Timestamp` values gives a number that is wrong whenever
the two fixes fall in different minutes, which is most of the time. It must never
be summed or averaged. Worse, the values 60–63 are not seconds at all: they are
status codes meaning respectively that no time is available, that the positioning
system is in manual input, in dead reckoning, or inoperative. Feed those into any
numeric aggregate and you have corrupted it. They must be partitioned out first,
and 62 and 63 in particular should be treated as a positional-quality signal in
their own right.

**`TimeReceived`** — a true instant on a common axis: the schema attributes it to
one ingest service, so values from different records are on the same clock and
may be compared and differenced. What the files do *not* establish is that this
clock is disciplined or monotonic, so treat latency outliers as possible clock
artefacts rather than certain network delay. Never difference `TimeReceived`
against a *different* record's phenomenon time and call the result a physical
duration; that mixes two axes.

**`Valid`, `PositionAccuracy`, `Raim`** — quality flags. Meaningful as *rates* over
an explicitly defined denominator; not differenceable. A rate computed per record
is weighted by how often each station transmits, so a handful of chatty stations
can dominate. Decide deliberately whether you want a per-record rate or a
per-station rate — they answer different questions.

**`AssignedMode`, `ClassBUnit`** — marked `status`: the station's current operating
state. They can in principle differ between two records from the same station, so
they belong to the observation, not to the equipment.

**`ClassBDisplay`, `ClassBDsc`, `ClassBBand`, `ClassBMsg22`** — these are the only
members with *no* semantic role, and the schema calls them capability flags. The
natural reading, which I mark as an inference rather than a stated fact, is that
they are attributes of the transponder and therefore constant per station. The
combination rule that follows is firm regardless: **de-duplicate to one row per
`UserID` before computing any capability statistic.** Counting these per record
measures how often equipment transmits, not how common that equipment is, and
will bias the census towards whatever hardware happens to report most frequently.
The same warning applies to any vessel-count or traffic-share statistic.

**Cross-record joins on motion.** The five observation values in a record are
co-observed under one phenomenon time. Do not assemble a synthetic record by
taking position from one report and speed from another.

**Sentinels, generally.** `Latitude` 91, `Longitude` 181, `Sog` 102.3,
`TrueHeading` 511, `Cog` 360 (the schema describes the encoded 3600 as meaning
360°), and `Timestamp` 60–63 are all in-band "not available" markers occupying
the same numeric field as real data. Every one of them must be excluded before
any sum, mean, min, max or difference. Note that `Latitude`, `Longitude` and
`Timestamp` are *required*, so a report with no usable position still occupies a
row — presence checks alone will not filter it.

**Absence versus sentinel.** `Sog`, `Cog`, `TrueHeading` and all the flags except
`Valid` are optional. A missing member and a sentinel value are different
conditions and the files give no reason to think they mean the same thing. Handle
both.

## 4. Time

The time axis of the *thing described* is established by `Timestamp`, which the
schema explicitly marks `phenomenonTime`. `TimeReceived` is marked
`ingestionTime` and belongs to the pipeline, not to the vessel.

The difficulty is that `Timestamp` carries only the second of the minute. It is
not a position on any axis by itself. The enclosing minute must be recovered from
`TimeReceived` — the schema says as much, and says that receipt follows the fix by
the network's delay. The reconstruction that follows from those two statements
is: take the candidate instants having second-of-minute equal to `Timestamp`, and
select the latest one at or before `TimeReceived`. Equivalently, the fix lies in
the 60-second window ending at `TimeReceived`. In the example record, receipt at
11:42:09Z with `Timestamp` 7 places the fix at 11:42:07Z, a two-second latency.

Do **not** compute latency as `TimeReceived`'s second minus `Timestamp` — that
goes negative across a minute boundary, and a receipt at 11:43:02Z with
`Timestamp` 57 means a fix at 11:42:57Z in the *previous* minute.

This reconstruction is only correct while the true latency is under 60 seconds,
and **the files do not bound the latency**. If a message is delayed by more than a
minute, the procedure yields a fix exactly one or more whole minutes late and
there is nothing in the record that reveals the error. The only defence available
from within the data is distributional: a healthy feed should show latency
concentrated near zero, and a latency distribution that looks flat or bimodal
across [0, 60) is evidence that the assumption is breaking.

When `Timestamp` is 60–63 there is no phenomenon time at all. `TimeReceived` is
then the only time available and functions purely as an upper bound on when the
fix occurred.

Relation to civil time: both members are UTC — `TimeReceived` per its description
and the trailing `Z` in the example, `Timestamp` because it is defined as the UTC
second of the minute. There is no local-time offset anywhere in the files and no
statement about leap seconds. Any conversion to local civil time requires a
timezone the files do not supply.

Finally, the cadence is declared irregular. Do not assume a fixed reporting
interval, and do not apply any method that presumes evenly spaced samples without
resampling first. A gap in a station's reports does not mean the vessel stopped
or left — it may equally mean it passed out of range of the shore receivers, and
the feed carries no receiver identity or signal-strength member that would let
you tell the two apart.

## 5. Ambiguities

**Ingest latency bound.** Not determined by the files, and it is the single
assumption the entire time reconstruction rests on. I am declining to fix a value
and recommend the distributional check above instead.

**Duplicate reception.** Whether one transmission heard by several receivers
appears once or several times is not determined. This matters directly for
density and rate statistics. Declining.

**Stream ordering.** Nothing states that records arrive ordered by `TimeReceived`.
Declining; sort defensively.

**What `Valid: false` invalidates.** The description says such a message "could
not be fully decoded", which implies partial validity, but does not say which
members survive. Declining to guess a field-level rule. My assumption for
practical use, marked as an assumption: exclude those records entirely from
positional analysis and retain them only for decode-failure rate.

**Whether sentinels reach the consumer.** The schema documents them and describes
the aggregator as reporting "the decoded value", so they presumably do. Whether
the aggregator ever pre-filters them instead is not stated. Guard for both. I
also note a genuine ambiguity in `Cog`: the text names 3600 as the *encoded*
not-available value corresponding to 360°. My reading — a guess — is that the
decoded field carries 360.0, but I would defensively exclude both 360 and 3600.

**Identity stability.** The files call `UserID` "the identity of the vessel or
station" but establish nothing about whether an identity is unique to one
physical vessel, or stable over time. I am therefore declining to warrant track
continuity across long gaps or across re-appearances; treat a large jump in
position with a small elapsed time as an identity problem, not a fast ship.

**Whether capability flags are constant.** As noted, they lack a semantic role and
are described as equipment capabilities. Constancy is my inference, not a stated
fact. If you rely on it, verify it empirically per `UserID`.

**Course at rest.** Whether `Cog` is meaningful when speed over ground is near
zero is not addressed in the files. I have a strong prior that it degenerates,
but that prior comes from outside these two documents, so I flag it as a **guess**
and would validate it against the data before filtering on it.

**Operating state and reporting rate.** `ClassBUnit` distinguishes carrier-sense
from self-organising units and the schema says the unit type "governs the
transmission schedule". It does not say what those schedules are. So you know
that reporting rate varies systematically with `ClassBUnit`, but not by how much —
which is enough to know that record-count-based statistics are biased, and not
enough to correct the bias from these files alone.

**Position reference point.** Nothing states where on the vessel the reported
position is measured, and no vessel dimensions are present. For anything
requiring metre-level interpretation this is undetermined.

**Semantic references.** The `$id` and the object-level `observedProperty` point at
`example.invalid` and `catalog.example.org`; the RDF, Dublin Core and QUDT
references are not dereferenceable here. All semantics in this answer therefore
rest on the prose descriptions, not on any resolved vocabulary.

**The single example proves nothing about typicality.** The one record supplied has
every optional member present and every capability flag true. That is one draw. It
establishes that such records are possible, not that they are common, and no
distributional claim should be built on it.
