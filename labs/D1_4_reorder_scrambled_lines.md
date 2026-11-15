---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "1.4"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D1_4_reorder_scrambled_lines.html"
---

# Lab 1.4 · Rebuild a validation function

Reorder scrambled lines, with distractors, into a working validation function.

Day 1 · Session 4: Parsons problems

### Goal

Rebuild two functions from their scrambled lines, leaving out the lines that do not belong. You write no new code: every decision is about order, indentation and which line is a trap.

## What you need

- The folder `1.4` of the workspace: `warmup.py` and `validate.py` (scrambled), and a test file for each
- Paper: number the lines there before you move anything in the editor
- AI policy: off. This lab is practice for the supervised check

### Order the warm-up on paper, then in the editor 6 min

```bash
# file: terminal
cd ../1.4
```

Open `warmup.py`. Seven lines; six of them make `total_valid(values)`, one is a distractor. On paper, write the order as numbers and mark the indentation of each line. Then move the lines in the editor, indent them, delete the distractor.

```bash
# file: terminal
uv run pytest test_warmup.py
```

### Order and indent the validation function 11 min

Open `validate.py`: sixteen lines, three of them distractors. The comment at the top is the specification: four reasons, checked in a fixed order. Work in this order:

1. Find the `def` line and the last `return`.
2. Pair every `if` with the `return` it guards.
3. Find what must exist before each line can run: `value` needs `text`, the range check needs `value`.
4. Place `try` and `except` around the one line that can fail.

Two pairs of lines look alike. Decide between them by asking what each would do with the row `{"consumption_m3": "250"}`.

### Run the tests; fix order or indentation 4 min

```bash
# file: terminal
uv run pytest test_validate.py
```

Read the first failing test, not the last. An `IndentationError` or a `NameError` points at a line: the first means a line sits at the wrong depth, the second that a line runs before the one that binds its name.

### Say why each distractor is wrong; check 4 min

For each of the four lines you deleted, tell a neighbour what the function would do if that line had been used. Then run the check: it accepts only supplied lines and no distractor.

```bash
# file: terminal
uv run ../lab.py check 1.4
```

### ✱ Stretch

Write one more distractor for `validate.py`, give your scrambled file to a neighbour, and say which test catches it.

## Check yourself

1. Why can the check of the meter not come before the check of the value, although both are single `if` lines?
2. What does `except TypeError:` catch when the text is `"N/A"`?
3. Which lines of the function are at depth one, and which at depth two?
