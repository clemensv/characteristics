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
