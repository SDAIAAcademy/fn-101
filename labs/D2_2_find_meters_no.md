---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "2.2"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D2_2_find_meters_no.html"
---

# Lab 2.2 · Find silent meters and unknown ids

Find meters with no reading and readings with no known meter.

Day 2 · Session 2: Sets and membership

### Goal

Compare the month's readings with the meter registry and answer three questions with sets: which meters sent nothing, which ids in the readings are unknown, and which meter and date pairs appear twice.

## What you need

- The folder `2.2` of the workspace: `coverage_report.py`, and in `data/` the files `readings_2026_09.csv` (the month as it arrived, 17,690 rows) and `meters.csv`
- AI policy: tutor. Hints and explanations of messages, no code

### Build the two sets of meter ids 5 min

```bash
# file: terminal
cd ../2.2
uv run python coverage_report.py
```

Two collections of ids matter: the meters in the registry and the meters that appear in the readings. Build each as a set with a comprehension. Try them at a Python prompt first and look at their sizes.

```python
# file: coverage_report.py
registered = {meter["meter_id"] for meter in meters}
reporting = {reading["meter_id"] for reading in readings}
```

### Find the meters with no reading 5 min

Write `silent_meters`: the ids that are in the registry and not in the readings. One operator between the two sets gives the answer; return it as a sorted list, because a set has no order and a report needs one.

### Find the readings with no known meter 5 min

Write `unknown_meters`: the same two sets, the other way round. Run the script and read both lists. Which of the two findings is a problem with the data file, and which is a question for the field team?

### Find the repeated meter and date pairs 6 min

A meter should have one reading per date. Write `repeated_keys`: walk the readings once, keep a set of the `(meter_id, date)` pairs seen so far, and collect a pair when you meet it a second time. A tuple can be a member of a set; a list cannot.

```python
# file: coverage_report.py
key = (reading["meter_id"], reading["date"])
if key in seen:
    ...
```

### Run the type checker and the lab check 4 min

```bash
# file: terminal
uv run python coverage_report.py
uv run mypy --strict coverage_report.py
uv run ../lab.py check 2.2
```

### ✱ Stretch

List the meters that have fewer than 30 different dates in the file, with the number of dates each has. You need a dictionary from meter id to a set of dates.

## Check yourself

1. Why does `silent_meters` return a sorted list and not the set itself?
2. What would `registered & reporting` hold, and how many ids?
3. Why can `(meter_id, date)` go into a set while `[meter_id, date]` cannot?
