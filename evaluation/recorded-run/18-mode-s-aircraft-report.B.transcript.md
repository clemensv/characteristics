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
