# 1. What this feed is

Each record is one dispatch from one fixed observing platform — a moored buoy, a
C-MAN station, or a partner platform — reporting the state of the sea and air
around it. `station_id` is the subject of the observation (`featureOfInterest`),
and every result in the record is about the surroundings of that platform and
nothing else. The platform's position is carried per record and is bound to
EPSG:4326 with the axes in the order that definition fixes: latitude first, then
longitude. Anything downstream that expects GeoJSON or CRS84 ordering must swap
them; nothing in the numbers themselves reveals the error.

The important thing about the record is not what it contains but that it is not a
snapshot. It reports one timestamp and three different kinds of temporal support
under it. Six members are instantaneous. Four wave members characterise the
twenty minutes ending at the timestamp. Pressure tendency characterises the three
hours ending at it. Three wind members characterise an interval whose length the
record does not carry at all. So a single record spans at least three hours of
phenomenon time, and treating the timestamp as the time of the whole record is
the first mistake available.

Only `station_id`, the two coordinates, and `timestamp` are required. Every
measurement is optional, and its absence is undeclared — not zero, not missing at
random. The instance omits visibility and tide, and the schema's own prose
explains why: those sensors are largely confined to particular platform types.
Missingness in this feed is therefore structured by platform capability, which
biases anything pooled naively across stations.

Two things the record does not carry are worth naming up front, because their
absence is easy to read as reassurance. There is no procedure or instrument
identifier anywhere, so the measuring arrangement behind any value is undeclared
and may not be inferred. There is no quality flag and no record status, so every
value arrives unqualified; absence of a quality declaration does not mean the
value passed anything.

Finally, the observed-property references on the individual results are QUDT
quantity kinds — Angle, Speed, Length, Period, Pressure, Temperature. These
classify; they do not identify a phenomenon. Wave height, visibility, and tide
all carry `Length`. Wind speed and gust both carry `Speed`. The two wave periods
both carry `Period`. Air and water temperature both carry `Temperature`. Any join
or grouping keyed on the declared observed property will conflate quantities that
must never be combined. Sameness of phenomenon in this feed rests on the member
position and its prose, not on the annotation.

# 2. Analytics

**Per-station time series of the instantaneous quantities.** Pressure, air
temperature, water temperature, and dewpoint all apply at the timestamp, at a
declared five-minute cadence, for a fixed subject. This is the one clean,
regularly sampled series the feed offers, and it supports trend, diurnal cycle,
and event detection directly.

**Air–sea temperature difference.** Both temperatures are instantaneous, share a
unit, share a timestamp, and share a feature, so their difference is well formed
within a single record without any alignment work. (No sensor height or depth is
carried, so the difference is between two unstated levels — see §5.)

**Dewpoint depression.** `air_temperature − dewpoint` is well formed for the same
reasons. Note that dewpoint was computed from air temperature and a humidity
channel the record does not carry, so the two are not independent measurements
and a correlation between them is partly definitional.

**Frontal and storm-passage detection from pressure tendency.** The three-hour
signed pressure change is supplied ready-made, with its sign convention stated
(negative falling, positive rising) and its window declared. It is directly
usable and must not be re-derived or accumulated (§3).

**Sea-state characterisation within a record.** The four wave members —
significant height, dominant period, average period, and mean direction — share
exactly the same twenty-minute window anchored at exactly the same instant. That
shared support is declared, not assumed, which makes derived sea-state indices
combining them internally consistent within one record. This is the strongest
combination licence the schema grants.

**Gust factor.** The schema states that the gust is the peak within the same
averaging window that produced the mean wind speed. Their ratio is therefore well
defined inside a record even though the window's length is unknown. It is
comparable across records only where the window length is the same, which the
record does not establish (§5).

**Spatial fields of the instantaneous quantities.** Position is machine-resolvable
against a named CRS, so gridding or interpolating sea-level pressure and the two
temperatures across stations at a common timestamp is supported. Pressure in
particular is reduced to sea level, which is what makes station-to-station
comparison meaningful at all. Wind statistics, tide, and visibility do not support
this (§3).

**Wave climate at a station.** Wave height and the two periods share a fixed
twenty-minute support that does not vary by platform type, so unlike the wind
members they are comparable across stations on support grounds. Distributions,
exceedance statistics, and inter-station comparison are supported subject to the
undeclared procedure.

**Wind–wave relationship, with a caveat.** Both are present, but they do not share
support: the wave window is twenty minutes and fixed, the wind window is short and
unknown. Any correlation is between quantities integrated over different and
partly non-overlapping stretches of time, and that mismatch must be carried
through the analysis rather than assumed away.

**Availability and gap analysis.** The declared five-minute cadence makes an
absent slot detectable as a gap. That is a legitimate consumer decision about
windowing and staleness. It does not license filling the gap, and it does not
assert that a record exists for every slot.

# 3. Combination rules

The gates that apply throughout: two values are like quantities only if they are
the same phenomenon, in a compatible unit, produced by the same summary function
where one applies, and over compatible temporal support. Different statistics of
one phenomenon are not like quantities. The procedure is undeclared for every
value here, so every cross-station combination below carries an undeclared
procedure difference that the data cannot expose.

**`station_id`** — not a quantity. Equality of `station_id` is the only grouping
key the schema licenses. Do not group by coordinate proximity.

**`latitude` / `longitude`** — a coordinate pair in EPSG:4326, latitude first.
Comparable only in that order. Degrees are angles, not distances: differencing
them does not yield a separation, which requires a geodetic computation on the
named CRS. Averaging positions across records of one station describes where the
platform sat; averaging across stations produces a centroid that is the location
of nothing. These members carry no `phenomenonTimeRelation`, so whether the
position applies at the timestamp is undeclared, and movement between consecutive
records must not be read as measured drift.

**`timestamp`** — comparable and orderable directly; differences are elapsed civil
time. Not summable or averageable as a quantity.

**`wind_direction`** — a circular quantity in degrees. Comparable within a station.
Differences must be taken modulo a full turn; a naive subtraction is wrong across
the north crossing. Never sum. Never average arithmetically — the arithmetic mean
of directions straddling north is meaningless, and even a proper circular mean
would be a mean of means over windows of unknown length. **Not combinable across
stations of different type**, because the averaging window differs by platform
type and the record does not say which it is. The reference direction is true
north by prose only; no frame is bound.

**`wind_speed`** — a mean over an interval whose length the schema deliberately
leaves indeterminate. Comparable and differenceable within one station.
**Must not be compared or pooled across stations without first establishing, from
station metadata outside this feed, that the two averaging windows are the same
length.** A two-minute mean and an eight-minute mean of the same wind are not the
same quantity. Never sum — a mean is not additive. Averaging consecutive records
is not a mean wind over the covering period: at a five-minute cadence an
eight-minute window overlaps its predecessor, so the values are not independent,
and a two-minute window leaves three minutes of every five unobserved.

**`gust`** — a maximum over that same unknown window. The maximum across a set of
records is a valid maximum over the union of their windows, provided you accept
that the union may have gaps. The mean of a set of gusts is a statistic of maxima
and is not a property of the wind; it may be computed but must be labelled as
what it is. Never sum. Gust and `wind_speed` are different statistics and are not
comparable as like quantities; their difference or ratio within one record is
nonetheless well formed, because the schema states they share a window and a unit.

**`wave_height`** — a mean of the highest third of the waves over twenty minutes.
Comparable, differenceable, and pooled across stations, since the support is fixed
and platform-independent. **Never sum**: the relation is `interval`, not
`accumulation`, and nothing here is additive. Averaging consecutive records
double-counts heavily — at a five-minute cadence, adjacent twenty-minute windows
share fifteen minutes — so an independent series requires subsampling to at least
twenty-minute spacing. Critically, **do not treat `wave_height` and
`average_wave_period` as comparable because they share derivation, statistic, and
support**: they are means over different populations (the highest third of wave
heights; all wave periods) and of different quantities. That distinction lives in
prose; the annotations alone do not carry it.

**`dominant_wave_period`** — read off a computed spectrum, not summarised from
readings. Comparable and differenceable across records and stations, sharing the
twenty-minute support. Never sum. It may be averaged arithmetically, but the mean
of a set of spectral peaks is not the peak of any mean spectrum, and the same
overlap caveat applies. Not a like quantity with `average_wave_period` despite the
shared unit, shared quantity kind, and shared window.

**`average_wave_period`** — mean of all wave periods over the same twenty minutes.
Same overlap caveat, same prohibition on summing.

**`mean_wave_direction`** — circular, and calculated from the spectrum at the
dominant frequency band only. All the circular rules for `wind_direction` apply.
Never sum, never average arithmetically. It describes the energy at the dominant
period, so pairing it with `average_wave_period`, which covers all waves, mixes
populations.

**`pressure`** — instantaneous, and already reduced to sea level, which is
precisely what makes it comparable and differenceable across stations and what
supports horizontal gradient analysis. Averaging over time within a station is
sound. Never sum. The reduction depends on a station elevation the record does not
carry, so a station with a wrong elevation carries a bias this feed cannot reveal,
and station pressure cannot be recovered.

**`air_temperature` / `water_temperature`** — instantaneous, measured, same unit.
Compare, difference, and average over time within a station freely. Cross-station
comparison is supported in principle but no measurement height or depth is
declared for either. Never sum. Do not average the two together; they are
different phenomena sharing a quantity kind.

**`dewpoint`** — instantaneous, calculated. Compare, difference, average over time.
Never sum. The formula is not machine-declared, so the humidity it came from may
not be reconstructed exactly.

**`pressure_tendency`** — already a difference over the three hours ending at the
timestamp. Comparable and differenceable across stations (fixed support, common
unit). **Never difference it again.** It may be summed only over a strictly
non-overlapping, contiguous, gap-free chain of three-hour steps, in which case the
sum telescopes to the net change; at a five-minute cadence that means taking every
thirty-sixth record. Summing consecutive records inflates the true change by
roughly a factor of thirty-six. Averaging consecutive records averages
overwhelmingly overlapping windows and yields a smoothed artefact, not a tendency.
It is not the derivative of the `pressure` member in this feed: that one is an
instantaneous value and the tendency was formed by the producer from its own pair
of readings, so cross-checking the two is a legitimate diagnostic but exact
agreement is not implied.

**`visibility`** — instantaneous, in nautical miles, from a sensor the schema says
ranges only to 1.6 nmi. The values are therefore right-censored at the top.
Treat 1.6 as a bound, not a measurement; means and variances computed over
censored values are biased. Comparable across stations only where the sensors
share that range, which the record does not state. Never sum.

**`tide`** — instantaneous, in feet, relative to Mean Lower Low Water. **No
vertical reference system is bound to this member.** A height means nothing
without a declared zero, and the schema names the datum in prose only, so what the
zero is — and whether two stations share one — is not established. **Compare,
difference, and average `tide` only within one station.** Do not compare,
difference, or average it across stations, and never sum it. (General knowledge,
not established by these files: MLLW is conventionally realised per station from
local tidal observations, which would make cross-station comparison actively wrong
rather than merely unsupported.)

**Across quantity kinds** — `wave_height`, `visibility`, and `tide` all declare
QUDT `Length`, in metres, nautical miles, and feet respectively, and describe three
unrelated phenomena. A shared quantity kind is a classification and never a licence
to combine. The same warning applies to the two `Speed` members, the two `Period`
members, and the two `Temperature` members.

# 4. Time

`timestamp` establishes the time axis. It carries the phenomenon-time role, so it
places the observed conditions rather than the record's publication or handling.

It is a plain Core `datetime` with no temporal reference system declared, which
means Core semantics are fully intended; the description states UTC and the
instance carries a `Z` offset. Positions on this axis therefore map onto civil UTC
directly — no epoch, no conversion, no local time, no reference-system lookup. The
value is built from year, month, day, hour, and minute fields, so the axis is
resolved to the minute and carries no sub-minute placement.

The axis is expected to advance in five-minute steps. That expectation describes
the producer, not the data: a record whose spacing departs from it is late, not
invalid; a missing slot is a detectable gap and nothing more; and the cadence
neither guarantees that a next record exists nor bounds any phenomenon time.

How results sit on the axis differs by member, and this is the part that governs
correct use. For the six instantaneous members the timestamp is the instant the
value applies. For every interval member the timestamp is the *closing* boundary:
the record carries no separate period boundaries, so `timestamp` anchors them all,
and each interval runs backwards from it, half-open. The wave quartet covers
[t − 20 min, t). Pressure tendency covers [t − 3 h, t). The three wind members
cover [t − L, t) for a length L that this feed does not carry and that must be
obtained from station metadata. Those three declare an interval relation with an
indeterminate extent — which is a deliberate, well-formed statement, not an
omission, and it must not be read as meaning the values are instantaneous.

Two consequences follow. First, the periods overlap one another inside a single
record and are not the same period, so a consumer that attributes all of a
record's content to its timestamp attributes three hours of pressure change to an
instant. Second, joining this feed to another on timestamp equality aligns the
instantaneous members and silently misaligns everything else unless the other
feed's support matches.

There is no result time, no ingestion time, and no effective time. The delay
between an observation applying and the record becoming available is therefore not
determinable from the data, and neither is any period for which a record is
intended to be acted on.

# 5. Ambiguities

**The wind averaging window length.** *Declining to decide.* The schema states
explicitly that the length follows the station type, that the record does not
carry the station type, and that the extent must be obtained from station
metadata. This is the single most consequential open item in the feed, and it is
open by design rather than by oversight.

**Which platform type any given record came from.** *Declining to decide.* Nothing
in the record declares it. One could try to read it off the shape of
`station_id` — the description offers a numeric example for a deep-ocean buoy and
an alphanumeric one for a C-MAN station — but the schema states no rule, two
examples are not a specification, and inferring semantics from the form of sample
values is exactly what should not be done here. If anyone does it anyway, it is a
guess and must be labelled one.

**Whether a station possesses a wave, visibility, or tide sensor.** *Declining to
decide.* All these members are optional and absence is undeclared. No capability
annotation exists, and presence or absence across a run of records is evidence
about the feed, not a declaration.

**The instrument or procedure behind any value.** *Declining to decide.* No
procedure is identified anywhere. This is comparability-critical and may not be
inferred from station identity, position, or the values themselves.

**The quality or verification state of any value.** *Declining to decide.* There is
no quality qualifier and no record status. Absence of these does not mean the data
are good, screened, or final, and nothing indicates whether records are ever
revised, superseded, or duplicated.

**Sensor heights and depths.** *Declining to decide.* No height is carried for the
anemometer or the air temperature sensor and no depth for the water temperature
sensor. *Assumption, from general knowledge rather than these files:* wind speed
varies substantially with measurement height, so cross-station wind comparison
carries an unquantified bias even when the averaging windows match.

**The tide datum and its sign convention.** *Declining to decide* on the datum: no
vertical reference system is bound, the realisation of MLLW is not identified, and
whether two stations share a zero is not established. *Guessing* on the sign: the
phrase "above or below" with "above" stated first suggests positive is up, but no
annotation establishes an axis direction, and this is a guess.

**The direction reference and encoding for the two direction members.** *Declining
to decide.* "Degrees true" appears in prose only; no reference frame is bound. The
admissible range, the treatment of the 0/360 boundary, and how a calm or an absent
direction is encoded are all undetermined.

**The circular-averaging convention used to produce `wind_direction`, and the
spectral method behind `wave_height`, `dominant_wave_period`, and
`mean_wave_direction`.** *Declining to decide.* The schema names the summary
function and the fact of a spectral computation but no method, and a method must
not be read out of a description. None of these values may be recomputed or
verified from the record.

**Whether the gust peak interval is five seconds or eight.** *Declining to decide.*
The description offers both and the record does not distinguish them.

**How missing measurements are encoded on the wire.** *Declining to decide.* The
instance omits two members, which is consistent with omission being the mechanism,
but one example does not establish it, and nothing rules out sentinel values
appearing in some deliveries.

**Whether the three-hour tendency window was actually complete.** *Declining to
decide.* The declared support states the extent of the period, not that readings
existed at both ends of it, and no quality annotation would reveal a partial one.

**The record-level observed property and every QUDT reference.** *Declining to
decide.* The catalogue behind `marine-surface-conditions` is not a real one and
none of these references is required to resolve. Unresolved is indeterminate, not
incorrect — but no equivalence, and no permission to combine, may be read from
them. In particular, the record-level property is overridden on every result
member, so it governs nothing in practice.

**Whether one record per station per five-minute slot is guaranteed.** *Declining
to decide.* The declared cadence is an expectation about a producer and asserts
neither completeness nor ordering nor the existence of a successor.
