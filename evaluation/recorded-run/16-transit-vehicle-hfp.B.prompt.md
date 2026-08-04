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
  "name": "VehicleEvent",
  "type": "object",
  "definitions": {
    "OperatingDayClockPosition": {
      "name": "OperatingDayClockPosition",
      "type": "object",
      "properties": {
        "ordinal": {
          "type": "string",
          "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}/[0-9]{4}$"
        },
        "oday": {
          "type": "date"
        },
        "start": {
          "type": "string",
          "pattern": "^[0-9]{2}:[0-9]{2}$"
        }
      },
      "required": [
        "ordinal",
        "oday",
        "start"
      ],
      "additionalProperties": false
    },
    "LocEnum": {
      "name": "LocEnum",
      "type": "string",
      "enum": [
        "GPS",
        "ODO",
        "MAN",
        "DR",
        "N/A"
      ]
    }
  },
  "properties": {
    "veh": {
      "type": "int32"
    },
    "oper": {
      "type": "int32"
    },
    "tst": {
      "type": "datetime"
    },
    "journey_start": {
      "type": {
        "$ref": "#/definitions/OperatingDayClockPosition"
      }
    },
    "desi": {
      "type": "string"
    },
    "route": {
      "type": "string"
    },
    "dir": {
      "type": "string",
      "enum": [
        "1",
        "2"
      ]
    },
    "lat": {
      "type": "double"
    },
    "long": {
      "type": "double"
    },
    "loc": {
      "type": {
        "$ref": "#/definitions/LocEnum"
      }
    },
    "spd": {
      "type": "double"
    },
    "hdg": {
      "type": "int32",
      "minimum": 0,
      "maximum": 360
    },
    "acc": {
      "type": "double"
    },
    "odo": {
      "type": "int32",
      "minimum": 0
    },
    "dl": {
      "type": "int32"
    },
    "stop": {
      "type": "int32"
    },
    "ttarr": {
      "type": "datetime"
    },
    "ttdep": {
      "type": "datetime"
    },
    "drst": {
      "type": "int32",
      "enum": [
        0,
        1
      ]
    },
    "occu": {
      "type": "int32",
      "minimum": 0,
      "maximum": 100
    }
  },
  "required": [
    "veh",
    "oper",
    "tst",
    "journey_start",
    "desi",
    "route",
    "dir",
    "loc"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "veh": 1216,
  "oper": 55,
  "tst": "2026-07-31T05:12:44.316Z",
  "journey_start": {
    "ordinal": "2026-07-31/0165",
    "oday": "2026-07-31",
    "start": "07:15"
  },
  "desi": "551",
  "route": "2551",
  "dir": "1",
  "lat": 60.20714,
  "long": 24.96233,
  "loc": "GPS",
  "spd": 8.42,
  "hdg": 187,
  "acc": -0.31,
  "odo": 4120,
  "dl": -95,
  "stop": 1130106,
  "ttarr": "2026-07-31T05:13:00Z",
  "ttdep": "2026-07-31T05:13:00Z",
  "drst": 0,
  "occu": 0
}
```
