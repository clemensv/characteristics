#!/usr/bin/env python3
"""Supervised, controlled, blinded evaluation of the semantic annotations.

This replaces the self-reported comprehension probe recorded in `EVALUATION.md`.
That probe asked a model to read a schema and rate its own confidence, which
questions 57 to 59 of `Q-A.md` object to on four grounds: the score was the
subject's own opinion, 40 of 43 samples had no control, nothing was blinded, and
one model is one data point. Each objection is answered by a part of this
harness.

  self-report   The subject is never asked how confident it is. A separate
                supervisor grades its transcript against a rubric derived
                mechanically from the annotations (`rubric.py`), claim by claim,
                with a verbatim quote required for every non-null verdict.

  no control    Every sample is run twice: once against the annotated schema and
                once against a control schema with the semantic layer stripped
                out. The control is generated at run time by the same code that
                generates the committed unannotated companions, so it cannot
                drift and no sample is exempt.

  no blinding   The supervisor sees the two transcripts in randomised order as A
                and B, is not told which arm is which, and is not given either
                schema. It is asked afterwards whether it could tell them apart,
                and that answer is reported as a measure of how well the
                blinding held rather than quietly dropped.

  one model     `--subject-model` may be repeated. The subject and the supervisor
                are separate clients, and the harness warns when they are the
                same model, because a model grading itself is not supervision.

What this harness still cannot do is settle whether an analysis is any good for
its domain. Those claims are emitted in the `expert` tier, are shown to a human,
and are excluded from every score. A language model is not a domain expert and
this harness does not let one pretend to be.

Usage:
    python run.py --transport none                       build and inspect prompts
    python run.py --subject-model gpt-5-mini \\
                  --supervisor-model claude-sonnet-4-5 \\
                  --samples 20-goes-magnetometer         run for real
    python run.py --report results/run-2026-08-03        score an existing run
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime
import importlib.util
import json
import pathlib
import random
import re
import sys

import models
import rubric

HERE = pathlib.Path(__file__).resolve().parent
SAMPLES = HERE.parent / "samples"
PROMPTS = HERE / "prompts"

ARM_BARE = "bare"            # a) types and member names, no prose, no annotations
ARM_PROSE = "prose"          # b) a) plus every `description`
ARM_ANNOTATED = "annotated"  # c) b) plus the annotations, specification withheld
ARM_SPEC = "spec"            # d) c) plus the specification itself
ARMS = (ARM_BARE, ARM_PROSE, ARM_ANNOTATED, ARM_SPEC)
LABELS = ("A", "B", "C", "D")
VERDICTS = ("correct", "incorrect", "declined", "unaddressed")

# Two tasks, graded against the same mechanically derived claims.
#
#   comprehension   the subject explains the feed in prose, and the claims are
#                   scored against what it said.
#   query           the subject writes one Stream Analytics query computing the
#                   five derived metrics it judges most valuable, and the claims
#                   are scored against what the query does. This asks whether a
#                   reader acts on the annotations, not merely whether it can
#                   restate them, and a violation is committed in SQL rather
#                   than conceded in prose.
TASKS = {
    "comprehension": ("subject.md", "supervisor.md"),
    "query": ("subject-query.md", "supervisor-query.md"),
}
QUALITY_SCALES = ("derived", "useful", "executable")


# --- control arm ------------------------------------------------------------

def _load_stripper():
    """Reuse the committed unannotated-companion generator, hyphenated name and all."""
    path = SAMPLES / "make-unannotated.py"
    spec = importlib.util.spec_from_file_location("make_unannotated", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NEUTRAL_ID = "https://example.invalid/schema"


def _neutral_description(text: str, stripper) -> str:
    """Cut the prose that discusses the annotations, and the derived-file notice.

    The committed unannotated companions carry a paragraph saying they are a
    stripped copy and telling the reader to compare them against the annotated
    file. In a control arm that paragraph is fatal: it announces the arm. The
    annotated samples carry the mirror-image problem, a paragraph explaining
    what the annotations are there to show. Both are cut, from both arms, so
    that the two schemas differ in the annotation keywords and in nothing else.
    """
    cuts = [text.find(opener) for opener in stripper.SAMPLE_PROSE_OPENERS]
    cuts = [c for c in cuts if c >= 0]
    if cuts:
        text = text[:min(cuts)]
    return text.replace(stripper.DERIVED_NOTE, "").rstrip()


def _strip_descriptions(node):
    """Remove every `description` in place, at any depth."""
    if isinstance(node, dict):
        node.pop("description", None)
        for value in node.values():
            _strip_descriptions(value)
    elif isinstance(node, list):
        for value in node:
            _strip_descriptions(value)
    return node


def build_arms(document, stripper) -> dict:
    """Return the four schemas the subject reads.

    The arms are cumulative: each adds one layer to the one before it, so a
    difference between two adjacent arms is attributable to that layer and to
    nothing else. `spec` and `annotated` carry the same schema; what separates
    them is whether the subject is also handed the specification, which is the
    difference between guessing what a keyword name means and reading it.
    """
    keywords = stripper.characteristics_keywords() | stripper.OTHER_EXTENSION_KEYWORDS
    annotated = json.loads(json.dumps(document))
    prose, _dropped = stripper.derive(json.loads(json.dumps(document)), keywords)
    bare = _strip_descriptions(json.loads(json.dumps(prose)))

    shared = _neutral_description(annotated.get("description", ""), stripper)
    arms = {
        ARM_BARE: bare,
        ARM_PROSE: prose,
        ARM_ANNOTATED: annotated,
        ARM_SPEC: json.loads(json.dumps(annotated)),
    }
    for arm, schema in arms.items():
        schema["$id"] = NEUTRAL_ID
        if arm == ARM_BARE:
            schema.pop("description", None)
        elif shared:
            schema["description"] = shared
        else:
            schema.pop("description", None)
    return arms


# --- samples ----------------------------------------------------------------

@dataclasses.dataclass
class Sample:
    name: str
    schema: pathlib.Path
    instance: pathlib.Path


def discover(selectors: list[str]) -> list[Sample]:
    found = []
    for schema in sorted(SAMPLES.rglob("schema.struct.json")):
        instance = schema.with_name("example.json")
        if not instance.exists():
            continue
        name = schema.parent.name
        if selectors and not any(s in name for s in selectors):
            continue
        found.append(Sample(name=name, schema=schema, instance=instance))
    return found


# --- subject ----------------------------------------------------------------

CONFIDENCE_PATTERN = re.compile(
    r"(?im)^\s*#*\s*\**\s*(confidence|self[- ]assessed confidence|overall confidence)\b.*$"
)


def subject_input(schema_text: str, instance_text: str) -> str:
    return (
        "schema.json\n\n```json\n" + schema_text.strip() + "\n```\n\n"
        "instance.json\n\n```json\n" + instance_text.strip() + "\n```\n"
    )


def scrub(transcript: str) -> str:
    """Remove any self-rating the subject volunteered.

    The subject is not asked for one, but models produce them unbidden, and a
    supervisor that sees `Confidence: high` anchors on it. Removing the line is
    cheap insurance for the thing questions 57 and 58 are about.
    """
    return CONFIDENCE_PATTERN.sub("", transcript).strip()


# --- supervisor -------------------------------------------------------------

def supervisor_input(claims: list[rubric.Claim], transcripts: dict) -> str:
    lines = ["CLAIMS", ""]
    for index, claim in enumerate(claims, start=1):
        lines.append(f"{index}. {claim.statement}")
        if claim.negative:
            lines.append(f"   wrong reading: {claim.negative}")
        lines.append("")
    for label in LABELS:
        lines += ["", f"TRANSCRIPT {label}", "", transcripts[label], ""]
    return "\n".join(lines)


JSON_BLOCK = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def parse_verdicts(text: str) -> dict:
    match = JSON_BLOCK.search(text)
    body = match.group(1) if match else text
    start, end = body.find("{"), body.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("supervisor returned no JSON object")
    return json.loads(body[start:end + 1])


# --- scoring ----------------------------------------------------------------

def tally(verdicts: list[dict], label: str, count: int) -> dict:
    counts = {v: 0 for v in VERDICTS}
    for verdict in verdicts:
        if verdict.get("transcript") != label:
            continue
        value = verdict.get("verdict")
        if value in counts:
            counts[value] += 1
    answered = counts["correct"] + counts["incorrect"]
    counts["claims"] = count
    counts["answered"] = answered
    counts["accuracy"] = round(counts["correct"] / answered, 4) if answered else None
    # Two hazard measures, because the choice of denominator decides the answer.
    # `hazard` divides by every claim, which makes silence free and rewards an
    # arm for declining. `hazard_answered` divides by the claims the transcript
    # actually committed on, which is the rate a reader relying on it would meet.
    counts["hazard"] = round(counts["incorrect"] / count, 4) if count else None
    counts["hazard_answered"] = (
        round(counts["incorrect"] / answered, 4) if answered else None)
    counts["coverage"] = round((answered + counts["declined"]) / count, 4) if count else None
    counts["decline_rate"] = round(counts["declined"] / count, 4) if count else None
    return counts


def summarise(records: list[dict]) -> dict:
    totals = {arm: {v: 0 for v in VERDICTS} | {"claims": 0} for arm in ARMS}
    blinding = {label: 0 for label in LABELS} | {
        "cannot tell": 0, "correct_guess": 0, "guesses": 0}
    for record in records:
        for arm in ARMS:
            scores = record["scores"].get(arm)
            if not scores:
                continue
            for key in VERDICTS + ("claims",):
                totals[arm][key] += scores.get(key, 0) or 0
        guess = (record.get("blinding") or {}).get("richest")
        if guess in blinding:
            blinding[guess] += 1
        if guess in LABELS:
            blinding["guesses"] += 1
            # `spec` and `annotated` carry an identical schema, so naming either
            # one counts as spotting the annotated material.
            if record["labels"].get(guess) in (ARM_ANNOTATED, ARM_SPEC):
                blinding["correct_guess"] += 1

    summary = {"arms": {}, "blinding": blinding, "samples": len(records)}
    tasks = {r.get("task", "comprehension") for r in records}
    if len(tasks) == 1:
        summary["task"] = tasks.pop()
    for arm, counts in totals.items():
        answered = counts["correct"] + counts["incorrect"]
        total = counts["claims"]
        summary["arms"][arm] = {
            **counts,
            "answered": answered,
            "accuracy": round(counts["correct"] / answered, 4) if answered else None,
            "hazard": round(counts["incorrect"] / total, 4) if total else None,
            "hazard_answered": round(counts["incorrect"] / answered, 4) if answered else None,
            "coverage": round((answered + counts["declined"]) / total, 4) if total else None,
            "decline_rate": round(counts["declined"] / total, 4) if total else None,
        }

    # Each arm adds one layer to the one before it, so report what each layer
    # bought rather than one lump difference between the extremes.
    steps = []
    for lower, upper, layer in ((ARM_BARE, ARM_PROSE, "descriptions"),
                               (ARM_PROSE, ARM_ANNOTATED, "annotations"),
                               (ARM_ANNOTATED, ARM_SPEC, "specification")):
        low, high = summary["arms"][lower], summary["arms"][upper]
        step = {"layer": layer, "from": lower, "to": upper}
        for metric in ("coverage", "accuracy", "hazard", "hazard_answered"):
            if low[metric] is not None and high[metric] is not None:
                step[metric] = round(high[metric] - low[metric], 4)
        steps.append(step)
    summary["layers"] = steps

    if blinding["guesses"]:
        summary["blinding"]["guess_accuracy"] = round(
            blinding["correct_guess"] / blinding["guesses"], 4)

    # Quality, where the task produced any: the mean of the supervisor's three
    # 0-5 scales per arm. Kept apart from the claim scores on purpose. This is
    # opinion, and one model's opinion at that.
    graded = [r for r in records if r.get("quality")]
    if graded:
        summary["quality"] = {}
        for arm in ARMS:
            rated = [r["quality"][arm] for r in graded if arm in r["quality"]]
            if not rated:
                continue
            summary["quality"][arm] = {
                scale: round(sum(x.get(scale) or 0 for x in rated) / len(rated), 2)
                for scale in QUALITY_SCALES
            } | {"rated": len(rated)}
    return summary


def render(summary: dict) -> str:
    lines = [
        "",
        f"samples: {summary['samples']}",
        "",
        f"{'arm':<12}{'claims':>8}{'correct':>9}{'wrong':>7}{'declined':>10}"
        f"{'untouched':>11}{'coverage':>10}{'accuracy':>10}{'hazard':>8}{'haz/ans':>9}",
    ]
    for arm in ARMS:
        a = summary["arms"][arm]
        lines.append(
            f"{arm:<12}{a['claims']:>8}{a['correct']:>9}{a['incorrect']:>7}"
            f"{a['declined']:>10}{a['unaddressed']:>11}"
            f"{str(a['coverage']):>10}{str(a['accuracy']):>10}"
            f"{str(a['hazard']):>8}{str(a['hazard_answered']):>9}"
        )
    lines += ["", "what each layer bought (positive = the layer raised the figure):", ""]
    for step in summary.get("layers", []):
        lines.append(
            f"  + {step['layer']:<15}"
            f"coverage {str(step.get('coverage')):>8}   "
            f"accuracy {str(step.get('accuracy')):>8}   "
            f"hazard {str(step.get('hazard')):>8}   "
            f"haz/ans {str(step.get('hazard_answered')):>8}"
        )
    blinding = summary["blinding"]
    if "quality" in summary:
        lines += [
            "",
            "quality of the five metrics each arm chose, 0 to 5, supervisor's opinion:",
            "",
            f"  {'arm':<12}{'derived':>9}{'useful':>9}{'executable':>12}{'samples':>9}",
        ]
        for arm in ARMS:
            q = summary["quality"].get(arm)
            if q:
                lines.append(
                    f"  {arm:<12}{q['derived']:>9}{q['useful']:>9}"
                    f"{q['executable']:>12}{q['rated']:>9}")
        lines.append("  this is a judgement, not a measurement; it is not in the figures above.")
    lines += [
        "",
        f"blinding: supervisor named an arm {blinding['guesses']} times, "
        f"said 'cannot tell' {blinding['cannot tell']} times",
    ]
    if "guess_accuracy" in blinding:
        lines.append(
            f"          it picked an annotated arm {blinding['guess_accuracy']:.0%} "
            f"of the time (0.5 is chance, since two of the four arms are annotated)"
        )
    lines += [
        "",
        "coverage is the share of claims the transcript engaged with at all.",
        "hazard divides wrong answers by every claim, so silence is free.",
        "haz/ans divides them by the claims the transcript committed on, which is the",
        "rate a reader relying on it would actually meet. Read both.",
        "expert-tier claims are excluded from every figure above and need a human.",
        "",
    ]
    return "\n".join(lines)


# --- run --------------------------------------------------------------------

def run_sample(sample: Sample, stripper, subject: models.Client,
               supervisor: models.Client, rng: random.Random,
               out: pathlib.Path, task: str = "comprehension") -> dict:
    document = json.loads(sample.schema.read_text(encoding="utf-8"))
    instance_text = sample.instance.read_text(encoding="utf-8")
    claims = [c for c in rubric.build(document) if c.tier == rubric.SCOREABLE]
    expert = [c for c in rubric.build(document) if c.tier == rubric.EXPERT]

    schemas = {arm: json.dumps(schema, indent=2, ensure_ascii=False)
               for arm, schema in build_arms(document, stripper).items()}

    subject_system = (PROMPTS / TASKS[task][0]).read_text(encoding="utf-8")
    spec_text = SPEC_SOURCE.read_text(encoding="utf-8")
    transcripts = {}
    for arm, schema_text in schemas.items():
        system = subject_system
        if arm == ARM_SPEC:
            system += ("\n\nThe specification that defines the annotation "
                       "keywords follows. Use it to interpret any keyword you "
                       "do not recognise, and treat any rule it states about "
                       "what may not be inferred as governing your answer.\n\n"
                       + spec_text)
        response = subject.complete(
            system, subject_input(schema_text, instance_text))
        transcripts[arm] = scrub(response.text)
        (out / f"{sample.name}.{arm}.subject.md").write_text(
            response.prompt + "\n\n=== RESPONSE ===\n\n" + response.text,
            encoding="utf-8")

    arms = list(ARMS)
    rng.shuffle(arms)
    labels = dict(zip(LABELS, arms))

    supervisor_system = (PROMPTS / TASKS[task][1]).read_text(encoding="utf-8")
    graded = supervisor.complete(
        supervisor_system,
        supervisor_input(claims, {label: transcripts[arm]
                                  for label, arm in labels.items()}))
    (out / f"{sample.name}.supervisor.md").write_text(
        graded.prompt + "\n\n=== RESPONSE ===\n\n" + graded.text, encoding="utf-8")

    record = {
        "sample": sample.name,
        "task": task,
        "claims": [dataclasses.asdict(c) for c in claims],
        "expert_claims": [dataclasses.asdict(c) for c in expert],
        "labels": labels,
        "subject_model": subject.model,
        "supervisor_model": supervisor.model,
        "scores": {},
        "blinding": {},
        "verdicts": [],
    }
    if not graded.text.strip():
        return record

    parsed = parse_verdicts(graded.text)
    record["verdicts"] = parsed.get("verdicts", [])
    record["blinding"] = parsed.get("blinding", {})
    quality = parsed.get("quality") or {}
    if quality:
        record["quality"] = {arm: quality[label]
                             for label, arm in labels.items() if label in quality}
    for label, arm in labels.items():
        record["scores"][arm] = tally(record["verdicts"], label, len(claims))
    return record


# --- two-phase run, for a subject that is not reachable over HTTP -----------
#
# `--emit` writes one prompt file per arm and freezes the A/B assignment into a
# manifest. Something outside this script answers each prompt and drops the
# answer beside it as `{sample}.{arm}.transcript.md`. `--ingest` then builds the
# supervisor prompt from those transcripts, and scores whatever verdicts have
# been dropped in as `{sample}.supervisor.json`. The arms are labelled at emit
# time so that no later step can influence the assignment.

SPEC_SOURCE = HERE.parent / "draft-vasters-json-structure-characteristics.md"
SPEC_COPY = "specification.md"

SPEC_NOTE = """

You also have the specification that defines the annotation keywords used by
this schema. It is the file `{spec}` in this same directory. Read it, and use it
to interpret any keyword you do not recognise. Where the specification states a
rule about what may or may not be inferred from a keyword, that rule governs
your answer.
"""


def emit(samples: list[Sample], stripper, rng: random.Random,
         out: pathlib.Path, task: str = "comprehension") -> dict:
    subject_system = (PROMPTS / TASKS[task][0]).read_text(encoding="utf-8")
    manifest: dict = {"task": task, "samples": {}}
    needs_spec = False
    for sample in samples:
        document = json.loads(sample.schema.read_text(encoding="utf-8"))
        instance_text = sample.instance.read_text(encoding="utf-8")
        derived = rubric.build(document)
        claims = [c for c in derived if c.tier == rubric.SCOREABLE]
        expert = [c for c in derived if c.tier == rubric.EXPERT]
        schemas = build_arms(document, stripper)

        arms = list(ARMS)
        rng.shuffle(arms)
        labels = dict(zip(LABELS, arms))

        # The prompt files are named by label, never by arm. A subject that can
        # read its condition off the path is not blinded, and the whole point of
        # the control arms is that the subject cannot tell it is in one.
        for label, arm in labels.items():
            schema_text = json.dumps(schemas[arm], indent=2, ensure_ascii=False)
            system = subject_system
            if arm == ARM_SPEC:
                system += SPEC_NOTE.format(spec=SPEC_COPY)
                needs_spec = True
            (out / f"{sample.name}.{label}.prompt.md").write_text(
                system + "\n\n---\n\n"
                + subject_input(schema_text, instance_text), encoding="utf-8")
        manifest["samples"][sample.name] = {
            "labels": labels,
            "claims": [dataclasses.asdict(c) for c in claims],
            "expert_claims": [dataclasses.asdict(c) for c in expert],
        }
    if needs_spec:
        (out / SPEC_COPY).write_text(
            SPEC_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def ingest(out: pathlib.Path, subject_model: str, supervisor_model: str) -> tuple[int, int]:
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    task = manifest.get("task", "comprehension")
    supervisor_system = (PROMPTS / TASKS[task][1]).read_text(encoding="utf-8")
    built = scored = 0
    for name, entry in sorted(manifest["samples"].items()):
        labels = entry["labels"]
        claims = [rubric.Claim(**c) for c in entry["claims"]]
        paths = {label: out / f"{name}.{label}.transcript.md" for label in labels}
        if not all(p.exists() for p in paths.values()):
            continue
        transcripts = {label: scrub(p.read_text(encoding="utf-8"))
                       for label, p in paths.items()}
        (out / f"{name}.supervisor.prompt.md").write_text(
            supervisor_system + "\n\n---\n\n"
            + supervisor_input(claims, transcripts), encoding="utf-8")
        built += 1

        verdicts = out / f"{name}.supervisor.json"
        if not verdicts.exists():
            continue
        parsed = parse_verdicts(verdicts.read_text(encoding="utf-8"))
        record = {
            "sample": name,
            "task": task,
            "claims": entry["claims"],
            "expert_claims": entry["expert_claims"],
            "labels": labels,
            "subject_model": subject_model,
            "supervisor_model": supervisor_model,
            "scores": {},
            "blinding": parsed.get("blinding", {}),
            "verdicts": parsed.get("verdicts", []),
        }
        # The quality block is the supervisor's judgement of the five metrics
        # each answer chose. It is keyed by label on the way in and by arm on
        # the way out, and it is never folded into the claim scores.
        quality = parsed.get("quality") or {}
        if quality:
            record["quality"] = {arm: quality[label]
                                 for label, arm in labels.items()
                                 if label in quality}
        for label, arm in labels.items():
            record["scores"][arm] = tally(record["verdicts"], label, len(claims))
        (out / f"{name}.{subject_model}.result.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        scored += 1
    return built, scored


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--transport", default="none", choices=("none", "openai"))
    parser.add_argument("--task", default="comprehension", choices=tuple(TASKS),
                        help="comprehension: explain the feed in prose. "
                             "query: write one Stream Analytics query computing "
                             "the five most valuable derived metrics. Both are "
                             "scored against the same claims.")
    parser.add_argument("--subject-model", action="append", default=[],
                        help="repeatable; every subject model is run over every sample")
    parser.add_argument("--supervisor-model", default="none")
    parser.add_argument("--samples", nargs="*", default=[],
                        help="substrings of sample directory names; default is all")
    parser.add_argument("--seed", type=int, default=None,
                        help="seed for the A/B assignment; recorded in the run")
    parser.add_argument("--out", default=None)
    parser.add_argument("--report", default=None,
                        help="score an existing run directory and exit")
    parser.add_argument("--emit", action="store_true",
                        help="write subject prompts and a manifest, then exit, "
                             "for a subject this script cannot call itself")
    parser.add_argument("--ingest", default=None,
                        help="build supervisor prompts from dropped-in transcripts "
                             "in an emitted directory, and score any verdicts found")
    args = parser.parse_args(argv[1:])

    if args.report:
        directory = pathlib.Path(args.report)
        if not directory.is_dir():
            print(f"--report needs an existing run directory; {directory} is not one",
                  file=sys.stderr)
            return 1
        records = [json.loads(p.read_text(encoding="utf-8"))
                   for p in sorted(directory.glob("*.result.json"))]
        if not records:
            print(f"no *.result.json in {directory}", file=sys.stderr)
            return 1
        summary = summarise(records)
        (directory / "summary.json").write_text(
            json.dumps(summary, indent=2), encoding="utf-8")
        print(render(summary))
        return 0

    if args.ingest:
        directory = pathlib.Path(args.ingest)
        if not (directory / "manifest.json").exists():
            print(f"{directory} has no manifest.json; run --emit first", file=sys.stderr)
            return 1
        subject_name = (args.subject_model or ["subject"])[0]
        built, scored = ingest(directory, subject_name, args.supervisor_model)
        print(f"supervisor prompts built: {built}   samples scored: {scored}")
        return 0

    subject_models = args.subject_model or ["none"]
    if args.supervisor_model in subject_models and args.transport != "none":
        print("WARNING: the supervisor is one of the subject models. A model "
              "grading its own transcript is not supervision; the run will "
              "produce numbers, and they will not mean what they appear to.",
              file=sys.stderr)

    samples = discover(args.samples)
    if not samples:
        print("no samples matched", file=sys.stderr)
        return 1

    stamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
    out = pathlib.Path(args.out or (HERE / "results" / stamp))
    out.mkdir(parents=True, exist_ok=True)

    seed = args.seed if args.seed is not None else random.randrange(2 ** 31)
    stripper = _load_stripper()

    if args.emit:
        manifest = emit(samples, stripper, random.Random(seed), out, args.task)
        (out / "seed.json").write_text(
            json.dumps({"seed": seed, "task": args.task}), encoding="utf-8")
        claims = sum(len(e["claims"]) for e in manifest["samples"].values())
        print(f"emitted {len(samples)} samples, {claims} scoreable claims, "
              f"task {args.task}, to {out}")
        print("answer each *.prompt.md and save the answer beside it as "
              "*.transcript.md, then re-run with --ingest")
        return 0

    supervisor = models.build(args.transport, args.supervisor_model)

    all_records = []
    for subject_name in subject_models:
        subject = models.build(args.transport, subject_name)
        rng = random.Random(f"{seed}:{subject_name}")
        for sample in samples:
            record = run_sample(sample, stripper, subject, supervisor, rng, out,
                                args.task)
            record["seed"] = seed
            path = out / f"{sample.name}.{subject_name}.result.json"
            path.write_text(json.dumps(record, indent=2, ensure_ascii=False),
                            encoding="utf-8")
            all_records.append(record)
            print(f"{sample.name:<36} {subject_name:<20} "
                  f"{len(record['claims']):>3} claims")

    summary = summarise(all_records)
    summary["seed"] = seed
    summary["subject_models"] = subject_models
    summary["supervisor_model"] = args.supervisor_model
    summary["transport"] = args.transport
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nwrote {out}")
    if args.transport == "none":
        print("transport 'none': prompts written, no model called, no scores.")
    else:
        print(render(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
