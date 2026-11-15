---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "2.3"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D2_3_stream_large_readings.html"
---

# Lab 2.3 · Stream a large readings file

Stream a large readings file with a generator and compare peak memory with a list.

Day 2 · Session 3: Comprehensions and generators

### Goal

Add up a file of 100,000 readings twice: once by loading every row into a list, once with a generator that hands over one value at a time. Then measure the peak memory of both.

## What you need

- The folder `2.3` of the workspace: `stream.py`, `memory.py` and `data/readings_large.csv` (100,000 rows)
- AI policy: tutor. Hints and explanations of messages, no code

### Run the list version and read how it works 4 min

```bash
# file: terminal
cd ../2.3
uv run python stream.py
```

The first total prints; the second stops at `NotImplementedError`. Read `total_list`: at its busiest moment, which collections exist at once, and how many items does each hold?

### Write the generator that yields one value per row 8 min

Write `read_values`. It opens the file, loops over the reader and, for each row, `yield`s the consumption as a float. There is no list and no `return`.

```python
# file: stream.py
with open(path, encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file):
        yield ...
```

Try it at a prompt: `values = read_values("data/readings_large.csv")` prints nothing and reads nothing. `next(values)` gives the first value, `next(values)` again the second.

### Add up the stream; compare the two totals 4 min

Write `total_stream` in one line: `sum` takes anything it can loop over, a generator included. Run the script: the two totals must be the same number.

```bash
# file: terminal
uv run python stream.py
```

### Measure both peaks of memory 5 min

```bash
# file: terminal
uv run python memory.py
```

The script measures the peak memory of each version with `tracemalloc` and writes `memory.txt`. Predict the ratio before you run it. Then predict what both peaks become for a file ten times as long.

### Run the type checker and the lab check 4 min

```bash
# file: terminal
uv run mypy --strict stream.py
uv run ../lab.py check 2.3
```

### ✱ Stretch

At a prompt, make one generator and pass it to `sum` twice in a row. Explain what the second call returns, and what you would have to do to get the total again.

## Check yourself

1. When does the file of `read_values` get opened: when the function is called, or later?
2. You need the highest value and the total. Can one pass over the generator give both?
3. Name one task on this file for which the list is the right choice.
