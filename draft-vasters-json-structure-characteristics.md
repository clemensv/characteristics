---
title: "JSON Structure: Characteristics"
abbrev: "JSON Structure Characteristics"
category: exp

docname: draft-vasters-json-structure-characteristics-latest
submissiontype: IETF
number:
date: 2026-07-28
consensus: false
v: 3
area: Web and Internet Transport
workgroup: Building Blocks for HTTP APIs
keyword: Internet-Draft
venue:
  github: "json-structure/characteristics"
  latest: "https://json-structure.github.io/characteristics/draft-vasters-json-structure-characteristics.html"

author:
  - fullname: Clemens Vasters
    organization: Microsoft Corporation
    email: clemensv@microsoft.com

normative:
  RFC3339:
  RFC3986:
  JSTRUCT-CORE:
    title: "JSON Structure Core"
    author:
      - fullname: Clemens Vasters
    target: https://json-structure.github.io/core/draft-vasters-json-structure-core.html
  JSTRUCT-UNITS:
    title: "JSON Structure: Symbols, Scientific Units, and Currencies"
    author:
      - fullname: Clemens Vasters
    target: https://json-structure.github.io/units/draft-vasters-json-structure-units.html
  ISO19108:
    title: "ISO 19108:2002 Geographic information - Temporal schema"
    author:
      - org: International Organization for Standardization
    date: 2002
    target: https://www.iso.org/standard/26013.html
  ISO19111:
    title: "ISO 19111:2019 Geographic information - Referencing by coordinates"
    author:
      - org: International Organization for Standardization
    date: 2019
    target: https://www.iso.org/standard/74039.html
  ISO19148:
    title: "ISO 19148:2021 Geographic information - Linear referencing"
    author:
      - org: International Organization for Standardization
    date: 2021
    target: https://www.iso.org/standard/75147.html
  ISO19156:
    title: "ISO 19156:2023 Geographic information - Observations, measurements and samples"
    author:
      - org: International Organization for Standardization
    date: 2023
    target: https://www.iso.org/standard/82463.html
  OGC-NAMES:
    title: "OGC Name Type Specification - definitions - part 1 - basic name"
    author:
      - org: Open Geospatial Consortium
    target: https://docs.ogc.org/pol/09-048r6.html

informative:
  JSTRUCT-RELATIONS:
    title: "JSON Structure: Relations"
    author:
      - fullname: Clemens Vasters
    target: https://json-structure.github.io/relations/draft-vasters-json-structure-relations.html
  JSTRUCT-IMPORT:
    title: "JSON Structure: Import"
    author:
      - fullname: Clemens Vasters
    target: https://json-structure.github.io/import/draft-vasters-json-structure-import.html
  OGC-TOPIC2:
    title: "OGC Abstract Specification Topic 2: Referencing by coordinates"
    author:
      - org: Open Geospatial Consortium
    date: 2019
    target: https://docs.ogc.org/as/18-005r4/18-005r4.html
  OGC-TOPIC25:
    title: "OGC Abstract Specification Topic 25: Abstract Conceptual Model for Time"
    author:
      - org: Open Geospatial Consortium
    target: https://docs.ogc.org/as/23-049/23-049.html
  QUDT:
    title: "QUDT Ontologies"
    author:
      - org: QUDT.org
    target: https://www.qudt.org/
  CF-STANDARD-NAMES:
    title: "CF Standard Name Table"
    author:
      - org: CF Conventions
    target: https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html
  SOSA-SSN:
    title: "Semantic Sensor Network Ontology"
    author:
      - org: World Wide Web Consortium
    target: https://www.w3.org/TR/vocab-ssn/
  RDF-CONCEPTS:
    title: "RDF 1.1 Concepts and Abstract Syntax"
    author:
      - org: World Wide Web Consortium
    target: https://www.w3.org/TR/rdf11-concepts/
  RDF-SCHEMA:
    title: "RDF Schema 1.1"
    author:
      - org: World Wide Web Consortium
    target: https://www.w3.org/TR/rdf-schema/
  OWL2:
    title: "OWL 2 Web Ontology Language Document Overview"
    author:
      - org: World Wide Web Consortium
    target: https://www.w3.org/TR/owl2-overview/
  SKOS:
    title: "SKOS Simple Knowledge Organization System Reference"
    author:
      - org: World Wide Web Consortium
    target: https://www.w3.org/TR/skos-reference/
  DCTERMS:
    title: "DCMI Metadata Terms"
    author:
      - org: Dublin Core Metadata Initiative
    target: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
  EPSG:
    title: "EPSG Geodetic Parameter Dataset"
    author:
      - org: International Association of Oil and Gas Producers
    target: https://epsg.org/
  WSDOT-LRS:
    title: "State Route Linear Referencing System"
    author:
      - org: Washington State Department of Transportation
    target: https://data.wsdot.wa.gov/arcgis/rest/services/Shared/LRSData/FeatureServer/9
  WSDOT-LRS-METADATA:
    title: "Washington State LRS metadata"
    author:
      - org: Washington State Department of Transportation
    target: https://data.wsdot.wa.gov/arcgis/rest/services/Shared/LRSData/FeatureServer/9/metadata?f=json
  WSDOT-MILEPOST:
    title: "Milepost Values metadata"
    author:
      - org: Washington State Department of Transportation
    target: https://data.wsdot.wa.gov/arcgis/rest/services/Shared/MilepostValues/FeatureServer/2/metadata?f=json
  WSDOT-CRAB:
    title: "County Road Administration Board Routes"
    author:
      - org: Washington State Department of Transportation
    target: https://data.wsdot.wa.gov/arcgis/rest/services/Shared/CRABRoutes/FeatureServer
  CALTRANS-LRS:
    title: "All Roads Linear Referencing System"
    author:
      - org: California Department of Transportation
    target: https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHhighway/All_Roads/FeatureServer
  FHWA-ARNOLD:
    title: "All Road Network of Linear Referenced Data"
    author:
      - org: Federal Highway Administration
    target: https://www.fhwa.dot.gov/policyinformation/hpms/arnold.cfm
  FHWA-HPMS:
    title: "Highway Performance Monitoring System Field Manual"
    author:
      - org: Federal Highway Administration
    target: https://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/
  INSPIRE-TN:
    title: "INSPIRE Data Specification on Transport Networks - Technical Guidelines"
    author:
      - org: European Commission
    target: https://inspire.ec.europa.eu/id/document/tg/tn
  UIC-RTM:
    title: "IRS 90940 RailTopoModel"
    author:
      - org: International Union of Railways
    target: https://uic.org/rail-system/railtopomodel/
  PDOK-NWB:
    title: "Nationaal Wegenbestand - Wegen WFS"
    author:
      - org: Rijkswaterstaat
    target: https://service.pdok.nl/rws/nwbwegen/wfs/v1_0?service=WFS&request=GetCapabilities
  NVDB-NO:
    title: "Nasjonal vegdatabank API Les v4"
    author:
      - org: Statens vegvesen
    target: https://nvdbapiles.atlas.vegvesen.no/
  NVDB-SE:
    title: "Nationell vagdatabas"
    author:
      - org: Trafikverket
    target: https://lastkajen.trafikverket.se/

--- abstract

Data types describe representation, but they do not explain the semantic,
temporal, spatial, and operational characteristics needed to interpret and
compare data. This document defines optional JSON Structure annotations that
bind schema nodes to terms in external vocabularies, and annotations for
observation results, observed properties, features of interest, procedures,
time semantics, quality, derivation, cadence, and spatial referencing.

The annotations provide progressively richer evidence. Their absence does not
make a schema invalid, and the annotations do not define analytical procedures,
expressions, causal inference, execution policy, or lineage.

--- middle

# Introduction {#introduction}

A schema states how a value is written. It gives a type, and with JSON Structure
Units {{JSTRUCT-UNITS}} it gives a unit, so that a reader knows a member holds a
number of metres. It does not state what the number measures, what the metres
are measured from, or when the measurement applies. Two schemas can agree on
`double` and on `m` and still describe water level above a tide-gauge datum and
height above an ellipsoid, which are not the same quantity and must not be
compared. That difference is usually recorded in prose documentation, inferred
from a member name, or known only to the people who built the system.

This document is an extension to JSON Structure Core {{JSTRUCT-CORE}} that
records it in the schema, by annotation, without changing what the schema
validates. Its keywords let a schema author bind a type or member to a term in a
published vocabulary, so that two systems naming a thing differently can
establish that they mean the same thing; declare what a record observes and
which member carries the result, as distinct from the property observed, the
feature it belongs to, the procedure that produced it, and the time it applies
to; and name the reference system a value is expressed against, whether a
temporal regime, a coordinate reference system, or a linear reference system, so
that a position can be interpreted and two positions can be compared.

Each of these is a binding to a definition maintained elsewhere. This document
defines no vocabulary, no observation model, and no reference system of its own.
Established bodies publish them, and an annotation refers to one. What is
defined here is the form of that reference, the roles a schema may assign to its
own members, and the rules by which a processor can check that the two agree.

The annotations are optional and additive. A processor that does not implement
them reads the schema exactly as JSON Structure Core defines it.

## Semantic Binding and External Definitions {#semantic-binding}

Most keywords defined here share one shape. Each is an object carrying a
`reference` property that identifies a definition and a `kind` property that
names the model the definition belongs to. The `reference` states which
definition applies, and the `kind` states which model defines it, so that a
reader knows how to interpret it and a processor knows what can be checked.
`concepts`, `observedProperty`, `temporalReferenceSystem`,
`coordinateReferenceSystem`, and `linearReferenceSystem` all follow this shape.

A definition is ordinarily maintained outside the schema, and `reference` is
then an absolute URI {{RFC3986}}. The reference-system keywords also admit a
definition held in the schema itself, carried by a shareable type that
{{meta-types}} calls a meta-type; `kind` is then `type` and `reference` is a
JSON Pointer to that type. The `kind` determines which form applies, and each
keyword states the rule for its own values.

A `kind` names a definition model and not the format of the resource that
carries it. The enumerations are open so that an author whose model is not
already named can name it.

The annotations bind terms; they do not express statements, node identity, or
entailment, and this document defines no prefix mechanism and no compact URI
form.

A value is read against one reference system and quantifies one phenomenon, so
the reference-system keywords and `observedProperty` each take a single binding.
Vocabularies overlap by design, and the same notion is deliberately given a term
in several of them, so `concepts` takes a list. It is the only keyword defined
here that admits more than one binding.

## Observable and Observed Property Concepts {#observable-observed-concepts}

Observation is one application of the general model in {{semantic-binding}}. An
*observable property definition* is the externally governed concept, such as
water level or bridge vibration, and this document defines no format for one.
An *observed property declaration* is the `observedProperty` annotation that
binds one record shape to one such definition.

An observation act is one concrete execution of an observing procedure for one
declared observed property and feature context, producing one result value and
optionally its qualifiers.

# Conventions {#conventions}

{::boilerplate bcp14-tagged}

# Annotation Model {#annotation-model}

`concepts` MAY occur on a type definition and on a property, collection item,
map value, or choice member schema, subject to {{vocabulary-characteristics}}.

`semanticRole`, `derivation`, `temporalReferenceSystem`, and `cadence` MAY occur
directly on a property, collection item, map value, or choice member schema,
subject to {{observation-characteristics}}. `phenomenonTimeRelation` MAY occur on a
direct property. `statistic` MAY occur wherever `derivation` occurs, subject to
{{statistic}}. `temporalReferenceSystem` MAY also occur on an object or tuple
that defines a temporal type, and binds an existing member of it.

`observedProperty` MAY occur on an object or tuple intended to describe an
observation record, and on a member schema of one that carries a result,
subject to {{observed-property}}.
`coordinateReferenceSystem` and `linearReferenceSystem` MAY occur on an object
or tuple and bind existing properties. `referenceRole` MAY occur on a member of
a meta-type, subject to {{meta-types}}.

All keywords defined here are direct peer keywords, and no wrapper is implied.
Every annotation is OPTIONAL, and a schema can use any subset, including none.
Conformance constrains only annotations that are present; it never requires
another annotation or an annotated property to exist.

Every `reference` value that is a URI SHOULD be resolvable, and dereferencing it
SHOULD yield a definition of the identified term or system. That recommendation
constrains the URI a schema author chooses. A processor is not required to
dereference a `reference`, and an unresolved `reference` is indeterminate rather
than incorrect.

The enumerations of this document are of two sorts. `semanticRole`,
`derivation`, `statistic`, `phenomenonTimeRelation`, `referenceRole`,
`sortOrder`, and the `kind` of `cadence` are closed, and a value outside the
enumeration is invalid. The `kind` of a reference-style keyword is open, and a
value outside the enumeration is valid; a processor MUST preserve it and MUST
NOT reject a schema for carrying it.

What a processor can verify follows that division. A value defined here is one a
processor can act on, and this document states what each establishes. A value
not defined here establishes nothing, and a processor MUST NOT infer a
constraint from it. This document defines no registry of further values and no
mechanism by which a private value acquires meaning for a processor that does
not already know it.

| Keyword | Meaning |
|---|---|
| `concepts` | Terms in external vocabularies that the annotated node corresponds to. |
| `semanticRole` | Function of a result, temporal, quality, status, or operational value. |
| `observedProperty` | Reference to an observable-property definition. |
| `phenomenonTimeRelation` | Refinement of how a result relates to `phenomenonTime`. |
| `derivation` | Category describing how a result value was produced. |
| `statistic` | Summary function that produced a result from a set of values. |
| `temporalReferenceSystem` | Binding from a temporal-position encoding to its reference definition. |
| `cadence` | Expected pattern of successive temporal positions. |
| `coordinateReferenceSystem` | CRS and ordered properties forming a coordinate. |
| `linearReferenceSystem` | LRS and properties forming a location along a linear element. |
| `referenceRole` | Function of a member within a reference-system meta-type. |

Omission means undeclared unless stated otherwise. It never implies compatible,
successful, or acceptable data.

# Vocabulary Characteristics {#vocabulary-characteristics}

## The `concepts` Keyword {#concepts}

The `concepts` keyword binds the annotated node to terms defined by external
vocabularies, following the model in {{semantic-binding}}. In this document a
concept is any term that a vocabulary defines, including a class, a property, or
a SKOS concept {{SKOS}}. The `skos-concept` kind names one such term type and
places no constraint on the others.

When present, `concepts` MUST be a non-empty array of objects. Each object MUST
have a REQUIRED `reference` string and a REQUIRED `kind` string. No other
properties are permitted.

The array is unordered and no entry is primary. Every entry holds
simultaneously: the annotated node corresponds to all of the terms listed, and a
reader does not select among them. Two entries MUST NOT carry the same
`reference`.

### The `reference` Property

`reference` MUST be an absolute URI {{RFC3986}} that identifies one term. The
URI is the identifier that the vocabulary assigns to the term. This document
defines no prefix mechanism, no compact form, and no resolution protocol.

### The `kind` Property

`kind` classifies which definition model the URI identifies. It is an open
enumeration. The following values are defined:

| Value | Referenced definition |
|---|---|
| `rdfs-class` | A class in RDF Schema {{RDF-SCHEMA}}. |
| `rdf-property` | An RDF property {{RDF-CONCEPTS}}. |
| `owl-class` | A class in OWL 2 {{OWL2}}. |
| `owl-object-property` | An OWL 2 object property. |
| `owl-datatype-property` | An OWL 2 datatype property. |
| `skos-concept` | A concept in a SKOS concept scheme {{SKOS}}. |
| `dcterms-property` | A property in DCMI Metadata Terms {{DCTERMS}}. |

Other values MAY identify further definition models. {{vocabulary-uris}} lists
namespace URIs for the vocabularies named above.

### Type Compatibility {#concept-type-compatibility}

A `kind` denotes either a class or a property, and the two attach to different
schema nodes:

* `rdfs-class` and `owl-class` denote a class, and the annotation MUST occur on
  a type definition.
* `rdf-property`, `owl-object-property`, `owl-datatype-property`, and
  `dcterms-property` denote a property, and the annotation MUST occur on a
  property, collection item, map value, or choice member schema.
* `skos-concept` denotes neither, and the annotation MAY occur on either.

All entries of one `concepts` array MUST agree. An array MUST NOT combine an
entry whose `kind` denotes a class with an entry whose `kind` denotes a
property. A `kind` outside the values defined above establishes no constraint,
and a processor MUST NOT infer one.

### Relationship to `observedProperty` {#concepts-and-observed-property}

`concepts` states which external terms the annotated node corresponds to.
`observedProperty` states which phenomenon a record quantifies. Where the term
is an observable-property definition, `observedProperty` carries it and
`concepts` MUST NOT name it. The same URI MUST NOT appear in both keywords on
one node.

Correspondences between one observable-property definition and terms in other
vocabularies belong to the definition and are recorded once there, as described
in {{observable-property-mappings}}. They are not repeated as `concepts` entries
in every schema that cites the definition.

A binding is a statement about meaning and not about resolution. A missing or
unresolved term is indeterminate and MUST NOT be repaired from property names,
descriptions, labels, or samples.

Example:

~~~ json
{
  "name": "TideGaugeReading",
  "type": "object",
  "description": "One water-level reading from a coastal tide gauge.",
  "concepts": [
    {
      "reference": "http://www.w3.org/ns/sosa/Observation",
      "kind": "owl-class"
    }
  ],
  "observedProperty": {
    "reference": "https://vocab.nerc.ac.uk/collection/P01/current/ASLVZZ01/",
    "kind": "nerc-p01"
  },
  "properties": {
    "waterLevel": {
      "type": "double",
      "unit": "m",
      "description": "Height of the water surface above chart datum.",
      "examples": [2.41],
      "semanticRole": "observationValue",
      "concepts": [
        {
          "reference": "http://www.w3.org/ns/sosa/hasSimpleResult",
          "kind": "rdf-property"
        }
      ]
    },
    "issued": {
      "type": "datetime",
      "description": "Instant at which the reading was published.",
      "examples": ["2026-03-11T08:15:00Z"],
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/issued",
          "kind": "dcterms-property"
        },
        {
          "reference": "http://www.w3.org/ns/prov#generatedAtTime",
          "kind": "rdf-property"
        }
      ]
    }
  }
}
~~~

# Observation Characteristics {#observation-characteristics}

## The `observedProperty` Keyword {#observed-property}

The `observedProperty` keyword identifies the observable-property definition
associated with an observation record, or with one result within it, as
introduced in {{observable-observed-concepts}}.

When present, `observedProperty` MUST be an object with a REQUIRED `reference`
string and a REQUIRED `kind` string. No other properties are permitted.

### The `reference` Property

`reference` MUST be an absolute URI {{RFC3986}} that identifies one immutable
observable-property definition. Version identity, when used, is implied by the
URI itself, and a materially different concept MUST be identified by a
different URI. The URI SHOULD deep-link to one concrete definition entry in the
selected vocabulary. This document does not define a resolution protocol, URI
layout, storage model, or catalog serialization.

### The `kind` Property

`kind` classifies which definition model the URI identifies. It is an open
enumeration, and a value identifies the vocabulary or catalog type that
publishes the definition.

Examples of catalog types include:

* `cf-standard-name` for URIs identifying entries from the CF Standard Name
  Table, for example a URI identifying `air_temperature`;
* `nerc-p01` for entries from the NERC Vocabulary Server Parameter Usage
  Vocabulary (P01) identified by dereferenceable concept URIs.

An organization that publishes its own catalog names its own model. The examples
in this document use `example-catalog` where the cited catalog is fictional.

Example:

~~~ json
{
  "observedProperty": {
    "reference": "https://vocab.nerc.ac.uk/collection/P01/current/CTMPZZ01/",
    "kind": "nerc-p01"
  }
}
~~~

### Attachment and Scope

`observedProperty` MAY occur on an object or tuple that describes an observation
record, and on a member schema of that object or tuple that carries a result.

On a record it identifies the observable property of every result in that record
that does not carry one of its own. On a result member it identifies the
observable property of that result alone and takes precedence over the record's.
A record whose results observe different properties therefore carries one
`observedProperty` on each such result, and a record whose results all observe
the same property carries one on the record.

Every annotation identifies exactly one observable property for the node it is
attached to. A missing or unresolved reference is indeterminate and MUST NOT be
repaired from labels, mappings, result schemas, units, descriptions, property
names, or samples.

The feature, procedure, and temporal roles of a record are shared by every
result in it. Where a record carries more than one result, a `resultQuality` on
the record qualifies all of them, and qualifying one result on its own requires
modelling that result as a nested object.

Example of a record with two results:

~~~ json
{
  "name": "BuoySurfacePacket",
  "type": "object",
  "properties": {
    "buoy_id": {
      "type": "string",
      "semanticRole": "featureOfInterest"
    },
    "measured_at": {
      "type": "datetime",
      "description": "Time both results occurred",
      "examples": ["2026-07-27T12:00:00Z"],
      "semanticRole": "phenomenonTime"
    },
    "sea_surface_temperature": {
      "type": "double",
      "unit": "Cel",
      "examples": [18.4],
      "semanticRole": "observationValue",
      "observedProperty": {
        "reference": "https://vocab.nerc.ac.uk/collection/P01/current/CTMPZZ01/",
        "kind": "nerc-p01"
      }
    },
    "practical_salinity": {
      "type": "double",
      "unit": "1",
      "examples": [35.1],
      "semanticRole": "observationValue",
      "observedProperty": {
        "reference": "https://vocab.nerc.ac.uk/collection/P01/current/PSLTZZ01/",
        "kind": "nerc-p01"
      }
    }
  },
  "required": ["buoy_id", "measured_at", "sea_surface_temperature", "practical_salinity"],
  "additionalProperties": false
}
~~~

The two results share one feature and one phenomenon time, and each names the
property it quantifies.

## Semantic Mappings and Result Hints {#observable-property-mappings}

An authority MAY publish semantic mappings from an observable-property
definition to other identified concepts, using relation kinds such as
`exactMatch`, `closeMatch`, `broader`, `narrower`, `related`, and
`quantityKind`. Mapping targets MUST be absolute URIs, and a mapping SHOULD
carry a review state such as `proposed`, `reviewed`, or `rejected`.

Only a reviewed `exactMatch` can provide evidence that two distinct identifiers
denote the same observable property. `closeMatch`, hierarchy, relatedness,
label similarity, and quantity-kind classification do not establish
equivalence, and no mapping alone authorizes execution.

A `quantityKind` mapping can reference a QUDT QuantityKind {{QUDT}} as a
classification and compatibility hint. Other mappings can target CF Standard
Names, SOSA/SSN concepts, or agency vocabularies
{{CF-STANDARD-NAMES}} {{SOSA-SSN}}.

An authority MAY identify an expected result schema. That schema and any
quantity-kind mapping are hints; the actual result schema and JSON Structure
Units annotations remain authoritative. An observable-property definition MUST
NOT override unit semantics or duplicate authoritative dimensions, unit lists,
conversion factors, or conversion formulas.

## The `semanticRole` Keyword {#semantic-role} 

The `semanticRole` keyword identifies the observation or operational function of an
annotated value.

The value of `semanticRole` MUST be one of the permitted values defined in this
section. The permitted values are a closed enumeration defined by this document.
A `semanticRole` value is never a URI; terms drawn from external vocabularies
are carried by `concepts` instead.

`semanticRole` is scalar; therefore each annotated schema element can carry one
`semanticRole` value.

### Observation Result Concern

A record using the roles of this concern, together with the feature and
procedure roles defined below:

~~~ json
{
  "name": "WaterLevelObservation",
  "type": "object",
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/water-level/v1",
    "kind": "example-catalog"
  },
  "properties": {
    "station": {
      "type": "string",
      "examples": ["USGS-12149000"],
      "semanticRole": "featureOfInterest"
    },
    "procedure": {
      "type": "string",
      "examples": ["Pressure transducer"],
      "semanticRole": "observingProcedure"
    },
    "result": {
      "type": "double",
      "description": "Water level above datum",
      "unit": "m",
      "examples": [2.47],
      "semanticRole": "observationValue"
    },
    "quality": {
      "type": "string",
      "description": "Quality classification for this result",
      "examples": ["validated", "estimated"],
      "semanticRole": "resultQuality"
    }
  },
  "required": ["station", "procedure", "result", "quality"],
  "additionalProperties": false
}
~~~

#### `observationValue` {#observation-value}

A property carrying the result of an observation act.

An `observationValue` is the outcome of one observation act, not the act
itself. Each act is represented by one complete value in one annotated
property. Structured or composite results can be represented with an object,
tuple, or another compatible compound type. Multiple `observationValue`
properties in the same containing type represent multiple results, not one
combined act.

#### `resultQuality` {#result-quality}

One result-quality value associated with the observation, corresponding to ISO
result semantics {{ISO19156}}.

`resultQuality` qualifies the `observationValue`; it is not the result value
itself.

A single observation act can carry multiple quality qualifiers, and each direct
property with `semanticRole: resultQuality` projects one of them.

The value schema or external vocabulary defines the quality scale. This
specification defines no threshold, ordering, confidence model, or processing
effect. Omission does not imply acceptable quality. Procedure-level quality
metadata describes the measuring process in general and is distinct from
`resultQuality`, which describes one observation result.

### Feature and Procedure Concern

A record using the roles of this concern:

~~~ json
{
  "name": "RiverSampleObservation",
  "type": "object",
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/dissolved-oxygen/v1",
    "kind": "example-catalog"
  },
  "properties": {
    "observationId": { "type": "uuid" },
    "waterBody": {
      "type": "string",
      "description": "River water body ultimately of interest",
      "examples": ["Rhine", "Niers", "Schwalm"],
      "semanticRole": "ultimateFeatureOfInterest"
    },
    "sampleParcel": {
      "type": "string",
      "description": "Sampled water parcel directly involved in observing",
      "examples": ["Surface sample at station 17"],
      "semanticRole": "proximateFeatureOfInterest"
    },
    "sampler": {
      "type": "uri",
      "description": "Instrument identifier from a device catalogue",
      "examples": ["https://vocab.nerc.ac.uk/collection/L22/current/TOOL1248/"],
      "semanticRole": "observingProcedure"
    },
    "dissolvedOxygen": {
      "type": "double",
      "unit": "mg/L",
      "semanticRole": "observationValue"
    }
  },
  "required": ["observationId", "waterBody", "sampleParcel", "sampler", "dissolvedOxygen"],
  "additionalProperties": false
}
~~~

#### `featureOfInterest` {#feature-of-interest}

Value identifying or describing the feature whose property is observed: the
entity that is the subject of the observation. It is distinct from
`observedProperty`, which identifies which property is observed, from
`observingProcedure`, which identifies how the value is produced, and from
`observationValue`, which carries the result.

The annotated property's value can be a scalar, object, tuple, or collection.
The property schema defines representation, cardinality, and requiredness.

Where the feature is a member of a collection held elsewhere in the document,
JSON Structure Relations {{JSTRUCT-RELATIONS}} states the reference:

~~~ json
{
  "definitions": {
    "HydroGraph": {
      "type": "object",
      "name": "HydroGraph",
      "properties": {
        "riverReaches": {
          "type": "array",
          "items": { "$ref": "#/definitions/RiverReach" }
        },
        "observations": {
          "type": "array",
          "items": { "$ref": "#/definitions/RiverObservation" }
        }
      },
      "required": ["riverReaches", "observations"],
      "additionalProperties": false
    },
    "RiverReach": {
      "type": "object",
      "name": "RiverReach",
      "identity": ["reachId"],
      "properties": {
        "reachId": { "type": "string" },
        "riverName": { "type": "string" },
        "fromNodeId": { "type": "string" },
        "toNodeId": { "type": "string" },
        "lengthMeters": { "type": "double", "unit": "m" }
      },
      "required": ["reachId", "riverName", "fromNodeId", "toNodeId"],
      "additionalProperties": false
    },
    "RiverObservation": {
      "type": "object",
      "name": "RiverObservation",
      "identity": ["observationId"],
      "properties": {
        "observationId": { "type": "uuid" },
        "reachIdRef": {
          "type": "string",
          "description": "River reach identifier",
          "semanticRole": "featureOfInterest"
        },
        "waterLevel": {
          "type": "double",
          "semanticRole": "observationValue",
          "unit": "m"
        }
      },
      "relations": {
        "featureReachRef": {
          "cardinality": "single",
          "targettype": { "$ref": "#/definitions/RiverReach" },
          "scope": "#/definitions/HydroGraph/properties/riverReaches"
        }
      },
      "required": ["observationId", "reachIdRef", "waterLevel"],
      "additionalProperties": false
    }
  }
}
~~~

In an instance, `reachIdRef` carries the same identifier value used by
the relation target identity, for example `"RR-1042"`.

#### `proximateFeatureOfInterest` {#proximate-feature-of-interest}

Value identifying or describing the feature directly involved in observing.

This role identifies the immediate feature participating in measurement
context (for example a sampled parcel). Where the observation involves
sampling, this is the feature that ISO 19156 {{ISO19156}} calls a sampling
feature.

#### `ultimateFeatureOfInterest` {#ultimate-feature-of-interest}

Value identifying or describing the feature ultimately of interest.

This role identifies the broader feature for which the observation is
semantically interpreted.

Neither proximate nor ultimate feature is inferred from the other. When
`featureOfInterest` and specialized FoI roles coexist, processors MUST preserve
them as separate declarations and MUST NOT assume equivalence. Feature identity
MUST NOT be inferred from observation identity, location, property names, or
transport metadata.

#### `observingProcedure` {#observing-procedure}

Value identifying or describing the procedure used for the observation act.

Procedure identity is comparability-critical: different procedures can yield
different biases or meanings for the same property and feature. Equality is
evidence for candidate grouping, not proof of statistical interchangeability.
When a shared catalog is available, procedure identifiers SHOULD be expressed
as URIs; a device or instrument registry serves where the procedure is
effectively defined by the instrument or sampler used.

### Temporal Concern (Observation Time)

A record using the roles of this concern:

~~~ json
{
  "name": "WaterLevelBulletin",
  "type": "object",
  "properties": {
    "station_id": {
      "type": "string",
      "semanticRole": "featureOfInterest"
    },
    "observed_at": {
      "type": "datetime",
      "description": "Time when the water level applied at the station",
      "examples": ["2026-07-27T12:00:00Z"],
      "semanticRole": "phenomenonTime"
    },
    "published_at": {
      "type": "datetime",
      "description": "Time when the result became available",
      "examples": ["2026-07-27T12:00:04Z"],
      "semanticRole": "resultTime"
    },
    "in_force": {
      "type": "object",
      "description": "Period during which the bulletin is in force",
      "semanticRole": "effectiveTime",
      "properties": {
        "start": { "type": "datetime" },
        "end": { "type": "datetime" }
      },
      "required": ["start", "end"],
      "additionalProperties": false
    },
    "water_level": {
      "type": "double",
      "unit": "m",
      "semanticRole": "observationValue"
    }
  },
  "required": ["station_id", "observed_at", "published_at", "in_force", "water_level"],
  "additionalProperties": false
}
~~~

#### `phenomenonTime`

Time during which the result applies to the observed property. It can be
represented as an instant or period.

When used for an instant, `phenomenonTime` MUST annotate a value whose Core
type and reference binding together encode a temporal position. It MAY instead
annotate a named object or tuple representing a period.

#### `resultTime`

Temporal position at which the result became available.

`resultTime` MUST annotate a value whose Core type and reference binding
together encode a temporal position.

#### `effectiveTime`

Period during which the record is in force and its use is intended.

`effectiveTime` MAY annotate a named object or tuple representing a period.

`effectiveTime` qualifies the record and not the phenomenon. It states how long
a warning, advisory, or other issued statement is meant to be acted on, and it
gives no boundary to any observed property. A record that describes a period of
the world, including a forecast, states that period with `phenomenonTime` or
with `phenomenonTimeStart` and `phenomenonTimeEnd`. The two are independent: a
warning in force for twelve hours may concern a phenomenon lasting minutes.

This document defines no record-versioning axis. The role is named
`effectiveTime` rather than `validTime` because the latter names the
bitemporal valid time of ISO 19108 {{ISO19108}}. `effectiveTime` is not that
valid time, which pairs the period a fact is held true of the world with the
period a system recorded it, and a processor MUST NOT read it as one.

“Time” or “Duration” in any ISO, boundary, or operational role name defined by
this document does not require a Gregorian, ISO 8601, or RFC 3339 encoding. The
`semanticRole` states semantics; the Core type and any
`temporalReferenceSystem` state representation and reference semantics.

### Temporal Concern (Flattened Period Boundaries)

A record using the roles of this concern. The two pairs are independent axes:
the phenomenon-time pair bounds what the result is about, and the
effective-time pair bounds how long the record is in force.

~~~ json
{
  "name": "AirQualityAdvisory",
  "type": "object",
  "properties": {
    "site_id": {
      "type": "string",
      "semanticRole": "featureOfInterest"
    },
    "averaging_window_opens": {
      "type": "datetime",
      "examples": ["2026-07-27T12:00:00Z"],
      "semanticRole": "phenomenonTimeStart"
    },
    "averaging_window_closes": {
      "type": "datetime",
      "examples": ["2026-07-27T13:00:00Z"],
      "semanticRole": "phenomenonTimeEnd"
    },
    "advisory_effective_at": {
      "type": "datetime",
      "examples": ["2026-07-27T15:00:00Z"],
      "semanticRole": "effectiveTimeStart"
    },
    "advisory_expires_at": {
      "type": "datetime",
      "examples": ["2026-07-28T03:00:00Z"],
      "semanticRole": "effectiveTimeEnd"
    },
    "mean_pm25": {
      "type": "double",
      "unit": "ug/m3",
      "semanticRole": "observationValue"
    }
  },
  "required": [
    "site_id",
    "averaging_window_opens",
    "averaging_window_closes",
    "advisory_effective_at",
    "advisory_expires_at",
    "mean_pm25"
  ],
  "additionalProperties": false
}
~~~

#### `phenomenonTimeStart`

Temporal position encoding the start of the `phenomenonTime` period.

`phenomenonTimeStart` MUST annotate a value whose Core type and reference
binding together encode a temporal position.

#### `phenomenonTimeEnd`

Temporal position encoding the end of the `phenomenonTime` period.

`phenomenonTimeEnd` MUST annotate a value whose Core type and reference
binding together encode a temporal position.

#### `effectiveTimeStart`

Temporal position encoding the start of the `effectiveTime` period.

`effectiveTimeStart` MUST annotate a value whose Core type and reference
binding together encode a temporal position.

#### `effectiveTimeEnd`

Temporal position encoding the end of the `effectiveTime` period.

`effectiveTimeEnd` MUST annotate a value whose Core type and reference binding
together encode a temporal position.

A paired start and end projects one period, not two separate attributes. Period
closure is not supplied by these role names. This specification uses half-open
`[start,end)` periods only for `phenomenonTimeRelation`; another convention requires a
separate representation or profile.

### Temporal Concern (Operational Event Time)

A planned activity, its execution, and its acceptance by a receiving system:

~~~ json
{
  "name": "SamplingRun",
  "type": "object",
  "properties": {
    "run_id": { "type": "uuid" },
    "scheduled_sample_time": {
      "type": "datetime",
      "description": "Planned time for sample collection",
      "examples": ["2026-07-27T14:00:00Z"],
      "semanticRole": "scheduledTime"
    },
    "actual_sample_time": {
      "type": "datetime",
      "description": "Time when sample collection actually occurred",
      "examples": ["2026-07-27T14:07:12Z"],
      "semanticRole": "actualTime"
    },
    "ingested_at": {
      "type": "datetime",
      "description": "Time when the receiving system accepted the record",
      "examples": ["2026-07-27T14:09:30Z"],
      "semanticRole": "ingestionTime"
    },
    "station_id": {
      "type": "string",
      "semanticRole": "featureOfInterest"
    }
  },
  "required": [
    "run_id",
    "scheduled_sample_time",
    "actual_sample_time",
    "ingested_at",
    "station_id"
  ],
  "additionalProperties": false
}
~~~

#### `ingestionTime`

Temporal position when a declared system accepted the record.

`ingestionTime` MUST annotate a value whose Core type and reference binding
together encode a temporal position.

#### `scheduledTime`

Planned temporal position for an activity.

`scheduledTime` MUST annotate a value whose Core type and reference binding
together encode a temporal position.

#### `actualTime`

Temporal position when the planned activity occurred.

`actualTime` MUST annotate a value whose Core type and reference binding
together encode a temporal position.

#### `forecastIssueTime`

Forecast-specific `resultTime`: the temporal position when a forecast product
was issued.

`forecastIssueTime` MUST annotate a value whose Core type and reference
binding together encode a temporal position.

A forecast record states the position or period it describes with
`phenomenonTime`, or with `phenomenonTimeStart` and `phenomenonTimeEnd`. A
forecast is an observation whose result time precedes its phenomenon time, and
it carries the same temporal roles as any other observation; nothing about the
phenomenon-time roles restricts them to positions that have already elapsed.
Using them here means a consumer asking what was stated when, about when, reads
the same two roles for a forecast as for a measurement.

#### `forecastLeadDuration`

Duration between the forecast issue position and the phenomenon-time position
the forecast describes.

`forecastLeadDuration` MUST annotate Core `duration` or a numeric value with a
temporal unit {{JSTRUCT-UNITS}}.

Example:

~~~ json
{
  "name": "RiverStageForecast",
  "type": "object",
  "properties": {
    "station_id": {
      "type": "string",
      "semanticRole": "featureOfInterest"
    },
    "issued_at": {
      "type": "datetime",
      "description": "Time when the forecast bulletin was issued",
      "examples": ["2026-07-27T09:00:00Z"],
      "semanticRole": "forecastIssueTime"
    },
    "forecast_window": {
      "type": "object",
      "description": "Phenomenon-time period the forecast describes",
      "semanticRole": "phenomenonTime",
      "properties": {
        "start": { "type": "datetime" },
        "end": { "type": "datetime" }
      },
      "required": ["start", "end"],
      "additionalProperties": false
    },
    "lead_time": {
      "type": "duration",
      "description": "Duration from forecast issue to the phenomenon time described",
      "examples": ["PT6H"],
      "semanticRole": "forecastLeadDuration"
    },
    "predicted_water_level": {
      "type": "double",
      "unit": "m",
      "semanticRole": "observationValue"
    }
  },
  "required": ["station_id", "issued_at", "forecast_window", "predicted_water_level"],
  "additionalProperties": false
}
~~~

These operational values describe the handling of the record. A processor MUST
NOT read any of them as `phenomenonTime`, `resultTime`, `observedProperty`,
`featureOfInterest`, or `observingProcedure`.

### Status Concern

#### `status`

State of the record itself, or of the feature it describes, such as whether a
value is provisional, verified, superseded, or withdrawn.

`status` MUST annotate a value drawn from a fixed set of states, which is a Core
`string` or an integer type. The states are defined outside this document. The
annotated schema MUST either constrain them with `enum` {{JSTRUCT-CORE}} or
identify the set that defines them, which MAY be a vocabulary referenced via
`concepts`.

`status` qualifies the record rather than the phenomenon. A change of status
does not change what was observed, and a record MAY be reissued with a new
status and an unchanged result.

`status` and `resultQuality` are distinct. `resultQuality` states how good a
result is, on a scale the quality vocabulary defines; `status` states how the
record carrying it is to be treated. A provisional record and a low-quality
result are independent conditions, and a processor MUST NOT read either
annotation as the other.

Example:

~~~ json
{
  "name": "WaterLevelRecord",
  "type": "object",
  "properties": {
    "water_level": {
      "type": "double",
      "unit": "m",
      "semanticRole": "observationValue"
    },
    "record_status": {
      "type": "string",
      "description": "Standing of this record in the publication lifecycle",
      "enum": ["provisional", "verified", "superseded", "withdrawn"],
      "examples": ["provisional"],
      "semanticRole": "status"
    }
  },
  "required": ["water_level", "record_status"],
  "additionalProperties": false
}
~~~

## The `derivation` Keyword {#derivation}

The `derivation` keyword classifies how a result value was produced.

When present, `derivation` MUST be one of:

| Derivation | Meaning |
|---|---|
| `measured` | Produced directly by an observation procedure performing measurement. |
| `statistic` | Produced by summarizing a set of values with one of the functions named by `statistic` ({{statistic}}). |
| `calculated` | Produced by a deterministic calculation that `statistic` does not name. |
| `estimated` | Inferred from incomplete, indirect, or uncertain evidence. |
| `modeled` | Produced by a model, simulation, or predictive procedure. |

Routine conversion, rounding, or serialization does not by itself change
`measured` to `calculated`. The category identifies no source, formula,
software, detailed procedure, or lineage.

`statistic` and `calculated` divide the calculations between them. Where the
result is one of the summaries this document names, the derivation is
`statistic` and the `statistic` keyword names which one, so a reader can tell an
hourly mean from an hourly maximum without reading prose. Every other
calculation is `calculated`, and the schema SHOULD explain the method in the
`description` of the annotated schema. This document defines no expression
language, and a processor MUST NOT parse a `description` or reproduce a
calculation from it.

Example:

~~~ json
{
  "name": "SeaStateReport",
  "type": "object",
  "properties": {
    "sea_state_index": {
      "type": "double",
      "description": "Composite sea-state index derived from significant wave height, peak period, and wind speed by the regional forecast model",
      "semanticRole": "observationValue",
      "derivation": "modeled"
    }
  },
  "required": ["sea_state_index"],
  "additionalProperties": false
}
~~~

## The `statistic` Keyword {#statistic}

The `statistic` keyword names the summary function that produced a result value
from a set of values.

When present, `statistic` MUST be one of:

| Statistic | Meaning |
|---|---|
| `mean` | Arithmetic mean of the set. |
| `median` | Middle value of the ordered set. |
| `mode` | Most frequent value of the set. |
| `minimum` | Least value of the set. |
| `maximum` | Greatest value of the set. |
| `sum` | Total of the set. |
| `count` | Number of values in the set. |
| `standardDeviation` | Standard deviation of the set. |
| `variance` | Variance of the set. |
| `range` | Difference between the greatest and least value. |

`statistic` and the `statistic` derivation are one declaration in two parts. A
schema whose `derivation` is `statistic` MUST carry a `statistic` keyword, and a
schema carrying a `statistic` keyword MUST have a `derivation` of `statistic`.
Neither part stands alone: the derivation says the value summarizes a set, and
the keyword says how. Where `phenomenonTimeRelation` is `accumulation`,
`statistic` MUST be `sum`.

A calculation that no value in the table names is `calculated` rather than
`statistic`, and {{derivation}} states what a schema does instead.

A vocabulary term names the phenomenon and frequently excludes the summary
function, so an hourly mean and an hourly maximum of one phenomenon carry the
same `observedProperty` and differ only here. Two results that carry the same
observable property and different statistics are not comparable as like
quantities.

The set that the statistic summarizes is the one the other annotations already
establish: the temporal roles give its extent in time, and the feature and
procedure roles give its subject. This document defines no other scoping, and
`statistic` takes no arguments. It does not state a window alignment, a
weighting, a sample count, a treatment of missing values, a percentile, or a
computation, and a processor MUST NOT recompute a result from it.

Example:

~~~ json
{
  "name": "HourlyAirTemperatureSummary",
  "type": "object",
  "observedProperty": {
    "reference": "https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html#air_temperature",
    "kind": "cf-standard-name"
  },
  "properties": {
    "station": {
      "type": "string",
      "examples": ["DWD-10382"],
      "semanticRole": "featureOfInterest"
    },
    "hour_start": {
      "type": "datetime",
      "examples": ["2026-07-27T12:00:00Z"],
      "semanticRole": "phenomenonTimeStart"
    },
    "hour_end": {
      "type": "datetime",
      "examples": ["2026-07-27T13:00:00Z"],
      "semanticRole": "phenomenonTimeEnd"
    },
    "temperature_mean": {
      "type": "double",
      "unit": "Cel",
      "description": "Mean air temperature over the hour",
      "examples": [21.4],
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "mean"
    },
    "temperature_max": {
      "type": "double",
      "unit": "Cel",
      "description": "Greatest air temperature over the hour",
      "examples": [24.9],
      "semanticRole": "observationValue",
      "derivation": "statistic",
      "statistic": "maximum"
    }
  },
  "required": ["station", "hour_start", "hour_end", "temperature_mean", "temperature_max"],
  "additionalProperties": false
}
~~~

The two results are distinguished only by `statistic`.

# Reference System Meta-Types {#meta-types}

A reference system need not be published by an authority. Where the `kind` of a
reference-system keyword is `type`, `reference` is a JSON Pointer
{{JSTRUCT-CORE}} to a shareable type definition, and that type definition is the
definition of the system. Such a type is a meta-type. It is ordinarily
maintained in its own document and brought into `definitions` with `$import`
{{JSTRUCT-IMPORT}}, so that one definition serves every schema that cites it.

A meta-type declares the members of the system, and the annotation maps the
members of the annotated schema onto them. The two need not agree in member
names, member order, or member count.

A meta-type is an ordinary type definition that a schema author writes, and it
is unrelated to the extension meta-schema of {{extension-meta-schema}}, which is
the schema of this specification.

## The `referenceRole` Keyword {#reference-role}

`referenceRole` states the function of a member within a meta-type. It MAY occur
on a property, collection item, map value, or choice member schema of a type
that a `reference` identifies, and it establishes nothing elsewhere.

When present, `referenceRole` MUST be one of:

| Value | Function of the member |
|---|---|
| `position` | Carries a temporal position, mapped by `position` ({{temporal-reference-systems}}). |
| `linearElement` | Identifies a linear element, mapped by `linearElement` ({{linear-reference-systems}}). |
| `measure` | Carries a distance along a linear element, mapped by `measure`. |
| `direction` | Qualifies direction of travel or orientation, mapped by `direction`. |

One meta-type MUST NOT declare two members with the same `referenceRole`. A
member without `referenceRole` is a component of the system that no annotation
maps, and an annotated schema MAY carry it, under any name, or omit it.

A mapping is established by `referenceRole` and never by a member name. A
processor MUST NOT infer a role from the name of a member, and a meta-type that
declares no member for a role a keyword requires is unusable by that keyword.

A coordinate reference system takes no roles, because its meta-type is a `tuple`
and the order of its elements establishes the axes ({{coordinate-reference-systems}}).

# Temporal Reference Characteristics {#temporal-reference-characteristics}

The keywords in this section concern temporal positions, the values that place
an observation or an operational event on a time line.
`phenomenonTimeRelation` states how a result relates to the position it
accompanies, `temporalReferenceSystem` states how a position value is to be
read, and `cadence` states how successive positions are expected to recur.

## The `phenomenonTimeRelation` Keyword {#phenomenon-time-relation}

The `phenomenonTimeRelation` keyword refines how a result value relates to
`phenomenonTime`. When `semanticRole: observationValue` is also present, it
describes the observation result. It is not a replacement for `phenomenonTime`.

When present, it MUST be one of:

| Value | Meaning |
|---|---|
| `instant` | Result applies at the sibling temporal position having role `phenomenonTime`. |
| `untilNext` | Result applies from that position until the next actual compatible observation. |
| `interval` | Result characterizes the half-open phenomenon-time period encoded by sibling boundaries. |
| `accumulation` | Result is accumulated over that half-open phenomenon-time period. |

`instant` and `untilNext` can be resolved only when a sibling
`phenomenonTime` annotation identifies a temporal position. `interval` and
`accumulation` can be resolved only when sibling `phenomenonTimeStart` and
`phenomenonTimeEnd` annotations identify boundaries in a common reference
regime or through an authoritative conversion. Otherwise the support is
declared but its temporal extent is indeterminate. Effective-time and
operational roles do not supply phenomenon-time boundaries.

These values state how a result relates to a phenomenon time and not how it was
produced; the summary function, where there is one, is carried by `statistic`
({{statistic}}). They do not authorize summation or prove complete coverage. For
`untilNext`, the successor is the next actual observation with compatible
resolved feature of interest, observed property, declared procedure, value
type, unit, temporal binding, and support. Cadence does not prove a successor
exists; without one the support end is unknown. Omission is not `instant`.

Example. `air_temperature` holds until the next compatible observation, so it
reads against the sibling `phenomenonTime`; `rainfall` is accumulated over the
period, so it reads against the sibling boundary pair:

~~~ json
{
  "name": "WeatherReport",
  "type": "object",
  "properties": {
    "observed_at": {
      "type": "datetime",
      "semanticRole": "phenomenonTime"
    },
    "window_opens": {
      "type": "datetime",
      "semanticRole": "phenomenonTimeStart"
    },
    "window_closes": {
      "type": "datetime",
      "semanticRole": "phenomenonTimeEnd"
    },
    "air_temperature": {
      "type": "double",
      "unit": "Cel",
      "semanticRole": "observationValue",
      "phenomenonTimeRelation": "untilNext"
    },
    "rainfall": {
      "type": "double",
      "unit": "mm",
      "semanticRole": "observationValue",
      "phenomenonTimeRelation": "accumulation"
    }
  },
  "required": [
    "observed_at",
    "window_opens",
    "window_closes",
    "air_temperature",
    "rainfall"
  ],
  "additionalProperties": false
}
~~~

## The `temporalReferenceSystem` Keyword {#temporal-reference-systems}

The `temporalReferenceSystem` keyword identifies the temporal reference
definition needed to interpret an encoded temporal position or duration.

It attaches to a temporally typed property or to a type definition that serves
as one. Where that type is an object or tuple, `position` names the member that
carries the position value.

When present, `temporalReferenceSystem` MUST be an object with a REQUIRED
`reference` string, a REQUIRED `kind` string, an OPTIONAL `position` string, and
an OPTIONAL `sortOrder` string. No other properties are permitted.

Core temporal types need no annotation when their Core semantics are fully
intended. A non-Core or ambiguous encoding is indeterminate without one.

### The `reference` Property

`reference` MUST identify one temporal reference definition. Where `kind` is
`type` it MUST be a JSON Pointer {{JSTRUCT-CORE}} resolving to a shareable type
definition, and otherwise it MUST be an absolute URI {{RFC3986}}. `kind` states
which definition model the reference identifies, and therefore what a reader can
expect to find at it. This document does not define a resolution protocol, URI
layout, storage model, or definition serialization.

Where the identified definition has a domain of validity, an annotated position
MUST lie in that domain.

### The `kind` Property

`kind` classifies which definition model the URI identifies. It is an open
enumeration. The following values are defined here:

| Kind | Referenced definition |
|---|---|
| `ogc-trs` | A concept in the OGC temporal reference system register, whose entries follow ISO 19108 {{ISO19108}}. |
| `ogc-temporal-crs` | A GML `TemporalCRS` served by the OGC definitions server, establishing a temporal datum, origin, and coordinate system {{ISO19111}} {{OGC-TOPIC2}}. |
| `type` | A meta-type declaring a member whose `referenceRole` is `position`, alongside the components of the regime ({{meta-types}}). |

Other values MAY name further definition models. {{reference-uris}} lists
resolvable URIs for the registered kinds.

Whichever model a `kind` names, the identified definition MUST establish the
components applicable to the encoding it governs. Where it defines a compound
regime that locates a position by scoped components {{OGC-TOPIC25}}, it MUST
state component order, the scope and reset behavior of each component, and the
rules for comparing positions from different scopes.

A `type` reference carries a regime that no register holds. The referenced
meta-type MUST declare a member whose `referenceRole` is `position`, and the
type and unit of that member establish the encoding. The `position` property
maps the annotated member onto it. The remaining members of the meta-type are
components of the regime that the annotation does not map. What a type
definition cannot express, such as reset behavior and comparison across scopes,
is stated in its `description`.

### The `position` Property

`position` is REQUIRED when the annotation is attached to an object or tuple
and is prohibited otherwise. It MUST name a direct member of that object or
tuple, and that member MUST be REQUIRED.

The named member carries the temporal position. Its values MUST sort in the
direction given by `sortOrder` under the ordering defined for its own type,
which for a string is lexical order. A compound position achieves this by
rendering its components most significant first at fixed width. A processor can
therefore order and compare positions without implementing the referenced
definition.

The remaining members MAY hold the individual components, identifiers, or other
detail. A processor is not required to interpret them.

### The `sortOrder` Property

`sortOrder` states how the ordering of the encoded value runs relative to
temporal order. When present, it MUST be one of:

| Value | Ordering |
|---|---|
| `forward` | An increasing value is a later position. |
| `backward` | An increasing value is an earlier position. |

When `sortOrder` is absent, the value is `forward`.

Most definitions count from an epoch toward the present and are therefore
`forward`. A definition that counts away from a datum into the past, such as
years before present, is `backward`.

`sortOrder` applies to the annotated value, or to the member named by `position`
where one is named. It states the direction of the ordering and nothing else,
and a definition whose values do not order under their own type at all is not
made orderable by declaring either value.

### Type Compatibility

The referenced definition establishes an encoding, and the annotated schema
MUST be able to carry it:

| Encoding established by the definition | Compatible schema |
|---|---|
| A date and time in a calendar, following {{RFC3339}} | Core `datetime`, `date`, `time`, or `string` |
| A count of units elapsed from an epoch | a Core integer or number type |
| Any other encoding | `string`, or an object or tuple carrying `position` |

Where the definition establishes a unit for its axis, a numeric position MUST
carry a `unit` or `ucumUnit` annotation compatible with that unit. Epoch
definitions differ in unit, so a count of seconds and a count of milliseconds
from the same origin are distinct definitions rather than one definition with
two encodings.

How much of this a reader can check depends on `kind`. An `ogc-temporal-crs`
definition determines the encoding, since its axis states either a unit of
measure, which takes a numeric position, or a date and time, which takes a
string. A `type` definition declares the type of each component and likewise
determines it. An `ogc-trs` concept names a time scale and establishes no axis,
unit, or encoding, so the compatibility check is indeterminate, as it is for a
`kind` outside this enumeration.

The annotation does not change the JSON base type, turn a data value into an
identifiable temporal object, or supply a conversion. A processor MUST compare,
order, or combine positions only within the same binding or through an
authoritative transformation. A position whose definition establishes only
order MUST NOT be treated as a metric coordinate without additional authority.
Property names alone establish none of these semantics.

Example. The clock is defined once as a meta-type and cited by `reference`, so
a record of another shape can name the same definition. The record names the
mapped member `ordinal` rather than `clockPosition`, and `position` establishes
the mapping; the remaining components are carried under the record's own names
and are not mapped. `ordinal` renders the components at fixed width, so a
processor can order two positions without implementing the definition.

~~~ json
{
  "$schema": "https://json-structure.org/meta/characteristics/v0/#",
  "$id": "https://schemas.example.org/racing-speed-observation",
  "name": "RacingSpeedObservation",
  "type": "object",
  "identity": ["observation_id"],
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/vehicle-speed/v1",
    "kind": "example-catalog"
  },
  "properties": {
    "observation_id": { "type": "uuid" },
    "entry_id": {
      "type": "string",
      "semanticRole": "featureOfInterest"
    },
    "race_clock": {
      "type": "object",
      "semanticRole": "phenomenonTime",
      "temporalReferenceSystem": {
        "reference": "#/definitions/RaceClockPosition",
        "kind": "type",
        "position": "ordinal"
      },
      "properties": {
        "ordinal": {
          "type": "string",
          "description": "Clock position rendered at fixed width and ordered lexically",
          "examples": ["2026-07-26/R/S03/L014/01250.5"]
        },
        "session": { "type": "string" },
        "stint": { "type": "uint32" },
        "lap": { "type": "uint32" },
        "distance_driven": { "type": "double", "unit": "m" }
      },
      "required": ["ordinal", "session", "stint", "lap", "distance_driven"],
      "additionalProperties": false
    },
    "speed": {
      "type": "double",
      "unit": "km/h",
      "semanticRole": "observationValue",
      "phenomenonTimeRelation": "instant",
      "derivation": "measured"
    }
  },
  "required": ["observation_id", "entry_id", "race_clock", "speed"],
  "additionalProperties": false,
  "definitions": {
    "RaceClockPosition": {
      "name": "RaceClockPosition",
      "type": "object",
      "description": "Motor-racing clock. A position is located by session, stint, lap, and distance driven within the lap. Stint numbering is entry-specific, and positions from different entries are comparable only within one session.",
      "properties": {
        "clockPosition": {
          "type": "string",
          "description": "Components rendered at fixed width, most significant first, so that positions sort lexically",
          "referenceRole": "position"
        },
        "session": { "type": "string" },
        "stint": { "type": "uint32" },
        "lap": { "type": "uint32" },
        "distanceDriven": { "type": "double", "unit": "m" }
      },
      "required": ["clockPosition"]
    }
  }
}
~~~

The compound position is comparable only under the rules of the identified
regime: equal stint, lap, and distance values do not imply equal positions
across sessions or entries. Mapping this clock to UTC or elapsed session time
requires an authoritative synchronization relation or transformation.

## The `cadence` Keyword {#cadence}

The `cadence` keyword describes expected producer behavior across successive
values of an annotated temporal position. A temporal role such as
`phenomenonTime`, `resultTime`, `ingestionTime`, or `forecastIssueTime`, when
also present, gives that sequence an observation or operational meaning.

When present, `cadence` MUST be an object with a REQUIRED `kind` string and an
OPTIONAL `period`. No other properties are permitted.

### The `kind` Property

`kind` states the expected recurrence pattern and MUST be one of:

| Kind | Meaning |
|---|---|
| `fixed` | Observations are expected at a regular period. |
| `irregular` | Observations occur without a regular period. |
| `onChange` | Observations occur when represented state changes. |

### The `period` Property

`period` is REQUIRED when `kind` is `fixed` and is prohibited otherwise. It
MUST express a positive interval in the temporal reference system applicable to
the annotated temporal position. For a Core `datetime`, `date`, or `time`, it
MUST be a positive Core `duration`. Another temporal reference system MAY use a
numeric, string, or structured interval representation defined by that system.

Cadence is not delivery time, a service-level objective, a completeness
assertion, or a phenomenon-time boundary. It does not assert that every
position has a record, that records arrive in order, or that an `untilNext`
successor exists.

Example:

~~~ json
{
  "name": "WindSpeedObservation",
  "type": "object",
  "properties": {
    "measured_at": {
      "type": "datetime",
      "description": "Instant to which the wind speed applies",
      "examples": ["2026-07-27T12:10:00Z"],
      "semanticRole": "phenomenonTime",
      "cadence": {
        "kind": "fixed",
        "period": "PT10M"
      }
    },
    "wind_speed": {
      "type": "double",
      "unit": "m/s",
      "semanticRole": "observationValue"
    }
  },
  "required": ["measured_at", "wind_speed"],
  "additionalProperties": false
}
~~~

# Spatial Reference Characteristics {#spatial-reference-characteristics}

Each keyword in this section has two parts. `reference` and `kind` identify an
external definition of a reference system. The remaining properties bind the
components of that system to named members of the object or tuple carrying the
annotation. A position in either system is held across several members, so
these keywords attach to a complex type and are not meaningful on a scalar.

## The `coordinateReferenceSystem` Keyword {#coordinate-reference-systems}

The `coordinateReferenceSystem` keyword identifies the coordinate reference
system {{ISO19111}} under which coordinate values held in properties of an
object or tuple are to be interpreted.

When present, `coordinateReferenceSystem` MUST be an object with a REQUIRED
`reference` string, a REQUIRED `kind` string, and a REQUIRED `coordinates`
array. No other properties are permitted.

### The `reference` Property

`reference` MUST identify one coordinate reference system whose definition
establishes an ordered set of axes, each with an axis direction and unit of
measure. Where `kind` is `type` it MUST be a JSON Pointer {{JSTRUCT-CORE}}
resolving to a shareable type definition, and otherwise it MUST be an absolute
URI {{RFC3986}}. `kind` states which definition model the reference identifies,
and therefore what a reader can expect to find at it.

A processor is not required to dereference the URI, and a returned
representation need not expose the axes. This document does not define
a resolution protocol, URI layout, storage model, or definition serialization.

### The `kind` Property

`kind` classifies which definition model the URI identifies. It is an open
enumeration. The following values are defined here:

| Kind | Referenced definition |
|---|---|
| `ogc-crs` | A GML CRS served by the OGC definitions server, named according to the OGC name type specification {{OGC-NAMES}}. |
| `epsg` | A record in the EPSG Geodetic Parameter Dataset {{EPSG}}. |
| `type` | A meta-type that is a `tuple` whose elements in order are the axes of an engineering or local system ({{meta-types}}). |

Other values MAY name further definition models.

A `type` reference carries an engineering or local system that no register
holds. The referenced meta-type MUST be a `tuple`, and the order given by its
`tuple` keyword is the axis order. `coordinates` maps the annotated properties
onto those elements by position, so the number of names in `coordinates` MUST
equal the number of elements and each element establishes the unit of its axis.
Axis direction, datum, and origin are stated in the `description` of the
meta-type or of its elements.

Schema authors SHOULD use a registered definition where one exists.
{{reference-uris}} lists resolvable URIs for the registered kinds.

### The `coordinates` Property

`coordinates` MUST be a non-empty ordered array of distinct property names.
Every name MUST resolve to a direct property of the annotated object or tuple.
The property at array index zero supplies axis 1 of the referenced coordinate
system, the property at index one supplies axis 2, and so on. The number of
names MUST equal the dimension of that coordinate system.

This ordering is an assertion by the schema author. It is not inferred from
property names or from a representation returned by dereferencing `reference`.

Coordinate properties MUST have numeric types. When a coordinate property has a
`unit` or `ucumUnit` annotation, that unit MUST be compatible with the
corresponding axis. A processor MAY verify the asserted ordering, units, and
dimension using a trusted authority-specific CRS database. Without such a
definition source, it MUST preserve the declaration but treat those checks and
coordinate transformations as indeterminate.

Properties not named by `coordinates` are not part of the coordinate. The
annotation therefore applies safely to an existing object that also contains
identity, temporal, status, or other values.

An object or tuple MUST NOT carry more than one `coordinateReferenceSystem`
annotation. An object containing multiple coordinates SHOULD model each
coordinate as a nested object. This document does not define coordinate epochs
for dynamic coordinate reference systems.

The coordinate order is significant. OGC CRS84 uses longitude, latitude:

~~~ json
{
  "name": "Crs84Position",
  "type": "object",
  "coordinateReferenceSystem": {
    "reference": "https://www.opengis.net/def/crs/OGC/1.3/CRS84",
    "kind": "ogc-crs",
    "coordinates": ["lon", "lat"]
  },
  "properties": {
    "lat": {
      "type": "double",
      "unit": "deg"
    },
    "lon": {
      "type": "double",
      "unit": "deg"
    }
  },
  "required": ["lat", "lon"],
  "additionalProperties": false
}
~~~

EPSG:4326 {{EPSG}} uses its authoritative latitude, longitude axis order:

~~~ json
{
  "name": "Epsg4326Position",
  "type": "object",
  "coordinateReferenceSystem": {
    "reference": "https://www.opengis.net/def/crs/EPSG/0/4326",
    "kind": "ogc-crs",
    "coordinates": ["lat", "lon"]
  },
  "properties": {
    "lat": {
      "type": "double",
      "unit": "deg"
    },
    "lon": {
      "type": "double",
      "unit": "deg"
    }
  },
  "required": ["lat", "lon"],
  "additionalProperties": false
}
~~~

### Vertical and Compound Systems

A vertical coordinate reference system has one axis, and `coordinates` then
names one property. This is the binding that makes a height or a depth
interpretable, because the number and its unit do not state what the value is
measured from.

The axis direction comes from the referenced definition and not from the
annotation, so whether the axis is positive up or positive down is a fact about
the identified system. Where `kind` is `type`, the `description` of the
meta-type or of its elements states it.

The following excerpt binds a gauge reading to NAVD88 height:

~~~ json
{
  "name": "GaugeHeightObservation",
  "type": "object",
  "coordinateReferenceSystem": {
    "reference": "https://www.opengis.net/def/crs/EPSG/0/5703",
    "kind": "ogc-crs",
    "coordinates": ["water_level"]
  },
  "properties": {
    "station": {
      "type": "string",
      "description": "Observed gauging station",
      "examples": ["USGS-12149000"],
      "semanticRole": "featureOfInterest"
    },
    "measured_at": {
      "type": "datetime",
      "examples": ["2026-07-27T12:00:00Z"],
      "semanticRole": "phenomenonTime"
    },
    "water_level": {
      "type": "double",
      "unit": "m",
      "description": "Water surface elevation",
      "examples": [2.47],
      "semanticRole": "observationValue"
    }
  },
  "required": ["station", "measured_at", "water_level"],
  "additionalProperties": false
}
~~~

Where a horizontal position and a height belong to one compound system, that
system has one definition and one set of axes, so a single annotation names all
of them in order. The annotation of such an object reads:

~~~ json
{
  "coordinateReferenceSystem": {
    "reference": "https://www.opengis.net/def/crs/EPSG/0/6349",
    "kind": "ogc-crs",
    "coordinates": ["lat", "lon", "height"]
  }
}
~~~

Where the height belongs to a different system from the horizontal position, or
where it is a result rather than part of a position, the two are separate
bindings. Since an object carries at most one `coordinateReferenceSystem`, the
schema models one of them as a nested object:

~~~ json
{
  "name": "StationWaterLevel",
  "type": "object",
  "coordinateReferenceSystem": {
    "reference": "https://www.opengis.net/def/crs/EPSG/0/5703",
    "kind": "ogc-crs",
    "coordinates": ["water_level"]
  },
  "properties": {
    "station_position": {
      "type": "object",
      "coordinateReferenceSystem": {
        "reference": "https://www.opengis.net/def/crs/OGC/1.3/CRS84",
        "kind": "ogc-crs",
        "coordinates": ["lon", "lat"]
      },
      "properties": {
        "lat": { "type": "double", "unit": "deg" },
        "lon": { "type": "double", "unit": "deg" }
      },
      "required": ["lat", "lon"],
      "additionalProperties": false
    },
    "water_level": {
      "type": "double",
      "unit": "m",
      "examples": [2.47],
      "semanticRole": "observationValue"
    }
  },
  "required": ["station_position", "water_level"],
  "additionalProperties": false
}
~~~

This specification does not define a CRS, datum, coordinate operation, or
transformation. Those definitions and semantics come from ISO 19111 and the
referenced authority.

## The `linearReferenceSystem` Keyword {#linear-reference-systems}

The `linearReferenceSystem` keyword identifies the linear reference system
{{ISO19148}} under which a location held in properties of an object or tuple is
to be interpreted.

When present, `linearReferenceSystem` MUST be an object with REQUIRED
`reference`, `kind`, `linearElement`, and `measure` strings and OPTIONAL
`measureEnd` and `direction` strings. No other properties are permitted.

### The `reference` Property

`reference` MUST identify one linear reference system. Where `kind` is `type` it
MUST be a JSON Pointer {{JSTRUCT-CORE}} resolving to a shareable type
definition, and otherwise it MUST be an absolute URI {{RFC3986}}. The identified
definition MUST establish the linear referencing method, the measure origin, the
increasing-measure direction, the measure unit, and the linear-element
namespace. `kind` states which definition model the reference identifies, and
therefore what a reader can expect to find at it.

A processor is not required to dereference the URI. This
document does not define a resolution protocol, URI layout, storage model, or
definition serialization.

### The `kind` Property

`kind` classifies which definition model the URI identifies. It is an open
enumeration. The following values are defined here:

| Kind | Referenced definition |
|---|---|
| `lrs-network` | A network published by a geospatial feature service whose layer and metadata resources establish the linear elements and the measure, such as the WSDOT State Route system {{WSDOT-LRS}}. |
| `type` | A meta-type declaring members whose `referenceRole` is `linearElement` and `measure`, and optionally `direction` ({{meta-types}}). |

Other values MAY name further definition models. {{reference-uris}} discusses
the availability of registered definitions.

A `type` reference carries a system that no authority publishes, such as one
internal to a plant, a terminal, or a private network. The referenced meta-type
MUST declare a member whose `referenceRole` is `linearElement` and a member
whose `referenceRole` is `measure`, and MAY declare one whose `referenceRole` is
`direction`. The `linearElement`, `measure`, and `direction` properties of the
annotation map the annotated properties onto those members, so the type of the
element identifier and the unit of the measure are checkable. Where the
annotation names a `measureEnd`, that property maps onto the same member of the
meta-type as `measure`, because both carry a distance in the same system. The
referencing method, measure origin, increasing-measure direction, and
linear-element namespace are stated in the `description` of the meta-type or of
its members.

### The `linearElement` Property

`linearElement` MUST name a direct property of the annotated object or tuple.
The property value identifies the road, railway, waterway, route, or other
linear element within the linear-element namespace established by the
identified system.

### The `measure` Property

`measure` MUST name a distinct direct numeric property. The property gives the
distance from the measure origin along the identified linear element. It MUST
have a `unit` or `ucumUnit` annotation compatible with the measure unit
established by the identified system.

### The `measureEnd` Property

`measureEnd`, when present, MUST name another distinct direct numeric property
whose type and unit are those required of `measure`.

Where `measureEnd` is absent, the annotation locates a point on the linear
element at `measure`. Where it is present, the annotation locates the span of
that element between `measure` and `measureEnd`, and `measure` is the start of
the span. Both ends lie on the one element that `linearElement` identifies, and
this document defines no span crossing two elements.

The span is closed at both ends. Two spans that share an end therefore share the
point at that end, which is the convention asset registers use for abutting
sections. A span whose ends are equal is the point at that measure. This
document does not require that `measureEnd` exceed `measure`, since a system
whose increasing-measure direction opposes the direction of travel encodes a
forward span with a decreasing pair.

### The `direction` Property

`direction`, when present, MUST name another distinct direct property. Its
value qualifies the direction of travel or orientation using the vocabulary
established by the identified system. It does not alter the increasing-measure
direction.

Properties not named by `linearElement`, `measure`, `measureEnd`, or `direction`
are not part of the linearly referenced location. An object or tuple MUST NOT
carry more than one `linearReferenceSystem` annotation.

This binding describes a location along one identified linear element, either a
point or a span. This document does not define offsets, referent-relative
addressing, interpolative methods, transformations between linear reference
systems, or network topology.

The following excerpt locates a point on a Washington State route, where `arm`
is the accumulated route mile measured from the route origin:

~~~ json
{
  "name": "WsdotStateRouteLocation",
  "type": "object",
  "linearReferenceSystem": {
    "reference": "https://data.wsdot.wa.gov/arcgis/rest/services/Shared/LRSData/FeatureServer/9",
    "kind": "lrs-network",
    "linearElement": "route_identifier",
    "measure": "arm",
    "direction": "inventory_direction"
  },
  "properties": {
    "route_identifier": {
      "type": "string"
    },
    "arm": {
      "type": "double",
      "unit": "mi",
      "ucumUnit": "[mi_i]"
    },
    "inventory_direction": {
      "type": "string"
    }
  },
  "required": ["route_identifier", "arm", "inventory_direction"],
  "additionalProperties": false
}
~~~

# Conformance {#conformance}

## Check Outcomes {#check-outcomes}

A check defined by this document has one of three outcomes. It is valid when a
processor evaluated it and it held, invalid when a processor evaluated it and it
did not hold, and indeterminate when a processor did not evaluate it because a
definition it depends on was not resolved.

A processor MUST report the three outcomes distinctly. It MUST NOT report an
indeterminate check as valid, MUST NOT reject a schema solely because a check
was indeterminate, and MUST NOT act on an annotation as though an indeterminate
check had held.

A rule whose subject lies within the schema is always evaluable, and a check of
such a rule is never indeterminate. A rule whose subject is an external
definition is indeterminate for as long as that definition is unresolved.

Which definitions a processor holds is a deployment matter, so two conforming
processors MAY reach different outcomes for one schema. They MUST differ only in
that one returns indeterminate where the other returns valid or invalid. A
processor MUST NOT return valid where a processor holding the definition would
return invalid.

A profile, a deployment, or an agreement between parties MAY require that named
checks be evaluated rather than left indeterminate. This document requires it of
no check.

## Schema Conformance {#schema-conformance}

A conforming schema selects the versioned extension meta-schema URI. It MAY use
any subset of the annotations defined by this document, including none, and it
MUST NOT be rejected merely because an annotation or annotated property is
absent.

Every annotation that is present:

* MUST occur at an attachment point permitted by this document;
* MUST have the defined value shape and use an allowed `kind`, `semanticRole`,
  or `referenceRole` value;
* MUST be compatible with the Core type of the annotated schema; and
* MUST satisfy the applicable rules of JSON Structure Units {{JSTRUCT-UNITS}}.

Validation MUST reject malformed annotations and invalid identifiers or values
within annotations, and those checks are never indeterminate. External
resolution, domain-of-validity, mapping-review, and transformation checks are
indeterminate while the definition they depend on is unresolved, and
{{check-outcomes}} states how a processor reports them.

## Processing Conformance {#processing-conformance}

A conforming processor MUST preserve declarations, externally resolved facts,
and inferences separately. It MUST preserve the differences among an
observation act, its result, an observable-property identity, a definition URI,
an identifiable temporal object, and a temporal-position
value.

A processor MUST NOT infer:

* any `semanticRole`, observed-property annotation, concept binding, derivation,
  statistic, or cadence from a name, label, description, type, unit, position,
  or sample;
* a `referenceRole`, or the member of a meta-type that a mapping property names,
  from a member name;
* graph structure, node identity, statements, or entailment from a concept
  binding, or a term of one vocabulary from a term of another;
* identity or semantic equivalence from labels, `closeMatch`, hierarchy,
  relatedness, or QuantityKind classification;
* a feature, procedure, or identity absent from the corresponding
  `semanticRole`, or a proximate feature from an ultimate feature or conversely;
* a temporal reference regime from a non-Core or ambiguous encoding;
* metric intervals from ordinal positions or an `untilNext` end from cadence;
* complete coverage from `interval` or `accumulation`;
* that absent quality means acceptable quality;
* a coordinate or linear reference binding from names or samples; or
* permission to aggregate, convert, transform, reject outliers, or infer
  causality.

A processor MAY ignore this extension. A processor claiming support MUST treat
unresolved identifiers, domains, mappings, or conversions
as indeterminate rather than compatible.

## Inheritance and Imports {#inheritance-and-imports}

An annotation on an inherited property or type remains part of the effective
schema. Core inheritance does not define a local override of an inherited
property. Cross-property rules MUST be checked against the effective inherited
type.

JSON Structure Import copies complete definitions, including annotations
{{JSTRUCT-IMPORT}}. Shadowing replaces the complete imported definition; it does
not merge individual annotations.

An annotation belongs to the definition it is written on, so characteristics are
part of what a type means rather than of how one schema uses it. A schema that
needs different characteristics for the same structure shadows the definition
and restates them, or defines a distinct type. This document defines no overlay
by which a schema attaches characteristics to a definition it does not own.

Where a type would inherit the same keyword from more than one base, the derived
definition MUST state that keyword itself, and the stated value is the effective
one. A definition that leaves two inherited values of one keyword in force is
not conforming, and a processor MUST NOT select between them.

# Extension Meta-Schema {#extension-meta-schema}

The extension meta-schema will be published at:

`https://json-structure.org/meta/characteristics/v0/#`

It will enable JSON Structure Units. A schema activates this specification by
selecting that URI once the meta-schema is published. The annotations carry no
profile or version member; the versioned meta-schema URI is the version
identifier.

The meta-schema validates the shape of each annotation defined here: the
presence and form of its members, the enumerations that {{annotation-model}}
states are closed, and the form required of a `reference` for the accompanying
`kind`. It does not express a rule
whose subject lies outside the annotated node. Such rules, including every rule
about a property that an annotation names and every rule about a definition that
a `reference` identifies, are checked against the effective schema rather than by
the meta-schema alone. No companion reference type or import is required.

# Security and Privacy Considerations {#security-considerations}

Incorrect or malicious catalog entries, labels, mappings,
feature identities, or procedure identities can cause results from different
subjects, acts, or concepts to be combined. Implementations MUST preserve
catalog-URI identity, MUST NOT infer equivalence from discovery labels, and MUST NOT treat an
unreviewed or non-exact mapping as approval. Catalog write access and mapping
review therefore require authentication, authorization, audit, and provenance.
Deprecation alternatives are migration advice, not automatic substitutions.

Incorrect temporal roles, boundaries, reference systems, transformations, or
domains of validity can reorder positions or create false coverage. Cadence MUST
NOT synthesize a missing `untilNext` successor. Incorrect CRS, axis order, LRS,
measure origin, unit, or direction can place a feature incorrectly. Processors
MUST NOT perform temporal, coordinate, linear, or unit transformations without
validating authoritative definitions.

Catalog labels and mappings, procedure and feature identities, locations,
times, statuses, and quality can reveal sensitive operations or subjects. Hidden
labels are not an access-control mechanism. This specification grants no access and
does not replace minimization, privacy review, retention, or export controls.

Remote registries, schemas, vocabularies, procedures, mapping targets, and
reference systems are untrusted input. Implementations SHOULD use HTTPS where
available, bounded retrieval, caching with version awareness, allow-lists where
appropriate, cycle detection, and explicit trust decisions. Dereferencing can
disclose processor interest.

# IANA Considerations {#iana-considerations}

This document has no IANA actions.

--- back

# Reference URIs (Informative) {#reference-uris}

The URIs below illustrate the `kind` values defined in this document. None of
these lists is exhaustive, and a publisher can supersede any definition.

## Vocabularies {#vocabulary-uris}

The `kind` values of {{concepts}} name these definition models, each of which
publishes its terms under one namespace URI:

* `http://www.w3.org/2000/01/rdf-schema#`, RDF Schema {{RDF-SCHEMA}}, for
  `rdfs-class`;
* `http://www.w3.org/1999/02/22-rdf-syntax-ns#`, RDF {{RDF-CONCEPTS}}, for
  `rdf-property`;
* `http://www.w3.org/2002/07/owl#`, OWL 2 {{OWL2}}, for `owl-class`,
  `owl-object-property`, and `owl-datatype-property`;
* `http://www.w3.org/2004/02/skos/core#`, SKOS {{SKOS}}, for `skos-concept`;
  and
* `http://purl.org/dc/terms/`, DCMI Metadata Terms {{DCTERMS}}, for
  `dcterms-property`.

A `reference` identifies a term rather than a namespace. Vocabularies that
define terms in these models and that are widely used with observation data
include the Semantic Sensor Network ontology {{SOSA-SSN}}, which publishes
`http://www.w3.org/ns/sosa/` and `http://www.w3.org/ns/ssn/`, and the
Provenance Ontology, which publishes `http://www.w3.org/ns/prov#`.

## Temporal Reference Systems {#temporal-reference-uris}

The URIs in this section resolve at the OGC definitions server.

Time-scale concepts, for `kind` `ogc-trs`:

* `http://www.opengis.net/def/trs/BIPM/0/UTC`, Coordinated Universal Time;
* `http://www.opengis.net/def/trs/BIPM/0/TAI`, International Atomic Time;
* `http://www.opengis.net/def/trs/IERS/0/UT1`, Universal Time UT1; and
* `http://www.opengis.net/def/trs/USNO/0/GPS`, GPS Time.

None of these constrains the type of the annotated value. Each names a time
scale and establishes no axis, unit, or encoding, so any of them can accompany
a Core temporal type, a string, a numeric epoch count, or a compound position.

Temporal coordinate reference systems, for `kind` `ogc-temporal-crs`. Each
establishes an origin and an axis, and the axis constrains the annotated type:

* `https://www.opengis.net/def/crs/OGC/0/GregorianDateTime`, a date and time in
  the Gregorian calendar. Its axis carries no unit, and it takes a Core
  `datetime`, `date`, or `time`, or a `string` in the same form.
* `https://www.opengis.net/def/crs/OGC/0/UnixTime`, seconds elapsed from
  1970-01-01T00:00:00Z. It takes an integer or number carrying UCUM `s`.
* `https://www.opengis.net/def/crs/OGC/0/AnsiDate`, days elapsed from
  1601-01-01T00:00:00Z. It takes an integer or number carrying UCUM `d`.
* `https://www.opengis.net/def/crs/OGC/0/JulianDate`, days elapsed from the
  Julian period origin. It takes a number carrying UCUM `d`, since its origin
  falls at noon and positions are ordinarily fractional.
* `https://www.opengis.net/def/crs/OGC/0/TruncatedJulianDate`, days elapsed
  from 1968-05-24T00:00:00Z. It takes a number carrying UCUM `d`.
* `https://www.opengis.net/def/crs/OGC/0/BeforePresentTime`, years counted
  backwards from 1950. It takes a number carrying UCUM `a`.
* `https://www.opengis.net/def/crs/OGC/0/ChronometricGeologicTime`, millions of
  years counted backwards from year zero. It takes a number carrying UCUM `Ma`.

None of the numeric definitions takes a string, and `GregorianDateTime` does
not take a number. The last two count backwards, so a larger value is an
earlier position, and an annotation citing either MUST declare `sortOrder` as
`backward`.

The register also serves a parameterized definition taking an origin and a
unit, which covers epoch counts for which no named definition exists. A count
of milliseconds from the Unix origin is identified by:

~~~
https://www.opengis.net/def/crs/OGC/0/Temporal
  ?epoch=%221970-01-01T00:00:00Z%22&uom=%22ms%22
~~~

Parameter values are quoted, and the URI is one line. The constraint follows
the `uom` parameter: this URI takes an integer or number carrying UCUM `ms`.
A count of seconds from the same origin is a different definition, not the same
definition read at a different scale.

## Coordinate Reference Systems {#coordinate-reference-uris}

For `kind` `ogc-crs`:

* `https://www.opengis.net/def/crs/OGC/1.3/CRS84`, WGS 84 with axes longitude,
  latitude;
* `https://www.opengis.net/def/crs/OGC/0/CRS84h`, WGS 84 with axes longitude,
  latitude, ellipsoidal height;
* `https://www.opengis.net/def/crs/EPSG/0/4326`, WGS 84 with axes latitude,
  longitude;
* `https://www.opengis.net/def/crs/EPSG/0/4979`, WGS 84 with axes latitude,
  longitude, ellipsoidal height; and
* `https://www.opengis.net/def/crs/EPSG/0/3857`, WGS 84 Pseudo-Mercator.

Axis order differs among these definitions, and the definition establishes it.
The first two and the next two describe the same datum in opposite axis order.

For `kind` `epsg`, the EPSG Geodetic Parameter Dataset serves its own records,
for example `https://apps.epsg.org/api/v1/CoordRefSystem/4326` {{EPSG}}. A
definition served at an OGC URI under an EPSG code, as in the list above, is
`ogc-crs` rather than `epsg`.

## Linear Reference Systems {#linear-reference-uris}

No register of linear reference systems corresponds to the temporal and
coordinate registers. ISO 19148 {{ISO19148}} specifies the conceptual schema,
in which a location is a measurement along a linear element and optionally an
offset from it, so that overlapping attributes can be carried against one
geometry without fragmenting it. It defines no identifiers for individual
systems. INSPIRE reuses it for transport network data across the European Union
{{INSPIRE-TN}}, and RailTopoModel applies its principles to railway axes and
mileposts {{UIC-RTM}}. A linear reference system is therefore published by the
authority that maintains the network, which is why `lrs-network` is the value
defined here for a published system, and why a system published in another form
is identified by a value naming the model that publishes it. A system that no
authority publishes is defined as a meta-type in the schema and cited with
`type`.

In the United States, the FHWA ARNOLD directive {{FHWA-ARNOLD}} requires each
state department of transportation to maintain one linear reference system
covering all public roads, modelled as the HPMS Field Manual prescribes
{{FHWA-HPMS}}: routes carrying measure values on their vertices, with
attributes held in event tables that cite a route and a measure rather than
segmenting the underlying geometry. A service published under that directive is
an `lrs-network`, and its layer and metadata resources establish the linear
elements and the measure:

* `https://data.wsdot.wa.gov/arcgis/rest/services/Shared/LRSData/FeatureServer/9`,
  the Washington state route network used in
  {{linear-reference-systems}} {{WSDOT-LRS}};
* `https://data.wsdot.wa.gov/arcgis/rest/services/Shared/CRABRoutes/FeatureServer`,
  the companion Washington county road network, keyed by county road number and
  county milepost {{WSDOT-CRAB}};
* `https://caltrans-gis.dot.ca.gov/arcgis/rest/services/CHhighway/All_Roads/FeatureServer`,
  the California all-roads network {{CALTRANS-LRS}}.

A service qualifies as an `lrs-network` only where its metadata establishes the
linear elements and the measure. A layer that carries measure values on its
vertices and a route identifier field without stating the unit of the measure,
the direction in which it increases, or the grammar of the identifier is a
rendering of positions in a reference system rather than a definition of one,
and it does not serve as a `reference`.

National road networks elsewhere publish the same model under other measures:
the Dutch Nationaal Wegenbestand serves road segments and hectometre points,
the latter being referents in the sense of ISO 19148, so that a location is a
segment, a referent, and an offset from it {{PDOK-NWB}}; the Norwegian Nasjonal
vegdatabank models the network as link sequences on which a position is a
dimensionless fraction of the length {{NVDB-NO}}; and the Swedish Nationell
vagdatabas is delivered through a download portal rather than an open query
endpoint {{NVDB-SE}}.

The `linearElement` member names the member holding the identifier of the
route, segment, or link sequence, whose type follows what the publishing
service records. The `measure` member names a numeric member whose unit is
established by the referenced system and not by the annotation: miles for the
ARNOLD networks, an offset from a hectometre referent for the Dutch network,
and a dimensionless fraction for the Norwegian one. The member SHOULD carry the
corresponding unit annotation {{JSTRUCT-UNITS}}.

# Changes from draft-vasters-json-structure-characteristics-00
{:numbered="false"}

- Initial version.

# Acknowledgments
{:numbered="false"}

The author thanks the JSON Structure community for review and feedback.

