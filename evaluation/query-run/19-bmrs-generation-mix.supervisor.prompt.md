You are a supervisor. You grade four answers against a fixed list of claims.

Each answer proposes five derived metrics for a data feed and gives one
streaming SQL query that computes them. You are not being asked whether an
answer is well written. You are asked two separate questions, and you must keep
them separate.

## Your stance

You are an adversarial grader. The answers were written by a different model
from a different vendor, and you are the hostile check on them. Assume each is
trying to look more competent than its SQL is, and grade so that the appearance
earns nothing.

Credit is earned, never assumed. You are not rewarded for being fair to an
answer, and a grader who credits an answer with a constraint it did not actually
honour has failed at this task. Where you genuinely cannot decide, withhold the
credit.

The query is the answer. Prose around it is a claim about the query, and a claim
about the query is not the query. When the notes and the SQL disagree, the SQL
is what the answer does and the notes are what it wishes it did.

This severity applies identically to all four transcripts. You are hostile to
unearned credit, not to any particular transcript.

You will be given:

* **CLAIMS** — numbered propositions. Each is true of the data these answers
  work on. Most carry a `wrong reading`: the specific error the claim exists to
  rule out.
* **TRANSCRIPT A**, **TRANSCRIPT B**, **TRANSCRIPT C** and **TRANSCRIPT D** —
  four independent answers, produced under conditions you are not told. They are
  not in any meaningful order. Do not speculate about the conditions while
  grading.

## Part 1 — correctness, claim by claim

For each claim, and separately for each of the four transcripts, choose exactly
one verdict. Every claim therefore receives four verdicts.

Judge the query and its accompanying notes together. What matters is whether the
computation the answer specifies is compatible with the claim.

* `correct` — the answer computes something that depends on the claim being
  true and treats it correctly, or its notes state the claim as a reason for
  what it computed or refused to compute.
* `incorrect` — the answer computes something the claim forbids. Averaging a
  quantity the claim says must not be averaged; summing across a boundary the
  claim says values may not be summed across; taking the wrong member as the
  event time in `TIMESTAMP BY`; differencing two values the claim says are not
  comparable; deriving a duration the claim says is not recoverable. The wrong
  reading committed in SQL is `incorrect` whether or not the prose admits it.
* `declined` — the answer raises the matter and explicitly does not settle it:
  it lists the computation among what it did not compute, or marks its handling
  as an assumption.
* `unaddressed` — the answer neither relies on the claim nor violates it. Most
  claims will be `unaddressed` for most transcripts, because five metrics cannot
  touch everything. That is expected and is not a fault.

Rules you must follow.

1. Judge only what is written. Do not credit an answer for a constraint you
   believe it understood but did not act on or state.
2. For `correct` and `incorrect` you MUST supply `quote`: a verbatim span from
   that transcript, copied exactly, that carries the verdict. A line of SQL is a
   good quote. If you cannot find one, the verdict is `unaddressed`.
3. **Prose does not override SQL.** An answer that states a constraint correctly
   in its notes and violates it in the query is `incorrect`. An answer whose
   notes promise a metric the query does not compute has not computed it. Where
   the two conflict, quote the SQL.
4. **Look for the violation before you look for the compliance.** Search the
   query for the wrong reading the claim exists to rule out, and settle that
   question first. Only if it is absent may you consider `correct`.
5. **Handling a constraint by accident is not `correct`.** A query earns
   `correct` when the computation depends on the claim being true, or the notes
   name the claim as the reason. A computation that happens not to trip over a
   constraint it never considered is `unaddressed`.
6. Do not round up. A metric that is right in form and wrong in the respect the
   claim is about is `incorrect`, not partial credit.
7. Do not use your own knowledge of the subject matter to decide a claim. The
   claim is the ground truth. If an answer contradicts a claim, that is
   `incorrect` even if you personally believe the answer.
8. Confidence is not evidence. A long, well-commented, professional-looking
   query gets no benefit of the doubt over a plain one.
9. Grade the four transcripts independently. Do not let one inform another, and
   do not compare them.
10. Silence is not a violation. An answer that never computes anything touching
    a claim is `unaddressed`, not `incorrect`. Severity means withholding
    credit, not inventing violations, and most claims being `unaddressed` is the
    expected outcome because five metrics cannot touch everything.

## Part 2 — quality of the selection

Separately, and only after Part 1 is finished, rate each transcript on three
scales from 0 to 5. This part is a judgement, is reported on its own, and is
never mixed into the claim scoring.

Rate these adversarially too. 3 is a competent answer. Reserve 5 for one you
could not improve, and do not award it to avoid seeming harsh.

* `derived` — are the five genuinely computed quantities rather than fields
  carried through or trivially renamed? 5 = all five are real computations.
* `useful` — would someone operating this feed actually want these five, and are
  they the most valuable five on offer? 5 = an expert would choose much the same.
* `executable` — is the query one statement of valid Stream Analytics SQL that
  would run against this schema, with a sound `TIMESTAMP BY`, well-formed
  windows, and correct member names? 5 = would run as written. Deduct for every
  member name that is not in the schema, every window that is malformed, and
  every construct the dialect does not have.

Add `note`: one sentence naming the single strongest and single weakest thing
about that answer's selection.

## Answer

JSON only, no prose before or after, in exactly this form:

```json
{
  "verdicts": [
    {"claim": 1, "transcript": "A", "verdict": "correct", "quote": "..."},
    {"claim": 1, "transcript": "B", "verdict": "unaddressed"},
    {"claim": 1, "transcript": "C", "verdict": "declined"},
    {"claim": 1, "transcript": "D", "verdict": "incorrect", "quote": "..."}
  ],
  "quality": {
    "A": {"derived": 4, "useful": 3, "executable": 5, "note": "..."},
    "B": {"derived": 5, "useful": 4, "executable": 4, "note": "..."},
    "C": {"derived": 3, "useful": 3, "executable": 5, "note": "..."},
    "D": {"derived": 4, "useful": 5, "executable": 3, "note": "..."}
  },
  "blinding": {"richest": "A" | "B" | "C" | "D" | "cannot tell", "why": "one sentence"}
}
```

The `blinding` field is not part of the grading and is not scored. It records
which transcript appeared to have had the most material available to it, and
whether you could tell at all. Answer it last, answer it honestly, and say
`cannot tell` if you cannot tell.


---

CLAIMS

1. `start_time` carries phenomenon time -- when the thing being described happened. Time series, windowing, and joins to other feeds are built on it.
   wrong reading: Treating `start_time` as the time the record was produced, received, or published, or using a different member for event time.

2. Successive `start_time` values are expected at cadence `fixed` with period "PT30M". A cadence is an expectation and not a constraint: a record that departs from it is late, not invalid, and a missing value must not be filled in because the cadence says one was due.
   wrong reading: Treating the cadence as a guarantee of completeness or as a validation rule, or interpolating absent values from it.

3. `ccgt_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `ccgt_mw` as though it were a raw sample.

4. `ccgt_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `ccgt_mw` as an instantaneous reading.

5. `ccgt_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `ccgt_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

6. `ccgt_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `ccgt_mw`.

7. `ocgt_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `ocgt_mw` as though it were a raw sample.

8. `ocgt_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `ocgt_mw` as an instantaneous reading.

9. `ocgt_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `ocgt_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

10. `ocgt_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `ocgt_mw`.

11. `coal_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `coal_mw` as though it were a raw sample.

12. `coal_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `coal_mw` as an instantaneous reading.

13. `coal_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `coal_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

14. `coal_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `coal_mw`.

15. `oil_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `oil_mw` as though it were a raw sample.

16. `oil_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `oil_mw` as an instantaneous reading.

17. `oil_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `oil_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

18. `oil_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `oil_mw`.

19. `nuclear_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `nuclear_mw` as though it were a raw sample.

20. `nuclear_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `nuclear_mw` as an instantaneous reading.

21. `nuclear_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `nuclear_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

22. `nuclear_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `nuclear_mw`.

23. `wind_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `wind_mw` as though it were a raw sample.

24. `wind_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `wind_mw` as an instantaneous reading.

25. `wind_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `wind_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

26. `wind_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `wind_mw`.

27. `biomass_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `biomass_mw` as though it were a raw sample.

28. `biomass_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `biomass_mw` as an instantaneous reading.

29. `biomass_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `biomass_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

30. `biomass_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `biomass_mw`.

31. `npshyd_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `npshyd_mw` as though it were a raw sample.

32. `npshyd_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `npshyd_mw` as an instantaneous reading.

33. `npshyd_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `npshyd_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

34. `npshyd_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `npshyd_mw`.

35. `ps_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `ps_mw` as though it were a raw sample.

36. `ps_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `ps_mw` as an instantaneous reading.

37. `ps_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `ps_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

38. `ps_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `ps_mw`.

39. `other_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `other_mw` as though it were a raw sample.

40. `other_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `other_mw` as an instantaneous reading.

41. `other_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `other_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

42. `other_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `other_mw`.

43. `intfr_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `intfr_mw` as though it were a raw sample.

44. `intfr_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `intfr_mw` as an instantaneous reading.

45. `intfr_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `intfr_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

46. `intfr_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `intfr_mw`.

47. `intifa2_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `intifa2_mw` as though it were a raw sample.

48. `intifa2_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `intifa2_mw` as an instantaneous reading.

49. `intifa2_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `intifa2_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

50. `intifa2_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `intifa2_mw`.

51. `intned_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `intned_mw` as though it were a raw sample.

52. `intned_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `intned_mw` as an instantaneous reading.

53. `intned_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `intned_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

54. `intned_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `intned_mw`.

55. `intnem_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `intnem_mw` as though it were a raw sample.

56. `intnem_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `intnem_mw` as an instantaneous reading.

57. `intnem_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `intnem_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

58. `intnem_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `intnem_mw`.

59. `intelec_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `intelec_mw` as though it were a raw sample.

60. `intelec_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `intelec_mw` as an instantaneous reading.

61. `intelec_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `intelec_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

62. `intelec_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `intelec_mw`.

63. `intnsl_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `intnsl_mw` as though it were a raw sample.

64. `intnsl_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `intnsl_mw` as an instantaneous reading.

65. `intnsl_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `intnsl_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

66. `intnsl_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `intnsl_mw`.

67. `intvkl_mw` is already a `mean` over a set of values. Re-applying an aggregate to it does not yield that aggregate of the underlying data -- a mean of means is not a mean, and an extremum of extrema is only valid for the same function.
   wrong reading: Averaging or summing `intvkl_mw` as though it were a raw sample.

68. `intvkl_mw` characterises a half-open period given by sibling boundary members, not a single instant.
   wrong reading: Treating `intvkl_mw` as an instantaneous reading.

69. `intvkl_mw` characterises a phenomenon-time period of length PT30M, stated by the schema rather than carried in the record. The period opens at the anchoring position and runs forward from it. The anchoring position is the sibling annotated `phenomenonTimeStart`, or `phenomenonTime` where the record carries no member in that role. For an anchoring position `t`, the period is `[t, t + PT30M)`.
   wrong reading: Treating `intvkl_mw` as an instantaneous reading at the record timestamp, running its period back from the anchoring position, or deriving its length from the cadence or from the spacing of successive records.

70. `intvkl_mw` is expressed in `MW`.
   wrong reading: Assuming a different or conventional unit for `intvkl_mw`.


TRANSCRIPT A

# GenerationMix — five derived metrics

## 1. The five metrics

1. **`total_mw` — the summed level across the whole closed member set.** The schema is `additionalProperties: false`, so the seventeen `_mw` members *are* the record; their sum is the only complete level the feed carries, and it is the denominator every other proportional metric needs.
2. **`ramp_mw_per_min` — signed change in `total_mw` between successive records, divided by the elapsed wall time between their `start_time` values.** An operator acts on rate of change, not level: a large negative ramp is the shape of a loss, a large positive ramp the shape of a pick-up, and both are invisible in the raw record.
3. **`net_int_mw` and `int_share_pct` — the signed sum of the seven `int`-prefixed members, and that sum as a percentage of `total_mw`.** The instance shows `intnem_mw` and `intelec_mw` negative while `intfr_mw`, `intifa2_mw`, `intned_mw`, `intnsl_mw`, `intvkl_mw` are positive, so this subgroup is the one part of the record demonstrated to reverse sign; its net and its weight tell the operator how much of the level is coming from a direction that can flip.
4. **`stdev_total_mw` and `range_total_mw` — dispersion of `total_mw` within the window.** Two records can share a mean and differ entirely in how settled they were; volatility is what distinguishes a steady window from one that was chased, and it is the natural threshold on which to alarm.
5. **`avg_member_completeness_pct` and `period_breaks_in_window` — the share of the seventeen optional `_mw` members actually present, and the count of `settlement_period` steps that were not `+1`.** Only `settlement_period` and `start_time` are required, so a record missing twelve members still parses and still produces a `total_mw` that is silently too low; this metric says whether the other four are computed on a whole record and an unbroken sequence, or not.

## 2. The query

```sql
-- Single statement.
--
-- PARTITIONING: nothing in GenerationMix identifies an individual source.
-- There is no id, station, region or unit member; `settlement_period` is a
-- bounded cycle index (1..50), not an identity. So there is no PARTITION BY
-- anywhere in this query and the feed is treated as one series.
--
-- DIALECT NOTE: COALESCE, ABS and CASE are used below and were not named in
-- the dialect notes I was given. I believe all three are supported here, but
-- I am flagging them as the one place I could not check. If COALESCE is
-- unavailable, each `COALESCE(x, 0)` becomes `CASE WHEN x IS NULL THEN 0
-- ELSE x END`; if ABS is unavailable, `MAX(ABS(r))` becomes
-- `MAX(CASE WHEN r < 0 THEN -r ELSE r END)`.

WITH Levels AS (
    SELECT
        System.Timestamp()  AS event_time,
        settlement_period,

        -- METRIC 1. Sum over the closed member set. `additionalProperties` is
        -- false, so these seventeen members are exhaustive for this type and
        -- the sum is complete by construction. COALESCE because every _mw
        -- member is optional -- only settlement_period and start_time are
        -- required -- and one NULL would otherwise null the whole total.
          COALESCE(ccgt_mw,    0) + COALESCE(ocgt_mw,   0)
        + COALESCE(coal_mw,    0) + COALESCE(oil_mw,    0)
        + COALESCE(nuclear_mw, 0) + COALESCE(wind_mw,   0)
        + COALESCE(biomass_mw, 0) + COALESCE(npshyd_mw, 0)
        + COALESCE(ps_mw,      0) + COALESCE(other_mw,  0)
        + COALESCE(intfr_mw,   0) + COALESCE(intifa2_mw, 0)
        + COALESCE(intned_mw,  0) + COALESCE(intnem_mw,  0)
        + COALESCE(intelec_mw, 0) + COALESCE(intnsl_mw,  0)
        + COALESCE(intvkl_mw,  0)                             AS total_mw,

        -- METRIC 3 (part). Signed net of the seven int-prefixed members.
        -- Deliberately NOT wrapped in ABS: the instance carries intnem_mw and
        -- intelec_mw negative alongside five positive siblings, so the sign of
        -- this sum is information, and the cancellation inside it is real.
          COALESCE(intfr_mw,   0) + COALESCE(intifa2_mw, 0)
        + COALESCE(intned_mw,  0) + COALESCE(intnem_mw,  0)
        + COALESCE(intelec_mw, 0) + COALESCE(intnsl_mw,  0)
        + COALESCE(intvkl_mw,  0)                             AS net_int_mw,

        -- METRIC 5 (part). How many of the seventeen optional _mw members this
        -- record actually carried. Conditions the trustworthiness of total_mw.
          (CASE WHEN ccgt_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN ocgt_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN coal_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN oil_mw     IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN nuclear_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN wind_mw    IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN biomass_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN npshyd_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN ps_mw      IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN other_mw   IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intfr_mw   IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intifa2_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intned_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intnem_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intelec_mw IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intnsl_mw  IS NOT NULL THEN 1 ELSE 0 END)
        + (CASE WHEN intvkl_mw  IS NOT NULL THEN 1 ELSE 0 END) AS members_present

    -- start_time is the only datetime member in the schema, so it is the only
    -- candidate for event time. No PARTITION BY: see header note.
    FROM input TIMESTAMP BY start_time
),

Deltas AS (
    -- Reach the previous record. No PARTITION BY, for the reason above.
    -- LIMIT DURATION(hour, 2) is required by the dialect; two hours is four
    -- times the assumed 30-minute cadence, so it survives up to three
    -- consecutive dropped periods before LAG returns NULL.
    SELECT
        event_time,
        settlement_period,
        total_mw,
        net_int_mw,
        members_present,
        LAG(total_mw, 1)          OVER (LIMIT DURATION(hour, 2)) AS prev_total_mw,
        LAG(settlement_period, 1) OVER (LIMIT DURATION(hour, 2)) AS prev_period,
        DATEDIFF(second,
                 LAG(event_time, 1) OVER (LIMIT DURATION(hour, 2)),
                 event_time)                                     AS gap_seconds
    FROM Levels
),

Rates AS (
    SELECT
        event_time,
        total_mw,
        net_int_mw,
        members_present,

        -- METRIC 2. Signed MW per minute. NULL rather than 0 on the first
        -- record and on any non-positive elapsed time, so that a missing
        -- comparison never masquerades as a flat ramp in the AVG below.
        CASE
            WHEN prev_total_mw IS NULL OR gap_seconds IS NULL OR gap_seconds <= 0
                THEN NULL
            ELSE (total_mw - prev_total_mw) * 60.0 / gap_seconds
        END AS ramp_mw_per_min,

        -- METRIC 3 (part). Share is only defined against a positive
        -- denominator; the schema places no lower bound on any _mw member, so
        -- total_mw is not guaranteed positive and the share is nulled when it
        -- is not.
        CASE
            WHEN total_mw > 0 THEN 100.0 * net_int_mw / total_mw
            ELSE NULL
        END AS int_share_pct,

        -- METRIC 5 (part). settlement_period is declared 1..50 and is assumed
        -- to advance by exactly one per record. A step to 1 is treated as a
        -- cycle reset, not a break, because the schema fixes only the upper
        -- bound (50) and not the cycle length, so the value the sequence
        -- resets *from* is not knowable here.
        CASE
            WHEN prev_period IS NULL                       THEN 0
            WHEN settlement_period = prev_period + 1       THEN 0
            WHEN settlement_period = 1                     THEN 0
            ELSE 1
        END AS period_break
    FROM Deltas
)

-- Window: HoppingWindow(minute, 180, 30) -- a 180-minute window advancing in
-- 30-minute hops. Size chosen to hold six records and hop chosen to emit once
-- per record, both under the assumed 30-minute cadence (assumption 3). Six
-- samples is the smallest window on which STDEV is worth reading; the hop
-- keeps the alarm latency down to one settlement period rather than one
-- window.
SELECT
    System.Timestamp()                                  AS window_end,
    COUNT(*)                                            AS records_in_window,

    -- 1. level
    AVG(total_mw)                                       AS avg_total_mw,
    MIN(total_mw)                                       AS min_total_mw,
    MAX(total_mw)                                       AS max_total_mw,

    -- 2. rate of change
    AVG(ramp_mw_per_min)                                AS avg_ramp_mw_per_min,
    MAX(ABS(ramp_mw_per_min))                           AS peak_abs_ramp_mw_per_min,

    -- 3. int-prefixed subgroup, signed
    AVG(net_int_mw)                                     AS avg_net_int_mw,
    MIN(net_int_mw)                                     AS min_net_int_mw,
    AVG(int_share_pct)                                  AS avg_int_share_pct,

    -- 4. dispersion
    STDEV(total_mw)                                     AS stdev_total_mw,
    MAX(total_mw) - MIN(total_mw)                       AS range_total_mw,

    -- 5. integrity of the four above
    AVG(CAST(members_present AS float)) * 100.0 / 17.0  AS avg_member_completeness_pct,
    SUM(period_break)                                   AS period_breaks_in_window
INTO output
FROM Rates
GROUP BY HoppingWindow(minute, 180, 30)
```

Sanity check against the one instance: `total_mw` = 22 871 (the ten non-`int` members) + 5 588 (the seven `int` members) = 28 459; `net_int_mw` = 5 588; `int_share_pct` = 19.64; `members_present` = 17, so completeness = 100 %.

## 3. What I did not compute

* **Per-member share of `total_mw` for each of the seventeen `_mw` members.** A share presumes the parts partition a whole. `intnem_mw` is −412.0 and `intelec_mw` is −184.0 in the instance, so the members do not partition `total_mw`; percentages over a set containing negatives sum to 100 % only by accident and are not comparable between records. I compute a share only for the aggregated `net_int_mw`, and interpret it as signed.
* **A Herfindahl or any concentration/diversity index over the members.** It requires squaring non-negative shares. `intnem_mw` and `intelec_mw` are negative; dropping them to force non-negativity would silently change the denominator, so the index would not be comparable record to record.
* **Any grouping of `ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw` as one class, or of `wind_mw`, `npshyd_mw`, `biomass_mw`, `ps_mw` as another.** The schema declares no such taxonomy — no enum, no annotation, no grouping construct — and the instance does not imply one. That classification is domain knowledge these two files do not carry, so no "thermal", "renewable", "low-carbon" or "dispatchable" aggregate appears above. The one grouping I did make, the seven `int`-prefixed members, rests on the shared name prefix alone and is flagged as assumption 2.
* **A reconciliation residual: reported total minus computed total.** This is the metric an operator of a summed feed most wants, and the feed cannot support it. There is no total member, and `additionalProperties: false` means one cannot arrive later. Nothing declares a reference for `total_mw` to be checked against, so no residual is computed.
* **Capacity factor, utilisation, or headroom for any member.** No nameplate, capacity, availability or limit member exists in the schema. Every such ratio would require a denominator I would have to invent.
* **A negative-value error flag on `ccgt_mw`, `coal_mw`, `nuclear_mw` and the other non-`int` members.** The schema author declared `minimum: 1` and `maximum: 50` on `settlement_period` and declared no bounds at all on any `_mw` member. They demonstrably knew how to constrain a value and chose not to constrain these, so a negative `coal_mw` is not licensed as an anomaly and I do not flag it.
* **Any charge/discharge, state-of-charge or round-trip treatment of `ps_mw`.** Nothing in the schema or the instance establishes that `ps_mw` is a store or that it is bidirectional; it is +742.0 in the one record available. It is summed into `total_mw` like every other member and given no special handling.
* **`SessionWindow` for outage detection.** Considered as the mechanism for metric 5. Rejected because `settlement_period` gives a direct, schema-licensed sequence test (`prev_period + 1`) that needs no timeout parameter, whereas a session timeout is a number I would have had to invent.
* **`PERCENTILE_CONT` on `total_mw`.** Available in the dialect and sound here, but over the six records a 180-minute window holds it adds nothing `MIN`, `MAX` and `STDEV` do not already say. Omitted as padding.
* **Suppressing the ramp across a `settlement_period` reset to 1.** Not done deliberately: `ramp_mw_per_min` divides by elapsed wall clock from `start_time`, which is well defined across a cycle boundary. Only the `period_break` flag treats the reset specially.

## 4. Assumptions

1. **Assumption — the `_mw` suffix means megawatts, and all seventeen members share that unit, so they may be added.** The schema declares no unit anywhere. Its `$uses` list names only `JSONStructureValidation`, so no units extension is in play; the unit exists solely in the member names. Every sum, ramp and share above fails if the members are not commensurable.
2. **Assumption — the `int` prefix marks a coherent subgroup**, so that `intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`, `intelec_mw`, `intnsl_mw` and `intvkl_mw` are the same kind of thing and their signed sum is meaningful. This rests on the shared prefix and on the observation that these are the only members negative in the instance. Nothing in the schema declares the group.
3. **Assumption — the cadence is one record per 30 minutes.** Inferred from a single instance: `settlement_period` 12 with `start_time` 2026-07-31T05:30:00Z is consistent with period *n* beginning (*n* − 1) × 30 minutes after midnight, and `maximum: 50` is consistent with a cycle of roughly a day at that spacing. One record is weak evidence. The `HoppingWindow(minute, 180, 30)` hop, the window size, and the `LIMIT DURATION(hour, 2)` on both `LAG` calls all depend on this; if the cadence differs, all three need re-sizing, though the metrics themselves do not change.
4. **Assumption — `settlement_period` advances by exactly one between consecutive records and resets to 1 at the start of each cycle.** The schema bounds it 1..50 but says nothing about its progression. `period_break` is built on this, and treats a step to 1 as a legitimate reset rather than a break.
5. **Assumption — `start_time` is the start of the interval the record describes, not the time the record was produced.** Taken from the member name. Consequence: `TIMESTAMP BY start_time` stamps each record at the opening of its interval, so a window closing at *T* includes a record whose interval is still running past *T*. Every windowed figure is therefore aligned on interval starts, not on interval coverage.
6. **Assumption — records are not revised or republished.** If the feed restates a settlement period, `LAG` compares the restatement against the record before it and `ramp_mw_per_min` is wrong for two consecutive outputs. Nothing in the two files establishes revision behaviour, and there is no version, sequence or revision member to detect it with.
7. **Assumption — a missing optional `_mw` member means the quantity is absent, and substituting 0 is the right null policy.** Every `_mw` member is optional; the alternative — nulling `total_mw` whenever any member is missing — would blank the whole metric on one absent value. `avg_member_completeness_pct` exists precisely to expose the resulting understatement, but it is an assumption that 0-substitution is preferable.
8. **Assumption — `total_mw` is positive whenever a share is meaningful.** No `_mw` member has a declared `minimum`, so a non-positive total is possible; `int_share_pct` is nulled in that case rather than returning a signed or infinite ratio.
9. **Assumption — the stream carries a single source.** The schema has no identifying member, which is why there is no `PARTITION BY`. This further assumes the feed does not multiplex several sources into one stream distinguished by something outside the record body, such as a partition key or a transport header; if it does, `LAG` interleaves unrelated series and metric 2 and metric 5 are both invalid.
10. **Assumption — `COALESCE`, `ABS` and `CASE` are supported in this dialect.** They were not named in the notes I was given. Substitutions for the first two are given in the query header comment.


TRANSCRIPT B

# GenerationMix — five derived metrics

## 1. The five metrics

All five are computed on a rolling six-hour window hopped every 30 minutes, so one row is emitted per settlement period and each row summarises the twelve periods up to it.

1. **Rolling 6-hour metered generation energy (MWh)** — `SUM` of the ten fuel members × 0.5 h, turning a stream of period *means* into the volume quantity; an operator needs the volume before any mix number means anything, and it is the denominator for metric 2.
2. **Rolling 6-hour wind share of metered generation (%)** — the mix headline this feed exists to carry; because every period is the same length the ratio of sums *is* the energy share, and it is a lower bound on GB wind because `wind_mw` covers only Balancing-Mechanism-metered units.
3. **Largest half-hour ramp of metered generation in the window (MW/min)** — how hard the system had to move between consecutive periods, which is what sizes response and reserve; computed from `start_time` differences rather than `settlement_period`, so it stays correct across a clock change.
4. **Rolling 6-hour net interconnector energy (MWh, signed, positive = import)** — how much of supply arrived across cables and in which direction; the seven `int*` members share one sign convention, so summing them with one another is the one cross-member sum the schema licenses.
5. **Standard deviation of `wind_mw` across the window (MW)** — dispersion of the uncontrolled component at a given mean, distinguishing a steady 6 GW of wind from a swinging one, which metric 1 and metric 2 cannot show.

## 2. The query

```sql
-- Event time is start_time: it is the only datetime member, and the feed
-- carries no end instant.  settlement_period is deliberately never used in
-- arithmetic (see section 3).
--
-- Dialect hedge: I am not certain COALESCE is available in this dialect.  If it
-- is not, replace each COALESCE(x, 0) with CASE WHEN x IS NULL THEN 0 ELSE x END.
-- ABS, STDEV, DATEDIFF and LAG ... LIMIT DURATION are assumed available.

WITH period AS (
    SELECT
        System.Timestamp()                    AS period_start,   -- = start_time
        COALESCE(ccgt_mw,    0)
      + COALESCE(ocgt_mw,    0)
      + COALESCE(coal_mw,    0)
      + COALESCE(oil_mw,     0)
      + COALESCE(nuclear_mw, 0)
      + COALESCE(wind_mw,    0)
      + COALESCE(biomass_mw, 0)
      + COALESCE(npshyd_mw,  0)
      + COALESCE(ps_mw,      0)
      + COALESCE(other_mw,   0)               AS gen_mw,         -- fuel members only
        COALESCE(wind_mw, 0)                  AS wind_mw,
        COALESCE(intfr_mw,   0)
      + COALESCE(intifa2_mw, 0)
      + COALESCE(intned_mw,  0)
      + COALESCE(intnem_mw,  0)
      + COALESCE(intelec_mw, 0)
      + COALESCE(intnsl_mw,  0)
      + COALESCE(intvkl_mw,  0)               AS net_import_mw   -- signed, + = import
    FROM input
    TIMESTAMP BY start_time
),

-- No member identifies an individual source, so there is no PARTITION BY here
-- or anywhere else in the query.  LIMIT DURATION is required on LAG.
lagged AS (
    SELECT
        period_start,
        gen_mw,
        wind_mw,
        net_import_mw,
        LAG(gen_mw,       1) OVER (LIMIT DURATION(hour, 2)) AS prev_gen_mw,
        LAG(period_start, 1) OVER (LIMIT DURATION(hour, 2)) AS prev_period_start
    FROM period
),

ramped AS (
    SELECT
        period_start,
        gen_mw,
        wind_mw,
        net_import_mw,
        CASE
            WHEN prev_period_start IS NOT NULL
             AND DATEDIFF(minute, prev_period_start, period_start) > 0
            THEN (gen_mw - prev_gen_mw)
                 / DATEDIFF(minute, prev_period_start, period_start)
            ELSE NULL
        END AS gen_ramp_mw_per_min
    FROM lagged
)

SELECT
    System.Timestamp()                                  AS window_end,

    -- 1. mean MW over a half-hour period -> MWh, summed over the window
    SUM(gen_mw) * 0.5                                   AS metered_generation_mwh_6h,

    -- 2. equal period lengths make the ratio of sums the energy share exactly
    CASE WHEN SUM(gen_mw) > 0
         THEN 100.0 * SUM(wind_mw) / SUM(gen_mw)
         ELSE NULL
    END                                                 AS wind_share_of_metered_pct_6h,

    -- 3. magnitude only; direction is discarded on purpose
    MAX(ABS(gen_ramp_mw_per_min))                       AS max_abs_gen_ramp_mw_per_min_6h,

    -- 4. signed, positive = net import to GB
    SUM(net_import_mw) * 0.5                            AS net_interconnector_mwh_6h,

    -- 5. dispersion of the uncontrolled component
    STDEV(wind_mw)                                      AS wind_stdev_mw_6h

INTO output
FROM ramped
-- HoppingWindow: 360-minute (6 h) window, 30-minute hop.  The hop matches the
-- declared half-hourly publication cadence, so one row is emitted per
-- settlement period and each window holds twelve periods.
GROUP BY HoppingWindow(minute, 360, 30)
```

## 3. What I did not compute

* **Total system supply as generation plus interconnectors** — the ten fuel members summed with the seven `int*` members. The schema says the interconnector values "may not be summed with the generation members without deciding how exports are to be treated", and the instance carries genuine negatives (`intnem_mw` = −412, `intelec_mw` = −184) which would silently cancel real generation. I kept the two sums apart as metrics 1 and 4 instead of deciding on the operator's behalf.
* **A combined gas total, `ccgt_mw` + `ocgt_mw`** — the schema states these are operationally unrelated fleets, bulk dispatched energy against minutes-at-a-time reserve. Their sum is a number nobody acts on.
* **A net or round-trip storage position from `ps_mw`** — the schema says the pumping load is metered as demand elsewhere and does not appear here as a negative, so `ps_mw` is not a net position and no storage balance is computable from this feed. It is included in metric 1 only as gross output.
* **A low-carbon or renewable share** (some combination of `nuclear_mw`, `wind_mw`, `npshyd_mw`, `biomass_mw`, `ps_mw`) — neither file establishes an emissions attribute for any member or a definition of "renewable", and where biomass and pumped storage fall is exactly the contested part. Writing it would be importing domain knowledge the files do not license.
* **Anything keyed on `settlement_period`** — no period-over-period differencing indexed by period number, and no settlement-day aggregate defined as periods 1..*n*. The schema says the count per day is 46, 48 or 50 and that arithmetic across a clock change is wrong; it also says periods are numbered from 1 at midnight UTC, and both cannot hold of a fixed 24-hour UTC day. I cannot delimit a settlement day soundly, so I did not attempt daily energy totals, and every time calculation in the query uses `start_time`.
* **Interconnector utilisation or capacity factor** — the schema notes that IFA and IFA2 have separate capacities but gives no capacity value for any cable and carries no capacity member, so `intfr_mw` / capacity and its siblings are not computable.
* **A true wind share of GB generation** — `wind_mw` omits distribution-connected wind and the files supply no figure for it, so I labelled metric 2 as a share of *metered* generation rather than presenting an understated number as the real one.
* **A feed-completeness counter** (`COUNT(*)` against the twelve half-hours a six-hour UTC window should contain) — this would be sound, since UTC is continuous through a clock change, but it ranks sixth and the brief is five.
* **`PERCENTILE_CONT` on any member** — twelve samples per window is too few for a stable percentile, so `STDEV` is the honest dispersion statistic here.

## 4. Assumptions

* **Assumption:** every record covers exactly half an hour, so a mean in MW multiplied by 0.5 is MWh. The schema states the period length; I rely on it for metrics 1 and 4.
* **Assumption:** consecutive `start_time` values are 30 minutes apart in UTC even across a GB clock change, and the publisher does not republish or restate a period. A restatement would be counted twice by the window sums and would produce a spurious zero-length interval in the ramp guard.
* **Assumption:** an absent optional member means zero output. Only `settlement_period` and `start_time` are required, so any fuel or cable may be missing, and the query cannot tell "not published" from "genuinely zero" — the instance carries real 0.0 values in `ocgt_mw`, `coal_mw` and `oil_mw`. If absence should instead void the total, remove the `COALESCE` wrappers so the sum becomes null.
* **Assumption:** the input is a single GB-wide stream. Nothing in the schema identifies an individual source, so there is no partition key; if several regions or publishers were multiplexed onto one input the query would silently mix them.
* **Assumption:** events arrive in or near event-time order and within whatever late-arrival tolerance is configured on the job. `LIMIT DURATION(hour, 2)` assumes the previous period is reachable within two hours; the out-of-order policy itself is job configuration, not part of this query.
* **Assumption:** the six-hour window and 30-minute hop are my choice, not something the files state. The hop is set to the declared half-hourly cadence so there is one output per settlement period; six hours gives twelve samples, enough for `STDEV` to mean something.
* **Assumption:** `System.Timestamp()` in the non-windowed step yields the event's own timestamp, i.e. `start_time`, and in the windowed `SELECT` yields the window end. Because `start_time` is the *start* of a period, `window_end` is the start instant of the newest period in the window and the underlying half hour runs 30 minutes past that stamp.
* **Assumption:** all seven `int*` members use the same sign convention, positive for import to GB. The schema states this for each of them individually, which is what makes their mutual sum in metric 4 legitimate.
* **Assumption (design choice, stated for clarity):** metric 3 reports ramp magnitude via `MAX(ABS(...))` and discards whether the swing was up or down, so that one column answers "how hard did the system have to move".
* **Assumption:** `COALESCE`, `ABS` and `STDEV` exist in this dialect. The query carries a comment with a `CASE`-based replacement for `COALESCE` in case it does not.


TRANSCRIPT C

# GB generation mix — five derived metrics

## 1. The five metrics

1. **Total metered generation output (MW).** The sum of the ten fuel members (`ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw`, `nuclear_mw`, `wind_mw`, `biomass_mw`, `npshyd_mw`, `ps_mw`, `other_mw`), interconnectors deliberately excluded. No member carries it and every share below is measured against it, so it is the first number an operator reads and the denominator for the rest.
2. **Half-hour wind ramp (MW per settlement period).** `wind_mw` minus its value in the immediately preceding period, emitted only when the two `start_time` values are exactly 1800 seconds apart. This is the swing the rest of the fleet had to absorb between one period and the next, and it is the single quantity that decides whether the coming period is comfortable.
3. **Wind share of metered generation output (fraction).** `wind_mw` divided by metric 1. The headline mix number — and the one whose denominator must be named, because `wind_mw` covers only Balancing-Mechanism-metered units and the denominator excludes imports, so this is a share of the metered mix and not of GB generation.
4. **Net interconnector position (MW, positive = net import to GB).** The signed sum of the seven cable members (`intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`, `intelec_mw`, `intnsl_mw`, `intvkl_mw`), kept out of metric 1. It tells the operator how much of supply is arriving over cables and, because the sign convention is declared, when GB has flipped to net export.
5. **Six-hour wind ramp volatility (MW).** `STDEV` of metric 2 over a six-hour hopping window. A regime measure rather than an event measure: it says how much reserve the recent past has been demanding, and a step change in it is a weather front arriving.

## 2. The query

```sql
-- Azure Stream Analytics / Fabric Eventstream SQL.
-- Event time is start_time, the member tagged semanticRole "phenomenonTimeStart"
-- and the only datetime in the record. settlement_period is emitted for
-- reference but is never used in arithmetic: the schema states that the count
-- of periods per settlement day is not constant, so differencing or ordering on
-- it is wrong across a clock change.
WITH base AS (
    SELECT
        start_time,
        settlement_period,
        wind_mw,

        -- METRIC 1 - total metered generation output, fuel members only.
        -- Interconnectors are excluded: the schema states they are signed net
        -- flows on cables, not fuels, and may not be summed with generation
        -- without a decision on exports. The decision taken here is to keep
        -- them out entirely and report them separately as metric 4.
        -- ps_mw is included as OUTPUT; this total is not net of pumping demand,
        -- which the schema says is metered elsewhere and is absent from the feed.
        -- Strict '+' is intentional: only settlement_period and start_time are
        -- required, so a member may be absent, and an absent member yields NULL
        -- here rather than a silently understated total. Absence is not zero -
        -- the publisher emits explicit 0.0 (see ocgt_mw, coal_mw, oil_mw).
        ccgt_mw + ocgt_mw + coal_mw + oil_mw + nuclear_mw
            + wind_mw + biomass_mw + npshyd_mw + ps_mw + other_mw
            AS total_metered_generation_mw,

        -- METRIC 4 - net interconnector position. All seven members share the
        -- declared convention "positive for import to GB", so they are additive
        -- with each other even though they are not additive with generation.
        intfr_mw + intifa2_mw + intned_mw + intnem_mw
            + intelec_mw + intnsl_mw + intvkl_mw
            AS net_interconnector_mw

    FROM input TIMESTAMP BY start_time
),

stepped AS (
    SELECT
        start_time,
        settlement_period,
        wind_mw,
        total_metered_generation_mw,
        net_interconnector_mw,

        -- METRIC 3 - wind share of the metered generation output above.
        CASE
            WHEN total_metered_generation_mw > 0
            THEN wind_mw / total_metered_generation_mw
            ELSE NULL
        END AS wind_share_of_metered_generation,

        -- METRIC 2 - half-hour wind ramp. No PARTITION BY: nothing in the
        -- record identifies an individual source (see the note below), so LAG
        -- reaches the previous event of the single stream. The ramp is emitted
        -- only when the previous record's start_time is exactly one declared
        -- support period (PT30M = 1800 s) earlier, so a missed, duplicated or
        -- out-of-order publication produces NULL instead of a fabricated rate.
        CASE
            WHEN DATEDIFF(
                     second,
                     LAG(start_time, 1) OVER (LIMIT DURATION(hour, 2)),
                     start_time) = 1800
            THEN wind_mw - LAG(wind_mw, 1) OVER (LIMIT DURATION(hour, 2))
            ELSE NULL
        END AS wind_ramp_mw_per_period,

        -- validity guard, not a metric: observed spacing against the declared
        -- cadence of PT30M.
        DATEDIFF(
            second,
            LAG(start_time, 1) OVER (LIMIT DURATION(hour, 2)),
            start_time) AS observed_gap_seconds

    FROM base
),

wind_vol AS (
    -- METRIC 5 - HoppingWindow, 6 hours long, hopping every 30 minutes
    -- (expressed in one unit as minute, 360, 30 to stay in the three-argument
    -- same-unit form). At the declared cadence a full window holds 12 ramps;
    -- ramp_samples_6h is emitted as a validity guard so a consumer can reject
    -- the statistic when the feed has gapped.
    SELECT
        System.Timestamp() AS window_end,
        STDEV(wind_ramp_mw_per_period) AS wind_ramp_stdev_6h_mw,
        COUNT(wind_ramp_mw_per_period) AS ramp_samples_6h
    FROM stepped
    GROUP BY HoppingWindow(minute, 360, 30)
)

SELECT
    s.start_time,                          -- carried, not a metric
    s.settlement_period,                   -- carried, not a metric
    s.total_metered_generation_mw,         -- metric 1
    s.wind_ramp_mw_per_period,             -- metric 2
    s.wind_share_of_metered_generation,    -- metric 3
    s.net_interconnector_mw,               -- metric 4
    v.wind_ramp_stdev_6h_mw,               -- metric 5
    s.observed_gap_seconds,                -- guard on metric 2
    v.ramp_samples_6h                      -- guard on metric 5
INTO output
FROM stepped s
-- Attaches the six-hour window ending at this record's own event time. The hop
-- is 30 minutes, so BETWEEN 0 AND 29 selects exactly one window per record.
-- I am not certain a LEFT OUTER JOIN between a per-event step and a windowed
-- step is accepted on every compatibility level; if it is not, run the wind_vol
-- step to its own output sink and join downstream, or drop to an inner JOIN and
-- accept that the first six hours after start produce no rows.
LEFT JOIN wind_vol v
    ON DATEDIFF(minute, s, v) BETWEEN 0 AND 29
```

**Event time.** `TIMESTAMP BY start_time`, and no other member. `start_time` is the only datetime in the record and carries `semanticRole: phenomenonTimeStart`.

**Windows.** One aggregating window: `HoppingWindow(minute, 360, 30)` — a six-hour hopping window advancing every 30 minutes, one hop per declared publication. Metrics 1–4 are per-record and use no window; metric 2 uses `LAG` with `LIMIT DURATION(hour, 2)`, which is a lookback bound and not a window.

**Partitioning.** None, because nothing in the record identifies an individual source. Every member is a whole-system quantity; there is no unit, BMU, zone or publisher identifier. `settlement_period` is tagged `dcterms:identifier`, but it identifies the half-hour inside a settlement day, not a source, and the schema warns against arithmetic on it. The stream is therefore treated as a single source and `LAG` is written without `PARTITION BY`.

## 3. What I did not compute

* **A combined gas total, `ccgt_mw + ocgt_mw`.** The schema states these describe operationally unrelated fleets — CCGT is the bulk fleet dispatched for energy, OCGT runs for minutes at a time as reserve. Summing them names a fleet that does not exist operationally, and it destroys the signal that matters most in `ocgt_mw`, which is that it is non-zero at all.
* **Any net or round-trip position for pumped storage from `ps_mw`.** The schema states the pumping load does not appear as a negative value here and is metered as demand elsewhere, so `ps_mw` is not a net position and no storage balance can be formed from this feed. For the same reason I did not add `ps_mw` to `npshyd_mw` into a "hydro" total: the schema separates them precisely because only one of them is a store.
* **A total supply figure or a demand proxy, generation plus interconnectors.** The schema explicitly says the cable members may not be summed with the generation members without deciding how exports are to be treated, and a demand figure would additionally need station load, distribution-connected generation and pumping demand — none of which are in the feed.
* **A per-settlement-day energy total.** Converting a member to MWh is licensed (a mean over a stated `supportPeriod` of PT30M is `mw * 0.5` MWh), but I cannot delimit a settlement day from this feed: the schema says periods are numbered from 1 at midnight UTC and also that a day may hold 46 or 50 periods. I cannot reconcile those two statements, so I cannot say which records constitute one day, and I did not use a `settlement_period` rollover to 1 as a day boundary either.
* **Carbon intensity, or a low-carbon / renewable share.** That requires emission factors and a classification of `biomass_mw`, `other_mw` and the imported members that the two files do not establish. `other_mw` is defined only as plant whose fuel type is not reported separately, which makes it unclassifiable by construction.
* **Capacity factors, headroom, or availability.** No capacity, unit count or availability appears anywhere in the schema.
* **Per-cable flow reversal flags** (a sign change on `intnem_mw`, `intelec_mw` and the rest between consecutive periods). This is sound and computable, but without capacity or outage data a reversal cannot be told apart from a trip, so the flag would raise alerts an operator cannot act on; metric 4 already carries the aggregate direction. Left out to stay at five.
* **A synthesised period end.** The feed carries no end instant, and I did not manufacture `start_time + 30 minutes` as a second timestamp nor treat any mean as an instantaneous value at a point inside its period.

## 4. Assumptions

* **Assumption: the input carries one system and one publisher.** Nothing identifies a source, so `LAG` and the window are written unpartitioned. If two feeds were ever merged onto the same input, both the ramp and the volatility would be wrong.
* **Assumption: a settlement period is published once and never restated.** The schema says nothing about revisions or corrections. `LAG` and the hopping window assume at most one record per `start_time`; a republished period would be read as a duplicate and, because its `start_time` gap would not be 1800 seconds, would null the ramp rather than corrupt it.
* **Assumption: labelling a value by the start of its support is acceptable.** Event time is `start_time`, so a window whose end is `T` contains the values that *begin* in the preceding six hours and therefore covers phenomenon time out to `T + 30 minutes`. The feed carries no end instant, so there is no alternative anchor; the offset is stated rather than corrected.
* **Assumption: records arrive within the job's late-arrival tolerance and roughly in event-time order,** and the previous period is within the `LIMIT DURATION(hour, 2)` lookback.
* **Assumption: an absent member means "not reported", not zero.** The instance carries explicit `0.0` for `ocgt_mw`, `coal_mw` and `oil_mw`, which suggests absence and zero are distinguishable, so the totals use strict addition and go NULL rather than coalescing to zero. If the publisher in fact omits members it means to be zero, metric 1 and metric 3 will be NULL more often than they should.
* **Assumption: the ten fuel members are mutually disjoint.** The schema states disjointness only for `npshyd_mw` against `ps_mw`. If any other pair overlaps, metric 1 double counts.
* **Assumption: including `ps_mw` in metric 1 is what an operator wants.** It makes the total a gross output total. Anyone wanting a total net of storage cannot get one from this feed.
* **Assumption: the hopping window boundaries coincide with publication instants** (on the hour and half hour), which is what makes `DATEDIFF(minute, s, v) BETWEEN 0 AND 29` select exactly the window ending at the record's own time. If publication is offset from the half hour, the join must be widened and the metric-5 column will lag by one hop.
* **Assumption: a standard deviation over at most twelve ramp samples is informative enough to publish.** It is a small-sample statistic; `ramp_samples_6h` is emitted so a consumer can decide.
* **Assumption about the dialect: `LEFT OUTER JOIN` between a windowed step and a per-event step is accepted,** as flagged in the query comment.


TRANSCRIPT D

# 19 — BMRS Generation Mix: five derived metrics

## 1. The five metrics

1. **`total_metered_generation_mw`** — the sum of the ten fuel-type means
   (`ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw`, `nuclear_mw`, `wind_mw`,
   `biomass_mw`, `npshyd_mw`, `ps_mw`, `other_mw`) for the settlement period.
   The record carries the mix but never the level; an operator needs the level to
   read any of the parts, and every share below divides by it.
2. **`wind_share_of_metered_generation`** — `wind_mw` divided by
   `total_metered_generation_mw`. One dimensionless number for the composition of
   the mix, and the one an operator watches because it is the part of the fleet
   that is not dispatched.
3. **`generation_ramp_mw_per_hour`** — the change in
   `total_metered_generation_mw` since the previous record, divided by the elapsed
   time between the two `start_time` values. The rate the fleet actually moved at,
   which is what sizes the flexibility a system operator must hold.
4. **`net_interconnector_mw`** — the signed sum of the seven cable flows
   (`intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`, `intelec_mw`,
   `intnsl_mw`, `intvkl_mw`), positive when GB is on balance importing. Whether
   the system is drawing on or supplying its neighbours, in one number, kept
   arithmetically apart from generation because these values are signed.
5. **`cadence_departure_flag`** (with `seconds_since_previous_period`) — the
   residual of the observed gap between successive `start_time` values against the
   `PT30M` cadence the schema declares on `start_time`. A silently missing
   half-hour corrupts metrics 1–4 without changing their type; the specification
   says a declared cadence is what "makes an absent value detectable as a gap
   rather than absorbed silently", and this is that flag.

`generation_members_present` and `interconnector_members_present` also appear in
the output. They are counters, not metrics, and are not among the five: only
`settlement_period` and `start_time` are `required`, so any `*_mw` member may be
absent, the sums go `NULL` when one is, and these counters are what make that
`NULL` interpretable.

## 2. The query

```sql
-- Grain: one row per settlement period, the grain of the feed.
-- No PARTITION BY: nothing in the record identifies a source. No member carries
--   semanticRole "featureOfInterest"; the fleet a value belongs to lives only in
--   the member name and its description. `settlement_period` is annotated
--   dcterms:identifier and identifies the period within the settlement day, not
--   a source, so it is not a partition key.
-- No windowed aggregation: see section 3.
WITH
periods AS
(
    -- TIMESTAMP BY start_time: the only member with a temporal semanticRole
    -- ("phenomenonTimeStart"), and the position on which every value member's
    -- supportPeriod (PT30M, anchor "start") is anchored.
    SELECT
        start_time,
        settlement_period,
        wind_mw,

        -- Metric 1. Ten members that share one observedProperty reference
        -- (qudt Power), one unit (MW), one statistic (mean), one
        -- phenomenonTimeRelation (interval) and one supportPeriod
        -- (PT30M, anchor start), so the sum of the means is the mean of the sum
        -- over the same half hour. NULL if any member is absent: nothing here
        -- licenses substituting zero for a value that was not recorded.
        (   ccgt_mw + ocgt_mw + coal_mw + oil_mw + nuclear_mw
          + wind_mw + biomass_mw + npshyd_mw + ps_mw + other_mw
        ) AS total_metered_generation_mw,

        (   CASE WHEN ccgt_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN ocgt_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN coal_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN oil_mw     IS NULL THEN 0 ELSE 1 END
          + CASE WHEN nuclear_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN wind_mw    IS NULL THEN 0 ELSE 1 END
          + CASE WHEN biomass_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN npshyd_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN ps_mw      IS NULL THEN 0 ELSE 1 END
          + CASE WHEN other_mw   IS NULL THEN 0 ELSE 1 END
        ) AS generation_members_present,

        -- Metric 4. Seven signed net flows, every one declared positive for
        -- import to GB, so they add on a common convention. Deliberately not
        -- added to the generation members.
        (   intfr_mw + intifa2_mw + intned_mw + intnem_mw
          + intelec_mw + intnsl_mw + intvkl_mw
        ) AS net_interconnector_mw,

        (   CASE WHEN intfr_mw   IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intifa2_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intned_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intnem_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intelec_mw IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intnsl_mw  IS NULL THEN 0 ELSE 1 END
          + CASE WHEN intvkl_mw  IS NULL THEN 0 ELSE 1 END
        ) AS interconnector_members_present

    FROM input TIMESTAMP BY start_time
),

transitions AS
(
    -- LIMIT DURATION is two hours: four beats of the declared PT30M cadence,
    -- so the previous record is still reachable across a missed beat or three.
    SELECT
        start_time,
        settlement_period,
        wind_mw,
        total_metered_generation_mw,
        generation_members_present,
        net_interconnector_mw,
        interconnector_members_present,
        LAG(start_time, 1)
            OVER (LIMIT DURATION(hour, 2)) AS prev_start_time,
        LAG(total_metered_generation_mw, 1)
            OVER (LIMIT DURATION(hour, 2)) AS prev_total_metered_generation_mw
    FROM periods
),

timed AS
(
    SELECT
        start_time,
        settlement_period,
        wind_mw,
        total_metered_generation_mw,
        generation_members_present,
        net_interconnector_mw,
        interconnector_members_present,
        prev_total_metered_generation_mw,
        DATEDIFF(second, prev_start_time, start_time)
            AS seconds_since_previous_period
    FROM transitions
)

SELECT
    -- carried, for identification only
    start_time,
    settlement_period,

    -- 1
    total_metered_generation_mw,

    -- 2. Share of the metered generation this feed reports. Not a share of GB
    -- generation: wind_mw covers only Balancing-Mechanism-metered units and the
    -- schema states it understates GB wind.
    CASE
        WHEN total_metered_generation_mw > 0
        THEN wind_mw / total_metered_generation_mw
    END AS wind_share_of_metered_generation,

    -- 3. Divided by the elapsed time actually observed, not by an assumed half
    -- hour: cadence is an expectation, not a constraint. Over a longer baseline
    -- this is still a mean rate of change, and the flag below says which.
    CASE
        WHEN seconds_since_previous_period > 0
        THEN (total_metered_generation_mw - prev_total_metered_generation_mw)
             * 3600.0 / seconds_since_previous_period
    END AS generation_ramp_mw_per_hour,

    -- 4
    net_interconnector_mw,

    -- 5. Residual against the declared PT30M cadence. A flag, not a rejection:
    -- a record whose timing departs from a declared cadence is late, not invalid.
    seconds_since_previous_period,
    CASE
        WHEN seconds_since_previous_period IS NULL THEN NULL
        WHEN seconds_since_previous_period = 1800  THEN 0
        ELSE 1
    END AS cadence_departure_flag,

    -- qualifiers on metrics 1 and 4, not metrics
    generation_members_present,
    interconnector_members_present

INTO output
FROM timed
```

## 3. What I did not compute

**Any total combining generation with interconnectors, and any demand or
net-supply figure.** `intfr_mw`, `intifa2_mw`, `intned_mw`, `intnem_mw`,
`intelec_mw`, `intnsl_mw` and `intvkl_mw` are signed, and `intfr_mw` states
outright that it may not be summed with the generation members without first
deciding how exports are treated. Separately, `ps_mw` is not a net position — its
pumping load is metered as demand elsewhere and is absent here — so no quantity
in this record is a supply-side total against which demand could be inferred.

**Carbon intensity, or a low-carbon / fossil split.** That needs an emission
factor per fuel. Neither file states one, and the specification is explicit that a
fact an annotation does not carry must not be repaired from property names,
descriptions, labels or samples. It would have involved `coal_mw`, `oil_mw`,
`ccgt_mw`, `ocgt_mw` and `biomass_mw`, and `biomass_mw` is the member on which
the answer would actually turn.

**A combined gas figure, `ccgt_mw + ocgt_mw`.** Arithmetically unobjectionable
and semantically misleading: the schema says these are operationally unrelated
fleets, bulk energy against minutes-long reserve, and a reader given one number
would treat them as one dispatchable fleet.

**A combined hydro figure, `npshyd_mw + ps_mw`.** The schema says they are
disjoint and says why they are reported apart — only one of them is a store.
Adding them presents released stored energy as natural inflow.

**Energy in MWh, from the MW means and the `PT30M` `supportPeriod`.** The most
tempting omission. The support period is declared, so the interval length is
known; but `statistic: mean` states no weighting, no sample count and no
treatment of missing values, and the specification says a processor MUST NOT
recompute a result from it. Multiplying by half an hour is only correct if the
mean is time-weighted, which nothing here says. One line to add if the publisher
confirms it.

**Anything keyed on `settlement_period`.** No arithmetic across it, no grouping
by it, no use of it as a partition key. It is annotated `dcterms:identifier`, its
description says a settlement day holds 46, 48 or 50 of them so arithmetic across
a clock change is wrong, and it identifies a period rather than a source.

**Cross-record aggregation of any kind: no `TumblingWindow`, `HoppingWindow`,
`SlidingWindow` or `SessionWindow` appears.** A mean of the half-hourly means over
a window, or a `STDEV` of `wind_mw` across one, is the mean or dispersion of the
window only if every period in it is present, and the specification forbids
inferring complete coverage from `phenomenonTimeRelation: interval`. It also
states that no annotation confers permission to aggregate. Such a metric is
computable — `AVG(wind_mw)` with `COUNT(*)` beside it over, say,
`TumblingWindow(hour, 6)`, where twelve is the count the declared `PT30M` cadence
implies for six UTC hours — but it sits at a different grain from metrics 1–5 and
one statement has one output, so I left the output at the grain of the feed.

**Filling absent members with zero.** `required` names only `settlement_period`
and `start_time`, so every `*_mw` member is optional. `COALESCE(ccgt_mw, 0)` and
the like would supply a value where none was recorded, which the specification
prohibits. The sums propagate `NULL` instead and the presence counters expose why.

**Capacity factors, headroom, or margin.** No member carries a capacity,
availability or registered-output figure.

**Per-cable import/export flags.** Computable and sound, but seven flags say less
to an operator than the one net position already in metric 4.

## 4. Assumptions

* **Assumption.** The ten fuel-type members are mutually disjoint and together
  cover what the feed reports as metered generation, so their sum double-counts
  nothing and is a level rather than an arbitrary total. The schema states
  disjointness only for the `npshyd_mw` / `ps_mw` pair, and implies the rest by
  defining `other_mw` as plant "whose fuel type BMRS does not report separately".
  Everything in metrics 1, 2 and 3 rests on this.
* **Assumption.** That the sum is meaningful at all. The member annotations
  establish that the ten values are *commensurable* — one `observedProperty`
  reference, one `unit`, one `statistic`, one `phenomenonTimeRelation`, one
  `supportPeriod` — and the specification says explicitly that a processor must
  not infer permission to aggregate from annotations. The licence to add them
  comes from the prose: the record-level `observedProperty` names a generation
  *mix*, and `other_mw` is defined as its residual category.
* **Assumption.** The input carries a single series. Nothing in the record has
  `semanticRole: featureOfInterest`, so if two publishers or two regions were ever
  multiplexed into one input the query would silently interleave them, and there
  is no member on which to partition to prevent it.
* **Assumption.** The "BM-metered" scope stated explicitly on `wind_mw` and
  `other_mw` applies to all ten fuel members, so that the denominator in metric 2
  is drawn on the same basis as its numerator. If it does not, the share is still
  well defined but is not a share of a coherent population.
* **Assumption.** A two-hour `LIMIT DURATION` is enough lookback. Beyond four
  missed beats of the declared cadence the ramp and the gap flag return `NULL`
  rather than reaching further back.
* **Assumption.** Late arrival and out-of-order tolerance for `start_time` are
  configured on the job, not expressed here. `TIMESTAMP BY` places the event; it
  does not state how long the query waits for a straggler.
* **Assumption.** `total_metered_generation_mw > 0` is the right guard for the
  share. No member declares a `minimum` and all are `double`, so the schema does
  not exclude a zero or negative total; the metric yields `NULL` rather than a
  ratio if one occurs.
* **Assumption.** `LAG(..., 1) OVER (LIMIT DURATION(hour, 2))` is accepted without
  a `PARTITION BY` clause. I believe it is, but I could not check, and if it is not
  the two `LAG` calls need a constant partition key.
* Not an assumption, for the record: `start_time` being UTC, the period being half
  an hour, the interconnector sign convention, and the `PT30M` cadence are all
  stated in the schema.
