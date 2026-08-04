<!-- regenerate: off (set to off if you edit this file) -->

# JSON Structure: Semantic and Reference-System Annotations

This is the working area for the individual Internet-Draft, "JSON Structure:
Semantic and Reference-System Annotations".

* [Editor's Copy](https://json-structure.github.io/semantic-annotations/#go.draft-vasters-json-structure-characteristics.html)
* [Datatracker Page](https://datatracker.ietf.org/doc/draft-vasters-json-structure-characteristics)
* [Individual Draft](https://datatracker.ietf.org/doc/html/draft-vasters-json-structure-characteristics)
* [Compare Editor's Copy to Individual Draft](https://json-structure.github.io/semantic-annotations/#go.draft-vasters-json-structure-characteristics.diff)


## Contributing

See the
[guidelines for contributions](https://github.com/json-structure/units/blob/main/CONTRIBUTING.md).

Contributions can be made by creating pull requests.
The GitHub interface supports creating pull requests using the Edit (✏) button.


## Scope and Non-goals

A quality of a value earns a keyword here when a consumer must know it to decide
whether two values may be combined or compared, and when it holds for the type
rather than varying from one instance to the next.

Scope:

* Defines optional annotations for observation-oriented semantics in JSON
	Structure schemas: `concepts`, `semanticRole`, `observedProperty`,
	`phenomenonTimeRelation`, `derivation`, `statistic`,
	`temporalReferenceSystem`, `cadence`, `coordinateReferenceSystem`,
	`vectorReferenceFrames`, `tensorReferenceFrames`, `frameTransforms`,
	`linearReferenceSystem`, `referenceRole`, `colorSpaces`, `audioChannels`,
	`spectralBands`, `codedValues`, and `measurementConditioning`.
* Covers roles for observation results, time semantics, quality,
	feature-of-interest variants, and observing procedure.
* Defines bindings for temporal, coordinate, vector-frame, tensor-frame, and
	linear reference systems, and for transformations between frames.
* Defines bindings for color spaces, audio channel layouts, spectral bands, and
	external code lists.
* Defines derivation, cadence, and measurement-conditioning annotations for
	result interpretation.

Non-goals:

* It is not a full ISO 19156 model or a normative JSON encoding of that model.
	It defines a role vocabulary laid over a record someone else designed, not an
	observation as a type to instantiate, classes for procedures or features, or
	relationships among observation entities. No record has to be shaped like an
	observation to carry these annotations.
* It does not define complete vocabularies for observed properties,
	procedures, quality values, or features of interest.
* It does not define identity or general relationship semantics
	(see JSON Structure Relations).
* It does not define units or conversion behavior
	(see JSON Structure Units).
* It does not define analytical procedures. It names summary functions but does
	not define what they compute, how gaps are treated, whether a window is
	inclusive, or whether a consumer may recompute a value.
* It does not define causal interpretation,
	execution policy, governance policy, or lineage policy.

Reference alignment:

* Observation concepts align with ISO 19156 and OGC Topic 20.
* Temporal terminology draws on ISO 19108, OGC Topic 25, ISO 19111 temporal
	CRS provisions, and GML 3.2.1 temporal schemas.


## Samples

[`samples/`](samples/) holds forty-three worked examples. Each directory contains a
`schema.struct.json` that declares the extension meta-schema
[`semantic-annotations-v0.json`](semantic-annotations-v0.json) and an `example.json`
instance that conforms to it. Run [`samples/validate-samples.ps1`](samples/validate-samples.ps1)
to check every schema, every instance, and every annotation.

Where a sample carries an `enum`, the meaning of each symbol is stated with
`altenums` from the [Alternate Names](../alternate-names/) extension — a
`lang:en` display label and a `description` sentence per symbol — rather than
packed into the description of the enclosing member.

Six of the real-world samples also carry a `schema-unannotated.struct.json`
holding the same record with the semantic layer removed, so that the two can be
read side by side. See
[what the annotations carry](samples/real-world/README.md#what-the-annotations-carry).

### Teaching samples

Fifteen samples introduce the annotations one theme at a time. See the
[samples README](samples/README.md).

| # | Directory | Theme |
|---|---|---|
| 01 | [`01-observation-basics`](samples/01-observation-basics/) | The core roles on one river gauging reading. |
| 02 | [`02-concepts-vocabulary`](samples/02-concepts-vocabulary/) | `concepts` on a type and on properties, covering all seven `kind` values. |
| 03 | [`03-sampling-features`](samples/03-sampling-features/) | The proximate and ultimate feature-of-interest chain. |
| 04 | [`04-temporal-roles`](samples/04-temporal-roles/) | `phenomenonTime`, `resultTime`, and a nested `effectiveTime`. |
| 05 | [`05-flattened-periods`](samples/05-flattened-periods/) | All four flattened boundary roles on two independent windows. |
| 06 | [`06-operational-times`](samples/06-operational-times/) | `scheduledTime`, `actualTime`, `ingestionTime`, and `status`. |
| 07 | [`07-forecasts`](samples/07-forecasts/) | `forecastIssueTime` and `forecastLeadDuration`. |
| 08 | [`08-status-and-quality`](samples/08-status-and-quality/) | `status` constrained by `enum`, and `resultQuality`. |
| 09 | [`09-derivation-and-statistic`](samples/09-derivation-and-statistic/) | Every `derivation` value, with the matching `statistic`. |
| 10 | [`10-phenomenon-time-relation`](samples/10-phenomenon-time-relation/) | All four `phenomenonTimeRelation` values. |
| 11 | [`11-cadence`](samples/11-cadence/) | `cadence` of kind `fixed`, `irregular`, and `onChange`. |
| 12 | [`12-temporal-reference-systems`](samples/12-temporal-reference-systems/) | `temporalReferenceSystem` against a published TRS and a meta-type. |
| 13 | [`13-coordinate-reference-systems`](samples/13-coordinate-reference-systems/) | CRS84 against EPSG:4326 axis order, plus a vertical system. |
| 14 | [`14-linear-reference-systems`](samples/14-linear-reference-systems/) | `linearReferenceSystem` against a route network and a meta-type. |
| 15 | [`15-station-network-telemetry`](samples/15-station-network-telemetry/) | A capstone that composes most of the annotations. |

### Real-world samples

Twenty-eight samples annotate schemas published by live open-data feeds and
standing reference datasets, one per domain and publisher. See the
[real-world README](samples/real-world/README.md).

| # | Directory | Source |
|---|---|---|
| 01 | [`01-ais-vessel-position`](samples/real-world/01-ais-vessel-position/) | aisstream.io AIS position reports |
| 02 | [`02-marine-buoy-observation`](samples/real-world/02-marine-buoy-observation/) | NOAA NDBC marine buoys |
| 03 | [`03-aerodrome-metar`](samples/real-world/03-aerodrome-metar/) | AviationWeather.gov METAR |
| 04 | [`04-lightning-stroke`](samples/real-world/04-lightning-stroke/) | Blitzortung lightning detection |
| 05 | [`05-earthquake-report`](samples/real-world/05-earthquake-report/) | JMA Bosai earthquake bulletins |
| 06 | [`06-solar-xray-flare`](samples/real-world/06-solar-xray-flare/) | NOAA SWPC GOES X-ray flares |
| 07 | [`07-grid-carbon-intensity`](samples/real-world/07-grid-carbon-intensity/) | National Grid ESO carbon intensity |
| 08 | [`08-public-power-generation`](samples/real-world/08-public-power-generation/) | Energy-Charts public power |
| 09 | [`09-orbit-mean-elements`](samples/real-world/09-orbit-mean-elements/) | CelesTrak orbital elements |
| 10 | [`10-transit-vehicle-position`](samples/real-world/10-transit-vehicle-position/) | SIRI real-time transit |
| 11 | [`11-route-travel-time`](samples/real-world/11-route-travel-time/) | NDW road travel times |
| 12 | [`12-bikeshare-station-status`](samples/real-world/12-bikeshare-station-status/) | GBFS bikeshare station status |
| 13 | [`13-weather-alert`](samples/real-world/13-weather-alert/) | US NWS CAP 1.2 warnings |
| 14 | [`14-marine-water-quality`](samples/real-world/14-marine-water-quality/) | King County water quality |
| 15 | [`15-pollen-forecast`](samples/real-world/15-pollen-forecast/) | DWD Pollenflug forecasts |
| 16 | [`16-transit-vehicle-hfp`](samples/real-world/16-transit-vehicle-hfp/) | HSL High-Frequency Positioning |
| 17 | [`17-usgs-instantaneous-value`](samples/real-world/17-usgs-instantaneous-value/) | USGS NWIS instantaneous values |
| 18 | [`18-mode-s-aircraft-report`](samples/real-world/18-mode-s-aircraft-report/) | Mode-S / ADS-B downlink reports |
| 19 | [`19-bmrs-generation-mix`](samples/real-world/19-bmrs-generation-mix/) | Elexon BMRS generation mix |
| 20 | [`20-goes-magnetometer`](samples/real-world/20-goes-magnetometer/) | NOAA SWPC GOES magnetometer |
| 21 | [`21-gcmt-moment-tensor`](samples/real-world/21-gcmt-moment-tensor/) | Global CMT moment tensor catalogue |
| 22 | [`22-ccsds-attitude-quaternion`](samples/real-world/22-ccsds-attitude-quaternion/) | CCSDS Attitude Parameter Message |
| 23 | [`23-kitti-sensor-alignment`](samples/real-world/23-kitti-sensor-alignment/) | KITTI lidar-to-camera calibration |
| 24 | [`24-fogra-characterization-patch`](samples/real-world/24-fogra-characterization-patch/) | ICC characterization registry, FOGRA51 |
| 25 | [`25-sensor-community-noise`](samples/real-world/25-sensor-community-noise/) | Sensor.Community noise and air quality |
| 26 | [`26-vatsim-pilot-position`](samples/real-world/26-vatsim-pilot-position/) | VATSIM pilot position reports |
| 27 | [`27-firms-modis-fire-detection`](samples/real-world/27-firms-modis-fire-detection/) | NASA FIRMS MODIS fire detections |
| 28 | [`28-broadcast-audio-frame`](samples/real-world/28-broadcast-audio-frame/) | ITU-R BS.2051 / ADM delivery frame |


## Schema comprehension evaluation

Every sample was put in front of an isolated language model (`GPT-5 mini`). Each
run received only two files — the sample's `schema.struct.json` and its
`example.json`, copied into a neutral sandbox with no repository, directory
names, or specification text — and was asked to propose the valuable analytics
dimensions the stream supports and why, then to flag any ambiguities and rate
its own confidence.

**Read the result as an observation, not as evidence.** The method has four
defects, and they are not incidental: the score is the subject's opinion of
itself, 40 of the 43 samples were run without an unannotated control, nothing
was blinded, and one model is one data point. What the run supports is that the
annotations are discoverable from the schema and get used. It does not support a
claim about how much difference they make, because for most samples nothing was
run without them.

What is worth reporting from it is not the confidence ratings but which
annotations the transcripts turned on, which is checkable:

* Agents used `temporalReferenceSystem` meta-types to *refuse* a mapping to UTC
	that the schema does not license, `coordinateReferenceSystem` to require
	axis-order and vertical-datum handling rather than assuming lat/lon,
	`vectorReferenceFrames`/`tensorReferenceFrames` to mark spacecraft-local
	components as not cross-comparable while treating the frame-invariant
	magnitude as comparable, `measurementConditioning` to recover A-weighting and
	the reference sound pressure, `codedValues` to plan registry joins against
	published code lists, and `spectralBands` to construct band-difference
	features.
* One transcript did the opposite and is more instructive: it reconstructed
	audio frame timing by dividing a frame counter by a member called
	`sample_rate`, a relation nothing in the schema stated. That is the failure
	mode the document is about, it went unremarked in the first write-up, and
	fixing it changed the specification and the sample rather than the
	evaluation.

Method, per-sample results, and the full list of caveats are in
[`EVALUATION.md`](EVALUATION.md). A controlled version — mechanically derived
rubric, an unannotated control arm for every sample, blinded grading by a
separate supervisor model, and a reported rate of positively wrong statements
per arm — is in [`evaluation/`](evaluation/), together with an account of what
it still cannot establish.


## Command Line Usage

Formatted text and HTML versions of the draft can be built using `make`.

```sh
$ make
```

Command line usage requires that you have the necessary software installed.  See
[the instructions](https://github.com/martinthomson/i-d-template/blob/main/doc/SETUP.md).
