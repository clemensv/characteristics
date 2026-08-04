# FIRMS MODIS active-fire detections — analyst's briefing

## 1. What this feed is

Each record is **one observation of one pixel by one instrument on one overpass**, not one fire. The schema is explicit that the record is an "active-fire pixel detection" and that the geometry is "the centre of the nominal one-kilometre fire pixel" — so the unit of observation is a footprint on the ground that the sensor judged to contain fire at the moment it looked. A large fire produces many records in the same overpass; several unrelated ignitions inside one footprint produce one record; and a fire that burns for a week produces records only at the instants a satellite happened to be overhead.

The payload carries a location, two brightness temperatures (a ~4 µm channel and a ~11 µm channel), a fire radiative power in megawatts, the UTC instant of acquisition, a satellite platform code, and a product identifier. That is the whole record — the schema forbids additional properties, so there is nothing else arriving that you might key on.

The single most consequential property of this feed is that **it is a detections-only stream**. There is no record type meaning "looked here, saw nothing," and no record type meaning "did not look here." Absence of a record is therefore uninterpretable from the feed alone: it may mean no fire, no overpass, or an observation that failed some upstream screen. Every denominator you might want — fires per unit area, detection rate, fraction of a region burning — is unavailable, because the feed gives you numerators only.

## 2. Analytics worth running

**Spatio-temporal clustering of pixels into fire complexes.** Latitude, longitude and acquisition instant together support grouping co-located, contemporaneous detections into candidate fire objects, and then tracking those objects across successive overpasses. This is supported because the three fields fully locate each detection in space and time; it is *necessary* rather than optional, because per-record analysis will systematically mistake fire size for fire count.

**FRP-weighted intensity per cluster, per region, per overpass.** Fire radiative power is a rate of radiative energy release attributed to the pixel, and the schema states its unit. It is the only member on the record that is plausibly additive over disjoint footprints, which makes "total FRP observed in this region on this overpass" the natural intensity index. Note the qualifiers in section 3 before summing anything.

**The two-channel temperature contrast.** The schema states the ~4 µm and ~11 µm brightness temperatures are "paired ... to screen false alarms and gauge fire intensity." Their difference is therefore the intended discriminator and is worth carrying as a derived column alongside FRP. Whether upstream screening has *already* been applied to this feed is not stated; see section 5.

**Diurnal structure via local solar time.** Longitude is on every record and the timestamp is UTC, so local solar time is derivable arithmetically (UTC hour plus longitude ÷ 15). This is a genuine analysis the data supports without external inputs. It is also a trap: what you will actually be measuring is the *overpass* clock, not the fire's clock, unless you first establish the sampling cadence empirically from the timestamps themselves.

**Per-platform and per-product agreement and cross-check.** Because `satellite` and `source` are on every record, you can compare what different platforms and products report for the same place and near-same time. Do this as a *diagnostic* — to characterise how the streams differ — before doing it as a *measurement*, because the files do not establish that the streams are interchangeable.

**Persistence and re-detection.** Repeated detections near the same coordinates across overpasses give a duration-of-activity signal. Use a spatial tolerance, not coordinate equality: the schema gives pixel centres, not cells of a fixed named grid, and nothing establishes that the same ground location yields the identical coordinate pair on a later overpass.

**Feed-health monitoring.** `frp` is the one non-required member. Tracking its missing rate, and tracking gaps in acquisition times per platform, is worth doing continuously — both directly affect whether any of the above is valid on a given day.

## 3. Combination rules

**Fire radiative power (`frp`, megawatts).** A rate attached to a footprint, so it is extensive in area: **summable across distinct pixels observed in the same overpass**, and differenceable and comparable between records. Conditions and prohibitions:

- Do not sum across platforms or products for the same time window without deduplicating. Two satellites can see the same ground at nearby times; the files give no detection identifier and no linkage between records, so the feed cannot tell you whether two records are two fires or one fire seen twice. Deduplication must be positional and is therefore approximate.
- Do not sum FRP across time and call the result energy. FRP is a power; integrating it requires a duration per sample, and no member gives one. Summing a Monday value and a Tuesday value yields megawatts, not megawatt-hours, and it is not a bigger fire — it is the same fire counted twice.
- Averaging FRP is legitimate but answers a narrow question ("mean intensity of a detected pixel"), and is biased by the detection threshold, which is not described. Prefer medians and quantiles; the distribution's shape is not established by these files, so do not assume a mean is representative.
- Because `frp` is not required, a missing value is **not zero**. Sums must be reported alongside the count of contributing records, or they silently vary with completeness.

**Brightness temperatures (`brightness`, `bright_t31`).** Both are intensive — properties of the radiation from a footprint, not amounts of anything.

- **Never sum them.** A sum of brightness temperatures has no meaning.
- Differences and comparisons are valid *between records that are on the same scale*. Their **unit is not stated by the schema** — only the channel and wavelength are. The instance values (331.7, 295.4) are consistent with kelvin, but that is my inference, not something the files establish.
- The consequence: `brightness − bright_t31` **within a record** is safe, because a temperature difference is the same number in kelvin or degrees Celsius. Comparing that difference across records is safe for the same reason. But **ratios of these values, and any statistic that depends on where zero sits, are not safe**, because they change meaning depending on which scale is in use and the files do not fix the scale.
- Averaging brightness temperatures across pixels is arithmetically possible but should be area- or count-weighted deliberately and interpreted as "typical observed pixel temperature," never as the temperature of a fire. A radiometrically meaningful aggregate would require the pixel footprint areas, which are not on the record.
- Do not compare `brightness` against `bright_t31` as though they were the same measurement: they are different channels, and the schema treats them as a pair to be contrasted, not as interchangeable readings.

**Latitude and longitude.** Comparable, and differenceable as displacements with the usual spherical caveats.

- Arithmetic means of latitude and longitude are **not** a centroid. They fail across the antimeridian and distort near the poles; if you need a centre, average unit vectors and convert back.
- Any positional average is weighted by detection density, which is itself an artefact of sampling — so a "mean fire location" is a statement about where the satellite looked at least as much as where things burned.
- Do not treat the stated precision as accuracy. Four decimal places is roughly ten metres; the schema describes a **nominal one-kilometre** pixel and gives the *centre*, not the fire's position within it. Sub-kilometre spatial inference is unsupported. How much the true footprint departs from the nominal kilometre is not established here.
- Summing coordinates is meaningless.

**`satellite` and `source`.** Categorical labels; only equality comparison. They must be carried through every aggregation as grouping keys, because they are the only handle you have on which sampling regime produced a number. Pooling across them without first showing they agree is the most likely way to produce a wrong answer from this feed.

**Counts of records.** Countable, but they are counts of *detected pixels*, not of fires and not of area. Comparing counts between regions, days, or platforms compares observing opportunity as much as fire activity, and the feed supplies nothing with which to normalise that away.

## 4. Time

`acq_datetime` is the only temporal member and it establishes the axis. It is described as the **UTC acquisition instant of the overpass** — that is, the moment the *instrument observed*, not a property of the fire. This distinction is the whole of the section:

- The record carries **no valid-time interval** for the burning. There is no ignition time, no extinction time, no observation window, no duration. A fire's timeline can only be reconstructed as the envelope of the instants at which it happened to be detected, and that envelope is bounded by overpass opportunity, not by the fire.
- There is no ingest, receipt, or publication timestamp. **Latency is not measurable from the feed**, and you cannot distinguish "arrived late" from "detected late." If you need latency, you must stamp arrival yourself at the boundary.
- Positions on the axis are absolute UTC instants, so they are directly orderable and differenceable across all records regardless of platform or product — this is the one quantity that combines without qualification.
- Mapping to civil time requires a time zone you must supply from outside the feed; nothing on the record identifies one. For diurnal analysis, **local solar time** is preferable and is derivable in-feed from longitude, as noted above.
- The schema types this member as a plain string and describes it as "ISO-8601 form" in prose only. There is no format constraint and no declared pattern, so the serialisation is not guaranteed to be stable — trailing `Z` versus a numeric offset, presence or absence of fractional seconds. Parse defensively rather than by string slicing, and normalise to an instant before comparing.
- The example instant is at whole minutes with zero seconds. Whether the feed's timestamps are quantised to the minute, or that is a coincidence of one record, is not determined by a single instance — I would not build sub-minute logic on it.

## 5. Ambiguities

**Unit and scale of the two brightness temperatures — declining to decide.** The schema names the channels and wavelengths but never states kelvin or degrees Celsius, and the validation extension is declared without any constraint being used. My reading of the instance values as kelvin is a **guess** and I have kept every rule in section 3 robust to being wrong about it.

**Whether upstream false-alarm screening has already been applied — declining.** The schema says the temperature pair is used "to screen false alarms," but does not say whether this feed contains screened output, unscreened candidates, or a mixture. There is no confidence, quality, or version member, and additional properties are forbidden, so nothing on the record can settle it. This matters: it decides whether you may take a detection at face value.

**Detection threshold and minimum detectable fire — not determined.** Nothing in the files states what it takes for a pixel to appear here. Every distributional statement about FRP is therefore conditional on an unknown truncation.

**Actual pixel footprint — declining.** The schema's own word is "nominal." Whether footprints vary, and with what, is not established, and there is no scan/track dimension on the record. Consequently pixel *area* is unavailable, which rules out area-normalised intensities and any conversion of FRP to per-unit-area quantities.

**Comparability across `source` and across `satellite` — declining.** The schema gives `MODIS_NRT` as an example product and `T`/`A` as example platform codes but says nothing about calibration, threshold, or overpass-time equivalence between them. I will not assert they are poolable; I will not assert they are not. Treat this as a hypothesis to test empirically before pooling.

**The complete value domains — not determined.** "Such as `MODIS_NRT`" and "such as `T` ... or `A`" are illustrative. No enumeration is declared, so both fields must be handled as open sets and unknown values must not be silently dropped.

**Duplicate and revision semantics — declining.** There is no identifier, no sequence number, and no version. Whether the same detection can be delivered twice, and whether a later record ever supersedes an earlier one for the same pixel and instant, is unanswerable from these files. This is a real operational risk for any running FRP total; I would design the ingest to be idempotent on the tuple of product, platform, instant and coordinates, but that is a **defensive assumption**, not something the files license.

**Why `frp` is optional while the other measurements are required — not determined.** It could mean the retrieval sometimes fails, or that it is absent under some acquisition condition. The distinction matters for whether missingness is ignorable, and the files do not decide it. Treat missing FRP as informative until shown otherwise.

**Coordinate reference and datum details beyond WGS-84 — partially determined.** The datum is stated for both coordinates; nothing states whether coordinates are ever wrapped, normalised, or bounded, since no range constraints are declared. Validate ranges yourself.

**Geographic and temporal extent of the feed — not determined.** One record from one place on one day says nothing about whether this stream is global or regional, continuous or windowed. Do not infer coverage from the sample.
