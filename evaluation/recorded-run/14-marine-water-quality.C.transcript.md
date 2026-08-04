# 1. What this feed is

Each record is one in-water observation made by a fixed instrument package at a named
monitoring station, reporting the physical, chemical and optical state of a parcel of
seawater at a stated depth, together with a quality-control verdict and the time the
record was made available. The station identity, the basin it sits in, the instrument
that produced the reading, and the two timestamps are always present; **every measured
quantity is optional.** The station is a mooring — a fixed platform sampling repeatedly
at the same place — so the series is a time series at a point, not a survey track.

The single most consequential thing to understand before using this data: the record
carries *one* quality flag for the *whole* record, not one flag per measurement. A
record marked `pass` is not a statement that each of its eighteen numbers is good, and a
record marked `suspect` or `fail` does not tell you which sensor was the problem. Any
pipeline that filters on the flag is making an all-or-nothing decision about a
multi-sensor package in which sensors fail independently. That is the default failure
mode of this feed.

# 2. Analytics worth running

**Publication latency and feed health.** The gap between when water was observed and when
the record was published is directly computable, per station and over time. This is the
one analysis the data supports cleanly and unconditionally, because both timestamps are
mandatory and both refer to the same record. Widening latency, or latency that becomes
bimodal, is the earliest visible symptom of telemetry or QC-pipeline trouble — visible
before any measured value looks wrong.

**QC-regime auditing.** The flag distinguishes *not yet evaluated* from *passed*. Tracking
the share of records in each state, per station and per week, tells you whether a
station's data has actually been reviewed or merely arrived. Series that silently mix
reviewed and unreviewed records are not comparable to themselves over time, and this feed
lets you detect that. Do it before any trend work.

**Water-mass characterisation (temperature–salinity structure).** Temperature and salinity
are reported together for the same parcel, so classic T–S analysis is available: which
water masses the station sees, when riverine or oceanic influence dominates, and when the
column is stratified. This works because the two values share a record and therefore share
a time, a place and a depth.

**Stratification and depth structure — only if depth is populated.** Depth is optional. Where
several records from one station at one time carry different depths, you have a profile
and can compute gradients. Where depth is absent you have a number with no vertical
position, and in a stratified estuary that number is close to meaningless for anything but
existence checks.

**Oxygen dynamics and hypoxia exposure.** Dissolved oxygen is reported both as a
concentration and as a percent of saturation. Concentration is what organisms experience;
saturation tells you whether the water is being drawn down biologically or merely warmed.
Both being present in the same record lets you separate thermal from biological causes of
low oxygen, which a single one of them cannot do.

**Bloom detection and nutrient drawdown.** Chlorophyll and nitrate arrive in the same record
from the same water. Their inverse excursions — chlorophyll rising while nitrate falls —
are the signature of a productive event, and this feed supports that correlation directly
because there is no cross-record joining involved and therefore no time-alignment error.

**Sensor-fouling and drift surveillance.** The two dispersion values (chlorophyll and
turbidity) describe how variable the measurement was *within* a single record's sampling
burst. Rising within-burst dispersion, especially in turbidity, is a classic biofouling and
bubble-entrainment signal, and it appears before the central value becomes obviously wrong.
Because the instrument is identified by a vocabulary URI, you can partition this analysis
by instrument type and separate genuine environmental patchiness from a behaviour peculiar
to one sensor model.

**Diel and seasonal cycling.** Oxygen and chlorophyll cycle on a day/night rhythm and a
seasonal one. The feed supports this, but see the time section: the binning must be done in
local solar time, and the files do not give you the coordinates needed to compute it
rigorously.

**What is *not* supported.** There are no coordinates anywhere in the record. You cannot map
stations, compute inter-station distances, interpolate spatially, compute a true solar
angle, or detect that a mooring was relocated. Basin is a free-text label, not a geometry
and not a controlled value, so grouping by it is exposed to spelling and renaming drift.
Carbonate-system work is also out of reach: pH alone does not constrain it, and no second
carbonate parameter is present.

# 3. Combination rules

**Everything measured here is intensive** — a property of a parcel of water, not an amount of
anything. **No quantity in this feed may be summed across records.** Adding two salinities or
two temperatures produces a number with no referent. The only summable thing is a count of
records. Say this out loud to anyone building aggregations, because SQL will happily do it.

**A precondition for averaging anything.** An average is only defined over a stated
population. Here that means: same station, same depth, same instrument type, same QC
status, and no duplicated observations. The files do not state that station identity plus
observation time is unique, so a restated or corrected record may coexist with the record
it supersedes, distinguishable only by publication time. Deduplicate to the latest
publication time per station-and-observation-time *before* aggregating, or accept
double-counting.

**Temperature (°C).** Differences and averages are valid within a coherent population.
Ratios are not — Celsius has an arbitrary zero, so one reading is never "twice as warm" as
another. Do not sum.

**pH.** Differences and averages are **not** valid in the ordinary way. pH is a logarithm of
hydrogen-ion activity; the arithmetic mean of two pH values is not the pH of the mixed
water, and a difference of 0.3 is a factor of two in acidity, not a small increment. If you
must average, convert to activity, average that, convert back — and even then the result
is only defensible over water of similar temperature and salinity. Never sum. Additionally,
the scale convention (total, free, or NBS) is not stated, and these differ by roughly a
tenth of a unit; **pH values from records produced under different conventions must not be
differenced at all**, and the files give you no way to tell them apart.

**Conductivity, specific conductivity, and salinity — treat as one measurement, not three.**
Salinity is derived from conductivity together with temperature and pressure; specific
conductivity is the same conductivity normalised to a reference temperature. They are three
presentations of one physical determination. **Do not correlate or regress them against each
other** — you will recover the conversion formula and mistake it for a finding. For
comparing ionic content across records taken at different temperatures, use the specific
(normalised) value; raw conductivity compared across records confounds temperature with
salt content. Salinity may be differenced and averaged over a coherent population; never
summed. The reference temperature behind "specific" is not stated in the files.

**Dissolved oxygen, concentration vs. saturation — likewise not independent.** Saturation
percent is the concentration expressed against a solubility that is itself a function of
temperature, salinity and pressure. They carry the same measurement. Concentration may be
differenced and averaged. Saturation percent is a normalised ratio: averaging it across
records at different temperatures and salinities produces a figure that corresponds to no
water sample, and summing it is meaningless. Cross-producer comparison of saturation is
further compromised because the solubility formulation used is not stated and the common
alternatives disagree by a small but non-negligible amount.

**Depth and pressure.** These are also very likely two expressions of one determination
rather than two independent facts; do not treat them as mutually corroborating. Neither the
vertical datum for depth (below the instantaneous surface? below a tidal datum?) nor whether
pressure is absolute or gauge-referenced is established. Depths from different records
should be differenced only within a single station.

**Chlorophyll and turbidity central values.** Differences and averages within a coherent
population are fine; sums are not. Turbidity in nephelometric units is defined by the
measurement method and optical geometry, so **turbidity from different instrument models is
not strictly comparable** — partition by the instrument URI before comparing. The same
caution applies with less force to chlorophyll.

**The two dispersion values are the sharpest trap here.** A standard deviation must never be
summed or averaged directly. Pooling dispersion requires combining *variances* weighted by
the number of subsamples behind each one, and **the subsample count is not reported**. You
therefore cannot correctly pool these across records at all. They are usable as a
per-record diagnostic and comparable between records only under the assumption that every
record's sampling burst has the same length and rate — which the files do not state. Report
them; do not aggregate them.

**Nitrate.** May be differenced and averaged within a coherent population; not summed. But
see the ambiguities: the unit is incomplete.

**Absent values.** A missing measurement is not zero and not a low value. Because every
measured member is optional and the quality flag is record-level, an absent value cannot be
distinguished from a measurement that was taken and withheld. Averages computed over
records where a member is sometimes absent are averages over a shifting population; carry
the count alongside every aggregate.

# 4. Time

**The observation time is the time axis of the thing described** — the moment the water was
in that state. The publication time is an axis of the *record*, describing when the
information became available; it is the right axis for latency, backfill and revision
analysis and the wrong axis for anything environmental. Ordering a series by publication
time will reorder the ocean.

Positions on the observation axis relate to civil time through the UTC offset carried in
the value itself. The example is expressed at zero offset, so it denotes an unambiguous
instant. Whether every record in the feed carries an offset is not established by these two
files; a value written without one would not be placeable on a global axis at all, and a
consumer should reject rather than assume such a value.

Two qualifications matter more than they appear to.

First, **the observation time is presented as an instant, but the record almost certainly is
not one.** The presence of within-record dispersion statistics means each record summarises a
burst of subsamples spanning some interval. The length of that interval is not given, and
neither is whether the stated time marks the start, the centre, or the end of it. Treat the
timestamp as an instant for coarse work; do not use it for anything at finer resolution than
the (unknown) burst length, and do not assume two records from different stations bearing
the same timestamp sampled the same window.

Second, **local civil time is not derivable from these files.** There are no coordinates and no
timezone member. Diel analysis — the day/night cycle in oxygen and chlorophyll, which is one
of the strongest signals in data like this — must be binned in local solar time, or the
cycle will smear and, across a season, drift. Binning in UTC is wrong here, and binning by a
fixed offset is wrong too wherever the location observes daylight saving, because the offset
changes mid-series.

Sampling cadence is not established. One record does not tell you whether the feed is
regular, and gap analysis, duty-cycle weighting, and any duration-based exposure metric
(e.g. hours below an oxygen threshold) all depend on knowing it. Until cadence is
established from the data itself, exposure must be reported as a count of records, not as a
duration.

# 5. Ambiguities

**Whether the quality flag applies per record or per measurement.** Declining to decide. The
evidence points to per-record, and that is what I have assumed throughout, but nothing here
states it, and the consequences differ enormously.

**What the "missing" flag state means.** Declining to decide. It may mark a placeholder for an
expected observation that never arrived, or a record whose values were all lost. Either way,
do not treat it as a low or zero reading.

**Whether "not evaluated" is safe to use.** Declining to decide. It is clearly distinct from
"pass", and folding the two together will bias any series; whether unevaluated data is
usable at all is a policy question these files do not answer.

**The denominator for nitrate.** The unit names an amount of substance with no volume. My
guess — **and it is a guess** — is micromoles per litre, which is the near-universal
convention for dissolved nutrients in seawater and is consistent in magnitude with the
example value. It could be micromoles per kilogram, which differs by roughly the density of
seawater, a few percent. This matters for absolute comparison against other datasets and not
much for internal trend work.

**The reference temperature behind "specific" conductivity.** Guess: 25 °C, the standard
convention. Not stated.

**The pH scale convention.** Declining to guess. Total, free and NBS scales are all in use for
seawater and differ by an amount comparable to a decade of acidification signal.

**The oxygen-saturation formulation.** Declining to guess. Several are in common use and they
disagree slightly.

**Whether the reported depth is a measurement or a conversion of pressure.** Guess: converted
from pressure, since the two are numerically consistent in the example. If so they are not
independent evidence.

**The vertical datum for depth, and whether pressure is absolute or gauge.** Declining to
decide, though the example's pressure value at the stated depth is consistent with a
gauge/in-water reading rather than an absolute one — **a guess.**

**The averaging window length behind each record, and where the timestamp sits within it.**
Not determined. This is the gap I would close first, because it bounds the temporal
resolution of everything else.

**The number of subsamples behind each dispersion value.** Not determined, and its absence
makes correct pooling of those values impossible rather than merely awkward.

**Whether station identity plus observation time is unique.** Not determined. There is no
revision counter or record version, so a corrected restatement would be detectable only as a
duplicate with a later publication time — and only if you look for it.

**Whether the station identifier is stable and whether the station has ever moved.** Not
determined. Without coordinates, a relocated mooring is invisible and would appear as a step
change in the environment.

**Whether the instrument reference identifies a model or an individual unit.** Guess: a model
or device *type*, since it points into a controlled vocabulary rather than carrying a serial
number. If so, you can partition by instrument type but cannot attribute drift to a specific
deployed unit or align it with calibration and servicing events.

**Units generally.** Units appear only inside member names; nothing in the schema declares them
in a form a tool could check, and no numeric bounds are enforced. The conductivity values are
internally consistent with siemens per metre as named, but a producer emitting the
also-common millisiemens per centimetre would be off by a factor of ten and **nothing here
would catch it.** Validate ranges yourself.

**Geographic location, and therefore basin membership.** Not determined. Basin is an
uncontrolled label; treat it as a hint, not a key.

**Whether chlorophyll is a direct measurement or a fluorescence proxy.** Declining to decide.
The distinction affects how much you trust absolute values versus relative change, and the
files do not address it.
