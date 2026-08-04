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

1. Coordinates at `#` are expressed in `http://www.opengis.net/def/crs/EPSG/0/4326`, with axes bound in the order lat, lon. Axis order follows that binding and must not be assumed.
   wrong reading: Assuming latitude/longitude order, or assuming WGS 84, without reading the binding.

2. `ts` is an operational instant (`resultTime`), not the time the observed phenomenon occurred, and must not be used as the time axis of the phenomenon.
   wrong reading: Using `ts` as the event time of the observation.

3. Positions in `ts` are expressed in the temporal reference system `#/definitions/PosixMillisecondEpoch` (kind `type`), not in an unqualified civil clock.
   wrong reading: Reading `ts` as ordinary UTC.

4. `ts` is on a clock of its own. Converting it to civil time requires a synchronisation relation that the schema does not supply, so a correct reader declines the conversion or states the external input it would need.
   wrong reading: Converting `ts` to UTC as though the mapping were given.

5. `ts` is expressed in `ms`.
   wrong reading: Assuming a different or conventional unit for `ts`.

6. `alt` is calculated rather than measured directly.
   wrong reading: Treating `alt` as a direct measurement.

7. `alt` is expressed in `[ft_i]`.
   wrong reading: Assuming a different or conventional unit for `alt`.

8. `lat` is calculated rather than measured directly.
   wrong reading: Treating `lat` as a direct measurement.

9. `lat` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `lat`.

10. `lon` is calculated rather than measured directly.
   wrong reading: Treating `lon` as a direct measurement.

11. `lon` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `lon`.

12. `spd` is calculated rather than measured directly.
   wrong reading: Treating `spd` as a direct measurement.

13. `spd` is expressed in `[kn_i]`.
   wrong reading: Assuming a different or conventional unit for `spd`.

14. `ang` is calculated rather than measured directly.
   wrong reading: Treating `ang` as a direct measurement.

15. `ang` is expressed in `deg`.
   wrong reading: Assuming a different or conventional unit for `ang`.

16. `vr` is calculated rather than measured directly.
   wrong reading: Treating `vr` as a direct measurement.

17. `vr` is expressed in `[ft_i]/min`.
   wrong reading: Assuming a different or conventional unit for `vr`.

18. `rssi` qualifies the result; it is not itself a result value and must not be analysed as one.
   wrong reading: Treating `rssi` as an observed quantity.


TRANSCRIPT A

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


TRANSCRIPT B

# 1. What this feed is

Each record is one decoded radio transmission, as seen by one ground receiver. It is not an aircraft position report, and it is not a track point. The distinction runs through everything below.

Three things are fixed in every record: which airframe transmitted (the 24-bit address, annotated `featureOfInterest`), which ground station decoded it (annotated `observingProcedure`), and when that station finished decoding (annotated `resultTime`). Everything else — position, altitude, speed, angle, vertical rate, callsign, squawk — is optional, and the schema states that which of them appear is determined by the downlink-format family of the transmission.

Two consequences follow immediately, and both are stated by the files rather than inferred.

The stream is **receiver-scoped, not aircraft-scoped**. The schema says plainly that one transmission decoded by two stations yields two records, differing in signal level, in timestamp, and sometimes in the decoded position itself, because a position is solved from whichever pair of encoded messages that particular station happened to receive. There is no transmission identifier anywhere in the record. So the feed contains duplicates that carry genuinely different numbers, and nothing in it marks them as duplicates.

The stream **carries no phenomenon time**. The one temporal member is the reception instant, and the schema is explicit that this is not the instant the reported state was true aboard the aircraft. Section 4 develops this; it is the error that will cost most.

The record-level observed property is a fictional catalogue entry (the specification reserves `example-catalog` for exactly that), so it identifies but does not resolve. Any check that depends on its content is *indeterminate* in the specification's sense, and a processor may not proceed as though it had held.

# 2. Analytics

**Per-receiver decode-quality and marginality analysis.** The signal level carries `semanticRole: resultQuality`, and the schema states what within-station variation means: a low level marks a message decoded near the noise floor, which is where bit errors surviving the parity check originate. Distribution of level within one station, and the association between low level and implausible decoded values, is therefore a supported and useful analysis. It is supported *only within one station* — see §3.

**Message-format composition.** Counting records by downlink-format family, per receiver and per airframe, is well supported: the family is a closed enumeration, it is required in every record, and it determines which members are populated. This is the honest way to characterise what a receiver is actually seeing. Do not run any independence test between the family literal and the raw format numbers: the schema says the literal is *synthesised from* them, so the relationship is definitional, not empirical.

**Emergency and special-code detection.** The squawk carries `semanticRole: status`, and the schema names three values whose meaning overrides the assignment. Detecting and alerting on those three is supported by the file directly. Trend or rate analysis over squawk assignments generally is not, because the register that assigns the other codes is neither enumerated nor referenced (see §5).

**Pressure-surface analysis.** Barometric altitude is bound to its own observed property, one that names the 1013.25 hPa reference in the identifier itself. Every record's altitude is therefore expressed against the same fixed reference, and this is the one quantity in the feed that is straightforwardly comparable and differenceable across airframes and across receivers. Vertical separation between two aircraft, and altitude-band occupancy, are supported. Anything involving height above terrain or above the ellipsoid is not, and cannot be made so from these files: the schema says the offset from geometric height varies with the state of the atmosphere and is not transmitted.

**Coverage and duplicate-overlap structure.** Grouping by airframe across receivers shows which stations see which aircraft, and how often. This is supported as a *counting* exercise. It is not supported as a *range* or *coverage-polygon* exercise, because no receiver position appears anywhere in the record, and the specification forbids repairing a missing binding from labels, names or samples — which rules out parsing the station identifier for a location.

**Trajectory reconstruction.** Partially supported, with a large caveat. Position is present only in the extended-squitter family, the two coordinates are bound as a single coordinate in a named geodetic reference system, and reception instants order correctly. That is enough to draw a track. It is *not* enough to compute speeds, headings or rates from that track, because the abscissa is reception time and not the time the position was true, and the schema gives no bound on the offset other than "the transmission interval of the format concerned", which the record does not carry.

**Analyses the files do not support, and which look supported.** Reconciling the reported vertical rate against successive altitudes: blocked, because the schema says the bit stating whether the rate came from the barometric or the geometric source is not forwarded. Comparing or trending the speed member: blocked, because the bit distinguishing ground speed from airspeed is not forwarded either. Anything at all with the angle member across records: blocked, because the same discarded bit decides whether it is a ground track or a magnetic heading, and neither the drift angle nor the magnetic variation that separate them is carried. Anything depending on the interpretation of a Comm-B register: the schema says the register number is not transmitted, that a decoder infers it from the bit pattern, and that it can infer it wrongly — and no confidence value accompanies the inference.

# 3. Combination rules

The general rule the specification imposes: two values may be combined only where the record agrees on the feature, the observed property, the unit and the derivation, and — for anything qualified by the receiver — on the procedure. The specification adds that procedure equality is "evidence for candidate grouping, not proof of statistical interchangeability", so equal station identifiers licence a grouping, not an assumption of homogeneity.

Note before the individual quantities: **nothing in this feed is an accumulation and nothing is already a summary.** Every state-bearing member declares `phenomenonTimeRelation: instant` and `derivation: calculated`; none declares `derivation: statistic`. So no member may be summed, and any mean a consumer computes is a new quantity the schema does not describe. The specification is explicit that these annotations "do not authorize summation or prove complete coverage", and that a processor must not read an instruction out of them.

There is a second, subtler trap in every average. The records are not a designed time series. No cadence is declared anywhere, and the specification forbids inferring one. Message rate varies by format, by airframe and by station, and duplicate reception inflates it unevenly. A naive mean over records is therefore weighted by transmission rate, not by time, and is not a time-average of anything.

| Quantity | Compare | Difference | Sum | Average | Condition / prohibition |
|---|---|---|---|---|---|
| Airframe address | Equality only | No | No | No | The sole identity in the feed. The specification forbids inferring feature identity from location, names, or other metadata — so callsign and squawk may never stand in for it. |
| Receiver identifier | Equality only | No | No | No | Grouping key. Equality is candidate grouping, not interchangeability. |
| Format family / format numbers | Equality only | No | Counts of records only | No | The numbers select a frame layout; they are selectors, not magnitudes, and carry no code-list binding. Arithmetic on them is meaningless. |
| Comm-B register code | Equality only, distrusted | No | No | No | Inferred by the decoder, not transmitted, and can be inferred wrongly. Treat as a hypothesis, not a fact. |
| Reception instant | Yes | Yes, within the stated caveats | No | Arithmetically defined, semantically rarely wanted | See §4. Cross-station differencing additionally assumes a clock synchronisation that nothing in the files asserts. |
| Callsign | Equality with care | No | No | No | Flight identity, not airframe; changes between legs; "frequently wrong or blank" per the schema. Never a grouping key for an airframe. |
| Squawk | Equality only | No | Counts only | No | Categorical. Three values carry an overriding meaning. |
| Barometric altitude | **Yes, freely** | **Yes, freely** | No | Yes, within one airframe, with the sampling caveat above | The only cross-airframe-comparable magnitude here. Equal values mean the same pressure surface, **not** the same geometric height. Must never be combined with, converted to, or differenced against any geometric or ellipsoidal height. |
| Latitude / longitude | Yes | Only through a proper geodetic computation | No | Only within one airframe, and biased by duplicates | The pair is one coordinate in one named system; degree differences are not distances, and this specification supplies no transformation. Solutions, not readings — two stations may legitimately disagree on the same transmission. |
| Speed | **No** | **No** | No | **No** | The record cannot say whether it is ground speed or airspeed. Two values may be two different quantities. |
| Angle | **No** | **No** | No | **No** | Same discarded bit: track over ground or magnetic heading. Additionally the schema admits both 0 and 360, so equality testing fails on identical directions, and circular wrap makes arithmetic means wrong even if the ambiguity were resolved. |
| Vertical rate | **No**, except as a coarse sign/magnitude indicator within one airframe | **No** | No | **No** | The altitude source behind it is unknown, so it cannot be reconciled with the altitude member and must not be integrated to obtain one. |
| Signal level | **Within one receiver only** | Within one receiver only | No | Within one receiver only | The schema states the scale is receiver-specific and that two stations' values are not comparable. Pooling across stations is the classic error here. |

Four further prohibitions that are not obvious from the table.

**Position and altitude are not one three-dimensional position.** The coordinate binding names the two horizontal members and nothing else, and the specification says properties not named are not part of the coordinate. Altitude is bound to a *different* observed property. Treating the three as a point in a compound vertical-plus-horizontal system is exactly the error the annotation exists to prevent.

**Speed and vertical rate declare the same observed property.** Both cite the same quantity-kind reference. Their units are dimensionally the same kind, so a unit-aware processor grouping results by observed property will happily pool a horizontal speed in knots with a vertical rate in feet per minute and convert between them. Do not group by that reference. (I treat this as a defect in the schema rather than an instruction; see §5.)

**Signal level qualifies everything or nothing.** It is the record's single result-quality value, and the specification states that a record-level quality qualifies every result in the record. There is no way in this schema to attribute signal quality to the position specifically rather than to the altitude or the speed.

**The identifiers must not be parsed.** The station identifier, the callsign and the airframe address are all strings with visible internal structure and none of them carries a code-list binding. The specification forbids inferring a code-list binding from names, samples, units, or the number of members present, and forbids repairing an unresolved register from labels or samples. Splitting the station identifier on its hyphens, or reading a prefix out of the address or the callsign, is precisely the inference the specification rules out.

**A record may carry one coordinate member without the other.** Neither is required, and no dependency ties them. Nothing in the schema prevents a half-coordinate, and absence must not be imputed: absence here is structural — it means the transmission format did not carry the value — not missing data.

# 4. Time

**No member establishes the time axis of the thing described.** That is the finding, and it is stated by both files jointly.

The record's one temporal member carries `semanticRole: resultTime` — the position at which the *result became available*, that is, when the ground station finished decoding. Every state-bearing member declares `phenomenonTimeRelation: instant`. The specification says `instant` "can be resolved only when a sibling `phenomenonTime` annotation identifies a temporal position", and that otherwise "the support is declared but its temporal extent is indeterminate". There is no phenomenon-time member in this schema. So the support of every reported value is formally indeterminate, and the specification's processing rules forbid promoting the reception instant into that role: a processor must not infer a semantic role from a name, type, unit, position or sample.

The schema's own prose says the same thing in domain terms: the transmissions carry no timestamp, the sampling instant is unavailable, and it can only be bounded by the transmission interval of the format concerned — a quantity the record does not carry. The bound is therefore not computable from this feed.

**How reception positions relate to civil time.** The reception member is bound to a temporal reference system defined inside the schema itself, and that definition states the mapping exactly: a position is a count of milliseconds since 1970-01-01T00:00:00Z that ignores leap seconds. Positions increase with time. Three consequences:

*Rendering is exact and naive.* Because the scale ignores leap seconds by construction, dividing by one thousand and rendering the result as a conventional epoch instant is the correct civil rendering — no leap-second table is needed and applying one would be wrong. On the single example record this yields 2026-07-31T05:12:44.316Z. (That is my arithmetic from the value in the file, not a fact the files state.)

*Elapsed time is understated across an inserted leap second.* The definition says a position taken during an inserted leap second repeats the previous one. A difference computed across such an insertion is short of true elapsed time by one second per insertion. Whether any insertion falls inside a given interval is not determinable from these files.

*The ordering is forward but not strict.* Because positions repeat during an insertion, sorting by this member does not strictly order transmissions, and equal positions do not imply simultaneity. The declared sort order tells you the direction only.

**The unit hazard is called out deliberately.** The definition explains why the regime is declared at all: the value is a bare integer whose scale differs by three orders of magnitude from the second-counts most feeds transmit, and nothing in the payload distinguishes the two. The member does carry an explicit millisecond unit, which is what makes the scale checkable — a consumer must read that annotation rather than sniffing magnitudes.

**Cross-station time is not underwritten.** The reception instant is the *station's* clock, produced by the *station's* decoding. Nothing in either file asserts any synchronisation relation between two stations' clocks. Differencing reception instants across stations — which is what any duplicate-detection window or any arrival-time technique needs — rests on an assumption the files do not supply.

# 5. Ambiguities

**The instance contradicts the schema about what a record is. I decline to decide this, and it is the most consequential open question.** The schema says the format family "determines which members of this record are populated", and its own field descriptions confine the speed, angle and vertical rate to a velocity message, the callsign to an identification message, and the squawk to an identity reply. The example record declares one extended-squitter transmission with a type code the schema assigns to airborne position — and then carries speed, angle, vertical rate, callsign *and* squawk as well. Under one reading the example is merely illustrative and not physically realisable. Under the other, the feeder emits a merged per-aircraft state vector on every message, carrying forward last-known values. The difference is not cosmetic: under the second reading the reception instant applies only to the member that triggered the record, every other member has an unknown and individually different age, and cross-member work such as position-plus-altitude or any track reconstruction is unsound. Nothing in either file settles which reading holds, so I decline; a consumer must establish this from the producer before doing anything else.

**The format-number range is internally inconsistent, and I decline to explain it.** The schema describes that member as the first five bits of the transmission — five bits admit thirty-two values — and then constrains it to a maximum of twenty-four. The type-code member, described the same way, is constrained to thirty-one. Why the two differ is a domain matter the files do not state.

**The format-family enumeration is narrower than the format-number range.** Six family literals are defined; the numeric range admits many more values. What the feeder emits for a transmission whose format has no literal is not stated, and the family literal is required in every record. Either such transmissions are dropped, or the enumeration is incomplete. Not determined.

**The reception member is typed as a 64-bit integer and appears in the example as a quoted string.** Whether the Core specification requires or permits string encoding for 64-bit integers — as would be usual to avoid precision loss — is governed by a document I do not have. I decline to call the example non-conforming, but a consumer must not assume the value arrives as a JSON number.

**The callsign padding does not match.** The schema says the value is padded to eight characters; the example carries six. Whether the feeder trims, or the example is idealised, is not determined. Equality-matching on callsigns is unsafe until this is settled.

**No receiver position is carried.** Range analysis, coverage mapping and any arrival-time technique all need it, and it is not there. Not determined by the files, and — per §3 — not recoverable by parsing the station identifier.

**No transmission identity is carried.** Duplicate detection across stations must therefore be heuristic, keyed on airframe plus a time window, and the width of that window depends on the inter-station clock relation that §4 shows is unasserted. Not determined.

**The squawk's state set is neither enumerated nor referenced, and I read this as a probable schema defect.** The specification requires a `status`-annotated value to be constrained by an enumeration or to identify the set that defines its states. This member is constrained only by a character pattern and carries no vocabulary or code-list binding. The practical effect: the three overriding values are documented in prose that no processor may act on programmatically, and every other code is unresolvable. The keyword that would have carried the register — `codedValues` — is unused here, as it is on the Comm-B register code, where it would have been equally apt.

**The temporal reference definition may not satisfy the specification's requirement for a schema-held one.** The specification says that where a temporal reference system is held as a type in the schema, that type must declare a member whose reference role is `position`. The definition here is a scalar integer type with no members and no such role. The annotation's own shape is correct — the position property is prohibited when the annotation attaches to a scalar, and it is correctly absent — so this may be a case the specification's text did not anticipate rather than an author error. I decline to decide it. It does not change the practical reading, because the definition's prose states the encoding unambiguously.

**Speed and vertical rate share one observed-property reference.** I record this as a defect rather than an ambiguity: nothing in the files makes the two the same quantity, their units are not the same, and the shared reference is a broad quantity-kind classification. The specification warns separately that quantity-kind classification does not establish equivalence between observable properties. A consumer that groups by observed property will nonetheless pool them.

**The horizontal coordinate members are simultaneously one coordinate and two independent results.** The coordinate binding treats them as a single two-axis position; the observation-role model treats each as a separate result, and the specification states that multiple result properties in one type represent multiple results and not one combined act. Nothing decides which view governs when, for instance, quality is attributed or a record is filtered. Not determined.

**The airborne sensor chain is not identified.** The declared procedure is the ground decoder. The altitude is described as the output of the aircraft's air data computer, and the position as a solution the decoder computed — so the instrument that actually produced the altitude number is nowhere identified, and per-airframe instrument bias can neither be attributed nor controlled for. The specification calls procedure identity comparability-critical; the comparability-critical part is missing.

**No accuracy, integrity or containment-radius value accompanies the position.** The only quality value in the record is the signal level, which is receiver-scoped and, per §3, qualifies every result equally. There is no basis in these files for a position uncertainty.

**Whether a station identifier denotes a stable procedure over time is not determined.** The schema calls it stable, which fixes the identifier, not the equipment behind it. A station whose antenna or firmware changed would keep its identifier and change its signal-level distribution. The specification's warning that procedure equality is evidence for grouping rather than proof of interchangeability applies directly.

**No cadence is declared anywhere, and I will not supply one.** There is therefore no schema-supported basis for a staleness threshold, a gap detector, or a window width. The specification forbids inferring cadence from names, samples or timing, and forbids using cadence to synthesise a missing successor. Any such threshold is a consumer's own operational choice and must be documented as such.


TRANSCRIPT C

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


TRANSCRIPT D

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
