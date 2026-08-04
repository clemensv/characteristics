# 1. What this feed is

Each record is a single timestamped snapshot from a fixed-identity marine
observing station: an identifier, a geographic position, an instant, and then a
mixed bag of surface meteorology (wind vector, gust, barometric pressure and its
tendency, air temperature, dewpoint, visibility) and sea state (wave height, two
wave periods, mean wave direction, water temperature, tide). Only the
identifier, position and time are guaranteed present. **Every measured quantity
is optional**, which means the feed is sparse by construction and the sparsity
carries information: the example record omits visibility and tide entirely, and
nothing in the data distinguishes "this station has no such sensor" from "the
sensor failed this cycle" from "the value was suppressed by quality control."
An analyst who treats absence as zero, or who back-fills it, will manufacture
signal.

The position travels *inside every record*, not alongside the station identity.
That is a deliberate shape and should be read as such: you may not assume that a
given `station_id` maps to one fixed coordinate pair. A moored buoy swings
around its anchor and can be re-deployed; the data model permits the position to
change from record to record and nothing constrains it not to. Join on identity
if you want a time series; join on position only if you have first checked
whether position is actually stable for that identity in your window.

The coordinates in the example put the station in the open western North
Atlantic — but that reading assumes the conventional sign and ordering of
latitude/longitude, which the files do not state (see §5).

# 2. Analytics

**Per-station time series and trend detection.** The identifier plus a
monotonic-comparable instant is the whole basis for this, and it is the analysis
the feed most directly supports. Pressure, temperature, wave height and wind
speed are all repeated scalar observations at one place, so run-length,
persistence, rate-of-change and threshold-crossing analyses are all sound
*within* one station.

**Gustiness.** `gust` divided by `wind_speed` is a dimensionless ratio. This is
the single most robust derived quantity in the feed, because it survives the
fact that the wind unit is never stated — the ratio is the same in knots, m/s or
mph. It is a usable turbulence/stability proxy and it is comparable across
stations even when nothing else is.

**Spectral narrowness of the sea state.** `dominant_wave_period` divided by
`average_wave_period` is likewise unit-free. A ratio near 1 indicates a narrow,
single-source sea; a large ratio indicates a mixed sea with swell arriving
separately from the locally generated wind waves. This is available without
knowing whether periods are in seconds.

**Air–sea temperature difference and dewpoint depression.** Both are
scientifically valuable (the first is a boundary-layer stability proxy, the
second a saturation/fog proxy). Both are *conditional*: they are only meaningful
if the two temperatures involved share a scale, and the files do not establish
that they do (see §3).

**Wind-driven versus swell-driven sea.** Comparing `wind_direction` to
`mean_wave_direction`, and `wind_speed` to `wave_height`, separates locally
generated wind sea from remotely generated swell. This is a genuinely useful
analysis but it is gated on a directional convention the files do not supply —
performing it naively is the most likely way to get a confidently wrong answer
from this feed.

**Cross-validating the reported tendency.** `pressure_tendency` is a change,
while `pressure` is a level. Differencing successive `pressure` values gives an
independent estimate of the same thing, which is a good data-quality check —
*provided* your differencing interval matches the (unstated) interval the
reported tendency is computed over. If they differ, the two will disagree
systematically and the disagreement means nothing.

**Availability and outage analysis.** Because members are optional, you can
profile sensor uptime per station per member over time. This is real and useful
and requires no unit knowledge at all.

**What the feed does not support well:** cross-station comparison of absolute
wind speed. Anemometer height is not carried, and wind speed is strongly
height-dependent, so two stations' wind speeds are not on the same footing
unless you know their sensor heights from outside this feed. Likewise extreme
value analysis is weakly supported, because there are no quality-control flags
— an outlier and a genuine extreme look identical here.

# 3. Combination rules

**`station_id`** is nominal. Group and join on it. Never order, difference or
average it, and do not infer proximity from numeric adjacency of identifiers.

**`latitude` / `longitude`** are angular coordinates on a sphere, not free
scalars. Within one station they may be averaged to estimate a mean mooring
position and differenced to measure watch-circle excursion. Across widely
separated stations a plain arithmetic mean is not a location. Longitude wraps at
the antimeridian; any differencing must be done modulo 360 or it will produce
errors of that magnitude for stations straddling the wrap.

**`wind_direction`, `mean_wave_direction`** are circular. They may be compared
only after reducing the difference to the shorter arc; they must **never** be
summed or arithmetically averaged. The mean of 350 and 10 is 180 under naive
arithmetic and 0 in reality. Vector-average (mean of unit vectors), or do not
average at all. Additionally, comparing `wind_direction` to
`mean_wave_direction` is only valid if both use the same convention (direction
*from* versus direction *toward*, and true versus magnetic north). The files
establish neither, and the two members could legitimately differ in convention.
Under one reading the example is a wind and sea in near-alignment; under the
other they are nearly opposed. **Do not difference these two members until the
convention is established externally.**

**`wind_speed`, `gust`** are non-negative magnitudes on a ratio scale. Within a
station they may be compared, differenced, averaged and ratioed. `gust` is a
*peak* statistic and `wind_speed` is a *mean* statistic; they are not
interchangeable and must not be pooled into a single "wind" series. Averaging
gusts produces a mean-of-maxima, which is not the maximum and not the mean —
label it as such or it will be misread. Cross-station combination is blocked by
the missing sensor height and by the missing averaging window.

**`wave_height`** may be compared, differenced and averaged within a station.
Note that a mean of wave heights is not the wave height of the mean sea state;
wave energy goes as the square, so if you want an energy-weighted aggregate you
must average the square and take the root, not average the height.

**`dominant_wave_period`, `average_wave_period`** are two different statistics
of the same underlying spectrum and **must not be combined with each other, nor
pooled into one series.** Each may be averaged within its own kind, but note
that period is a reciprocal quantity: the mean of periods is not the reciprocal
of the mean frequency. For physics that is frequency-linear, convert, average,
convert back.

**`pressure`** may be compared, differenced and averaged within a station.
Across stations it may be compared only if all values are reduced to a common
reference (typically sea level); the files do not say whether they are, and for
a marine surface station the distinction is smaller than for land stations but
not necessarily zero.

**`pressure_tendency`** is already a difference. It must **never** be added to
or differenced against `pressure` — they are not the same kind of quantity.
Tendencies may be averaged across records only if every record's tendency covers
the same window length, which the files do not guarantee. Tendencies over
adjacent, non-overlapping windows may be summed to give the total change; over
overlapping windows they may not, and nothing here tells you which case you are
in.

**`air_temperature`, `water_temperature`, `dewpoint`** are on an interval scale.
Differences are meaningful; sums are not; averages are meaningful only for
values on the same scale. Ratios are meaningless (a 20-degree reading is not
"twice as warm" as 10). Crucially, the files do not state that these three share
a unit — nothing prevents one being Celsius and another Fahrenheit — so
`air_temperature − water_temperature` and `air_temperature − dewpoint`, both
standard and valuable derivations, are **conditional on an assumption you must
make explicit and verify externally.** The example values are mutually plausible
on a single Celsius scale, but three plausible numbers do not establish a
convention.

**`visibility`** is a non-negative magnitude, comparable and differenceable, but
it is typically censored at a sensor maximum, and this feed carries no indicator
of censoring. Averaging censored values biases low.

**`tide`** is a signed displacement relative to a datum that the files do not
identify. Differences of tide *at the same station* are meaningful (change in
water level). Comparing or averaging tide *across* stations is meaningless
unless they share a datum, and nothing here says they do. Tide must not be
combined with `wave_height`, which measures a different thing about the same
water surface.

**Universally:** because no member carries a unit, any combination of two
different members into a physical formula (wave steepness, wind stress, relative
humidity, air density) is unsound from these files alone. Only unit-free
constructions — ratios of like to like — are safe.

# 4. Time

`timestamp` is the sole member establishing the time axis, and it is required,
so every record has a position on that axis. It is a date-and-time type, and the
example carries an explicit `Z` offset, which pins that value to UTC and
therefore to civil time anywhere via the ordinary offset rules. Ordering,
differencing and windowing across records are sound wherever the offset is
present.

Two cautions on the axis itself.

First, **what the timestamp denotes with respect to the measurement is not
determined.** Several of the members are unavoidably aggregates over an
interval: mean wind speed, mean wave period, mean wave direction and wave height
are all statistics over a sampling window, and `pressure_tendency` is explicitly
a change over some prior window. The record gives one instant and no window
boundaries. Whether the instant is the start, midpoint or end of the sampling
window is left open, and the answer shifts every derived rate by up to the
window length. When correlating this feed against another time series — radar,
satellite, model output — that offset is the dominant alignment error and you
cannot resolve it from these files.

Second, **the tendency's window is a second, invisible time axis.** It is
implied by a member but never represented, so it cannot be read, checked or
harmonised across stations from within the data.

There is no ingest or record-creation time, and no sequence or version member.
Consequently late-arriving, duplicated or corrected observations for the same
station and instant are indistinguishable from one another. If you deduplicate
on `(station_id, timestamp)` — which appears to be the natural key — you will
silently pick one of a duplicate pair with no basis for preferring either.

# 5. Ambiguities

**Units of every measured quantity — not determined; I decline to decide.** No
member carries a unit and neither file states one. Wind speed could be m/s,
knots, km/h or mph; pressure could be hPa/mbar, inHg or kPa; temperatures could
be Celsius or Fahrenheit; wave height metres or feet; periods seconds; distances
and tide any length unit. The example values are individually plausible under a
common metric reading, but plausibility is not specification, and this is
precisely the class of assumption that produces confident, silent, order-of-
magnitude errors. Resolve it from the feed's documentation before computing any
cross-member physical quantity.

**Whether all temperature members share one scale — not determined; I decline to
decide.** Even granting a metric reading overall, nothing forbids mixed scales
across the three temperature members.

**Directional convention (from/toward, true/magnetic) for wind and waves — not
determined; I decline to decide.** This is the highest-consequence gap in the
feed, because both readings yield a coherent-looking answer and the two answers
are 180° apart.

**Angular unit for directions — guess:** degrees rather than radians. Marked as
a guess; the values 212.0 and 205.0 exceed 2π, which rules out radians for these
particular values, so the guess is well-supported but is still an inference from
one record rather than a stated fact.

**Coordinate reference system and datum for position — not determined; I decline
to decide.** No CRS is named. A modern global datum is likely, but at the metre
scale the choice matters and cannot be read off.

**Sign convention for longitude — guess:** negative is west of the prime
meridian, and the ordering is the conventional one. Marked as a guess; the
single negative longitude in the example is consistent with it but does not
establish it.

**Vertical datum for `tide` — not determined; I decline to decide.** Sign,
zero-point and reference surface are all unstated, so absolute tide values are
uninterpretable and only within-station differences are usable.

**Sampling/averaging window for wind, waves and gust; gust duration — not
determined; I decline to decide.**

**Window length for `pressure_tendency` — not determined; I decline to decide.**
A three-hour convention is common in surface meteorology, but adopting it here
would be an unsupported import from outside these files.

**Sensor heights (anemometer, thermometer) and water-temperature measurement
depth — not determined; I decline to decide.** These block cross-station
comparison of wind and, to a lesser degree, temperature.

**Meaning of an absent member — not determined; I decline to decide.** No
sensor, transient failure, failed quality control and value-not-applicable are
all collapsed into the same absence.

**Whether `(station_id, timestamp)` is unique — guess:** it is the intended key.
Marked as a guess; nothing in the files declares a key or forbids duplicates.

**Whether position is constant per station — not determined.** The model permits
it to vary and gives no way to tell drift from redeployment from a correction.

**Nominal reporting cadence — not determined.** Only one record is available, so
no interval can be inferred. Gap detection therefore requires an externally
supplied expected cadence.

**Value ranges and quality control — not determined.** No bounds are declared,
no quality flags exist, and no member marks a value as estimated, interpolated
or suspect. Outliers and genuine extremes are indistinguishable from within the
feed.

**Whether the identifier in the example belongs to a known station network —
guess, and I decline to rely on it.** The identifier's form and the coordinates
are suggestive, but treating a recognised-looking identifier as authoritative
would be exactly the kind of external fact the files do not establish.
