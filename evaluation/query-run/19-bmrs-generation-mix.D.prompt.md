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


You also have the specification that defines the annotation keywords used by
this schema. It is the file `specification.md` in this same directory. Read it, and use it
to interpret any keyword you do not recognise. Where the specification states a
rule about what may or may not be inferred from a keyword, that rule governs
your answer.


---

schema.json

```json
{
  "$schema": "https://json-structure.org/meta/semantic-annotations/v0/#",
  "$id": "https://example.invalid/schema",
  "$uses": [
    "JSONStructureSemanticAnnotations"
  ],
  "name": "GenerationMix",
  "description": "The half-hourly generation outturn summary for the GB transmission system, published by Elexon on the Balancing Mechanism Reporting Service. Derived from the elexon-bmrs feeder schema published in the xRegistry catalogue.",
  "type": "object",
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/transmission-system-generation-mix/v1",
    "kind": "example-catalog"
  },
  "properties": {
    "settlement_period": {
      "type": "int32",
      "minimum": 1,
      "maximum": 50,
      "description": "GB settlement period number within the settlement day, from the `settlement_period` field. Periods are half an hour long and are numbered from 1 at midnight UTC. The count per day is not constant: a settlement day has 48 periods normally, 46 on the spring clock change and 50 on the autumn one, so the period number does not map to a fixed clock time and arithmetic on it across a clock change is wrong.",
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/identifier",
          "kind": "dcterms-property"
        }
      ]
    },
    "start_time": {
      "type": "datetime",
      "description": "UTC instant at which the settlement period begins, from the `start_time` field. The feed carries no end instant. The period is half an hour long and half-open, and each value member states that length in its own `supportPeriod` anchored on this position; the cadence declared here says what the publisher is expected to do next and does not bound the period any value applies to.",
      "semanticRole": "phenomenonTimeStart",
      "cadence": {
        "kind": "fixed",
        "period": "PT30M"
      }
    },
    "ccgt_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of combined-cycle gas turbine plant over the settlement period. CCGT units burn gas in a turbine and raise steam from the exhaust; they are the bulk gas fleet and are dispatched for energy.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "ocgt_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of open-cycle gas turbine plant over the settlement period. OCGT units burn the same fuel as CCGT but recover no exhaust heat; they run for minutes at a time as reserve, so a value here and a value in `ccgt_mw` describe operationally unrelated fleets.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "coal_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of coal-fired plant over the settlement period.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "oil_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of oil-fired plant over the settlement period.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "nuclear_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of nuclear plant over the settlement period.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "wind_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of wind farms over the settlement period, onshore and offshore combined. It covers only the units that are metered in the Balancing Mechanism, so wind connected to distribution networks is absent and the value understates GB wind generation.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "biomass_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of biomass-fuelled plant over the settlement period, including units converted from coal.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "npshyd_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of non-pumped-storage hydroelectric plant over the settlement period: run-of-river and reservoir schemes that generate from natural inflow. It is disjoint from `ps_mw`, and the two are separated because only one of them is a store.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "ps_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output of pumped-storage hydroelectric plant over the settlement period. The units both generate and consume, and the pumping load does not appear here as a negative value; it is metered as demand elsewhere in the settlement data, so this member is not a net position.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "other_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean output over the settlement period of metered plant whose fuel type BMRS does not report separately.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "intfr_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean net flow over the settlement period on the IFA interconnector to France. This is a cable and not a fuel: the value is signed, positive when GB is importing and negative when it is exporting, so it may not be summed with the generation members without deciding how exports are to be treated.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "intifa2_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean net flow over the settlement period on the IFA2 interconnector to France, signed positive for import to GB. IFA and IFA2 are separate cables with separate capacities and are reported separately.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "intned_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean net flow over the settlement period on the BritNed interconnector to the Netherlands, signed positive for import to GB.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "intnem_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean net flow over the settlement period on the Nemo Link interconnector to Belgium, signed positive for import to GB.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "intelec_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean net flow over the settlement period on the East-West interconnector to Ireland, signed positive for import to GB. The code reads as an abbreviation of electricity and names a specific cable.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "intnsl_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean net flow over the settlement period on the North Sea Link interconnector to Norway, signed positive for import to GB.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    },
    "intvkl_mw": {
      "type": "double",
      "unit": "MW",
      "description": "Mean net flow over the settlement period on the Viking Link interconnector to Denmark, signed positive for import to GB.",
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean",
      "phenomenonTimeRelation": "interval",
      "supportPeriod": {
        "length": "PT30M",
        "anchor": "start"
      },
      "observedProperty": {
        "reference": "http://qudt.org/vocab/quantitykind/Power",
        "kind": "qudt-quantity-kind"
      }
    }
  },
  "required": [
    "settlement_period",
    "start_time"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "settlement_period": 12,
  "start_time": "2026-07-31T05:30:00Z",
  "ccgt_mw": 9412.0,
  "ocgt_mw": 0.0,
  "coal_mw": 0.0,
  "oil_mw": 0.0,
  "nuclear_mw": 3908.0,
  "wind_mw": 6231.0,
  "biomass_mw": 2104.0,
  "npshyd_mw": 318.0,
  "ps_mw": 742.0,
  "other_mw": 156.0,
  "intfr_mw": 1980.0,
  "intifa2_mw": 1010.0,
  "intned_mw": 998.0,
  "intnem_mw": -412.0,
  "intelec_mw": -184.0,
  "intnsl_mw": 1394.0,
  "intvkl_mw": 802.0
}
```
