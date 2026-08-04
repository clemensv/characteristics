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
    "JSONStructureSemanticAnnotations",
    "JSONStructureAlternateNames"
  ],
  "name": "GcmtMomentTensor",
  "description": "A centroid-moment-tensor solution as published in the Global CMT catalogue, transcribed from the fixed-column `ndk` record into a record with named members.",
  "type": "object",
  "concepts": [
    {
      "reference": "http://purl.org/dc/dcmitype/Event",
      "kind": "rdfs-class"
    }
  ],
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/seismic-moment-tensor/v1",
    "kind": "example-catalog"
  },
  "coordinateReferenceSystem": {
    "reference": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "kind": "ogc-crs",
    "coordinates": [
      "centroid_latitude",
      "centroid_longitude"
    ]
  },
  "tensorReferenceFrames": [
    {
      "frames": [
        {
          "reference": {
            "$ref": "#/definitions/UpSouthEastFrame"
          },
          "kind": "type"
        },
        {
          "reference": {
            "$ref": "#/definitions/UpSouthEastFrame"
          },
          "kind": "type"
        }
      ],
      "symmetry": "symmetric",
      "components": [
        {
          "index": [
            0,
            0
          ],
          "property": "mrr"
        },
        {
          "index": [
            1,
            1
          ],
          "property": "mtt"
        },
        {
          "index": [
            2,
            2
          ],
          "property": "mpp"
        },
        {
          "index": [
            0,
            1
          ],
          "property": "mrt"
        },
        {
          "index": [
            0,
            2
          ],
          "property": "mrp"
        },
        {
          "index": [
            1,
            2
          ],
          "property": "mtp"
        }
      ]
    }
  ],
  "properties": {
    "event_name": {
      "type": "string",
      "description": "CMT event name from the second line of the `ndk` record, for example `C200501010120A`. Current events use a fourteen-character name of the form XYYYYMMDDhhmmZ in which the leading letter records which data types entered the inversion: B for body waves only, S for surface waves only, M for mantle waves only, and C for a combination. The name is the catalogue's stable identifier for the solution.",
      "concepts": [
        {
          "reference": "http://purl.org/dc/terms/identifier",
          "kind": "dcterms-property"
        }
      ]
    },
    "centroid_time": {
      "type": "datetime",
      "description": "Centroid time, formed by adding the centroid time offset on the third line of the `ndk` record to the reference hypocentre time on the first line. The catalogue publishes the offset rather than the absolute instant, so this member is the result of that addition. It is the time about which the moment release is centred, not the time rupture began, and earthquakes are not scheduled, so successive values carry no period.",
      "semanticRole": "phenomenonTime",
      "derivation": "calculated",
      "cadence": {
        "kind": "irregular"
      }
    },
    "centroid_latitude": {
      "type": "double",
      "unit": "deg",
      "description": "Centroid latitude from the third line of the `ndk` record. It is an inversion result and differs from the hypocentre latitude reported on the first line, which comes from a separate location catalogue.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "centroid_longitude": {
      "type": "double",
      "unit": "deg",
      "description": "Centroid longitude from the third line of the `ndk` record, on the same basis as the latitude.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "centroid_depth": {
      "type": "double",
      "ucumUnit": "km",
      "minimum": 0,
      "description": "Centroid depth from the third line of the `ndk` record, measured downwards from the surface. It is deliberately not bound by the coordinate reference system annotation on this record: EPSG:4326 is a two-dimensional system with no vertical axis, and depth increases in the opposite sense to the ellipsoidal height a three-dimensional system would supply.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "depth_type": {
      "type": "string",
      "description": "How the centroid depth was arrived at, from the third line of the `ndk` record. It qualifies the depth rather than describing the earthquake, because a depth that was held fixed carries no information from this inversion.",
      "enum": [
        "FREE",
        "FIX",
        "BDY"
      ],
      "altenums": {
        "description": {
          "FREE": "Depth was a result of the inversion.",
          "FIX": "Depth was held fixed and not inverted for.",
          "BDY": "Depth was fixed from modelling of broad-band P waveforms."
        }
      },
      "semanticRole": "resultQuality"
    },
    "half_duration": {
      "type": "double",
      "ucumUnit": "s",
      "minimum": 0,
      "description": "Half the duration of the moment-rate function assumed in the inversion, from the second line of the `ndk` record. The catalogue assumes it from an empirical relationship with the scalar moment rather than deriving it from the analysis. Its presence is the reason the tensor members carry no phenomenon time relation of `instant`: the solution integrates moment release over a source duration.",
      "semanticRole": "observationValue",
      "derivation": "modeled"
    },
    "scalar_moment": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "minimum": 0,
      "description": "Scalar moment from the fifth line of the `ndk` record, published there scaled by the exponent given on the fourth. It is a function of the tensor and adds no independent information, but it is invariant under a change of frame where the six components are not, so it is the member to compare between catalogues that disagree about the frame.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "mrr": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "description": "Component of the moment tensor at the up axis in both index positions, from the fourth line of the `ndk` record, published there scaled by the exponent that opens that line. The catalogue reports an estimated standard error beside each component, which this record does not carry.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "mtt": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "description": "Component of the moment tensor at the south axis in both index positions. Under the zero-trace constraint the catalogue applies by default, this component and the other two on the diagonal sum to zero.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "mpp": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "description": "Component of the moment tensor at the east axis in both index positions.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "mrt": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "description": "Component of the moment tensor at the up axis and the south axis. The symmetry declared by the annotation puts the same value at the south axis and the up axis, which is why the catalogue publishes six values for a tensor with nine positions. For very shallow earthquakes this component is poorly constrained and the catalogue holds it at zero, marking that by a standard error of zero.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "mrp": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "description": "Component of the moment tensor at the up axis and the east axis, held at zero for very shallow earthquakes on the same basis as `mrt`.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
    },
    "mtp": {
      "type": "double",
      "ucumUnit": "dyn.cm",
      "description": "Component of the moment tensor at the south axis and the east axis.",
      "semanticRole": "observationValue",
      "derivation": "calculated"
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
  "additionalProperties": false,
  "definitions": {
    "UpSouthEastFrame": {
      "name": "UpSouthEastFrame",
      "type": "tuple",
      "description": "The spherical frame the Global CMT catalogue resolves its moment tensors on. No register serves it, so it is written out here and cited by pointer. The axes are given in the order r, t, p, which is the order the component names on the fourth line of the `ndk` record are built from.",
      "properties": {
        "r": {
          "type": "double",
          "description": "Radially outward from the centre of the Earth, that is, up."
        },
        "t": {
          "type": "double",
          "description": "Along the direction of increasing colatitude, that is, south."
        },
        "p": {
          "type": "double",
          "description": "Along the direction of increasing longitude, that is, east."
        }
      },
      "tuple": [
        "r",
        "t",
        "p"
      ]
    }
  }
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
