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
  "name": "GcmtMomentTensor",
  "type": "object",
  "properties": {
    "event_name": {
      "type": "string"
    },
    "centroid_time": {
      "type": "datetime"
    },
    "centroid_latitude": {
      "type": "double"
    },
    "centroid_longitude": {
      "type": "double"
    },
    "centroid_depth": {
      "type": "double",
      "ucumUnit": "km",
      "minimum": 0
    },
    "depth_type": {
      "type": "string",
      "enum": [
        "FREE",
        "FIX",
        "BDY"
      ]
    },
    "half_duration": {
      "type": "double",
      "ucumUnit": "s",
      "minimum": 0
    },
    "scalar_moment": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "minimum": 0
    },
    "mrr": {
      "type": "double",
      "ucumUnit": "dyn.cm"
    },
    "mtt": {
      "type": "double",
      "ucumUnit": "dyn.cm"
    },
    "mpp": {
      "type": "double",
      "ucumUnit": "dyn.cm"
    },
    "mrt": {
      "type": "double",
      "ucumUnit": "dyn.cm"
    },
    "mrp": {
      "type": "double",
      "ucumUnit": "dyn.cm"
    },
    "mtp": {
      "type": "double",
      "ucumUnit": "dyn.cm"
    }
  },
  "required": [
    "event_name",
    "centroid_time",
    "centroid_latitude",
    "centroid_longitude",
    "centroid_depth",
    "scalar_moment",
    "mrr",
    "mtt",
    "mpp",
    "mrt",
    "mrp",
    "mtp"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "event_name": "C200501010120A",
  "centroid_time": "2005-01-01T01:20:05.1Z",
  "centroid_latitude": 13.76,
  "centroid_longitude": -89.08,
  "centroid_depth": 162.8,
  "depth_type": "FREE",
  "half_duration": 0.6,
  "scalar_moment": 1.312e23,
  "mrr": 0.838e23,
  "mtt": -0.005e23,
  "mpp": -0.833e23,
  "mrt": 1.050e23,
  "mrp": -0.369e23,
  "mtp": 0.044e23
}
```
