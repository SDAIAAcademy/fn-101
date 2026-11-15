---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "1.3"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D1_3_annotate_supplied_reading.html"
---

# Lab 1.3 · Annotate the reading parser

Annotate the supplied reading parser and fix every error the type checker reports.

Day 1 · Session 3: Type hints and a checker

### Goal

Add type hints to a small parser and let a type checker find its bugs before any input does. You finish with a parser that passes its tests and a strict type check with no errors.

## What you need

- The folder `1.3` of the workspace: `parser.py` (five functions, no hints) and `test_parser.py`
- A type checker: the labs use mypy; Pyright reports the same problems in other words
- AI policy: tutor. An assistant may explain what a checker message means; you make the change

### Run the tests and the checker on the supplied parser 4 min

```bash
# file: terminal
cd ../1.3
uv run pytest
uv run mypy parser.py
```

Four tests fail, and the checker says `Success: no issues found`. Both are true: a checker reads only functions that carry hints, and this file has none. A clean report on code without hints proves nothing.

### Annotate every function 7 min

Write down what each function promises, from its docstring and the tests, not from what its code happens to do. A bad line gives `None`, so the promise includes `None`.

```python
# file: parser.py
def split_line(line: str) -> list[str] | None:
def parse_value(text: str) -> float | None:
def parse_line(line: str) -> tuple[str, str, float] | None:
def total(lines: list[str]) -> float:
def highest(lines: list[str]) -> float | None:
```

```bash
# file: terminal
uv run mypy --strict parser.py
```

Now the checker has something to compare the code with. Count the errors it reports.

### Fix each error the checker reports 10 min

Take the errors from the top. Each names a line and what does not fit. Most say the same thing in different places: a value that may be `None` is used as if it never were. Handle the `None` first, then use the value.

```python
# file: parser.py
parts = split_line(line)
if parts is None:
    return None
meter_id, day, text = parts
```

Do not silence an error with `# type: ignore` or `Any`: every one of them is a line that crashes on some input. Run the checker again after each fix and watch the count fall.

### Run the tests, the strict check and the lab check 4 min

```bash
# file: terminal
uv run pytest
uv run mypy --strict parser.py
uv run ../lab.py check 1.3
```

### ✱ Stretch

Replace the tuple with a `NamedTuple` called `Reading`, so that `reading[2]` becomes `reading.m3`. The tests still pass: a named tuple is a tuple.

## Check yourself

1. Why did the first run of the checker report no issues on a file with four failing tests?
2. Which error pointed at a comparison between a number and a piece of text, and what would Python have done at that line?
3. A hint says `-> float | None`. What must every caller do before arithmetic?
