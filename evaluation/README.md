# Supervised evaluation harness

The evaluation recorded in [`../EVALUATION.md`](../EVALUATION.md) asked a
language model to read a schema and then rate its own confidence. Questions 57
to 59 of [`../Q-A.md`](../Q-A.md) object to that on four grounds, and the
objections are correct:

* the score was the subject's opinion of itself;
* 40 of the 43 samples had no control, so nothing separates what the annotations
  carried from what the model already knew;
* nothing was blinded;
* one model is one data point.

This harness answers each of the four. It does not turn the probe into a
benchmark, and the section on what it still cannot do is not boilerplate.

## What it does

**A rubric, not an opinion.** `rubric.py` derives a list of claims from an
annotated schema mechanically. Each claim is a proposition the annotations
entail, paired with the `wrong reading` it exists to rule out — the plausible
error a competent reader makes without the annotation. Nothing in the rubric is
a matter of taste, and nothing in it was written per sample.

**Two arms.** Every sample is run twice. The annotated arm gets the schema as
published. The control arm gets the same schema with the semantic layer removed
by `samples/make-unannotated.py`, the same code that generates the committed
unannotated companions. The control is built into the run directory at run time,
so every one of the 43 samples has one and none can go stale.

The two schemas are made to differ in the annotations and in nothing else. Both
get the same neutral `$id`. Both get the same root description, cut at the point
where the annotated sample starts discussing its own annotations and stripped of
the notice the generator adds to derived files. Without that step the control
arm announces itself: the committed companions carry a paragraph saying they are
a stripped copy and inviting the reader to compare them against the annotated
version.

**A supervisor.** A second model grades each transcript claim by claim. It sees
the claims and the two transcripts. It does not see either schema, is not told
which arm produced which transcript, and is not told that there are arms. Every
`correct` and `incorrect` verdict must carry a verbatim quote; a verdict that
cannot be quoted becomes `unaddressed`.

**Four verdicts, and declining is not failing.**

| verdict | meaning |
| --- | --- |
| `correct` | the transcript asserts the claim and stands behind it |
| `incorrect` | the transcript asserts the wrong reading, or something else incompatible |
| `declined` | the transcript raises the matter and explicitly does not settle it |
| `unaddressed` | the transcript never engages the matter |

A transcript that states the right answer but marks it as a guess is `declined`,
not `correct`. That rule is what makes the control arm mean anything. A model
with prior knowledge of METAR or of ITU-R BT.709 will often guess right from
member names alone; crediting those guesses as knowledge would collapse the
ablation to nothing. And declining is the behaviour the document asks for — an
unannotated schema does not determine the reference system, and saying so is the
right answer, which is why `declined` is scored as neither success nor harm.

**Four numbers.**

| number | definition | why |
| --- | --- | --- |
| accuracy | `correct / (correct + incorrect)` | of the matters it committed on, how often it was right |
| coverage | `(correct + incorrect + declined) / claims` | how much of the rubric it engaged at all |
| **hazard** | `incorrect / claims` | the share it got positively wrong |
| hazard reduction | `hazard(control) − hazard(annotated)` | the ablation result |

Hazard is the number that matters. A silent transcript is a nuisance; a
transcript that confidently states the wrong reference frame is the failure the
annotations exist to prevent.

**Blinding, measured rather than claimed.** Transcripts are presented as A and B
in an order drawn from a recorded seed. Blinding a control transcript is
imperfect by construction — an absent unit is sometimes visible in what a reader
did not say. So the supervisor is asked, after grading, which transcript looks
like it had more to work with. The share of times it names the annotated arm is
reported. Around a half means the blinding held; near certainty means it did
not, and the accuracy figures should be read as an upper bound.

**More than one model.** `--subject-model` is repeatable and the supervisor is a
separate client. The harness warns when the supervisor is also a subject model,
because a model grading its own transcript is not supervision.

## What it still cannot do

* **It cannot judge whether an analysis is good for its domain.** Two claims per
  sample are emitted in the `expert` tier — whether the proposed analyses suit
  the domain, and what a domain expert would say is missing. They are shown to a
  reader and excluded from every figure. A language model is not a domain
  expert, and this harness does not let one act as a substitute for the review
  that questions 3 and 56 ask for.
* **It cannot detect a right answer arrived at from priors and asserted without
  hedging.** The subject is asked to mark its guesses, and the marked ones are
  scored as `declined`. An unmarked guess that happens to be right is
  indistinguishable from knowledge and is scored as `correct`. This inflates the
  control arm, which is the conservative direction: it understates the
  difference the annotations make.
* **It cannot make the supervisor infallible.** The supervisor is a model
  applying a rule to prose. The quote requirement makes its verdicts auditable
  and the run directory keeps every prompt and every response, so a human can
  check them. That is a mitigation, not a guarantee.
* **The samples are not blind to their domain.** The schema `name` and root
  description identify the source feed in both arms. That is symmetric and so
  does not confound the ablation, but it means the subject is not reasoning from
  structure alone, and the isolation claimed in `EVALUATION.md` is weaker than
  it sounds.
* **The rubric is derived from the annotations, so the annotated arm is graded
  against its own inputs.** That is the intended design — the question is
  whether a reader recovers what the schema states — but it is not a test of
  whether the annotations are the right things to state.

## Running it

Build every prompt without calling a model, and read them:

```
python run.py --transport none --out results/dry
```

Run for real. Set `EVAL_API_KEY`, and `EVAL_API_BASE` if the endpoint is not
OpenAI's:

```
python run.py --transport openai \
  --subject-model gpt-5-mini \
  --subject-model <a second, different model> \
  --supervisor-model <a third, not either of the above> \
  --seed 1
```

Score a run again, or after editing verdicts by hand:

```
python run.py --report results/20260803T101500Z
```

Inspect the rubric for one sample:

```
python rubric.py ../samples/real-world/20-goes-magnetometer/schema.struct.json
```

Every run directory holds, per sample, the full subject prompt and response for
each arm, the full supervisor prompt and response, a result file with the claims
and verdicts, and the A/B assignment. The seed is recorded so the assignment can
be reproduced. Nothing is summarised without the material behind it being kept.
