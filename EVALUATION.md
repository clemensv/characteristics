# Schema Comprehension Evaluation

This document records an empirical test of the central claim behind *JSON
Structure: Characteristics*: that the annotations make a schema **understandable
to a machine reader on its own**, without access to the specification, the
surrounding repository, or a human explaining the domain.

The test was run over **all 43 worked examples** in [`samples/`](samples/)
(15 teaching samples plus 28 real-world samples). Each sample was handed to an
isolated language model that saw nothing but the sample's own schema and one
example instance.

---

## 1. Method

### 1.1 Isolation

For every sample a fresh, empty sandbox directory `sNN/` was created outside the
repository. Exactly two files were copied into it:

| Sandbox file | Source |
|---|---|
| `schema.json`   | the sample's `schema.struct.json` |
| `instance.json` | the sample's `example.json` |

Nothing else was placed in the sandbox. The directory name was a neutral
`sNN` so that no domain hint leaked through the path. The agent was **not**
given:

* the specification draft or the meta-schema,
* the repository, its README files, or any sibling samples,
* the original file names (`schema.struct.json` / `example.json`) or the
  descriptive directory names (`20-goes-magnetometer`, …),
* web search, fetch, or any other tool.

### 1.2 The agent

* **Model:** `GPT-5 mini` — deliberately a small, general model rather than a
  frontier one, so the result measures what the *schema* conveys rather than
  what a large model already knows.
* **Runs:** 43 independent runs, one per sample, no shared state between runs.
* **Instruction (identical for every run):** read exactly the two files in the
  sandbox and nothing else; propose the valuable analytics dimensions the stream
  supports and why; flag ambiguities and assumptions; and finish with a
  self-assessed **confidence** rating and an explicit list of which
  **annotations** were used.

### 1.3 What was measured

1. Whether the agent could propose **domain-appropriate analytics** at all.
2. Its **self-rated confidence** (high / medium / low).
3. Which **annotations it named** as load-bearing — and, critically, whether the
   annotation changed the answer from a plausible guess to a *correct* one.

This is a comprehension probe, not a benchmark with a numeric score. The signal
is qualitative: *does the semantic layer carry enough for an uninformed reader to
reason correctly about the data?*

---

## 2. Headline results

| Metric | Result |
|---|---|
| Samples evaluated | 43 / 43 |
| High confidence | 40 |
| Medium confidence | 3 |
| Low confidence | 0 |
| Agents that named annotations as materially helpful | 43 / 43 |
| Agents that reported annotations as unhelpful ("none") | 0 / 43 |

The three medium ratings — `07-forecasts`, `22-ccsds-attitude-quaternion`, and
`28-broadcast-audio-frame` — were caution about genuine residual ambiguities in
the *payload*, not failures to understand the schema (see §5).

---

## 3. Per-sample outcomes

Confidence and the annotations each agent leaned on. "TRS", "CRS" abbreviate
temporal / coordinate reference system.

### 3.1 Teaching samples

| # | Sample | Conf. | Annotations the agent leaned on |
|---|---|---|---|
| 01 | observation-basics | high | `semanticRole`, `observedProperty` (CF), `unit` m, `qualityFlag` enum, `altenums` |
| 02 | concepts-vocabulary | high | `semanticRole`, `observedProperty`, `unit` mm, QUDT length, phenomenon/result time, feature-of-interest |
| 03 | sampling-features | high | `semanticRole`, `unit` mg/L, `qualityFlag` enum, observing procedure |
| 04 | temporal-roles | high | phenomenon / result / effective time roles, `unit` m, `warningLevel` enum |
| 05 | flattened-periods | high | `semanticRole`, `statistic` mean, `unit` µg/m³, AQI category, half-open `[start, end)` |
| 06 | operational-times | high | scheduled / actual / phenomenon / result / ingestion roles, `unit` µS/cm, `observedProperty`, run status |
| 07 | forecasts | **medium** | `derivation` modeled, `cadence` PT6H, `phenomenonTimeRelation` interval, `unit` m |
| 08 | status-and-quality | high | record status enum, quality grade, `unit` m, `observedProperty` (CF) |
| 09 | derivation-and-statistic | high | `derivation`, `statistic`, `phenomenonTimeRelation`, `unit` |
| 10 | phenomenon-time-relation | high | `phenomenonTimeRelation` (untilNext / accumulation), `statistic`, `unit` |
| 11 | cadence | high | `cadence` kind / period PT5M, `semanticRole`, enum, `altenums` |
| 12 | temporal-reference-systems | high | `temporalReferenceSystem`, OGC temporal CRS, meta-type position, units |
| 13 | coordinate-reference-systems | high | `coordinateReferenceSystem`, EPSG / CRS84 / EPSG:5703, coordinate axis order |
| 14 | linear-reference-systems | high | `linearReferenceSystem`, reference role, arm / chainage units |
| 15 | station-network-telemetry | high | most of the model — roles, `statistic`, `cadence`, CRS, `altenums` |

### 3.2 Real-world samples

| # | Sample | Conf. | Annotations the agent leaned on |
|---|---|---|---|
| 01 | ais-vessel-position | high | CRS EPSG:4326, `unit` `[kn_i]`, `cadence` irregular, `resultQuality`, sentinel codes |
| 02 | marine-buoy | high | `phenomenonTimeRelation`, `derivation`, `statistic`, `cadence`, CRS |
| 03 | aerodrome-metar | high | units, CRS (4326 / 5714 vertical), `cadence` PT1H, `statistic` |
| 04 | lightning-stroke | high | `semanticRole`, CRS 4326, `unit` m, `derivation` calculated, `resultQuality` |
| 05 | earthquake-report | high | `semanticRole`, `derivation`, `statistic`, CRS, bulletin type |
| 06 | solar-xray-flare | high | phenomenon start / end, `statistic` maximum, units W/m², J/m² |
| 07 | grid-carbon-intensity | high | `unit` gCO₂/kWh, `derivation` modeled / calculated, `cadence` PT30M, index enum |
| 08 | public-power-generation | high | `statistic` mean / sum, `phenomenonTimeRelation` interval, `unit` MW / % |
| 09 | orbit-mean-elements | high | `temporalReferenceSystem` meta-type, units, `derivation` modeled |
| 10 | transit-vehicle-position | high | CRS84, `cadence` PT30S, roles, `unit` deg |
| 11 | route-travel-time | high | `linearReferenceSystem`, `derivation` / `statistic`, `cadence` PT1M, `resultQuality` |
| 12 | bikeshare-station-status | high | phenomenon / result time, `cadence` onChange, `statistic` count, TRS |
| 13 | weather-alert | high | effective / phenomenon dual-time roles, severity / urgency / certainty enums |
| 14 | marine-water-quality | high | roles, `observedProperty`, `derivation`, `statistic`, `cadence`, QC flag |
| 15 | pollen-forecast | high | `derivation` modeled, forecast lead duration, `phenomenonTimeRelation` interval |
| 16 | transit-vehicle-hfp | high | `temporalReferenceSystem` meta-type, location enum, sign convention, `altenums` |
| 17 | usgs-instantaneous-value | high | `observedProperty`, `unit` `[ft_i]`, `cadence` PT15M, qualifier / exception enums |
| 18 | mode-s-aircraft-report | high | POSIX-millisecond epoch TRS, message-type enum, reserved squawks, `observedProperty` |
| 19 | bmrs-generation-mix | high | `unit` MW, `statistic`, `cadence`, phenomenon start, signed interconnectors |
| 20 | goes-magnetometer | high | `vectorReferenceFrames`, `unit` nT, `derivation`, `cadence` PT1M |
| 21 | gcmt-moment-tensor | high | `tensorReferenceFrames`, symmetry, components, UCUM unit, depth type |
| 22 | ccsds-attitude-quaternion | **medium** | `frameTransforms`, components, encoding, both frame meta-types |
| 23 | kitti-sensor-alignment | high | `frameTransforms`, rotation-matrix encoding, translation, frame meta-types |
| 24 | fogra-characterization-patch | high | `colorSpaces`, illuminant, observer, channels, UCUM unit |
| 25 | sensor-community-noise | high | `measurementConditioning` weighting / level reference, `statistic` min / max |
| 26 | vatsim-pilot-position | high | `codedValues` → ICAO Doc 8643 / Doc 7910, `kind` icao, WGS-84 |
| 27 | firms-modis-fire-detection | high | `spectralBands`, calibration brightness temperature, units K / MW |
| 28 | broadcast-audio-frame | **medium** | `audioChannels`, level reference full-scale, linear encoding, `sample_rate`, `temporalReferenceSystem`, `cadence` |

---

## 4. Where annotations drove correct, non-obvious reasoning

These are the cases where the agent reached a conclusion it could **not** have
reached from the raw field names and values alone — the annotation is what
supplied the missing semantics.

* **`12-temporal-reference-systems`** — read the `temporalReferenceSystem`
  meta-type and correctly *refused* to map an instrument beam clock onto UTC
  without an explicit synchronization relation.
* **`13-coordinate-reference-systems`** — proposed CRS **axis-order validation**
  and **vertical-datum transformation** directly from the
  `coordinateReferenceSystem` bindings, rather than assuming lat/lon order.
* **`09-orbit-mean-elements`** — treated the epoch's ordinal time as
  authoritative and the UTC field as a convenience rendering, matching the
  leap-second nuance the TRS meta-type encodes.
* **`20-goes-magnetometer`** — noted that the vector **components are
  spacecraft-local (`vectorReferenceFrames`) and therefore not comparable across
  satellites, while the magnitude is** — a frame-invariance argument straight
  from the annotation.
* **`21-gcmt-moment-tensor`** — decomposed the moment tensor while respecting
  `tensorReferenceFrames` and the declared symmetry.
* **`25-sensor-community-noise`** — inferred **A-weighting and the 20 µPa
  reference sound pressure** from `measurementConditioning`, and warned against
  mixing weighting curves when aggregating.
* **`26-vatsim-pilot-position`** — proposed **registry joins against ICAO Doc
  8643 (aircraft types) and Doc 7910 (airports)** purely from
  `codedValues.reference` / `kind`.
* **`27-firms-modis-fire-detection`** — built a **band-difference** fire metric
  and a brightness-temperature calibration step from `spectralBands`.
* **`16-transit-vehicle-hfp`, `01-ais-vessel-position`,
  `17-usgs-instantaneous-value`** — surfaced local-datum, operating-day-clock,
  and receiver-scoped caveats that the reference-system and role annotations make
  explicit.

---

## 5. The three medium ratings

None of the mediums indicate the agent misread the schema; each is appropriate
caution about something the *payload itself* leaves open.

* **`07-forecasts`** — wanted ensemble spread / probability information that the
  instance genuinely does not carry. The forecast annotations were understood;
  the agent simply flagged what a deterministic forecast cannot tell you.
* **`22-ccsds-attitude-quaternion`** — read the scalar-last component order from
  the annotation but flagged quaternion **handedness / rotation sense** as an
  edge the sample record does not pin down.
* **`28-broadcast-audio-frame`** — flagged residual per-sample edge cases, yet it
  used `sample_rate` + `frame_index` to reconstruct frame timing
  (`seconds = frame_index / sample_rate`) and read full-scale normalization from
  the `levelReference` / `encoding` annotations. This is the sample where an
  earlier revision was ambiguous about timing; after `temporalReferenceSystem`,
  `cadence`, and an explicit `sample_rate` were added, the agent no longer flags
  missing sample-rate information — a direct confirmation that the added
  annotations closed the gap.

---

## 6. Interpretation and caveats

**What this shows.** Even a small, general model, fully isolated, could interpret
all 43 schemas well enough to propose sound analytics — 40 of 43 at high
confidence and none at low — and in every case named specific annotations as the
thing that made the data legible. In the reference-system, coded-value, and
conditioning cases the annotation is what produced the *correct* answer
(comparability rules, registry joins, frame invariance, weighting) instead of a
plausible-sounding guess. The semantic layer is therefore both **self-describing**
(a reader can discover what it means from the schema) and **load-bearing** (it
changes the analytical conclusion).

**Caveats.**

* This is a comprehension probe, not a scored benchmark; "confidence" is the
  agent's own self-assessment.
* A single small model was used; results will vary with model and prompt. The
  choice of a small model is deliberate — a frontier model's prior knowledge
  would blur the line between what the *schema* conveys and what the model
  already knew.
* Isolation was enforced by sandboxing and instruction, not by a hardened
  sandbox; the neutral file and directory names were the main defense against
  domain leakage.
* Each sample was judged on its own; no cross-sample consistency was tested.

---

## 7. Reproducing the test

For each sample directory `D`:

1. Create an empty directory `S`.
2. Copy `D/schema.struct.json` → `S/schema.json` and
   `D/example.json` → `S/instance.json`.
3. Run a language model with tools disabled, instructing it to read only the two
   files in `S` and to (a) propose valuable analytics dimensions and why,
   (b) flag ambiguities and assumptions, and (c) end with a confidence rating
   and a list of the annotations it used.
4. Record the confidence and the named annotations.

Delete the sandbox directories when finished; they contain only copies of the
sample files.
