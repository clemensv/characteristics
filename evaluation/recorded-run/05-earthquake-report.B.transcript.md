# Reading the EarthquakeReport feed

## 1. What this feed is

**These records are bulletins, not earthquakes.** That is the single most important
thing to understand before touching the data.

Each record is one published revision of a Japan Meteorological Agency report
about a seismic event. The unit of the row is the report; the unit of the
phenomenon is the earthquake. They are related many-to-one: a stable event
identifier is shared by every bulletin describing the same earthquake, a serial
number orders the revisions within that event, and a composite report identifier
is the actual primary key of a row. A single earthquake will therefore appear
several times in the stream, with progressively refined values, and the record
that says a bulletin was *cancelled* is itself a row.

What each row carries is a **solution**, not a measurement. The hypocentre
coordinates, the depth and the magnitude are all marked as calculated: they are
the output of inverting arrival times and displacement amplitudes across a
national network, not readings taken off an instrument. The maximum intensity
values — both at report level and per prefecture — are marked as statistics,
specifically maxima over the set of stations that had reported by the time the
bulletin was cut. The tsunami flag is marked as *estimated*, and its description
is explicit that it was inferred from free-text commentary by the ingestion
bridge rather than read from a coded field published by JMA.

So the feed mixes three provenance classes in one row: values computed by the
publishing authority, statistics summarised by the publishing authority, and one
value guessed by the pipeline. They should not be trusted equally.

A fourth thing sits alongside the results: the bulletin product code carries the
role of *result quality*. It is not a category for faceting a chart, it is the
maturity grade of the solution in that row. One of its values is documented as a
flash issued before the source parameters have been determined at all. Rows of
that kind are structurally incapable of carrying a hypocentre or magnitude.

## 2. Analytics worth running

**Solution latency.** The two published time members are declared with distinct
roles — one is the time the rupture began, the other the time the solution became
available — and a third records handover into the distribution channel. Their
differences are therefore well-defined and meaningful: report-minus-origin is how
long JMA took to produce a solution; control-minus-report is how long the
distribution system took to move it. Stratified by bulletin product code, this
directly measures the timeliness contract of each product class. This is the
cleanest analysis in the stream because the schema does the hard part — telling
you which instant means what — that a raw feed would leave you to guess.

**Revision convergence.** Group by event identifier, order by serial, and watch
magnitude, coordinates, depth and maximum intensity move. Because the source
parameters are explicitly calculated quantities and the intensity is explicitly a
maximum over a growing station set, the drift between serials is *solution
refinement and reporting completeness*, not physical change. This tells you how
much an early bulletin can be trusted, how much magnitude typically moves between
first and final, and how long it takes to stabilise. It is also the analysis most
often destroyed by people who treat rows as events.

**Catalogue construction and seismicity statistics.** Collapse to one row per
event — latest serial that is not a cancellation and that actually carries a
determined hypocentre — and you have a usable catalogue for event rates,
magnitude distributions, depth distributions and spatial patterns. The
identifier/serial/status triple is exactly what makes this deduplication
possible, and its presence is the reason this feed can be used for catalogue work
at all.

**Source-region profiling.** The epicentre area code is a stable coded identifier
for a seismic source region, and a coordinate reference system is declared for the
coordinate pair, so grouping by region and characterising its depth and magnitude
distribution is supported.

**Shaking versus source.** Within the product class that carries both, you can
relate maximum intensity to magnitude and depth. This is supported because both
appear in the same row for the same event, at the same phenomenon instant.
Intensity must be handled as an ordered category throughout.

**Pipeline and data-quality monitoring.** The rate of corrections and
cancellations, the rate at which the English title is absent, the rate at which
the tsunami flag is null, and the rate at which coordinates are omitted broken
down by product code, are all directly measurable and are genuinely diagnostic
because the schema distinguishes authority-published values from bridge-inferred
ones.

**What is not supported.** Total energy release (see §3 on magnitude). Anything
about whether a tsunami occurred — the flag is an estimate of a bulletin's
*intent*, not an observation. Intensity at any specific place: there are no
station-level values and no prefecture geometry. Rupture duration or extent:
every computed quantity is tagged as relating to an *instant*, so the record
describes a point in time and nothing in it bounds an interval.

## 3. Combination rules

| Quantity | Compare | Difference | Sum | Average | Condition |
|---|---|---|---|---|---|
| Event identifier | equality only | no | no | no | Nominal. Digits, but an identifier. |
| Serial | yes, **within one event only** | within one event only | no | no | Ordinal revision index; has no cross-event meaning. |
| Report identifier | equality only | no | no | no | The true row key. |
| Information type | equality only | no | no | no | Categorical status; counts by category are fine. |
| Origin time | yes | yes, **after deduplicating to one row per event** | no | no | Instants. Differencing two bulletins about the same quake yields zero and is a bug, not a result. |
| Report time, control time | yes | yes | no | no | Different axes from origin time. |
| Latency (report − origin, control − report) | yes | yes | yes | **yes** | Durations. This is the derived quantity that *is* safe to average. |
| Latitude, longitude | yes | see below | **no** | **no** | Angular; see below. |
| Depth | yes | yes | rarely meaningful | yes, within a defined population | Kilometres, ratio scale. |
| Magnitude | yes | yes, with care | **no** | **only with a caveat** | See below. |
| Maximum intensity (both levels) | **order only** | **no** | **no** | **no** | Ordered categories, not numbers. |
| Prefecture count per record | no | no | no | no | Reflects reporting completeness, not the earthquake. |
| Epicentre area code, prefecture code | equality only | no | no | no | Nominal, and **not the same code space**. |
| Tsunami flag | equality only, three-valued | no | no | no | Estimated, not published. |
| Bulletin product code | equality only | no | no | no | A quality grade, not a result. |

**Coordinates must not be arithmetically averaged.** Degrees of latitude and
longitude are angular coordinates on a declared geodetic reference system. Their
plain arithmetic mean is not a centroid, their plain difference is not a
distance, and longitude wraps. Any spatial aggregation must be done geodesically
or in a projection. Latitude, longitude and depth are also documented as coming
out of one joint inversion: their errors are correlated and they must not be
treated as three independent measurements.

**Magnitude.** Comparison and ordering are safe; so are counts above a threshold
and quantiles. Summing is never meaningful. Whether the arithmetic mean is
meaningful depends on whether the scale is logarithmic in the underlying physical
quantity — the two files say only that it is dimensionless, computed from
displacement amplitudes by the published JMA formula, and "similar to Richter
magnitude for shallow events". *I am assuming, from outside these files, that it
is logarithmic; the files do not state it.* On that assumption a mean magnitude
must never be read as an energy average. Independently of that assumption,
magnitudes here are on the JMA scale only and must not be pooled with magnitudes
from any other catalogue.

**Intensity must never be arithmetised.** The scale includes "5-" and "5+" as
distinct values. There is no numeric interpretation under which these behave. A
mean intensity, a sum of intensities, or a difference of two intensities are all
meaningless. Ordering is available, and *maximum* is available and composes
correctly — the maximum over a set of prefecture maxima is a valid maximum. The
mean of a set of maxima is not a mean of anything. Note also that the scale is
closed at 7: it cannot distinguish among the most severe events, so 7 is a
ceiling category and any distribution is censored at the top.

**Do not count the report-level maximum and the prefecture maxima as separate
observations.** The report-level value is a maximum over a station set that
includes the stations behind the prefecture values. Pooling them double-counts.

**Do not mix the three time axes.** Binning by report time or control time and
calling the result seismicity is wrong: the source parameters are attached to the
origin instant, and the report time reflects the operations of the agency, not
the behaviour of the Earth.

**Do not pool across bulletin product codes without stratifying.** Product codes
denote different solution maturities, including one issued before source
parameters exist. A magnitude distribution computed over an unstratified mix is a
mixture of populations of different quality.

**Absence is not random, and absence is not null.** Two different missingness
mechanisms are in play. Some members are nullable and will carry an explicit
null; others are neither required nor nullable and will simply *not be present*.
Code that treats a missing key and a null value as the same thing will
mis-handle one of the two. More importantly, the omissions are documented as
systematically tied to the bulletin product class — flashes, commentary bulletins
and source-element update notices are the ones that lack coordinates, magnitude
and intensity. Dropping incomplete rows therefore silently filters by product
maturity. That is usually the right thing to do, but it must be a decision, not
an accident. A missing intensity means "this product carries no intensity
summary", not "no shaking".

## 4. Time

The time axis of the thing described is the **origin time** — the instant at which
rupture began. It is the only member carrying the phenomenon-time role, and it is
the instant to which the hypocentre, depth and magnitude are attached; all of
those are tagged as relating to an instant rather than to an interval. The report
time is the result time (when the solution became available) and the control time
is the ingestion time (handover to distribution). Both are properties of the
publishing process, not of the earthquake. Report time is later than and
independent of origin time by the schema's own statement, so the two must never
be substituted for one another.

The origin-time axis is declared to have **irregular cadence with no period**.
Consequences: there is no expected spacing, so nothing may be resampled,
interpolated or gap-filled as though it were a regular series; and the absence of
a record in an interval is not a zero-valued sample, it is simply no bulletin.

All three timestamps are RFC 3339 and are stated to have been normalised to UTC;
the example carries a `Z` offset on each. The upstream feed is described as
publishing in Japanese local time with a local offset, so **rendering these back
to civil time for a Japanese audience requires converting out of UTC**. The files
do not state the numeric offset. *I am assuming, from outside these files, that
it is UTC+9.*

There is a discrepancy here that anyone building on this feed will hit. The event
identifier is documented as JMA's rendering of the origin time in
`YYYYMMDDHHMMSS` form, and the origin time is documented as having been converted
to UTC. If the identifier is copied unchanged from a local-time source and the
timestamp has been shifted, the two should disagree by the offset. In the example
they agree digit for digit, and the digits embedded in the detail URL follow the
same convention. Either the identifier was rebuilt after conversion, or the
timestamps are local-time values wearing a `Z`. **I am declining to decide which.**
The operational rule that holds either way: do not parse the event identifier as a
UTC timestamp, do not assume the identifier and the origin time agree, and treat
the identifier strictly as an opaque key.

## 5. Ambiguities

**Origin time versus the identifier digits.** As above. *Declining to decide.*
Consequence stated above.

**Whether the coordinate is a precise hypocentre or a representative point for a
named source region.** The member is described as a hypocentre coordinate, but the
source path it is drawn from is the coordinate of the hypocentre *Area*. These are
not the same thing, and the difference matters for anything distance-based.
*Declining to decide.* Until resolved, do not compute epicentral distances and
present them as precise.

**No uncertainty is published for any computed value.** No error ellipse, no depth
uncertainty, no magnitude standard error. Not determined by these files.
Consequence: no weighting, no confidence intervals, no principled outlier test on
the source parameters.

**Scope of a cancellation.** Whether a cancelled bulletin retracts only that
serial or invalidates the event entirely is not determined. *Declining.* The
conservative reading — exclude the event from a catalogue until a later
non-cancelled bulletin appears — is a choice, not something the files license.

**Whether the serial is per event or per event-and-product.** An event may
plausibly produce a flash and then a full hypocentre-and-intensity bulletin under
one identifier. If the serial is shared across products, "take the highest serial"
may select a different product than intended. *Declining.* Deduplicating by
identifier *and* product code is the safer construction.

**The trailing integer in the detail URL.** In the example it is `1` while the
serial is `2`. What it denotes is not determined.

**Whether the prefecture list is complete, and whether it may be empty.** The array
is always present, but nothing establishes that it enumerates every prefecture
that felt the event, nor what an empty array would mean. Not determined.

**Prefecture codes and epicentre area codes appear to be different code spaces** —
the example uses `290` for the source region and `400`/`410`/`300` for
prefectures. *This is a guess* based on one record and on the differing
descriptions; the files publish neither code list. Do not join the two on code
equality without confirming.

**Sign information in depth is discarded.** The transformation is documented as
taking the absolute value of a signed source figure. Whether that sign ever
carried meaning is not determined; if it did, it is not recoverable from this
feed.

**The observable-property and schema identifiers are placeholders** pointing at
non-resolvable hosts, so the authoritative definition of the observed property
cannot be consulted. Not determined.

**The record's declared concept is a generic "Event", while the record is in fact a
report about an event.** I read this as a modelling looseness rather than a claim
that one row equals one earthquake — everything else in the two files points the
other way — but *that reading is my inference*, not something the files state.

**The annotation vocabulary itself** — the meanings of the derivation, statistic,
cadence, semantic-role and phenomenon-time-relation keywords — is referenced but
not available to me. I have read them from their names and from the surrounding
descriptions, which are consistent, but I have not verified them against their
defining specification.
