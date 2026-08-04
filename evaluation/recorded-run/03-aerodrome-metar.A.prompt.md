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
  "name": "Metar",
  "type": "object",
  "properties": {
    "icao_id": {
      "type": "string"
    },
    "name": {
      "type": [
        "string",
        "null"
      ]
    },
    "position": {
      "type": "object",
      "properties": {
        "latitude": {
          "type": "double"
        },
        "longitude": {
          "type": "double"
        }
      },
      "required": [
        "latitude",
        "longitude"
      ],
      "additionalProperties": false
    },
    "elevation": {
      "type": "double"
    },
    "obs_time": {
      "type": "datetime"
    },
    "report_time": {
      "type": [
        "datetime",
        "null"
      ]
    },
    "metar_type": {
      "type": [
        "string",
        "null"
      ]
    },
    "temp": {
      "type": "double"
    },
    "dewp": {
      "type": "double"
    },
    "wdir": {
      "type": "int32"
    },
    "wspd": {
      "type": "int32"
    },
    "wgst": {
      "type": "int32"
    },
    "visib": {
      "type": [
        "string",
        "null"
      ]
    },
    "altim": {
      "type": "double"
    },
    "slp": {
      "type": "double"
    },
    "wx_string": {
      "type": [
        "string",
        "null"
      ]
    },
    "clouds": {
      "type": [
        "string",
        "null"
      ]
    },
    "flt_cat": {
      "type": [
        "string",
        "null"
      ]
    },
    "qc_field": {
      "type": [
        "int32",
        "null"
      ]
    },
    "raw_ob": {
      "type": "string"
    }
  },
  "required": [
    "icao_id",
    "obs_time",
    "raw_ob"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "icao_id": "KJFK",
  "name": "New York/JF Kennedy Intl, NY, US",
  "position": {
    "latitude": 40.6386,
    "longitude": -73.7622
  },
  "elevation": 3.4,
  "obs_time": "2026-07-30T11:51:00Z",
  "report_time": "2026-07-30T11:53:00Z",
  "metar_type": "METAR",
  "temp": 26.1,
  "dewp": 22.2,
  "wdir": 210,
  "wspd": 12,
  "wgst": 18,
  "visib": "10+",
  "altim": 1015.6,
  "slp": 1015.4,
  "wx_string": null,
  "clouds": "[{\"cover\":\"FEW\",\"base\":4500},{\"cover\":\"SCT\",\"base\":25000}]",
  "flt_cat": "VFR",
  "qc_field": 2,
  "raw_ob": "METAR KJFK 301151Z 21012G18KT 10SM FEW045 SCT250 26/22 A2999 RMK AO2 SLP154 T02610222"
}
```
