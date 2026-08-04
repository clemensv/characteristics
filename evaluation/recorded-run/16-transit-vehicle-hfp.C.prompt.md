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
  "description": "A `vp` vehicle-position event from the HSL High-Frequency Positioning feed for the Helsinki region, published on MQTT at roughly one message per second per vehicle. Derived from the hsl-hfp feeder schema published in the xRegistry catalogue.",
  "type": "object",
  "definitions": {
    "OperatingDayClockPosition": {
      "name": "OperatingDayClockPosition",
      "type": "object",
      "description": "Meta-type for the HSL operating-day regime. A position is located by an operating day and a departure time within that day. The operating day is not a calendar day: it ends at approximately 04:30 local time on the following calendar date, so a trip that departs at 00:30 carries the previous date as its operating day and a departure time of `00:30` that occurs after every larger clock time on the same operating day. A position is therefore not an RFC 3339 civil instant and MUST NOT be compared with one without applying the regime. Because the clock component wraps within a position, ordering on the raw `start` string is wrong; the `ordinal` member renders the day and the minutes elapsed since the start of the operating day at fixed width, most significant first, so that positions sort correctly under lexical order without implementing this definition. Positions increase with time, so the ordering is forward.",
      "properties": {
        "ordinal": {
          "type": "string",
          "description": "Position rendered at fixed width, most significant first: YYYY-MM-DD/MMMM, where the second component is the count of minutes elapsed since 04:30 local time on the operating day, zero-padded to four digits. Example: 2026-07-30/1200 for a departure at 00:30 on 31 July.",
          "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}/[0-9]{4}$"
        },
        "oday": {
          "type": "date",
          "description": "Operating day of the trip from the HFP payload `oday` field, in `YYYY-MM-DD`. It looks like a calendar date and is not one: it labels the service day that the trip belongs to, and the service day runs past midnight into the following calendar date."
        },
        "start": {
          "type": "string",
          "description": "Scheduled departure from the first stop of the trip from the HFP payload `start` field, in `HH:mm` 24-hour local time. It is a clock reading within the operating day named by `oday`, not a time of day on that calendar date.",
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
      ],
      "description": "Method that produced the reported position."
    }
  },
  "properties": {
    "veh": {
      "type": "int32",
      "description": "Vehicle number painted on the side of the vehicle, from the HFP payload `veh` field. It is unique only in combination with `oper`, so the pair identifies the physical vehicle whose motion this record reports."
    },
    "oper": {
      "type": "int32",
      "description": "Numeric identifier of the operator running the trip, from the HFP payload `oper` field. This is the operator that actually operates the service and MAY differ from the owning operator carried on the MQTT topic when a service is subcontracted."
    },
    "tst": {
      "type": "datetime",
      "description": "UTC timestamp with millisecond precision generated by the vehicle, from the HFP payload `tst` field. It is the instant at which the vehicle sampled the state reported by this record."
    },
    "journey_start": {
      "type": {
        "$ref": "#/definitions/OperatingDayClockPosition"
      },
      "description": "Scheduled departure of this trip from its first stop, carried in the native HFP encoding as an operating day and a clock reading within it. The pair identifies the trip and is the anchor that `dl` is measured against. The OperatingDayClockPosition meta-type declares the regime, because the operating day does not coincide with the calendar day and the clock reading wraps within a single operating day."
    },
    "desi": {
      "type": "string",
      "description": "Route number shown to passengers on the head sign, from the HFP payload `desi` field, for example `551` or `H72`. It is a display label and is not the GTFS route identifier."
    },
    "route": {
      "type": "string",
      "description": "GTFS route identifier the vehicle is currently running on, from the HFP payload `route` field."
    },
    "dir": {
      "type": "string",
      "enum": [
        "1",
        "2"
      ],
      "description": "Direction of travel along the route, from the HFP payload `dir` field, carried as a string rather than a number. Neither value names a compass bearing."
    },
    "lat": {
      "type": "double",
      "description": "WGS84 latitude of the vehicle in decimal degrees, from the HFP payload `lat` field. Omitted when the vehicle location is unavailable."
    },
    "long": {
      "type": "double",
      "description": "WGS84 longitude of the vehicle in decimal degrees, from the HFP payload `long` field. Omitted when the vehicle location is unavailable."
    },
    "loc": {
      "type": {
        "$ref": "#/definitions/LocEnum"
      },
      "description": "Source of the reported position, from the HFP payload `loc` field. It is the procedure that produced `lat` and `long`, and it changes without warning between messages of the same trip: a value of `ODO` or `DR` means the coordinates were propagated from the odometer or from other onboard sensors rather than fixed by satellite, and a value of `MAN` means a human entered them."
    },
    "spd": {
      "type": "double",
      "description": "Instantaneous ground speed of the vehicle in metres per second, from the HFP payload `spd` field."
    },
    "hdg": {
      "type": "int32",
      "minimum": 0,
      "maximum": 360,
      "description": "Heading of the vehicle in degrees clockwise from geographic north, from the HFP payload `hdg` field."
    },
    "acc": {
      "type": "double",
      "description": "Acceleration in metres per second squared, from the HFP payload `acc` field. The vehicle does not measure it: it is the difference between this speed sample and the previous one divided by the interval between them, so it inherits the noise of both samples and is undefined for the first message of a trip. The interval it characterizes closes at `tst` and opens at the timestamp of the preceding message, which this record does not carry, and its length varies with the actual spacing of messages. No `supportPeriod` is declared because there is no length to state, and the extent of the period is indeterminate from the record alone. The one-second cadence on `tst` says what the vehicle is expected to emit next and does not bound this interval."
    },
    "odo": {
      "type": "int32",
      "minimum": 0,
      "description": "Odometer reading in metres, from the HFP payload `odo` field. It is not a lifetime total: the counter is reset when the vehicle actually begins the trip, so the value accumulates from that reset up to `tst`. The reset instant is not carried by this record. `journey_start` holds the scheduled departure, which is a `scheduledTime` and does not supply a phenomenon-time boundary, and `dl` measures precisely the discrepancy between the schedule and the vehicle's actual running. The length of the accumulation therefore differs from message to message and from vehicle to vehicle, so no `supportPeriod` is declared and the opening boundary of the period is indeterminate from the record."
    },
    "dl": {
      "type": "int32",
      "description": "Deviation from the published timetable in seconds, from the HFP payload `dl` field. The sign convention is the opposite of the usual one: a negative value means the vehicle is running late and a positive value means it is running early. The value is computed by the onboard system against the schedule anchored at `journey_start`."
    },
    "stop": {
      "type": "int32",
      "description": "Numeric GTFS identifier of the stop this event relates to, from the HFP payload `stop` field. On a `vp` event it names the stop the vehicle most recently departed from, and it is absent between the end of one stop relation and the start of the next."
    },
    "ttarr": {
      "type": "datetime",
      "description": "Timetabled arrival at the stop named by `stop`, from the HFP payload `ttarr` field, normalised by the publisher to a UTC instant. It is a planned time, not an observed one, and it is populated only while the vehicle stands in a stop relation."
    },
    "ttdep": {
      "type": "datetime",
      "description": "Timetabled departure from the stop named by `stop`, from the HFP payload `ttdep` field, normalised by the publisher to a UTC instant. It is a planned time, not an observed one, and it never precedes `ttarr`."
    },
    "drst": {
      "type": "int32",
      "enum": [
        0,
        1
      ],
      "description": "Door state at `tst`, from the HFP payload `drst` field. It is a state of the vehicle rather than a quantity, and it is absent when the onboard system cannot determine it."
    },
    "occu": {
      "type": "int32",
      "minimum": 0,
      "maximum": 100,
      "description": "Passenger occupancy as a percentage of capacity, from the HFP payload `occu` field. Only Suomenlinna ferries report a measured value; every other vehicle class transmits a constant, so a consumer must know the transport mode before reading it."
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
