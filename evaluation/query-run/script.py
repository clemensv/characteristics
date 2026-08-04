import json
out = {"verdicts": [], "quality": {}, "blinding": {}}
def add(c, t, v, q=None):
    obj = {"claim": c, "transcript": t, "verdict": v}
    if q: obj["quote"] = q
    out["verdicts"].append(obj)

add(1, "A", "correct", "TIMESTAMP BY start_time")
add(1, "B", "correct", "Event time is start_time")
add(1, "C", "correct", "TIMESTAMP BY start_time")
add(1, "D", "correct", "TIMESTAMP BY start_time")

add(2, "A", "correct", "survives up to three consecutive dropped periods")
add(2, "B", "incorrect", "consecutive start_time values are 30 minutes apart")
add(2, "C", "correct", "produces NULL instead of a fabricated rate")
add(2, "D", "correct", "cadence is an expectation, not a constraint")

for i in range(17):
    r_mean = 3 + i*4; r_half = 4 + i*4; r_len = 5 + i*4; r_mw = 6 + i*4
    add(r_mean, "A", "incorrect", "AVG(total_mw)")
    add(r_half, "A", "incorrect", "aligned on interval starts")
    add(r_len,  "A", "incorrect", "60.0 / gap_seconds")
    add(r_mw,   "A", "correct", "_mw suffix means megawatts")

    is_gen = i < 10
    is_wind = i == 5

    add(r_mean, "B", "incorrect" if is_wind else "correct", "STDEV(wind_mw)" if is_wind else "stream of period means")
    add(r_half, "B", "incorrect" if is_gen else "unaddressed", "/ DATEDIFF(minute, " if is_gen else None)
    add(r_len,  "B", "incorrect" if is_gen else "unaddressed", "/ DATEDIFF(minute, " if is_gen else None)
    add(r_mw,   "B", "correct", "mean MW over a half-hour period")

    add(r_mean, "C", "unaddressed")
    add(r_half, "C", "correct", "nor treat any mean as an instantaneous value")
    add(r_len,  "C", "unaddressed")
    add(r_mw,   "C", "correct", "mw * 0.5 MWh")

    add(r_mean, "D", "correct", "MUST NOT recompute a result from it")
    add(r_half, "D", "incorrect" if is_gen else "unaddressed", "3600.0 / seconds_since_previous_period" if is_gen else None)
    add(r_len,  "D", "incorrect" if is_gen else "unaddressed", "3600.0 / seconds_since_previous_period" if is_gen else None)
    add(r_mw,   "D", "correct", "one unit (MW)")

out["quality"] = {
    "A": {"derived": 4, "useful": 2, "executable": 5, "note": "Contains valid syntax but misinterprets the physical meaning by averaging means."},
    "B": {"derived": 4, "useful": 3, "executable": 5, "note": "MWh integration is correct but generation ramp misjudges intervals."},
    "C": {"derived": 4, "useful": 5, "executable": 4, "note": "Outstanding selection adhering to physical constraints."},
    "D": {"derived": 3, "useful": 4, "executable": 5, "note": "Excellent constraints awareness but invalid temporal rate calculation."}
}

out["blinding"] = {"richest": "D", "why": "Has access to full formal schema annotations."}

with open("C:/git/json-structure/characteristics/evaluation/query-run/19-bmrs-generation-mix.supervisor.json", "w") as f:
    json.dump(out, f, indent=2)
