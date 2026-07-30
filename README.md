<!-- regenerate: on (set to off if you edit this file) -->

# JSON Structure: Characteristics

This is the working area for the individual Internet-Draft, "JSON Structure:
Characteristics".

* [Editor's Copy](https://json-structure.github.io/characteristics/#go.draft-vasters-json-structure-characteristics.html)
* [Datatracker Page](https://datatracker.ietf.org/doc/draft-vasters-json-structure-characteristics)
* [Individual Draft](https://datatracker.ietf.org/doc/html/draft-vasters-json-structure-characteristics)
* [Compare Editor's Copy to Individual Draft](https://json-structure.github.io/characteristics/#go.draft-vasters-json-structure-characteristics.diff)


## Contributing

See the
[guidelines for contributions](https://github.com/json-structure/units/blob/main/CONTRIBUTING.md).

Contributions can be made by creating pull requests.
The GitHub interface supports creating pull requests using the Edit (✏) button.


## Scope and Non-goals

Scope:

* Defines optional annotations for observation-oriented semantics in JSON
	Structure schemas: `semanticRole`, `observedProperty`, `phenomenonTimeRelation`,
	`derivation`, `temporalReferenceSystem`, `cadence`,
	`coordinateReferenceSystem`, and `linearReferenceSystem`.
* Covers roles for observation results, time semantics, quality,
	feature-of-interest variants, and observing procedure.
* Defines bindings for temporal, coordinate, and linear reference systems.
* Defines derivation and cadence annotations for result interpretation.

Non-goals:

* It is not a full ISO 19156 model or a normative JSON encoding of that model.
* It does not define complete vocabularies for observed properties,
	procedures, quality values, or features of interest.
* It does not define identity or general relationship semantics
	(see JSON Structure Relations).
* It does not define units or conversion behavior
	(see JSON Structure Units).
* It does not define statistics, analytical methods, causal interpretation,
	execution policy, governance policy, or lineage policy.

Reference alignment:

* Observation concepts align with ISO 19156 and OGC Topic 20.
* Temporal terminology draws on ISO 19108, OGC Topic 25, ISO 19111 temporal
	CRS provisions, and GML 3.2.1 temporal schemas.


## Command Line Usage

Formatted text and HTML versions of the draft can be built using `make`.

```sh
$ make
```

Command line usage requires that you have the necessary software installed.  See
[the instructions](https://github.com/martinthomson/i-d-template/blob/main/doc/SETUP.md).
