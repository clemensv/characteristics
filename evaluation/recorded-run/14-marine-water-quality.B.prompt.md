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


You also have the specification that defines the annotation keywords used by
this schema. It is the file `specification.md` in this same directory. Read it, and use it
to interpret any keyword you do not recognise. Where the specification states a
rule about what may or may not be inferred from a keyword, that rule governs
your answer.


---

schema.json

```json
{
  "$schema": "https://json-structure.org/meta/semantic-annotations/v0/#",
  "$id": "https://example.invalid/schema",
  "$uses": [
    "JSONStructureSemanticAnnotations",
    "JSONStructureAlternateNames"
  ],
  "name": "WaterQualityReading",
  "description": "A water-quality reading from a King County (Washington) marine monitoring mooring in Puget Sound, carrying the CTD, optical and nutrient channels published for one sampling cycle. Derived from the king-county-marine feeder schema published in the xRegistry catalogue; the upstream description text on that schema is a copy of the King County Metro water-taxi wording and does not describe this record, so it has been replaced with an accurate one.",
  "type": "object",
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/marine-water-quality/v1",
    "kind": "example-catalog"
  },
  "properties": {
    "station_id": {
      "type": "string",
      "description": "Stable bridge identifier for the buoy or mooring dataset. The mooring is the programme-level feature of interest: the station the monitoring programme reports against, distinct from the water parcel actually sampled and from the basin the result is interpreted for.",
      "semanticRole": "featureOfInterest",
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/identifier",
          "kind": "dcterms-property"
        }
      ]
    },
    "station_name": {
      "type": "string",
      "description": "Human-readable station name derived from the dataset title."
    },
    "sampled_depth_m": {
      "type": "double",
      "description": "Depth below the sea surface of the water parcel that the sonde package sampled in this cycle. The water parcel at this depth is the proximate feature of interest: it is the physical entity directly subjected to the measurement act, and it is not the mooring and not the basin.",
      "unit": "m",
      "symbol": "m",
      "semanticRole": "proximateFeatureOfInterest"
    },
    "basin": {
      "type": "string",
      "description": "Identifier of the marine basin or classified water body for which the reading is ultimately interpreted under the monitoring programme. The basin is the ultimate feature of interest and is not inferred from the mooring or from the sampled parcel.",
      "semanticRole": "ultimateFeatureOfInterest"
    },
    "sonde": {
      "type": "uri",
      "description": "Device-catalogue URI identifying the profiling sonde package and therefore the measurement procedure applied to the sampled parcel. Procedure identity is comparability-critical: readings from a different package are not interchangeable with these even where the property and the station agree.",
      "semanticRole": "observingProcedure"
    },
    "observation_time": {
      "type": "datetime",
      "description": "Observation timestamp normalized to UTC ISO 8601 form. This is the instant the stated conditions applied to the sampled water parcel. The mooring runs one sampling cycle every fifteen minutes, so the producer is expected to publish one record per station per quarter-hour slot.",
      "semanticRole": "phenomenonTime",
      "cadence": {
        "kind": "fixed",
        "period": "PT15M"
      }
    },
    "published_time": {
      "type": "datetime",
      "description": "Instant at which the reading became available from the shore-side data-processing system, after telemetry and automated quality control. It follows the observation time by minutes to hours and must not be read as the time the conditions applied.",
      "semanticRole": "resultTime"
    },
    "qc_flag": {
      "type": "string",
      "description": "QARTOD quality classification assigned to this reading by the automated quality-control procedure. It states how good the result is and is independent of the publication standing of the record.",
      "enum": [
        "pass",
        "not_evaluated",
        "suspect",
        "fail",
        "missing"
      ],
      "altenums": {
        "lang:en": {
          "pass": "Pass",
          "not_evaluated": "Not Evaluated",
          "suspect": "Suspect or Of High Interest",
          "fail": "Fail",
          "missing": "Missing Data"
        },
        "description": {
          "pass": "QARTOD flag 1: the value passed every applied test.",
          "not_evaluated": "QARTOD flag 2: no quality-control test was applied to this value.",
          "suspect": "QARTOD flag 3: the value failed a test that does not disqualify it, or is of high interest.",
          "fail": "QARTOD flag 4: the value failed a critical test and must not be used.",
          "missing": "QARTOD flag 9: no value is present."
        }
      },
      "semanticRole": "resultQuality"
    },
    "water_temperature_c": {
      "type": "double",
      "description": "Water temperature in degrees Celsius.",
      "unit": "Cel",
      "symbol": "°C",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_temperature",
        "kind": "cf-standard-name"
      }
    },
    "conductivity_s_m": {
      "type": "double",
      "description": "Electrical conductivity in siemens per meter, as read by the conductivity cell at the in-situ temperature and pressure.",
      "unit": "S/m",
      "symbol": "S/m",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_electrical_conductivity",
        "kind": "cf-standard-name"
      }
    },
    "specific_conductivity_s_m": {
      "type": "double",
      "description": "Specific conductivity in siemens per meter: the measured conductivity normalized to a reference temperature of 25 degrees Celsius by the standard temperature-compensation relation. The normalization is a deterministic calculation that no named summary function describes.",
      "unit": "S/m",
      "symbol": "S/m",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_electrical_conductivity",
        "kind": "cf-standard-name"
      }
    },
    "pressure_dbar": {
      "type": "double",
      "description": "Water pressure in decibar as published by the raw datasets.",
      "unit": "dbar",
      "symbol": "dbar",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_pressure",
        "kind": "cf-standard-name"
      }
    },
    "salinity_psu": {
      "type": "double",
      "description": "Salinity in practical salinity units, derived from the measured conductivity, temperature and pressure by the practical salinity scale relation. It is not read from a sensor of its own.",
      "unit": "PSU",
      "symbol": "PSU",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_practical_salinity",
        "kind": "cf-standard-name"
      }
    },
    "dissolved_oxygen_mg_l": {
      "type": "double",
      "description": "Dissolved oxygen concentration in milligrams per liter, read from the optode.",
      "unit": "mg/L",
      "symbol": "mg/L",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#mass_concentration_of_oxygen_in_sea_water",
        "kind": "cf-standard-name"
      }
    },
    "dissolved_oxygen_saturation_pct": {
      "type": "double",
      "description": "Dissolved oxygen saturation as a percentage, computed from the measured oxygen concentration and the solubility of oxygen at the concurrent temperature, salinity and pressure. It is a derived quantity rather than a sensor channel.",
      "unit": "P1",
      "symbol": "%",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#fractional_saturation_of_oxygen_in_sea_water",
        "kind": "cf-standard-name"
      }
    },
    "ph": {
      "type": "double",
      "description": "Measured pH value, reported on the total scale.",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_ph_reported_on_total_scale",
        "kind": "cf-standard-name"
      }
    },
    "chlorophyll_ug_l": {
      "type": "double",
      "description": "Chlorophyll fluorescence or chlorophyll concentration in micrograms per liter, read from the fluorometer.",
      "unit": "ug/L",
      "symbol": "µg/L",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#mass_concentration_of_chlorophyll_in_sea_water",
        "kind": "cf-standard-name"
      }
    },
    "chlorophyll_stddev_ug_l": {
      "type": "double",
      "description": "Standard deviation of chlorophyll fluorescence in micrograms per liter, summarizing the fluorometer burst taken within the sampling cycle. It carries the same observable property as the chlorophyll concentration and differs from it only in the summary function applied, so the two are not comparable as like quantities. The burst lies within the sampling cycle but its length is configured per deployment and is not published in this feed, so no `supportPeriod` is declared and the extent of the period the value characterizes is indeterminate from the record.",
      "unit": "ug/L",
      "symbol": "µg/L",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "standardDeviation",
      "phenomenonTimeRelation": "interval",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#mass_concentration_of_chlorophyll_in_sea_water",
        "kind": "cf-standard-name"
      }
    },
    "turbidity_ntu": {
      "type": "double",
      "description": "Turbidity in nephelometric turbidity units, read from the optical backscatter sensor.",
      "unit": "NTU",
      "symbol": "NTU",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_turbidity",
        "kind": "cf-standard-name"
      }
    },
    "turbidity_stddev_ntu": {
      "type": "double",
      "description": "Standard deviation of turbidity in nephelometric turbidity units, summarizing the optical backscatter burst taken within the sampling cycle. As with the chlorophyll standard deviation, the burst length is configured per deployment and is not published, so no `supportPeriod` is declared and the extent of the period is indeterminate from the record.",
      "unit": "NTU",
      "symbol": "NTU",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "standardDeviation",
      "phenomenonTimeRelation": "interval",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#sea_water_turbidity",
        "kind": "cf-standard-name"
      }
    },
    "nitrate_umol": {
      "type": "double",
      "description": "Nitrate or nitrate-plus-nitrite concentration in micromoles, read from the ultraviolet nitrate analyser.",
      "unit": "umol",
      "symbol": "µmol",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#mole_concentration_of_nitrate_in_sea_water",
        "kind": "cf-standard-name"
      }
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
