# 1. What this feed is

Each record is one surface weather observation issued by one aerodrome reporting
station, identified by its ICAO code. The thing being observed is the station
site — not a grid cell, not an airspace volume — so every record is a point
observation anchored to a fixed piece of ground whose horizontal position and
mean-sea-level elevation travel with the record.

The payload mixes three different kinds of value that happen to sit side by side:
directly sensed atmospheric quantities (temperature, dewpoint, present weather,
cloud layers, visibility), wind statistics computed over a short window rather
than sampled at an instant, and quantities that are not observations at all but
reductions and classifications computed from other observations (altimeter
setting, sea-level pressure, flight category). It also carries the original
coded text of the report, which is a re-encoding of most of the decoded members
rather than an independent source of information.

The nominal rhythm is one routine report per station per hour, issued close to
the end of the hour, with off-cycle special reports interleaved when conditions
change enough to warrant one.

# 2. Analytics

**Per-station time series and climatology.** The observation time is explicitly
the time the conditions obtained, and a nominal hourly cadence is declared, so
temperature, dewpoint and pressure form a usable series per station. This is the
one family of analyses the data supports with no external inputs.

**Dewpoint depression and moisture regime.** Temperature and dewpoint are the
same unit, the same derivation, and both apply at the same instant, so their
difference is well defined within a record. That difference is the natural
driver for fog and low-ceiling work.

**Gust structure.** The gust value is a maximum over the same ten-minute window
that produced the sustained wind mean, which is exactly the condition needed for
a gust factor to mean anything. Ratios and differences between the two are
sound within a record.

**Wind roses and directional exposure.** Direction and speed share a support
window and an anchor, so they pair into a vector per record. Crosswind analysis
against specific runways is *not* supported by these files alone — runway
headings appear nowhere.

**Flight-category availability.** The category is a calculated classification, so
counting how often a station sits in each class, by hour or season, is a
legitimate and cheap operational summary.

**Reporting latency and observing-programme behaviour.** The record carries both
the time the conditions obtained and the time the encoded result was issued.
Differencing them measures the reporting pipeline. Separately, the routine/special
flag describes the observing programme rather than the atmosphere, so its rate is
a measure of how often conditions were changing — and a warning that the series
is not evenly spaced.

**Spatial fields across stations.** Positions are in a stated geographic CRS and
elevations in a stated vertical CRS, so multi-station interpolation and gradient
work is possible — but only for sea-level pressure among the pressure members
(see below).

Two analyses that look available and are not: anything requiring local civil
time, and anything requiring the quality-control flag's meaning.

# 3. Combination rules

**Temperature, dewpoint.** Same unit, same instant, measured. Differences within
a record (dewpoint depression) and across records or stations are valid.
Averages are defined. Sums are not meaningful — these are interval-scale
quantities, and neither is a ratio of two Celsius values. Averaging a run of
records is a sample mean of hourly snapshots, not a time-weighted mean of the
period, and it is biased whenever special reports thicken the sampling during
changing weather.

**Wind direction.** A bearing. Ordinary arithmetic is invalid: a naïve mean of
350° and 10° gives 180°, the opposite direction. Use circular statistics or
resolve to vector components. Before any of that, drop the zero values — zero is
a sentinel meaning variable-or-calm, not a bearing of due north, and the files
give no way to tell those two cases apart. Differencing two directions requires
wrapping to ±180°.

**Wind speed and gust.** Both are knots and both are statistics over a
ten-minute window ending at the observation time, so within a record they may be
compared, differenced and ratioed. Across records: the gust is a maximum, and
maxima do not average. A "daily maximum gust" taken from hourly reports is the
maximum over roughly sixty minutes of sampled window per day, not over the day —
it is a lower bound on the true peak, and it should be reported as one. Absence
of a gust value does not mean zero gust; it means no gust met the reporting
criterion, so imputing zero and averaging corrupts both the mean and the
variance. Both members are whole-knot integers, so a one-knot difference is at
the quantisation floor.

**The support-window trap that applies to all three wind members.** The values
summarise ten minutes, but the cadence is an hour. Averaging them yields a mean
over the sampled sixth of elapsed time, not a mean over the elapsed time.
Anything phrased as "average wind over the day" must be qualified accordingly.

**Visibility.** A string, in statute miles, and censored. "10+" means *at least*
ten, not ten. Parsing it to 10 and averaging biases the mean downward and
destroys the upper tail. Treat it as right-censored data, or reduce it to
threshold counts. Note also that this is the only imperial-length member in a
record whose elevation is metric — do not let a unit-inference routine mix them.

**Altimeter setting.** Reduced to the aerodrome's own elevation. Across records
from one station it may be differenced to obtain pressure tendency. Across
stations at different elevations it is **not** a comparable pressure field, and
differencing it between stations does not yield a pressure gradient. In the
example record the altimeter setting and the sea-level pressure agree almost
exactly, but that is an artefact of a station three metres above sea level and
must not be generalised.

**Sea-level pressure.** This is the member intended for cross-station comparison
and gradient work, because the reduction puts every station on a common surface.
Its accuracy degrades with the size of the reduction, so comparisons among
stations of very different elevation carry reduction error that the record does
not quantify. It may be absent.

**Altimeter setting versus sea-level pressure.** Same unit, different reference
surfaces. Never concatenate them into one series, never substitute one for the
other when one is missing, and never difference them expecting a physical
quantity.

**Elevation.** A fixed station attribute in a mean-sea-level vertical datum.
Differences between stations are valid within that datum. It must not be
combined with ellipsoidal (GNSS) heights without a geoid correction. It is not a
time series and should not be averaged over records.

**Latitude and longitude.** Degrees in a geographic CRS. Distances require a
geodesic computation, not Euclidean arithmetic on degrees, and longitude must
never be averaged naïvely across the antimeridian.

**Flight category.** A label, and one *computed from* ceiling and visibility.
Only counting and grouping are valid — no arithmetic, no averaging of an ordinal
encoding without saying so. Crucially, it is not independent evidence: using it
as a predictor alongside visibility and cloud in the same model is circular.

**Quality-control flag.** A bitmask. It is not ordered and not additive: a value
of 2 is not worse than 1 and not half of 4. Summing or averaging it is
meaningless. Without the bit definitions, the only defensible use is
zero-versus-nonzero grouping.

**Report type.** Categorical, and about the observing programme rather than the
air. Group by it; never treat it as a condition of the atmosphere.

**Present weather and cloud layers.** Strings; the cloud member is a nested
document carried as encoded text. Coverage codes are categorical. Layer base
values carry no declared unit anywhere in the record — see the ambiguities.

**Observation time versus report time.** Never mix the two axes. Ordering or
binning a series by report time places observations at the wrong point on the
phenomenon axis; their difference is only meaningful as pipeline latency.

**All cross-record combinations above assume a common station identifier**
unless explicitly stated as cross-station.

# 4. Time

The observation time is the time axis of the thing described: it is the instant
at which the reported conditions obtained. The report time belongs to the
publishing process, not to the atmosphere, and is a second, distinct axis.

Positions on the phenomenon axis are UTC instants. The upstream source delivers
them as epoch seconds, so the resolution is one second, though in practice the
value is the nominal observation minute rather than a precise sensor instant.

Nothing in the record carries a local offset or a timezone. Civil time at the
station is therefore **not determined** by these files. Any diurnal analysis must
either stay in UTC or bring in an external timezone-and-DST lookup keyed on the
station. Binning stations together by UTC hour-of-day silently mixes different
local times of day and will produce a smeared, meaningless diurnal curve for any
multi-station set.

Two further alignment points that are easy to get wrong. First, the record is not
internally simultaneous: temperature, dewpoint, pressure, visibility, present
weather and cloud all apply *at* the observation instant, while the three wind
members apply to the ten-minute interval *ending* at that instant. Treating them
as co-timed introduces up to ten minutes of offset. Second, routine reports fall
near the end of the clock hour — the example is at :51 — so the hour label of a
report is not the hour it characterises; its wind window lies in the last ten
minutes of that hour. The declared hourly cadence is nominal, and special
reports break it.

# 5. Ambiguities

- **Cloud layer base unit and datum.** Not stated anywhere. The example shows
  4500 and 25000 against raw codes of 045 and 250, which fixes the factor of one
  hundred but not the unit. My reading is feet above ground level, by METAR
  convention — **this is a guess** from general knowledge, not something the
  files establish. The datum relationship between cloud base and the station's
  mean-sea-level elevation is **not determined**; I decline to assume they share
  a reference.
- **Coverage codes and ceiling definition.** Which coverage codes constitute a
  ceiling, and the numeric thresholds that map ceiling and visibility onto the
  four flight categories, are **not determined**. I decline to supply them.
- **Quality-control bit meanings.** **Not determined.** Declining.
- **Visibility string grammar.** The unit is stated and two shapes are alluded
  to (a plus-qualified value and fractions), but no complete grammar is given. I
  decline to specify a parser.
- **Zero wind direction.** Conflates variable and calm with no discriminator
  provided. **Not determined.** Whether due north is encoded as 0 or 360 is also
  **not determined**.
- **Missing gust.** Described as omitted when no gust was *reported*, which is a
  statement about reporting, not about occurrence. Whether a missing gust means
  no gust occurred, none met threshold, or the sensor was unavailable is **not
  determined**.
- **Null versus absent.** Only the station identifier, observation time and raw
  text are mandatory; several members are additionally nullable. Whether an
  explicit null differs in meaning from an omitted member is **not determined**.
- **Per-record station geometry.** Position and elevation ride on each record
  rather than on a station table, and neither is mandatory. If two records for
  the same station disagree on coordinates, which is authoritative — and whether
  the disagreement signals a re-survey or an error — is **not determined**. No
  station registry is supplied.
- **Corrections and duplicates.** Whether reports are ever amended or
  retransmitted, and how two records sharing a station and observation time
  should be resolved, is **not determined**. The report-type member is an open
  string; values beyond the two named ones may occur.
- **Completeness.** Whether the feed contains every station and every cycle is
  **not determined**, so a gap cannot be distinguished from a station that did
  not report.
- **Temperature resolution.** The example carries tenths, and my general
  knowledge says that precision comes from an optional remark group and is
  absent from some reports, leaving whole degrees. Whether resolution varies
  across this feed is **not determined** from the files; treat mixed precision as
  a live possibility when computing small differences.
- **Concept definitions.** The observable-property and catalogue references point
  at placeholder hosts that cannot be dereferenced, and the schema's own
  identifier is likewise a placeholder. The precise definitions behind the
  aerodrome-surface-weather, present-weather, cloud-layers and flight-category
  concepts are therefore **not available**, and I decline to substitute my own.
- **Pressure back-conversion.** The altimeter setting is published in
  hectopascals while the raw text carries it in inches of mercury; the conversion
  and rounding have already happened. Back-converting will not reproduce the
  original figure exactly. This is an observation about the example, not a
  documented rule.
- **Who computes the derived members.** The reductions and the flight category
  are marked as calculated, but whether they are computed upstream or by this
  feed — and hence whether their conventions are stable over time — is **not
  determined**.
