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
  "name": "FirmsModisFireDetection",
  "description": "One active-fire pixel detection from a NASA FIRMS MODIS product, transcribed from the NASA.FIRMS.FireDetection event of the real-time-sources feeder for the case where the acquiring instrument is MODIS.",
  "type": "object",
  "properties": {
    "source": {
      "type": "string",
      "description": "FIRMS product source identifier for the satellite and sensor, from the `source` field, such as `MODIS_NRT`. It identifies the product the detection came from."
    },
    "latitude": {
      "type": "double",
      "description": "Latitude of the centre of the nominal one-kilometre fire pixel in WGS-84 decimal degrees, from the `latitude` field."
    },
    "longitude": {
      "type": "double",
      "description": "Longitude of the pixel centre in WGS-84 decimal degrees, from the `longitude` field."
    },
    "brightness": {
      "type": "double",
      "description": "Brightness temperature of the fire pixel in MODIS channel 21/22, near four micrometres, from the `brightness` field. It is the first band of the pair the fire product resolves."
    },
    "bright_t31": {
      "type": "double",
      "description": "Brightness temperature of the fire pixel in MODIS channel 31, near eleven micrometres, from the `bright_t31` field. Paired with `brightness` to screen false alarms and gauge fire intensity."
    },
    "frp": {
      "type": "double",
      "description": "Fire radiative power in megawatts, from the `frp` field: the radiative energy release rate within the pixel."
    },
    "acq_datetime": {
      "type": "string",
      "description": "UTC acquisition instant of the overpass, from the `acq_datetime` field, in ISO-8601 form."
    },
    "satellite": {
      "type": "string",
      "description": "Short platform code of the acquiring satellite, from the `satellite` field, such as `T` for Terra or `A` for Aqua."
    }
  },
  "required": [
    "source",
    "latitude",
    "longitude",
    "brightness",
    "bright_t31",
    "acq_datetime",
    "satellite"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "source": "MODIS_NRT",
  "latitude": -13.2456,
  "longitude": 27.8891,
  "brightness": 331.7,
  "bright_t31": 295.4,
  "frp": 84.6,
  "acq_datetime": "2026-08-02T11:42:00Z",
  "satellite": "A"
}
```
