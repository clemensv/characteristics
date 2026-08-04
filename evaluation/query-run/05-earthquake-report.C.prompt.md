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
  "$schema": "https://json-structure.org/meta/extended/v0/#",
  "$id": "https://example.invalid/schema",
  "$uses": [
    "JSONStructureValidation"
  ],
  "name": "EarthquakeReport",
  "type": "object",
  "properties": {
    "event_id": {
      "type": "string",
      "pattern": "^[0-9]{14}$"
    },
    "serial": {
      "type": "integer",
      "minimum": 0
    },
    "report_id": {
      "type": "string"
    },
    "info_type": {
      "type": "string",
      "enum": [
        "ISSUED",
        "CORRECTED",
        "CANCELLED"
      ]
    },
    "origin_datetime": {
      "type": "datetime"
    },
    "report_datetime": {
      "type": "datetime"
    },
    "control_datetime": {
      "type": "datetime"
    },
    "title_jp": {
      "type": "string"
    },
    "title_en": {
      "type": [
        "string",
        "null"
      ]
    },
    "epicenter_area_code": {
      "type": [
        "string",
        "null"
      ]
    },
    "epicenter_area_jp": {
      "type": [
        "string",
        "null"
      ]
    },
    "latitude": {
      "type": "double",
      "minimum": -90.0,
      "maximum": 90.0
    },
    "longitude": {
      "type": "double",
      "minimum": -180.0,
      "maximum": 180.0
    },
    "depth_km": {
      "type": "double",
      "minimum": 0.0,
      "maximum": 700.0
    },
    "magnitude": {
      "type": [
        "double",
        "null"
      ]
    },
    "max_intensity": {
      "type": "string",
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
      ]
    },
    "bulletin_type": {
      "type": "string",
      "enum": [
        "VXSE51",
        "VXSE52",
        "VXSE53",
        "VXSE5k",
        "VXSE61",
        "VYSE52"
      ]
    },
    "detail_url": {
      "type": "uri"
    },
    "affected_prefectures": {
      "type": "array",
      "items": {
        "type": {
          "$ref": "#/definitions/AffectedPrefecture"
        }
      }
    },
    "tsunami_possible": {
      "type": [
        "boolean",
        "null"
      ]
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
      "properties": {
        "code": {
          "type": "string"
        },
        "max_intensity": {
          "type": "string",
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
          ]
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
