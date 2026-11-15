---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "4.4"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D4_4_get_hints_from.html"
---

# Lab 4.4 · Debug a third defect with the tutor

Get hints from the course tutor on a new defect, then explain the fix in your own words.

Day 4 · Session 4: Learning with an assistant without losing the skill

### Goal

Mazen, the maintenance planner, reports a third defect in Miqyas. Use the six steps again, and this time ask the course tutor, Dalil, for hints when you are stuck. The lab ends with the tutor closed: you explain the fix in your own words, without code.

## What you need

- The folder `4.4` of the workspace: the package `miqyas/`, `symptom.md`, `debug_log.md`, `test_regression.py`, `explanation.md` and the data
- The tutor, `tutor.py`, one level up. With `--recorded` it needs no key and no network. With a question in quotes it asks a free hosted model, and needs a key in `TUTOR_API_KEY` or `OPENROUTER_API_KEY`
- AI policy: off for the first step, tutor for the next two, off again for the last

### Reproduce and shrink on your own, in the log 6 min

```bash
# file: terminal
cd ../4.4
uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md
```

Read `symptom.md` and the Districts table of `out/report.md`. Write **Reproduce** in `debug_log.md`. Then shrink: which function hands the report its anomalies per district, and what is the smallest input you could give it by hand? Write **Shrink** and a first **Hypothesis**, even a vague one, before you ask anyone.

### Ask the tutor for one hint at a time 6 min

```bash
# file: terminal
uv run ../tutor.py --recorded
uv run ../tutor.py "two districts show the same list: where would you look first?"
```

Take one hint, then do what it suggests before you take the next: run the experiment, answer its question in the log under **Test**. Every exchange is added to `tutor_log.md`. On the hosted path, only your question and the source files you name with `--file` leave the laptop; the tutor refuses data files.

Stop asking as soon as your hypothesis names a line. If you have a key, compare one recorded hint with one hosted answer: which left more of the thinking to you?

### Fix the line and write the regression test 6 min

Write the test first, from your shrunk case, in `test_regression.py`: two meters in two districts, one anomaly, and an assertion about what each district holds. Run it and watch it fail. Then change the one line in `miqyas/report.py` and watch it pass. Fill **Fix** and **Regression** in the log.

```bash
# file: terminal
uv run pytest test_regression.py
uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md
```

### Close the tutor; explain the fix in words 7 min

Close the terminal with the tutor and the editor with the code. In `explanation.md`, write for a colleague who was not here: what was wrong, why it produced exactly this symptom, and why your change repairs it. At least forty words, no code. Then read it to your neighbour, who asks one question. If you cannot write it without looking, go back to **Test**: you have a fix and not yet an understanding.

```bash
# file: terminal
uv run ../lab.py check 4.4
```

### ✱ Stretch

With a key set, ask the hosted tutor outright for the corrected code, and note in the log what it does. Then read the instruction it was given, `RULE` in `tutor.py`, and the function below it that withholds code blocks. Which of the two would you trust less on its own?

## Check yourself

1. Which hint moved you on, and what did you do with it before asking again?
2. This defect and defect A of yesterday are the same idea of Day 1. Which one?
3. What is the difference between a hint you can use and an answer you can paste, a week from now?
