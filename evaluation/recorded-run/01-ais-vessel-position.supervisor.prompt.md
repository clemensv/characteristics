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

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order Latitude, Longitude. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. `TimeReceived` is an operational instant (`ingestionTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `TimeReceived` as the event time of the observation.

3. `Timestamp` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `Timestamp` as the time the record was produced, received, or published, or using a different member for event time.

4. Successive `Timestamp` values are expected at cadence `irregular`. A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

5. `Valid` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `Valid` as an observed quantity.

6. `Latitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `Latitude`.

7. `Longitude` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `Longitude`.

8. `PositionAccuracy` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `PositionAccuracy` as an observed quantity.

9. `Raim` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `Raim` as an observed quantity.

10. `Sog` is expressed in `[kn_i]`.
   wrong reading: Assuming a different or conventional unit for `Sog`.

11. `Cog` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `Cog`.

12. `TrueHeading` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `TrueHeading`.


TRANSCRIPT A

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


TRANSCRIPT B

# Reading the feed

## 1. What this feed is

Each record is a **point-in-time report of where one identified mobile unit was and how it was moving**, as received by whatever collected the feed. A record binds an integer identity to a coordinate pair, a reception instant, a small set of quality/validity flags, and — when present — a speed, a course, and a heading. A further group of booleans describes the *reporting device and its operating mode* rather than anything about the world.

The stream is therefore a **sequence of independent samples, not a continuous track**. Nothing in the material says a record's state holds until the next record, and nothing states a reporting cadence. A track is something you reconstruct by grouping on the identity and ordering on the reception instant; it is not something the feed gives you.

Only six things are guaranteed to be present: the identity, the reception instant, the undocumented integer `Timestamp`, the `Valid` flag, and the two coordinates. **Everything about motion — speed, course, heading — is optional and may simply be absent.** Any pipeline that assumes motion data is present will silently drop or mis-handle records.

The schema's name and the abbreviations used are strongly suggestive of maritime AIS Class B position reporting. *That is a guess from naming alone.* The files establish no domain, no vessel, no sensor, no platform type, and no issuing authority. I use no domain knowledge below; everything in sections 2–4 stands on the two files.

## 2. Analytics worth running, and why the data supports them

**Track reconstruction per unit.** The identity, a typed instant, and a coordinate pair are all *required*, so every record can be placed on a per-unit timeline without loss. This is the only analysis fully supported by the required members alone. It rests on one unverified assumption: that the identity is stable and unique per physical unit (see §5).

**Spatial occupancy, density, and dwell.** Coordinates are required and never missing, so heat maps, cell counts, and "how many distinct units entered region R" are computable over the whole stream with no coverage bias from optional fields. Note that *density is report-weighted, not unit-weighted*: a unit reporting ten times as often contributes ten times the mass. Deduplicate to distinct identities per cell if you want an occupancy measure rather than a chattiness measure.

**Presence, gaps, and reporting behaviour.** Grouping by identity and differencing consecutive reception instants gives inter-report intervals. This supports gap detection, session/voyage segmentation by silence threshold, and per-unit reporting-rate profiles. It is well supported because both inputs are required. What it does *not* support is calling a gap a real outage: the files do not establish whether this stream is complete or a sample, so a gap may be a collection artefact.

**Data-quality profiling.** The proportion of records with each boolean set, cross-tabulated by unit and by time, is fully supported. The single instance shows `Valid` true while `PositionAccuracy` is false, which demonstrates these are not the same flag and must be profiled separately. This is worth running *first*, because the polarity of these flags is undetermined (§5) and their empirical joint distribution is the only evidence available for interpreting them.

**Presence/absence analysis of the optional members.** Because absence is permitted and `additionalProperties` is closed, the pattern of which optional members appear is itself a signal — it may distinguish device classes, firmware, or upstream decoders. This is supported and cheap. It is also a prerequisite for every motion analysis, since missingness is likely to be non-random.

**Speed distributions and motion-regime segmentation** (stopped / slow / underway), *within this feed only*. Supported for relative comparison and for clustering, because all records in one feed plausibly share one unit of measure. Not supported for any statement in physical units, and not supported for comparison against any external speed source — the unit is not established anywhere.

**Course and heading behaviour**: turn detection, course-change rate, steadiness. Supported provided you treat these as circular quantities (§3). Circular variance of course over a window is a good, well-founded manoeuvre detector here.

**Heading-versus-course divergence** is the analysis analysts most want and the one this material least supports. It requires that the two angles share a reference direction and rotational sense. Only one of them is named "True"; the other's reference is unstated. The single instance has them 2.3 apart, which is consistent with a shared reference but a single record cannot establish it. Treat any drift/set computation as an assumption, and validate it against the population before using it.

**Not supported by these files:** anything about what the units *are* (no type, size, class, name, or voyage data); any latency or end-to-end delay measurement (requires knowing what `Timestamp` is and whose clock `TimeReceived` uses — neither is established); any absolute-speed or absolute-distance claim in named physical units; any fusion with an external positional dataset without first resolving the coordinate reference.

## 3. Combination rules, quantity by quantity

**Identity (`UserID`).** Equality and grouping only. It is a label that happens to be stored as an integer. **Never sum, average, difference, or order it**, and never treat numeric adjacency as relatedness — no numbering scheme is established. Its use as a grouping key assumes uniqueness and temporal stability, neither of which the files state.

**Reception instant (`TimeReceived`).** Compare and order freely. **Difference two of them** to get an elapsed duration — this is the one arithmetic operation on time that is sound here. **Never sum instants.** Averaging is meaningful only as a midpoint, not as a quantity. Differences are trustworthy as *reception* spacing; treating them as the spacing of the underlying events assumes constant delay, which is not established. If more than one receiver contributes to the stream, differences across records from different receivers may not reflect real event spacing at all.

**`Timestamp`.** **Do not combine it with anything.** No unit, no epoch, no origin, no range, no monotonicity, and no wrap behaviour is established. It must not be differenced against `TimeReceived`, summed, or averaged; it must not be used to order records. The instance actively rules out the obvious reading: as seconds since the Unix epoch, the value 7 would place the record in 1970, irreconcilable with the accompanying instant. So the epoch interpretation is *excluded by the material itself*. Equality comparison is the only defensible operation, and even that has no established meaning.

**Coordinates (`Latitude`, `Longitude`).** These are **two components of one quantity and must always travel as a pair**; never combine the latitude of one record with the longitude of another. Within one reference system they may be compared and differenced — but a difference in degrees **is not a distance**. Euclidean distance on raw degrees is wrong everywhere except trivially near the equator, because a degree of longitude shrinks with latitude. Use a geodesic or a projection.

**Do not take a component-wise arithmetic mean to get a "mean position."** Longitude is cyclic and wraps; an arithmetic mean is catastrophically wrong across the wrap and distorted elsewhere. Use a unit-vector (Cartesian) mean, or work in a projected system.

Summing coordinates is meaningless. Comparing or differencing coordinates against *any other data source* requires that both use the same geodetic reference — the files establish none, so cross-source fusion carries an unquantified datum offset. The `double` type also permits far more precision than the source plausibly carries; do not read trailing digits as resolution.

**`Sog` (speed).** Within a single feed it may be compared, differenced, and averaged — **on the assumption that all records share one unit**, which the files do not state but which is the natural reading of a single feed under one schema. It may **not** be combined with speed from any external source without reconciling units; the plausible candidates differ by factors of roughly 1.9 to 3.6, so the error is large and silent.

Two further traps. First, **a plain mean of `Sog` across records is not mean speed over time** unless reports are equally spaced — and spacing is not established. Weight by the interval to the next report if you want a time-average. Second, no "unavailable" sentinel value is documented; if the encoding uses one, it will be an ordinary-looking number that poisons every mean and maximum. Profile the distribution before aggregating.

**`Cog` (course) and `TrueHeading`.** Both are **circular quantities and must not be treated as ordinary numbers.** Specifically:

- **Never take an arithmetic mean.** 350 and 10 average to 180 — the exact opposite of the correct answer. Use the vector mean of unit vectors, or circular statistics.
- **Never sum them.**
- **Difference only modulo the circle**, wrapping to the shortest signed arc in (−180, 180]. A raw subtraction produces spurious 350-unit jumps at every wrap.
- **Ordering comparisons ("greater than") are not meaningful** on a circle. "Within an arc of X" is meaningful; "above 300" is not, unless you mean it as an arc.
- Standard deviation, min, max, median, and linear interpolation are all invalid without circular treatment.

Additionally these two must not be differenced against each other unless you accept the unverified assumption that they share a reference direction and rotational sense. They also differ in stored precision — one integral, one fractional — so their difference inherits the coarser resolution. And the integral one admits values outside a compass range with no documented sentinel; screen for out-of-range values before any circular aggregation, because a single sentinel will drag a vector mean anywhere.

**The boolean flags — `Valid`, `PositionAccuracy`, `Raim`.** These are predicates about a record, not measurements. Use them to filter, and aggregate them only as *proportions over a stated denominator*. Never sum them together — they are not commensurable with one another. Their polarity is not established (§5), so a filter written in the wrong direction will silently keep exactly the records you meant to drop. The single instance shows `Valid` and `PositionAccuracy` disagreeing, so they must never be conflated or used interchangeably.

**The device/mode flags (`AssignedMode` and the `ClassB*` group).** These describe the reporting equipment, not the world. If they are constant per unit — which is plausible but **not established** — then averaging them across *records* produces a report-weighted statistic that says more about which units are chatty than about the population. **Deduplicate to one row per identity before computing any fleet-level proportion over these.** Comparing them record-to-record is fine; summing or averaging over raw records is a trap. As a group they are also not commensurable with each other and must not be summed into a score.

**Absence, across all optional members.** **Do not impute a missing boolean as `false`, and do not impute a missing number as zero.** The schema permits absence and states nothing about its meaning; a missing speed is not a speed of zero, and a missing flag is not a cleared flag. Missing and false must remain distinguishable through the whole pipeline, and every proportion must state whether its denominator is all records or only records where the member was present.

## 4. Time

**`TimeReceived` is the only member that establishes a time axis.** It is the sole member with a temporal type, and the instance carries a UTC designator, so its values are absolute instants — orderable, differenceable into elapsed durations, and convertible to civil time in any zone given that zone's rules.

The critical point, and the thing an analyst will get wrong: **this axis is a reception axis, not an observation axis.** The member's own name places it at the point of receipt. The files nowhere state the delay between the described state holding and the record being received, nor whether that delay is constant, nor whose clock stamped it. Consequences that follow directly:

- Ordering records by this member is ordering by *arrival*. If delays vary — different receivers, different paths, buffering, replay — arrival order need not match the order in which the states actually occurred.
- Interpolating a position between two consecutive instants assumes constant delay across that interval. That assumption is unstated and unverified.
- Cross-unit synchrony ("these two were close at the same moment") is only as good as the assumption that both records suffered the same delay.

**`Timestamp` does not establish a time axis** and must not be used as one. It carries no epoch, unit, origin, or range, and as noted the instance excludes the epoch-seconds reading outright.

On the relation to civil time: with a UTC anchor, each instant maps unambiguously to civil time in any zone. Durations obtained by differencing are **elapsed UTC durations, not wall-clock differences** — across a daylight-saving transition the two disagree by an hour, so bucketing by local hour-of-day requires an explicit zone conversion and must not be done by string slicing. The schema guarantees only that values are instants; it does not guarantee that every record carries the same offset designator as this one, so normalise to UTC on ingest rather than assuming.

Finally, **a record marks an instant, not an interval.** No validity duration or "state held until" is expressed. Any resampling, gap-filling, forward-fill, or "last known position" logic is an interpretation layered on top of the data, and the choice of hold-time is yours, not the feed's.

## 5. Ambiguities

**Declining to decide** — the files do not settle these, and I will not manufacture an answer:

- **The domain.** Nothing states what is being tracked, on what medium, by whom, or under what standard. *Guess, marked as such:* the schema name and the abbreviations suggest maritime AIS Class B position reporting. Nothing in the two files establishes this and I have not used it anywhere above.
- **The unit of `Sog`.** Undetermined. *Guess: knots.* Do not act on that guess; the plausible alternatives differ by nearly a factor of four.
- **The angular unit and reference of `Cog` and `TrueHeading`.** *Guess: degrees,* on the weak evidence that both instance values fall below 360. The reference direction of `Cog` and the rotational sense of both are undetermined; only one member's name asserts a reference at all. Whether the two share a reference — the precondition for any divergence computation — is undetermined.
- **The geodetic reference and unit of the coordinates.** *Guess: decimal degrees.* The datum is entirely undetermined, which is the blocker for fusing this feed with any other spatial dataset. Sign conventions (north-positive, east-positive) are likewise unstated; I assume the conventional ones and flag that as an assumption.
- **The meaning of `Timestamp`.** Undetermined, and I decline to use it. *Guess, marked and not relied upon:* a coarse sub-minute field, given the small value and the presence of a full instant alongside it. That guess is not sufficient to justify any arithmetic.
- **The polarity and referent of every boolean.** Does `PositionAccuracy` true mean *high* accuracy or *low*? Does `Valid` qualify the position, the whole record, or a decode step? What does each `ClassB*` flag assert? All undetermined. Written the wrong way round, these filters invert your dataset without erroring.
- **Identity uniqueness and stability.** Whether one identity maps to exactly one unit, whether it persists over time, and whether it can be reassigned or spoofed. Every per-unit analysis assumes all three. Also unstated: whether identity values can exceed the signed 32-bit range, and what happens if so.
- **The meaning of absence** for the optional members, and whether missingness is random or systematic.
- **Sentinel / "unavailable" encodings** in the numeric members. This is the highest-risk unknown here, because a sentinel is indistinguishable from a real value and will corrupt means, extremes, and circular aggregates without any error surfacing.
- **Reporting cadence, and whether the stream is complete.** Undetermined. Every time-weighted statistic and every gap-based inference depends on it.
- **Whether `TimeReceived` is stamped by a receiver or by the unit, and the delay distribution.** Undetermined; see §4.
- **Deduplication.** Whether one underlying report can appear more than once — for instance via multiple receivers. Undetermined. Undetected duplicates inflate density maps and bias every unweighted aggregate toward whatever is best-covered.
- **Effective coordinate resolution.** The storage type permits far more precision than the source plausibly carries. *Guess:* true resolution is coarser than the stored digits. Do not report positions to full stored precision.
- **Ordering guarantees.** Whether records arrive in reception order, and whether late arrivals occur. Undetermined; sort explicitly rather than trusting arrival order.

**What I would need to resolve these:** a units declaration for the speed and the two angles, a geodetic reference for the coordinates, a definition of `Timestamp`, the polarity and referent of each flag, and a statement of which clock stamps `TimeReceived`. None of it is inferable from one schema and one record, and inferring it would be guessing dressed as analysis.


TRANSCRIPT C

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


TRANSCRIPT D

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
