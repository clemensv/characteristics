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
