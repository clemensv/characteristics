You are reading a data feed you have never seen before.

The directory you have been given contains exactly two files: a schema and one
example record that conforms to it. Read only those two files. You have no
network, no search, no other documents, and no access to any specification.

Produce, in this order:

1. **What this feed is.** What the records describe, in a few sentences.
2. **Analytics.** The analyses this stream supports that would be worth running,
   and for each one, why the data supports it.
3. **Combination rules.** For each quantity, state whether values may be
   compared, differenced, summed, or averaged across records, and under what
   condition. Where two values must not be combined, say so and say why.
4. **Time.** Which member establishes the time axis of the thing described, and
   how positions on that axis relate to civil time.
5. **Ambiguities.** Anything the two files leave open. For each, state plainly
   whether you are declining to decide it or guessing, and mark a guess as a
   guess.

Two rules govern the whole answer.

Do not invent facts about the domain that the two files do not establish. If
something is not in the files, either say it is not determined or mark your
answer as an assumption. Declining to answer where the files do not decide the
matter is a correct answer, not a failure.

Do not describe the files. Nobody wants an inventory of member names and types.
State what a person analysing this data would need to know and would get wrong
without you.


---

schema.json

```json
{
  "$schema": "https://json-structure.org/meta/extended/v0/#",
  "$id": "https://example.invalid/schema",
  "$uses": [
    "JSONStructureValidation"
  ],
  "name": "WaterQualityReading",
  "type": "object",
  "properties": {
    "station_id": {
      "type": "string"
    },
    "station_name": {
      "type": "string"
    },
    "sampled_depth_m": {
      "type": "double"
    },
    "basin": {
      "type": "string"
    },
    "sonde": {
      "type": "uri"
    },
    "observation_time": {
      "type": "datetime"
    },
    "published_time": {
      "type": "datetime"
    },
    "qc_flag": {
      "type": "string",
      "enum": [
        "pass",
        "not_evaluated",
        "suspect",
        "fail",
        "missing"
      ]
    },
    "water_temperature_c": {
      "type": "double"
    },
    "conductivity_s_m": {
      "type": "double"
    },
    "specific_conductivity_s_m": {
      "type": "double"
    },
    "pressure_dbar": {
      "type": "double"
    },
    "salinity_psu": {
      "type": "double"
    },
    "dissolved_oxygen_mg_l": {
      "type": "double"
    },
    "dissolved_oxygen_saturation_pct": {
      "type": "double"
    },
    "ph": {
      "type": "double"
    },
    "chlorophyll_ug_l": {
      "type": "double"
    },
    "chlorophyll_stddev_ug_l": {
      "type": "double"
    },
    "turbidity_ntu": {
      "type": "double"
    },
    "turbidity_stddev_ntu": {
      "type": "double"
    },
    "nitrate_umol": {
      "type": "double"
    }
  },
  "required": [
    "station_id",
    "station_name",
    "basin",
    "sonde",
    "observation_time",
    "published_time",
    "qc_flag"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "station_id": "kingcounty-marine-pointwells",
  "station_name": "Point Wells Marine Monitoring Mooring",
  "sampled_depth_m": 1.0,
  "basin": "Puget Sound - Main Basin",
  "sonde": "http://vocab.nerc.ac.uk/collection/L22/current/TOOL0872/",
  "observation_time": "2026-07-27T19:15:00Z",
  "published_time": "2026-07-27T19:38:41Z",
  "qc_flag": "pass",
  "water_temperature_c": 13.842,
  "conductivity_s_m": 3.1274,
  "specific_conductivity_s_m": 4.0186,
  "pressure_dbar": 1.04,
  "salinity_psu": 28.913,
  "dissolved_oxygen_mg_l": 8.42,
  "dissolved_oxygen_saturation_pct": 96.7,
  "ph": 7.86,
  "chlorophyll_ug_l": 4.31,
  "chlorophyll_stddev_ug_l": 0.62,
  "turbidity_ntu": 1.94,
  "turbidity_stddev_ntu": 0.28,
  "nitrate_umol": 12.7
}
```
