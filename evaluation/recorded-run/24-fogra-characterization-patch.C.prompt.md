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
  "$schema": "https://json-structure.org/meta/semantic-annotations/v0/#",
  "$id": "https://example.invalid/schema",
  "$uses": [
    "JSONStructureSemanticAnnotations",
    "JSONStructureUnits"
  ],
  "name": "FograCharacterizationPatch",
  "description": "One patch of a printing characterization dataset, transcribed from the FOGRA51 file published in the characterization data registry of the International Color Consortium.",
  "type": "object",
  "observedProperty": {
    "reference": "https://catalog.example.org/observable-properties/printed-colour/v1",
    "kind": "example-catalog"
  },
  "colorSpaces": [
    {
      "reference": "https://registry.color.org/cmyk-registry/fogra51",
      "kind": "icc-registry",
      "channels": [
        "cyan",
        "magenta",
        "yellow",
        "black"
      ]
    },
    {
      "reference": "https://cie.co.at/publications/colorimetry-part-4-cie-1976-lab-colour-space-1",
      "kind": "cie",
      "channels": [
        "l_star",
        "a_star",
        "b_star"
      ],
      "illuminant": "D50",
      "observer": "cie-1931-2"
    }
  ],
  "properties": {
    "sample_id": {
      "type": "int32",
      "description": "Index of the patch within the target, from the `SAMPLE_ID` column. The target the file characterizes holds one thousand six hundred and seventeen patches and the index identifies the position of this one within it.",
      "semanticRole": "featureOfInterest"
    },
    "cyan": {
      "type": "double",
      "ucumUnit": "%",
      "description": "Cyan ink amount sent to the press, from the `CMYK_C` column, as a percentage of full coverage.",
      "semanticRole": "observationValue"
    },
    "magenta": {
      "type": "double",
      "ucumUnit": "%",
      "description": "Magenta ink amount sent to the press, from the `CMYK_M` column.",
      "semanticRole": "observationValue"
    },
    "yellow": {
      "type": "double",
      "ucumUnit": "%",
      "description": "Yellow ink amount sent to the press, from the `CMYK_Y` column.",
      "semanticRole": "observationValue"
    },
    "black": {
      "type": "double",
      "ucumUnit": "%",
      "description": "Black ink amount sent to the press, from the `CMYK_K` column. The channel is named for the printing term rather than for its initial, which is why the ordering of the channels has to be stated by the annotation and cannot be inferred from the member names.",
      "semanticRole": "observationValue"
    },
    "l_star": {
      "type": "double",
      "description": "Lightness read off the printed patch, from the `LAB_L` column, on the perceptually near-uniform scale defined by the fourth part of the colorimetry standard. It runs from zero at black to one hundred at the diffuse white the illuminant and the measurement geometry establish.",
      "semanticRole": "observationValue"
    },
    "a_star": {
      "type": "double",
      "description": "Red and green coordinate read off the printed patch, from the `LAB_A` column. It is positive towards red and negative towards green, and its zero is fixed by the illuminant rather than by anything in the sheet.",
      "semanticRole": "observationValue"
    },
    "b_star": {
      "type": "double",
      "description": "Yellow and blue coordinate read off the printed patch, from the `LAB_B` column, positive towards yellow and negative towards blue.",
      "semanticRole": "observationValue"
    },
    "instrumentation": {
      "type": "string",
      "description": "The measurement conditions the file states for every patch it holds, from its `INSTRUMENTATION` header line, carried here verbatim. The illuminant and observer it names are also declared on the colorimetric space so that a processor need not parse the sentence; the geometry, the filter, the backing and the standard the readings were taken under have no keyword of their own and are preserved as text.",
      "semanticRole": "observingProcedure"
    }
  },
  "required": [
    "sample_id",
    "cyan",
    "magenta",
    "yellow",
    "black",
    "l_star",
    "a_star",
    "b_star"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "sample_id": 73,
  "cyan": 100.0,
  "magenta": 0.0,
  "yellow": 0.0,
  "black": 0.0,
  "l_star": 56.12,
  "a_star": -34.9,
  "b_star": -52.52,
  "instrumentation": "D50, 2 degree, geometry 45/0, no polarisation filter, white backing, according to ISO 13655:2009 M1"
}
```
