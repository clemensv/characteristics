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
  "description": "A decoded Mode-S or ADS-B downlink message from a ground receiver, as forwarded by the mode-s feeder. Derived from the mode-s feeder schema published in the xRegistry catalogue.",
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
      ],
      "description": "Downlink-format family of the decoded message, synthesised by the feeder from `df` and `tc`. It determines which members of this record are populated."
    }
  },
  "properties": {
    "icao24": {
      "type": "string",
      "pattern": "^[0-9a-f]{6}$",
      "description": "ICAO 24-bit aircraft address in lower-case hexadecimal, from the `icao24` field. It is assigned to the airframe by the state of registry and is the only identifier present in every message format, so it is the identity of the aircraft whose state this record reports."
    },
    "receiver_id": {
      "type": "string",
      "description": "Stable identifier of the ground station that decoded this transmission, from the `receiver_id` field. It is the procedure that produced every value in this record: the same transmission decoded by two stations yields two records that differ in `rssi`, in `ts`, and occasionally in the decoded position, because a position derived from a pair of CPR-encoded messages depends on which pair the station happened to receive."
    },
    "msg_type": {
      "type": {
        "$ref": "#/definitions/MessageTypeEnum"
      },
      "description": "Kebab-case downlink-format family literal synthesised by the feeder from `df` and `tc`, from the `msg_type` field. It exists because the numeric `df` and `tc` values are unreadable without ICAO Annex 10."
    },
    "df": {
      "type": "int32",
      "minimum": 0,
      "maximum": 24,
      "description": "Downlink Format, the first five bits of the Mode-S transmission, from the `df` field. It selects the frame layout: 4 and 20 are altitude replies, 5 and 21 are identity replies, 11 is an all-call reply, and 17 is an extended squitter carrying ADS-B."
    },
    "tc": {
      "type": "int32",
      "minimum": 0,
      "maximum": 31,
      "description": "Type Code, the first five bits of the ADS-B payload, from the `tc` field. It is present only when `df` is 17 and it selects the meaning of the remaining bits: 1 to 4 carry identification, 9 to 18 airborne position against a barometric altitude, 19 velocity, and 20 to 22 airborne position against a geometric altitude."
    },
    "bcode": {
      "type": "string",
      "description": "BDS register code of a Comm-B reply, from the `bcode` field, present only when `df` is 20 or 21. The register number determines what the 56-bit payload contains, and it is not transmitted: a decoder infers it from the bit pattern and can infer it wrongly."
    },
    "ts": {
      "type": "int64",
      "description": "Instant at which the ground station decoded this transmission, from the `ts` field, as a count of milliseconds since the POSIX epoch. It is not the instant the reported state was true aboard the aircraft: Mode-S transmissions carry no timestamp, so the sampling instant is unavailable and can only be bounded by the transmission interval of the format concerned."
    },
    "cs": {
      "type": "string",
      "description": "Aircraft callsign as broadcast in the identification message, from the `cs` field. It is entered by the crew and is padded to eight characters; it is the flight identity rather than the airframe, so it changes between legs and is frequently wrong or blank."
    },
    "sq": {
      "type": "string",
      "pattern": "^[0-7]{4}$",
      "description": "Mode-A squawk code assigned by air traffic control, from the `sq` field, in octal. Three values are reserved and carry a meaning that overrides the assignment: 7500 unlawful interference, 7600 radio failure, 7700 general emergency."
    },
    "alt": {
      "type": "int32",
      "description": "Barometric altitude in feet, from the `alt` field. It is not a height above the ground or above the ellipsoid: it is the altitude the aircraft's air data computer derives from static pressure referenced to the standard pressure setting of 1013.25 hPa, so two aircraft reporting the same value are on the same pressure surface and not at the same geometric height. The offset from geometric height varies with the state of the atmosphere and is not transmitted."
    },
    "lat": {
      "type": "double",
      "minimum": -90,
      "maximum": 90,
      "description": "WGS84 latitude in decimal degrees, from the `lat` field. ADS-B transmits position in a compact encoding that is ambiguous in isolation, so the decoder resolves it from a pair of consecutive messages or against a known receiver position; the value is therefore a solution rather than a reading."
    },
    "lon": {
      "type": "double",
      "minimum": -180,
      "maximum": 180,
      "description": "WGS84 longitude in decimal degrees, from the `lon` field, resolved by the same decoding as `lat`."
    },
    "spd": {
      "type": "double",
      "description": "Speed in knots, from the `spd` field, present only in a velocity message. The velocity message reports either ground speed or airspeed depending on a subtype bit that the feeder does not forward, so a consumer cannot tell from this record which of the two it received."
    },
    "ang": {
      "type": "double",
      "minimum": 0,
      "maximum": 360,
      "description": "Angle in degrees, from the `ang` field, present only in a velocity message. It is the track over the ground when the message reports ground speed and the magnetic heading when it reports airspeed, and the two differ by the drift angle and by magnetic variation. As with `spd`, the subtype that decides which one it is has been discarded."
    },
    "vr": {
      "type": "int32",
      "description": "Vertical rate in feet per minute, from the `vr` field, positive upward. The velocity message states whether the rate was computed from the barometric or the geometric altitude source, and that bit is not forwarded either, so the value cannot be reconciled with `alt` without assuming which source produced it."
    },
    "rssi": {
      "type": "double",
      "description": "Received signal level reported by the decoder in decibels relative to the full scale of the receiver's analogue-to-digital converter, from the `rssi` field. The scale is receiver-specific and the values of two stations are not comparable, but within one station a low level marks a message decoded near the noise floor, which is where bit errors that survive the parity check originate."
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
