You are a supervisor. You grade four transcripts against a fixed list of claims.

You are not being asked whether a transcript is good, insightful, or well
written. You are asked, for each claim and each transcript, whether the
transcript got that specific matter right, got it wrong, declined to decide it,
or never touched it. Nothing else you think about the transcripts is wanted.

## Your stance

You are an adversarial grader. The transcripts were written by a different model
from a different vendor, and you are the hostile check on them. Assume each is
trying to appear more knowledgeable than it is, and grade so that appearance
earns nothing.

Credit is earned, never assumed. The default verdict is `unaddressed`, and a
transcript moves off it only by saying something specific enough that you can
point at the words. You are not rewarded for being fair to a transcript, and a
grader who credits an answer with something it did not quite say has failed at
this task. Being wrong in the direction of severity costs the evaluation far
less than being wrong in the direction of generosity, so where you genuinely
cannot decide, withhold the credit.

This severity applies identically to all four transcripts. You are hostile to
unearned credit, not to any particular transcript, and you must not go looking
for a transcript to punish.

You will be given:

* **CLAIMS** — numbered propositions. Each is true of the data the transcripts
  describe. Most carry a `wrong reading`: the specific error the claim exists to
  rule out.
* **TRANSCRIPT A**, **TRANSCRIPT B**, **TRANSCRIPT C** and **TRANSCRIPT D** —
  four independent readings of that data, produced under conditions you are not
  told. They are not in any meaningful order. Do not speculate about the
  conditions while grading.

For each claim, and separately for each of the four transcripts, choose exactly
one verdict. Every claim therefore receives four verdicts.

* `correct` — the transcript asserts the claim, or asserts something that
  entails it, as a statement it is standing behind.
* `incorrect` — the transcript asserts the wrong reading, or asserts anything
  else incompatible with the claim.
* `declined` — the transcript raises the matter and explicitly does not settle
  it: it says the files do not determine it, or it marks its answer as an
  assumption or a guess. **A transcript that states the correct answer but marks
  it as a guess or an assumption is `declined`, not `correct`.** Knowing that you
  do not know is a distinct outcome from knowing.
* `unaddressed` — the transcript never engages the matter at all.

Rules you must follow.

1. Judge only what is written. Do not credit a transcript for something you
   believe it meant, or for something a competent reader would obviously know.
2. For `correct` and `incorrect` you MUST supply `quote`: a verbatim span from
   that transcript, copied exactly, that carries the verdict. If you cannot find
   one, the verdict is `unaddressed`.
3. **The quote must carry the claim standing alone.** Read it with the rest of
   the transcript covered up. If someone who saw only those words would not
   learn the claim from them, the verdict is not `correct`, however clearly the
   surrounding paragraphs gesture at it. Naming the member, using the right
   technical term, or discussing the general area is not asserting the
   proposition.
4. **Look for the wrong reading before you look for the right one.** Search the
   transcript for the error the claim exists to rule out, and settle that
   question first. Only if the wrong reading is absent may you consider
   `correct`.
5. **A transcript that both asserts the claim and commits the wrong reading is
   `incorrect`.** Do not let a correct sentence elsewhere rescue it. Reciting a
   rule and then breaking it is worse than not knowing the rule, not better.
6. Do not round up. If a transcript gets part of a claim right and part of it
   wrong, and the wrong part is what the claim is about, that is `incorrect`. If
   the wrong part is incidental, it is `unaddressed`. It is not `correct`.
7. Do not use your own knowledge of the subject matter to decide a claim. The
   claim is the ground truth. If a transcript contradicts a claim, that is
   `incorrect` even if you personally believe the transcript.
8. Confidence is not evidence. Length is not evidence. A fluent, assured,
   well-organised transcript gets no benefit of the doubt over a terse one.
9. Grade the four transcripts independently. Do not let one inform another, and
   do not compare them. A matter that transcript C settles is still
   `unaddressed` in transcript A if transcript A never raises it.
10. Silence is not an error. A transcript that never touches a claim is
    `unaddressed`, and `unaddressed` is not a mark against it. Severity means
    withholding credit, not inventing violations.

Answer with JSON only, no prose before or after, in exactly this form:

```json
{
  "verdicts": [
    {"claim": 1, "transcript": "A", "verdict": "correct", "quote": "..."},
    {"claim": 1, "transcript": "B", "verdict": "unaddressed"},
    {"claim": 1, "transcript": "C", "verdict": "declined"},
    {"claim": 1, "transcript": "D", "verdict": "incorrect", "quote": "..."}
  ],
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

# 1. What this feed is

Each record is a cross-sectional snapshot of electricity supply on a single power system, broken down by production category and by cross-border link, tagged to a numbered half-hourly-style trading interval and to an instant. One record = one interval; the members within it are the simultaneous contributions of gas-fired plant (combined-cycle and open-cycle), coal, oil, nuclear, wind, biomass, non-pumped hydro, pumped storage, an unspecified residual, and seven named external interconnectors.

The category names and the interconnector names are strongly suggestive of the Great Britain transmission system, but nothing in the two files names a country, an operator, a market, or a source system. Treat the geography as an inference, not a given.

Two things the records are *not*: they are not energy, and they are not demand. The naming convention says megawatts, i.e. a rate; and there is no member for load, price, or emissions. Any statement about MWh, cost, or carbon requires a duration or a factor that this feed does not carry.

The single most consequential absence: **there is no solar member**. Whether solar is folded into the residual, sits outside the measurement boundary (e.g. because it is connected below the transmission system and never metered here), or simply is not published, is not determined. An analyst who sums these members and calls the result "total generation" will be wrong by whatever that boundary excludes, and will be wrong by a different amount at midday than at midnight.

# 2. Analytics

**Mix composition and share over time.** Every record is a complete simultaneous cross-section in one common unit, so within-record shares are computable directly, and the timestamp lets those shares be tracked as a series. Caveat carried from §3: shares are only well-defined once you have decided how to treat negative values and a possibly incomplete denominator.

**Ramp and volatility analysis.** Consecutive records differenced member-by-member give the change in output per interval — the raw material for wind ramp distributions, gas-plant following behaviour, and reserve sizing questions. This works because the member set is stable across records and the interval spacing is recoverable from the timestamps themselves.

**Displacement / correlation studies.** Wind against CCGT, or wind against net imports, over many records shows which technology absorbs variability. Supported because all categories are observed at the same instant, so contemporaneous correlation is not an alignment artefact.

**Net interconnector position.** The interconnector members are signed (the example carries two negatives), so import/export flipping, per-link utilisation, and aggregate net exchange are all directly derivable per interval.

**Storage cycling.** Pumped storage is carried as its own signed member, so charge/discharge alternation and cycle counts are observable. State of charge and round-trip efficiency are not.

**Diurnal and seasonal profiling.** The absolute instant on every record supports grouping by hour, day, month, or by the interval ordinal, and hence typical-day and duck-curve style profiles.

**Displacement-of-coal / retirement tracking.** Zero-run detection on coal and oil is trivially supported; the example shows explicit zeros, so a genuine zero is representable and distinguishable from absence.

**Data-quality surveillance.** Because two independent time indices are present, records can be cross-checked against each other, and gaps, duplicates, and off-grid timestamps can be detected. This is worth running *before* any of the above.

**Energy accounting** is supported only conditionally — see §3 and §4. **Emissions, prices, curtailment, capacity/availability, per-plant detail, and demand** are not supported at all from this feed alone; each needs data that is not here.

# 3. Combination rules

**The interval ordinal.** This is a label, not a measurement. It may be compared for ordering and differenced *only within a single day-frame*, and even then the difference is an interval count, not a duration, unless intervals are equal-length. It must never be summed, averaged, or used as a join key on its own: it is not unique across days, and two records with the same ordinal from different days are different things. Do not treat it as a quantity of any kind.

**The instant.** Ordering and differencing are valid; the difference is elapsed time and is the empirical way to establish interval length. Summing instants is meaningless. This is the only member suitable as a primary key — subject to the revision problem in §5. Records whose timestamps carry different UTC offsets must be normalised to a single reference before being ordered or differenced; the example carries an explicit `Z`, but the files do not establish that every record will.

**All power members (production categories, storage, interconnectors).** All are nominally the same unit, so:

- *Within one record*: they may be summed and differenced freely. That is the one unambiguously safe aggregation here.
- *Across records*: they may be **differenced** (ramp), and **averaged** to obtain mean power — but averaging is only an unweighted mean if every interval in the window has the same duration. If interval length varies (which the ordinal's upper bound of 50 implies it can), the average must be time-weighted or it silently over-weights short intervals.
- *Across records*: they may **not** simply be summed. Adding rates across time produces a number with no physical meaning. Energy requires multiplying each value by its own interval duration first, and that duration is not carried in the data.
- *Across records*: comparison is valid, with the caveat that a value from a long clock-change interval is not comparable like-for-like with a value from a normal interval if the value is an interval average rather than an instantaneous reading.

**Signed members must not be pooled with unsigned ones for share calculations.** Interconnectors and pumped storage may be negative — the example proves it for two interconnectors. A "percent of the mix" computed over a denominator that includes negative terms produces shares above 100% for some categories and negative shares for others. Decide explicitly: either exclude negative terms from the denominator, or split the record into a gross-supply side and a net-export side, and say which you did. Do not let a spreadsheet decide it for you.

**The residual category must not be treated as disjoint from the named ones.** Nothing establishes that the categories partition anything, and nothing establishes that the residual excludes what the named members already count. Adding it into a total risks double-counting; excluding it risks under-counting. There is no published total in the record against which either choice can be checked.

**Absence is not zero.** Only the interval ordinal and the instant are required; every power member may be missing. The example carries explicit `0.0` values, which proves that zero is expressible — so a missing member means "not stated", not "none". Any sum or mean that silently coerces missing to zero will understate totals and shift shares, without raising an error. This is the failure mode most likely to occur and least likely to be noticed.

**Validation will not save you.** Range constraints are applied only to the interval ordinal. The power members are unbounded, so implausible or wrongly-signed values pass schema validation cleanly. Plausibility checking is the analyst's job.

# 4. Time

The **instant** establishes the time axis. It is an absolute point, and in the example it is expressed with an explicit UTC designator, so it maps to civil time in any zone by applying that zone's offset rules — rules that are not in these files. The interval ordinal is a secondary index: it locates the record within some day-frame, but the files never define where that day begins.

The relationship between the two is under-determined, and the single example makes the problem visible rather than resolving it. **Guess:** intervals are thirty minutes and numbered from 1 at the start of the day. Under that guess, ordinal 12 begins 5h30m after the day boundary, and the example's instant of 05:30 UTC places the day boundary exactly at 00:00 UTC. But a day anchored to UTC always contains exactly 48 half-hours, which cannot produce the ordinal's permitted maximum of 50. A maximum of 50 only makes sense for a day-frame anchored to a local clock that shifts twice a year — and under a local anchor with a summer offset of one hour, this July record's ordinal 12 should begin at 04:30 UTC, not 05:30.

So one of these is true, and the files do not say which: the intervals are not half-hourly; or the numbering does not start where I assumed; or the day-frame is UTC-anchored and the bound of 50 is merely permissive; or the timestamp in this example is a local wall-clock time incorrectly labelled as UTC. That last possibility is the dangerous one, because it would silently shift the entire series by an offset that changes twice a year. **I am declining to decide this.** Resolve it empirically before analysis: pull the records spanning a clock-change day, count the intervals in it, and check whether the timestamp spacing stays constant across the transition. Until then, do not join this feed to anything else on wall-clock time.

Positions on the axis are interval *starts*, per the member's name. Each value therefore describes the interval that follows its stamp, not the one that precedes it. Whether the value is the mean over that interval or an instantaneous reading at its start is not determined, and this matters: only the mean interpretation makes value × duration a correct energy figure.

# 5. Ambiguities

**Units.** That these are megawatts rests entirely on a naming convention. Nothing declares a unit, a scale factor, or a magnitude. *Not determined* — verify against the publisher before reporting absolute numbers.

**Interval duration.** Not carried in the data. Required for every energy figure. *Guess:* thirty minutes, based on the ordinal's bound. Recoverable empirically from timestamp spacing; do that.

**Day-frame anchoring and the 50-interval maximum.** *Declining to decide* — see §4.

**Mean or instantaneous.** Whether each power value is the average over its interval or a spot reading at the start is *not determined*. Affects energy totals and affects whether ramp differences are true ramps or sampling artefacts.

**Measurement boundary.** Whether these figures cover only transmission-connected plant, or all plant including distribution-connected and behind-the-meter generation, is *not determined*. The absence of a solar member is evidence that the boundary is narrower than "everything", but the files do not say where it sits.

**What the residual contains,** and whether it overlaps the named categories: *not determined*.

**Sign convention.** *Guess:* positive means import (for links) and generating/discharging (for storage); negative means export and pumping. The negatives in the example establish that the members are signed, but not which direction each sign means. Getting this backwards inverts every net-exchange conclusion, so confirm it.

**Data vintage and revision.** There is no version, revision, publication-time, or provenance member. Consequently an initial estimate and a later restatement of the same interval are *indistinguishable* — same ordinal, same instant, different numbers, no tiebreak. If this feed is ever revised, deduplication by timestamp will keep whichever record happened to arrive last in your pipeline, and back-tests will not be reproducible. *Not determined* whether revisions occur; if they do, you need ingest-time metadata that this feed does not provide. Capture your own receipt timestamp at ingest.

**Whether the figures are metered, estimated, or forecast.** *Not determined.* A forecast feed and a settled-metering feed have identical shape here.

**Numeric resolution.** Every value in the example is integral despite a floating-point declaration. Whether the source publishes sub-MW resolution is *not determined*; do not report more precision than you can justify.

**Completeness of the category list.** Whether these are all the categories that will ever appear, or whether new ones (a solar member, a new interconnector) may be added later, is *not determined*. Since the record shape forbids unrecognised members, a new category would require a schema change — so pipelines built on this shape will reject, rather than ignore, an extended future record. Plan for that.


TRANSCRIPT B

# 1. What this feed is

Each record is a half-hourly summary of what was producing electricity on the GB
transmission system, and what was flowing over the cables that connect it to
neighbouring systems, during one settlement period. Every quantity in a record
is a **mean power in megawatts over the same half hour** — not an instantaneous
reading, not an energy total. The half hour is fixed by one UTC instant carried
in the record and runs forward from it, half-open.

Two structural facts dominate everything an analyst does with it. First, the
plant members report **gross output of the metered fleet**, while the
interconnector members report **signed net flow on a specific cable**, positive
into GB. These are different kinds of number wearing the same unit. Second, the
feed is **not a balance**: pumped-storage pumping load is absent (it is metered
as demand elsewhere), wind connected below transmission is absent, and the
record's own text says the wind figure therefore understates GB wind. Nothing in
the two files establishes that the listed categories exhaust GB generation.

The record names a system-level observable property, but it carries no member
identifying the feature observed and no member identifying the measuring or
estimating procedure. Both are therefore undeclared, and omission never implies
that they are constant or acceptable.

# 2. Analytics

**Fuel-mix composition and its shape over time.** Every value in a record covers
the *identical* half-open interval — same length, same anchor, same anchoring
instant — so cross-member arithmetic within a record is exact rather than
approximate. Shares, ratios, and stacked mixes are well-founded provided the
denominator is chosen deliberately (see §3).

**Ramp rates and volatility.** Consecutive records carry the same statistic over
equal-length adjacent windows, so differencing one member across records yields
a legitimate change-per-half-hour. This is the natural way to characterise wind
variability, gas following, and nuclear stability.

**Import dependence and per-cable behaviour.** Each interconnector is reported
separately and signed, so flow direction, per-cable duty cycle, simultaneous
import and export, and correlation between cables are all directly supported.
The example record shows five cables importing and two exporting at the same
instant — which is exactly why an unsigned aggregate would be wrong.

**Energy volumes (MWh).** A mean power over a known half hour converts to energy
by multiplying by 0.5 h. Structurally supported, but it rests on an assumption
the annotations decline to make (see §5).

**Displacement and substitution analysis.** Because gas, coal, biomass, nuclear
and wind are separated, and interconnectors are separated from them, questions of
the form "what moves when wind moves" are answerable within a record set.

**Coverage and clock-change auditing.** The declared half-hourly cadence is an
*expectation about the publisher*, not a guarantee and not a constraint on the
data; a missing half hour is late, not malformed. Any downstream aggregate must
therefore be preceded by a coverage check built from the time instants
themselves, including the short and long days.

**Peaks — with a caveat.** Maxima and minima across records are comparable, but
the maximum of a half-hour mean is not the instantaneous peak, and the
annotations explicitly do not permit recovering the underlying sample set.

**What the feed does not support on its own:** emissions or carbon intensity
(requires external per-fuel factors), demand or system balance (the load side is
absent), and joins to other settlement-keyed data (see §5, the missing
settlement date).

# 3. Combination rules

**Settlement period number.** It is an identifier, not a measure. It may be
tested for equality and used as a key. It must not be differenced, summed, or
averaged, and period *n* on one day is not the same clock position as period *n*
on another, because the number of periods in a day is not constant. Treating it
as an offset is wrong at exactly the two days a year when it matters most.

**Start instant.** Instants may be ordered and compared, and two of them may be
differenced to give a duration. They must not be summed. They are the only sound
basis for placing a record on a time axis.

**The ten plant members, among themselves, within one record.** Freely summable
and averageable. All carry the same unit, the same summary function, and the same
support interval anchored on the same position, and the mean of a sum over
identical windows is the sum of the means. This is the one aggregation the files
fully licence.

**The ten plant members, across records.** A given member may be compared and
differenced between records without qualification. Averaging across records is
valid as an unweighted mean only because every record's window is the same
length; it is a mean *of the periods present*, and the declared cadence does not
establish that every period is present. Summing a member across records produces
nothing meaningful in MW — convert to energy first, then sum.

**Pumped storage.** Summable with the other plant members as output, but it is
not a net position: the pumping load is not represented here as a negative value.
Any attempt to close an energy balance, compute net storage contribution, or
infer round-trip behaviour from this feed will be wrong by the whole of the
pumping load.

**Non-pumped hydro and pumped storage.** Disjoint, so summing them double-counts
nothing. But the sum conflates a primary source with a store, which is precisely
the distinction the two members exist to preserve.

**CCGT and OCGT.** Arithmetically summable as gas-fired output. They must not be
treated as one dispatchable fleet: they are operationally unrelated, one being
bulk energy plant and the other short-duration reserve, so a combined series
answers no dispatch question that either series answers separately.

**Wind.** Comparable with itself over time and usable for shape and variability.
It must not be used as a level for GB wind generation, nor as the numerator of a
GB wind-share figure, because generation below transmission is excluded.

**The seven interconnector members, among themselves.** Summable to a net import
position, and the two French cables may be summed to a total French flow, since
they share unit and sign convention. Comparing capacities or utilisation between
cables requires ratings the files do not carry.

**Interconnectors with plant members.** Do **not** sum them without an explicit
decision about exports. The values are signed: a negative one is power leaving
GB, and adding it to gross production yields neither total generation nor total
supply. If a "total" is wanted, state whether exports are netted, clipped at
zero, or excluded — the files do not decide it, and the three choices give three
different numbers. In the example record, gross plant output is 22 871 MW and net
interconnector flow is +5 588 MW, but that +5 588 is itself the residue of
+6 184 in and −596 out.

**Across this feed and any other.** Every value member declares the same generic
observable property — a quantity kind of *power*. Equal quantity-kind
classification does not establish that two quantities are the same observable
property, and here it demonstrably does not: gas-turbine output and a Norwegian
cable flow carry the identical declaration. A pipeline that groups or joins on
observed property will silently pool them. The distinguishing facts live in the
per-member prose, not in a resolvable identifier. By the same argument, a value
here must not be combined with a megawatt value from another feed on the strength
of matching unit and quantity kind alone.

# 4. Time

The time axis is established by the **start instant**, which is declared as the
opening boundary of the phenomenon-time period. It is a plain UTC date-time with
standard semantics — no alternative temporal reference regime is declared — so a
position on this axis *is* a civil-time instant and needs no conversion. The
example carries an explicit `Z`.

The record carries no closing boundary, and none is needed: each value member
states its own period length of thirty minutes, anchored at the start. The
interval a value characterises is therefore `[start, start + 30 min)`, half-open,
so the instant that closes one period opens the next and no half hour is counted
twice.

The declared half-hourly cadence is a separate statement from that length. It
describes what the publisher is expected to do next; it does not bound the period
any value applies to, does not assert that a successor record exists, does not
assert ordered arrival, and does not make an off-cadence stream invalid. That the
two happen to be numerically equal here is a fact about this feed, not an
identity between the two ideas.

The settlement period number does **not** establish the time axis. It is an
identifier that does not map to a fixed clock time across the year.

# 5. Ambiguities

**The settlement-day rule contradicts itself.** The record states both that
periods are numbered from 1 at midnight UTC *and* that a day has 46 or 50 periods
on clock-change days. Both cannot hold: a day bounded at midnight UTC always
contains 48 half hours. **I decline to decide which is correct.** The consequence
is concrete: you cannot reconstruct the start instant from a date and a period
number, or vice versa, using these two files. Use the start instant and treat the
period number as an opaque key.

**No settlement date is carried.** Settlement data is conventionally keyed by
date *and* period; only the period is here. Deriving the date from the start
instant requires the day-boundary rule that is contradictory above, so joins to
period-keyed data are not safely constructible from these files. **Declining to
resolve.**

**What the mean averages.** The annotation names the function and deliberately
states nothing about weighting, sample count, window alignment, or treatment of
missing data, and forbids recomputation. Multiplying by half an hour to get MWh
implicitly assumes a time-weighted mean over the full, gap-free window. **That is
an assumption, and I mark it as one.** It is the assumption most analyses of this
feed will make and the one most likely to be silently wrong during partial
outages.

**Absent members.** Only the period number and the start instant are required;
every quantity is optional. Whether an absent member means zero, unknown, or not
applicable is **not determined**, and omission carries no implication of an
acceptable or defaulted value. The example distinguishes an explicit `0.0` from
absence, which is suggestive but not decisive.

**Provisional versus final.** There is no publication time, no status, and no
quality qualifier. Nothing lets a consumer tell a first publication from a
restatement, or detect that a value was later revised. **Not determined.** I am
not guessing whether revision occurs.

**Procedure.** No observing procedure is identified, so it is not established
that the same metering or estimation method produced values in two different
records. Comparability across records is therefore assumed rather than
demonstrated. **Marked as an assumption**; I have no basis in the files to doubt
it, and none to assert it.

**Feature of interest.** No member identifies the system observed; only the
record's prose names it. That every record concerns the same system is a
**guess** — a well-founded one, but a guess, and it is not machine-checkable.

**Sign range of plant members.** The interconnector members are stated to be
signed; the plant members carry no lower bound and no statement that they are
non-negative. Whether a negative plant value can occur is **not determined**.

**Exhaustiveness.** Wind is stated to be incomplete and the residual category is
stated to cover only metered plant whose fuel is not separately reported. The
files do not say that the listed categories cover all GB generation, and the
record shape is closed, so a new cable or fuel category cannot appear without a
schema change. Any figure presented as a national total is **not supported**.

**The record-level observable property.** Its identifier points at a catalogue
that cannot be resolved from here. That is an indeterminate binding, not an
incorrect one, and it must not be repaired from member names, descriptions, or
the sample. **Declining to substitute a meaning for it.**


TRANSCRIPT C

## 1. What this feed is

Each record is a half-hourly snapshot of how the GB transmission system was being supplied during one settlement period: the mean power output of each metered generation fleet, broken down by fuel or technology, plus the mean net power flowing on each of seven interconnectors to neighbouring systems. It is an *outturn* summary — what actually happened over a closed half-hour — not a forecast, a schedule, or an instantaneous reading. Everything is a mean over the same half-hour window, expressed in megawatts, so a record is a power picture, not an energy total.

Two scope limits matter more than anything else about this feed. First, its population is plant metered in the Balancing Mechanism. Wind connected to distribution networks is simply not in it, so the wind figure is a floor on GB wind, not a measure of it. Second, the interconnector members are not fuels. They are cables carrying signed net flow, and a negative value is GB exporting — which is a load on the GB system, not negative generation.

## 2. Analytics this stream supports

**Energy accounting.** Because each value is an interval mean over a support of known, fixed length, energy for a period is the value times half an hour, and periods can be accumulated into daily, monthly or annual MWh by fuel. This is the single strongest thing the feed enables, and it is only sound because the statistic and the support length are both pinned down; a stream of instantaneous readings would not permit it.

**Fuel-mix composition and shares over time.** All generation members share a unit, a statistic, a support length and an interval, so they are on a common footing within a record and their shares are meaningful — once you have chosen a denominator, which is a modelling decision the data does not make for you (see §3).

**Ramping and flexibility analysis.** Differences between consecutive records give MW change per half hour per fleet. This is well defined because successive records are the same statistic over adjacent, equal, non-overlapping windows.

**Dispatch-regime classification.** Nuclear held near-flat, CCGT following net demand, and OCGT sitting at zero for long stretches are distinguishable behaviours, and OCGT moving off zero is itself a signal — that fleet exists to run for minutes as reserve. A separate CCGT and OCGT breakdown is what makes reserve activation visible at all.

**Wind variability, for balancing purposes.** Volatility, persistence, and low-wind episode length are all computable — but as properties of *transmission-metered* wind, which is the population that actually matters for balancing actions, not as properties of the national wind resource.

**Interconnector position and reversal analysis.** Net import, per-cable utilisation, direction flips, and coincidence of import surges with low wind are all supported, because every cable carries the same sign convention and the same support.

**Diurnal and seasonal profiling** — provided the time axis is handled as in §4, not via period numbers.

## 3. Combination rules

**Within one record**

- The ten generation members may be summed. They share unit, interval, support and statistic. Note that only one disjointness claim is actually established — non-pumped hydro and pumped storage are stated to be separate populations. That the remaining fleets do not overlap is a reasonable reading of the fuel labels but is an *assumption*, not something the data guarantees; the one explicit warning about category placement is that units converted from coal are counted as biomass, not coal.
- The seven interconnector members may be summed with each other. They share a sign convention (positive = import to GB), so the sum is a well-defined net import position and its sign is meaningful.
- Interconnectors must **not** be silently added to the generation total. Doing so treats an export as negative generation, which it is not: an export is a withdrawal from the GB system. Any "total supply" figure requires an explicit decision — count imports only, count net flow, or exclude cables — and that decision changes the answer whenever any cable is exporting. In the sample record two cables are exporting while five are importing, so this is not a hypothetical.
- CCGT and OCGT must not be added together and then reasoned about as one gas fleet for anything dispatch-related. Arithmetically the sum is fine; interpretively it merges bulk energy plant with short-run reserve plant, and the resulting series answers no question anyone is asking.
- Pumped storage output must not be treated as a net storage position. Pumping load is absent from this record entirely — it is metered as demand elsewhere — so charge/discharge balance, round-trip efficiency, and state of energy cannot be derived here at any level of aggregation.
- Absent members must not be read as zero. Only the period number and the start instant are guaranteed present; every measured value is optional. The sample record shows that a genuine zero is transmitted as `0.0`, so absence and zero are distinguishable in principle — but what absence *means* is not established (see §5). Coercing missing to zero silently biases every sum, share and mean downward.

**Across records**

- Any single quantity may be compared, differenced and averaged across records: same unit, same statistic, same support length, adjacent non-overlapping intervals.
- An unweighted mean of N consecutive records equals the time-weighted mean power over that span **only if** the span is contiguous and complete. Every gap breaks that equivalence, and the feed carries no completeness guarantee — the declared half-hourly cadence states what the publisher intends to emit next, not that it did.
- Records must be aligned on the start instant, not the period number.
- The period number must never be summed, averaged, differenced, or used to compute elapsed time. It is an identifier, it restarts each settlement day, and the number of periods per day is not constant — 48 normally, 46 and 50 at the two clock changes. Differencing period numbers across a day boundary or a clock change yields a wrong duration.
- Do not compare the wind figure against any externally sourced GB wind total, or against a capacity base that includes distribution-connected wind. Different populations; the ratio is not a capacity factor.

## 4. Time

The start instant is the time axis. It is the beginning of the interval each value describes, given as a UTC instant, and every value in the record applies to the half-open half-hour that begins there — start inclusive, start-plus-thirty-minutes exclusive. Successive records therefore tile time without overlap and without gap, when complete. The record carries no end instant; the interval length comes from each value's own declared support, not from the publication cadence, and the two must not be conflated — the cadence says when the next record is due, and would still say that if the values had a different support.

Positions on this axis are absolute UTC instants, so they are unambiguous on their own and are the correct join key and sort key. Civil time is a derived view: to bucket by local day, label by local hour, or produce a daily profile you must convert to Europe/London yourself, and the offset changes twice a year. That conversion is exactly where the variable settlement-day length shows up — a "day" of 46 or 50 periods is a local-time day, and resampling code that assumes 48 half-hours per day will be wrong twice a year and silently correct the rest of the time.

The record does not carry a settlement date. The period number alone therefore does not identify a settlement day and is not a key; the start instant is.

## 5. Ambiguities

- **The period-numbering statement is internally inconsistent.** Periods are said to be numbered from 1 at midnight UTC, yet the count per day is said to vary with the clock change. Fixed half-hours counted from a fixed UTC midnight would always give 48. One of the two statements is loose. I am **declining to decide** which; the operative instruction — that the period number does not map to a fixed clock time and must not be used for arithmetic — is consistent either way, and is what should be implemented.
- **What an absent value member means** — zero, not applicable, not yet available, or withheld — is **not determined**. This is the most consequential open point for anyone writing a loader.
- **Whether the generation categories are exhaustive.** There is an "other" bucket for fuel types not reported separately, but whether it makes the breakdown complete for all transmission-metered plant, and whether its composition is stable over time, is **not determined**. Treating "other" as a fixed category across years is a **guess**, and one I would not make.
- **Solar does not appear.** Whether it falls inside "other", or is outside the feed's population entirely, is **not determined**. Do not present a mix breakdown from this feed as covering all GB supply without settling this.
- **Sign range of the generation members.** Only the interconnectors are stated to be signed. Whether generation values can be negative (station load, metering artefacts) is **not determined**; the sample record is non-negative throughout, which establishes nothing about the general case.
- **The basis of the mean** — time-weighted over the whole half-hour versus an average of discrete samples — is not stated. I am **assuming** time-weighted, because that is what makes the multiply-by-half-an-hour energy conversion exact. If it is a sample mean over sparse samples, energy totals inherit a sampling error of unknown size. Marked as an assumption.
- **No revision, publication-time, or version member exists.** If a period is ever restated, two records for the same instant cannot be ordered or distinguished. Whether restatement happens is **not determined**; that the data model cannot express it is certain.
- **No data-quality, estimation or completeness flags.** Estimated and metered values, if both occur, are indistinguishable.
- **The member set is closed.** No unlisted member may appear, so a newly commissioned interconnector cannot enter this feed without a schema change. Whether that means such flows would be absent, folded into an existing member, or land in "other" is **not determined** — and any of those would distort a net-import series computed from historical code.
- **Nothing external is dereferenceable.** The schema's own identifier and its record-level observable-property reference point at placeholder hosts, so none of the above can be settled by following a link. They have to be settled with the publisher.


TRANSCRIPT D

# 1. What this feed is

Each record is one half-hour slice of the British transmission system's generation picture: for a single GB settlement period it gives the average electrical power, in megawatts, delivered by each metered fuel category, plus the average net power flowing over each of the cross-border cables into or out of GB. Records are power, not energy, and every figure is an average over the half hour rather than an instantaneous reading — so a record cannot tell you anything about what happened inside its own thirty minutes.

The population is not "GB generation". It is generation that is metered in the Balancing Mechanism. Plant connected to distribution networks is outside that boundary. This is stated for wind but the boundary is a property of the metering arrangement, not of wind, so it should be assumed to apply to every fuel member: the record is a view of the transmission-metered fleet, and it systematically undercounts anything embedded. There is no member for solar at all, and no total, no demand figure, and no price.

# 2. Analytics

**Energy accounting.** Every value is a mean over a fixed half hour, so multiplying by 0.5 h converts any member to MWh for that period, and those MWh values are additive across periods and across members. This is the foundation for every volumetric question — daily fuel volumes, monthly totals, annual mix.

**Fuel mix and share of generation.** The fuel members partition the metered fleet by fuel type, and `other_mw` is explicitly the residue of that partition, so summing them gives a closed total against which shares can be taken. The share is a share of transmission-metered generation and must be labelled as such; it is not a share of GB electricity.

**Ramping and variability.** Successive records on a common time axis with an identical support length make first differences meaningful: MW per half hour of ramp for any member. Wind variability, CCGT following, and the correlation between them are all directly supported, because the periods are equal-length and so the differences are comparable to each other without reweighting.

**Residual load proxy.** Total metered generation minus wind (and minus nuclear, if the question is about must-run) gives what dispatchable plant had to cover. The files support the arithmetic; they do not support calling it demand, since no demand member exists.

**Net interconnector position.** All the interconnector members share one sign convention — positive is import to GB — so they may be summed into a single net import figure. Movement of that figure over time, and its relationship to CCGT and wind, is well supported.

**Displacement and event detection.** Zero and near-zero runs in `coal_mw` and `oil_mw` are directly readable, so dating the last coal hour, or counting oil-running periods, is straightforward. `ocgt_mw` becoming non-zero is a scarcity signal in its own right, because those units are described as reserve plant that runs for minutes.

**Diurnal and seasonal profiles.** Supported, but the grouping key must be derived from the UTC instant, not from the period number (see §4).

**Not supported by these files:** carbon intensity, emissions, capacity factors, plant availability, prices, curtailment, and anything about the mix inside a half hour. Each of those needs external data — emissions factors, installed capacities, market data — that is nowhere in the record.

# 3. Combination rules

**Across records, same member.** All the MW members may be compared, differenced and averaged freely across records. The reason is that every value is a mean over a support of identical length, so no weighting is required: the arithmetic mean of N period means is the true mean power over those N periods, and a difference between two of them is a genuine change in mean power.

**Summing a member across records is wrong as stated.** Adding MW to MW across periods yields a quantity with no physical meaning. Convert to energy first — multiply each value by 0.5 h — and then sum. This is the single most common error available with this feed.

**Across members, within one record — fuels.** `ccgt_mw`, `ocgt_mw`, `coal_mw`, `oil_mw`, `nuclear_mw`, `wind_mw`, `biomass_mw`, `npshyd_mw`, `ps_mw` and `other_mw` are disjoint categories of the same metered fleet, measured the same way, so they may be summed into a metered-generation total. `npshyd_mw` and `ps_mw` are stated to be disjoint, so summing them does not double-count.

**`ps_mw` needs a decision before it goes into a total.** It is gross generation from pumped storage, not a net position; the pumping load is not carried here as a negative and lives in the demand side of the settlement data, which this feed does not contain. So a total that includes `ps_mw` counts energy that was drawn from the same system earlier. That is correct for "what was supplied in this half hour" and wrong for "what was produced from primary energy in this half hour". Pick one and say which.

**Interconnectors must not be added to a fuel total unlabelled.** They are signed net flows on cables, not fuel output, and they go negative when GB exports. Adding them to a generation sum silently produces a supply-to-GB figure in which an export is treated as negative generation. That may be what you want, but it must be a stated choice, not a side effect. If you want generation, exclude them. If you want supply, include them and rename the result.

**Interconnectors may be summed with each other.** They are separate physical cables with a common sign convention, so their sum is a well-defined net GB import. Do not merge `intfr_mw` and `intifa2_mw` on the grounds that both go to France — they are distinct cables with distinct capacities and are reported separately; keep them separate unless you specifically want the France corridor total, in which case sum them and say so.

**`ccgt_mw` and `ocgt_mw` must not be pooled into "gas" for operational analysis.** They are the same fuel but operationally unrelated fleets — bulk energy plant against short-duration reserve. Pooling them is legitimate for a fuel-consumption or emissions question and misleading for a dispatch or flexibility question.

**`settlement_period` must not be averaged, summed, or differenced across a day boundary or across a clock change.** It is an ordinal label within a day whose count per day is not constant. It may be used for equality comparison and for ordering within a single settlement day only.

**Missing is not zero.** Only the period number and the start instant are guaranteed present; every MW member may be absent. An absent member means the value was not reported, and treating it as zero will silently understate totals and manufacture false ramps. The example record does carry explicit `0.0` for the plant that was not running, which suggests the publisher distinguishes the two cases, but that is one record and is not a guarantee — code defensively.

# 4. Time

The time axis is established by `start_time`, and by nothing else. It is a UTC instant marking the beginning of the period, and it is the only member that identifies a record absolutely; the period number alone does not, because it carries no date.

Each period is half an hour long and half-open — the interval is `[start_time, start_time + 30 min)` — so the value attaches to that whole span, not to the instant. Consecutive records tile without overlap and without gaps, which is what makes differencing and averaging across them sound. There is no end instant in the record; it is implied by the fixed length.

Relation to civil time: the positions are UTC, so mapping to British civil time requires applying the Europe/London offset for the date in question — UTC in winter, UTC+1 under British Summer Time. The example instant, 05:30Z on 31 July 2026, is 06:30 local. Any grouping by hour of day, any "morning peak" definition, and any daily boundary must be computed from the UTC instant plus that offset, and must not be computed from the period number, because the period-to-clock-time mapping is not fixed across the year.

# 5. Ambiguities

**The anchoring of period 1 is self-contradictory, and I decline to decide it.** The period number is said to start at 1 at midnight UTC, which would give 48 periods every day of the year. It is also said that the day has 46 periods at the spring clock change and 50 at the autumn one, which can only be true if the day is anchored on local midnight. Both cannot hold. The single example record is consistent with the UTC anchoring and not with the local one: 31 July 2026 is inside British Summer Time, so local midnight is 23:00Z the previous day, which would put period 12 at 04:30Z, whereas the record says 05:30Z. One example is not enough to overturn a stated rule about clock-change days, and the two readings differ by a whole period for half the year. Do not derive clock time from the period number under any circumstances; use `start_time`, which is unambiguous either way.

**Units are asserted only in prose and in member names, not declared.** That megawatts are meant is stated in the descriptions and echoed by the `_mw` suffixes, and the magnitudes in the example are consistent with GB at that scale. But there is no machine-readable unit on any member, so unit correctness cannot be validated automatically and must be enforced by convention. I am treating MW as established by the prose; I flag that nothing checks it.

**The per-member support declaration is claimed but not present.** The time member asserts that each value member states its own half-hour support. No such declaration appears on any value member. The half-hour length is therefore known only from prose. This matters because the whole case for unweighted averaging across records rests on equal support; that case currently rests on narrative, not on anything a tool can read.

**Whether the metering boundary applies beyond wind is my assumption.** The Balancing-Mechanism-only scope is stated explicitly for wind alone. It is a property of how the data is collected rather than of the fuel, so I am assuming it applies to every fuel member, and therefore that every total from this feed is a transmission-metered total that undercounts embedded plant. This is an assumption, clearly marked. If it is wrong, the fuel totals are more complete than I have said; it is not wrong in a way that would make them less complete.

**The absence of solar is unexplained.** There is no solar member. Whether solar is genuinely absent from the metered fleet, is folded into `other_mw`, or is simply not reported is not determined. My guess — and I mark it as a guess — is that GB solar is overwhelmingly distribution-connected and therefore falls outside the metering boundary, which would mean it is absent rather than hidden inside `other_mw`. Either way, do not present any mix figure from this feed as including solar.

**Revisions and record identity are undetermined.** There is no revision number, publication timestamp, or version flag. If the publisher ever restates a settlement period — and settlement data of this kind commonly is restated, which is domain knowledge and not something these files establish — there is no way to tell an initial value from a corrected one, and no way to order two records for the same instant. Treat `start_time` as the key and decide a last-write-wins or first-write-wins policy explicitly; the files do not decide it for you.

**Sign conventions on the fuel members are not stated.** The interconnectors are explicitly signed; the fuel members say nothing about sign. Whether a fuel member can ever be negative — station load, metering correction — is not determined. I decline to guess. Validate for negatives and investigate rather than clipping them.

**`intelec_mw` naming.** The code reads like a generic abbreviation for electricity but is said to name one specific cable to Ireland. Nothing here is ambiguous about the meaning; the risk is purely that a reader will mistake it for a total or an aggregate. It is not one.

**`other_mw` composition is undetermined.** It is the residue of BMRS's own fuel-type reporting, so its contents can change if BMRS begins reporting a fuel separately. Nothing in the files pins its composition or warns of a break. Do not model it as a stable category over long spans.
