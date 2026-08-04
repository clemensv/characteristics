# Reading the Mode-S / ADS-B feeder stream

## 1. What this feed is

Each record is one aircraft-state report produced by a **ground station**, not by an aircraft. An aircraft transponder radiated something; a named receiver heard it, decoded it, and emitted this record. The record therefore has two subjects at once: the airframe it is about (identified by its ICAO 24-bit address) and the station that produced it (identified by `receiver_id`, which the schema explicitly marks as the *observing procedure* — the thing responsible for every value in the record).

That double subject is the single most important fact about the feed. The same radio transmission heard by two stations produces **two records, not one**, and they will legitimately disagree: different signal levels, different reception timestamps, and sometimes different decoded positions, because the position is solved from a *pair* of encoded messages and two stations may have caught different pairs. There is no member that identifies the underlying transmission, so **the feed cannot be de-duplicated from its own contents**. Any count you compute is a count of receptions, not of transmissions and not of aircraft events.

The second important fact: with the sole exception of the signal level, **nothing in the record is a measurement**. Position, altitude, speed, angle and vertical rate all carry `derivation: calculated` — they are decoder outputs, reconstructed from a compressed and partly ambiguous bit encoding. The signal level is the only quantity that describes something the receiver directly observed, and it is classified as *result quality*, not as an observation of the aircraft. The squawk is a *status* code, not a measurement of anything physical.

The third: the message format determines which members exist. The schema states plainly that only the extended-squitter family carries position and velocity at all; the surveillance and Comm-B families carry an altitude or a squawk and little else, and the all-call reply carries nothing but the address. So the stream is **heterogeneous and sparse by construction**. Only five members are required. Absence is the normal case, not an error.

There is a serious inconsistency between the schema's account and the supplied example, discussed in §5.1, which changes what a "record" means. Read that before building anything.

## 2. Analytics this stream supports, and why

**Per-airframe track reconstruction.** The address is present in every record and is described as the airframe identity, so grouping by it is sound. Ordering within a group is sound because the time member declares a forward sort order. This gives you flight paths, level changes, and airport arrival/departure sequences. Constraint: build tracks **within a single `receiver_id` first**, because cross-station position disagreement is decode variance and will appear as spurious jitter or as phantom lateral excursions if you interleave stations naively.

**Receiver characterisation and coverage mapping.** This is the analysis the schema most directly supports, and it is usually the one people skip. Signal level is a per-station quality measure, and position and barometric altitude accompany it, so within one station you can map detection range against bearing and altitude, find terrain and structure shadowing, detect antenna degradation over time, and establish that station's practical noise floor. The stable station identifier makes this a longitudinal analysis rather than a snapshot.

**Decode-confidence filtering as a pre-step to everything else.** The schema states that low signal level marks messages decoded near the noise floor, and that this is where bit errors surviving the parity check originate. That makes signal level a usable *prior on correctness of the other members in the same record*. Establish a per-station low-level threshold from that station's own distribution and filter or flag before doing kinematics. Without this step, your position and altitude outlier population will be dominated by decode errors and you will misread them as aircraft behaviour.

**Cross-station agreement as a system diagnostic.** Where two stations report the same address at near-identical times, the spread in their decoded positions quantifies the decode path's variance. This is a genuine and valuable analysis — but it measures the *receiver network*, not the aircraft. Do not report it as position accuracy of the aircraft.

**Message-mix analysis, which reveals two different things.** The format families split cleanly by cause: the extended squitter is broadcast by the aircraft unprompted, whereas the surveillance and Comm-B families are described as *replies to a ground interrogation*. So the proportion of extended squitters in an airframe's records is evidence about that airframe's equipage (does it broadcast ADS-B at all, or is it Mode-S only?), while the volume of reply-type records is evidence about **interrogation activity in the area** — that is, about ground radar, not about the aircraft. Conflating those two is an easy and consequential mistake.

**Special-condition monitoring.** Three squawk values are stated to carry a meaning that overrides the assigned code. Exact-string matching on those three is a well-founded alert. Treat it as a report that the transponder was set that way, not as confirmation that the condition obtains; the code can be stale or mis-decoded, and the files establish no corroborating flag.

**Flight-identity association over time.** The callsign is the flight leg, the address is the airframe. Accumulating the association between them yields an airframe-utilisation view and a leg-segmentation signal. The schema warns the callsign is crew-entered, frequently wrong, and frequently blank, so this analysis needs corroboration and should never be used as a primary key.

**Pressure-surface occupancy statistics.** Because every altitude value shares one declared pressure reference, cross-aircraft altitude comparison is exact and cheap. Cruise-level occupancy, level-change detection, and vertical-separation checking between aircraft are all well founded — as statements about pressure surfaces (see §3).

**Feed liveness and latency monitoring.** The time member is reception time, so comparing it against your own ingestion clock measures the pipeline, per station. This is a legitimate use and is arguably the member's most defensible use.

**What this stream does not support.** Multilateration is out of reach: the time member is a millisecond-resolution *decode* time, not a sub-microsecond time of arrival, and no raw timing member exists. Any true-airspeed, wind, or geometric-climb analysis is out of reach for the reasons in §3. Aircraft counts and traffic-density estimates are out of reach without an external de-duplication scheme, because receptions are not transmissions.

## 3. Combination rules

### Identifiers and codes

**Aircraft address** — equality only. It is a valid join and grouping key across records and across stations, since it is stated to be the only identifier present in every format. No arithmetic, no ordering with meaning. Whether an address is stable over an airframe's whole life, or ever reused, is not determined by these files; do not assume either way for long-horizon studies.

**Receiver identifier** — equality only, and it must be **carried as a grouping dimension into every aggregate you compute**. Dropping it silently mixes provenances. This is the rule most often broken.

**Downlink format, type code, format-family literal, Comm-B register code** — these are categorical, and two of them are numerically typed, which is a trap. Count them; never sum, difference or average them. A mean downlink format has no meaning. Type code ranges are ordered only in the sense that the ordering carries a lookup table, not a magnitude.

**Squawk** — a four-character octal *string*, and it must stay a string. Do not parse it as a decimal integer: "0021" is not twenty-one, "3421" is not three thousand four hundred and twenty-one, and codes with leading zeros will be destroyed by numeric coercion. Equality comparison only; no sum, no average, no numeric sort. The three reserved codes are detected by exact match.

**Callsign** — equality after normalising the padding described in the schema. It groups a flight leg, not an airframe, so it changes between legs for the same aircraft. Because it is stated to be frequently wrong or blank, it must not be used as a join key on its own, and any count of distinct callsigns is a count of *broadcast strings*, not of flights.

### Time

**Reception timestamp** — differences are valid **within one station** and yield elapsed milliseconds on the POSIX scale. Across stations, differencing is only as good as the stations' clock agreement, and these files declare a shared time *scale* while declaring nothing about a shared *clock*; see §4. Differences spanning an inserted leap second under-report elapsed physical time. Summing timestamps is meaningless. Averaging is defensible only as a midpoint, and only within one clock regime.

### Altitude

**Barometric altitude** — the schema is unusually explicit here and the consequences are not obvious.

- *Comparison and differencing between aircraft is valid and is the intended use.* Every value is referenced to the same standard pressure setting, so the difference between two aircraft's values is their separation **on the pressure scale** — which is exactly the quantity vertical separation is defined against. This works even though neither value is a height.
- *Differencing one aircraft's values over time* gives change in pressure altitude. It is **not** a geometric climb, and converting it to one requires the atmospheric offset, which the schema states is not transmitted.
- *Averaging across aircraft* yields a mean pressure surface. Report it as such or not at all.
- **Never** difference an altitude against a terrain elevation, a runway elevation, an ellipsoidal height, or any geometric quantity from another source. Two aircraft with equal values are on the same pressure surface and are at *different geometric heights*; the offset varies with the state of the atmosphere and is absent from the data. This is the mistake that produces confident, wrong terrain-clearance and ground-proximity analyses.
- Summing altitudes is never meaningful.

### Horizontal position

**Latitude and longitude** — one geodetic reference frame is declared for the whole feed, with the axis order pinned explicitly, so all records are mutually comparable in space and no axis-order guessing is required.

- *Within one station and one airframe*, ordering by reception time and differencing successive positions gives displacement. But the time axis is reception time, not the instant the position was true (§4), so any speed derived this way carries the reception jitter as error. Treat derived speeds as indicative, not as measurements.
- *Across stations*, do **not** difference positions and call the result displacement. The schema states the decoded position depends on which message pair the station happened to receive; a cross-station difference is decode variance and may be pure artefact.
- *Averaging* positions is not a neutral operation. Arithmetic means of degrees are only approximately a centroid, they are distorted by meridian convergence away from the equator, and they break across the antimeridian, which the declared bounds permit records to sit on from either side. Averaging across stations additionally averages a good solution with a possibly bad one rather than detecting the disagreement.
- Summing coordinates is never meaningful.
- **Critically: the declared reference frame covers the two horizontal coordinates only.** The altitude is on a pressure datum, not a geodetic one. You therefore **do not have a three-dimensional geodetic position** in this record, and assembling the three numbers into a 3D point in that frame — a `POINTZ`, a globe-viewer entity, a 3D distance calculation — silently mixes two incompatible vertical references. Any 3D geometry built this way is wrong.

### Velocity quantities

**Speed** — the schema states the subtype bit that would say whether this is ground speed or airspeed has been discarded by the feeder. Consequently the values are **not a single quantity**, and across records you may not difference, sum or average them, because you would be combining two physically different measures whose difference is the wind. Within one record it is a magnitude in the declared unit and nothing more. Comparing it against a speed you derived from successive positions is valid *only under the assumption that it is ground speed* — and that assumption cannot be checked from this record. Mark it as an assumption wherever you make it.

**Angle** — two independent problems, and both bite.

1. *Referent.* The schema states this is track over the ground when the message carried ground speed and magnetic heading when it carried airspeed, and that the deciding bit was discarded. Those are different angular quantities with different origins, differing by drift angle and by magnetic variation, and the variation is not transmitted. So cross-record differencing and averaging mixes two data and is not permitted without an external determination of the subtype.
2. *Circularity.* Even where the referent is known, this is a circular quantity. The arithmetic mean is invalid — the mean of 350 and 10 is not 180. Use a vector (unit-circle) mean. Differences must be reduced modulo a full turn into a half-open half-turn range. The declared bounds admit both endpoints of the circle, so the same direction has two representations and binning code must fold them together.

Comparing the angle to a bearing computed from successive positions additionally requires the ground-track subtype *and* a true-north referent. Both are assumptions.

**Vertical rate** — sign convention is fixed (positive upward), so signs may be compared. The source (barometric or geometric) is stated to be undeclared in the forwarded record, so averaging across records is valid only if the source is constant, which is undetermined. Two specific operations are unsound and both are commonly attempted:

- *Integrating the vertical rate over time to predict or check altitude.* This fails twice: the rate may not be on the same vertical reference as the altitude, and the time axis is not the sampling axis.
- *Reconciling a reported rate against a rate computed by differencing altitudes.* Same two failures. A mismatch does not evidence a data error.

### Signal quality

**Signal level** — the schema is categorical: the scale is receiver-specific and two stations' values are **not comparable**. That forbids cross-station comparison, cross-station averaging, and — most importantly — using it as a **weight** when fusing multi-station reports, which is the natural thing to reach for and is invalid here. Within one station, it is meaningfully ordered, and a low value flags a marginal decode.

It is expressed in decibels, i.e. on a logarithmic scale, so within one station a *difference* of two values is a **ratio**, not a linear difference in signal, and an arithmetic mean of the values is not the mean signal. Converting back to a linear scale would require knowing whether the decibel figure is referenced to power or to amplitude, which these files do not state — so do not convert.

### Record counts

Counting records is not counting aircraft events. Counts are confounded by station coverage, by receiver sensitivity, by the interrogation environment (for the reply formats), and by duplicate reception across stations that cannot be de-duplicated from the record contents. Any rate you compute is a **reception rate at a station**, and it must be reported that way.

## 4. Time

**Which member is the time axis, and of what.** The reception timestamp carries the *result time* role: it is the instant the ground station decoded the transmission. The schema then states the thing analysts most need to hear — Mode-S transmissions carry no timestamp, so **the instant at which the reported state was actually true aboard the aircraft is not available in this feed at all**, and can only be bounded by the transmission interval of the format concerned, which is itself not given in these files.

So the answer has two parts. The time axis *of the record* is the reception timestamp, and it is well-defined. The time axis *of the thing described* — the aircraft state — is **not established by these files**. The value members declare that each refers to an instant rather than an interval, but the identity of that instant is not transmitted. The practical rule: you may order and window records by reception time, but every derived quantity that divides by a time interval (speed from positions, climb rate from altitudes, acceleration) inherits reception-side latency and jitter as error of unbounded and unstated magnitude.

**How positions on the axis relate to civil time.** The axis is a count of milliseconds since the 1970 epoch that **ignores leap seconds**. The schema is explicit that this makes it a scaled POSIX time and *not* a UTC instant. Three consequences that matter:

- The mapping to civil time is **not injective**. During an inserted leap second the count repeats the preceding second, so one value can denote two distinct civil instants. Sub-second reasoning across such an insertion is unsound.
- **Elapsed-time differences under-report** physical elapsed time by one second for each insertion the interval spans.
- The **ordering is declared forward**: a larger value is later. Within one clock, ordering is therefore safe outside the leap-second case.

**The scale trap.** The schema calls this out deliberately: the value is a bare integer in milliseconds, and it differs by three orders of magnitude from the second-count that most feeds transmit, with nothing in the payload to distinguish the two. A consumer that assumes seconds will silently place every record tens of thousands of years in the future. The example value read as milliseconds falls in 2026; read as seconds it is nonsense. That contrast is the cheapest available sanity check and should be an ingestion assertion.

**Encoding.** The example transmits this integer as a **quoted JSON string** while transmitting the other numeric members bare. Parsers that expect a JSON number here will fail or, worse, coerce. *(Guess: the quoting exists because 64-bit integers are not safely representable in the JSON number type as many parsers implement it. The files do not say this, and they also do not say whether the quoted form is required or merely permitted — so accept both on input.)*

**Cross-station time.** The schema describes the underlying regime as the reception clock of the receiver *network*, which establishes that all stations report on the same **scale**. It does not establish that they are on the same **clock**: no member reports a clock offset, a synchronisation source, or a synchronisation quality. Cross-station ordering at sub-second resolution is therefore not warranted by these files, and neither is any technique that depends on relative arrival times between stations.

## 5. Ambiguities

### 5.1 Is a record one message, or an accumulated state? — **Declining to decide. This blocks correct interpretation and must be resolved with the producer.**

The schema says a record is one decoded downlink message, and that the format family determines which members are populated. It further states that only the extended squitter carries position and velocity, that identification content sits in one type-code range, airborne position in another, and velocity in a third, and that the squawk belongs to the identity-reply formats.

The supplied example declares an extended squitter with a type code in the **airborne-position** range, and then carries a callsign, a squawk, a speed, an angle and a vertical rate — content that, on the schema's own account, belongs to three *other* messages. A single transmission of the declared kind cannot contain all of that.

Two readings are available and the files do not choose between them:

- **(a)** Records really are per-message and sparse, and the example is an illustrative composite rather than a realistic record. Then most records carry two or three optional members and you must join across records to assemble state.
- **(b)** The feed actually emits a rolled-up per-aircraft state, in which the format members describe only the *triggering* message and the other members are values carried forward from earlier receptions. Then each member has its own, older and unrecorded, phenomenon time; the reception timestamp is **not** the result time of most members; and the record's declared result-time semantics are wrong.

The difference is not cosmetic. Under (b), attaching the reception timestamp to a carried-forward member overstates its freshness by an unknown amount, and every time-series built from this feed inherits that error. Until it is resolved: do not attach the timestamp to any member that the record's own declared format cannot carry, and treat the freshness of such members as unknown.

### 5.2 Which vertical reference the altitude uses in the geometric-position formats — **Declining to decide.**

The altitude member is described unconditionally as barometric. But the type-code description states that one range of type codes carries airborne position referenced against a *geometric* altitude. The files do not say what the altitude member contains for those records — the barometric value from elsewhere, the geometric value, or nothing. Records in that type-code range should be excluded from pressure-surface analyses until this is settled, since including them risks mixing two vertical references inside one column.

### 5.3 The discarded subtype and source bits — **Declining to decide; not recoverable.**

Whether the speed is ground speed or airspeed, whether the angle is ground track or magnetic heading, and whether the vertical rate is barometric or geometric are each stated to be undetermined because the deciding bits were not forwarded, and the record type forbids extra members, so they cannot be reintroduced at this layer. There is no inference available from the record itself. Any analysis that needs them must either obtain them from the producer or state its assumption explicitly and propagate the resulting uncertainty.

### 5.4 Station clock synchronisation — **Declining to decide.** Discussed in §4. Shared scale is established; shared clock is not.

### 5.5 What absence of a member means — **Declining to decide.**

Only five members are required. When an optional member is absent, the files do not distinguish "the format does not carry this", "the format carries it but the decode failed", and "the value was carried but suppressed". These have different implications for missing-data handling: the first is structural and should not be imputed at all, the second is a quality signal and belongs in your decode-failure statistics.

### 5.6 The Comm-B payload is absent — **Determined, and worth stating.**

The record can name the register a Comm-B reply used, and the schema warns that this register number is *inferred* rather than transmitted and may be inferred wrongly. But the record has no member carrying the register's contents, and extra members are forbidden. So for these formats the record tells you what kind of information arrived and not what it said. The register code is provenance without content; it is useful for message-mix analysis and for nothing else.

### 5.7 Formats outside the declared family list — **Inference, marked as such.**

The format-family literal is required and constrained to six values, while the numeric format member's permitted range is much wider. *Inference:* the feed is therefore filtered to those six families and other formats are dropped upstream rather than passed through unlabelled. The files do not say this outright, so if your coverage analysis depends on the completeness of the message population, verify it.

### 5.8 An internal inconsistency in the format member's bounds — **Flagging, not resolving.**

The numeric format member is described as a five-bit field, which implies an upper bound of thirty-one, while its declared maximum is twenty-four. Whether the feeder rejects higher values, clamps them, or the bound is simply an error is not determined. Validate rather than assume.

### 5.9 Callsign padding — **Flagging.**

The schema states the callsign is padded to eight characters; the example carries six with no padding. Either the feeder trims, or padding is inconsistent. Normalise on ingest and do not rely on fixed width.

### 5.10 Receiver position is absent — **Determined.**

The schema notes that position decoding may be resolved against a known receiver position, but no member carries that position and extra members are forbidden. Decoded positions are therefore **not auditable from the feed**: you cannot reproduce the decode, and you cannot bound the error a wrong assumed station position would introduce. If you need coverage geometry, the station coordinates must come from an external register keyed by the station identifier.

### 5.11 Ground versus airborne state — **Not determined.**

Nothing in the two files indicates whether the feed includes surface-movement reports or how they would be distinguished, and the type-code ranges the schema enumerates do not cover the full permitted range. Do not assume all records are airborne.

### 5.12 Emergency-code semantics — **Guess, marked as a guess.**

The schema says the three reserved squawks carry a meaning that overrides the assignment. *Guess:* they should be treated as latching alerts requiring human review rather than as instantaneous conditions, since a transponder retains a code between messages and a single mis-decode in either direction is plausible given the stated bit-error mechanism. The files do not establish any dwell, confirmation, or clearing rule, so this is my judgement and not theirs.
