# 1. What this feed is

Each record is **one reception event**: a single receiver, named by `receiver_id`, decoded a single message from a single transmitting entity identified by a six-hex-digit code, and reported what it got out of it. The record carries a per-reception signal quantity and a per-reception timestamp alongside the decoded content, which is what makes it a reception record rather than an aircraft-state record. The optional members — position, altitude, speed, angle, vertical rate, callsign, squawk — are what the decoder happened to recover from that one message; only the identity of the transmitter, the identity of the receiver, the message class, and the timestamp are guaranteed present.

The consequence that governs everything downstream: **this is a sensor-network observation feed, not a track feed.** One transmission heard by three receivers produces three records. One aircraft transmitting frequently produces many more records than one transmitting rarely. An aircraft nobody heard produces none. Nothing in the two files declares uniqueness, ordering, deduplication, or completeness.

A second, subtler point. The vocabulary here — the ICAO-style 24-bit identifier, the downlink-format numbering, the ADS-B and Comm-B labels — will be familiar to many readers, and that familiarity is the main hazard. The files supply those *words*; they do not supply their *definitions*, and in particular they do not supply a single unit, datum, epoch, reference direction, or sign convention. Everything below distinguishes what the files guarantee from what a reader may be tempted to supply from memory.

# 2. Analytics worth running

**Field-presence profiling, first, before anything else.** Only five members are required; ten are optional. Cross-tabulate the presence rate of each optional member against `msg_type` and against `receiver_id`. Every later aggregate is silently conditioned on availability, and availability is almost certainly not uniform across message classes or receivers. This is supported because message class and receiver are always present, so presence is always attributable. Skipping this step is the most common way these aggregates go wrong.

**Receiver coverage and network characterisation.** This is the strongest analysis the feed supports, because a record *is* a reception, so the data are a direct sample of the thing being measured. For each receiver, map the volume of positions from which it successfully received, the reception rate as a function of range and altitude, and the directional distribution of successful receptions. Diagnose apparent coverage gaps and asymmetries. You may report the geometry of what was heard; attributing a gap to a physical cause (terrain, antenna pattern, interference) is not supported by these files and would be speculation.

**Multi-receiver overlap and redundancy.** For each transmitter in each time window, count distinct receiving stations. Supported because both keys are on every record. Directly useful for siting decisions and for knowing how badly a naive record count over-counts.

**Per-aircraft trajectory reconstruction.** Group on `icao24`, order by `ts` within a single `receiver_id`, and plot the position and altitude members. Supported because an entity key, a time-bearing member, and position members all exist. Caveats that matter: sampling is event-driven and irregular, only the subset of records carrying position participates, and interpolation between fixes assumes motion the data does not warrant.

**Empirical recovery of unit ratios.** The files name no units, but the data can supply the conversion factors. Regress the position displacement per unit `ts` against `spd`, and the altitude change per unit `ts` against `vr`. If a stable slope emerges, that slope *is* the unit relationship, measured rather than assumed, and its stability is itself evidence that the members mean what their names suggest. If no stable slope emerges, that is a finding: the members are not the consistent pair they appear to be. This is a genuinely productive analysis precisely because the schema is unannotated.

**Internal-consistency auditing.** Two members redundantly encode message class, and nothing constrains them to agree; disagreement rate per receiver is a decoder-health metric. Related: the message-class enumeration admits six labels while the numeric class member admits twenty-five values, and the label is required on every record. Records whose numeric class falls outside the six labelled values must therefore carry a label that cannot be correct. Measure how often that happens. Also measure which optional members empirically co-occur with which message class, and treat rare combinations as suspect — but treat them as *empirically* rare, since the files never say which classes are supposed to carry what.

**Receiver clock behaviour.** Per receiver, check `ts` monotonicity, gap distribution, and backward jumps. Nothing asserts a steered or monotonic clock. Do this before any time-series work, not after.

**Identity and label churn.** Track whether a given transmitter identifier presents more than one callsign or squawk within a session, and how often. Both members are per-record, so the analysis is supported. What churn *means* is not determined by the files.

**Analyses the feed does not support without outside input:** any count of aircraft events rather than receptions, absent a deduplication rule the schema does not provide; any statement in named physical units; any absolute civil-time statement; any claim that absence of records implies absence of aircraft.

# 3. Combination rules

**`ts`.** Differences within a single `receiver_id` are meaningful as elapsed intervals *in the unit `ts` uses*, provided that receiver's clock is monotonic and unstepped — which is not asserted anywhere and must be verified. Differences **across** different `receiver_id` values are unsafe: two receivers' clocks may carry an arbitrary relative offset, and nothing declares them synchronised. Any analysis whose conclusion depends on sub-interval timing between stations is invalid until that offset is measured or bounded. Never sum. Averaging is meaningful only as a window midpoint, never as a "typical time." Note also that the declared 64-bit width exceeds exact double-precision integer range; the string encoding in the sample preserves the value, but code that routes this member through a floating-point number is not safe in general even though this particular value survives it.

**`alt`.** Comparable and differenceable only among records sharing a common unit *and* a common vertical reference. The files establish neither, and do not forbid a mixture, so cross-record differencing carries an unverified assumption. Within one transmitter, successive differences are meaningful as change in whatever the member measures. Averaging across different transmitters is a population description, not a physical quantity, and is corrupted outright if the reference varies. Never sum. One more trap: the member is integer-typed, so it is quantised at source at an unstated granularity; the round sample value is weakly consistent with coarse quantisation. Differences taken over short intervals will be dominated by that quantum, so derived vertical rates from short baselines are noise.

**`lat` / `lon`.** The declared bounds make degrees the only sensible reading, but no geodetic datum is stated, so any join to an external geospatial source rests on an assumed datum. Comparison and differencing are valid for displacement of a single transmitter. **Never sum.** Averaging longitude arithmetically is wrong: ±180 are both admissible and denote the same meridian, so a naive mean across that wrap produces a point on the opposite side of the world. Use a circular or unit-vector mean, or none. Separately, degrees are not linear in ground distance and the scale differs between the two members everywhere except the equator, so Euclidean distance computed in degrees is wrong.

**`ang`.** This is a circular quantity — the declared range is inclusive at both ends, so 0 and 360 are two encodings of one direction. Therefore: arithmetic averaging is invalid, naive differencing is invalid (359 and 1 differ by 2, not 358), summing is meaningless, and equality comparison or histogram binning will split the two encodings of the same direction unless you normalise first. Use circular statistics. Further, the files do not state what the angle is the direction *of*, nor its reference direction; values from producers using different reference directions are not combinable, and the resulting bias would vary with place and time rather than being a constant you could subtract out.

**`spd`.** No unit and no reference frame are stated. Comparison and differencing require both to be common across the records being combined, which is not guaranteed. Never sum. Averaging is permitted arithmetically but is usually the wrong statistic: records arrive on message events, not on a clock, so a mean over records is weighted by reception rate and receiver coverage rather than by time. Aggregate to one value per transmitter per time bucket first, then average across transmitters. **Do not combine this member with `ang` into a velocity vector** — they sit adjacent and look like a polar pair, but nothing in the files binds the angle to the direction of this speed.

**`vr`.** Same unit and event-weighting cautions as speed. Differences within one transmitter are meaningful as change of rate. Never sum raw values across records; a time-integral weighted by the intervals is a different and legitimate operation. Comparing this member against the time-derivative of `alt` is a useful consistency check only if the two share a unit relationship and a vertical reference, which is not established — a systematic disagreement between them is therefore a finding to investigate, not automatically an error.

**`rssi`.** This is a property of the reception, not of the transmitter, so any per-aircraft aggregate of it is really measuring the receiver and the geometry. **Not comparable across `receiver_id` values** unless the stations are identically calibrated, which is nowhere asserted; treat cross-receiver comparison, differencing, and pooled averaging as invalid by default. Within a single receiver, relative comparison and ranking are defensible. Never sum. Arithmetic averaging is unsafe under the assumption — which the name and the negative sample value suggest but the files do not state — that this is a logarithmic quantity; the mean of log-domain values is not the log of the mean of the underlying quantity. Convert to linear, average, convert back, or report medians.

**`df`, `tc`, `sq`.** These are codes, not magnitudes. Compare for equality, group by them, count them. **Never difference, sum, or average them.** The declared numeric types and ranges on the first two actively invite a mean that would be meaningless. The squawk member additionally has a small code space and is not unique across transmitters, so it must never be used as a join key.

**`msg_type`, `receiver_id`, `icao24`, `cs`, `bcode`.** Grouping and equality only. Use `icao24` as the entity key; the files do not establish that it is stable per physical transmitter over time, but it is the only member with a declared identifying form. Do **not** join on `cs` — it is unconstrained, optional, and may change within a session.

**Record counts.** `count(*)` counts receptions. It over-counts transmissions in proportion to how many stations heard each one, and that factor varies by place, altitude, and time. Deduplicating back to transmissions is not reliably possible here: there is no message identity or sequence member, and the timestamp is per-receiver. Any rate, density, or "how much traffic" figure must state whether it means receptions or transmissions, and only the former is directly measurable.

**Selection bias, applying to every aggregate above.** Records exist only where a receiver heard something. A spatial density map is a map of coverage multiplied by activity, not a map of activity. Absence of records is not evidence of absence.

# 4. Time

`ts` is the only time-bearing member, so it is the axis by default — but the axis it establishes is the axis of the **reception**, not of the aircraft state. The record is receiver-scoped: it names the receiving station and carries a per-reception signal quantity. Nothing in the files provides a separate validity time for the position, altitude, or motion members. If the timestamp marks reception, then those state members carry an unknown and possibly variable latency relative to it, and that latency is not recoverable from these files. This matters most for the derived-versus-reported consistency checks described above, and for any attempt to align this feed against another time series.

That the timestamp marks reception rather than emission is a **guess**, though a well-founded one: it is the reading consistent with a record that is scoped to a receiver and carries a reception-quality quantity. The files do not say.

There is not one time axis but one **per `receiver_id`**, until relative clock offsets are shown to be negligible. Treat multi-receiver time comparison as invalid by default.

**The relation to civil time is not determined by the files.** Placing a value on a civil calendar requires three things none of which is stated: the unit of the count, the epoch it counts from, and the timescale (in particular, whether it is a UTC-referenced clock, in which case differences spanning a leap second are not true elapsed intervals, or a free-running station clock, in which case they drift). The member is an unlabelled integer.

As a marked **guess**: the magnitude of the sample value is consistent with a count of milliseconds since the 1970 Unix epoch, which would place that record in 2026. I offer this only as the hypothesis to test against an authoritative out-of-band statement; I am not treating it as established, and nothing in the two files supports it. A useful cross-check available from the data itself: if this reading is right, the spacing between consecutive receptions from a single active transmitter should land in a plausible sub-second-to-seconds range, and the empirically recovered unit ratios described in section 2 should come out at recognisable magnitudes.

# 5. Ambiguities

**Declining to decide** — the files do not determine these, and I will not supply an answer:

- The unit of altitude, speed, vertical rate, signal strength, and time. Five separate undetermined units.
- The vertical reference of the altitude member. Barometric and geometric references differ, and the files neither fix one nor forbid a mixture within the feed.
- The epoch and timescale of the timestamp.
- The reference direction of the angle member, and what the angle is the direction of.
- The geodetic datum of the coordinates.
- Whether the two overlapping encodings of message class are required to agree, and which is authoritative when they do not.
- Whether the type-code member applies to all message classes or only some. Its optionality is consistent with the latter but does not establish it.
- The meaning of `bcode` entirely. It is an unconstrained string with no pattern, enumeration, or description. I cannot say anything about it.
- Whether the same reception may appear more than once, and whether records arrive in timestamp order. Neither is declared, so both must be assumed possible.
- Whether the transmitter identifier is stable to one physical unit over time.
- Whether the position, altitude, and motion members within one record are mutually simultaneous, or decoded from different messages, or interpolated.
- **Whether a missing optional member means "not applicable to this message class" or "present but not decoded."** This is the most consequential undetermined item after units, because it decides whether missingness is informative and whether imputation is ever legitimate. I decline to decide it; measure it empirically per message class and per receiver instead.
- The quantisation granularity of the integer-typed members.
- Whether the signal-strength values from different stations are calibrated to a common scale.

**Guesses, marked as such:**

- **Guess:** the timestamp is milliseconds since the 1970 epoch, placing the sample in 2026. Basis: magnitude only.
- **Guess:** the timestamp marks reception rather than emission. Basis: the record is receiver-scoped and carries a reception-quality quantity.
- **Guess:** a negative vertical rate means decreasing altitude. The sign convention is not stated anywhere; only the sample value hints at it, and a hint from one record is not a convention.
- **Guess:** the angle values 0 and 360 denote the same direction. Basis: an inclusive-at-both-ends range over a full turn. If they are instead distinct sentinel values, the circular treatment recommended above would be wrong.
- **Guess:** the coordinate members are in degrees. Basis: the declared bounds. Strong, but still inferred rather than stated.
- **Guess:** the speed and angle members describe the same motion vector. I have recommended against relying on this; test it empirically before using it.
- **Guess:** the signal-strength member is a logarithmic quantity. Basis: its name and the negative sample value. The averaging warning in section 3 depends on this guess; if it is linear, arithmetic averaging is fine.

**Two structural notes an analyst needs.** First, the schema's numeric bounds are narrower than one might assume: speed, vertical rate, altitude, and signal strength carry no bounds at all, so schema-valid records may contain negative altitudes or negative speeds. Range validation belongs in the pipeline and cannot be inherited from the schema. Second, the schema's identifier resolves to a reserved non-routable name, so there is no external document to fetch that would resolve any of the above. The missing semantics have to come from the feed's operator or be estimated from the data; they cannot be looked up.
