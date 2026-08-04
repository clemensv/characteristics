## 1. What this feed is

Each record is one sampling cycle from a fixed marine monitoring mooring operated in Puget Sound, Washington. A single cycle carries the CTD channels (temperature, conductivity, pressure, and the salinity derived from them), the optical channels (dissolved oxygen, pH, chlorophyll, turbidity), and a nitrate channel, all attributed to one water parcel at one stated depth at one instant.

The thing to understand before touching the data is that a record names three different physical things, and confusing them is the primary source of wrong answers. The mooring is the station the programme reports against. The water parcel at the stated depth is what was actually measured. The basin is the water body the result is meant to inform. A "station average" that silently pools parcels sampled at different depths is not an average of anything real, and a basin-level conclusion drawn from one mooring is a claim the record does not support on its own.

Cycles are nominally quarter-hourly, so the stream is a regular grid with detectable gaps rather than an irregular event log.

## 2. Analytics worth running

**Diel and seasonal cycling.** Temperature, oxygen, chlorophyll and pH at a fixed station and depth on a fifteen-minute grid resolve the daily light-driven cycle cleanly. The cadence is declared and fixed, so a missing slot is a genuine gap rather than a scheduling artefact, and you can quantify completeness rather than guess at it.

**Hypoxia exposure.** Both oxygen concentration and percent saturation are present, and both are timestamped to the instant the condition held for the sampled parcel. Threshold crossings and time-below-threshold are therefore computable — with the caveat in section 4 that these are point values, not fifteen-minute block means.

**Bloom detection with a confounder control.** Chlorophyll and turbidity are read concurrently from the same parcel. Elevated fluorescence accompanied by elevated turbidity is a different story from elevated fluorescence alone, and the concurrency is what makes the discrimination possible.

**Nutrient drawdown.** Nitrate and chlorophyll share a timestamp and a parcel, so uptake episodes can be examined without cross-feed alignment.

**Freshwater and stratification signals.** Salinity and temperature together characterise the parcel's water mass. True stratification analysis requires records at differing depths within the same cycle; whether the feed supplies those is not established (section 5).

**Patchiness and sensor health.** The two standard-deviation channels summarise within-cycle bursts and give a within-cycle variability signal that the instantaneous channels cannot. Their usefulness is bounded by the unpublished burst configuration.

**Pipeline latency and completeness.** The gap between the observation instant and the publication instant is directly measurable per record, giving a latency distribution, a basis for choosing a watermark in any streaming consumer, and a way to distinguish a genuinely absent reading from one that simply has not arrived yet. The example record shows roughly twenty-four minutes.

**Quality-flag epidemiology.** Flag prevalence over time at a station is a leading indicator of sensor fouling, drift or failure, independent of the physical signals themselves.

## 3. Combination rules

**Blanket gates that apply to every quantity below.** Two values are candidates for comparison, differencing or averaging only when the station agrees, the sampled depth agrees, the sonde agrees, and the summary function agrees. The sonde identity is comparability-critical and is stated to be so: readings from a different package are not interchangeable even when the property and the station match, so any recalibration or hardware swap that changes the sonde URI creates a seam in the series that must be handled as a seam, not smoothed over. Records flagged `fail` or `missing` must be excluded before any aggregate; `not_evaluated` means no test was applied and must not be treated as equivalent to `pass`; `suspect` should be carried through as a marked subset rather than silently kept or silently dropped. There is exactly one flag per record, not one per channel — see section 5.

**Water temperature.** Compare and difference freely within the gates. Average freely, but only as a time-weighted mean over an unbiased set of slots; a gappy day averages toward whatever hours survived. Never sum: Celsius has an arbitrary zero, so a sum of temperatures is not a quantity. Note that a *difference* of two Celsius values is a well-formed interval even though the values themselves are not on a ratio scale.

**Conductivity and specific conductivity.** These two must never be compared with each other, differenced against each other, pooled, or fed into the same series — despite carrying the same unit, the same symbol and the same standard-name reference. One is read at the in-situ temperature, the other is normalised to 25 °C. Identical units and identical property references here mean identical *dimension*, not identical *quantity*. This is the sharpest trap in the feed, because every naive check an analyst might run to confirm the two are compatible will pass.

Within its own series, in-situ conductivity may be compared, differenced and averaged, but any change in it conflates a change in ionic content with a change in temperature; if you want the ionic signal, use the specific conductivity or the salinity. Specific conductivity may be compared, differenced and averaged across records that differ in temperature — that is what it exists for. Neither may be summed.

**Pressure.** Compare, difference and average within the gates. Do not sum. The reference datum is not stated (section 5), which restricts differencing to within this feed.

**Salinity.** Compare, difference and average within the gates. Do not sum. The critical restriction is statistical rather than dimensional: salinity is a deterministic function of the conductivity, temperature and pressure in the very same record. It is not an independent observation. Placing salinity alongside temperature and conductivity as co-predictors in a regression, or reporting a correlation between salinity and conductivity as a finding, is degenerate — you are measuring the definition, not the ocean.

**Dissolved oxygen concentration.** Compare, difference and average within the gates. Never sum, and never attempt a mass or inventory total: this is an intensive concentration, and the feed carries no volume, no water-column geometry and no station coordinates with which to integrate it.

**Oxygen saturation percentage.** Compare, difference and average within the gates, and do not sum. Two further restrictions. It is computed from the oxygen concentration together with the concurrent temperature, salinity and pressure, so it is not independent of any of those and must not be treated as a separate observation in a joint statistical model. And because solubility is a nonlinear function of temperature and salinity, the mean of the saturation values is not the saturation computed from the mean concentration; pick one convention and do not mix results derived under both.

**pH.** Comparison and differencing are valid — a pH difference is a log ratio of hydrogen-ion activity and is meaningful. Arithmetic averaging is not valid if what you want is a mean hydrogen-ion activity, because the scale is logarithmic; convert, average, convert back, or state explicitly that you are reporting a mean of the logarithm. Never sum. Comparison against pH from any external source is valid only if that source is also on the total scale; the scale is stated here precisely because scale mismatch silently corrupts such comparisons.

**Chlorophyll.** Compare, difference and average within the gates. Do not sum. Cross-station and cross-instrument comparison is not supported, because whether this channel is raw fluorescence or a calibrated concentration is left open (section 5) — within one station and one sonde the series is internally consistent either way, which is why the ambiguity only bites when you widen the scope.

**Turbidity.** Same rules as chlorophyll. NTU is defined by the measurement geometry of the instrument, so the sonde gate is not a formality here: turbidity from a different optical package is a different quantity in practice even under the same unit.

**The two standard-deviation channels.** These carry the same observed property as their parent channels but a different summary function, and they are therefore not like quantities. Do not compare a standard deviation to a concentration, do not difference them, do not place them on the same axis as if they were the same measurement, and do not let them fall into the same aggregation as the parent channel. A ratio of standard deviation to mean is a legitimate derived index of within-burst variability, but it is a new quantity, not a comparison of the two.

Standard deviations must not be averaged across records, and must not be pooled into an aggregate spread. Pooling requires variances and per-burst sample counts; the burst length is configured per deployment and is not published, and no support period is declared. Even comparing one record's standard deviation to another's rests on the assumption that both bursts had the same configuration — an assumption the feed does not license. Treat cross-record comparison of these channels as provisional and say so.

**Nitrate.** Compare, difference and average within the gates; do not sum. Comparison against any external nitrate series is blocked until the unit question in section 5 is resolved.

**Across stations.** Different stations sample different places. Values may be compared at the level of the basin they are interpreted for, and only when the basin agrees and the procedure agrees. Nothing in a record licenses inferring the basin from the station or the parcel; the basin is stated independently precisely because it is not derivable.

**Across depths.** Different depths are different parcels. Differencing across depths within a cycle is the correct way to compute vertical structure. Pooling across depths into a single station mean is not an average of a physical quantity and should never be done implicitly.

## 4. Time

The observation timestamp is the time axis of the thing described: the instant at which the stated conditions held for the sampled water parcel. It is UTC, ISO 8601, and lands on quarter-hour slots under a declared fixed fifteen-minute cadence, so the series can be treated as a regular grid and an absent slot read as a real gap.

The publication timestamp is the instant the reading became available downstream, after telemetry and automated quality control. It trails the observation by minutes to hours and must never be used to bucket, bin, window or sort the physical signals. Its legitimate uses are latency measurement, late-arrival handling, watermarking, and as-of reconstruction of what a consumer could have known at a given moment. A dashboard that plots temperature against publication time is showing the behaviour of the data pipeline, not the water.

All sensor channels are instantaneous point values, not fifteen-minute averages. This matters for any integral: time below an oxygen threshold, cumulative exposure, or daily load must be obtained by interpolating between points, and treating each value as representative of the whole quarter-hour block is a modelling choice you are making, not something the data states. It also caps the resolvable frequency — anything varying on a timescale shorter than about half an hour aliases.

The two standard-deviation channels are the exception: they characterise an interval inside the cycle rather than an instant, and the extent of that interval is not published. They cannot be aligned to a known window and should not be plotted as though they applied to the full quarter hour.

Relating positions on the axis to civil time requires a conversion the record does not carry. The stations are described as being in King County, Washington, which places them in the US Pacific zone with summer time — an inference from the prose, not a declared member. Any diel analysis must convert to local time properly rather than applying a fixed offset, or the summer half of the year will be smeared by an hour against the solar cycle that drives the very signals being studied.

## 5. Ambiguities

**Whether the sampled depth is fixed or varies between cycles.** The measurement package is called a profiling sonde, which suggests the depth may change from cycle to cycle, while the example shows a single shallow depth. This is the single largest hazard in the feed: if depth varies, a naive time series "at the station" silently interleaves different water parcels and every trend derived from it is suspect. **Declining to decide.** Determine it empirically from the data before building anything, and treat depth as a grouping key until you have.

**Records without a depth.** The depth member is not required, so a record may arrive with no proximate feature identified. Such a record cannot be placed in the water column and cannot be pooled with records that carry a depth. What the producer intends by omitting it is **not determined**; excluding those records from depth-scoped analysis is the conservative course.

**Whether the quality flag covers the whole record or a single channel.** Only one flag is present, and it is described as classifying "this reading." **Guess: it applies to the record as a whole.** If it is in fact a roll-up of per-channel flags, then a `suspect` record may have exactly one bad channel and discarding it wholesale throws away good data — while a `pass` record could in principle hide an unevaluated channel. The distinction changes the yield of the dataset materially and cannot be settled from what is here.

**The nitrate unit.** The unit given is micromoles — an amount of substance — while the description calls the value a concentration. A concentration requires a volume or mass denominator. **Guess: micromoles per litre.** This is a guess and should not be relied on; the values cannot be compared with any externally sourced nitrate series, in µmol/L or µmol/kg, until the producer resolves it.

**The pressure datum.** Whether pressure is absolute or referenced to the sea surface is not stated. **Guess: sea-surface-referenced**, since the example shows roughly one decibar at roughly one metre, whereas absolute pressure at that depth would be about eleven. Differencing within the feed is unaffected; comparison to external pressure data is blocked until confirmed.

**Whether chlorophyll is raw fluorescence or calibrated concentration.** The description offers both readings of the same channel. **Not determined.** Within one station and one sonde this does not matter; it blocks absolute concentration claims, cross-station comparison, and any comparison to laboratory or satellite chlorophyll.

**Burst length and sample count behind the standard-deviation channels.** Explicitly unpublished and explicitly left indeterminate. **Declining to decide.** Consequences are set out in section 3: no pooling, no variance arithmetic, and cross-record comparison only under an assumption of stable deployment configuration.

**Revisions and duplicates.** There is no version, sequence or revision member. If a reading is reprocessed and republished, nothing distinguishes the correction from a duplicate except the later publication timestamp. **Guess: deduplicate on station and observation time, keeping the latest publication timestamp.** That is a plausible convention, not a stated one, and it will silently discard a genuine second reading if the producer ever emits two distinct parcels in one slot.

**Absence versus the `missing` flag.** Every measurement channel is optional, and the flag vocabulary also includes `missing`. Whether an omitted field and a `missing` flag mean the same thing, or whether one indicates a channel not fitted to this deployment and the other a channel that failed, is **not determined**.

**Station location.** There are no coordinates. No mapping, no spatial interpolation, no comparison against satellite products or circulation model output is possible without an external station registry, which is outside this feed.

**Trust in the descriptive text.** The schema records that it inherited a description from an upstream feeder that was outright wrong for this record and had to be replaced. That is a useful warning: the descriptive prose here is a corrected artefact of a chain of copies, and any single description should be treated as authoritative only where it is internally consistent with the units, roles and example values. The nitrate unit mismatch above is plausibly one such residue.
