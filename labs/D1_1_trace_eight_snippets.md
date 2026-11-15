---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "1.1"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D1_1_trace_eight_snippets.html"
---

# Lab 1.1 · Trace eight snippets

Trace eight snippets on paper, then check each answer in a step visualiser.

Day 1 · Session 1: Values, names and references

### Goal

Say what eight short programs print before running any of them, then find, for every wrong answer, the exact line you misread. The skill is the prediction; the score is only where you start from.

## What you need

- The workspace (built in the first step) and its folder `1.1`: eight files in `snippets/`, `predictions.txt` and `misread.md`
- Paper and a pen
- A step visualiser: Python Tutor in a browser, or the supplied `trace.py`, which works offline
- AI policy: off. No assistant, and no running the code before your prediction is written down

### Build the workspace and open the lab folder 4 min

From the course folder, build the workspace once. It appears beside the course folder and holds one folder per lab.

```bash
# file: terminal
uv run labs/kit/setup.py
cd ../manahil-labs
uv run lab.py list
cd 1.1
```

Open the folder `manahil-labs` in your editor. Read `snippets/s1.py` to `s8.py`; do not run them.

### Predict the output of all eight on paper 10 min

For each snippet draw a small table: one column per name, one row per line that runs. When two names hold the same list or dictionary, draw one box and two arrows, not two boxes. Then write what the snippet prints into `predictions.txt`, one line per snippet.

```text
# file: predictions.txt
s1: [1, 2, 3, 4] 4
s2:
s7: first printed line / second printed line
```

The first line above is the answer to `s1`, as a model of the form. Snippet 7 prints two lines: write both on one line with ` / ` between them.

### Step through each wrong one in a visualiser 7 min

Now run the check. It tells you which predictions do not match, not what the right answer is.

```bash
# file: terminal
uv run ../lab.py check 1.1
uv run ../trace.py snippets/s4.py
```

For each snippet that does not match, step through it: paste it into Python Tutor and press Next, or run `trace.py` on it. Stop at the first line where the picture differs from your table. That line is what you misread.

### Note what you misread; run the check 4 min

In `misread.md` write one line per wrong prediction: the snippet, the line, and what that line really does. Correct nothing in `predictions.txt`: the wrong answers are your record.

```text
# file: misread.md
s4: line 3 gives the name log a new empty list; the list that day names is not touched after line 2
```

```bash
# file: terminal
uv run ../lab.py check 1.1
```

### ✱ Stretch

Change one line of snippet 7 so that both grids print the same, and predict the new output before you run it. Then explain to a neighbour why `[[0] * 2] * 3` and the comprehension differ.

## Check yourself

1. In snippet 4, the function assigns `log = []`. Why does the caller's list keep both values?
2. In snippet 6, which part of the copy is shared with the original, and which is not?
3. Snippet 8 calls `tag` twice with one argument each. How many lists exist?
