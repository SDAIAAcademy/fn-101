---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "3.4"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D3_4_ai_off_find.html"
---

# Lab 3.4 · Find and fix two seeded defects

With AI off, find and fix two seeded defects and write a regression test for each.

Day 3 · Session 4: A debugging method

### Goal

Two colleagues report that Miqyas gives wrong results. With no assistant, find each defect by the six-step method, fix it, and leave behind a test that would catch it if it ever came back.

## What you need

- The folder `3.4` of the workspace: the package `miqyas/` (four modules and a command line, about 320 lines), `symptoms.md`, `two_runs.py`, `debug_log.md`, `test_regression.py`, and the data
- AI policy: off for the whole first attempt. If you are still stuck on a defect after the lab, ask the tutor for a hint tomorrow, in lab 4.4's way

### Reproduce both reports and write what you see 5 min

```bash
# file: terminal
cd ../3.4
uv run python two_runs.py
uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md
```

Read `symptoms.md`, run both commands, and write under **Reproduce** in `debug_log.md`, for each defect, the command and the wrong output. Neither command crashes: both give a wrong answer quietly. Do not open the package yet.

### Defect A: shrink, hypothesis, test, fix 8 min

**Shrink.** Does it need 17,690 rows? Try `data/tiny.csv`, two rows. Does it need two calls? Write down the smallest case that still fails.

**Hypothesis.** Read `load_readings` in `miqyas/readings.py` with the small case in mind and write one sentence: "I think … because …", with the line.

**Test.** Prove it before you change anything: a `print` on the first line of the function, or `breakpoint()` there and `p` to print a name. What does the function start with on the second call?

**Fix.** Change the one line, run `two_runs.py` again, and note the before and after in the log.

### Defect B: shrink, hypothesis, test, fix 7 min

The report's number for M-0012 is wrong, and Salma has given you the right one. Which function produces that number? Shrink until no file is needed at all: three values you can check in your head. Then the same four steps, in the log.

```python
# file: at a prompt
>>> from miqyas.anomalies import median
>>> median([1.0, 2.0, 3.0])
```

### Write a regression test for each; run the check 5 min

In `test_regression.py`, write one test per defect from your shrunk case. A good regression test is small, needs no explanation, and fails for the right reason.

```python
# file: test_regression.py
def test_defect_b_median_does_not_depend_on_the_order():
    assert median([3.0, 1.0, 2.0]) == 2.0
```

```bash
# file: terminal
uv run pytest test_regression.py
uv run ../lab.py check 3.4
```

The check puts each defect back into a copy of the package and runs your tests against it: a test that still passes there guards nothing.

### ✱ Stretch

Put defect A back and step through it with the debugger: add `breakpoint()` as the first line of `load_readings`, run `two_runs.py`, and at each stop type `p len(seen)`, then `c` to continue.

## Check yourself

1. Which slide of Day 1 showed defect A, in four lines?
2. Defect B changed no count in this month's report. Why is it still a defect worth a test?
3. Your fix works. What does the regression test add?
