## 1. What this feed is

Each record is a half-hourly snapshot of how the GB transmission system was being supplied during one settlement period: the mean power output of each metered generation fleet, broken down by fuel or technology, plus the mean net power flowing on each of seven interconnectors to neighbouring systems. It is an *outturn* summary — what actually happened over a closed half-hour — not a forecast, a schedule, or an instantaneous reading. Everything is a mean over the same half-hour window, expressed in megawatts, so a record is a power picture, not an energy total.

Two scope limits matter more than anything else about this feed. First, its population is plant metered in the Balancing Mechanism. Wind connected to distribution networks is simply not in it, so the wind figure is a floor on GB wind, not a measure of it. Second, the interconnector members are not fuels. They are cables carrying signed net flow, and a negative value is GB exporting — which is a load on the GB system, not negative generation.

## 2. Analytics this stream supports

**Energy accounting.** Because each value is an interval mean over a support of known, fixed length, energy for a period is the value times half an hour, and periods can be accumulated into daily, monthly or annual MWh by fuel. This is the single strongest thing the feed enables, and it is only sound because the statistic and the support length are both pinned down; a stream of instantaneous readings would not permit it.

**Fuel-mix composition and shares over time.** All generation members share a unit, a statistic, a support length and an interval, so they are on a common footing within a record and their shares are meaningful — once you have chosen a denominator, which is a modelling decision the data does not make for you (see §3).

**Ramping and flexibility analysis.** Differences between consecutive records give MW change per half hour per fleet. This is well defined because successive records are the same statistic over adjacent, equal, non-overlapping windows.

**Dispatch-regime classification.** Nuclear held near-flat, CCGT following net demand, and OCGT sitting at zero for long stretches are distinguishable behaviours, and OCGT moving off zero is itself a signal — that fleet exists to run for minutes as reserve. A separate CCGT and OCGT breakdown is what makes reserve activation visible at all.

**Wind variability, for balancing purposes.** Volatility, persistence, and low-wind episode length are all computable — but as properties of *transmission-metered* wind, which is the population that actually matters for balancing actions, not as properties of the national wind resource.

**Interconnector position and reversal analysis.** Net import, per-cable utilisation, direction flips, and coincidence of import surges with low wind are all supported, because every cable carries the same sign convention and the same support.

**Diurnal and seasonal profiling** — provided the time axis is handled as in §4, not via period numbers.

## 3. Combination rules

**Within one record**

- The ten generation members may be summed. They share unit, interval, support and statistic. Note that only one disjointness claim is actually established — non-pumped hydro and pumped storage are stated to be separate populations. That the remaining fleets do not overlap is a reasonable reading of the fuel labels but is an *assumption*, not something the data guarantees; the one explicit warning about category placement is that units converted from coal are counted as biomass, not coal.
- The seven interconnector members may be summed with each other. They share a sign convention (positive = import to GB), so the sum is a well-defined net import position and its sign is meaningful.
- Interconnectors must **not** be silently added to the generation total. Doing so treats an export as negative generation, which it is not: an export is a withdrawal from the GB system. Any "total supply" figure requires an explicit decision — count imports only, count net flow, or exclude cables — and that decision changes the answer whenever any cable is exporting. In the sample record two cables are exporting while five are importing, so this is not a hypothetical.
- CCGT and OCGT must not be added together and then reasoned about as one gas fleet for anything dispatch-related. Arithmetically the sum is fine; interpretively it merges bulk energy plant with short-run reserve plant, and the resulting series answers no question anyone is asking.
- Pumped storage output must not be treated as a net storage position. Pumping load is absent from this record entirely — it is metered as demand elsewhere — so charge/discharge balance, round-trip efficiency, and state of energy cannot be derived here at any level of aggregation.
- Absent members must not be read as zero. Only the period number and the start instant are guaranteed present; every measured value is optional. The sample record shows that a genuine zero is transmitted as `0.0`, so absence and zero are distinguishable in principle — but what absence *means* is not established (see §5). Coercing missing to zero silently biases every sum, share and mean downward.

**Across records**

- Any single quantity may be compared, differenced and averaged across records: same unit, same statistic, same support length, adjacent non-overlapping intervals.
- An unweighted mean of N consecutive records equals the time-weighted mean power over that span **only if** the span is contiguous and complete. Every gap breaks that equivalence, and the feed carries no completeness guarantee — the declared half-hourly cadence states what the publisher intends to emit next, not that it did.
- Records must be aligned on the start instant, not the period number.
- The period number must never be summed, averaged, differenced, or used to compute elapsed time. It is an identifier, it restarts each settlement day, and the number of periods per day is not constant — 48 normally, 46 and 50 at the two clock changes. Differencing period numbers across a day boundary or a clock change yields a wrong duration.
- Do not compare the wind figure against any externally sourced GB wind total, or against a capacity base that includes distribution-connected wind. Different populations; the ratio is not a capacity factor.

## 4. Time

The start instant is the time axis. It is the beginning of the interval each value describes, given as a UTC instant, and every value in the record applies to the half-open half-hour that begins there — start inclusive, start-plus-thirty-minutes exclusive. Successive records therefore tile time without overlap and without gap, when complete. The record carries no end instant; the interval length comes from each value's own declared support, not from the publication cadence, and the two must not be conflated — the cadence says when the next record is due, and would still say that if the values had a different support.

Positions on this axis are absolute UTC instants, so they are unambiguous on their own and are the correct join key and sort key. Civil time is a derived view: to bucket by local day, label by local hour, or produce a daily profile you must convert to Europe/London yourself, and the offset changes twice a year. That conversion is exactly where the variable settlement-day length shows up — a "day" of 46 or 50 periods is a local-time day, and resampling code that assumes 48 half-hours per day will be wrong twice a year and silently correct the rest of the time.

The record does not carry a settlement date. The period number alone therefore does not identify a settlement day and is not a key; the start instant is.

## 5. Ambiguities

- **The period-numbering statement is internally inconsistent.** Periods are said to be numbered from 1 at midnight UTC, yet the count per day is said to vary with the clock change. Fixed half-hours counted from a fixed UTC midnight would always give 48. One of the two statements is loose. I am **declining to decide** which; the operative instruction — that the period number does not map to a fixed clock time and must not be used for arithmetic — is consistent either way, and is what should be implemented.
- **What an absent value member means** — zero, not applicable, not yet available, or withheld — is **not determined**. This is the most consequential open point for anyone writing a loader.
- **Whether the generation categories are exhaustive.** There is an "other" bucket for fuel types not reported separately, but whether it makes the breakdown complete for all transmission-metered plant, and whether its composition is stable over time, is **not determined**. Treating "other" as a fixed category across years is a **guess**, and one I would not make.
- **Solar does not appear.** Whether it falls inside "other", or is outside the feed's population entirely, is **not determined**. Do not present a mix breakdown from this feed as covering all GB supply without settling this.
- **Sign range of the generation members.** Only the interconnectors are stated to be signed. Whether generation values can be negative (station load, metering artefacts) is **not determined**; the sample record is non-negative throughout, which establishes nothing about the general case.
- **The basis of the mean** — time-weighted over the whole half-hour versus an average of discrete samples — is not stated. I am **assuming** time-weighted, because that is what makes the multiply-by-half-an-hour energy conversion exact. If it is a sample mean over sparse samples, energy totals inherit a sampling error of unknown size. Marked as an assumption.
- **No revision, publication-time, or version member exists.** If a period is ever restated, two records for the same instant cannot be ordered or distinguished. Whether restatement happens is **not determined**; that the data model cannot express it is certain.
- **No data-quality, estimation or completeness flags.** Estimated and metered values, if both occur, are indistinguishable.
- **The member set is closed.** No unlisted member may appear, so a newly commissioned interconnector cannot enter this feed without a schema change. Whether that means such flows would be absent, folded into an existing member, or land in "other" is **not determined** — and any of those would distort a net-import series computed from historical code.
- **Nothing external is dereferenceable.** The schema's own identifier and its record-level observable-property reference point at placeholder hosts, so none of the above can be settled by following a link. They have to be settled with the publisher.
