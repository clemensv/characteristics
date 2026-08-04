# 1. What this feed is

Each record is a single **pixel-level thermal detection**, not a fire. It says that at one instant, one satellite instrument looking at one roughly one-kilometre patch of ground saw a thermal anomaly, and reports where that patch was, how hot it looked in two infrared channels, and how much radiative power was coming out of it.

The unit of observation is therefore *(pixel × overpass)*. A single wildfire burning for a week will appear as many records; a single record tells you nothing about how long anything has been burning, whether it burned before, or whether it will burn again. There is no fire identifier, no event identifier, no burn-area member, and no member that links one record to another. Any notion of "a fire" is something the analyst constructs downstream by clustering; it is not present in the data.

The records are also **presence-only**. There is no record for "this pixel was observed and was not burning", and no record for "this pixel was not observed at all". The absence of a detection is not evidence of absence of fire.

---

# 2. Analytics this stream supports

**Spatial clustering into fire complexes.** Coordinates are pixel centres in a stated geodetic reference (WGS-84), so detections from one overpass can be grouped by proximity into contiguous burning areas. This is the primary analysis the data supports, and it is supported because the geometry is unambiguous: a defined datum, a defined point semantics (centre, not corner), and a stated nominal footprint scale to calibrate the clustering radius against.

**Total radiative power of a fire complex at an instant.** Fire radiative power is a power, i.e. an extensive rate quantity attached to a pixel. Summing it over the pixels of one cluster in one overpass yields the radiative power of that complex. This is the one genuinely additive quantity in the feed.

**Intensity screening using the two-band pair.** The schema declares both temperature members as sensor bands under a single brightness-temperature calibration, and states explicitly that the pair exists to screen false alarms and gauge fire intensity. The difference between the short-wave band and the long-wave band is therefore a first-class derived quantity, not an incidental arithmetic result: it separates a genuinely hot sub-pixel source from a merely warm background.

**Comparison of the same region between platforms.** The platform code is marked as the observing procedure, which is the schema's way of saying that two records from different platforms are products of two different measurement processes. Because platforms differ, records from different platforms sample the same ground at different times, which supports looking at how a fire changed between two looks — provided the platform difference is treated as a stratification variable and not averaged away.

**Rate-of-change of a complex between consecutive overpasses.** Given clustering plus per-overpass FRP totals, the growth or decay of a complex can be tracked. The support here is weaker than the above and is conditional: it holds only where the same ground was actually observed in both overpasses, which this feed does not tell you.

**What the data does *not* support, despite looking like it does:**

- **Detection-count time series as a measure of fire activity.** Counts confound fire activity with observation opportunity. Nothing in the records states which ground was viewed, when, how often, or whether the view was obstructed. A drop in counts is equally consistent with rain, cloud, an orbital gap, or a feed outage. Any count-based trend line is a sampling artefact until an independent coverage record is joined in, and no such member exists here.
- **Burned area.** No area member, and detection is not extent.
- **Total energy released.** See §3.
- **Quality-filtered analysis.** There is no confidence, quality-flag, day/night, scan-geometry, or footprint-size member. Any workflow that assumes such filtering is available will have to source it elsewhere.

---

# 3. Combination rules, quantity by quantity

### Brightness temperatures (the two infrared bands)

**Comparable and differenceable, within the same band.** Both are on the kelvin scale, which is an absolute-zero-anchored ratio scale, so differences between two values of the *same* band are physically meaningful, and both bands share a declared common calibration basis.

**The cross-band difference is meaningful and intended.** Subtracting the long-wave value from the short-wave value within a single record is the designed use of the pair.

**Never average the two bands together.** The arithmetic mean of a four-micrometre brightness temperature and an eleven-micrometre brightness temperature is not a temperature of anything. The units match; the quantities do not. Matching units are not a licence to combine — this is the single most likely mistake with this feed, because a naive "average all the kelvin columns" pipeline will silently produce a number.

**Never sum brightness temperatures, across bands or within one.** A sum of temperatures is not a temperature and is not an energy. Temperatures are intensive; they do not accumulate over pixels.

**Averaging a single band across pixels is arithmetically valid and physically treacherous.** The mean is a mean of the reported quantity and nothing more. The files establish no linear relation between brightness temperature and radiated energy, so a mean brightness temperature must not be reported or reasoned about as a mean fire intensity or a mean energy. If you want energy-like aggregation, use FRP, which is the member that carries that meaning.

**Do not treat these as the temperature of the fire.** They are pixel-integrated brightness temperatures over a roughly one-kilometre patch that is mostly not on fire. Comparing one pixel's value to another compares two mixtures, not two flames.

### Fire radiative power

**Summable — under three conditions, all of which the analyst must enforce and none of which the data enforces.**

1. *Same acquisition instant.* Summing power values taken at different times adds instantaneous rates that never coexisted. The sum is not the power of anything at any moment.
2. *Same platform.* The platform is marked as the observing procedure. The files do not establish that the two platforms are mutually calibrated, so cross-platform sums mix measurement processes without a stated equivalence.
3. *Non-overlapping pixels.* The files describe a nominal one-kilometre pixel but do not state that pixel footprints tile the ground without overlap, and the word *nominal* signals that the real footprint is not fixed. Where two detections overlap on the ground, summing double-counts the shared radiance. This is an assumption you are making, not a fact the files grant.

**Averageable, but say which average you mean.** A mean FRP over the pixels of a cluster is a mean per-pixel intensity. It is not the intensity of the fire, and it moves in the opposite direction from the total when a fire spreads at constant per-pixel intensity: the total rises while the mean stays flat. Reporting the mean where the audience expects the total is a real and common error.

**Do not sum FRP over time to obtain energy.** Power integrated over time is energy, but integration needs a duration, and no member gives one. Each record is a rate at an instant; the interval it represents, the instrument dwell, and the gap to the next overpass are all absent. Multiplying FRP by an assumed interval is an assumption about orbital revisit that this feed does not supply, and it must be labelled as such if done.

**Missing FRP is not zero.** FRP is the only measurement member that is not required. Whether it is absent because it could not be retrieved, because it fell below a reporting threshold, or for some other reason is not stated. Consequently:

- A sum computed by coalescing missing FRP to zero is biased low by an unknown amount.
- A mean computed over only the records that have FRP is a mean over a self-selected subset, and if absence correlates with weak fires the mean is biased high.
- The correct handling is to report the number of records lacking FRP alongside any FRP aggregate, so consumers can see the size of the hole. Neither choice of imputation is defensible from these files alone.

### Latitude and longitude

**Comparable; usable for bounds, ordering, and distance.** They are on a stated datum, so they are mutually consistent across records.

**Differenceable only locally, and never as plain scalars.** A degree of longitude is not a fixed ground distance; it shrinks toward the poles. A difference in degrees is not a distance and must not be used as one. Distance requires a geodetic computation.

**Never summable.** Angular coordinates have no additive meaning.

**Averageable only with care, and the result is not what most people assume.** An arithmetic mean of coordinates gives an unweighted point that is not a centre of mass of the fire — it is a centre of the *detections*, so it is pulled toward whichever part of the fire happened to be resolved into more pixels. It also breaks across the antimeridian, where naive averaging of longitudes places the result on the opposite side of the planet. If a representative point is wanted, an FRP-weighted centroid is more defensible, but note that this silently discards every record with missing FRP.

**Areal densities are not computable.** Power per unit area needs a footprint, and no per-record footprint is given. Dividing by an assumed one square kilometre is an assumption, and the schema's own word *nominal* warns against it.

### Product source

**Not established as interchangeable.** The source identifies the product a detection came from. The files do not state that two different sources are mutually calibrated, share processing, or have the same detection sensitivity. Records should be pooled across differing sources only after a decision has been made externally to treat them as comparable, and that decision should be recorded. Pooling them by default is not supported by these files.

### Platform code

**A stratification key, not a payload value.** Because it is marked as the observing procedure, it identifies which measurement process produced the numbers. It should appear in every group-by that touches a measured quantity, and it should never be dropped on the grounds that the numbers "are all in kelvin anyway".

---

# 4. Time

The time axis is set by the acquisition instant, which is marked as the time of the phenomenon — that is, the time the world was in the reported state, not the time a record was written, ingested, or published.

**It is an instant, not an interval.** There is no start, no end, no validity window, no duration. Every record is a point sample. The thing described — a burning patch of ground — has a duration; the record does not. Nothing in the data tells you when a fire began, when it stopped, or whether it was burning between two records.

**The axis is irregular and instrument-driven.** Positions on it are determined by when a satellite happened to be overhead, not by any regular cadence. Consequently the sequence of records for a location is not a time series in the usual sense: it cannot be resampled, interpolated, or differenced as though the sampling were uniform, and a gap on the axis carries no information about the world.

**Relation to civil time.** Instants are given in UTC and are explicitly zone-anchored, so they are directly and unambiguously orderable and differenceable across records without any conversion — this is the one part of the feed with no hidden traps. But *local civil time at the fire* is **not derivable from these files.** Civil time depends on the political time zone and daylight-saving rules in force at that place on that date, and none of that is present. Deriving an offset from longitude is an astronomical approximation of solar time, not civil time, and it will be wrong by hours in many jurisdictions. I decline to give a rule for local time: it requires an external time-zone database, and that dependency should be stated explicitly wherever local-time reporting is required.

This matters because the analyses people most want — diurnal fire behaviour, "afternoon burning peaks", agricultural burning schedules — are all local-time analyses, and they cannot be done from this feed without joining external data.

**Precision is not stated.** The example instant lands on a whole minute with zero seconds. Whether that reflects true minute-level resolution, truncation, or a coincidence is not determined. Do not build logic that depends on sub-minute ordering.

**There is no record time.** With only a phenomenon time and no ingestion or publication time, latency is invisible, late arrivals are undetectable, and no bitemporal or as-of reconstruction is possible. If a record is ever revised or superseded, nothing here would let you tell.

---

# 5. Ambiguities

**Declining to decide:**

- **What a missing FRP means.** Not retrievable, below threshold, suppressed, or something else — the files do not say, and the three possibilities imply different and incompatible imputation strategies. This must be resolved from outside the feed before any FRP aggregate is trusted.
- **Whether the platform code set is closed.** Two codes are offered as examples. The phrasing is explicitly illustrative, so an unrecognised code is a live possibility and consumers must not fail on one.
- **Whether the two named product sources are intercalibrated.** Not stated.
- **Which of the two candidate short-wave channels supplied the value**, or whether that choice can vary between records. The schema names a channel pair for that member and does not resolve it. Whether the two channels are interchangeable for analysis is not determined here.
- **Whether records are unique.** There is no key, no identifier, and no stated uniqueness constraint. Whether the same pixel-overpass can arrive twice, and how a consumer should deduplicate if it does, is not determined. Deduplicating on the full value tuple is a workaround, not a documented guarantee.
- **Whether records are ordered or complete.** Neither delivery order nor completeness is addressed.
- **Whether pixel footprints overlap.** Bears directly on the validity of FRP summation, and is left open.
- **Local civil time**, as above.

**Guesses and assumptions, marked as such:**

- *Assumption:* the unit tokens carry their conventional meanings — arc degrees, kelvin, megawatts. The unit vocabulary is referenced by the schema but its definitions are not included in the material available to me, so I am reading the tokens conventionally rather than authoritatively.
- *Assumption:* the FRP value is the radiative power at the acquisition instant rather than an average over some retrieval window. The description calls it a rate and attaches it to an instantaneous acquisition, which supports this reading, but a dwell-averaged interpretation is not excluded by the text.
- *Guess:* the reason FRP is the only optional measurement is that its retrieval can fail where the two temperatures still succeed, i.e. it is a derived product downstream of them. This is inference from the required-set alone and should not be relied upon; it is offered only because it makes the missing-FRP handling question concrete.
- *Assumption:* records are additive event notifications rather than revisions of prior records, so a consumer can append rather than upsert. Nothing states this; nothing contradicts it either, and there is no key on which an upsert could be performed.

**Not ambiguous, and worth stating because it is often assumed to be:** the coordinates are unambiguously pixel *centres* on a stated datum, so no corner-versus-centre correction is needed and no datum shift should be applied. Extra members are prohibited by the schema, so a record carrying unexpected fields is invalid rather than merely unusual — a consumer that silently passes such records through is not conforming.
