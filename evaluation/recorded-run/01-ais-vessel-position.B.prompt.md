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
  "name": "StandardClassBPositionReport",
  "type": "object",
  "properties": {
    "UserID": {
      "type": "int32"
    },
    "TimeReceived": {
      "type": "datetime"
    },
    "Timestamp": {
      "type": "int32"
    },
    "Valid": {
      "type": "boolean"
    },
    "Latitude": {
      "type": "double"
    },
    "Longitude": {
      "type": "double"
    },
    "PositionAccuracy": {
      "type": "boolean"
    },
    "Raim": {
      "type": "boolean"
    },
    "Sog": {
      "type": "double"
    },
    "Cog": {
      "type": "double"
    },
    "TrueHeading": {
      "type": "int32"
    },
    "AssignedMode": {
      "type": "boolean"
    },
    "ClassBUnit": {
      "type": "boolean"
    },
    "ClassBDisplay": {
      "type": "boolean"
    },
    "ClassBDsc": {
      "type": "boolean"
    },
    "ClassBBand": {
      "type": "boolean"
    },
    "ClassBMsg22": {
      "type": "boolean"
    }
  },
  "required": [
    "UserID",
    "TimeReceived",
    "Timestamp",
    "Valid",
    "Latitude",
    "Longitude"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "UserID": 244630123,
  "TimeReceived": "2026-07-30T11:42:09Z",
  "Timestamp": 7,
  "Valid": true,
  "Latitude": 51.9042,
  "Longitude": 4.0117,
  "PositionAccuracy": false,
  "Raim": true,
  "Sog": 6.4,
  "Cog": 287.3,
  "TrueHeading": 285,
  "AssignedMode": false,
  "ClassBUnit": true,
  "ClassBDisplay": true,
  "ClassBDsc": true,
  "ClassBBand": true,
  "ClassBMsg22": true
}
```
