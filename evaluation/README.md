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

**Two tasks, one rubric.** `--task` selects what the subject is asked to do.
Both tasks are graded against the same mechanically derived claims, so the two
runs are directly comparable, and the difference between them is itself a
result.

| task | the subject is asked to |
| --- | --- |
| `comprehension` | explain the feed in prose: what it is, what it supports, what may be combined with what, where the time axis is, what is left open |
| `query` | write one Azure Stream Analytics query — the dialect Fabric Eventstream's SQL operator takes — computing the five derived metrics it judges most valuable, and say what it deliberately did not compute |

The second task exists because knowing a constraint and honouring it are not the
same act. In `comprehension` a claim is scored against what the subject said. In
`query` it is scored against what the subject's SQL does: averaging a quantity
the claim says may not be averaged, or naming the wrong member in `TIMESTAMP BY`,
is `incorrect` whether or not the prose alongside it recites the rule correctly.
A violation committed in code is harder to talk one's way out of than a
sentence, and it is the form the error takes in production.

For the `query` task the supervisor also rates each answer's five metrics on
three 0-to-5 scales — are they genuinely derived, would an operator want them,
would the query run. That block is reported on its own and is never mixed into
the claim scoring, because it is one model's opinion and the harness does not
pretend otherwise.

**Four arms.** Every sample is run four times, and the arms are cumulative, so a
difference between two adjacent arms is attributable to the one layer that
separates them.

| arm | what the subject reads |
| --- | --- |
| `bare` | member names and types, nothing else |
| `prose` | `bare` plus every `description` |
| `annotated` | `prose` plus the annotation keywords, specification withheld |
| `spec` | `annotated` plus this document's specification text |

The `bare` and `prose` arms are built by stripping the published schema with
`samples/make-unannotated.py`, the same code that generates the committed
unannotated companions. They are built into the run directory at run time, so no
sample is exempt and none can go stale.

The schemas are made to differ in the intended layer and in nothing else. All
four get the same neutral `$id`. All four get the same root description, cut at
the point where the annotated sample starts discussing its own annotations and
stripped of the notice the generator adds to derived files. Without that step
the stripped arms announce themselves: the committed companions carry a
paragraph saying they are a stripped copy and inviting the reader to compare
them against the annotated version.

**A supervisor from another vendor, told to be hostile.** A second model grades
each transcript claim by claim. It sees the claims and the four transcripts. It
does not see any schema, is not told which arm produced which transcript, and is
not told that there are arms. Every `correct` and `incorrect` verdict must carry
a verbatim quote; a verdict that cannot be quoted becomes `unaddressed`.

Two properties of the supervisor matter enough to be part of the design rather
than an implementation detail.

It is **a different model family from a different vendor** than the subject. A
model grading its own family's output is the weakest link in an evaluation of
this shape, and the recorded runs were regraded across that boundary once it was
available.

It is **adversarial**. It is told that credit is earned and never assumed, that
the default verdict is `unaddressed`, and that a grader who credits an answer
with something it did not quite say has failed. Three rules do most of the work:
the quote must carry the claim standing alone, with the rest of the transcript
covered up; the wrong reading is searched for before the right one; and a
transcript that both states a claim and commits the error it rules out is
`incorrect`, because reciting a rule and then breaking it is worse than not
knowing it. In the query task this last rule has teeth, since prose that
contradicts its own SQL is graded on the SQL.

Severity is aimed at unearned credit, not at any transcript. Silence remains
`unaddressed` and costs nothing, and the supervisor is told so explicitly, so
the stance withholds credit rather than manufacturing violations.

**Four verdicts, and declining is not failing.**

| verdict | meaning |
| --- | --- |
| `correct` | the transcript asserts the claim and stands behind it |
| `incorrect` | the transcript asserts the wrong reading, or something else incompatible |
| `declined` | the transcript raises the matter and explicitly does not settle it |
| `unaddressed` | the transcript never engages the matter |

A transcript that states the right answer but marks it as a guess is `declined`,
not `correct`. That rule is what makes the stripped arms mean anything. A model
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
| hazard reduction | `hazard(lower arm) − hazard(higher arm)` | what one layer bought |

Hazard is the number that matters. A silent transcript is a nuisance; a
transcript that confidently states the wrong reference frame is the failure the
annotations exist to prevent.

**Blinding, measured rather than claimed.** Transcripts are presented as A to D
in an order drawn from a recorded seed. Blinding a stripped transcript is
imperfect by construction — an absent unit is sometimes visible in what a reader
did not say. So the supervisor is asked, after grading, which transcript looks
like it had more to work with. The share of times it names one of the two
annotated arms is reported. Around a half is chance; near certainty means the
blinding did not hold and the accuracy figures should be read as an upper bound.

In both recorded runs the blinding largely did not hold. See below.

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
  stripped arms, which is the conservative direction: it understates the
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
* **A `description` that restates what an annotation encodes collapses the
  `prose`/`annotated` comparison.** Several samples explain in prose the same
  fact the annotation carries. Where they do, the `prose` arm recovers it and
  the layer appears to buy nothing. This understates the annotations against a
  hand-written description and says nothing about whether a machine could act on
  either.
* **The supervisor is not stable, and the instability is large.** Both runs were
  graded twice: once by the same model family as the subject under neutral
  instructions, then again by a different vendor's model under the adversarial
  stance. The second grading moved `correct` in the comprehension run from 248 to
  190 on the `annotated` arm, and moved `incorrect` in the query run from 7 to 31
  on the `prose` arm. Both gradings are kept, the earlier one under
  `prior-grading/`, so the movement can be inspected rather than taken on trust.
  The figures quoted here are the adversarial cross-vendor grading throughout. No
  difference between adjacent arms smaller than that movement should be read as
  evidence of anything.
* **Counting claims overstates repeated mistakes.** The rubric emits one claim
  per annotated member, so a single decision in a query is scored once for every
  member it touches. In the BMRS sample one division by the elapsed time between
  records produces twenty violations, because seventeen fuel members carry the
  same annotations. Wherever violation counts are quoted below, the count of
  distinct decisions behind them is quoted too, and the second number is the one
  to reason from.
* **It cannot confirm the `spec` arm read the specification.** The prompt writes
  `specification.md` into the run directory and tells the subject to read it,
  but nothing checks that it did. A subject that skips the file produces a
  transcript indistinguishable from the `annotated` arm, and the arm silently
  measures nothing. The recorded run had to be re-run once for exactly this
  reason. Any null result for that arm is only worth reading if the subject can
  be shown to have opened the file.

## The recorded runs

Two runs are kept under version control. Both were answered and graded by
sub-agents with no access to this repository beyond the single prompt file each
was given.

### `recorded-run` — the comprehension task

Seed 23, thirteen samples, 285 scoreable claims, four arms, 1140 verdicts.

| arm | correct | wrong | declined | untouched | coverage | accuracy | hazard | haz/ans |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 49 | 28 | 123 | 85 | 0.7018 | 0.6364 | 0.0982 | 0.3636 |
| `prose` | 177 | 9 | 11 | 88 | 0.6912 | 0.9516 | 0.0316 | 0.0484 |
| `annotated` | 190 | 5 | 6 | 84 | 0.7053 | 0.9744 | 0.0175 | 0.0256 |
| `spec` | 202 | 6 | 4 | 73 | 0.7439 | 0.9712 | 0.0211 | 0.0288 |

Those 28, 9, 5 and 6 violations are 8, 6, 3 and 4 distinct decisions once
repetition across members is collapsed.

Restricted to the 25 claims the `supportPeriod` annotations entail, in the three
samples that carry them:

| arm | correct | wrong | declined | untouched |
| --- | ---: | ---: | ---: | ---: |
| `bare` | 0 | 17 | 5 | 3 |
| `prose` | 20 | 0 | 4 | 1 |
| `annotated` | 24 | 0 | 0 | 1 |
| `spec` | 25 | 0 | 0 | 0 |

Every wrong answer in that subset is the `bare` arm inferring the length of a
settlement period from the spacing of records, which is the reading the
`supportPeriod` keyword exists to rule out and the defect the BMRS sample
previously encoded in its own prose. It is the one part of either run that both
gradings agree on almost exactly.

### `query-run` — the streaming-query task

Seed 31, six samples, 188 scoreable claims, four arms, 752 verdicts. The claims
are the same kind; what changed is that they are scored against SQL.

| arm | correct | wrong | declined | untouched | coverage | accuracy | hazard | haz/ans |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 30 | 61 | 12 | 85 | 0.5479 | 0.3297 | 0.3245 | 0.6703 |
| `prose` | 80 | 31 | 6 | 71 | 0.6223 | 0.7207 | 0.1649 | 0.2793 |
| `annotated` | 84 | 5 | 3 | 96 | 0.4894 | 0.9438 | 0.0266 | 0.0562 |
| `spec` | 91 | 22 | 5 | 70 | 0.6277 | 0.8053 | 0.1170 | 0.1947 |

Supervisor's rating of the five metrics each arm chose, 0 to 5, opinion and not
measurement:

| arm | derived | useful | executable |
| --- | ---: | ---: | ---: |
| `bare` | 3.67 | 3.33 | 3.83 |
| `prose` | 4.33 | 4.00 | 3.67 |
| `annotated` | 4.17 | 4.00 | 3.67 |
| `spec` | 4.17 | 4.17 | 4.00 |

**Read the violation counts as distinct decisions, not as claims.** Collapsed
that way they are `bare` 11, `prose` 11, `annotated` 3, `spec` 3. The `spec`
arm's 22 violations are three decisions, one of which — dividing by the elapsed
time between records to turn megawatts into megawatt-hours — is scored twenty
times because seventeen fuel members carry the same annotations. Read raw, that
arm looks like a regression; read properly, it is tied for best.

**Descriptions do not change what a reader does.** By distinct decisions the
`prose` arm is exactly level with `bare`, at eleven wrong decisions each, while
the two annotated arms make three. The claim-level figures flatter `prose`
because its mistakes happen to fall on members that carry fewer claims. Prose
told the reader enough to describe the feed correctly, and not enough to make it
write different SQL.

**The unannotated reader is wrong most times it commits.** Its `haz/ans` is
0.6703: of the claims its query engaged at all, two thirds were violated,
against 0.3636 for the same arm on the comprehension task. Prose lets a reader
hedge and SQL does not.

**On the `supportPeriod` claims the separation is total.** Restricted to those
25 claims in this run:

| arm | correct | wrong | untouched |
| --- | ---: | ---: | ---: |
| `bare` | 0 | 18 | 7 |
| `prose` | 4 | 12 | 9 |
| `annotated` | 6 | 0 | 19 |
| `spec` | 7 | 10 | 8 |

`bare` and `prose` both compute a rate by dividing by the interval between
successive records — `/ DATEDIFF(minute, ...)` in one, `3600.0 /
seconds_since_previous_period` in the other — which is verbatim the reading the
keyword exists to forbid. The `annotated` arm never does it.

The `spec` arm does, and that is the uncomfortable half of the result. It had
the annotations and the specification and still derived the period from record
spacing. One of the two annotation-bearing arms honoured the keyword and one did
not, on one sample. The annotation is doing something no description did, and it
is not doing it reliably. Anyone quoting the `annotated` column of that table
should quote the `spec` column beside it.

**The residual mistake is the time axis.** Of the eight distinct non-`bare`
violations, five are one error: naming an operational timestamp in `TIMESTAMP
BY` when the schema annotates a different member as the phenomenon time. One
answer stated the rule and broke it in the same breath, writing `Event time:
TIMESTAMP BY TimeReceived, and no other member` under a schema that marks
`TimeReceived` as `ingestionTime`. An annotation a reader can recite is not yet
an annotation a reader acts on, and that is the strongest argument in either run
for machine-checkable conformance rather than documentation.

One caveat on that count. Stream Analytics permits a single `TIMESTAMP BY` per
input, so an answer that wants an ingestion-lag metric is pushed towards the
operational member, and the rubric scores any such choice as a violation. The
count is an upper bound on carelessness and a lower bound on the awkwardness of
the constraint.

### What the change of supervisor did

Both runs were graded twice on identical transcripts: first by the same model
family as the subject under neutral instructions, then by a different vendor's
model told to be adversarial. Only the grader changed.

| | comprehension `annotated` correct | query `prose` wrong | query `bare` declined |
| --- | ---: | ---: | ---: |
| same family, neutral | 248 | 7 | 83 |
| cross-vendor, adversarial | 190 | 31 | 12 |

The first grading credited the `prose` arm with 20 of 25 `supportPeriod` claims
correct in the query run. Its query divides by `DATEDIFF(minute, ...)`. The
second grading scores those 12 as violations and 4 as correct. That is the
adversarial rule about prose not overriding SQL doing exactly what it was added
to do, and it is the reason the earlier figures should not be quoted.

Both gradings are kept. The earlier one is under `prior-grading/` in each run
directory, complete with its verdicts and quotes.

### What is common to both

Subjects and supervisor were separate sub-agents with no access to this
conversation, this repository, or each other, each given one prompt file and
forbidden any other read. The subjects are one model family; the supervisor is a
different family from a different vendor, and self-identified as such when
asked. That closes the worst of the circularity, but the two vendors' models are
trained on overlapping public data and neither is a domain expert, so this is a
weaker independence than two human reviewers would give.

The blinding half-held. In the comprehension run the supervisor named an
annotated arm 10 times out of 13 and said `cannot tell` 3 times; in the query run
it named one 6 times out of 6. Chance is a half, since two of the four arms are
annotated. The earlier same-family grading said `cannot tell` not once in
nineteen gradings, so the cross-vendor supervisor is measurably less certain
which transcript was richer — but it is still well above chance, and no figure
here is protected by the blinding.

**The `spec` arm buying little is the result the design wants.** In the
comprehension run it costs one more violation than `annotated` and buys 0.039 of
coverage; in the query run it buys 0.138 of coverage and, on the one sample where
it matters, loses the `supportPeriod` constraint that `annotated` kept. An
annotation vocabulary earns its keep by being legible where it is used; if a
reader had to fetch the specification to work out what `supportPeriod` meant, the
keyword would be doing less work than a sentence of prose. On distinct decisions
the two arms are tied at three, which is the honest summary: reading the
specification neither rescued nor damaged the result.

That conclusion is bounded by what the arms were asked to do. Neither task asks
anyone to decide conformance. Nothing here shows the specification is
unnecessary to an implementer who must apply the resolution order, the
prohibitions, or the cardinality of the boundary roles; those are rules a reader
cannot recover from a well-named keyword and were never put to the subject.

## Running it

Build every prompt without calling a model, and read them:

```
python run.py --transport none --out results/dry
```

The streaming-query task instead of the comprehension task:

```
python run.py --task query --transport none --out results/dry-query
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
python run.py --report recorded-run
```

Inspect the rubric for one sample:

```
python rubric.py ../samples/real-world/20-goes-magnetometer/schema.struct.json
```

Every run directory holds, per sample, the full subject prompt and response for
each arm, the full supervisor prompt and response, a result file with the claims
and verdicts, and the arm assignment. The seed is recorded so the assignment can
be reproduced. Nothing is summarised without the material behind it being kept.

New runs go wherever `--out` points, and `results/` is ignored by git so that
working runs stay local. `recorded-run` and `query-run` are the exceptions: they
are kept under version control so that the figures quoted above can be checked
against the transcripts that produced them. Their copies of `specification.md`
are not kept, being duplicates of the draft two directories up; `--emit` writes
one again when a run needs it.

Each also holds a `prior-grading/` directory: the verdicts, results and summary
from the first, same-family, non-adversarial grading of the very same
transcripts. Nothing else differs between the two, so the pair is the only
honest measure this harness has of how much a supervisor's identity and stance
move the numbers. `--report` ignores it.
