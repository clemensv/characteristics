You are handed a data feed you have never seen before, and asked to put it to
work.

The directory you have been given contains exactly two files: a schema and one
example record that conforms to it. Read only those two files. You have no
network, no search, no other documents, and no access to any specification.

Write **one** streaming SQL query, in the dialect of Azure Stream Analytics —
the same dialect the SQL operator of Microsoft Fabric Eventstream accepts — that
computes what you judge to be the **five most valuable derived metrics** this
stream supports.

A derived metric is computed, not carried. An aggregate over a window, a rate of
change, a difference between successive records, a ratio, a residual against a
declared reference, a flag raised by a threshold: those are derived. A field
copied from the record to the output is not, and does not count towards the
five.

Produce, in this order:

1. **The five metrics.** One line each: what it is, and why an operator of this
   feed would want it. Order them by how valuable you think they are.
2. **The query.** A single statement, using `WITH ... AS` for intermediate
   steps. It must:
   * declare the event time explicitly with `TIMESTAMP BY`, naming the member
     you have chosen and no other;
   * name the window type and size wherever it aggregates;
   * partition by whatever identifies an individual source, if anything does.
3. **What you did not compute.** Any aggregation, comparison or combination you
   considered and deliberately left out, and the reason. Be specific: name the
   members involved.
4. **Assumptions.** Anything the query relies on that the two files do not
   establish. Mark each one as an assumption.

Notes on the dialect, so that you are not judged on syntax you cannot look up.
`SELECT ... INTO output FROM input TIMESTAMP BY <member>` is the shape of a
statement. Windows are `TumblingWindow(minute, 5)`, `HoppingWindow(minute, 5, 1)`,
`SlidingWindow(minute, 5)` and `SessionWindow(minute, 5, 60)`, and appear in the
`GROUP BY`. `System.Timestamp()` is the end of the current window. `LAG(expr, 1)
OVER (PARTITION BY k LIMIT DURATION(minute, 10))` reaches the previous event and
the `LIMIT DURATION` is required. `DATEDIFF(second, a, b)` differences two
timestamps. The usual aggregates are available, including `STDEV` and
`PERCENTILE_CONT`. If you need something the dialect lacks, write plain SQL and
say in a comment that you are unsure it is supported.

Two rules govern the whole answer.

Do not invent facts about the domain that the two files do not establish. If the
files do not license an aggregation, do not write it. Choosing not to compute
something, and saying why, is a correct answer and is worth more than a metric
that looks impressive and is unsound.

Do not pad. Five metrics, not eight. A query that computes fewer things
correctly beats one that computes more things wrongly.


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
