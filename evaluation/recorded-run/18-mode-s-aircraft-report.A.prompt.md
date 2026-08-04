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
  "name": "ModeSRecord",
  "type": "object",
  "definitions": {
    "MessageTypeEnum": {
      "name": "MessageTypeEnum",
      "type": "string",
      "enum": [
        "df17-adsb",
        "df4-altitude",
        "df5-identity",
        "df11-acquisition",
        "df20-comm-b",
        "df21-comm-b"
      ]
    }
  },
  "properties": {
    "icao24": {
      "type": "string",
      "pattern": "^[0-9a-f]{6}$"
    },
    "receiver_id": {
      "type": "string"
    },
    "msg_type": {
      "type": {
        "$ref": "#/definitions/MessageTypeEnum"
      }
    },
    "df": {
      "type": "int32",
      "minimum": 0,
      "maximum": 24
    },
    "tc": {
      "type": "int32",
      "minimum": 0,
      "maximum": 31
    },
    "bcode": {
      "type": "string"
    },
    "ts": {
      "type": "int64"
    },
    "cs": {
      "type": "string"
    },
    "sq": {
      "type": "string",
      "pattern": "^[0-7]{4}$"
    },
    "alt": {
      "type": "int32"
    },
    "lat": {
      "type": "double",
      "minimum": -90,
      "maximum": 90
    },
    "lon": {
      "type": "double",
      "minimum": -180,
      "maximum": 180
    },
    "spd": {
      "type": "double"
    },
    "ang": {
      "type": "double",
      "minimum": 0,
      "maximum": 360
    },
    "vr": {
      "type": "int32"
    },
    "rssi": {
      "type": "double"
    }
  },
  "required": [
    "icao24",
    "receiver_id",
    "msg_type",
    "df",
    "ts"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "icao24": "4ca7b3",
  "receiver_id": "EHAM-NORTH-01",
  "msg_type": "df17-adsb",
  "df": 17,
  "tc": 11,
  "ts": "1785474764316",
  "cs": "EIN17A",
  "sq": "3421",
  "alt": 34000,
  "lat": 52.31047,
  "lon": 4.76812,
  "spd": 441.2,
  "ang": 187.4,
  "vr": -64,
  "rssi": -18.7
}
```
