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
  "name": "BuoyObservation",
  "type": "object",
  "properties": {
    "station_id": {
      "type": "string"
    },
    "latitude": {
      "type": "double"
    },
    "longitude": {
      "type": "double"
    },
    "timestamp": {
      "type": "datetime"
    },
    "wind_direction": {
      "type": "double"
    },
    "wind_speed": {
      "type": "double"
    },
    "gust": {
      "type": "double"
    },
    "wave_height": {
      "type": "double"
    },
    "dominant_wave_period": {
      "type": "double"
    },
    "average_wave_period": {
      "type": "double"
    },
    "mean_wave_direction": {
      "type": "double"
    },
    "pressure": {
      "type": "double"
    },
    "air_temperature": {
      "type": "double"
    },
    "water_temperature": {
      "type": "double"
    },
    "dewpoint": {
      "type": "double"
    },
    "pressure_tendency": {
      "type": "double"
    },
    "visibility": {
      "type": "double"
    },
    "tide": {
      "type": "double"
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
