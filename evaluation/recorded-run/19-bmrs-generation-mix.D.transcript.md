# 1. What this feed is

Each record is one half-hour slice of the British transmission system's generation picture: for a single GB settlement period it gives the average electrical power, in megawatts, delivered by each metered fuel category, plus the average net power flowing over each of the cross-border cables into or out of GB. Records are power, not energy, and every figure is an average over the half hour rather than an instantaneous reading — so a record cannot tell you anything about what happened inside its own thirty minutes.

The population is not "GB generation". It is generation that is metered in the Balancing Mechanism. Plant connected to distribution networks is outside that boundary. This is stated for wind but the boundary is a property of the metering arrangement, not of wind, so it should be assumed to apply to every fuel member: the record is a view of the transmission-metered fleet, and it systematically undercounts anything embedded. There is no member for solar at all, and no total, no demand figure, and no price.

# 2. Analytics

**Energy accounting.** Every value is a mean over a fixed half hour, so multiplying by 0.5 h converts any member to MWh for that period, and those MWh values are additive across periods and across members. This is the foundation for every volumetric question — daily fuel volumes, monthly totals, annual mix.

**Fuel mix and share of generation.** The fuel members partition the metered fleet by fuel type, and `other_mw` is explicitly the residue of that partition, so summing them gives a closed total against which shares can be taken. The share is a share of transmission-metered generation and must be labelled as such; it is not a share of GB electricity.

**Ramping and variability.** Successive records on a common time axis with an identical support length make first differences meaningful: MW per half hour of ramp for any member. Wind variability, CCGT following, and the correlation between them are all directly supported, because the periods are equal-length and so the differences are comparable to each other without reweighting.

**Residual load proxy.** Total metered generation minus wind (and minus nuclear, if the question is about must-run) gives what dispatchable plant had to cover. The files support the arithmetic; they do not support calling it demand, since no demand member exists.

**Net interconnector position.** All the interconnector members share one sign convention — positive is import to GB — so they may be summed into a single net import figure. Movement of that figure over time, and its relationship to CCGT and wind, is well supported.

**Displacement and event detection.** Zero and near-zero runs in `coal_mw` and `oil_mw` are directly readable, so dating the last coal hour, or counting oil-running periods, is straightforward. `ocgt_mw` becoming non-zero is a scarcity signal in its own right, because those units are described as reserve plant that runs for minutes.

**Diurnal and seasonal profiles.** Supported, but the grouping key must be derived from the UTC instant, not from the period number (see §4).

**Not supported by these files:** carbon intensity, emissions, capacity factors, plant availability, prices, curtailment, and anything about the mix inside a half hour. Each of those needs external data — emissions factors, installed capacities, market data — that is nowhere in the record.

# 3. Combination rules

**Across records, same member.** All the MW members may be compared, differenced and averaged freely across records. The reason is that every value is a mean over a support of identical length, so no weighting is required: the arithmetic mean of N period means is the true mean power over those N periods, and a difference between two of them is a genuine change in mean power.

**Summing a member across records is wrong as stated.** Adding MW to MW across periods yields a quantity with no physical meaning. Convert to energy first — multiply each value by 0.5 h — and then sum. This is the single most common error available with this feed.

**Across members, within one record — fuels.** `ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw`, `nuclear_mw`, `wind_mw`, `biomass_mw`, `npshyd_mw`, `ps_mw` and `other_mw` are disjoint categories of the same metered fleet, measured the same way, so they may be summed into a metered-generation total. `npshyd_mw` and `ps_mw` are stated to be disjoint, so summing them does not double-count.

**`ps_mw` needs a decision before it goes into a total.** It is gross generation from pumped storage, not a net position; the pumping load is not carried here as a negative and lives in the demand side of the settlement data, which this feed does not contain. So a total that includes `ps_mw` counts energy that was drawn from the same system earlier. That is correct for "what was supplied in this half hour" and wrong for "what was produced from primary energy in this half hour". Pick one and say which.

**Interconnectors must not be added to a fuel total unlabelled.** They are signed net flows on cables, not fuel output, and they go negative when GB exports. Adding them to a generation sum silently produces a supply-to-GB figure in which an export is treated as negative generation. That may be what you want, but it must be a stated choice, not a side effect. If you want generation, exclude them. If you want supply, include them and rename the result.

**Interconnectors may be summed with each other.** They are separate physical cables with a common sign convention, so their sum is a well-defined net GB import. Do not merge `intfr_mw` and `intifa2_mw` on the grounds that both go to France — they are distinct cables with distinct capacities and are reported separately; keep them separate unless you specifically want the France corridor total, in which case sum them and say so.

**`ccgt_mw` and `ocgt_mw` must not be pooled into "gas" for operational analysis.** They are the same fuel but operationally unrelated fleets — bulk energy plant against short-duration reserve. Pooling them is legitimate for a fuel-consumption or emissions question and misleading for a dispatch or flexibility question.

**`settlement_period` must not be averaged, summed, or differenced across a day boundary or across a clock change.** It is an ordinal label within a day whose count per day is not constant. It may be used for equality comparison and for ordering within a single settlement day only.

**Missing is not zero.** Only the period number and the start instant are guaranteed present; every MW member may be absent. An absent member means the value was not reported, and treating it as zero will silently understate totals and manufacture false ramps. The example record does carry explicit `0.0` for the plant that was not running, which suggests the publisher distinguishes the two cases, but that is one record and is not a guarantee — code defensively.

# 4. Time

The time axis is established by `start_time`, and by nothing else. It is a UTC instant marking the beginning of the period, and it is the only member that identifies a record absolutely; the period number alone does not, because it carries no date.

Each period is half an hour long and half-open — the interval is `[start_time, start_time + 30 min)` — so the value attaches to that whole span, not to the instant. Consecutive records tile without overlap and without gaps, which is what makes differencing and averaging across them sound. There is no end instant in the record; it is implied by the fixed length.

Relation to civil time: the positions are UTC, so mapping to British civil time requires applying the Europe/London offset for the date in question — UTC in winter, UTC+1 under British Summer Time. The example instant, 05:30Z on 31 July 2026, is 06:30 local. Any grouping by hour of day, any "morning peak" definition, and any daily boundary must be computed from the UTC instant plus that offset, and must not be computed from the period number, because the period-to-clock-time mapping is not fixed across the year.

# 5. Ambiguities

**The anchoring of period 1 is self-contradictory, and I decline to decide it.** The period number is said to start at 1 at midnight UTC, which would give 48 periods every day of the year. It is also said that the day has 46 periods at the spring clock change and 50 at the autumn one, which can only be true if the day is anchored on local midnight. Both cannot hold. The single example record is consistent with the UTC anchoring and not with the local one: 31 July 2026 is inside British Summer Time, so local midnight is 23:00Z the previous day, which would put period 12 at 04:30Z, whereas the record says 05:30Z. One example is not enough to overturn a stated rule about clock-change days, and the two readings differ by a whole period for half the year. Do not derive clock time from the period number under any circumstances; use `start_time`, which is unambiguous either way.

**Units are asserted only in prose and in member names, not declared.** That megawatts are meant is stated in the descriptions and echoed by the `_mw` suffixes, and the magnitudes in the example are consistent with GB at that scale. But there is no machine-readable unit on any member, so unit correctness cannot be validated automatically and must be enforced by convention. I am treating MW as established by the prose; I flag that nothing checks it.

**The per-member support declaration is claimed but not present.** The time member asserts that each value member states its own half-hour support. No such declaration appears on any value member. The half-hour length is therefore known only from prose. This matters because the whole case for unweighted averaging across records rests on equal support; that case currently rests on narrative, not on anything a tool can read.

**Whether the metering boundary applies beyond wind is my assumption.** The Balancing-Mechanism-only scope is stated explicitly for wind alone. It is a property of how the data is collected rather than of the fuel, so I am assuming it applies to every fuel member, and therefore that every total from this feed is a transmission-metered total that undercounts embedded plant. This is an assumption, clearly marked. If it is wrong, the fuel totals are more complete than I have said; it is not wrong in a way that would make them less complete.

**The absence of solar is unexplained.** There is no solar member. Whether solar is genuinely absent from the metered fleet, is folded into `other_mw`, or is simply not reported is not determined. My guess — and I mark it as a guess — is that GB solar is overwhelmingly distribution-connected and therefore falls outside the metering boundary, which would mean it is absent rather than hidden inside `other_mw`. Either way, do not present any mix figure from this feed as including solar.

**Revisions and record identity are undetermined.** There is no revision number, publication timestamp, or version flag. If the publisher ever restates a settlement period — and settlement data of this kind commonly is restated, which is domain knowledge and not something these files establish — there is no way to tell an initial value from a corrected one, and no way to order two records for the same instant. Treat `start_time` as the key and decide a last-write-wins or first-write-wins policy explicitly; the files do not decide it for you.

**Sign conventions on the fuel members are not stated.** The interconnectors are explicitly signed; the fuel members say nothing about sign. Whether a fuel member can ever be negative — station load, metering correction — is not determined. I decline to guess. Validate for negatives and investigate rather than clipping them.

**`intelec_mw` naming.** The code reads like a generic abbreviation for electricity but is said to name one specific cable to Ireland. Nothing here is ambiguous about the meaning; the risk is purely that a reader will mistake it for a total or an aggregate. It is not one.

**`other_mw` composition is undetermined.** It is the residue of BMRS's own fuel-type reporting, so its contents can change if BMRS begins reporting a fuel separately. Nothing in the files pins its composition or warns of a break. Do not model it as a stable category over long spans.
