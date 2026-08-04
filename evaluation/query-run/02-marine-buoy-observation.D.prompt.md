You are handed a data feed you have never seen before, and asked to put it to
work.

The directory you have been given contains exactly two files: a schema and one
example record that conforms to it. Read only those two files. You have no
network, no search, no other documents, and no access to any specification.

Write **one** streaming SQL query, in the dialect of Azure Stream Analytics —
the same dialect the SQL operator of Microsoft Fabric Eventstream accepts — that
computes what you judge to be the **five most valuable derived metrics** this
stream supports.

A derived metric is computed, not carried. An aggregate over a window, a rate of
change, a difference between successive records, a ratio, a residual against a
declared reference, a flag raised by a threshold: those are derived. A field
copied from the record to the output is not, and does not count towards the
five.

Produce, in this order:

1. **The five metrics.** One line each: what it is, and why an operator of this
   feed would want it. Order them by how valuable you think they are.
2. **The query.** A single statement, using `WITH ... AS` for intermediate
   steps. It must:
   * declare the event time explicitly with `TIMESTAMP BY`, naming the member
     you have chosen and no other;
   * name the window type and size wherever it aggregates;
   * partition by whatever identifies an individual source, if anything does.
3. **What you did not compute.** Any aggregation, comparison or combination you
   considered and deliberately left out, and the reason. Be specific: name the
   members involved.
4. **Assumptions.** Anything the query relies on that the two files do not
   establish. Mark each one as an assumption.

Notes on the dialect, so that you are not judged on syntax you cannot look up.
`SELECT ... INTO output FROM input TIMESTAMP BY <member>` is the shape of a
statement. Windows are `TumblingWindow(minute, 5)`, `HoppingWindow(minute, 5, 1)`,
`SlidingWindow(minute, 5)` and `SessionWindow(minute, 5, 60)`, and appear in the
`GROUP BY`. `System.Timestamp()` is the end of the current window. `LAG(expr, 1)
OVER (PARTITION BY k LIMIT DURATION(minute, 10))` reaches the previous event and
the `LIMIT DURATION` is required. `DATEDIFF(second, a, b)` differences two
timestamps. The usual aggregates are available, including `STDEV` and
`PERCENTILE_CONT`. If you need something the dialect lacks, write plain SQL and
say in a comment that you are unsure it is supported.

Two rules govern the whole answer.

Do not invent facts about the domain that the two files do not establish. If the
files do not license an aggregation, do not write it. Choosing not to compute
something, and saying why, is a correct answer and is worth more than a metric
that looks impressive and is unsound.

Do not pad. Five metrics, not eight. A query that computes fewer things
correctly beats one that computes more things wrongly.


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
    "JSONStructureSemanticAnnotations"
  ],
  "name": "BuoyObservation",
  "description": "Real-time standard meteorological and oceanographic observation from an NDBC buoy, C-MAN station, or partner platform. Sourced from the NDBC latest_obs.txt composite file which is updated every five minutes. Fields cover wind, waves, pressure, temperature, dewpoint, pressure tendency, visibility, and tide. Derived from the noaa-ndbc feeder schema published in the xRegistry catalogue.",
  "type": "object",
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/marine-surface-conditions/v1",
    "kind": "example-catalog"
  },
  "coordinateReferenceSystem": {
    "reference": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "kind": "ogc-crs",
    "coordinates": [
      "latitude",
      "longitude"
    ]
  },
  "properties": {
    "station_id": {
      "type": "string",
      "description": "NDBC station identifier. Five-character alphanumeric code assigned by NDBC (e.g. '41001' for deep-ocean buoys, 'BURL1' for C-MAN stations). It identifies the observing platform whose surroundings are observed.",
      "semanticRole": "featureOfInterest",
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/identifier",
          "kind": "dcterms-property"
        }
      ]
    },
    "latitude": {
      "type": "double",
      "description": "Latitude of the observing platform in decimal degrees north. Negative values indicate southern hemisphere.",
      "unit": "deg",
      "symbol": "°",
      "concepts": [
        {
          "reference": "http://www.w3.org/2003/01/geo/wgs84_pos#lat",
          "kind": "rdf-property"
        }
      ]
    },
    "longitude": {
      "type": "double",
      "description": "Longitude of the observing platform in decimal degrees east. Negative values indicate western hemisphere.",
      "unit": "deg",
      "symbol": "°",
      "concepts": [
        {
          "reference": "http://www.w3.org/2003/01/geo/wgs84_pos#long",
          "kind": "rdf-property"
        }
      ]
    },
    "timestamp": {
      "type": "datetime",
      "description": "Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC data. The NDBC composite file from which this record is drawn is refreshed every five minutes, so the producer is expected to publish one record per station per five-minute slot.",
      "semanticRole": "phenomenonTime",
      "cadence": {
        "kind": "fixed",
        "period": "PT5M"
      }
    },
    "wind_direction": {
      "type": "double",
      "description": "Wind direction (the direction the wind is coming from) averaged over an 8-minute period for buoys or a 2-minute period for land stations. Unit: degrees true. The reported value is the mean of the samples taken over that averaging window rather than an instantaneous reading. The window ends at the observation time, and its length is not fixed by this schema: it follows the station type, which the record does not carry, so no `supportPeriod` is declared and the extent of the period must be obtained from the NDBC station metadata.",
      "unit": "deg",
      "symbol": "°",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Angle",
        "kind": "qudt-quantity-kind"
      }
    },
    "wind_speed": {
      "type": "double",
      "description": "Average wind speed during the observation period: 8 minutes for buoys, 2 minutes for land stations. Unit: meters per second. The reported value is the mean of the anemometer samples taken over that averaging window. The window ends at the observation time and its length follows the station type, which the record does not carry, so no `supportPeriod` is declared and the extent of the period is indeterminate from this schema alone.",
      "unit": "m/s",
      "symbol": "m/s",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Speed",
        "kind": "qudt-quantity-kind"
      }
    },
    "gust": {
      "type": "double",
      "description": "Peak 5-second or 8-second gust speed during the observation period. Unit: meters per second. The reported value is the greatest short-interval wind speed observed within the same averaging window that produced wind_speed, whose length follows the station type and is not fixed by this schema, so no `supportPeriod` is declared here either.",
      "unit": "m/s",
      "symbol": "m/s",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "maximum",
      "phenomenonTimeRelation": "interval",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Speed",
        "kind": "qudt-quantity-kind"
      }
    },
    "wave_height": {
      "type": "double",
      "description": "Significant wave height — the average of the highest one-third of all wave heights during a 20-minute sampling period. Unit: meters. The summary function is the arithmetic mean, so the statistic is 'mean'; the population it is taken over is not the full set of waves in the window but the highest one-third of them, and that restriction is stated here because the statistic keyword names the function only.",
      "unit": "m",
      "symbol": "m",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT20M",
        "anchor": "end"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Length",
        "kind": "qudt-quantity-kind"
      }
    },
    "dominant_wave_period": {
      "type": "double",
      "description": "Dominant wave period — the period (in seconds) of the wave band with the maximum energy in the spectral wave analysis. Unit: seconds. The value is read off a computed energy spectrum rather than produced by applying a named summary function to a set of readings, so the derivation is 'calculated'.",
      "unit": "s",
      "symbol": "s",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT20M",
        "anchor": "end"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Period",
        "kind": "qudt-quantity-kind"
      }
    },
    "average_wave_period": {
      "type": "double",
      "description": "Average wave period of all waves during the 20-minute sampling period. Unit: seconds. The reported value is the mean of the individual wave periods measured over that window.",
      "unit": "s",
      "symbol": "s",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT20M",
        "anchor": "end"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Period",
        "kind": "qudt-quantity-kind"
      }
    },
    "mean_wave_direction": {
      "type": "double",
      "description": "Mean wave direction corresponding to the energy at the dominant wave period (DPD). Unit: degrees true. The value is obtained from the directional moments of the computed wave spectrum at a single frequency band, not by averaging a set of direction readings, so the derivation is 'calculated'.",
      "unit": "deg",
      "symbol": "°",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT20M",
        "anchor": "end"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Angle",
        "kind": "qudt-quantity-kind"
      }
    },
    "pressure": {
      "type": "double",
      "description": "Sea-level pressure reduced using the standard atmosphere from the station elevation. Unit: hectopascals. The barometer reading is transformed by the standard-atmosphere reduction formula before publication, so the derivation is 'calculated'.",
      "unit": "hPa",
      "symbol": "hPa",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Pressure",
        "kind": "qudt-quantity-kind"
      }
    },
    "air_temperature": {
      "type": "double",
      "description": "Air temperature measured at the station. Unit: degrees Celsius.",
      "unit": "CEL",
      "symbol": "°C",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Temperature",
        "kind": "qudt-quantity-kind"
      }
    },
    "water_temperature": {
      "type": "double",
      "description": "Sea surface temperature. For buoys, measured by a hull-contact sensor near the waterline. Unit: degrees Celsius.",
      "unit": "CEL",
      "symbol": "°C",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Temperature",
        "kind": "qudt-quantity-kind"
      }
    },
    "dewpoint": {
      "type": "double",
      "description": "Dewpoint temperature computed from air temperature and relative humidity. Unit: degrees Celsius. Two sensor channels are combined by a deterministic psychrometric formula, so the derivation is 'calculated'.",
      "unit": "CEL",
      "symbol": "°C",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/DewPointTemperature",
        "kind": "qudt-quantity-kind"
      }
    },
    "pressure_tendency": {
      "type": "double",
      "description": "Pressure tendency — the signed change in sea-level pressure over the preceding 3 hours. A negative value indicates falling pressure; a positive value indicates rising pressure. Unit: hectopascals. The value is a difference between two pressure readings three hours apart, so the derivation is 'calculated' and the value applies to the three-hour interval ending at the observation time.",
      "unit": "hPa",
      "symbol": "hPa",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT3H",
        "anchor": "end"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Pressure",
        "kind": "qudt-quantity-kind"
      }
    },
    "visibility": {
      "type": "double",
      "description": "Station visibility as reported by the observing platform. Buoy visibility sensors have a range of 0 to 1.6 nautical miles and are generally only available on C-MAN stations. Unit: nautical miles.",
      "unit": "[nmi_i]",
      "symbol": "nmi",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Length",
        "kind": "qudt-quantity-kind"
      }
    },
    "tide": {
      "type": "double",
      "description": "Water level above or below Mean Lower Low Water (MLLW) at coastal and C-MAN stations. Unit: feet.",
      "unit": "[ft_i]",
      "symbol": "ft",
      "semanticRole": "observationValue",
      "derivation": "measured",
      "phenomenonTimeRelation": "instant",
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Length",
        "kind": "qudt-quantity-kind"
      }
    }
  },
  "required": [
    "station_id",
    "latitude",
    "longitude",
    "timestamp"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "station_id": "41001",
  "latitude": 34.724,
  "longitude": -72.317,
  "timestamp": "2026-07-30T11:50:00Z",
  "wind_direction": 212.0,
  "wind_speed": 7.2,
  "gust": 9.3,
  "wave_height": 1.8,
  "dominant_wave_period": 8.3,
  "average_wave_period": 5.9,
  "mean_wave_direction": 205.0,
  "pressure": 1016.4,
  "air_temperature": 26.1,
  "water_temperature": 27.4,
  "dewpoint": 22.8,
  "pressure_tendency": -0.7
}
```
