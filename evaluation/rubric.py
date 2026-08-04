#!/usr/bin/env python3
"""Derive a per-sample grading rubric mechanically from an annotated schema.

The point of this module is to keep the supervisor honest. A supervisor that is
handed a transcript and asked "was this good?" produces one model's opinion of
another model's opinion, which is what questions 57 and 58 of `Q-A.md` object
to. This module instead derives, from the annotations themselves, a list of
propositions that a correct reader of the data must not get wrong, each one
traceable to the schema node and the keyword that establishes it. The supervisor
grades a transcript against those propositions and nothing else.

Each claim carries:

  id          stable identifier, `<pointer>::<keyword>`
  tier        `scoreable` or `expert` (see below)
  statement   the ground truth, as a proposition
  negative    the plausible wrong reading the annotation exists to prevent,
              or None where there is no single obvious one
  evidence    JSON pointer and keyword that establish the statement
  literals    strings whose presence in a transcript is a model-free signal

Tiers matter. A `scoreable` claim is entailed by the schema: whether a
transcript gets it right is decidable by reading the schema, and a supervisor
that has the schema can decide it. An `expert` claim -- whether a proposed
analysis is sensible for the domain -- is not decidable that way, and this
harness does not pretend a language model can settle it. Expert claims are
emitted for human review and are excluded from every score. That is the
distinction question 58 asks for, enforced in code rather than promised in
prose.

Usage:
    python rubric.py <schema.struct.json> [--json]
"""

from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import dataclass, field, asdict

SCOREABLE = "scoreable"
EXPERT = "expert"


@dataclass
class Claim:
    id: str
    tier: str
    statement: str
    evidence: str
    negative: str | None = None
    literals: list[str] = field(default_factory=list)


def _walk(node, pointer="#"):
    """Yield (pointer, mapping) for every object in the document."""
    if isinstance(node, dict):
        yield pointer, node
        for key, value in node.items():
            yield from _walk(value, f"{pointer}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, f"{pointer}/{index}")


def _name(pointer: str) -> str:
    """The member name a pointer addresses, for readable claim statements."""
    parts = [p for p in pointer.split("/") if p]
    for index in range(len(parts) - 1, -1, -1):
        if parts[index] not in ("properties", "definitions", "items"):
            return parts[index]
    return pointer


def _ref_text(value) -> str:
    if isinstance(value, dict):
        return str(value.get("$ref", value))
    return str(value)


# --- claim generators -------------------------------------------------------
#
# One function per keyword. Each returns zero or more Claims for one annotated
# node. A generator states what the annotation establishes and, where there is
# one, the specific wrong reading a consumer would fall into without it. The
# negative is what makes the ablation arm meaningful: in the unannotated arm the
# question is whether a subject asserts the negative or correctly declines.


def _semantic_role(pointer, node):
    role = node.get("semanticRole")
    member = _name(pointer)
    if role in ("phenomenonTime", "phenomenonTimeStart", "phenomenonTimeEnd"):
        return [Claim(
            id=f"{pointer}::semanticRole",
            tier=SCOREABLE,
            statement=(
                f"`{member}` carries phenomenon time -- when the thing being "
                f"described happened. Time series, windowing, and joins to other "
                f"feeds are built on it."
            ),
            negative=(
                f"Treating `{member}` as the time the record was produced, "
                f"received, or published, or using a different member for event time."
            ),
            evidence=f"{pointer} semanticRole={role}",
            literals=[member],
        )]
    if role in ("resultTime", "ingestionTime", "scheduledTime", "actualTime",
                "forecastIssueTime"):
        return [Claim(
            id=f"{pointer}::semanticRole",
            tier=SCOREABLE,
            statement=(
                f"`{member}` is an operational instant (`{role}`), not the time "
                f"the observed phenomenon occurred, and must not be used as the "
                f"time axis of the phenomenon."
            ),
            negative=f"Using `{member}` as the event time of the observation.",
            evidence=f"{pointer} semanticRole={role}",
            literals=[member],
        )]
    if role == "resultQuality":
        return [Claim(
            id=f"{pointer}::semanticRole",
            tier=SCOREABLE,
            statement=(
                f"`{member}` qualifies the result; it is not itself a result "
                f"value and must not be analysed as one."
            ),
            negative=f"Treating `{member}` as an observed quantity.",
            evidence=f"{pointer} semanticRole=resultQuality",
            literals=[member],
        )]
    return []


def _derivation(pointer, node):
    value = node.get("derivation")
    member = _name(pointer)
    if value in ("modeled", "estimated"):
        return [Claim(
            id=f"{pointer}::derivation",
            tier=SCOREABLE,
            statement=(
                f"`{member}` is `{value}` and is not a measurement. It must not "
                f"be presented as observed fact or used as ground truth against "
                f"which measurements are validated."
            ),
            negative=f"Treating `{member}` as a measured observation.",
            evidence=f"{pointer} derivation={value}",
            literals=[member, value],
        )]
    if value == "calculated":
        return [Claim(
            id=f"{pointer}::derivation",
            tier=SCOREABLE,
            statement=(
                f"`{member}` is calculated rather than measured directly."
            ),
            negative=f"Treating `{member}` as a direct measurement.",
            evidence=f"{pointer} derivation=calculated",
            literals=[member],
        )]
    return []


def _statistic(pointer, node):
    value = node.get("statistic")
    member = _name(pointer)
    if value is None:
        return []
    name = value.get("kind") if isinstance(value, dict) else value
    return [Claim(
        id=f"{pointer}::statistic",
        tier=SCOREABLE,
        statement=(
            f"`{member}` is already a `{name}` over a set of values. Re-applying "
            f"an aggregate to it does not yield that aggregate of the underlying "
            f"data -- a mean of means is not a mean, and an extremum of extrema "
            f"is only valid for the same function."
        ),
        negative=f"Averaging or summing `{member}` as though it were a raw sample.",
        evidence=f"{pointer} statistic={name}",
        literals=[member, str(name)],
    )]


def _phenomenon_time_relation(pointer, node):
    value = node.get("phenomenonTimeRelation")
    member = _name(pointer)
    if value == "accumulation":
        return [Claim(
            id=f"{pointer}::phenomenonTimeRelation",
            tier=SCOREABLE,
            statement=(
                f"`{member}` is accumulated over the phenomenon-time period, not "
                f"an instantaneous reading, so it may be summed across adjacent "
                f"periods but not averaged as a rate without dividing by duration."
            ),
            negative=f"Treating `{member}` as an instantaneous value at a timestamp.",
            evidence=f"{pointer} phenomenonTimeRelation=accumulation",
            literals=[member],
        )]
    if value == "untilNext":
        return [Claim(
            id=f"{pointer}::phenomenonTimeRelation",
            tier=SCOREABLE,
            statement=(
                f"`{member}` holds from its position until the next actual "
                f"observation. The successor is not guaranteed to exist and must "
                f"not be synthesised."
            ),
            negative=f"Assuming `{member}` applies only at its own instant, or "
                     f"inventing a successor to close the interval.",
            evidence=f"{pointer} phenomenonTimeRelation=untilNext",
            literals=[member],
        )]
    if value == "interval":
        return [Claim(
            id=f"{pointer}::phenomenonTimeRelation",
            tier=SCOREABLE,
            statement=(
                f"`{member}` characterises a half-open period given by sibling "
                f"boundary members, not a single instant."
            ),
            negative=f"Treating `{member}` as an instantaneous reading.",
            evidence=f"{pointer} phenomenonTimeRelation=interval",
            literals=[member],
        )]
    return []


def _support_period(pointer, node):
    value = node.get("supportPeriod")
    if not isinstance(value, dict):
        return []
    member = _name(pointer)
    length = value.get("length")
    anchor = value.get("anchor")
    shown = length if isinstance(length, str) else json.dumps(length)
    if anchor == "end":
        span = f"the period is `[t - {shown}, t)`"
        sits = "The period closes at the anchoring position and runs back to it"
        role = "`phenomenonTimeEnd`"
        wrong_direction = "forward from"
    else:
        span = f"the period is `[t, t + {shown})`"
        sits = "The period opens at the anchoring position and runs forward from it"
        role = "`phenomenonTimeStart`"
        wrong_direction = "back from"
    return [Claim(
        id=f"{pointer}::supportPeriod",
        tier=SCOREABLE,
        statement=(
            f"`{member}` characterises a phenomenon-time period of length "
            f"{shown}, stated by the schema rather than carried in the record. "
            f"{sits}. The anchoring position is the sibling annotated "
            f"{role}, or `phenomenonTime` where the record carries no member in "
            f"that role. For an anchoring position `t`, {span}."
        ),
        negative=(
            f"Treating `{member}` as an instantaneous reading at the record "
            f"timestamp, running its period {wrong_direction} the anchoring "
            f"position, or deriving its length from the cadence or from the "
            f"spacing of successive records."
        ),
        evidence=f"{pointer} supportPeriod={json.dumps(value)}",
        literals=[member] + ([shown] if isinstance(length, str) else []),
    )]


def _cadence(pointer, node):
    value = node.get("cadence")
    if not isinstance(value, dict):
        return []
    member = _name(pointer)
    kind = value.get("kind")
    period = value.get("period")
    statement = (
        f"Successive `{member}` values are expected at cadence `{kind}`"
        + (f" with period {json.dumps(period)}" if period is not None else "")
        + ". A cadence is an expectation and not a constraint: a record that "
          "departs from it is late, not invalid, and a missing value must not be "
          "filled in because the cadence says one was due."
    )
    return [Claim(
        id=f"{pointer}::cadence",
        tier=SCOREABLE,
        statement=statement,
        negative=(
            "Treating the cadence as a guarantee of completeness or as a "
            "validation rule, or interpolating absent values from it."
        ),
        evidence=f"{pointer} cadence={json.dumps(value)}",
        literals=[member] + ([str(period)] if period is not None else []),
    )]


def _temporal_reference_system(pointer, node):
    value = node.get("temporalReferenceSystem")
    if not isinstance(value, dict):
        return []
    member = _name(pointer)
    kind = value.get("kind")
    reference = _ref_text(value.get("reference"))
    claims = [Claim(
        id=f"{pointer}::temporalReferenceSystem",
        tier=SCOREABLE,
        statement=(
            f"Positions in `{member}` are expressed in the temporal reference "
            f"system `{reference}` (kind `{kind}`), not in an unqualified civil "
            f"clock."
        ),
        negative=f"Reading `{member}` as ordinary UTC.",
        evidence=f"{pointer} temporalReferenceSystem.kind={kind}",
        literals=[member, str(kind)],
    )]
    if kind == "type":
        claims.append(Claim(
            id=f"{pointer}::temporalReferenceSystem.civil",
            tier=SCOREABLE,
            statement=(
                f"`{member}` is on a clock of its own. Converting it to civil "
                f"time requires a synchronisation relation that the schema does "
                f"not supply, so a correct reader declines the conversion or "
                f"states the external input it would need."
            ),
            negative=f"Converting `{member}` to UTC as though the mapping were given.",
            evidence=f"{pointer} temporalReferenceSystem.kind=type",
            literals=[member],
        ))
    if value.get("sortOrder") == "backward":
        claims.append(Claim(
            id=f"{pointer}::sortOrder",
            tier=SCOREABLE,
            statement=(
                f"An increasing `{member}` is an *earlier* position, not a later one."
            ),
            negative=f"Sorting `{member}` ascending and calling it chronological order.",
            evidence=f"{pointer} sortOrder=backward",
            literals=[member],
        ))
    return claims


def _coordinate_reference_system(pointer, node):
    value = node.get("coordinateReferenceSystem")
    if not isinstance(value, dict):
        return []
    reference = _ref_text(value.get("reference"))
    axes = value.get("axes") or value.get("coordinates") or []
    order = ", ".join(str(a) for a in axes) if isinstance(axes, list) else str(axes)
    claims = [Claim(
        id=f"{pointer}::coordinateReferenceSystem",
        tier=SCOREABLE,
        statement=(
            f"Coordinates at `{_name(pointer)}` are expressed in `{reference}`"
            + (f", with axes bound in the order {order}." if order else ".")
            + " Axis order follows that binding and must not be assumed."
        ),
        negative=(
            "Assuming latitude/longitude order, or assuming WGS 84, without "
            "reading the binding."
        ),
        evidence=f"{pointer} coordinateReferenceSystem.reference={reference}",
        literals=[reference],
    )]
    return claims


def _vector_reference_frames(pointer, node):
    value = node.get("vectorReferenceFrames")
    if not isinstance(value, list):
        return []
    claims = []
    for index, frame in enumerate(value):
        if not isinstance(frame, dict):
            continue
        reference = _ref_text(frame.get("reference"))
        components = frame.get("components")
        claims.append(Claim(
            id=f"{pointer}::vectorReferenceFrames[{index}]",
            tier=SCOREABLE,
            statement=(
                f"The components"
                + (f" {json.dumps(components)}" if isinstance(components, list) else "")
                + f" are expressed in frame `{reference}`. Components "
                f"from different frames are not comparable and must not be "
                f"differenced or averaged across frames; a frame-invariant "
                f"quantity such as the magnitude is comparable."
            ),
            negative=(
                "Comparing or aggregating individual components across records "
                "in different frames as though they shared an axis system."
            ),
            evidence=f"{pointer} vectorReferenceFrames[{index}].reference={reference}",
            literals=[reference],
        ))
    return claims


def _tensor_reference_frames(pointer, node):
    value = node.get("tensorReferenceFrames")
    if not isinstance(value, list):
        return []
    claims = []
    for index, frame in enumerate(value):
        if not isinstance(frame, dict):
            continue
        symmetry = frame.get("symmetry")
        reference = _ref_text(frame.get("reference"))
        claims.append(Claim(
            id=f"{pointer}::tensorReferenceFrames[{index}]",
            tier=SCOREABLE,
            statement=(
                f"The tensor components are expressed in frame `{reference}`"
                + (f" and the tensor is `{symmetry}`, which fixes how many "
                   f"components are independent." if symmetry else ".")
            ),
            negative=(
                "Treating the components as independent numbers in an unspecified "
                "frame."
            ),
            evidence=f"{pointer} tensorReferenceFrames[{index}]",
            literals=[reference] + ([str(symmetry)] if symmetry else []),
        ))
    return claims


def _frame_transforms(pointer, node):
    value = node.get("frameTransforms")
    if not isinstance(value, list):
        return []
    claims = []
    for index, transform in enumerate(value):
        if not isinstance(transform, dict):
            continue
        encoding = transform.get("encoding")
        source = _ref_text((transform.get("from") or {}).get("reference"))
        target = _ref_text((transform.get("to") or {}).get("reference"))
        components = transform.get("components")
        sequence = transform.get("rotationSequence")
        statement = (
            f"The transform is encoded as `{encoding}` and carries coordinates "
            f"out of `{source}` into `{target}`"
            + (f", with components in the order {json.dumps(components)}"
               if isinstance(components, list) else "")
            + ". The direction and the component order are fixed by the "
              "annotation and are not conventions to be guessed."
        )
        if encoding == "eulerAngles":
            statement += (
                f" The angles are three successive *intrinsic* rotations in the "
                f"sequence `{sequence}`; reading them as extrinsic rotations in "
                f"that sequence gives a different rotation."
            )
        claims.append(Claim(
            id=f"{pointer}::frameTransforms[{index}]",
            tier=SCOREABLE,
            statement=statement,
            negative=(
                "Assuming a component order or rotation sense from convention, "
                "or applying the transform in the opposite direction."
            ),
            evidence=f"{pointer} frameTransforms[{index}].encoding={encoding}",
            literals=[str(encoding), source, target] + ([str(sequence)] if sequence else []),
        ))
    return claims


def _linear_reference_system(pointer, node):
    value = node.get("linearReferenceSystem")
    if not isinstance(value, dict):
        return []
    reference = _ref_text(value.get("reference"))
    return [Claim(
        id=f"{pointer}::linearReferenceSystem",
        tier=SCOREABLE,
        statement=(
            f"The location is a measure along a linear element under "
            f"`{reference}`, not a coordinate. Measures are only comparable "
            f"within the same linear element."
        ),
        negative="Treating the measure as a coordinate or comparing measures "
                 "across different linear elements.",
        evidence=f"{pointer} linearReferenceSystem.reference={reference}",
        literals=[reference],
    )]


def _color_spaces(pointer, node):
    value = node.get("colorSpaces")
    if not isinstance(value, list):
        return []
    claims = []
    for index, space in enumerate(value):
        if not isinstance(space, dict):
            continue
        parts = []
        for key in ("transfer", "alphaMode", "illuminant", "observer"):
            if key in space:
                parts.append(f"`{key}` is `{space[key]}`")
        reference = _ref_text(space.get("reference"))
        channels = space.get("channels")
        claims.append(Claim(
            id=f"{pointer}::colorSpaces[{index}]",
            tier=SCOREABLE,
            statement=(
                f"Channel values are in color space `{reference}`"
                + (f", carried by the members {json.dumps(channels)} in that "
                   f"order" if isinstance(channels, list) else "")
                + (", where " + "; ".join(parts) + "." if parts else ".")
                + " Values must not be treated as linear-light or as sRGB "
                  "unless that is what is declared."
            ),
            negative=(
                "Assuming sRGB, assuming values are linear in radiometric "
                "quantity, or compositing premultiplied and straight alpha alike."
            ),
            evidence=f"{pointer} colorSpaces[{index}]",
            literals=[reference],
        ))
    return claims


def _audio_channels(pointer, node):
    value = node.get("audioChannels")
    if not isinstance(value, list):
        return []
    claims = []
    for index, group in enumerate(value):
        if not isinstance(group, dict):
            continue
        level = group.get("levelReference", "fullScale")
        encoding = group.get("encoding")
        channels = group.get("channels")
        claims.append(Claim(
            id=f"{pointer}::audioChannels[{index}]",
            tier=SCOREABLE,
            statement=(
                f"Sample amplitudes are relative to `{level}`"
                + (f" and encoded as `{encoding}`" if encoding else "")
                + (f"; the channel order is {json.dumps(channels)}." if channels
                   else ".")
                + " Channel identity comes from that ordering, not from position "
                  "in the record read as a convention."
            ),
            negative=(
                "Assuming a conventional channel order, or comparing levels "
                "against a different reference."
            ),
            evidence=f"{pointer} audioChannels[{index}]",
            literals=[str(level)] + ([str(encoding)] if encoding else []),
        ))
    return claims


def _measurement_conditioning(pointer, node):
    value = node.get("measurementConditioning")
    if not isinstance(value, dict):
        return []
    member = _name(pointer)
    weighting = value.get("weighting")
    time_weighting = value.get("timeWeighting")
    level = value.get("levelReference")
    parts = []
    if weighting:
        parts.append(f"frequency weighting `{weighting}`")
    if time_weighting:
        parts.append(f"time weighting `{time_weighting}`")
    if level:
        parts.append(f"level reference `{level}`")
    return [Claim(
        id=f"{pointer}::measurementConditioning",
        tier=SCOREABLE,
        statement=(
            f"`{member}` carries " + ", ".join(parts) + ". Levels conditioned "
            "differently are different quantities and must not be pooled, "
            "compared, or averaged together."
        ),
        negative=(
            f"Aggregating `{member}` with levels under another weighting or "
            f"reference, or reading it as an unweighted sound pressure level."
        ),
        evidence=f"{pointer} measurementConditioning={json.dumps(value)}",
        literals=[member] + [str(p) for p in (weighting, time_weighting, level) if p],
    )]


def _spectral_bands(pointer, node):
    value = node.get("spectralBands")
    if not isinstance(value, list):
        return []
    claims = []
    for index, band in enumerate(value):
        if not isinstance(band, dict):
            continue
        calibration = band.get("calibration")
        reference = _ref_text(band.get("reference"))
        bands = band.get("bands")
        statement = f"Band values follow the band set `{reference}`"
        if isinstance(bands, list):
            statement += f", carried by the members {json.dumps(bands)} in that order"
        if calibration == "digitalNumber":
            statement += (
                " and are scaled digital numbers, which become a physical "
                "quantity only when the per-acquisition coefficients are applied. "
                "They are not radiance or reflectance as they stand."
            )
        elif calibration:
            statement += f" and are calibrated as `{calibration}`."
        else:
            statement += "."
        claims.append(Claim(
            id=f"{pointer}::spectralBands[{index}]",
            tier=SCOREABLE,
            statement=statement,
            negative="Treating raw band values as a physical quantity, or "
                     "assuming which sensor band each member holds.",
            evidence=f"{pointer} spectralBands[{index}].calibration={calibration}",
            literals=[reference] + ([str(calibration)] if calibration else []),
        ))
    return claims


def _coded_values(pointer, node):
    value = node.get("codedValues")
    if not isinstance(value, dict):
        return []
    member = _name(pointer)
    reference = _ref_text(value.get("reference"))
    kind = value.get("kind")
    return [Claim(
        id=f"{pointer}::codedValues",
        tier=SCOREABLE,
        statement=(
            f"`{member}` holds codes from the external list `{reference}` "
            f"(kind `{kind}`) and is resolved by joining to that register, not "
            f"by parsing the string."
        ),
        negative=f"Inventing the meaning of `{member}` codes, or treating them "
                 f"as free text.",
        evidence=f"{pointer} codedValues.reference={reference}",
        literals=[member, reference],
    )]


def _unit(pointer, node):
    value = node.get("unit")
    if not isinstance(value, str):
        return []
    member = _name(pointer)
    return [Claim(
        id=f"{pointer}::unit",
        tier=SCOREABLE,
        statement=f"`{member}` is expressed in `{value}`.",
        negative=f"Assuming a different or conventional unit for `{member}`.",
        evidence=f"{pointer} unit={value}",
        literals=[member, value],
    )]


GENERATORS = (
    _semantic_role,
    _derivation,
    _statistic,
    _phenomenon_time_relation,
    _support_period,
    _cadence,
    _temporal_reference_system,
    _coordinate_reference_system,
    _vector_reference_frames,
    _tensor_reference_frames,
    _frame_transforms,
    _linear_reference_system,
    _color_spaces,
    _audio_channels,
    _measurement_conditioning,
    _spectral_bands,
    _coded_values,
    _unit,
)


EXPERT_CLAIMS = (
    Claim(
        id="#::domain-fitness",
        tier=EXPERT,
        statement=(
            "The analyses the transcript proposes are ones a practitioner in "
            "this domain would recognise as useful and would actually run."
        ),
        evidence="not entailed by the schema; requires a domain expert",
    ),
    Claim(
        id="#::domain-omission",
        tier=EXPERT,
        statement=(
            "The transcript omits no analysis that a practitioner would consider "
            "obvious for this feed."
        ),
        evidence="not entailed by the schema; requires a domain expert",
    ),
)


def build(document) -> list[Claim]:
    """Every claim the annotations of one schema entail, plus the expert tier."""
    claims: list[Claim] = []
    seen: set[str] = set()
    for pointer, node in _walk(document):
        for generator in GENERATORS:
            for claim in generator(pointer, node):
                if claim.id in seen:
                    continue
                seen.add(claim.id)
                claims.append(claim)
    claims.extend(EXPERT_CLAIMS)
    return claims


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    document = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    claims = build(document)
    if "--json" in argv[1:]:
        print(json.dumps([asdict(c) for c in claims], indent=2, ensure_ascii=False))
        return 0
    scoreable = [c for c in claims if c.tier == SCOREABLE]
    print(f"{len(scoreable)} scoreable claims, {len(claims) - len(scoreable)} expert claims")
    for claim in claims:
        print(f"\n[{claim.tier}] {claim.id}\n  {claim.statement}")
        if claim.negative:
            print(f"  wrong reading: {claim.negative}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
