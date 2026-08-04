# Reading the feed

## 1. What this feed is

Each record is one relayed radio report from a single shipborne mobile station,
carrying where that station said it was, how fast and in what direction it was
moving, how good its own position-fixing device believed the fix to be, and what
class of equipment it is. The station is the subject: everything else in the
record is a statement about that one station at one moment. Records are
independent of one another; the feed gives you no vessel record, no voyage, no
destination, no identity beyond a nine-digit number, and no notion of a track —
a track is something you build by grouping on that number, and the feed neither
supplies one nor guarantees that the reports you have for a station are all of
them, or in order.

Two distinct times are present and they are not the same time. One is when the
originating equipment fixed its position; the other is when the relay service
received and decoded the transmission. The first is the time the data is *about*
and it is only partially encoded. The second is the time the data *arrived* and
it is fully encoded. Confusing them is the most expensive mistake available here,
and section 4 covers it.

The other thing to understand up front is that this is a decoded radio protocol,
not a sensor stream. Several quantities encode "no data" as an in-range-looking
number rather than as an absent member, and the record separately carries a flag
saying whether the transmission decoded at all. A consumer that treats the
numbers as numbers will silently ingest positions off the coast of nowhere and
speeds of a hundred knots.

## 2. Analytics worth running, and why the data supports them

**Per-station track reconstruction.** The station identifier is declared as the
feature of interest, so it — and only it — is the legitimate grouping key for
"the same thing over time". Position is bound to a named coordinate reference
system, so successive positions for one identifier are in a common frame and can
be strung together. This is the base analysis everything else sits on, and its
weak point is the time axis, not the geometry.

**Kinematic self-consistency checking.** The record carries a position *and* the
station's own speed and course at one shared phenomenon time. That redundancy is
the useful thing: the displacement implied by two consecutive positions can be
checked against the reported speed and course, and disagreement flags a bad fix,
a spoofed transmission, a mis-decoded sentence, or a dropped record. The data
supports this because position and motion are declared as results sharing one
feature, one phenomenon time, and one procedure — the temporal role of a record
is shared by every result in it. It requires a geodetic distance and bearing
computation that neither file supplies; the coordinate reference system is
identified, not implemented, and no conversion or coordinate operation is
defined here.

**Course-versus-heading difference.** Both are carried, both are stated to be
referred to true, and they are genuinely different quantities: one is the
direction the station is travelling over the ground, the other the direction it
is pointing. Their difference is the classic indicator of set, drift, or leeway.
The data supports it in the sense that both are present with a stated common
reference; the arithmetic is circular and the two must not be pooled (section 3).

**Spatial occupancy and traffic density.** Position plus identifier plus a
declared coordinate reference system supports gridded density and region
crossing counts. The trap is that the reporting cadence is declared *irregular*,
so a count of records in a cell is a count of *transmissions*, not of vessels and
not of vessel-time. Any density product that does not re-weight by identifier or
by dwell time is measuring how talkative the equipment in that cell is.

**Equipment population and quality statistics.** The unit type, band capability,
display, DSC and channel-management flags describe the transmitting equipment,
and the accuracy and integrity-monitoring flags describe its position-fixing
device. Proportions across the fleet — how much of the traffic is DGNSS-quality,
how much runs integrity monitoring, how the carrier-sense and self-organising
populations divide — are directly supported. They must be computed per
*identifier*, not per record, or the answer is weighted by transmission rate.

**Decode reliability.** The decoder flag is required on every record, so the
share of transmissions that failed to decode is measurable, and can be broken
down by region, by hour of receipt, or by equipment class.

**Base-station control incidence.** The assigned-mode flag says whether a
station's reporting behaviour is being controlled by a base station, so the
prevalence and geography of assigned mode is measurable as reported.

**What the feed does not support.** Anything requiring vessel identity, type,
dimensions, draught, cargo, destination, or navigational status — none is
present, and the schema forbids additional members. Anything requiring
completeness: neither file asserts that every transmission is relayed or that
every relayed transmission is retained. Anything requiring receiver-network
latency measurement — see section 4, where that turns out to be circular. And
any accumulation, such as distance travelled or time underway, without external
machinery: no member is declared as an accumulation or an interval quantity, and
nothing in the record authorises summation over time.

## 3. Combination rules, quantity by quantity

A precondition applies to all of them. Two values may be combined at all only if
they concern the same feature, which here means the same station identifier.
Feature identity may not be inferred from proximity, from similar positions, or
from anything other than that declared identifier. And no record whose decode
flag is false should enter any computation: that flag states the fields are not
reliable, which is a statement about the record's contents, not about its
transport.

**Station identifier.** Comparable for equality and groupable. Never
differenced, summed, or averaged — it is declared an identifier and a feature
key, not a quantity. One caution follows from the declared type rather than from
the domain: it is carried as a signed 32-bit integer while its description calls
it nine digits. Any identifier whose decimal form begins with a zero cannot round-trip
through an integer without losing that digit, and comparing such a value against
a string-typed identifier from another system will fail. Whether such
identifiers occur is not established by these files.

**Latitude and longitude.** Bound together as one coordinate in a named system
whose axis order is latitude first, longitude second — which is exactly what the
specification's own list of reference URIs states for that identifier, so the
schema's assertion checks out. They are comparable and differenceable *only*
against coordinates in the same system. Two consequences bite immediately.
First, joining this feed to anything using the longitude-first form of WGS 84 —
which is the same datum in the opposite axis order — requires swapping the pair,
and nothing in the data will tell you that you failed to: both are plausible
numbers in the same unit. Second, differencing degrees does not give a distance.
The difference of two latitudes and two longitudes is a difference of angular
coordinates; converting it to metres is a geodetic operation that these
annotations explicitly do not supply and that a processor is forbidden to
perform without an authoritative definition.

Averaging them across records is defensible only as a crude centroid of a small
cluster, and is wrong outright near the longitude wrap: the stated range runs to
±180, so an arithmetic mean of two longitudes straddling that discontinuity
lands on the opposite side of the world. Summing coordinates is meaningless —
they are positions on axes with a datum origin, not magnitudes.

The out-of-range sentinels (91 for latitude, 181 for longitude) are not
positions. They are in-band "not available" codes documented in prose only:
no enumeration constrains them, no code-list binding resolves them, and the
declared type admits them. They must be excluded before any arithmetic. A single
un-filtered sentinel will drag a centroid, a bounding box, or a mean into
nonsense.

**Speed over ground.** A magnitude in knots. Comparable, differenceable, and
averageable across records of the same station, once the 102.3 "not available"
sentinel is excluded. Two qualifications. Because the cadence is declared
irregular, a plain mean over records is a mean over *samples*, not over time; if
the station transmits more often when manoeuvring, the mean is biased toward
manoeuvring speeds. A time-weighted mean is what most questions actually want,
and it requires the reconstructed fix times of section 4. Second, it must not be
summed: no member here is declared as an accumulation or as characterising an
interval, and nothing authorises treating a sequence of instantaneous speeds as
covering the gaps between them. Multiplying speed by an elapsed time to obtain
distance is a calculation you may choose to perform, but it is not licensed by
anything in these files and it inherits every weakness of the time axis.

**Course over ground and true heading.** Both circular. Neither may be
arithmetically averaged: the mean of 350 and 10 is 180, pointing the wrong way.
Circular statistics — vector mean of the unit directions — is the correct
treatment, and the discontinuity is established by the stated ranges (course to
359.9, heading to 359). Differences must be taken modulo 360 and reduced to the
±180 branch. Neither may be summed. Their sentinels (360 for course, 511 for
heading) are again in-band codes carried in prose and admitted by the declared
types, and must be filtered first — 511 in particular will destroy any circular
computation it enters.

**Course and heading must not be pooled with each other.** They are different
quantities: direction of travel over the ground versus direction the hull points.
This needs saying because the annotations actively invite the mistake: both
carry the *same* observed-property reference, a generic angle quantity kind. A
consumer joining on observed property will treat them as one series. The
specification is explicit that a quantity-kind classification is a compatibility
hint and does not establish that two things are the same observable property, so
the shared reference is not evidence of comparability — it is only evidence that
both are angles.

**Speed and course are not a velocity vector.** They look like one, and a
consumer will be tempted to decompose them into north and east components. No
reference frame is declared for them, and the specification forbids inferring
that members sharing a unit or an observed property are the components of one
vector quantity. You may compute components, but the result is a *calculated*
value in a frame you asserted, not a measured one the feed published, and it
carries no machine-checkable frame binding for anyone downstream. Related: the
"true" reference for course and heading appears only in prose descriptions. No
frame annotation binds it. If another feed supplies magnetic-referenced
directions, nothing in either schema will detect the mismatch.

**The second-of-minute stamp.** Not a quantity. It must never be summed,
averaged, differenced, or used as a sort key. Its values wrap every minute, so
the difference between 58 and 3 is not −55 seconds of anything; and its top four
values are not times at all but status codes (unavailable, manual input,
dead reckoning, inoperative) documented only in the description, with no
enumeration and no code-list binding to resolve them.

**Receipt time.** A full instant, comparable and differenceable as such. It is
declared as the time the ingest system accepted the record, and the
specification forbids reading such a value as the time the phenomenon occurred.
Differencing two receipt times for one station gives the spacing of *arrivals*,
which includes propagation and queueing delay and is not the spacing of the
fixes. Nothing asserts that records arrive in the order the fixes were taken —
the declared cadence carries no ordering guarantee — so receipt order is not fix
order.

**The quality and status flags.** Countable and groupable; a proportion over
records is a legitimate summary, and a proportion over distinct stations is
usually the one you want. None of them is a weight. The accuracy flag is a
two-state indicator with a stated 10 m threshold, not an uncertainty and not a
variance; there is no confidence model here and the specification defines none,
so it may be used to filter but not to weight a least-squares fit. Absence of a
flag does not mean the good value: three of these members are optional, and
omission is undeclared, never "acceptable".

One structural point that will catch a careful reader. The schema declares five
separate results in one record, and it attaches the quality flags as direct
members of the record. Under the specification, a quality qualifier attached at
record level qualifies *every* result in that record; narrowing one to a single
result would require nesting that result in its own object. So although the
accuracy flag is described as being about position, the schema as written does
not scope it to position, and there is no annotated way to say that the speed
and course in a low-accuracy record are fine. Treat the flag as qualifying the
whole record, which is the conservative reading and the one the structure
actually states.

**The equipment capability flags** carry no declared role at all. They describe
the transmitting unit, are stable per station rather than per moment, and should
be treated as station attributes to group by, not as observations to aggregate
over time.

## 4. Time

The time axis of the thing described — the position fix — is carried by the
second-of-minute member. That is the member declared as phenomenon time, and it
is the only one. The receipt time is declared as an ingestion time, which the
specification classifies as describing the handling of the record; it must not be
read as the time the fix applies, and no analysis that needs the fix time may
substitute it.

The problem is that the phenomenon-time member does not, on its own, place
anything on a civil time axis. It gives a second of the minute and nothing else.
The description states the reconstruction rule — recover the enclosing minute
from the receipt time — and that rule is prose, not annotation: the member is a
bare integer with no temporal reference system, no unit, no meta-type, and no
mapping onto a position. Under the specification an encoding like this is
indeterminate until a temporal reference system is declared, and a processor is
forbidden to infer the regime from the encoding. So nothing here establishes,
in a machine-checkable way, that this feed's fix times are UTC or that they can
be compared with anyone else's.

More seriously, the reconstruction rule is not well-defined at minute
boundaries, and the files do not say how to resolve it. In the example record
the fix is stamped at second 7 and the receipt at 11:42:09Z, so the fix falls two
seconds before receipt and the naive rule — take the minute from the receipt —
gives the right answer. Now suppose a fix stamped at second 58 arrives at
11:42:03Z. The naive rule yields 11:42:58Z, which is fifty-five seconds *after*
the record was received. The correct answer is plainly 11:41:58Z, one minute
earlier. There is no member that disambiguates this, and no stated bound on the
delay between fix and receipt, so the general case is not resolvable from the
data alone.

*This next part is my suggestion, not something the files establish:* choose,
among the candidate minutes, the one that puts the fix at or before the receipt
instant with the smallest non-negative lag. That is the only rule I can see that
is consistent with the stated fact that receipt follows the fix. It fails
whenever the true delay exceeds sixty seconds, and the files state no delay
bound, so it cannot be validated from what is here.

That heuristic has a consequence worth stating on its own, because it will
otherwise be discovered the hard way: **you cannot measure relay latency from
this feed.** Any latency you compute is the difference between the receipt time
and a fix time that was derived *from* the receipt time. The result is bounded
below sixty seconds by construction, and it is an artifact of the reconstruction,
not a measurement of the network.

Three further points about the time axis. Successive positions on it are
declared to recur irregularly, so gaps are not anomalies, absence of a record is
not evidence of anything, and no window may be assumed filled — a declared
cadence is an expectation about a producer, it constrains no instance, and it
never licenses supplying a value where none was recorded. Second, the four
sentinel stamps place the record nowhere on the axis at all; a record carrying
one has no reconstructable fix time, and two of those sentinels additionally say
the fix came from manual input or dead reckoning. Third, whether the originating
station's clock and the relay's clock agree is not stated, and cross-station
comparison of reconstructed fix times depends entirely on that.

That third sentinel point exposes a contradiction in the schema itself, and it
matters for analysis. Position is annotated as *measured* — produced directly by
an observation procedure. But a record whose stamp says the positioning system
was in dead-reckoning or manual-input mode did not measure that position; by the
specification's own test, something stood between the procedure and the value,
which would make it estimated rather than measured. The derivation annotation is
a statement about the type and cannot vary per record, so the schema asserts
"measured" over records that themselves say otherwise. Filter on the stamp before
trusting the derivation.

## 5. What the two files leave open

**What the record-level observed property actually is.** It points at a
fictitious catalogue — the specification names that catalogue kind as its
placeholder for exactly this — so the definition does not resolve. An unresolved
reference is indeterminate and may not be repaired from member names,
descriptions, or samples. **Declining to decide.** Treat the observable property
of the position as unestablished, and do not join this feed to another on the
strength of that identifier.

**Whether the motion values are instantaneous or averaged over some support.**
No relation to phenomenon time is declared and no support period is given.
Omission is explicitly not the same as "instant". **Declining to decide.** If you
need to know whether a reported speed is a snapshot or a short mean, the files
do not tell you, and the difference matters for any smoothing or gap-filling you
apply.

**How the fix time is recovered at a minute boundary.** Covered in section 4.
The rule I proposed is **a guess**, offered because the alternative is to have no
rule at all; it is not supported by anything in the files, and it silently fails
past a minute of delay.

**Whether the accuracy and integrity flags qualify position only or every result
in the record.** The descriptions say position; the structure says everything.
I have taken the structural reading, and I flag this as a genuine conflict rather
than a decision the files make. **Declining to decide** which was intended.

**What produced any of these values.** No observing procedure is identified.
Procedure identity is comparability-critical — different procedures give
different biases for the same property and feature — so comparing reported
speeds across stations is comparing across unknown and possibly different
equipment. The carrier-sense versus self-organising flag is described as
governing the *transmission schedule*, not the position fixing, so it is not a
procedure proxy and I decline to use it as one.

**Position resolution.** The speed's native resolution is stated. The position's
is not. Position is carried as a double with no stated quantisation, and the
number of decimal places in one sample establishes nothing. **Declining to
decide** — do not assume a resolution when deciding whether two positions differ.

**Coverage, ordering, and duplication.** Nothing states that every transmission
is relayed, that a station's reports are complete, that records are unique, or
that they arrive in fix order. The declared cadence asserts none of these; it is
not a completeness assertion or a service level. **Declining to decide** — verify
against your own delivery, not against the schema.

**Identifier stability.** Whether a station identifier is permanent, reused, or
reassigned is not addressed. **Declining to decide.** Long-horizon per-identifier
analysis rests on an assumption the files do not support.

**Whether records with a false decode flag are published with populated
members.** Not stated. **Declining to decide** — filter them out rather than
inspect them.

**The distinction between an absent member and a sentinel value.** Three of the
motion members are optional, so "no data" has two encodings, and no rule says
which a producer uses or whether it uses both. **Declining to decide;** handle
both paths.

Two defects worth reporting to whoever maintains the schema, since they affect
what a conforming tool will do with it. The two status flags are booleans, but a
status value is required to be drawn from a fixed set carried as a string or an
integer, constrained by an enumeration or bound to an external set — neither
holds here, so a strict processor will report those annotations invalid. And the
sentinel codes throughout — the unavailable positions, speeds, courses, headings,
and the four stamp states — exist only as prose. A code-list binding or an
enumeration would make them machine-visible; as written, every consumer has to
rediscover them by reading descriptions, and the ones that do not will produce
plausible, wrong numbers.
