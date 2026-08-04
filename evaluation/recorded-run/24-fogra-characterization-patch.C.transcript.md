# 1. What this feed is

Each record is one calibration point of a printing press: a specific combination of four ink amounts that was **commanded** to the press, paired with the colour that was **measured** off the sheet where that combination landed. The records are transcribed from a published characterization file (FOGRA51) held in the ICC's characterization data registry, and the whole set of them — 1617 patches — constitutes a description of what colours that particular printing condition can produce and how ink requests map onto them.

The single most important thing to understand before touching this data: the record contains two different kinds of number that the schema does not structurally distinguish. The four ink values are an *instruction*, not an observation. The three colour coordinates are an *observation* of the result. Both are tagged with the same role in the schema, so nothing but the prose descriptions tells you which is stimulus and which is response. Any pipeline that treats all seven values as measurements of the same thing is wrong from the first line.

The second thing: the colour readings are only meaningful relative to a stated set of measurement conditions, and those conditions are attached to the record as a free-text sentence with no internal structure. They are not decoration. They are the precondition for the readings meaning anything at all.

# 2. Analytics

**Forward device characterization — modelling ink request → resulting colour.** This is what the data is built for. Every record is an exact input/output pair under one fixed measurement condition, and the target sweeps 1617 combinations, so the relation can be fitted, interpolated, or tabulated across the ink space. The files support this because the ink values are stated as exact commanded amounts (not recovered estimates) and every colour reading in the file shares one declared colorimetric space and one measurement condition.

**Gamut extent.** The set of measured colour coordinates across all patches bounds what this printing condition can reach. Supported because all readings share illuminant, observer, and measurement conditions, so they are points in one common space and their extent is a coherent object.

**Colour difference between patches.** The schema states the colour scale is perceptually near-uniform, which is exactly the property that licenses treating distance between two patches as a difference magnitude. Supported for any pair of patches sharing the measurement condition. Note the limit: the files license *a* distance interpretation on this scale; they do not name or specify any particular difference formula, so anything beyond a plain distance in the three coordinates is your choice, not theirs.

**Per-channel tone response.** Records in which three of the four inks are zero isolate one ink's behaviour across coverage. The example record is such a case — full cyan alone. Supported because the ink amounts are exact and independently specified per channel.

**Neutrality analysis.** The schema states that the zero of the two chromatic coordinates is fixed by the illuminant, not by the sheet. That makes "how close is this patch to neutral" a well-posed question with a fixed reference, so grey-axis behaviour across the black-ink patches is analysable. This would *not* be well-posed if the zero were sheet-relative, and the schema is explicit that it is not.

**Total commanded coverage.** The four ink values share a unit and a basis (percentage of full coverage), so their sum within a record is arithmetically well-defined and its distribution across the target is computable. Whether that sum is a meaningful or constrained quantity in printing is not established by these files.

**Conformance comparison against another dataset.** Possible in principle, but only under the gate described in §3 — and see §5, because the gate cannot be evaluated mechanically.

**Analyses this data does not support.** Nothing temporal: there is no time member, so no drift, trend, repeatability, or run-to-run comparison is available (see §4). Nothing about measurement uncertainty: no uncertainty, replicate count, or tolerance is carried. Nothing spectral: only three colorimetric coordinates are present per patch, and the files carry no member that would let the readings be restated under a different illuminant or observer than the one declared. Whether such restatement is possible at all from these members is outside what the files decide; what is decided is that the inputs for it are not here.

# 3. Combination rules

**Patch index.** An identifier of position within the target, not a magnitude. Never difference, sum, or average it. The only valid operation is equality — matching the same patch across datasets, if you have another dataset built on the same target. Whether the index is unique, dense, or one-based is not established. Whether adjacent indices are adjacent on the physical sheet is also not established; do not read spatial locality into the ordering.

**The four ink amounts.** All four carry the same unit and the same basis, so within a single record they may be summed. Across records they may be compared and differenced, but only between records whose CMYK space resolves to the same registry entry — these are device coordinates for one specific printing condition, and an ink percentage from a different printing condition is a different quantity wearing the same name. Do not compare or difference them across printing conditions.

Averaging ink values across records is arithmetically defined but analytically misleading, and this is worth stating plainly: the population of patches is a *target design*, chosen to sample the ink space. A mean ink amount across records therefore describes how the target was laid out, not anything about the press, the ink, or the paper. It is a property of the questionnaire, not of the answers.

**Lightness.** Differences between patches are the licensed combination, because the schema states the scale is perceptually near-uniform — that is precisely a claim that equal differences mean equal amounts. Comparison and differencing are valid only between readings taken under identical illuminant, observer, and measurement conditions. Ratios are not licensed by anything in the files: the scale's upper end is fixed by the illuminant and the measurement geometry, which is a convention, and nothing here establishes that the scale is proportional to any underlying physical quantity. Treat it as an interval scale and do not compute ratios or percentage changes on it.

**The two chromatic coordinates.** The schema is explicit that their zero is set by the illuminant and not by anything in the sheet. That makes them interval quantities with a conventional origin. Consequences, each of which is a common error:

- Differences are valid; ratios are not. A patch with twice the chromatic coordinate value of another is not "twice as red."
- A value of zero does not mean the ink has no red–green or yellow–blue character. It means the patch sits on the neutral axis *as defined by D50*. Under a different illuminant the same sheet would not sit at zero.
- Summing these coordinates across records is meaningless. There is no aggregate they add up to.
- Sign carries direction and must not be discarded before averaging; averaging magnitudes and averaging signed values give different and non-interchangeable results.

**The three colour coordinates together.** They are the three components of one point, not three independent measurements. Never sum or average them with each other. The combination the files license across the triple is distance between two patches.

Componentwise averaging of the triple across records yields a centroid in the perceptual space. That is a defensible object, but it is the centroid of a *set of patches*, not the colour of any mixture of inks and not a summary of the press — and, as with the ink values, the set was chosen by the target designer, so the centroid describes the target's sampling plan.

**Ink amounts and colour coordinates must never be combined arithmetically with one another.** They differ in kind (instruction versus observation) and in unit (one carries a percentage unit, the other carries no unit at all — which also means the colour coordinates must not be fed through any unit conversion or auto-scaling machinery).

**Channel ordering.** When assembling the four ink values into a tuple for any downstream model, take the order from the declared channel list — cyan, magenta, yellow, black. Do not derive it from the member names. The schema warns about this explicitly, and the warning is real: the fourth channel is named for the printing term rather than for the letter it is conventionally abbreviated with, so alphabetical or naive ordering produces a silently wrong tuple that will still typecheck and still run.

**The gate on all cross-record colour combination.** The measurement-condition text is stated to apply to every patch in this file, so within one file all colour readings are mutually comparable and differenceable. Across files, they are comparable only if both the colorimetric space declaration *and* the measurement-condition text agree. Illuminant and observer are machine-comparable. The geometry, the filter state, the backing, and the measurement standard are only present as prose, so this gate cannot be evaluated by a program. See §5.

**Records lacking the measurement-condition text.** That member is not required. A record without it retains illuminant and observer from the space declaration, but geometry, filter, backing, and standard are then unknown. Do not pool such records with records whose conditions are known, and do not assume they share the conditions of the record next to them in the stream.

# 4. Time

**No member establishes a time axis, and I decline to assign one.** The question presupposes something these files do not provide.

Specifically:

- There is no timestamp, date, epoch, duration, or timezone anywhere in the record.
- The patch index is an index into a target's patch inventory. It is a position in a *layout*, not a position in time. Nothing states that patches were printed or measured in index order, and even if they were, no origin or spacing is given, so the index cannot be converted into a position on any time axis.
- The measurement-condition text names a standard with a year attached. That is the edition year of a document. Treating it as a measurement date, an acquisition date, or a validity window would be a serious error, and I want to name it because it is the one number in the record that looks like a date and is not one.

The consequences are worth stating, because they determine what you can and cannot build. These records cannot be time-joined to anything. They cannot be trended, aged, windowed, or ordered chronologically. Two records carrying the same patch index cannot be distinguished, ordered, or reconciled — nothing here identifies a printing occasion, a measurement session, or a run. If you are pooling data from more than one source, you have no way to detect that you have mixed occasions together.

If your platform requires an event time for ingestion, you must supply it from outside this data and you must record that you did so. Do not synthesise one from the patch index.

*Guess, marked as such:* the source file this was transcribed from very likely carries dating information in header lines that were not brought across, since only one header line was preserved. I have no evidence for this beyond the fact that one header line was explicitly carried and the schema admits no other members. Treat it as a lead for recovering provenance, not as a fact.

# 5. Ambiguities

**The measurement condition cannot be compared mechanically.** *Declining to decide.* The schema itself says the geometry, filter, backing, and standard have no keyword of their own and survive only as text. So the precondition for pooling colour readings across datasets is a free-form sentence, and two datasets that are genuinely equivalent may state it differently, while two that differ materially may differ in a way a string comparison misses. I am not going to rule on how to normalise it. What I will say is that this comparison must be treated as requiring human adjudication, and a pipeline that silently pools on illuminant and observer alone — the two things that *are* machine-readable — will pool data it should not.

**The measurement-condition designation appearing at the end of that sentence.** *Declining.* It names a defined measurement condition, but nothing in these files defines it or states what it implies about the readings. I will not guess at its meaning. What follows regardless: two datasets differing in it must not be assumed poolable.

**Value ranges.** *Not determined.* No bounds are declared on any numeric member. Whether ink amounts are confined to 0–100, whether lightness can exceed 100, and whether the chromatic coordinates have any practical envelope are all open. Do not build validation on assumed ranges.

**Whether the mapping is invertible.** *Not determined, and not decidable from one record.* Whether distinct ink combinations can produce indistinguishable measured colour is a property of the full set, not of the schema, and the files say nothing about it. If you are building a separation (colour → ink), you must establish this empirically from the full 1617 patches; do not assume a unique inverse exists.

**Whether each reading is a single measurement or an aggregate.** *Declining.* No replicate count, no uncertainty, no aggregation method is present. I could offer a plausible convention here and I am deliberately not doing so, because the answer changes how you would weight or de-noise the data and guessing it would be worse than leaving it open. Treat the readings as of unknown replication.

**Patch index semantics.** *Not determined.* Uniqueness, base (0 or 1), density over 1..1617, and any relationship to physical sheet position are all unstated. Do not assume the index is a usable spatial coordinate.

**What the identifiers point at.** *Not determined.* The observed-property reference and the schema identifier are placeholder addresses that do not resolve, so the formal definition of "printed colour" behind them is unavailable. The CMYK space reference looks like a real registry entry but its contents are not available here — which means the substrate, ink set, press, and screening that define this printing condition are named by reference only and are not present in the data. Anyone comparing this to another dataset is comparing two registry keys, not two described conditions.

**What was dropped in transcription.** *Not determined.* The record admits no members beyond those defined, and one header line was carried through explicitly. Whatever else the source file held — further headers, further columns — is absent, and nothing here says what it was.

**The role tagging does not separate stimulus from response.** *Not an ambiguity so much as a hazard, and I am flagging it as one.* All seven numeric members carry the same semantic role. The distinction between the four commanded inputs and the three measured outputs exists only in the prose descriptions. Any consumer that routes on the role annotation alone will treat the press instruction as a measurement of the sheet. This is the failure mode most likely to occur and least likely to announce itself.

**What "sent to the press" means precisely.** *Not determined.* Whether the stated ink amount is the value before or after any device-side transform is not established. This matters if you intend to reproduce the condition rather than merely model it.
