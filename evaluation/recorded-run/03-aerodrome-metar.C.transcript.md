# 1. What this feed is

Each record is one surface weather observation issued by a single aerodrome
reporting station, keyed by its ICAO identifier, and stamped with the instant
the conditions obtained. It carries the decoded surface state — air temperature,
dewpoint, wind, prevailing visibility, two different pressure reductions, present
weather, cloud layers — alongside the original coded observation text from which
all of those were decoded, plus one derived operational label (the flight
category) and an automated quality-check bitmask.

The critical framing point: this is not a sensor telemetry stream. It is the
output of an **observing programme**. Records exist because the programme's rules
say a report is due, and some records exist precisely because the weather
changed. The record set is therefore not a uniform sample of the atmosphere, and
several members describe the programme rather than the sky. Treating the feed as
an evenly-spaced instrument time series is the single largest source of error
available here.

# 2. Analytics worth running

**Flight-category availability and persistence per aerodrome.** Every record
carries a category label and an observation instant, so you can compute the
fraction of time an aerodrome sits in each category, the transition matrix
between categories, and the duration distribution of below-VFR spells. This is
the highest-value analysis in the feed because the label is already
authoritative — it is stated to be produced by applying published thresholds,
which means you should consume it, not recompute it (see §5).

**Gust structure.** Sustained speed and gust speed are stated to come from the
same ten-minute window, one as the mean and one as the peak. That shared window
is what makes the gust factor (peak minus mean, or peak over mean) a coherent
quantity rather than a comparison of two unrelated samples. Gust-factor
distributions by direction sector and by category are well supported.

**Fog and low-ceiling onset lead time.** Temperature and dewpoint are both on the
same scale at the same instant, so their spread is meaningful per record. You can
test how far ahead of a mist/fog present-weather code or a category degradation
the spread begins closing. The data support this because both values, the present
weather codes, the cloud layers and the resulting category all share one
timestamp.

**Latency and pipeline health.** The gap between when conditions obtained and
when the report was issued is directly measurable per record. Its distribution,
and its tail, tell you the usable freshness of the feed for any operational
consumer.

**Decode fidelity auditing.** The raw coded text is retained alongside every
decoded value, so every decoded member can be independently re-derived and
checked. In this example the decoded wind (210° / 12 kt / gust 18) reproduces the
coded wind group exactly, and the two pressure members reproduce the altimeter
group and the sea-level-pressure remark. Any systematic decoder drift is
detectable without external data.

**Observing-programme volatility.** The rate of special (non-routine) reports per
station per unit time is itself a signal of how fast conditions are changing.
This is a legitimate analysis *of the programme*; it is not a measurement of the
atmosphere, and it must not be mixed into atmospheric statistics.

**Pressure/density altitude.** Altimeter setting, station elevation and
temperature are all present, which is the input set such a computation needs. The
formulas themselves are not in the files; supply them from outside and say so.

**Not supported without external data:** anything requiring runway orientation
(crosswind and tailwind components, runway selection) — runway headings are
nowhere in this feed. Also anything requiring local civil time (§4).

# 3. Combination rules

**Air temperature and dewpoint.** Interval scale with an arbitrary zero.
*Comparable* across records and across stations. *Differenceable* — the
temperature-minus-dewpoint spread is the intended and meaningful difference, and
differences of the same quantity across time or stations are meaningful.
*Averageable* over records, with the caveat in the last paragraph of this section
about which records you average. **Never summed** — the sum of two Celsius
temperatures has no referent. **Never ratioed** — "20 °C is twice 10 °C" is
false on this scale. Cross-station comparison of raw temperature conflates
elevation differences; elevation is available per record, but the files supply no
lapse rate, so any elevation correction is yours and must be declared.

**Wind direction.** A circular quantity in degrees true. **Not** differenceable,
summable or averageable by ordinary arithmetic: the mean of 350 and 010 is not
180. Use vector or circular statistics only. Additionally, the value 0 is a
**sentinel**, not a bearing — it denotes variable or calm. Any record with
direction 0 must be excluded from, or separately handled in, every directional
aggregate; including it drags every mean toward north. Comparison of two
directions is meaningful only modulo 360.

**Sustained wind speed.** A ratio-scale quantity, so comparable, differenceable,
averageable, and formally summable. But each value is a **ten-minute mean ending
at the observation instant**, not an instantaneous reading and not an hourly
mean. Consequences: a series of these values is a once-per-cycle snapshot of a
ten-minute window, so integrating it over time to obtain run-of-wind or total
wind travel is invalid — the windows do not tile the interval. Averaging a set of
them yields "the mean of the sampled ten-minute means", which is a different
estimand from "the mean wind over the period"; the difference matters when
sampling is condition-triggered.

**Gust speed.** A maximum over the same ten-minute window as the sustained speed.
*Differenceable against the sustained speed of the same record* — that is the one
combination this pairing is built for. **Do not average gusts with sustained
speeds**, and **do not average gusts across records naively**: gust speed is
present only when gusts were reported, so absence is informative, not missing at
random. Substituting zero for an absent gust is wrong (it fabricates a calm
peak); dropping the absent records is also wrong for any question about typical
gustiness (it conditions on gusts existing). Decide and declare which estimand
you want.

**Altimeter setting and sea-level pressure.** Both are in hectopascals and they
are **different quantities**. One is reduced to the aerodrome elevation under a
standard-atmosphere assumption; the other is reduced to mean sea level using the
station elevation and its temperature history. They must not be pooled, averaged
together, or treated as interchangeable, and their difference is an artefact of
two reduction procedures, not a physical anomaly. For cross-station synoptic work
— pressure gradients, trough and ridge location — use the sea-level reduction
only; it is the one constructed to be comparable between stations of differing
elevation. The altimeter setting is comparable across stations only in the sense
that it is the value each aerodrome would set; differences in it partly encode
elevation differences. Within a single station, either may be differenced across
time to obtain a tendency, but do not mix the two series.

**Prevailing visibility.** Delivered as text with qualifiers, and at least one
qualifier ("10+") denotes a **censored** value: the true visibility is at or above
the stated figure, not equal to it. Parsing it to 10 and averaging biases every
visibility mean downward, and the bias grows as conditions improve. Fractional
forms will not parse as decimals. Visibility may be compared and ordered
(treating censored values as at-or-above the bound); it may be averaged only with
explicit censoring handling; it must never be summed.

**Cloud layer heights.** Delivered as an embedded encoded array, so they require a
second parsing step before any arithmetic. Within one record, layers may be
ordered and the lowest obscuring layer identified. Across records, bases may be
compared and differenced **only if the height reference is the same**, which the
files do not state (§5). Do not add a cloud base to the station elevation: the
units differ from elevation's units and the reference level is undetermined.

**Station elevation and position.** Fixed station metadata repeated on every
record, not measurements. Comparable across stations; averaging them across
records is meaningless (it just weights stations by report count). Latitude and
longitude are geographic degrees on the stated reference frame and must be
handled as such — degree differences are not distances, and longitude degrees do
not convert to distance at a fixed rate.

**Quality-control flag.** A **bitmask**. It is nominal, not ordinal and not
numeric. It must not be compared as a magnitude, differenced, summed or averaged.
Only per-bit prevalence counts are legitimate, and only if you know the bit
meanings, which the files do not give.

**Flight category, present weather, report type, station name, raw text.**
Categorical or free text. Only counts, proportions and transition frequencies.
Note that the flight category is a **deterministic function of the ceiling and
visibility already in the record**; using it as an explanatory variable alongside
visibility or cloud data in the same model is circular.

**The only legitimate summation in this feed is counting records** (reports per
station, hours in a category, number of gust events). Every measured quantity
here is intensive or instantaneous; none of them add.

**Governing all averaging:** records are of two kinds, routine and special, and
the special ones exist *because conditions were changing or had deteriorated*.
Any average taken over a mixed set is biased toward disturbed weather, and the
bias is worst exactly when the weather is worst. For climatological or
distributional work, restrict to routine reports, or weight by the time each
observation represents. State which you did.

# 4. Time

The time axis of the thing described is the **observation time** — the instant at
which the reported surface conditions obtained. Every measured member in the
record is anchored to that instant (the wind members to the ten-minute window
ending at it). All time-series construction, joining, resampling, and lag analysis
must key on that member.

The **report time** is the issuance instant of the encoded result — a property of
the dissemination process, not of the atmosphere. Using it as the time axis
shifts every value later by a variable latency and destroys any lead/lag analysis.
Its only correct use is as the endpoint of a latency measurement, or for
reconstructing what a consumer knew at a given moment (as-of / point-in-time
joins), which is a genuinely different and useful question from what the weather
was.

Both instants are absolute points on the UTC timeline. The observation time
originates as a count of seconds from the epoch, so it carries no zone or
daylight-saving ambiguity at all; the report time arrives as a UTC-qualified
string. Positions on the axis therefore relate to civil time **only through a UTC
offset for the aerodrome, which these files do not provide**. Longitude is not a
time zone and must not be used as one. Consequently any diurnal-cycle, local
business-hours, or day-boundary analysis requires an external zone mapping — I am
declining to supply one.

Axis spacing is irregular by construction. The routine cycle is stated to produce
about one report per station per hour, normally near the end of the hour, and the
example sits at :51 — so the natural "hourly" series is offset from the top of the
hour, and special reports insert additional, condition-triggered points between
them. Two consequences: methods that assume uniform sampling (spectral analysis,
naive fixed-lag correlation, differencing as a proxy for a rate) require explicit
resampling first; and the resampling rule you choose reintroduces the
special-report bias unless it is time-weighted. Whether a report near the end of
an hour should be labelled with that hour or the next one is a convention the
files do not settle — pick one and declare it.

# 5. Ambiguities

**Cloud base units and reference level — inference, flagged.** The schema states
only that each layer carries a coverage code and a base height; it gives no unit
and no reference. In the single example the decoded bases correspond to the coded
cloud groups multiplied by one hundred, which is consistent with feet. Whether
those heights are above ground or above mean sea level is **not determined**, and
it matters: station elevation here is small, so a single example cannot
distinguish the two. I am declining to decide it. Do not combine cloud bases with
station elevation until it is resolved.

**Ceiling definition and flight-category thresholds — declining.** The category is
stated to be derived from ceiling and visibility, but neither the rule that picks
the ceiling out of the cloud layers nor the numeric thresholds appear in the
files. Consume the supplied category; do not attempt to recompute it, and do not
assume any particular threshold set.

**Quality-control bit semantics — declining.** The mask is stated to be per-check
bits, but no bit is defined. You cannot filter on quality with this feed alone.
The observed value of 2 tells you one specific check fired or passed, and nothing
more.

**Temperature and dewpoint precision — inference, flagged.** In the example, the
decoded values carry tenths while the main coded body carries whole degrees; the
tenths appear to come from a supplementary group in the remarks. If that reading
is right, then precision varies between reports and between stations depending on
whether that group is present, and any analysis sensitive to sub-degree resolution
(dewpoint spread near zero, fog onset) will have heterogeneous resolution. I
cannot confirm this from one example — treat it as a hypothesis to test against a
larger sample.

**The direction-zero sentinel — partial inference, flagged.** Zero is stated to
mean "variable or calm", which conflates two physically different states. It is
plausible that the two can be separated by whether the sustained speed is also
zero, but the files do not say that, and they do not say whether a variable wind
might instead be reported with a nonzero mean direction. Declining to decide.

**Missing versus null.** Most measured members are optional rather than nullable,
while several textual members are explicitly nullable. Whether an absent member
and an explicit null carry different meanings for a given quantity is **not
established** by the files. Only the station identifier, the observation instant
and the raw text are guaranteed present; assume nothing else exists in any given
record.

**Visibility qualifier vocabulary — declining.** One censoring qualifier and the
existence of fractional forms are mentioned; the full set of forms that may appear
is not enumerated. Write the parser defensively and log unparsed forms rather than
coercing them.

**Reporting-station identity over time — not determined.** Nothing in the files
establishes whether a station's position, elevation or name are stable across the
history of the feed, or whether an identifier can be reassigned. For long-baseline
work, treat the station metadata as observed-per-record rather than as a static
dimension table until you have verified stability empirically.

**Multi-station scope — assumption.** Because position and elevation ride on every
record rather than being fixed, the feed can plainly carry more than one station,
but the files do not state the population of stations, its stability, or any
guarantee of completeness. Do not compute network-wide statistics as if the
station set were fixed.

**Duplicate, corrected and amended reports — not determined.** Nothing in the
files says whether a later record can supersede an earlier one for the same
station and observation instant. Until verified, do not assume that station plus
observation instant is a unique key; check for it, and decide a
last-report-wins or first-report-wins rule explicitly.
