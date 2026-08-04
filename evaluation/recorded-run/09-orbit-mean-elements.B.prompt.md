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
  "name": "OrbitMeanElements",
  "type": "object",
  "properties": {
    "OBJECT_NAME": {
      "type": [
        "null",
        "string"
      ]
    },
    "OBJECT_ID": {
      "type": [
        "null",
        "string"
      ],
      "pattern": "^[0-9]{4}-[0-9]{3}[A-Z]{0,3}$"
    },
    "NORAD_CAT_ID": {
      "type": "int32",
      "minimum": 1,
      "maximum": 999999999
    },
    "CLASSIFICATION_TYPE": {
      "type": {
        "$ref": "#/definitions/ClassificationTypeEnum"
      }
    },
    "ORIGINATOR": {
      "type": "string"
    },
    "MEAN_ELEMENT_THEORY": {
      "type": "string"
    },
    "CREATION_DATE": {
      "type": "datetime"
    },
    "EPOCH": {
      "type": "object",
      "properties": {
        "ordinal": {
          "type": "string",
          "pattern": "^[0-9]{4}/[0-9]{3}\\.[0-9]{8}$"
        },
        "year": {
          "type": "int32",
          "minimum": 1957
        },
        "day_of_year": {
          "type": "double",
          "minimum": 1
        },
        "utc": {
          "type": "datetime"
        }
      },
      "required": [
        "ordinal",
        "year",
        "day_of_year"
      ],
      "additionalProperties": false
    },
    "MEAN_MOTION": {
      "type": "double",
      "minimum": 0
    },
    "ECCENTRICITY": {
      "type": "double",
      "minimum": 0,
      "maximum": 1
    },
    "INCLINATION": {
      "type": "double",
      "minimum": 0,
      "maximum": 180
    },
    "RA_OF_ASC_NODE": {
      "type": "double",
      "minimum": 0,
      "maximum": 360
    },
    "ARG_OF_PERICENTER": {
      "type": "double",
      "minimum": 0,
      "maximum": 360
    },
    "MEAN_ANOMALY": {
      "type": "double",
      "minimum": 0,
      "maximum": 360
    },
    "BSTAR": {
      "type": "double"
    },
    "MEAN_MOTION_DOT": {
      "type": "double"
    },
    "MEAN_MOTION_DDOT": {
      "type": "double"
    },
    "EPHEMERIS_TYPE": {
      "type": "int32",
      "minimum": 0
    },
    "ELEMENT_SET_NO": {
      "type": "int32",
      "minimum": 0
    },
    "REV_AT_EPOCH": {
      "type": "int32",
      "minimum": 0
    }
  },
  "required": [
    "NORAD_CAT_ID",
    "CLASSIFICATION_TYPE",
    "ORIGINATOR",
    "MEAN_ELEMENT_THEORY",
    "CREATION_DATE",
    "EPOCH",
    "MEAN_MOTION",
    "ECCENTRICITY",
    "INCLINATION",
    "RA_OF_ASC_NODE",
    "ARG_OF_PERICENTER",
    "MEAN_ANOMALY",
    "BSTAR",
    "MEAN_MOTION_DOT",
    "MEAN_MOTION_DDOT",
    "EPHEMERIS_TYPE",
    "ELEMENT_SET_NO",
    "REV_AT_EPOCH"
  ],
  "additionalProperties": false,
  "definitions": {
    "ClassificationTypeEnum": {
      "name": "ClassificationTypeEnum",
      "type": "string",
      "enum": [
        "U",
        "C",
        "S"
      ]
    }
  }
}
```

instance.json

```json
{
  "OBJECT_NAME": "ISS (ZARYA)",
  "OBJECT_ID": "1998-067A",
  "NORAD_CAT_ID": 25544,
  "CLASSIFICATION_TYPE": "U",
  "ORIGINATOR": "18 SPCS",
  "MEAN_ELEMENT_THEORY": "SGP4",
  "CREATION_DATE": "2026-07-30T20:11:05Z",
  "EPOCH": {
    "ordinal": "2026/211.76644861",
    "year": 2026,
    "day_of_year": 211.76644861,
    "utc": "2026-07-30T18:23:41.160Z"
  },
  "MEAN_MOTION": 15.50123456,
  "ECCENTRICITY": 0.0003421,
  "INCLINATION": 51.6392,
  "RA_OF_ASC_NODE": 247.8134,
  "ARG_OF_PERICENTER": 118.4257,
  "MEAN_ANOMALY": 241.7003,
  "BSTAR": 0.00021473,
  "MEAN_MOTION_DOT": 0.00012345,
  "MEAN_MOTION_DDOT": 0.0,
  "EPHEMERIS_TYPE": 0,
  "ELEMENT_SET_NO": 999,
  "REV_AT_EPOCH": 52871
}
```
