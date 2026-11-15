---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "3.3"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D3_3_reject_malformed_lines.html"
---

# Lab 3.3 · Reject malformed lines with a reason

Reject malformed lines with a reason code so every input line is accounted for.

Day 3 · Session 3: Exceptions that explain

### Goal

Take in a raw ticket file in which some lines are broken in eight different ways. Accept the good lines, reject each bad one with a reason code and a detail, and prove that every line of the input is accounted for.

## What you need

- The folder `3.3` of the workspace: `intake.py` and `data/tickets_raw.jsonl` (435 lines)
- AI policy: tutor. Hints and explanations of messages, no code

### Run the intake and read the first crash 4 min

```bash
# file: terminal
cd ../3.3
uv run python intake.py
```

Read the docstring at the top of `intake.py`: eight reason codes, in the order in which they are checked. Two are already written in `parse_ticket`. Read how they raise `Rejected`: a code for the machine, a detail for a person.

### Add the six checks, each raising a reason 10 min

Add the six remaining checks to `parse_ticket`, in order. Each is a guard that raises; the ticket is returned only when none did.

```python
# file: intake.py
if not isinstance(ticket, dict):
    raise Rejected("NOT_OBJECT", f"the line holds a {type(ticket).__name__}, not an object")
for field in REQUIRED:
    if field not in ticket:
        raise Rejected("MISSING_FIELD", f"{field} is absent")
```

For the date, let Python decide: `date.fromisoformat` raises `ValueError` for anything that is not a real date, and you turn that into a `Rejected`. For the meter id use `METER_ID.fullmatch`. Try your function at a prompt on a line you typed.

### Catch the rejection around one call per line 4 min

Write the loop of `intake`. Number the lines from 1. The `try` holds one call; the `except` names `Rejected` and nothing wider, so that a mistake in your own code still shows itself.

```python
# file: intake.py
for line_no, line in enumerate(file, start=1):
    try:
        accepted.append(parse_ticket(line))
    except Rejected as problem:
        rejected.append((line_no, problem.reason, problem.detail))
```

### Write the rejection log; run the lab check 7 min

Write `write_rejections` with `csv.writer`: a header row, then one row per rejection. Run the intake. Its last lines count the reasons, and an `assert` in `main` stops the run if accepted plus rejected is not the number of lines.

```bash
# file: terminal
uv run python intake.py
uv run mypy --strict intake.py
uv run ../lab.py check 3.3
```

Open `out/rejections.csv`. Pick one line number, find that line in the input, and decide whether the detail would let Badr's team repair it.

### ✱ Stretch

Add a ninth reason, `DUPLICATE_ID`, for a ticket id that an earlier line already used. Where does the set of seen ids live, and why not in a default argument?

## Check yourself

1. A line has no `priority` field and a bad date. Which reason does it get, and why only one?
2. What would `except Exception:` have hidden while you were writing the checks?
3. The log has 35 rows. Which single number proves that no line was lost?
