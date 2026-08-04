# Earthquake bulletin feed — analyst's briefing

## 1. What this feed is

Each record is **a bulletin about an earthquake, not an earthquake**. The pairing of
an `event_id` with a monotonic `serial`, plus an `info_type` drawn from
`ISSUED` / `CORRECTED` / `CANCELLED`, means one seismic event generates a *chain*
of records over time, each one a revised or withdrawn statement about the same
event. The example is `serial: 2` — already a second statement about that event —
and its `report_id` is the event key and the serial glued together.

Each bulletin carries a full restatement of the event parameters: where it
happened (coordinates, depth, and a named source region), how big it was
(magnitude), how strongly it was felt (an intensity grade, both overall and
broken out by prefecture), whether a tsunami is in play, and a URL to a
per-bulletin detail document. It also carries three distinct timestamps and a
product-type code (`bulletin_type`) identifying which of several bulletin
products this is.

The single most consequential thing to understand before touching this data:
**the row count is a count of bulletins, not of earthquakes**, and later rows
supersede earlier ones. Any analysis that does not first collapse the chain to
one row per `event_id` will over-count events, over-count tsunami flags,
double-count prefectures, and mix preliminary estimates with revised ones.

## 2. Analytics worth running

**Dissemination latency.** Three absolute instants are present on *every*
record, and they are required, so `report_datetime − origin_datetime` and
`control_datetime − report_datetime` are computable with no missingness and no
imputation. This supports a well-founded latency distribution: time from the
event itself to a public statement, and the further processing delay after that.
It can be cut by `bulletin_type`, by `serial` (first bulletin vs. follow-ups), by
`max_intensity`, and by epicenter area. This is the analysis the data supports
*best*, because it depends only on fields that are mandatory and absolute.

**Revision behaviour.** Because the event parameters are restated in full on
every bulletin, and the bulletins are ordered within an event by `serial`, you
can measure how the picture of an event changes as it matures: how much the
coordinates move, how the depth and magnitude estimates shift, whether the
intensity grade is revised up or down, and how long after the origin the
parameters stop changing. You can also measure how often a first bulletin is
followed by a `CORRECTED` or `CANCELLED` one — an operational quality signal for
the feed itself.

**Shaking footprint versus source parameters.** Each bulletin lists the
prefectures that reported shaking and the strongest grade in each. That supports
a study of how far and how strongly shaking is reported as a function of
magnitude, depth, and source region — count of prefectures reporting, highest
grade reported, and the drop-off in grade across the affected set. The response
variable here is an *ordinal grade*, not a number, so this must be done with
ordinal methods (rank correlation, proportional-odds style models, contingency
tables). Treating the grade as a number will produce results that look fine and
are not.

**Source-region climatology.** After collapsing to one row per event, the
coordinates, depth, magnitude, and named area support the usual descriptive
work: event counts and depth/magnitude distributions per named source region,
and depth-versus-location structure. Note that the schema caps depth at 700 km,
which tells you the feed is expected to cover deep events, not only crustal ones.

**Tsunami-flag conditioning.** `tsunami_possible` is mandatory on every bulletin,
so you can measure how the flag co-varies with magnitude, depth, and source
region, and how often it is revised between serials. This is only sound if nulls
are handled explicitly (see §5) and if you dedupe to the *final* bulletin, since
an early flag may be withdrawn.

**Feed-quality monitoring.** Serial gaps, events whose chain never reaches a
terminal state, records missing an epicenter name or a magnitude, and
prefecture codes that appear or disappear over time are all directly observable
and are worth a standing dashboard. Missingness here is not random — it is a
statement about how mature the bulletin is.

## 3. Combination rules

**Intensity grades** (`max_intensity`, at both the record level and inside
`affected_prefectures`). These are labelled `1`…`4`, `5-`, `5+`, `6-`, `6+`, `7`.
They may be **compared and ranked**; they may **not** be differenced, summed, or
averaged. The `+`/`-` variants at 5 and 6 make it plain that the labels are
category names, not measurements — there is no quantity for which "5+" minus
"5-" has a value. The mean of a set of grades is undefined; the *maximum* of a
set of grades is well defined, because a maximum only needs an ordering. So
max-of-max across prefectures is legitimate; mean-of-max is not. Ranking rests
on the assumption that the enumeration is listed in increasing severity, which
the files do not state in words — I treat it as established by the label forms
themselves, but flag it in §5.

**Prefecture intensities specifically.** Each entry is already an aggregate — the
strongest grade observed somewhere in that prefecture. Aggregates of that kind
cannot be re-aggregated into a total: three prefectures at grade 4 do not make
anything "greater" than one prefecture at grade 4. You may count how many
prefectures reached a given grade; you may not add or average the grades. Also,
**absence from the list is not a zero**. There is no grade below `1` in the
scale, so a prefecture that felt nothing and a prefecture that was never
assessed are represented identically — by omission. Do not fill omitted
prefectures with a floor value.

**Magnitude.** The files give a bare number with no unit, no named scale, and no
statement of what physical quantity it is linear in. Two magnitudes may be
compared and ranked **only under the assumption that all records use one and the
same scale**, which the files do not assert — and `bulletin_type` shows that
several distinct bulletin products feed this stream, so the assumption is not
free. Summing magnitudes is meaningless under any reading. Averaging magnitudes
across events is a decision I decline to bless from these files alone: whether
an arithmetic mean of these numbers means anything depends on what the scale is
linear in, and the files do not say. Averaging the *successive magnitude
estimates for one event* across its own serials is separately wrong — those are
revisions of one quantity, and the correct summary is the last one, not the mean.

**Depth.** A length in kilometres, bounded 0–700, and the only unambiguously
ratio-scaled quantity in the record. It may be compared, differenced, averaged,
and binned across records. One caveat: the files do not state the reference
surface the depth is measured from, so depth is comparable *within* this feed
but not automatically against depths from any other source.

**Latitude and longitude.** Comparable and mappable. They may **not** be
differenced as if degrees were a distance: a degree of longitude is not a fixed
ground distance and shrinks toward the poles, so coordinate deltas are not
displacements. Averaging coordinates across events yields a rectangular centroid
that is not a spherical mean and that will sit in the wrong place for any
spatially spread set; use it only as a rough label, never as a location. The
files name no geodetic datum or reference frame, so these coordinates should be
treated as internally consistent and not as interchangeable with coordinates
from another source without a stated datum.

**Timestamps.** All three are absolute instants and may be differenced freely,
both within an event and across events, in either direction — this is what makes
the latency analysis sound. They may be ordered and binned. Averaging instants
is meaningful only as "mean time of day/date" and is rarely what you want;
averaging *differences* of instants (mean latency) is the well-formed operation.
Never difference a timestamp on one record against a timestamp on another record
*of a different kind* without saying so — `control_datetime` on one bulletin
minus `origin_datetime` on another bulletin of a different event is a number
with no referent.

**Serial.** An ordinal position **scoped to its `event_id`**. It may be compared
only against other serials carrying the same `event_id`, where it establishes
which bulletin is later. Across events it means nothing: serial 5 of one event
and serial 5 of another are not comparable, are not "the same stage", and their
difference is not a quantity. Never sum or average serials. The maximum serial
per event is a legitimate derived count ("how many bulletins this event
required"), subject to the gap question in §5.

**Identifier and category strings** — `event_id`, `report_id`,
`epicenter_area_code`, prefecture `code`, `info_type`, `bulletin_type`,
`detail_url`. All nominal. Equality and grouping only; no ordering, no
arithmetic, no averaging. `epicenter_area_code` (`290`) and prefecture `code`
(`400`, `410`, `300`) are digit strings that will silently coerce to integers in
most tools — do not let them, and do not compute on them. Whether those two code
sets even inhabit the same namespace is not determined by the files, so do not
join one to the other.

**`tsunami_possible`.** A three-valued field: true, false, and null. Counting
true is fine after deduplication; treating null as false is a substantive
decision the files do not authorise. Within one event the flag may change
between serials, so the event-level answer is the value on the surviving
bulletin, not the disjunction over the chain.

**Cross-record combination in general.** Before *any* aggregate over this stream,
collapse each `event_id` to a single bulletin — normally the highest serial —
and decide explicitly what to do with `CANCELLED` chains, which appear to
withdraw rather than update. Aggregating the raw stream weights events by how
many bulletins they happened to generate, which correlates with severity, and
therefore biases every result in a direction that looks plausible.

## 4. Time

Three timestamps are present, and they are not interchangeable.

**`origin_datetime` is the time axis of the thing described.** It is the instant
of the earthquake itself. Every question about seismicity — rates, inter-event
intervals, time-of-day patterns, clustering, before/after comparisons — must be
placed on this axis. It is also the only one of the three that is stable across a
revision chain in principle: the other two advance with each new bulletin, so
plotting events on them will smear a single earthquake across the timeline.

`report_datetime` and `control_datetime` are the time axis of the *bulletin* —
when the statement was made and when it was handled. They are the right axis for
studying the feed's own behaviour (latency, revision cadence, operational load)
and the wrong axis for studying earthquakes.

**Relation to civil time.** All three are absolute instants carrying an explicit
UTC offset in the example (`Z`), so each denotes an unambiguous point on the
global timeline and converts to any civil clock by applying that zone's offset
rules. They are not floating local times and must not be read as wall-clock
readings in some implied local zone. Consequently, differences between them are
true elapsed durations and are unaffected by daylight-saving transitions or zone
choice.

The files do **not** establish the local civil zone in which these events occur
or in which the bulletins are authored. Any "time of day" analysis therefore
requires you to choose and declare a zone; the data will not choose one for you,
and a time-of-day histogram built directly on the UTC values is a histogram of
UTC, not of local day and night. Whether the offset is always `Z` or merely
happens to be so in this one example is not established either.

Within the single example the three timestamps are ordered
origin ≤ report ≤ control, which is the only ordering that makes sense given what
they denote — but the files impose no constraint enforcing it, so validate rather
than assume, and expect the occasional inversion.

## 5. Ambiguities

**Whether a later bulletin fully supersedes an earlier one or amends it.**
Not determined, and this is the highest-stakes gap in the pair of files. Every
bulletin restates every parameter, which *suggests* full replacement, but
nothing says so. If bulletins were ever partial, "take the highest serial"
would silently drop fields. I am declining to decide this; it must be resolved
before building any event-level table.

**What `CANCELLED` withdraws.** Whether it retracts the whole event or only the
preceding bulletin is not determined. I decline to decide it. It changes event
counts directly.

**The ordering of the intensity grades.** The files never state that the
enumeration is ordered by severity. I am treating `1 < 2 < 3 < 4 < 5- < 5+ <
6- < 6+ < 7` as established by the label forms and their listed order — that is
a *strong inference*, not something the files assert, and I mark it as such. If
it is wrong, every ranking and every "maximum" in this document is wrong with it.

**Whether the record-level `max_intensity` is the maximum over
`affected_prefectures`.** In the example it is (top level `4`; prefectures `4`,
`3`, `2`). One example does not establish a rule. **Guess:** it is the maximum,
and the two are redundant. Do not rely on it — if you need the relation, verify
it across the corpus, because a mismatch may be meaningful (e.g. an intensity
observed outside the listed prefectures) rather than an error.

**Three different ways of saying "missing", with no stated distinction.**
Some fields may be absent but never null; `magnitude` may be absent *or* null;
`tsunami_possible` must be present but may be null. The files do not say whether
absent and null mean different things — "not yet determined" versus "not
applicable" versus "withheld". I decline to decide; treat the distinction as
unknown and preserve it rather than normalising nulls and absences together.

**What the magnitude scale is.** Not determined — no unit, no scale name, no
stated bounds. This blocks any principled averaging (see §3) and blocks
comparison against magnitudes from any other source.

**Whether all bulletin types report on the same scales.** `bulletin_type` has six
values, implying six distinct products, and the files say nothing about whether
they populate magnitude and intensity identically. I decline to assume they do.
Segment by `bulletin_type` before pooling.

**The `bulletin_type` value `VXSE5k`.** Its siblings all end in a digit; this one
ends in a letter. Whether it is a literal code, a wildcard, or a family
placeholder is not determined. I decline to decide.

**Code namespaces.** Whether `epicenter_area_code` and prefecture `code` share a
scheme, what the codes denote, and whether the code sets are stable over time
are all undetermined. There is no lookup table in the material, so codes cannot
be resolved to places at all — only the epicenter's *name* is given, and only in
one language, and only when present.

**Reference frames.** No geodetic datum for the coordinates and no reference
surface for depth. Both are undetermined; both matter the moment you join to
anything external.

**Serial semantics.** Whether serials start at 0 or 1, increment by exactly one,
and never repeat is not determined. The example jumps straight to 2 with no
serial-1 record present in the material. Do not infer "number of bulletins" from
the maximum serial without checking.

**Uniqueness.** Nothing states that `report_id` is unique, that `(event_id,
serial)` is unique, or that a prefecture code appears at most once in
`affected_prefectures`. Deduplicate defensively.

**Empty and absent prefecture lists.** The list is mandatory but may evidently be
empty, and no minimum is imposed. Whether "empty" means "no shaking reported"
or "not yet assessed" is not determined — and given that revision chains exist,
both readings are plausible at different serials.

**Granularity floor.** The record is closed and carries intensity only at
prefecture level. Sub-prefecture or station-level analysis is not possible from
this feed; the per-bulletin `detail_url` may carry more, but nothing in the
material describes what is behind it, so I decline to assume it does.

**Feed completeness and delivery order.** Nothing establishes that the stream
contains every bulletin, arrives in order, or arrives at all for every event.
Treat gaps as unexplained rather than as absence of events.

**Retention of the event key across time.** `event_id` is 14 digits and in the
example equals `origin_datetime` rendered as `YYYYMMDDhhmmss`; `report_id` is
that key with `_2` appended. Both are single-example observations, not stated
rules. **Guess:** the composition is as it appears. Do not parse a time out of
`event_id` in production code on the strength of it — use `origin_datetime`,
which is typed as a timestamp and means what you need it to mean.
