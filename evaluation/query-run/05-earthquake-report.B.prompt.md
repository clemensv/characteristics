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
  "name": "EarthquakeReport",
  "description": "JMA Bosai earthquake and seismic intensity report header enriched with parsed hypocenter coordinates and prefecture intensity summaries. Derived from the jma-bosai-quake feeder schema published in the xRegistry catalogue and trimmed to the hypocentre, magnitude, origin time, report issue time and report status.",
  "type": "object",
  "concepts": [
    {
      "reference": "http://purl.org/dc/dcmitype/Event",
      "kind": "rdfs-class"
    }
  ],
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/earthquake-hypocentre-and-magnitude/v1",
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
    "event_id": {
      "type": "string",
      "description": "Stable JMA earthquake event identifier copied from list.json eid and detail Head.EventID. JMA uses the earthquake origin time in YYYYMMDDHHMMSS form as the event id, so multiple serial reports for the same earthquake share this value.",
      "pattern": "^[0-9]{14}$",
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/identifier",
          "kind": "dcterms-property"
        }
      ]
    },
    "serial": {
      "type": "integer",
      "description": "JMA report serial number parsed from list.json ser and detail Head.Serial. The serial identifies the revision sequence for bulletins sharing the same event id.",
      "minimum": 0
    },
    "report_id": {
      "type": "string",
      "description": "Composite report identifier formed as event_id, an underscore, and the JMA serial number. It distinguishes initial, corrected, and subsequent bulletins for the same earthquake event."
    },
    "info_type": {
      "type": "string",
      "description": "Normalized information type derived from the Japanese JMA ift field: ISSUED for 発表, CORRECTED for 訂正, and CANCELLED for 取消. The value states the standing of this bulletin within the revision sequence rather than any property of the earthquake itself.",
      "enum": [
        "ISSUED",
        "CORRECTED",
        "CANCELLED"
      ],
      "altenums": {
        "lang:en": {
          "ISSUED": "Issued",
          "CORRECTED": "Corrected",
          "CANCELLED": "Cancelled"
        },
        "description": {
          "ISSUED": "First publication of this bulletin.",
          "CORRECTED": "Correction of a bulletin already published.",
          "CANCELLED": "Withdrawal of a bulletin already published."
        }
      },
      "semanticRole": "status"
    },
    "origin_datetime": {
      "type": "datetime",
      "description": "Earthquake origin time converted from list.json at to an RFC3339 UTC timestamp. JMA uses this time as the basis for the event id. This is the instant at which rupture began, so it is the phenomenon time against which the hypocentre and magnitude results are read. Earthquakes are not scheduled, so successive values carry no period.",
      "semanticRole": "phenomenonTime",
      "cadence": {
        "kind": "irregular"
      }
    },
    "report_datetime": {
      "type": "datetime",
      "description": "Report publication time converted from list.json rdt to an RFC3339 UTC timestamp. JMA publishes rdt with a local offset for the report release time. This is the instant at which the hypocentre and magnitude solution carried by this bulletin became available, which is later than, and independent of, the origin time.",
      "semanticRole": "resultTime"
    },
    "control_datetime": {
      "type": "datetime",
      "description": "JMA control timestamp — when the bulletin was published to the JMA distribution system, distinct from report_datetime which is the event report time. This field converts the compact list.json ctt value from JST to an RFC3339 UTC timestamp. It records the handover of the finished bulletin into the distribution channel rather than the completion of the solution.",
      "semanticRole": "ingestionTime"
    },
    "title_jp": {
      "type": "string",
      "description": "Japanese JMA bulletin title copied from list.json ttl, such as 震源・震度情報 for earthquake and seismic intensity information.",
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/title",
          "kind": "dcterms-property"
        }
      ]
    },
    "title_en": {
      "type": [
        "string",
        "null"
      ],
      "description": "English bulletin title copied from list.json en_ttl when supplied by the multilingual JMA Bosai feed. Null is emitted when en_ttl is absent, including some 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.",
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/title",
          "kind": "dcterms-property"
        }
      ]
    },
    "epicenter_area_code": {
      "type": [
        "string",
        "null"
      ],
      "description": "JMA hypocenter or epicenter area code copied from list.json acd and detail Body.Earthquake.Hypocenter.Area.Code. The code names the seismic source region that the bulletin describes. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.",
      "semanticRole": "featureOfInterest"
    },
    "epicenter_area_jp": {
      "type": [
        "string",
        "null"
      ],
      "description": "Japanese epicenter area name copied from list.json anm and detail Body.Earthquake.Hypocenter.Area.Name. Null is emitted when the source bulletin omits hypocenter metadata, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins."
    },
    "latitude": {
      "type": "double",
      "description": "Hypocenter latitude in WGS84 decimal degrees parsed from the ISO 6709 coordinate string in list.json cod or detail Body.Earthquake.Hypocenter.Area.Coordinate. The value is not observed directly: JMA computes the hypocentre by inverting arrival times recorded across the national seismograph network. The member is omitted when the coordinate is absent or cannot be parsed, including for 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.",
      "minimum": -90.0,
      "maximum": 90.0,
      "unit": "deg",
      "symbol": "°",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "concepts": [
        {
          "reference": "http://www.w3.org/2003/01/geo/wgs84_pos#lat",
          "kind": "rdf-property"
        }
      ]
    },
    "longitude": {
      "type": "double",
      "description": "Hypocenter longitude in WGS84 decimal degrees parsed from the ISO 6709 coordinate string in list.json cod or detail Body.Earthquake.Hypocenter.Area.Coordinate. The value is computed together with the latitude and depth from the same hypocentre inversion. The member is omitted when the coordinate is absent or cannot be parsed, including for 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.",
      "minimum": -180.0,
      "maximum": 180.0,
      "unit": "deg",
      "symbol": "°",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "concepts": [
        {
          "reference": "http://www.w3.org/2003/01/geo/wgs84_pos#long",
          "kind": "rdf-property"
        }
      ]
    },
    "depth_km": {
      "type": "double",
      "description": "Hypocenter depth in kilometres parsed from the third component of the ISO 6709 coordinate string. JMA encodes depth in metres with a sign in cod; this field divides the absolute metre value by 1000 so +35.0+135.5-10000/ becomes 10.0 km. The depth is a component of the same computed hypocentre solution as the latitude and longitude. The member is omitted when list.json cod is absent.",
      "minimum": 0.0,
      "maximum": 700.0,
      "unit": "km",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant"
    },
    "magnitude": {
      "type": [
        "double",
        "null"
      ],
      "description": "Dimensionless JMA earthquake magnitude parsed from list.json mag or detail Body.Earthquake.Magnitude and expressed on the JMA magnitude scale, which is similar to Richter magnitude for shallow events. The value is computed from displacement amplitudes recorded across the network by the published JMA magnitude formula, not read from any single instrument. Null is emitted when the source bulletin omits magnitude, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.",
      "semanticRole": "observationValue",
      "derivation": "calculated",
      "phenomenonTimeRelation": "instant",
      "concepts": [
        {
          "reference": "http://qudt.org/vocab/quantitykind/Dimensionless",
          "kind": "skos-concept"
        }
      ]
    },
    "max_intensity": {
      "type": "string",
      "description": "Maximum observed JMA seismic intensity for the report copied from list.json maxi or detail Body.Intensity.Observation.MaxInt. The value is the maximum function applied to the set of shindo values observed at the contributing stations, so it is a statistic over those observations rather than a reading from one instrument. The member is omitted when the bulletin has no observed intensity summary.",
      "pattern": "^(1|2|3|4|5-|5\\+|6-|6\\+|7)$",
      "enum": [
        "1",
        "2",
        "3",
        "4",
        "5-",
        "5+",
        "6-",
        "6+",
        "7"
      ],
      "altenums": {
        "lang:en": {
          "1": "Shindo 1",
          "2": "Shindo 2",
          "3": "Shindo 3",
          "4": "Shindo 4",
          "5-": "Shindo 5 Lower",
          "5+": "Shindo 5 Upper",
          "6-": "Shindo 6 Lower",
          "6+": "Shindo 6 Upper",
          "7": "Shindo 7"
        },
        "description": {
          "1": "Felt only by some people at rest indoors.",
          "2": "Felt by many people indoors; hanging objects swing slightly.",
          "3": "Felt by most people indoors; dishes rattle.",
          "4": "Hanging objects swing markedly; unstable ornaments may fall.",
          "5-": "Many people are frightened; unsecured furniture may move.",
          "5+": "Difficult to walk without holding on; unsecured furniture may topple.",
          "6-": "Difficult to stand; wall tiles and windows may break.",
          "6+": "Impossible to move without crawling; many unreinforced buildings are damaged.",
          "7": "People are thrown by the shaking; even reinforced buildings may lean or collapse."
        }
      },
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "maximum"
    },
    "bulletin_type": {
      "type": "string",
      "description": "JMA detail bulletin product code parsed from the detail JSON filename. Tsunami-specific VTSE products are deliberately not modeled by this source. The code is the scale on which the maturity of the hypocentre and magnitude solution is expressed, so it qualifies the results in this record rather than being a result itself.",
      "enum": [
        "VXSE51",
        "VXSE52",
        "VXSE53",
        "VXSE5k",
        "VXSE61",
        "VYSE52"
      ],
      "altenums": {
        "lang:en": {
          "VXSE51": "震度速報",
          "VXSE52": "震源に関する情報",
          "VXSE53": "震源・震度に関する情報",
          "VXSE5k": "震源・震度情報",
          "VXSE61": "長周期地震動に関する観測情報",
          "VYSE52": "南海トラフ地震関連解説情報"
        },
        "description": {
          "VXSE51": "Seismic-intensity flash, issued within about a minute and a half of detection and before the source parameters are determined.",
          "VXSE52": "Hypocentre information: determined source parameters without an observed-intensity summary.",
          "VXSE53": "Hypocentre and intensity information: determined source parameters together with observed intensities.",
          "VXSE5k": "Bosai-portal variant of the hypocentre and intensity product.",
          "VXSE61": "Long-period ground-motion observation information.",
          "VYSE52": "Nankai Trough earthquake related commentary."
        }
      },
      "semanticRole": "resultQuality"
    },
    "detail_url": {
      "type": "uri",
      "description": "Absolute URL for the full JMA Bosai earthquake detail JSON referenced by list.json json."
    },
    "affected_prefectures": {
      "type": "array",
      "description": "Prefecture intensity summaries derived from list.json int[]. Each entry includes the JMA prefecture code and maximum JMA seismic intensity reported for that prefecture.",
      "items": {
        "type": {
          "$ref": "#/definitions/AffectedPrefecture"
        },
        "description": "Maximum seismic intensity reported for one Japanese prefecture affected by this earthquake."
      }
    },
    "tsunami_possible": {
      "type": [
        "boolean",
        "null"
      ],
      "description": "Interpretation of tsunami-related text in the full detail JSON comments. True means the detail bulletin text indicates tsunami attention or possibility; false means the detail explicitly states there is no tsunami concern; null means no tsunami-related detail text was available or fetched. The value is inferred from free-text comments by the bridge rather than published as a coded field, so it is an estimate of the bulletin's intent.",
      "derivation": "estimated"
    }
  },
  "required": [
    "event_id",
    "serial",
    "report_id",
    "info_type",
    "origin_datetime",
    "report_datetime",
    "control_datetime",
    "title_jp",
    "bulletin_type",
    "detail_url",
    "affected_prefectures",
    "tsunami_possible"
  ],
  "additionalProperties": false,
  "definitions": {
    "AffectedPrefecture": {
      "name": "AffectedPrefecture",
      "type": "object",
      "description": "Prefecture-level maximum seismic intensity summary from each object in the JMA Bosai list.json int array. JMA publishes this compact list with prefecture code and the maximum observed JMA seismic intensity in that prefecture for the report.",
      "concepts": [
        {
          "reference": "http://www.w3.org/ns/sosa/FeatureOfInterest",
          "kind": "owl-class"
        }
      ],
      "properties": {
        "code": {
          "type": "string",
          "description": "JMA prefecture code copied from int[].code in the Bosai earthquake list entry. The code identifies the prefecture in which one or more observations contributed to the report.",
          "concepts": [
            {
              "reference": "http://purl.org/dc/terms/identifier",
              "kind": "dcterms-property"
            }
          ]
        },
        "max_intensity": {
          "type": "string",
          "description": "Maximum JMA seismic intensity observed in the prefecture for this report, copied from int[].maxi and expressed on the JMA shindo scale. The value is the maximum function applied to the shindo values observed at the stations within the prefecture.",
          "pattern": "^(1|2|3|4|5-|5\\+|6-|6\\+|7)$",
          "enum": [
            "1",
            "2",
            "3",
            "4",
            "5-",
            "5+",
            "6-",
            "6+",
            "7"
          ],
          "altenums": {
            "lang:en": {
              "1": "Shindo 1",
              "2": "Shindo 2",
              "3": "Shindo 3",
              "4": "Shindo 4",
              "5-": "Shindo 5 Lower",
              "5+": "Shindo 5 Upper",
              "6-": "Shindo 6 Lower",
              "6+": "Shindo 6 Upper",
              "7": "Shindo 7"
            },
            "description": {
              "1": "Felt only by some people at rest indoors.",
              "2": "Felt by many people indoors; hanging objects swing slightly.",
              "3": "Felt by most people indoors; dishes rattle.",
              "4": "Hanging objects swing markedly; unstable ornaments may fall.",
              "5-": "Many people are frightened; unsecured furniture may move.",
              "5+": "Difficult to walk without holding on; unsecured furniture may topple.",
              "6-": "Difficult to stand; wall tiles and windows may break.",
              "6+": "Impossible to move without crawling; many unreinforced buildings are damaged.",
              "7": "People are thrown by the shaking; even reinforced buildings may lean or collapse."
            }
          },
          "derivation": "statistic",
          "statistic": "maximum"
        }
      },
      "required": [
        "code",
        "max_intensity"
      ],
      "additionalProperties": false
    }
  }
}
```

instance.json

```json
{
  "event_id": "20260729143207",
  "serial": 2,
  "report_id": "20260729143207_2",
  "info_type": "ISSUED",
  "origin_datetime": "2026-07-29T14:32:07Z",
  "report_datetime": "2026-07-29T14:38:00Z",
  "control_datetime": "2026-07-29T14:38:12Z",
  "title_jp": "震源・震度に関する情報",
  "title_en": "Information on Seismic Intensity and Epicenter",
  "epicenter_area_code": "290",
  "epicenter_area_jp": "宮城県沖",
  "latitude": 38.3,
  "longitude": 141.9,
  "depth_km": 50.0,
  "magnitude": 5.4,
  "max_intensity": "4",
  "bulletin_type": "VXSE53",
  "detail_url": "https://www.jma.go.jp/bosai/quake/data/20260729143800_20260729143207_VXSE53_1.json",
  "affected_prefectures": [
    { "code": "400", "max_intensity": "4" },
    { "code": "410", "max_intensity": "3" },
    { "code": "300", "max_intensity": "2" }
  ],
  "tsunami_possible": false
}
```
