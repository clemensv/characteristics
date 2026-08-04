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
    "JSONStructureSemanticAnnotations"
  ],
  "name": "CcsdsAttitudeQuaternion",
  "description": "A spacecraft attitude reported as a quaternion, transcribed from the Attitude Parameter Message the Consultative Committee for Space Data Systems prints as an example in its Attitude Data Messages standard.",
  "type": "object",
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/spacecraft-attitude/v1",
    "kind": "example-catalog"
  },
  "frameTransforms": [
    {
      "from": {
        "reference": {
          "$ref": "#/definitions/SpacecraftBodyFrame"
        },
        "kind": "type"
      },
      "to": {
        "reference": {
          "$ref": "#/definitions/TerrestrialFrame"
        },
        "kind": "type"
      },
      "encoding": "quaternion",
      "components": [
        "qc",
        "q1",
        "q2",
        "q3"
      ]
    }
  ],
  "properties": {
    "object_name": {
      "type": "string",
      "description": "Name of the spacecraft the attitude belongs to, from the `OBJECT_NAME` keyword of the message.",
      "semanticRole": "featureOfInterest"
    },
    "object_id": {
      "type": "string",
      "description": "International designator of the spacecraft, from the `OBJECT_ID` keyword, in the launch-year and launch-number form the message uses, for example `1997-074A`.",
      "semanticRole": "featureOfInterest"
    },
    "originator": {
      "type": "string",
      "description": "Organisation that produced the message, from the `ORIGINATOR` keyword. The standard does not require the originator to be the operator of the spacecraft.",
      "semanticRole": "observingProcedure"
    },
    "creation_date": {
      "type": "datetime",
      "description": "Time the message was produced, from the `CREATION_DATE` keyword. This is later than the epoch of the attitude it carries and is not a property of the attitude.",
      "semanticRole": "resultTime"
    },
    "epoch": {
      "type": "datetime",
      "description": "Time the attitude holds at, from the `EPOCH` keyword. The message states its time system in a keyword of its own and every time in the record is in that system; this record carries the value converted to UTC.",
      "semanticRole": "phenomenonTime"
    },
    "q1": {
      "type": "double",
      "description": "First vector component of the attitude quaternion, equal to the first component of the rotation axis multiplied by the sine of half the rotation angle. The message prints this component first and the scalar last, and the annotation names the scalar first, because the annotation states meaning and the record states storage.",
      "semanticRole": "observationValue"
    },
    "q2": {
      "type": "double",
      "description": "Second vector component of the attitude quaternion, equal to the second component of the rotation axis multiplied by the sine of half the rotation angle.",
      "semanticRole": "observationValue"
    },
    "q3": {
      "type": "double",
      "description": "Third vector component of the attitude quaternion, equal to the third component of the rotation axis multiplied by the sine of half the rotation angle.",
      "semanticRole": "observationValue"
    },
    "qc": {
      "type": "double",
      "description": "Scalar component of the attitude quaternion, equal to the cosine of half the rotation angle. The standard that first carried these messages made the position of this component a field a producer filled in, taking the value `FIRST` or `LAST`; the current issue removed that field and fixed the position at last, recording the rationale as simplicity of the standard. The rotation angle it stands for is confined to a half turn either way whenever this value is not negative.",
      "semanticRole": "observationValue"
    }
  },
  "required": [
    "object_name",
    "object_id",
    "originator",
    "creation_date",
    "epoch",
    "q1",
    "q2",
    "q3",
    "qc"
  ],
  "additionalProperties": false,
  "definitions": {
    "SpacecraftBodyFrame": {
      "name": "SpacecraftBodyFrame",
      "type": "tuple",
      "description": "The frame fixed to the spacecraft structure, named `SC_BODY_1` in the message. The standard lists the permitted frame names in an annex and gives no identifier that resolves to a definition, so the axes are written out here and cited by pointer. Which physical directions the three axes point in is a matter for the interface control document of the individual spacecraft, and the descriptions below record what such a document would state.",
      "properties": {
        "x": {
          "type": "double",
          "description": "First body axis, along the boresight of the primary instrument."
        },
        "y": {
          "type": "double",
          "description": "Second body axis, completing a right-handed set with the other two."
        },
        "z": {
          "type": "double",
          "description": "Third body axis, along the nominal nadir direction of the spacecraft."
        }
      },
      "tuple": [
        "x",
        "y",
        "z"
      ]
    },
    "TerrestrialFrame": {
      "name": "TerrestrialFrame",
      "type": "tuple",
      "description": "The Earth-fixed geocentric frame the attitude is reported against, named `ITRF1997` in the message. It is a realization of the international terrestrial reference system and is named in the message by that bare string, so it too is written out here rather than cited by URI. Writing it out records the axis order the components are indexed in, which the message does not state either.",
      "properties": {
        "x": {
          "type": "double",
          "description": "From the geocentre towards the intersection of the equator and the reference meridian."
        },
        "y": {
          "type": "double",
          "description": "From the geocentre, completing a right-handed set with the other two."
        },
        "z": {
          "type": "double",
          "description": "From the geocentre towards the reference pole."
        }
      },
      "tuple": [
        "x",
        "y",
        "z"
      ]
    }
  }
}
```

instance.json

```json
{
  "object_name": "TRMM",
  "object_id": "1997-074A",
  "originator": "GSFC",
  "creation_date": "2003-09-30T19:23:57Z",
  "epoch": "2003-09-30T14:28:15.1172Z",
  "q1": 0.00005,
  "q2": 0.87543,
  "q3": 0.40949,
  "qc": 0.25678
}
```
