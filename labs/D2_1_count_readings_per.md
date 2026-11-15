---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "2.1"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D2_1_count_readings_per.html"
---

# Lab 2.1 · Count readings per meter and district

Count readings per meter and district, then time a nested-loop version on 100,000 rows.

Day 2 · Session 1: Dictionaries for counting and grouping

### Goal

Count a month of readings per meter and per district with dictionaries, then measure what a loop inside a loop costs on 100,000 rows. You leave with two functions and two timings.

## What you need

- The folder `2.1` of the workspace: `count.py`, `timing.py`, and in `data/` the files `readings_clean.csv` (17,561 rows), `meters.csv` (600 meters) and `readings_large.csv` (100,000 rows)
- AI policy: tutor. Hints and explanations of messages, no code

### Count the readings of each meter in one pass 7 min

```bash
# file: terminal
cd ../2.1
uv run python count.py
```

It stops at `NotImplementedError`: that is your first function. Write `count_per_meter`: start with an empty dictionary, walk the readings once, and for each one add 1 to the count of its meter. `counts.get(key, 0)` answers 0 for a meter you have not seen yet.

```python
# file: count.py
counts: dict[str, int] = {}
for reading in readings:
    ...
return counts
```

### Build an index of meters; count per district 8 min

Read `count_per_district_slow`: it is correct, and for every reading it searches the list of meters. In `count_per_district`, do the search once for all: build a dictionary from meter id to district, then count with one lookup per reading.

```python
# file: count.py
district_of = {meter["meter_id"]: meter["district"] for meter in meters}
```

```bash
# file: terminal
uv run python count.py
```

The six counts add up to 17,561, the number of rows in the file. Check that they do.

### Time both versions on 100,000 rows 6 min

```bash
# file: terminal
uv run python timing.py
```

The script runs the slow version and yours on the large file, checks that they agree, and writes `timings.txt`. Before you look: with 600 meters, how many comparisons does the slow version make per reading, on average? Then read the ratio.

### Run the type checker and the lab check 4 min

```bash
# file: terminal
uv run mypy --strict count.py
uv run ../lab.py check 2.1
```

### ✱ Stretch

Group the readings by district into lists of values (`dict[str, list[float]]`) and print each district's highest reading. `groups.setdefault(district, []).append(value)` does the grouping in one line.

## Check yourself

1. Your function and the slow one give the same counts. What exactly did you move out of the loop?
2. The registry grows to 60,000 meters. What happens to each version's time?
3. What would `counts[meter_id] += 1` do for the first reading of a meter, without `get`?
