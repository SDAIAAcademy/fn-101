---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "1.2"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D1_2_split_40_line.html"
---

# Lab 1.2 · Split a script into four functions

Split a 40-line script into four functions with stated inputs and outputs.

Day 1 · Session 2: Functions with clear contracts

### Goal

Turn a forty-line script that works into four functions with stated inputs and outputs, without changing what it prints. Afterwards each job can be tested alone and imported by other code.

## What you need

- The folder `1.2` of the workspace: `monthly_bill.py`, `test_bill.py` and `data/sample_meter.csv` (thirty days of meter M-0042)
- AI policy: tutor. An assistant may explain an error message; it does not write the functions

### Run the script and mark its four jobs 5 min

```bash
# file: terminal
cd ../1.2
uv run python monthly_bill.py
uv run pytest
```

The script prints a bill of four lines; keep that output, you will compare with it. The tests cannot even start: they import four functions that do not exist yet. Read the script and draw a line between its four jobs: read the file, keep the numbers, compute the amount, write the text.

### Move each job into a function with a docstring 12 min

The tests are the contract. Read `test_bill.py` first: it tells you each function's name, what goes in and what comes out.

| Function | Takes | Returns |
| --- | --- | --- |
| `load_rows(path)` | the path of the file | a list of dictionaries, one per row |
| `clean(rows)` | those rows | the numbers, and how many rows were skipped |
| `bill(total_m3)` | a month's consumption | the amount due in SAR |
| `format_bill(meter_id, values, skipped, amount)` | the facts of a bill | four lines as one string |

A function gets everything it needs through its parameters and gives its result with `return`. Only `load_rows` touches a file; none of the four prints. Give each a one-line docstring that says what goes in and what comes out.

```python
# file: monthly_bill.py
def bill(total_m3):
    """Take a month's consumption in cubic metres; return the amount due in SAR."""
    ...
```

### Put the script part under a main guard 4 min

What is left is the script: call the four functions and print. Put it in `main()` and call that only when the file is run, so that importing the file runs nothing.

```python
# file: monthly_bill.py
def main():
    rows = load_rows("data/sample_meter.csv")
    ...

if __name__ == "__main__":
    main()
```

### Run the tests and the check 4 min

```bash
# file: terminal
uv run python monthly_bill.py
uv run pytest
uv run ../lab.py check 1.2
```

The bill must be the same four lines as before. The check also imports your file and expects silence.

### ✱ Stretch

Add a doctest to `bill` for a month of exactly 15 cubic metres and run it with `uv run python -m doctest -v monthly_bill.py`.

## Check yourself

1. Which of your four functions could you test without any file on disk?
2. What would `import monthly_bill` have done before your change?
3. The tariff changes next year. How many functions do you open?
