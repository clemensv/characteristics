# 1. What this feed is

Each record is one sampling cycle of a fixed marine monitoring mooring operated by
King County, Washington, in Puget Sound. A cycle produces a bundle of CTD, optical
and nutrient channels — temperature, conductivity and its 25 °C-normalised
counterpart, pressure, salinity, dissolved oxygen as concentration and as
saturation, pH, chlorophyll, turbidity, and nitrate — plus two within-cycle
variability figures for the optical channels.

The record separates three subjects that a consumer will otherwise conflate. The
mooring is the programme-level feature the results are reported against. The water
parcel at the stated depth is the thing actually measured. The basin is the water
body the result is ultimately interpreted for. None of the three is derivable from
either of the others, and the schema says so; a query that groups by station and
calls the answer a basin figure, or that treats two stations in one basin as
observations of the same parcel, is combining different subjects.

One further identity carries the same weight: the sonde package URI is the
measurement procedure. Two readings of the same property at the same station and
depth are not interchangeable if they came from different packages.

# 2. Analytics

**Time series at a station and depth.** Every scalar channel is a point value
stamped with the instant it applied, at a declared quarter-hourly rhythm. That
supports trend, diel cycle, seasonal cycle, and threshold-crossing work at a
single station — provided the series is cut by depth and by sonde, not just by
station.

**Publication latency.** The record carries the instant the conditions applied and
the instant the shore system published, as two separate, distinctly-typed roles.
Their difference is a clean, per-record measure of telemetry-plus-QC delay (23 m
41 s in the example), and its distribution by station, by sonde and by quality
class is directly computable. Nothing else in the feed measures pipeline health.

**Quality-conditioned availability.** The QARTOD class is enumerated with its
codes' meanings attached, including one class that means "must not be used" and
one that means "never tested". Counting records by class per station per period
gives instrument-health and QC-coverage statistics, and is the necessary
precondition for every other analysis here.

**Within-cycle variability.** The two standard deviations are the only evidence in
the feed about behaviour *between* the quarter-hourly stamps. High chlorophyll or
turbidity variance within a burst is a usable signal of patchiness, resuspension,
bubbles or biofouling, and it is usable *relative to itself over time at one
deployment*. It is not usable as a variance in the statistical sense across
records, because the burst length is not published.

**Internal-consistency checking.** Three channels are declared calculated rather
than measured: specific conductivity from conductivity and temperature, salinity
from conductivity, temperature and pressure, and oxygen saturation from oxygen
concentration and the concurrent temperature, salinity and pressure. Recomputing
each from its stated inputs is a real QC test — a divergence indicates a
processing fault. What it is *not* is corroboration: agreement between salinity
and conductivity, or between oxygen concentration and oxygen saturation, is
arithmetic, not two independent instruments agreeing.

**Basin-level roll-up.** The programme's own interpretation target is the basin,
and each record declares its basin explicitly, so aggregation to basin is the
intended use. But the feed supplies no coordinates, no basin geometry and no
station weights, so any basin figure is an unweighted mean of whichever moorings
reported, and its representativeness is the consumer's assumption.

**What the feed cannot support.** Spatial interpolation or mapping of any kind:
there are no coordinates in the record. Stratification profiles: one depth per
record, and no guarantee that a station reports more than one. Flux or load
calculations: no discharge, no volume, and nothing here is an accumulated
quantity.

# 3. Combination rules

**The grouping key for any cross-record combination is station, sonde, depth, and
quality class.** Station identifies the feature; sonde identifies the procedure and
is comparability-critical; depth identifies the water parcel actually measured, and
a different depth is a different parcel, not a different reading of the same one.
Values whose quality class is `fail` must be excluded outright, and `not_evaluated`
must not be pooled with `pass` as though it were equivalent, since it asserts only
that nothing was checked.

With that key held fixed:

| Quantity | Compare | Difference | Sum | Average |
|---|---|---|---|---|
| water temperature | yes | yes | no | yes |
| conductivity (in situ) | yes | yes | no | yes |
| specific conductivity (25 °C) | yes | yes | no | yes |
| pressure | yes | yes | no | yes |
| salinity | yes | yes | no | yes |
| dissolved oxygen, mg/L | yes | yes | no | yes |
| dissolved oxygen, % saturation | yes | yes | no | yes |
| pH | yes | as a log ratio | no | not as a plain mean |
| chlorophyll | yes | yes | no | yes |
| turbidity | yes | yes | no | yes |
| nitrate | yes | yes | no | unit ambiguity first — see §5 |
| chlorophyll std. deviation | trend only | no | no | no |
| turbidity std. deviation | trend only | no | no | no |

Nothing in this feed may be summed. Every scalar channel is an intensive state
variable observed at an instant; none is an accumulation over a period, and a total
of temperatures, salinities or oxygen concentrations is not a quantity.

**Averages are averages of samples, not of time.** Every scalar channel is declared
to apply *at* the observation instant, not to hold until the next reading. A
consumer computing "mean daily oxygen" or "hours below a threshold" by treating
each value as valid for its fifteen-minute slot is asserting a step-function
semantics the feed explicitly does not declare. The declared cadence does not
license filling a gap either: an absent slot is absent, and an unweighted mean over
present records is biased toward whatever times the mooring was reporting.

**Pairs that must not be combined:**

- *Chlorophyll and its standard deviation; turbidity and its standard deviation.*
  Each pair shares a unit and the same observable-property reference and differs
  only in the summary function applied. They are not like quantities. They must not
  be differenced, ratioed as if commensurate, or fed into one series.
- *The two standard deviations across records.* The burst they summarise lies
  inside the cycle but its length is set per deployment and is not published, so
  the extent of the period each value characterises is indeterminate. Two such
  values may not be pooled, weighted, or combined into a longer-window variance,
  because the number of underlying samples is unknown. Watching one deployment's
  series rise or fall is legitimate; arithmetic across deployments is not.
- *Conductivity and specific conductivity.* They carry the same observable-property
  reference and the same unit, so a naive join will treat them as one quantity.
  They are referenced to different temperatures — in situ versus 25 °C — and are
  therefore different quantities. Do not difference them, do not substitute one for
  the other when the other is absent, and do not concatenate them into one series.
- *Anything across differing sonde values.* Turbidity in NTU and chlorophyll from a
  fluorometer are the clearest cases: both are instrument-defined optical scales,
  and equality of the declared property does not make two packages' numbers
  interchangeable. Even where the sonde URI is equal, that is grounds for grouping,
  not proof of statistical interchangeability across a recalibration.
- *Anything across differing depth, or with depth absent.* Depth is optional in
  this schema. A record without it cannot be placed in a depth-conditioned series
  at all, and must not be assumed to sit at the station's usual depth.

**pH** is a logarithmic quantity. Its differences are meaningful as log ratios of
activity; an arithmetic mean of pH is not the pH of the mean hydrogen ion activity.
That is chemistry rather than something the two files establish, so I mark it as
general knowledge, but the files give no unit and no basis for treating pH as an
ordinary linear scale either.

**Oxygen concentration and oxygen saturation** are not independent. Do not treat
their agreement as a cross-check, and do not build a model that regresses one on
the other; the second was computed from the first.

# 4. Time

The time axis of the phenomenon is the observation timestamp. It is the instant at
which the stated conditions applied to the sampled water parcel, and it is the only
member that places the *thing described* on a time line.

It is a Core datetime with no temporal reference system declared, which means it is
read under ordinary civil-calendar semantics; the description states it is
normalised to UTC and the example carries a `Z` offset. Positions on this axis are
therefore directly civil-time instants requiring no transformation, and they order
forward. Local solar or civil time for Puget Sound differs from these stamps by the
Pacific time offset, which the feed does not carry; a diel analysis must supply it
from outside. (The time zone is my general knowledge, not a fact these two files
establish.)

The publication timestamp is *not* the time axis. It records when the reading
became available after telemetry and automated QC, follows the observation by
minutes to hours, and must never be read as when the conditions held. Sorting or
windowing a series by publication time reorders the phenomenon.

The observation timestamp declares a fixed fifteen-minute cadence. That is an
expectation about producer behaviour, not a constraint on the data and not a
property of any value. It does not assert that every quarter-hour slot has a
record, that records arrive in order, that a successor exists, or that a value may
be interpolated where none was recorded. A stream that misses a beat is late, not
malformed. What the cadence legitimately does is size a window, set a staleness
threshold, and make an absent slot detectable as a gap rather than absorbed
silently — all consumer-side decisions.

Every scalar channel is a point on that axis. The two standard deviations are the
exception: they characterise an interval rather than an instant, and that interval
is stated to lie within the sampling cycle but is otherwise unlocated and of
unknown length. Their position on the time axis is therefore known only to within
the cycle.

The example stamp falls exactly on a quarter hour. Phase alignment is not
guaranteed by anything in the files; only the period is declared.

# 5. Ambiguities

**Which channel a non-`pass` flag refers to.** There is one quality value and it
qualifies every result in the record jointly. When a record is `suspect`, nothing
recovers which of the fifteen channels was suspect. *Declining to decide* — this
must be resolved with the producer, and until it is, a non-`pass` record has to be
excluded wholesale rather than partially.

**What `missing` means when values are present.** The class is documented as "no
value is present", but every value member is optional, so absence is already
expressible structurally. Whether `missing` means the whole cycle failed or one
channel did is *not determined*. Declining.

**Nitrate: unit and analyte.** Two separate defects. The declared unit is an amount
of substance, µmol, while the description calls the value a concentration; those
are not the same thing and the feed does not reconcile them. My *guess*, marked as
a guess, is that µmol/L is intended, since that is the common marine convention —
but I am not willing to rely on it, and nitrate values here cannot be compared with
any external dataset until the producer states the denominator. Separately, the
description says "nitrate or nitrate-plus-nitrite" while the property reference
names nitrate alone. Those are different quantities for any budget or ratio work.
*Declining to decide* which is published.

**Chlorophyll: fluorescence or concentration.** The same defect. The property
reference names a mass concentration; the description offers "fluorescence or
concentration" as alternatives. The value is declared *measured* rather than
calculated, which leans toward the raw fluorometer reading rather than a
calibration-fitted concentration — but that is my inference from the derivation
annotation, not something the files state. *Declining to decide.* The consequence
is real: raw fluorescence and calibrated chlorophyll are not comparable across
instruments even at identical stated units.

**Pressure: absolute or gauge.** Not stated; the description only says "as
published by the raw datasets". The example value of 1.04 dbar alongside a 1.0 m
depth is consistent with in-situ sea pressure rather than absolute pressure. That
is a *guess* from one sample and I mark it as such; a single instance is not a
definition.

**How depth is obtained, and whether it is stable.** Depth carries no derivation
annotation, so whether it is a nominal deployment depth, a measured value, or a
figure derived from the pressure channel is *not determined*. If it is derived from
pressure, then depth and pressure are not independent facts about the record and
must not be used as though they were. Nor does anything establish that a station's
depth is constant over time; the description explicitly scopes it to "this cycle".

**Identifier registers.** Neither the station identifier nor the basin is bound to
any code list. They are free strings — the basin in the example is a human label
with spaces and a hyphen. Grouping by basin is therefore string matching on a label
that can drift between releases, and joining the station identifier to any external
station registry is not licensed by the schema. *Not determined*; treat both as
opaque and pin them against a producer-supplied list.

**Record identity and revision.** There is no record identifier, no publication
status, and no ingestion time. If two records appear for the same station and slot,
nothing in the feed says whether the later supersedes the earlier or duplicates it.
*Declining to decide* — this is a question for the producer's delivery contract.

**Which temperature-compensation and which pH convention.** Specific conductivity
is said to use "the standard temperature-compensation relation", which is not
identified; different relations give different numbers. pH is stated to be on the
total scale but nothing says at what temperature it is reported. Both *not
determined*.

**Extensibility is closed.** The record forbids additional properties, so the
missing facts above — burst length, deployment identifier, coordinates, per-channel
flags, the nitrate denominator — cannot arrive in the payload. They must come from
a separate channel, and any consumer design should assume that.

**A provenance caution.** The schema's own description records that the upstream
description it derives from was a mis-copied text describing an unrelated service,
and that it was replaced. The prose in this feed has already been wrong once. Where
the descriptions here are the only source for something — the nitrate denominator,
the chlorophyll analyte, the pressure reference — that history is a reason to
confirm rather than to rely.
