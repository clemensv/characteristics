# Class B position reports — analyst's briefing

## 1. What this feed is

Each record is one **observation of one moving object at one instant**: a nine-digit
station identity, a geographic position, a speed and direction of travel over the
ground, the direction the hull is pointing, and a set of flags describing the state
and the capabilities of the transmitting equipment.

Three things about its nature matter more than its contents.

It is an **event stream, not a state table**. Records arrive because a station
transmitted and because a receiver in a terrestrial network happened to hear it.
Nothing in the record is a query result or a periodic sample under your control. The
population of records is shaped by the transmitters' schedules and by radio reception,
both of which are outside the data.

It is **relayed, not first-hand**. The record was decoded by an intermediary and
carries that intermediary's own reception time alongside the originator's own notion
of when the fix was taken. Those are two different clocks measuring two different
events, and the record keeps them separate on purpose.

It is a **restricted slice**. This record type describes only Class B shipborne
equipment. It is not a census of vessel traffic; it is a census of one class of
transmitter that a particular receiver network could hear. The schema also states
plainly that this message carries no navigational status, so operational state
("under way", "at anchor", "restricted in ability to manoeuvre") is simply not
present and cannot be read out of these records — only inferred, at your own risk.

---

## 2. Analytics worth running

**Per-station trajectory reconstruction.** Stable subject identity plus position plus
a recoverable phenomenon time is exactly the minimum needed to order observations of
one object into a track. This is the foundation for everything else. The limit: the
sampling interval is set by the transmitter and by reception, so tracks are irregular
and gappy, and gaps are indistinguishable from silence, loss of reception, and the
station having left the covered area.

**Kinematic consistency checking and gap classification.** Position and velocity are
given *for the same instant*. That means each record independently predicts where the
next one should be. Dead-reckon forward from record *n* and compare to record *n+1*:
consistent → normal gap; grossly inconsistent → decode error, identity collision,
duplicate delivery, or a track that is not what it claims to be. This is the highest-
value quality check available and it needs no external data.

**Course-versus-heading divergence.** Direction of motion over the ground and hull
orientation are two different physical quantities, expressed here on the same datum
(degrees true) at the same instant. Their circular difference is the crab angle — the
signature of current, wind, or a vessel not going where it is pointing. In the example
record, motion is 2.3° to the right of the hull. This quantity is only available
because both members are present in the same record, and analysts routinely destroy it
by treating course and heading as interchangeable.

**Stop and dwell detection.** Speed over ground near zero, sustained across
consecutive reports for one identity, identifies stationary periods. Note the
inference boundary: the data supports "not moving over the ground". It does not
support "anchored", "moored", or "drifting" — those distinctions are not in this
record type.

**Spatial distribution of reception-weighted activity.** Positions aggregate into
density surfaces. But the honest name for the product is a map of *where this network
heard Class B transmitters*, not a map of where vessels are. Empty areas are
ambiguous between no traffic and no coverage, and the data cannot separate the two.

**Fix-quality stratification.** Two independent per-fix quality signals are carried:
a stated accuracy class and an integrity-monitoring flag. Any analysis whose result
depends on displacements comparable to the fix error — close-quarters proximity,
short-baseline speed derivation, precise berth assignment — must be stratified or
weighted by these, or it is measuring receiver error and reporting it as motion.

**Equipment population census.** Unit type and the capability flags describe the
hardware, not the moment. Counted correctly (see §3), they characterise the installed
base of transmitters in the covered area.

**Ingest latency measurement.** The difference between the originator's fix second and
the second-of-minute of the relay's receipt time gives the pipeline delay — modulo one
minute. This is a genuine, self-contained observability signal about the feed itself,
and it also bounds how much you can trust the receipt time as a proxy for event time.

**Base-station control detection.** The assigned/autonomous mode flag is a per-report
operating state. Clustering of assigned mode in space or time indicates shore-side
management of reporting behaviour — an operational signal about the *environment*,
distinct from anything about the vessel.

---

## 3. Combination rules

The controlling principle: **all kinematic combination is valid only within a single
station identity.** Position, speed, course and heading describe one object's motion.
Differencing two of them across two identities does not yield motion; it yields the
separation of two different objects observed at two different, unsynchronised
instants.

### Identity

The station identity is an integer only in its storage. It is nominal. **Equality and
grouping only.** Never difference, sum, average, rank, or bin it. Arithmetic on it is
always a bug, and no numeric structure in it may be assumed.

Whether one identity corresponds to one physical vessel, stably, across the whole
observation window is **not established by these files**. Longitudinal analysis rests
on that assumption; state it.

### Geographic coordinates

Continuous and comparable — **after** excluding the not-available sentinels, which are
carried *in band as ordinary numbers* outside the declared coordinate ranges. A mean
latitude computed over raw values that include the sentinel is silently wrong and will
pass every structural validation the schema performs, because the declared numeric
type is far wider than the valid domain. Filter on range before any arithmetic.

Differences are **angular, not metric**. A longitude difference is not a distance and
does not correspond to a fixed ground distance at different latitudes. Convert on the
stated ellipsoidal datum before differencing for distance.

Longitude is **cyclic** at ±180. Linear averaging or linear differencing across that
discontinuity is wrong.

Averaging positions over records yields a **report-weighted centroid, not a
time-weighted mean position**, because the reporting interval is not specified and is
not uniform. If you want a time average, weight by the interval between recovered
phenomenon times.

Averaging positions across identities describes the report population, never a vessel.

### Speed over ground

Comparable, differenceable and averageable **within one identity**, after excluding
its not-available sentinel. Two limits:

- The underlying quantisation is coarse (0.1 kn per the schema). Differences at or
  below that granularity are not measurements.
- The mean of speed values is **not** the average speed over the interval, and is
  **not** track distance divided by elapsed time. It is a mean over reports.

Across identities, a mean is a statistic about the reporting population. It is biased
toward stations that transmit more often and that sit in better reception, and the
files give you no way to correct that bias.

### Directions (course over ground, heading)

**These are angles on a circle. Ordinary arithmetic is invalid on them.**

- **Never sum.** The sum of two bearings is meaningless.
- **Never take an arithmetic mean.** The linear mean of 350° and 10° is 180° — the
  exact reverse of the correct answer. Use unit-vector (circular) averaging.
- **Difference only modulo 360, normalised to (−180, 180].**
- **Do not order or threshold** them as if they were magnitudes.
- Exclude each member's own not-available sentinel before any of this.

Course and heading share a datum, so **their circular difference is meaningful** and is
the one legitimate cross-member angular combination here. Beyond that they are
distinct quantities: never average them together, never substitute one for the other,
and never fill a missing course from heading or vice versa.

One consequence, not a domain claim: course over ground is the direction of a velocity
vector. As speed approaches zero the direction is undefined and whatever value is
reported is noise. Exclude course from analysis at low speed rather than treating it
as a heading substitute.

### Second-of-minute fix marker

This is the member most likely to be misused, because it looks like a count and is
neither a count nor a duration.

- It is a **position on a 60-second cycle**, not elapsed time. **Never sum. Never
  average.**
- Differencing two values gives elapsed seconds **only modulo 60**, and only if you
  already know the two reports are less than a minute apart. Otherwise you are
  aliasing.
- Four in-band codes above the valid range are **not times at all** — they encode
  equipment state: time unavailable, manual position entry, dead reckoning, and
  positioning system inoperative. They must be excluded from every numeric use, and
  they carry information you should act on: under dead reckoning or manual entry the
  reported position is not a measured fix. Kinematic analysis that silently includes
  those records is treating computed positions as observations.

### Relay receipt instants

These are true civil instants. Differences between them are genuine elapsed durations
and may be compared, differenced and averaged.

But the receipt instant is **not** when the reported thing happened. The schema states
it lags the fix by propagation and queueing delay. Therefore:

- Do **not** use receipt-time differences as the denominator of any rate. Variable
  latency propagates directly into every derived speed, acceleration or turn rate.
- Do **not** assume receipt order reproduces fix order, particularly across different
  stations or receivers. The files do not guarantee it.

### Per-fix flags versus per-equipment flags

Both are categorical: **countable, never differenced, never averaged as numbers**. You
may compute proportions. The distinction that matters:

- **Accuracy, integrity monitoring, decode validity and assigned/autonomous mode are
  per-record.** They may legitimately change from one report to the next for the same
  station. Do not collapse them to one value per identity.
- **Unit type and the four capability flags describe the equipment.** Counting them
  per record answers "what fraction of *transmissions*", which is dominated by whoever
  transmits most. To characterise the fleet, **reduce to one value per distinct
  identity first**. Report-weighted capability statistics are the single most common
  aggregation error available in this data.

The decode-validity flag is a **gate, not a covariate**. When it is false the schema
says the message was not fully decoded — which means every other member in that
record is suspect, including ones that look entirely plausible. Filter on it before
anything else.

### Two distinct kinds of missing

Only identity, receipt time, fix second, validity and the two coordinates are
guaranteed present. Everything else can be **absent**, *and* several members can be
**present carrying a not-available sentinel**. These are different states and the files
do not say they mean the same thing. A pipeline that maps both to null discards a
real distinction; a pipeline that handles only one of them corrupts its arithmetic.

### Permitted operations

| Quantity class | Compare | Difference | Sum | Average |
|---|---|---|---|---|
| Station identity | equality only | no | no | no |
| Latitude / longitude | yes, sentinel-filtered | yes, as angles; convert for distance; longitude wraps | no | report-weighted centroid only |
| Speed over ground | yes | yes, above 0.1 kn granularity | no | over reports, not over time |
| Course / heading | not by magnitude | modulo 360 only | no | circular mean only |
| Fix second-of-minute | cyclic position only | mod 60, and only under 60 s | no | no |
| Receipt instant | yes | yes, true durations | no | epoch centroid only |
| Per-fix flags | yes | no | count only | proportion only |
| Equipment flags | yes | no | count per identity | proportion per identity |

Structural validation against this schema proves nothing about semantic validity: the
declared numeric types are far wider than the valid domains, so every sentinel and
every out-of-domain value passes. Range checking is your job, not the schema's.

---

## 4. Time

**The time axis of the described thing is set by the originator's fix second, not by
the relay's receipt time.** Position, speed, course and heading all refer to the
instant the originating station's position-fixing system produced the fix. The receipt
time is when an intermediary got the message; it is metadata about the pipeline.

That fix marker is, however, **not a point on the civil axis**. It carries a second of
the minute and nothing else — no minute, hour or date. The enclosing minute must be
recovered from the receipt time, and the schema says so explicitly.

**The recovery rule the files support:** take the latest instant whose second equals
the fix marker and which is not later than the receipt time. In the example, a receipt
at 11:42:09 UTC with fix second 7 resolves to 11:42:07 UTC — two seconds of latency.
The alternative candidate, 11:41:07, would imply 62 seconds of latency.

**Where this breaks, and it is not a corner case:** the rule is correct only while
latency stays under one minute, and *the files place no bound on latency*. Whenever
delay crosses a minute boundary, the recovered instant is wrong by exactly a whole
number of minutes while looking perfectly well-formed. Under-60-second latency is an
assumption you are making, not a fact you have.

**Resolution.** The recovered phenomenon time is good to one second and no better.
Rates computed over short baselines are therefore poorly determined, and the error is
in the denominator where it does the most damage.

**When there is no phenomenon time at all.** If the fix marker carries one of the
state codes rather than a second, no civil instant for the fix is recoverable. Those
records have only a receipt time, which is the time of ingest and not of the event.
Substituting one for the other silently converts an unobserved event into an observed
one.

**Datum.** The example is explicitly UTC-offset-zero and the schema names a UTC source,
so the axis is UTC. Nothing in either file maps positions on that axis to any local
civil time, time zone, or daylight-saving regime. Any local-time analysis needs an
external mapping these files do not provide.

---

## 5. Ambiguities

Each item states whether I am declining to decide, or guessing.

**Reporting cadence.** How often a station transmits, and whether that rate depends on
its behaviour, is not established. **Declining.** Consequence: no per-record average
is a time average, and no gap can be interpreted as anomalous without an expected
interval.

**Receiver coverage.** The network is described as terrestrial; its geographic extent,
gaps and duty cycle are not established. **Declining.** Consequence: absence of records
is uninterpretable, and any density product is confounded with reception.

**Whether the stream carries other record types.** One schema was provided. Whether
other message types, or other equipment classes, arrive alongside is not established.
**Declining.** Do not label outputs from this alone as vessel traffic.

**Identity stability and uniqueness.** Whether one identity maps to exactly one
physical station for the whole window is not established. **Declining.**

**Duplicate delivery.** Whether one transmission heard by multiple receivers produces
multiple records is not established. **Declining.** If you need to deduplicate, the
natural key — same identity, same fix second, same position, differing receipt times —
is a **guess** at the right key, not something the files support.

**Latency bound.** Not established. **Declining** to bound it. The minute-recovery rule
above is the reading the files most directly support; the sub-60-second premise it
rests on is an **assumption**.

**Clock provenance and synchronisation.** Whose clock stamps the receipt, and how well
it is disciplined, is not established. **Declining.**

**Meaning of absent optional members.** Whether absence means not transmitted, not
decoded, or dropped by the relay is not established, and whether it differs from the
in-band not-available sentinels is not established. **Declining.**

**Meaning of `false` on capability flags.** For two of the capability flags the schema
states only what `true` means. Whether `false` asserts absence of the capability or is
merely a decoder default is not established for those. **Declining.** Do not report
"fraction of units lacking X" from those two.

**One capability flag is described as operating state.** The unit-type flag is
characterised both as a hardware type and as part of reported operating state.
Whether it can legitimately change for one identity is not established. **Declining**;
until it is resolved, treat disagreement across records for one identity as
unexplained rather than as a change.

**Course not-available encoding.** The schema's wording refers to the sentinel both as
an encoded value of 3600 and as 360 degrees. Which literal actually arrives in the
delivered record is **ambiguous in the source text**. **Declining** to pick one; guard
against both, since either passes type validation.

**Speed grid.** The schema notes 0.1 kn native resolution but says the relay reports
"the decoded value". That values arrive on the 0.1 kn grid, unrescaled and unsmoothed,
is a **guess** — consistent with the single example, but one example proves nothing.

**Content of records flagged as not fully decoded.** Which members remain trustworthy
when validity is false, and whether such records are emitted at all, is not
established. **Declining.** Excluding them entirely is my **recommendation**, not a
fact from the files.

**Coordinate sentinel co-occurrence.** Whether one coordinate may carry its sentinel
while the other is valid is not established. **Declining**; test both independently.

**Heading reference offset.** Whether the reported heading is the hull's or is subject
to an installation offset is not established. **Declining.**

**Geographic scope.** One example record is one point. I **decline** to infer the
feed's region, jurisdiction or operating area from it; naming a place would be an
inference from outside these files.

---

**One thing that is determined and is easy to overlook:** these records bind a
persistent, specific station identity to a position and a time. In aggregate that is a
movement history of individually identifiable assets. Whatever handling, retention and
disclosure rules apply to that in your setting, they apply here — the files establish
the identifiability, and they say nothing about the rules.
