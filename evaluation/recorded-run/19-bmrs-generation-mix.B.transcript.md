# 1. What this feed is

Each record is a half-hourly summary of what was producing electricity on the GB
transmission system, and what was flowing over the cables that connect it to
neighbouring systems, during one settlement period. Every quantity in a record
is a **mean power in megawatts over the same half hour** — not an instantaneous
reading, not an energy total. The half hour is fixed by one UTC instant carried
in the record and runs forward from it, half-open.

Two structural facts dominate everything an analyst does with it. First, the
plant members report **gross output of the metered fleet**, while the
interconnector members report **signed net flow on a specific cable**, positive
into GB. These are different kinds of number wearing the same unit. Second, the
feed is **not a balance**: pumped-storage pumping load is absent (it is metered
as demand elsewhere), wind connected below transmission is absent, and the
record's own text says the wind figure therefore understates GB wind. Nothing in
the two files establishes that the listed categories exhaust GB generation.

The record names a system-level observable property, but it carries no member
identifying the feature observed and no member identifying the measuring or
estimating procedure. Both are therefore undeclared, and omission never implies
that they are constant or acceptable.

# 2. Analytics

**Fuel-mix composition and its shape over time.** Every value in a record covers
the *identical* half-open interval — same length, same anchor, same anchoring
instant — so cross-member arithmetic within a record is exact rather than
approximate. Shares, ratios, and stacked mixes are well-founded provided the
denominator is chosen deliberately (see §3).

**Ramp rates and volatility.** Consecutive records carry the same statistic over
equal-length adjacent windows, so differencing one member across records yields
a legitimate change-per-half-hour. This is the natural way to characterise wind
variability, gas following, and nuclear stability.

**Import dependence and per-cable behaviour.** Each interconnector is reported
separately and signed, so flow direction, per-cable duty cycle, simultaneous
import and export, and correlation between cables are all directly supported.
The example record shows five cables importing and two exporting at the same
instant — which is exactly why an unsigned aggregate would be wrong.

**Energy volumes (MWh).** A mean power over a known half hour converts to energy
by multiplying by 0.5 h. Structurally supported, but it rests on an assumption
the annotations decline to make (see §5).

**Displacement and substitution analysis.** Because gas, coal, biomass, nuclear
and wind are separated, and interconnectors are separated from them, questions of
the form "what moves when wind moves" are answerable within a record set.

**Coverage and clock-change auditing.** The declared half-hourly cadence is an
*expectation about the publisher*, not a guarantee and not a constraint on the
data; a missing half hour is late, not malformed. Any downstream aggregate must
therefore be preceded by a coverage check built from the time instants
themselves, including the short and long days.

**Peaks — with a caveat.** Maxima and minima across records are comparable, but
the maximum of a half-hour mean is not the instantaneous peak, and the
annotations explicitly do not permit recovering the underlying sample set.

**What the feed does not support on its own:** emissions or carbon intensity
(requires external per-fuel factors), demand or system balance (the load side is
absent), and joins to other settlement-keyed data (see §5, the missing
settlement date).

# 3. Combination rules

**Settlement period number.** It is an identifier, not a measure. It may be
tested for equality and used as a key. It must not be differenced, summed, or
averaged, and period *n* on one day is not the same clock position as period *n*
on another, because the number of periods in a day is not constant. Treating it
as an offset is wrong at exactly the two days a year when it matters most.

**Start instant.** Instants may be ordered and compared, and two of them may be
differenced to give a duration. They must not be summed. They are the only sound
basis for placing a record on a time axis.

**The ten plant members, among themselves, within one record.** Freely summable
and averageable. All carry the same unit, the same summary function, and the same
support interval anchored on the same position, and the mean of a sum over
identical windows is the sum of the means. This is the one aggregation the files
fully licence.

**The ten plant members, across records.** A given member may be compared and
differenced between records without qualification. Averaging across records is
valid as an unweighted mean only because every record's window is the same
length; it is a mean *of the periods present*, and the declared cadence does not
establish that every period is present. Summing a member across records produces
nothing meaningful in MW — convert to energy first, then sum.

**Pumped storage.** Summable with the other plant members as output, but it is
not a net position: the pumping load is not represented here as a negative value.
Any attempt to close an energy balance, compute net storage contribution, or
infer round-trip behaviour from this feed will be wrong by the whole of the
pumping load.

**Non-pumped hydro and pumped storage.** Disjoint, so summing them double-counts
nothing. But the sum conflates a primary source with a store, which is precisely
the distinction the two members exist to preserve.

**CCGT and OCGT.** Arithmetically summable as gas-fired output. They must not be
treated as one dispatchable fleet: they are operationally unrelated, one being
bulk energy plant and the other short-duration reserve, so a combined series
answers no dispatch question that either series answers separately.

**Wind.** Comparable with itself over time and usable for shape and variability.
It must not be used as a level for GB wind generation, nor as the numerator of a
GB wind-share figure, because generation below transmission is excluded.

**The seven interconnector members, among themselves.** Summable to a net import
position, and the two French cables may be summed to a total French flow, since
they share unit and sign convention. Comparing capacities or utilisation between
cables requires ratings the files do not carry.

**Interconnectors with plant members.** Do **not** sum them without an explicit
decision about exports. The values are signed: a negative one is power leaving
GB, and adding it to gross production yields neither total generation nor total
supply. If a "total" is wanted, state whether exports are netted, clipped at
zero, or excluded — the files do not decide it, and the three choices give three
different numbers. In the example record, gross plant output is 22 871 MW and net
interconnector flow is +5 588 MW, but that +5 588 is itself the residue of
+6 184 in and −596 out.

**Across this feed and any other.** Every value member declares the same generic
observable property — a quantity kind of *power*. Equal quantity-kind
classification does not establish that two quantities are the same observable
property, and here it demonstrably does not: gas-turbine output and a Norwegian
cable flow carry the identical declaration. A pipeline that groups or joins on
observed property will silently pool them. The distinguishing facts live in the
per-member prose, not in a resolvable identifier. By the same argument, a value
here must not be combined with a megawatt value from another feed on the strength
of matching unit and quantity kind alone.

# 4. Time

The time axis is established by the **start instant**, which is declared as the
opening boundary of the phenomenon-time period. It is a plain UTC date-time with
standard semantics — no alternative temporal reference regime is declared — so a
position on this axis *is* a civil-time instant and needs no conversion. The
example carries an explicit `Z`.

The record carries no closing boundary, and none is needed: each value member
states its own period length of thirty minutes, anchored at the start. The
interval a value characterises is therefore `[start, start + 30 min)`, half-open,
so the instant that closes one period opens the next and no half hour is counted
twice.

The declared half-hourly cadence is a separate statement from that length. It
describes what the publisher is expected to do next; it does not bound the period
any value applies to, does not assert that a successor record exists, does not
assert ordered arrival, and does not make an off-cadence stream invalid. That the
two happen to be numerically equal here is a fact about this feed, not an
identity between the two ideas.

The settlement period number does **not** establish the time axis. It is an
identifier that does not map to a fixed clock time across the year.

# 5. Ambiguities

**The settlement-day rule contradicts itself.** The record states both that
periods are numbered from 1 at midnight UTC *and* that a day has 46 or 50 periods
on clock-change days. Both cannot hold: a day bounded at midnight UTC always
contains 48 half hours. **I decline to decide which is correct.** The consequence
is concrete: you cannot reconstruct the start instant from a date and a period
number, or vice versa, using these two files. Use the start instant and treat the
period number as an opaque key.

**No settlement date is carried.** Settlement data is conventionally keyed by
date *and* period; only the period is here. Deriving the date from the start
instant requires the day-boundary rule that is contradictory above, so joins to
period-keyed data are not safely constructible from these files. **Declining to
resolve.**

**What the mean averages.** The annotation names the function and deliberately
states nothing about weighting, sample count, window alignment, or treatment of
missing data, and forbids recomputation. Multiplying by half an hour to get MWh
implicitly assumes a time-weighted mean over the full, gap-free window. **That is
an assumption, and I mark it as one.** It is the assumption most analyses of this
feed will make and the one most likely to be silently wrong during partial
outages.

**Absent members.** Only the period number and the start instant are required;
every quantity is optional. Whether an absent member means zero, unknown, or not
applicable is **not determined**, and omission carries no implication of an
acceptable or defaulted value. The example distinguishes an explicit `0.0` from
absence, which is suggestive but not decisive.

**Provisional versus final.** There is no publication time, no status, and no
quality qualifier. Nothing lets a consumer tell a first publication from a
restatement, or detect that a value was later revised. **Not determined.** I am
not guessing whether revision occurs.

**Procedure.** No observing procedure is identified, so it is not established
that the same metering or estimation method produced values in two different
records. Comparability across records is therefore assumed rather than
demonstrated. **Marked as an assumption**; I have no basis in the files to doubt
it, and none to assert it.

**Feature of interest.** No member identifies the system observed; only the
record's prose names it. That every record concerns the same system is a
**guess** — a well-founded one, but a guess, and it is not machine-checkable.

**Sign range of plant members.** The interconnector members are stated to be
signed; the plant members carry no lower bound and no statement that they are
non-negative. Whether a negative plant value can occur is **not determined**.

**Exhaustiveness.** Wind is stated to be incomplete and the residual category is
stated to cover only metered plant whose fuel is not separately reported. The
files do not say that the listed categories cover all GB generation, and the
record shape is closed, so a new cable or fuel category cannot appear without a
schema change. Any figure presented as a national total is **not supported**.

**The record-level observable property.** Its identifier points at a catalogue
that cannot be resolved from here. That is an indeterminate binding, not an
incorrect one, and it must not be repaired from member names, descriptions, or
the sample. **Declining to substitute a meaning for it.**
