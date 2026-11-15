---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/"
---

# Python for Data and AI Work

Read, trace and debug Python by hand, then write small typed functions that grow into a command-line tool that reruns

Participants write Python the way data and AI work needs it: small typed functions over collections and files, errors that fail loudly, and code moved out of notebooks into scripts that rerun. The case is a fictional regional water utility with synthetic meter readings in comma-separated values (CSV) files and bilingual service tickets in JavaScript Object Notation (JSON) Lines. Each day opens with an AI-off drill in reading, tracing or debugging code by hand, and the labs grow into a command-line tool that validates readings, flags anomalies and writes a summary report. Arabic text normalisation and SQL are left to FN-104, version control to FN-102.

- **Audience:** Beginners. Graduates and career changers entering the AI Engineering or Data Science track; computing and data graduates who pass the placement test skip the courses it covers.
- **Prerequisites:** Has written and run a short program in any language, or completed the guided pre-work on values, conditions and loops
- **Case study:** Manahil Water Services: Manahil Water Services is a fictional regional water utility with 600 meters in six districts. Its metering team checks a month of daily readings (a CSV file with missing, repeated, out-of-range and unknown-meter rows) and its customer care team works a queue of service tickets in Arabic and English (JSON Lines). Every lab works on these files and the labs grow into Miqyas, a command-line tool that validates the readings, flags anomalies and writes a report; all data is synthetic and the same on every machine.

## Outcomes

- LO1 (Awareness): Explain what a short program prints, step by step, including name binding, shared mutable lists and dictionaries, and scope, given ten unseen snippets on paper, without a computer or assistant
- LO2 (Awareness): Distinguish when a notebook, a script or an importable module is the right home for a piece of code, given four tasks described by the utility's analysts
- LO3 (Applied): Implement typed functions that load, validate and aggregate records with lists, dictionaries, sets and comprehensions, given a month of meter readings with missing, duplicated and out-of-range values
- LO4 (Applied): Apply exception handling and input validation so that each bad record is reported with a reason instead of crashing or passing silently, given a ticket file with malformed lines, mixed Arabic and English text and a wrong encoding
- LO5 (Applied): Use a repeatable debugging method: reproduce, shrink the input, form a hypothesis, test it, fix, and add a regression check, given three seeded defects in the course codebase, with AI assistance off
- LO6 (Applied): Prepare a command-line tool from an exploratory notebook, with an entry point, arguments and a written report, given the utility's analysis notebook and raw files

## Day 1: Read before you write

Tracing code by hand, functions with contracts, type hints, and rebuilding code from its lines

#### [day1#title] Read before you write

*SDAIA Academy · Python for Data and AI Work*

Day 1: Tracing code by hand, functions with contracts, type hints, and rebuilding code from its lines

Data & AI Foundations Track · 4 teaching days + capstone day · 4 sessions · 4 labs · FN-101

#### [day1#four-days-one-tool] Four days from reading one line to shipping one tool

*The week*

1. **Day 1**: Read before you write (trace, functions, types)
2. **Day 2**: Collections (dictionaries, sets, generators, records)
3. **Day 3**: Files, text and failure (CSV, encodings, exceptions, debugging)
4. **Day 4**: From notebook to tool (entry point, tests, the tutor)
5. **Capstone**: Your own tool (work orders, a public repository)

> **What you leave with.** A command-line tool that validates a month of readings, flags anomalies and writes the same report on every run, and the habit of reading code before trusting it.

#### [day1#ai-off-tutor-full] Three ways of working with an assistant, and every lab says which

*How we work*

- **AI off.** The daily drills, the first attempt at each debugging lab, and the supervised check. Paper, an editor, the documentation.
- **AI tutor.** The other labs. The assistant gives hints and explains messages. It does not give code.
- **AI full.** The capstone. You may delegate, and you then walk through the code and change it live, on request.

> **Why not full from the start.** Day 4 shows the evidence: people who delegate while learning finish, and then cannot debug what they finished.

#### [day1#manahil-case] Manahil Water Services: 600 meters, one month, two messy files

*The case study*

| File | Holds |
| --- | --- |
| `meters.csv` | 600 meters in six districts |
| `readings_2026_09.csv` | 17,690 daily readings, 129 of them bad |
| `tickets.jsonl` | 400 service tickets, Arabic and English |

- **Salma**, metering analyst, has a notebook nobody else can rerun
- **Badr**, customer care lead, wants the ticket queue sorted
- **You** join as Shouq, the junior analyst
- The fix is **Miqyas**, a command-line tool you build by Day 4

> **All of it is synthetic.** No real person, meter or phone number. You still treat the tickets as personal data, because the habits are the point.

#### [day1#workspace-setup] One command builds the workspace; every lab has its own folder

*Setup*

```bash
# file: terminal
uv run labs/kit/setup.py
cd ../manahil-labs
uv run lab.py list
cd 1.1
```

- `uv run …` runs Python with the project's tools: a test runner, a type checker, a linter
- `lab.py start 2.1 --discard` gives a lab back its supplied state
- `lab.py check 2.1` runs your code and says what is still to do

> **Nothing to install by hand.** The first `uv run` downloads the tools once. No model is downloaded at any point of the course.

#### [day1#drill-1] Predict the output · 10 minutes

*Drill 1 · AI off*

Five snippets on paper: `labs/drills/day1.md`. No computer, no assistant. Write what each prints.

#### [day1#agenda] Read before you write

*Today*

- **Session 1 · Values, names and references**: Names bind to objects, assignment never copies, and a shared list changes for every name that holds it
- **Session 2 · Functions with clear contracts**: One job per function, inputs and outputs stated, effects kept at the edge, and scope explained by the call stack
- **Session 3 · Type hints and a checker**: Type hints as promises a checker verifies: built-in generics, None as a value that must be handled, and reading the checker's report
- **Session 4 · Parsons problems**: Rebuilding a function from its scrambled lines: order, indentation, and the lines that do not belong

### Session 1: Values, names and references

#### [day1#s1] Values, names and references

*Session 1*

- Trace a short program line by line with a table of names and objects
- Predict when two names share one mutable object and when they do not
- Distinguish rebinding a name from mutating an object

#### [day1#a-name-is-a-label] A name is a label tied to an object, not a box that holds a value

*Names and objects*

```python
# file: names.py
reading = 0.742
latest = reading
reading = 0.810
print(latest)        # 0.742
```

- Line 1 makes an object, `0.742`, and ties the name `reading` to it
- Line 2 ties a **second name** to the same object
- Line 3 ties `reading` to a new object; `latest` is not asked

> **Read `=` as "now names".** The right side is worked out first; then the name on the left is tied to the result.

#### [day1#assignment-never-copies] Assignment never copies: b = a gives one list two names

*Aliasing*

```python
# file: snippets/s1.py
a = [1, 2, 3]
b = a
b.append(4)
print(a, len(b))
```

- **It prints.** `[1, 2, 3, 4] 4`

There was only ever one list. `append` changed it, and both names show the change.

> **What goes wrong.** You "save the original" with `backup = rows`, clean `rows`, and the backup is cleaned too.

#### [day1#mutate-or-rebind] A line either changes an object or moves a name. Know which.

*Two different things a line can do*

| The line | What it does | Who sees it |
| --- | --- | --- |
| `b.append(4)`, `b[0] = 9`, `d["k"] = 1` | changes the object (**mutation**) | every name tied to that object |
| `b = b + [4]`, `b = []`, `n = n + 1` | ties the name to another object (**rebinding**) | only that name |

> **The test.** Is there a bare name on the left of `=`? Then it is rebinding. A dot or a bracket on the left, or a method that changes in place, is mutation.

#### [day1#immutable-values] Numbers, strings and tuples cannot change, so sharing them is harmless

*Mutable and immutable*

- **Cannot be changed.** `int`, `float`, `str`, `bool`, `tuple`, `None`. Every "change" makes a new object: `y = y + 5`, `name.upper()`.
- **Can be changed in place.** `list`, `dict`, `set`, and most objects you define. Sharing one of these is where surprises come from.

```python
# file: snippets/s2.py
x = 10
y = x
y = y + 5
print(x, y)          # 10 15
```

#### [day1#copies-are-shallow] A copy is one level deep: the outside is new, the inside is shared

*Copies*

```python
# file: snippets/s6.py
meter = {"id": "M-0042", "readings": [0.6]}
backup = dict(meter)
backup["id"] = "M-0043"
backup["readings"].append(0.7)
print(meter["id"], meter["readings"])
```

- `a[:]`, `list(a)`, `dict(d)` and `.copy()` make a new outer object
- What is inside is **not** copied: both dictionaries point at one list of readings
- `copy.deepcopy` copies all levels, when you need it

> **It prints** `M-0042 [0.6, 0.7]`: the id was safe, the readings were not.

#### [day1#equal-or-same] == asks "equal value?"; is asks "the same object?"

*Two questions*

```python
# file: same.py
a = [0.7, 0.9]
b = a
c = a[:]
print(a == c, a is c)    # True False
print(a == b, a is b)    # True True
```

- Use `==` for values, almost always
- Use `is` for `None`: `if value is None`
- When a trace surprises you, `a is b` tells you whether you have one object or two

#### [day1#functions-share-arguments] A call ties the parameter name to the caller's object: no copy there either

*Calling a function*

```python
# file: snippets/s4.py
def add_reading(log, value):
    log.append(value)
    log = []
    log.append(-1)

day = [1.2]
add_reading(day, 0.8)
print(day)
```

- call: `log` and `day` name one list
- line 2: that list becomes `[1.2, 0.8]`
- line 3: `log` is tied to a new empty list
- line 4: the new list gets `-1`; nobody else sees it
- prints: `[1.2, 0.8]`

#### [day1#trace-table] Trace on paper: a column per name, a row per line that runs

*The method*

| Line | `readings` | `copy` | Note |
| --- | --- | --- | --- |
| `readings = [0.7, 0.9]` | list A: 0.7, 0.9 |  | a new list, A |
| `copy = readings[:]` | A | list B: 0.7, 0.9 | a slice makes a second list |
| `copy[0] = 9.9` | A | B: 9.9, 0.9 | mutation of B only |
| `readings.append(1.1)` | A: 0.7, 0.9, 1.1 | B | mutation of A only |
| `print(readings, copy)` | `[0.7, 0.9, 1.1] [9.9, 0.9]` |  |  |

> **Give objects letters.** Two names with the same letter share an object. That is the whole trick, and it is what a step visualiser draws for you.

#### [day1#check-shared-list] What does the last line print?

*Checkpoint*

**Question:** Salma keeps yesterday's readings before cleaning today's: `before = rows`, then `rows.remove(-1.0)`, then `rows = rows + [0.5]`. The list started as `[0.7, -1.0]`. What is `before` now?

- A. [0.7, -1.0]
- B. [0.7]
- C. [0.7, 0.5]
- D. [0.7, -1.0, 0.5]

#### [day1#lab-1-1] Trace eight snippets

Lab 1.1 · 25 min

Trace eight snippets on paper, then check each answer in a step visualiser.

[D1_1_trace_eight_snippets.html](https://sdaiaacademy.github.io/fn-101/labs/D1_1_trace_eight_snippets.html)

- [ ] Build the workspace and open the lab folder (4 min)
- [ ] Predict the output of all eight on paper (10 min)
- [ ] Step through each wrong one in a visualiser (7 min)
- [ ] Note what you misread; run the check (4 min)
- [ ] ✱ Stretch: Change one line of snippet 7 so that both grids print the same, and predict before you run

### Session 2: Functions with clear contracts

#### [day1#s2] Functions with clear contracts

*Session 2*

- Split a script into functions that each do one job
- State a function's inputs and output in its signature and docstring
- Explain what a function can see and change, using scope and the call stack

#### [day1#one-job-per-function] A forty-line script does four jobs, and you can test none of them

*Decomposition*

1. **1 · Load** read the file into rows
2. **2 · Clean** keep the numbers, count the rest
3. **3 · Compute** the amount due
4. **4 · Present** four lines of text

- To check the tariff you must have a file, run everything, and read the last line
- A function per job gives each job a **name**, a **way in** and a **way out**

#### [day1#contract-in-signature] Everything in comes through parameters; everything out through return

*Contracts*

```python
# file: monthly_bill.py
def bill(total_m3):
    """Take a month's consumption in
    cubic metres; return the amount
    due in SAR."""
    if total_m3 <= 15:
        amount = total_m3 * 2.0
    else:
        amount = 30.0 + (total_m3 - 15) * 4.5
    return amount + 5.0
```

- The first line and the docstring are the **contract**: what goes in, what comes out
- No name from outside is read, nothing outside is changed
- So one line checks it: `bill(15.0) == 35.0`

> **What goes wrong.** A function that `print`s its result returns `None`. The caller has nothing to work with.

#### [day1#pure-core-effects-edge] Keep files and printing at the edge, and the middle becomes easy to test

*Where the effects go*

- **Edge in.** `load_rows(path)` is the only function that opens a file.
- **The middle.** `clean`, `bill`, `format_bill`: values in, values out. The same input always gives the same output.
- **Edge out.** `main()` is the only place that prints.

> **You will see this shape all week.** Miqyas loads at one end, writes a report at the other, and everything between is functions you can call with three rows typed by hand.

#### [day1#scope-local-names] A name bound inside a function lives inside that call, and nowhere else

*Scope*

```python
# file: snippets/s5.py
total = 0

def add(value):
    total = value
    return total

add(5)
print(total, add(7))     # 0 7
```

- Assigning to `total` inside `add` makes a **local** name
- The `total` of line 1 is a different name in a different scope
- A function may **read** an outer name; assigning never reaches it

> **So do not rely on outer names at all.** Pass what the function needs; return what it produces.

#### [day1#call-stack] Every call gets its own frame of names, stacked on the caller's

*The call stack*

1. **bill(17.211)** total_m3, amount
2. **main()** rows, values, skipped
3. **the module** load_rows, clean, bill, main

- The top frame is the function running now
- When it returns, its frame and its local names are gone
- A **traceback** is this stack printed at the moment of an error, the top frame last

#### [day1#docstrings-and-doctests] A docstring states the contract; a doctest is an example that runs

*Saying the contract*

```python
# file: readings.py
def parse_value(text):
    """Turn the consumption cell into
    cubic metres.

    >>> parse_value(" 0.750 ")
    0.75
    >>> parse_value("12")
    12.0
    """
```

- First line: what goes in, what comes out, in words
- Lines that start with `>>>` are a session someone can retype
- `python -m doctest file.py` runs them and reports any that no longer hold

> **Examples age well.** A sentence can drift from the code without anyone noticing; an example that runs cannot.

#### [day1#main-guard] The main guard lets a file be both a script and something to import

*Run or import*

```python
# file: monthly_bill.py
def main():
    rows = load_rows("data/sample_meter.csv")
    values, skipped = clean(rows)
    amount = bill(sum(values))
    ...

if __name__ == "__main__":
    main()
```

- Run the file: Python sets `__name__` to `"__main__"`, so `main()` runs
- Import the file: `__name__` is `"monthly_bill"`, nothing runs
- The tests import it. Without the guard, every test run would print a bill

#### [day1#default-argument-trap] A default value is made once, when the function is defined

*A trap in the signature*

```python
# file: snippets/s8.py
def tag(reading, tags=[]):
    tags.append(reading)
    return tags

first = tag("high")
second = tag("low")
print(first, second, first is second)
```

- **It prints.** `['high', 'low'] ['high', 'low'] True`

```python
# file: the fix
def tag(reading, tags=None):
    if tags is None:
        tags = []
```

> **One list for every call.** A mutable default remembers what earlier calls did. Remember this slide on Day 3.

#### [day1#check-function-contract] Which version of the function can be tested with one line?

*Checkpoint*

**Question:** Shouq needs a function that counts the rows of a month with an empty consumption cell. Four colleagues propose one each. Which can be checked by a single `assert`, with no file on disk?

- A. count_missing() opens the month's file and returns the count
- B. count_missing(rows) prints the count
- C. count_missing(rows) returns the count
- D. count_missing(rows) stores the count in a global named missing

#### [day1#lab-1-2] Split a script into four functions

Lab 1.2 · 25 min

Split a 40-line script into four functions with stated inputs and outputs.

[D1_2_split_40_line.html](https://sdaiaacademy.github.io/fn-101/labs/D1_2_split_40_line.html)

- [ ] Run the script and mark its four jobs (5 min)
- [ ] Move each job into a function with a docstring (12 min)
- [ ] Put the script part under a main guard (4 min)
- [ ] Run the tests and the check (4 min)
- [ ] ✱ Stretch: Add a doctest to bill for a month of exactly 15 cubic metres and run it

### Session 3: Type hints and a checker

#### [day1#s3] Type hints and a checker

*Session 3*

- Annotate parameters and return values with built-in types
- Read a type checker's report and find the line it points at
- Handle a value that may be None before using it

#### [day1#hints-are-promises] A type hint is a promise about a value, written where a tool can check it

*Type hints*

```python
# file: parser.py
def parse_value(text: str) -> float | None:
    if text == "":
        return None
    return float(text)
```

- `text: str`: callers promise to pass text
- `-> float | None`: the function promises a number, or `None`
- Python itself **ignores** hints when it runs the code
- A **type checker** reads them and finds every line that breaks a promise

#### [day1#built-in-generics] Say what is inside: a list of what, a dictionary from what to what

*Hints for collections*

| Hint | Reads as | At Manahil |
| --- | --- | --- |
| `list[float]` | a list of numbers | one meter's month |
| `dict[str, int]` | text keys, whole-number values | readings per district |
| `set[str]` | a set of text | the known meter ids |
| `tuple[str, str, float]` | exactly three values, in this order | meter, day, cubic metres |
| `dict[str, str]` | text to text | one row of a CSV file |

> **The last row matters.** A CSV reader gives you text for every cell, numbers included. The hint says so, and the checker stops you adding text to a number.

#### [day1#none-is-a-value] "Or None" in a hint forces every caller to handle the missing case

*The value that is not there*

```python
# file: before
value = parse_value(text)
return meter_id, day, round(value, 3)
```

```python
# file: after
value = parse_value(text)
if value is None:
    return None
return meter_id, day, round(value, 3)
```

- Before: an empty cell crashes at `round(None, 3)`, some day, on some file
- After the check, the checker knows `value` is a `float` on the last line: this is called **narrowing**

> **Not `if not value`.** A reading of `0.0` is a real reading, and it is "not value" too.

#### [day1#checker-reads-annotated-only] On code without hints, a clean report from the checker proves nothing

*From the lab's run*

- **0** issues reported on the supplied parser, while 4 of its 6 tests fail
- **9** errors in strict mode: every one says "missing a type annotation"
- **9** different errors once five signatures are annotated: each a real bug

> **Strict mode** refuses unannotated functions, so "no issues" means what it says. The labs and the capstone use `mypy --strict`.

#### [day1#read-a-checker-report] Every line of the report is a place, a complaint and a code

*Reading the report*

```text
# file: uv run mypy --strict parser.py
parser.py:26: error: "None" object is not iterable  [misc]
parser.py:43: error: Unsupported operand types for > ("float" and "str")  [operator]
parser.py:45: error: Incompatible return value type (got "str", expected "float | None")  [return-value]
```

- **Line 26.** Three names are unpacked from something that may be `None`.
- **Line 43.** A number is compared with text. Python would raise a TypeError here.
- **Line 45.** The function returns text where its hint promised a number.

#### [day1#hints-do-not-validate-data] A checker verifies your code, not the file someone sends you

*What hints cannot do*

- **The checker catches.** Text added to a number, a forgotten `None`, a wrong return, a misspelt field of a record: mistakes in the **program**.
- **The checker cannot see.** A cell that holds `N/A`, a reading of 9,000 cubic metres, a meter that is not in the registry: mistakes in the **data**.

> **Both are needed.** Hints keep the code honest. Validation at the door, with a reason for every rejected row, keeps the data honest. That is Day 3.

#### [day1#checker-and-linter] A type checker and a linter read your code without running it

*Two kinds of tool*

| Tool | Asks | Examples | In the workspace |
| --- | --- | --- | --- |
| Type checker | do the values fit the hints? | mypy, Pyright | `uv run mypy --strict file.py` |
| Linter | is anything unused, shadowed or suspicious? | Ruff | `uv run ruff check` |
| Formatter | is the layout the usual one? | Ruff | `uv run ruff format` |

> **The names are examples.** An editor such as VS Code or VSCodium shows the same reports as you type. What matters is that a clean report is part of "done".

#### [day1#check-optional-return] The checker rejects this line. What is the right repair?

*Checkpoint*

**Question:** `highest(lines)` is annotated `-> float | None`. A colleague writes `peak = highest(lines) * 1.1` and the checker reports that `None` does not support `*`.

- A. Keep the result in a name, test it `is None` first, then multiply
- B. Add `# type: ignore` to the line, since the files are never empty in practice
- C. Change the hint of `highest` to `-> float`
- D. Write `if not highest(lines)` and return early

#### [day1#lab-1-3] Annotate the reading parser

Lab 1.3 · 25 min

Annotate the supplied reading parser and fix every error the type checker reports.

[D1_3_annotate_supplied_reading.html](https://sdaiaacademy.github.io/fn-101/labs/D1_3_annotate_supplied_reading.html)

- [ ] Run the tests and the checker on the supplied parser (4 min)
- [ ] Annotate every function (7 min)
- [ ] Fix each error the checker reports (10 min)
- [ ] Run the tests, the strict check and the lab check (4 min)
- [ ] ✱ Stretch: Replace the tuple with a NamedTuple so that reading[2] becomes reading.m3

### Session 4: Parsons problems

#### [day1#s4] Parsons problems

*Session 4*

- Order the lines of a function so that each name is bound before it is used
- Use indentation to say which lines belong to a branch, a loop or a try
- Reject a distractor by saying what it would do

#### [day1#what-is-a-parsons-problem] All the lines are given, scrambled. You decide order and indentation.

*Parsons problems*

```python
# file: scrambled
return total
if value >= 0:
total = value
def total_valid(values):
total += value
for value in values:
total = 0.0
```

- No syntax to recall: every character you need is on the page
- What is left is the **structure**: what runs first, what is inside what
- One line is a **distractor**: it looks right and does not belong

> **Why practise this.** It is the skill between reading and writing, and it is one part of the supervised check.

#### [day1#bind-before-use] A line can run only after the lines that bind the names it reads

*Rule 1*

1. **text = row[…].strip()** needs `row`, a parameter
2. **value = float(text)** needs `text`
3. **if value < 0 or value > 200:** needs `value`

- For each line, list the names it **reads**; find the line that **binds** each
- That gives you chains like this one before you think about meaning at all
- Run a line too early and Python says `NameError: name 'value' is not defined`

#### [day1#indentation-is-structure] Indentation says what belongs to what, and one level changes the answer

*Rule 2*

```python
# file: right
for value in values:
    if value >= 0:
        total += value
return total
```

```python
# file: one level off
for value in values:
    if value >= 0:
        total += value
    return total
```

- Left: return after the loop, the sum of all valid values
- Right: return **inside** the loop, so the function ends after the first value
- Both are valid Python. Only a test, or a trace, tells them apart

#### [day1#guard-clauses-first] Reject each bad case early; what reaches the last line is good

*The shape of a validation function*

```python
# file: validate.py
def validate_reading(row, known):
    text = row["consumption_m3"].strip()
    if text == "":
        return "MISSING_VALUE"
    ...
    if row["meter_id"] not in known:
        return "UNKNOWN_METER"
    return ""
```

- Each `if` guards one `return` with one reason
- The order of the guards is part of the specification
- The final line is not indented under any `if`

> **Pair them up.** In a scrambled validation function, match every `if` with its `return` first. Half the puzzle is done.

#### [day1#try-wraps-one-line] try wraps the one line that can fail; except names that failure

*Where the try goes*

```python
# file: validate.py
try:
    value = float(text)
except ValueError:
    return "NOT_A_NUMBER"
```

- `float("N/A")` raises **ValueError**
- `except TypeError:` would catch nothing here: the error passes through and the function crashes
- `except:` alone would catch everything, including your own typing mistakes

> **Name the exception you expect.** You find its name by trying the failing call once and reading the last line of what Python prints.

#### [day1#distractors-look-alike] Decide between two lines that look alike by running one concrete row in your head

*Distractors*

| The row has | `if value < 0 or value > 200:` | `if value < 0 and value > 200:` |
| --- | --- | --- |
| `"250"` | False or True: **rejected** | False and True: accepted |
| `"-0.5"` | True or False: **rejected** | True and False: accepted |
| `"0.742"` | accepted | accepted |

> **No number is below 0 and above 200 at once.** The second line never rejects anything. You see it in ten seconds with one value; you may not see it in ten minutes of staring.

#### [day1#from-lines-to-writing] The same three questions build a function when no lines are given

*From reading to writing*

- **1 · What is the contract?** Inputs, output, and the cases in words. Session 2.
- **2 · What must exist first?** The chain of names: load, then convert, then compare. Today's rule 1.
- **3 · What is inside what?** Which lines belong to the loop, the branch, the try. Today's rule 2.

> **From tomorrow you write.** Every lab still starts from a supplied state and a set of tests that say what "right" means.

#### [day1#check-parsons-order] Where does the last line of the function go?

*Checkpoint*

**Question:** A function counts the good rows. Placed so far: `count = 0`, the `for` line, the `if` line, `count += 1`. Left: `return count`. A test shows it returns 1 for 30 good rows.

- A. Directly under `count = 0`, before the loop
- B. Under `count += 1`, at the same depth
- C. Under the `if` line, at the depth of the `if`
- D. After the loop, at the depth of the `for` line

#### [day1#lab-1-4] Rebuild a validation function

Lab 1.4 · 25 min

Reorder scrambled lines, with distractors, into a working validation function.

[D1_4_reorder_scrambled_lines.html](https://sdaiaacademy.github.io/fn-101/labs/D1_4_reorder_scrambled_lines.html)

- [ ] Order the warm-up on paper, then in the editor (6 min)
- [ ] Order and indent the validation function (11 min)
- [ ] Run the tests; fix order or indentation (4 min)
- [ ] Say why each distractor is wrong; check (4 min)
- [ ] ✱ Stretch: Write one more distractor for a neighbour and say which test catches it

#### [day1#wrap-up] Three things to keep

*Day 1 · wrap-up*

- **One object, many names.** Assignment and calls never copy. Mutation is seen through every name; rebinding through one.
- **A function is a contract.** In through parameters, out through return, effects at the edge. Hints make the contract checkable.
- **Give the line an input.** To judge a line, a distractor or a suggestion, run one concrete value through it by hand.

#### [day1#next] Day 2: Collections for data work

*Next*

Finish any lab at home from its own folder; each one starts from a supplied state. Tomorrow opens with drill 2, on lists and dictionaries that share their contents.

## Day 2: Collections for data work

Dictionaries, sets, comprehensions, generators and data classes on a month of readings and a ticket queue

#### [day2#title] Collections for data work

*SDAIA Academy · Python for Data and AI Work*

Day 2: Dictionaries, sets, comprehensions, generators and data classes on a month of readings and a ticket queue

Data & AI Foundations Track · 4 teaching days + capstone day · 4 sessions · 4 labs · FN-101

#### [day2#drill-2] Lists and dictionaries that share · 10 minutes

*Drill 2 · AI off*

Five snippets on paper: `labs/drills/day2.md`. No computer, no assistant. Write what each prints.

#### [day2#review-day1] One list or two?

*Review of Day 1*

**Question:** A function `clean(rows)` runs `rows.sort()` and returns `rows[:10]`. A caller writes `top = clean(month)`. Afterwards, what is true of `month`?

- A. It is unchanged: the function worked on its own copy
- B. It is sorted, and still has all its rows
- C. It is sorted and cut to ten rows
- D. It is the same object as `top`

#### [day2#agenda] Collections for data work

*Today*

- **Session 1 · Dictionaries for counting and grouping**: A dictionary as an index: counting, grouping, and why one lookup replaces a loop
- **Session 2 · Sets and membership**: Sets answer membership and difference questions directly: what is missing, what is unknown, what repeats
- **Session 3 · Comprehensions and generators**: Comprehensions build a collection in one expression; generators hand over one item at a time and keep memory flat
- **Session 4 · Records as data classes**: A data class gives a record named, typed fields; sorting with a key puts a queue in working order

### Session 1: Dictionaries for counting and grouping

#### [day2#s1] Dictionaries for counting and grouping

*Session 1*

- Count and group records with a dictionary in one pass
- Build an index from a key to a record and use it in place of a search
- Explain why a loop inside a loop is slow on 100,000 rows, and measure it

#### [day2#dict-is-an-index] A dictionary answers "what belongs to this key?" in one step

*Dictionaries*

```python
# file: index.py
district_of = {
    "M-0001": "Al-Rabwa",
    "M-0002": "Al-Yasmin",
}
print(district_of["M-0002"])
print("M-9001" in district_of)
```

- Each **key** appears once and leads to one **value**
- Looking up a key does not search: it goes straight there
- `in` asks whether a key exists, without raising an error
- Keys keep the order in which they were added

> **Think "index", like the back of a book.** You do not read the book to find a word; you look the word up.

#### [day2#counting-pattern] Counting: one pass, one dictionary, get with a default

*Pattern 1*

```python
# file: count.py
counts: dict[str, int] = {}
for reading in readings:
    meter_id = reading["meter_id"]
    counts[meter_id] = counts.get(meter_id, 0) + 1
```

- `counts.get(key, 0)`: the count so far, or 0 for a key not seen yet
- `counts[key] += 1` alone raises `KeyError` on the first reading of a meter
- `collections.Counter(…)` is this loop, ready made

- **On the month.** 588 meters have readings in the clean file; M-0001 has 30, one per day of September (lab 2.1).

#### [day2#grouping-pattern] Grouping: the value is a list, and each record joins the list of its key

*Pattern 2*

```python
# file: group.py
by_meter: dict[str, list[float]] = {}
for reading in readings:
    value = float(reading["consumption_m3"])
    meter_id = reading["meter_id"]
    by_meter.setdefault(meter_id, []).append(value)
```

- `setdefault(key, [])` returns the list of the key, creating an empty one the first time
- After the loop, `by_meter["M-0042"]` is that meter's whole month
- This is how Miqyas finds each meter's median before it looks for anomalies

> **What goes wrong.** `dict.fromkeys(ids, [])` gives every key the **same** list. Yesterday's aliasing, in a dictionary.

#### [day2#index-then-lookup] To combine two files, index one of them and look up from the other

*Pattern 3*

1. **1 · Index** meters.csv becomes meter id → district, once
2. **2 · Walk** each reading, one after another
3. **3 · Look up** the district of its meter, in one step

```python
# file: count.py
district_of = {m["meter_id"]: m["district"] for m in meters}
for reading in readings:
    district = district_of[reading["meter_id"]]
```

#### [day2#nested-loop-cost] The same counts, a hundred times slower: a loop inside a loop

*From the lab's run*

- **2.3 s** nested loop: for each of 100,000 readings, search 600 meters
- **0.024 s** dictionary: index 600 meters once, then one lookup per reading
- **300** comparisons per reading, on average, in the nested version

> **It gets worse with size.** Ten times the meters makes the nested version ten times slower again. The dictionary version hardly notices.

#### [day2#why-lookup-is-fast] The key itself says where its value is stored

*Why one step*

- Python turns the key into a number, its **hash**, and uses it as an address
- So finding a key costs about the same in 600 entries as in 600,000
- The price: a key must never change. Text, numbers and tuples can be keys; lists and dictionaries cannot

```python
# file: at a prompt
>>> {["M-0001", "2026-09-01"]: 0.7}
TypeError: unhashable type: 'list'
>>> {("M-0001", "2026-09-01"): 0.7}
{('M-0001', '2026-09-01'): 0.7}
```

#### [day2#missing-keys] Three ways to ask for a key, and they fail differently on purpose

*When the key is not there*

| You write | Key missing | Use it when |
| --- | --- | --- |
| `district_of[meter_id]` | raises `KeyError` | a missing key is a fault you want to hear about |
| `district_of.get(meter_id)` | gives `None` | missing is normal and you handle `None` next |
| `meter_id in district_of` | gives `False` | you only need to know |

> **At Manahil.** Twenty rows of the month carry a meter id that is not in the registry. A loud `KeyError` finds them; a quiet `get` with a default district would hide them in a total.

#### [day2#check-index-outside-loop] Why is this version still slow?

*Checkpoint*

**Question:** A colleague replaces the nested loop. Inside `for reading in readings:` the first line is now `district_of = {m["meter_id"]: m["district"] for m in meters}`, then a lookup. The counts are right; 100,000 rows still take seconds.

- A. The index is rebuilt for every reading, which walks all the meters each time
- B. Dictionary lookups are slow when the dictionary has 600 keys
- C. Comprehensions are slower than loops
- D. 100,000 rows are too many for a Python loop

#### [day2#lab-2-1] Count readings per meter and district

Lab 2.1 · 25 min

Count readings per meter and district, then time a nested-loop version on 100,000 rows.

[D2_1_count_readings_per.html](https://sdaiaacademy.github.io/fn-101/labs/D2_1_count_readings_per.html)

- [ ] Count the readings of each meter in one pass (7 min)
- [ ] Build an index of meters; count per district (8 min)
- [ ] Time both versions on 100,000 rows (6 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Group the readings by district into lists of values and print each district's highest reading

### Session 2: Sets and membership

#### [day2#s2] Sets and membership

*Session 2*

- Answer a membership question with a set in place of a search through a list
- Compare two collections with difference and intersection
- Use a tuple as a key to find repeated records

#### [day2#set-is-membership] A set holds each value once and answers "is it in there?" in one step

*Sets*

```python
# file: known.py
known = {m["meter_id"] for m in meters}
print(len(known))             # 600
print("M-0042" in known)      # True
print("M-9001" in known)      # False
```

- A set is a dictionary with keys and no values
- `x in a_list` walks the list; `x in a_set` goes straight to the answer
- No order, no positions, no repeats: only membership

> **You have used one already.** Yesterday's `validate_reading(row, known)` took the registry as a set, for exactly this question.

#### [day2#set-algebra] Three operators answer what is missing, what is extra and what is shared

*Comparing two collections*

| Expression | Reads as | At Manahil |
| --- | --- | --- |
| `registered` | ids in the registry | 600 |
| `reporting` | ids that appear in the month's readings | 593 |
| `registered - reporting` | registered and silent | 12 |
| `reporting - registered` | reporting and unknown | 5 |
| `registered & reporting` | in both | 588 |
| `registered \| reporting` | in either | 605 |

#### [day2#two-findings-two-owners] The same operator, two different problems, two different owners

*What the two differences mean*

- **12 meters sent nothing.** Registered, and not one row in September. A dead meter, an empty house, a reader that never synchronised. A question for **the field team**.
- **5 ids are unknown.** M-9001 to M-9005, four rows each. A registry that is behind, or a mistyped id. A problem in **the data**, and those 20 rows cannot be billed to anyone.

> **A check that finds something must say who acts on it.** Miqyas rejects the 20 rows with the reason UNKNOWN_METER; the silent meters go into a list for the field team.

#### [day2#dedup-and-order] A set drops repeats and forgets order: sort before you show it

*What a set gives up*

```python
# file: at a prompt
>>> ids = ["M-0002", "M-0001", "M-0002"]
>>> set(ids)
{'M-0002', 'M-0001'}
>>> sorted(set(ids))
['M-0001', 'M-0002']
```

- `set(a_list)` is the shortest way to drop repeats
- The order you see printed is not promised, and can differ between runs
- `sorted(…)` turns any collection into a list in a fixed order

> **A report must be the same on two runs.** Anything that leaves your function for a file or a screen goes through `sorted` first.

#### [day2#seen-set-pattern] Finding repeats: remember what you have seen, as a set of tuples

*Pattern*

```python
# file: coverage_report.py
seen: set[tuple[str, str]] = set()
repeated: set[tuple[str, str]] = set()
for reading in readings:
    key = (reading["meter_id"], reading["date"])
    if key in seen:
        repeated.add(key)
    seen.add(key)
```

- The identity of a reading is the **pair**: this meter, this date
- A tuple cannot change, so it can be a member of a set
- `set()` makes an empty set; `{}` is an empty dictionary

- **On the month.** 30 pairs appear more than once. Miqyas keeps the first row of each and rejects the repeat as DUPLICATE.

#### [day2#choosing-a-collection] Choose the collection by the question you will ask of it

*Four collections*

| You will ask | Use | Example |
| --- | --- | --- |
| what is at position 3? what comes next? | `list` | the rows of a file, in file order |
| what belongs to this key? | `dict` | meter id → district; district → count |
| is it in there? what differs? | `set` | the known meter ids |
| a few values that travel together and never change | `tuple` | (meter id, date) |

> **Changing your mind is cheap.** `set(a_list)`, `sorted(a_set)`, `list(a_dict)`, `dict(pairs)` convert in one call.

#### [day2#check-set-difference] Which expression finds them?

*Checkpoint*

**Question:** Badr has the set `ticketed` (meter ids named in open tickets) and Salma the set `flagged` (meter ids with an anomaly). They want the meters that have an anomaly and **no** open ticket, to call those customers first.

- A. ticketed & flagged
- B. ticketed - flagged
- C. ticketed | flagged
- D. flagged - ticketed

#### [day2#lab-2-2] Find silent meters and unknown ids

Lab 2.2 · 25 min

Find meters with no reading and readings with no known meter.

[D2_2_find_meters_no.html](https://sdaiaacademy.github.io/fn-101/labs/D2_2_find_meters_no.html)

- [ ] Build the two sets of meter ids (5 min)
- [ ] Find the meters with no reading (5 min)
- [ ] Find the readings with no known meter (5 min)
- [ ] Find the repeated meter and date pairs (6 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: List the meters that have fewer than 30 different dates, with the number of dates each has

### Session 3: Comprehensions and generators

#### [day2#s3] Comprehensions and generators

*Session 3*

- Write list, dictionary and set comprehensions with a filter
- Write a generator function that yields records while a file is read
- Compare the peak memory of a list and of a stream, and say when each fits

#### [day2#comprehension-forms] A comprehension builds a collection in one expression: what, from where, which

*Comprehensions*

```python
# file: forms.py
values = [float(r["consumption_m3"]) for r in rows]                 # a list
high = [v for v in values if v > 5.0]                               # with a filter
known = {m["meter_id"] for m in meters}                             # a set
district_of = {m["meter_id"]: m["district"] for m in meters}        # a dictionary
```

- **What.** The expression at the front: one item of the result.
- **From where.** `for … in …`: the same line as in a loop.
- **Which.** An optional `if` at the end keeps only some.

#### [day2#when-a-loop-reads-better] One expression and one condition fit a comprehension; anything more wants a loop

*Judgement*

- **Comprehension.** Transform each item, or keep some. The reader sees the whole idea on one line.
- **Loop.** Counting and grouping, a `try` around each item, two results at once, an early exit, or a line that no longer fits on the screen.

```python
# file: too much
ok = [float(r["consumption_m3"]) for r in rows if r["consumption_m3"].strip() != ""
      and r["meter_id"] in known and 0 <= float(r["consumption_m3"]) <= 200]
```

> **What goes wrong.** The line above converts twice, crashes on `N/A`, and cannot say why a row was left out.

#### [day2#generator-function] A function with yield hands over one value, then waits to be asked again

*Generators*

```python
# file: stream.py
def read_values(path):
    with open(path, encoding="utf-8",
              newline="") as file:
        for row in csv.DictReader(file):
            yield float(row["consumption_m3"])
```

- `return` ends a function; `yield` **pauses** it, with all its names kept
- The next request resumes it on the line after the `yield`
- At any moment, one row exists. The file stays open until the loop is done

#### [day2#lazy-nothing-runs] Calling a generator function runs nothing: the work happens when values are asked for

*Laziness*

- call: `values = read_values("data/readings_large.csv")` no file is opened yet
- next(values): opens the file, reads one row, gives `0.606` and pauses
- next(values): reads one more row, gives `0.544` and pauses
- sum(values): asks again and again until the file ends: the total of everything **left**

> **`for` and `sum` ask for you.** You rarely write `next`; every loop over a generator is this conversation.

#### [day2#memory-list-vs-stream] The same total of 100,000 rows, with two hundred times less memory

*From the lab's run*

| Item | Value |
| --- | --- |
| List of all rows | 35,900 KiB |
| Stream, one row at a time | 160 KiB |

- Both give **137,769.165** cubic metres
- A file ten times as long: the list needs ten times the memory, the stream the same 160 KiB
- A year of every meter's hourly readings does not fit in a list on a laptop. It does fit in a stream

#### [day2#one-pass-only] A generator can be walked once. Then it is empty.

*The price*

```python
# file: at a prompt
>>> values = read_values(path)
>>> sum(values)
137769.165
>>> sum(values)
0
>>> len(values)
TypeError: object of type 'generator' has no len()
```

- No length, no positions, no second pass
- Need two results? Compute both in **one** loop, or call the function again for a fresh generator
- Need to sort, or to find a median? You need all the values: use a list

> **The silent zero.** A second pass does not raise an error. It quietly gives the result for no data.

#### [day2#generator-expression] Round brackets make a comprehension lazy

*The short form*

```python
# file: two ways
total = sum([float(r["consumption_m3"])
             for r in rows])

total = sum(float(r["consumption_m3"])
            for r in rows)
```

- First: build a list of 100,000 numbers, add them, throw the list away
- Second: hand each number to `sum` as it is made
- Works with `sum`, `max`, `min`, `any`, `all`, `sorted`, `set`

#### [day2#check-generator-twice] What does the report show?

*Checkpoint*

**Question:** A script does `values = read_values(path)`, then `highest = max(values)`, then `total = sum(values)`, and prints both. The file holds 100,000 good readings.

- A. The right highest value and the right total
- B. The right highest value, then an error on the second line
- C. The right highest value and a total of 0
- D. A highest value of 0 and the right total

#### [day2#lab-2-3] Stream a large readings file

Lab 2.3 · 25 min

Stream a large readings file with a generator and compare peak memory with a list.

[D2_3_stream_large_readings.html](https://sdaiaacademy.github.io/fn-101/labs/D2_3_stream_large_readings.html)

- [ ] Run the list version and read how it works (4 min)
- [ ] Write the generator that yields one value per row (8 min)
- [ ] Add up the stream; compare the two totals (4 min)
- [ ] Measure both peaks of memory (5 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Use the generator twice in a row and explain what the second pass returns

### Session 4: Records as data classes

#### [day2#s4] Records as data classes

*Session 4*

- Model a record as a frozen data class with typed fields and a method
- Sort records by several fields with a key function that returns a tuple
- Leave out of a record the personal data the task does not need

#### [day2#dict-records-fail-late] A dictionary as a record accepts any mistake until the line that uses it

*Records*

```python
# file: queue.py
ticket = json.loads(line)
ticket["priorty"] = "urgent"
if ticket["opened"] < "2026-09-01":
    ...
```

- Line 2 misspells the field and **adds a new key**. No error, ever
- Line 3 compares dates as text. It works only while every file writes year-month-day
- Nothing says which fields a ticket has, or what type each is
- The checker sees `dict[str, str]` and can help with none of it

#### [day2#dataclass-basics] A data class is a record with named, typed fields, written in six lines

*Data classes*

```python
# file: tickets.py
@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    opened: date
    district: str
    priority: str
    status: str
    text: str
```

- The decorator writes the constructor, a readable printout and `==` for you
- `Ticket(ticket_id="T-20001", opened=…)` builds one; `t.priority` reads a field
- A misspelt field is an `AttributeError` at run time and an error from the checker before

#### [day2#frozen-records] frozen=True makes a record that nobody can change behind your back

*Frozen*

```python
# file: at a prompt
>>> t.priority = "low"
dataclasses.FrozenInstanceError:
    cannot assign to field 'priority'
>>> urgent = replace(t, priority="urgent")
```

- Yesterday: a shared mutable object changes for every name that holds it
- A frozen record can be shared freely: there is nothing to mutate
- A "change" makes a new record with `dataclasses.replace`, like `upper()` on a string
- Frozen records can be keys of a dictionary and members of a set

#### [day2#methods-on-records] A method is a function that lives with the data it needs

*Behaviour that belongs to the record*

```python
# file: tickets.py
    def age_days(self, today: date) -> int:
        """Whole days from the day the
        ticket was opened to today."""
        return (today - self.opened).days
```

- `self` is the record the method was called on: `t.age_days(today)`
- `today` comes in as a parameter. A method that asked the clock would give a different answer tomorrow, and could not be tested
- `opened` is a `date`, so subtraction gives days. As text it would give an error

- **On the queue.** The oldest open urgent ticket, T-20087, is 41 days old on the course's "today", 1 October 2026 (lab 2.4).

#### [day2#sort-with-key] sorted needs to know what to compare: give it a key function

*Sorting*

```python
# file: sorting.py
RANK = {"urgent": 0, "high": 1,
        "normal": 2, "low": 3}

by_text = sorted(tickets,
                 key=lambda t: t.priority)
by_rank = sorted(tickets,
                 key=lambda t: RANK[t.priority])
```

- The key function is called once per item; items are ordered by what it returns
- By text: high, low, normal, urgent. Alphabetical, and useless
- By rank: urgent first, because 0 is the smallest
- `lambda t: …` is a function small enough to write in place

#### [day2#tuple-keys-multi-sort] A key that returns a tuple sorts by the first item, then the second, then the third

*Sorting by several fields*

```python
# file: tickets.py
sorted(waiting, key=lambda t: (PRIORITY_RANK[t.priority], t.opened, t.ticket_id))
```

| Ticket | Rank | Opened | Age in days | District |
| --- | --- | --- | --- | --- |
| T-20087 | 0 urgent | 2026-08-21 | 41 | Al-Yasmin |
| T-20274 | 0 urgent | 2026-08-24 | 38 | Al-Naseem |
| T-20066 | 0 urgent | 2026-08-25 | 37 | Al-Khuzama |
| T-20196 | 0 urgent | 2026-08-26 | 36 | Al-Naseem |

> **The last item breaks ties.** Two urgent tickets of the same day would otherwise come out in file order; the ticket id makes the queue the same on every run.

#### [day2#carry-only-what-you-need] A record carries only the fields the task needs

*Responsible use*

- **In the file.** Ten fields per ticket, among them a phone number and an identity number: personal data.
- **In `Ticket`.** Six fields. The queue is ordered by priority and age; it needs to call nobody and identify nobody.

- What is never copied into the record cannot be printed, logged or written by mistake
- The free **text** of a ticket can hold a phone number too. Tomorrow's first lab masks it before anything is written

> **The data here is synthetic.** The habit is real: Abdulaziz, the data protection officer, reads your output files, not your intentions.

#### [day2#check-sort-key] Which key puts the queue in working order?

*Checkpoint*

**Question:** Customer care works the most urgent tickets first and, within a priority, the oldest first. `RANK` gives urgent 0 and low 3. Which call is right?

- A. sorted(waiting, key=lambda t: (t.priority, t.opened))
- B. sorted(waiting, key=lambda t: (RANK[t.priority], t.opened))
- C. sorted(waiting, key=lambda t: (RANK[t.priority], t.opened), reverse=True)
- D. sorted(waiting, key=lambda t: (t.opened, RANK[t.priority]))

#### [day2#lab-2-4] Model and sort the ticket queue

Lab 2.4 · 25 min

Model a ticket as a data class and sort tickets by priority and age.

[D2_4_model_ticket_as.html](https://sdaiaacademy.github.io/fn-101/labs/D2_4_model_ticket_as.html)

- [ ] Define the frozen data class and its age method (8 min)
- [ ] Build tickets from the lines of the file (6 min)
- [ ] Sort the open tickets by priority, then age (7 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Count the open tickets per district and priority with a dictionary whose keys are tuples

#### [day2#wrap-up] Three things to keep

*Day 2 · wrap-up*

- **Choose by the question.** A dictionary for "what belongs to this key", a set for "is it in there", a list for order. One lookup replaces a loop.
- **Stream what you use once.** A generator keeps memory flat and can be walked once. Sort, median and second passes need a list.
- **Records have names and types.** A frozen data class with only the fields the task needs; a tuple key puts them in order.

#### [day2#next] Day 3: Files, text and failure

*Next*

Tomorrow the files stop being clean: wrong encodings, broken lines, and two defects planted in the code. Drill 3 is a traceback to read on paper.

## Day 3: Files, text and failure

Reading and writing CSV and JSON Lines, bytes and encodings, exceptions that give a reason, and a method for debugging

#### [day3#title] Files, text and failure

*SDAIA Academy · Python for Data and AI Work*

Day 3: Reading and writing CSV and JSON Lines, bytes and encodings, exceptions that give a reason, and a method for debugging

Data & AI Foundations Track · 4 teaching days + capstone day · 4 sessions · 4 labs · FN-101

#### [day3#drill-3] Read a traceback · 10 minutes

*Drill 3 · AI off*

One program, the traceback it ended with, five questions: `labs/drills/day3.md`. On paper, no computer, no assistant.

#### [day3#review-day2] Which collection answers the question?

*Review of Day 2*

**Question:** For each of 17,690 rows you must decide whether its meter id is one of the 600 registered ids. Which choice keeps the whole job to one pass with one step per row?

- A. A list of the registered ids, tested with `in`
- B. A sorted list of the registered ids, tested with `in`
- C. A set of the registered ids, tested with `in`
- D. A generator of the registered ids, tested with `in`

#### [day3#agenda] Files, text and failure

*Today*

- **Session 1 · CSV and JSON Lines**: Reading CSV and JSON Lines with the standard library, writing JSON that reruns the same, and keeping personal data out of every output
- **Session 2 · Text, bytes and encodings**: Text is bytes plus an encoding: UTF-8, the default that open uses, decoding errors, and why ignoring them is not a repair
- **Session 3 · Exceptions that explain**: Raising early with a specific exception, an exception of your own that carries a reason code, and a loop that accounts for every line
- **Session 4 · A debugging method**: Six steps that turn a symptom into a fix that stays fixed: reproduce, shrink, hypothesis, test, fix, regression

### Session 1: CSV and JSON Lines

#### [day3#s1] CSV and JSON Lines

*Session 1*

- Read a CSV file and a JSON Lines file with the encoding and newline handling named
- Write JSON output that is the same on every run and keeps Arabic readable
- Mask personal data before anything is written, printed or logged

#### [day3#open-with-names] Three things to say every time you open a text file

*Opening a file*

```python
# file: load.py
with open(path, encoding="utf-8",
          newline="") as file:
    rows = list(csv.DictReader(file))
```

- `with`: the file is closed when the block ends, also when an error happens inside it
- `encoding="utf-8"`: you decide how bytes become text, not the machine you happen to be on
- `newline=""`: for CSV, let the csv module handle line ends, so that a line break inside a quoted cell survives

> **What goes wrong.** Leave the encoding out and the same script reads Arabic on one laptop and crashes on the next. Session 2 shows it.

#### [day3#csv-everything-is-text] A CSV reader hands you text for every cell. Numbers and dates are your job.

*CSV*

```python
# file: at a prompt
>>> row = rows[0]
>>> row
{'meter_id': 'M-0001', 'date': '2026-09-01',
 'consumption_m3': '5.399'}
>>> row["consumption_m3"] * 2
'5.3995.399'
```

- `csv.DictReader` uses the header line as keys: one `dict[str, str]` per row
- CSV has no types. `'5.399'` is five characters until you call `float`
- Convert in one place, at the door, and reject there what will not convert

#### [day3#csv-is-not-split] A comma inside a cell is why line.split(",") is not a CSV reader

*Why a module, not split*

```text
# file: readings_2026_09.csv
meter_id,date,consumption_m3
M-0001,2026-09-01,5.399
M-0580,2026-09-01,"0,361"
```

|  | Third row gives |
| --- | --- |
| `line.split(",")` | four pieces: `"0` and `361"` apart |
| `csv.DictReader` | three cells; the value is `0,361` |

- A spreadsheet set to a comma as the decimal mark writes numbers this way, in quotes
- The month file has 7 such cells. The reader gets them whole; `float` then refuses them, and they are rejected as NOT_A_NUMBER with the text in the detail

#### [day3#json-lines] JSON Lines is one JSON value per line: a file you can read one record at a time

*JSON Lines*

```python
# file: load.py
with open(path, encoding="utf-8") as file:
    for line in file:
        ticket = json.loads(line)
```

- Each line stands alone: a broken line spoils one record, not the file
- Records can be appended, and streamed with a generator
- Unlike CSV, a value has a type: text, number, true or false, null, list, object

- **At Manahil.** Each of the 400 tickets is one line with ten fields. The free text is Arabic, English or both in one sentence.

#### [day3#write-reproducible] Write output that is the same bytes on every run, and that a person can read

*Writing*

```python
# file: summary.py
with open(path, "w", encoding="utf-8",
          newline="\n") as file:
    json.dump(summary, file,
              ensure_ascii=False, indent=2)
    file.write("\n")
```

- `ensure_ascii=False`: Arabic is written as Arabic, not as escapes such as `ا`
- `indent=2`: one field per line, so that two versions can be compared
- Keys in a fixed order: build the dictionary from `sorted` names
- No clock time inside the file: put that in the log

> **Same input, same bytes.** Then "did anything change?" is answered by comparing two files, and Day 4's tool can prove it reruns.

#### [day3#tickets-are-personal-data] A ticket is personal data in three places, and the third is easy to miss

*Responsible use*

- **The phone field.** Every ticket has one. Callbacks need to recognise it, not to show it: the last two digits are enough.
- **The identity field.** No report needs it. It is never copied out of the input.
- **The free text.** "Call me on 05…": 14 of the 400 texts hold a phone number the customer typed in.

> **Mask before anything is written, printed or logged.** A debug print of one ticket is a leak with a shorter name.

#### [day3#mask-before-write] A pattern that looks right finds 9 of the 14 phone numbers

*From the lab's run*

| Pattern | Found |
| --- | --- |
| `\+?[0-9]{9,}` | 9 of 14 |
| `\+?\d{9,}` | 14 of 14 |

- Five customers typed their number in Arabic-Indic digits: ٠٥٥…
- In Python, `\d` matches a digit of any script; `[0-9]` matches ten characters only
- You find this by counting what the mask caught, not by reading the pattern

> **Test a mask on the data it must protect.** Then have someone else search the output for what should not be there.

#### [day3#check-mask-where] Where does the masking go?

*Checkpoint*

**Question:** A script loads tickets, logs each ticket it processes "for debugging", builds a summary and writes it to a file. The phone numbers must not leave the program. Where is masking applied?

- A. In the function that writes the summary file
- B. Where each ticket line is first turned into a record
- C. In a second script that cleans the summary file afterwards
- D. Nowhere, if the file is only sent to colleagues

#### [day3#lab-3-1] Write a district summary with phones masked

Lab 3.1 · 25 min

Load readings and tickets and write a JSON summary per district, masking phone numbers before anything is written.

[D3_1_load_readings_tickets.html](https://sdaiaacademy.github.io/fn-101/labs/D3_1_load_readings_tickets.html)

- [ ] Load the two CSV files and the JSON Lines file (7 min)
- [ ] Mask the phone field and the phone numbers in text (8 min)
- [ ] Write the summary as JSON; read it as a reviewer (6 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Change the pattern to [0-9] and count the phone numbers that now slip through; say why

### Session 2: Text, bytes and encodings

#### [day3#s2] Text, bytes and encodings

*Session 2*

- Explain the difference between bytes and text, and what an encoding does
- Read a UnicodeDecodeError: the codec, the byte and the position
- Decode a file line by line and report the lines that fail instead of ignoring them

#### [day3#bytes-and-text] A file holds bytes. Text appears only when an encoding is applied.

*Bytes and text*

| The word عداد (meter) | Bytes |
| --- | --- |
| in UTF-8 | `d8 b9 d8 af d8 a7 d8 af` |
| in Windows-1256 | `da cf c7 cf` |

- **Text** (`str`) is a sequence of characters: 4 here
- **Bytes** are numbers from 0 to 255: 8 here, or 4
- An **encoding** is the table between the two. `encode` goes to bytes, `decode` comes back

> **The bytes do not say which table wrote them.** Someone has to tell you, or you have to find out.

#### [day3#utf8-in-one-slide] UTF-8 covers every script and is the encoding to write, always

*UTF-8*

- **One byte.** English letters, digits, punctuation: the same bytes as ASCII. `M-0042` is six bytes.
- **Two bytes.** Each Arabic letter. The letter ف is `d9 81`.
- **Not every byte order is valid.** A decoder can tell when bytes are **not** UTF-8. That is a feature: wrong input fails loudly.

- Older systems wrote one byte per Arabic letter (Windows-1256). Their files are still arriving
- Read what you are given, with the encoding it was written in. Write UTF-8

#### [day3#default-encoding-trap] open(path) without an encoding uses whatever the machine prefers

*The trap*

```python
# file: decode.py
with open(path) as file:        # which encoding?
    return [json.loads(line) for line in file]
```

- On many Windows laptops the default is a one-byte Western table (cp1252)
- On most servers and in notebooks in the cloud it is UTF-8
- So the same script works in one place and fails in the other, on the same file

> **This is changing.** PEP 686 makes UTF-8 the default from Python 3.15. Until every machine you meet runs it, and for every file that is not UTF-8, name the encoding.

#### [day3#read-a-decode-error] A decode error names the codec, the byte and the position. Use all three.

*Reading the error*

```text
# file: uv run python decode.py
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 131:
    character maps to <undefined>
```

- **The codec.** "charmap": a one-byte table was decoding. Nobody chose it; it was the default.
- **The byte.** `0x81` has no character in that table. In UTF-8 it is the second half of ف.
- **The position.** Byte 131 of what was being decoded: where to look in the file.

#### [day3#mojibake] The wrong one-byte table raises nothing and gives you the wrong text

*The quiet failure*

| The UTF-8 bytes of عداد, decoded as | Result | Error? |
| --- | --- | --- |
| UTF-8 | عداد | no |
| Windows-1256 | ط¹ط¯ط§ط¯ | no |
| cp1252, errors replaced | Ø¹Ø¯Ø§Ø¯ | no |

> **"It opened without an error" is not "it was decoded correctly".** Text like the second and third rows, in a report or a database, means a file was read with the wrong table somewhere upstream.

#### [day3#never-ignore] errors="ignore" makes the error go away by deleting the customer's words

*The tempting repair*

| Line 12 of the branch file, decoded as UTF-8 with | The text of the ticket becomes |
| --- | --- |
| `errors="strict"` (the default) | a `UnicodeDecodeError`: you are told |
| `errors="ignore"` | a few spaces, one stray letter and M-0365 |
| `errors="replace"` | rows of � marks and M-0365 |
| the encoding it was written in (Windows-1256) | الفاتورة مرتفعة جدا هذا الشهر، أرجو مراجعة قراءة العداد M-0365 |

> **Fail loudly, then report.** Decode strictly, catch the error per line, and list the lines that fail with the byte that stopped you. Then someone can decide.

#### [day3#line-by-line-report] Decode each line by itself, so that one bad line cannot hide the rest

*The method*

```python
# file: decode.py
data = Path(path).read_bytes()
for line_no, raw in enumerate(
        data.splitlines(), start=1):
    try:
        decoded.append(raw.decode(encoding))
    except UnicodeDecodeError as problem:
        failed.append(...)
```

**113 + 7** lines decoded and lines reported: all 120 accounted for

Lines 12, 22, 37, 55, 82, 84 and 94 fail, each at an Arabic letter written in Windows-1256.

#### [day3#check-decode-choice] The export fails on a few lines. What do you do?

*Checkpoint*

**Question:** A nightly file of 50,000 tickets is declared UTF-8. Tonight the load stops with a `UnicodeDecodeError` at one byte. Badr needs the queue in the morning.

- A. Add `errors="ignore"` so that the load finishes
- B. Switch the whole file to Windows-1256, which never raises
- C. Refuse the file until the sender fixes it
- D. Load the lines that decode; report the rest by line and byte

#### [day3#lab-3-2] Decode a ticket file that fails

Lab 3.2 · 25 min

Open a ticket file that fails to decode, read it with the declared encoding and list the lines that still fail.

[D3_2_open_ticket_file.html](https://sdaiaacademy.github.io/fn-101/labs/D3_2_open_ticket_file.html)

- [ ] Run the loader and read the error it raises (5 min)
- [ ] Open the file with its declared encoding (5 min)
- [ ] Decode line by line and collect each failure (9 min)
- [ ] Write the report; run the lab check (6 min)
- [ ] ✱ Stretch: Decode the failing lines as Windows-1256 and print the tickets they hold

### Session 3: Exceptions that explain

#### [day3#s3] Exceptions that explain

*Session 3*

- Raise and catch specific exceptions, around the one call that can fail
- Define an exception that carries a reason code and a detail
- Write a loader in which accepted plus rejected equals the lines of the input

#### [day3#three-ways-to-meet-bad-data] A program can meet a bad record in three ways. Only one is acceptable.

*Bad input*

- **Crash.** Line 37 is broken, so nobody gets the other 434. And tomorrow, line 52.
- **Pass silently.** Skip it, or fill in a default. The report looks complete and is wrong by an unknown amount.
- **Reject with a reason.** The run finishes, the good records are used, and each bad one is listed with where and why.

> **The rule of the house.** Accepted plus rejected equals the lines of the input. Always, and checked by the program itself.

#### [day3#exceptions-travel] An exception travels up the call stack until some caller catches it

*Exceptions*

1. **parse_value("N/A")** raises ValueError
2. **parse_row(row)** no handler: passes it on
3. **load_readings(path)** has try and except: handles it, goes on

- `raise` stops the function at once; nothing is returned
- Each caller in turn either handles it or is stopped too
- If nobody handles it, the program ends and prints the stack: the traceback
- So the place that **detects** a problem need not be the place that **decides** what to do

#### [day3#catch-specific] Catch the exception you expect, by name. A wide net catches your own mistakes too.

*Catching*

```python
# file: too wide
try:
    value = flaot(text)
except Exception:
    skipped += 1
```

```python
# file: specific
try:
    value = float(text)
except ValueError:
    skipped += 1
```

- Left: the misspelt `flaot` raises a `NameError` on every row. The net catches it, and the script reports that all 17,690 rows were "skipped"
- Right: only "this text is not a number" is handled. Anything else still stops the run and shows you where

> **A bare `except:` is the widest net of all.** The labs' checks refuse it.

#### [day3#own-exception-with-reason] An exception of your own can carry what the handler needs: a code and a detail

*Your own exception*

```python
# file: intake.py
class Rejected(Exception):
    def __init__(self, reason, detail):
        super().__init__(f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail

raise Rejected("BAD_PRIORITY",
               f"priority is {value!r}")
```

- A **reason code** for programs: it can be counted, grouped and tested
- A **detail** for people: the actual value, so that someone can repair the line
- The handler catches `Rejected` and nothing else: every other exception is a bug to see

#### [day3#raise-early-guards] Day 1's guard clauses, with raise in place of return

*Validation as guards*

```python
# file: intake.py
if ticket["priority"] not in PRIORITIES:
    raise Rejected("BAD_PRIORITY", ...)
try:
    date.fromisoformat(ticket["opened"])
except ValueError:
    raise Rejected("BAD_DATE", ...) from None
return ticket
```

- The function now returns **only** good tickets. A caller cannot forget to look at a reason
- Let the library judge: `fromisoformat` knows that September has 30 days
- Translate its `ValueError` into your own exception, with your own code
- The first guard that fires wins: one reason per line

#### [day3#try-around-one-record] The try wraps one call for one line, and the loop goes on

*The loop*

```python
# file: intake.py
for line_no, line in enumerate(file, start=1):
    try:
        accepted.append(parse_ticket(line))
    except Rejected as problem:
        rejected.append((line_no,
                         problem.reason,
                         problem.detail))
```

- Inside the loop: one bad line costs one line
- A `try` around the **whole loop** would end at the first rejection and lose every line after it
- The line number is counted here, where it is known, and stored with the reason

> **You wrote this shape an hour ago.** Decode each line, catch the decode error, collect the failure: the same loop with another exception.

#### [day3#account-for-every-line] 435 lines in: 400 accepted, 35 rejected, 0 unaccounted for

*From the lab's run*

| Reason | Lines |
| --- | --- |
| MISSING_FIELD | 8 |
| BAD_JSON | 6 |
| BAD_PRIORITY | 5 |
| BAD_DATE, BAD_METER_ID | 4 + 4 |
| EMPTY_LINE, EMPTY_TEXT | 3 + 3 |
| NOT_OBJECT | 2 |

```python
# file: intake.py
assert len(accepted) + len(rejected) == lines
```

- The program checks its own accounting on every run
- The table tells the sender what to fix first
- The log, `rejections.csv`, says which line and what was in it

#### [day3#check-except-scope] The log says 435 rejected and 0 accepted. Why?

*Checkpoint*

**Question:** A colleague's intake finishes without a crash. Every line is in the rejection log with the reason `UNKNOWN`. The loop reads: `try: accepted.append(parse_tiket(line))`, then `except Exception: rejected.append((line_no, "UNKNOWN", ""))`.

- A. Every line of the file is malformed
- B. A typo raises NameError on every line; the wide except logs it
- C. The try is inside the loop and should be around it
- D. The file was opened with the wrong encoding

#### [day3#lab-3-3] Reject malformed lines with a reason

Lab 3.3 · 25 min

Reject malformed lines with a reason code so every input line is accounted for.

[D3_3_reject_malformed_lines.html](https://sdaiaacademy.github.io/fn-101/labs/D3_3_reject_malformed_lines.html)

- [ ] Run the intake and read the first crash (4 min)
- [ ] Add the six checks, each raising a reason (10 min)
- [ ] Catch the rejection around one call per line (4 min)
- [ ] Write the rejection log; run the lab check (7 min)
- [ ] ✱ Stretch: Add a ninth reason, DUPLICATE_ID, for a ticket id that an earlier line already used

### Session 4: A debugging method

#### [day3#s4] A debugging method

*Session 4*

- Read a traceback from its last line upward
- Shrink a failing input to the smallest one that still fails
- Write a regression test that fails on the defect and passes on the fix

#### [day3#six-steps] Six steps turn "it gives wrong numbers" into a fix that stays fixed

*A method, not a talent*

- **1 · Reproduce.** One command that shows the wrong result, every time.
- **2 · Shrink.** The smallest input that still shows it.
- **3 · Hypothesis.** One sentence: "I think … because …".
- **4 · Test it.** An observation that would prove you wrong.
- **5 · Fix.** The smallest change, at the cause.
- **6 · Regression check.** A test that fails without the fix.

#### [day3#read-traceback-bottom-up] Read a traceback from its last line upward

*When it crashes*

```text
# file: the traceback of drill 3
Traceback (most recent call last):
  File "drill.py", line 22, in <module>
    print(total(rows))
  File "drill.py", line 17, in total
    result += to_number(row["consumption_m3"])
  File "drill.py", line 11, in to_number
    return float(text)
ValueError: could not convert string to float: 'N/A'
```

- **Last line.** **What** went wrong, and with which value.
- **The frame above it.** **Where**: file, line, function.
- **The frames further up.** **How we got there**: who called whom.

#### [day3#quiet-wrong-answers] The harder defects raise nothing: they give a wrong answer politely

*When it does not crash*

- **Report A.** The same file, read twice in one job. Run 1: 17,561 accepted. Run 2: 0 accepted.
- **Report B.** The report gives a median of 0.653 for meter M-0012. Sorted by hand, it is 0.696.

- No traceback to read. You start from a **difference**: what you got against what must be true
- So step 1 is to make that difference appear on demand, with one command
- And somebody has to know what "must be true" is: here, the operator and Salma

#### [day3#shrink-the-input] Shrink until the failing case fits in your head

*Step 2*

1. **17,690 rows** fails, and tells you nothing
2. **Half of them** still fails? Halve again
3. **2 rows, or 3 values** fails, and you can check it by hand

- Shrink the **data** (fewer rows, one meter), the **steps** (one function, not the whole tool) and the **calls** (does it need two?)
- Each cut either keeps the failure, so you continue, or loses it, and then you have learnt what matters
- The smallest failing case is the regression test, almost written

#### [day3#hypothesis-then-test] Say what you think is wrong before you touch the code, then try to prove yourself wrong

*Steps 3 and 4*

- **A hypothesis.** "I think the count is wrong because line 40 of report.py starts the total at 1." A file, a line, a reason.
- **A test of it.** "If so, a file of one row gives 2." Run it. One row gives 1: the hypothesis is dead, in thirty seconds, with no code changed.

```python
# file: looking inside
print("start:", len(seen))   # the quick look

breakpoint()                 # or stop here, then:
# p name    print a name
# n         next line
# s         step into a call
# c         continue      q   quit
```

#### [day3#regression-test] A regression test fails on the defect and passes on the fix. Then it stays.

*Step 6*

```python
# file: test_regression.py
def test_total_of_one_row():
    rows = [{"consumption_m3": "0.5"}]
    assert total(rows) == 0.5
```

- Write it from the shrunk case, **before** or right after the fix
- See it fail on the old code. A test you never saw fail may be testing nothing
- See it pass on the new code
- Keep it: it runs with every later change, for as long as the code lives

> **The lab's check does step 2 of that list for you.** It puts each defect back into a copy of the package and expects your test to fail there.

#### [day3#why-ai-off-here] The first attempt at a debugging lab is yours alone

*How we work*

- An assistant will often find a seeded defect in seconds. Then the lab has taught you to ask
- The skill is the six steps: you need them for the defect no assistant has seen
- The supervised check has one debugging task, in a locked editor

- **After the attempt.** Still stuck? Tomorrow's last lab uses the course tutor for hints, which you turn into your own explanation.

> **The evidence comes tomorrow.** Day 4 looks at what a controlled study found when people learnt with and without an assistant.

#### [day3#check-debug-next-step] What is the next step?

*Checkpoint*

**Question:** The district report shows Al-Rabwa with twice the readings it should have. You can make it happen every time with one command on the month file. You have not opened the code yet.

- A. Find the smallest input that still doubles: one district, a handful of rows
- B. Read the whole package from the top until something looks wrong
- C. Divide the count of that district by two in the report
- D. Write a regression test on the whole month file

#### [day3#lab-3-4] Find and fix two seeded defects

Lab 3.4 · 25 min

With AI off, find and fix two seeded defects and write a regression test for each.

[D3_4_ai_off_find.html](https://sdaiaacademy.github.io/fn-101/labs/D3_4_ai_off_find.html)

- [ ] Reproduce both reports and write what you see (5 min)
- [ ] Defect A: shrink, hypothesis, test, fix (8 min)
- [ ] Defect B: shrink, hypothesis, test, fix (7 min)
- [ ] Write a regression test for each; run the check (5 min)
- [ ] ✱ Stretch: Step through defect A with the debugger: stop on the first line of the function in each call and print what it starts with

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **Name the encoding.** Bytes become text through a table you choose. Decode strictly, report what fails, never ignore.
- **Every line is accounted for.** Reject with a code and a detail; catch only what you expect; accepted plus rejected equals the input.
- **Six steps.** Reproduce, shrink, hypothesis, test, fix, regression check. The test is what makes the fix last.

#### [day3#next] Day 4: From notebook to tool

*Next*

Tomorrow Salma's notebook becomes a command that anyone can rerun, with tests around its one rule. Lab 4.1 opens a notebook: have JupyterLab or an editor that opens notebooks ready.

## Day 4: From notebook to tool

What a notebook hides, a module with a command line, tests that pin a rule down, and an assistant that gives hints instead of answers

#### [day4#title] From notebook to tool

*SDAIA Academy · Python for Data and AI Work*

Day 4: What a notebook hides, a module with a command line, tests that pin a rule down, and an assistant that gives hints instead of answers

Data & AI Foundations Track · 4 teaching days + capstone day · 4 sessions · 4 labs · FN-101

#### [day4#drill-4] Order the lines, find the bug · 10 minutes

*Drill 4 · AI off*

A scrambled function with one line that does not belong, then a bug to find by hand: `labs/drills/day4.md`. On paper, no computer, no assistant.

#### [day4#review-day3] Where does the try go?

*Review of Day 3*

**Question:** An intake reads 435 ticket lines. A broken line must be recorded with its reason, and the lines after it must still be read. Where does the `try` belong?

- A. Around the whole loop over the lines
- B. Inside the loop, around the one call that parses one line
- C. Around the call of the intake function, in the script
- D. Inside the loop, with `except: pass` to keep going

#### [day4#agenda] From notebook to tool

*Today*

- **Session 1 · What notebooks hide**: What the kernel remembers and the page does not show; restart and run all
- **Session 2 · Scripts, modules and an entry point**: From cells to a tool: an entry point, arguments, exit codes, logging, the same report on every run
- **Session 3 · Tests as a safety net**: A test is an example with a verdict: boundaries, empty input, and what passing proves
- **Session 4 · Learning with an assistant without losing the skill**: What a controlled study found about learning with an assistant, and a way of working that keeps the skill

### Session 1: What notebooks hide

#### [day4#s1] What notebooks hide

*Session 1*

- Read the execution counts of a saved notebook and say in which order it was run
- Find a name that only the kernel remembers and an output that the code on screen does not produce
- Choose a notebook, a script or a module for a task, with a one-line reason

#### [day4#page-and-kernel] A notebook is two things: a page that is saved and a memory that is not

*Notebooks*

- **The page.** Cells of code and text, and under each code cell the output of the last time it ran. This is the file, `analysis.ipynb`. It is what you send to a colleague.
- **The kernel.** A running Python that holds every name any cell has bound since it started. It lives on your laptop only, and ends when you close it.

> **What goes wrong.** The page and the kernel can disagree, and nothing on the screen says so. Every problem of this session is one form of that sentence.

#### [day4#execution-counts] The number in brackets is the order of running, not the order on the page

*Reading a saved notebook*

| Cell, top to bottom | Count |
| --- | --- |
| Load the two files | [1] |
| Keep the valid readings | [3] |
| Set the factor to 3.0 | [4] |
| Find the anomalies | [8] |
| Count per district | [9] |
| What if: set the factor to 2.0 | [7] |

- A **gap** (no 2, no 5, no 6): a cell was run and deleted, or run again later
- A **step backwards** (9, then 7): the cell below ran before the cells above it
- Counts **1, 2, 3 and on**: the page was run once, top to bottom

#### [day4#deleted-cell] A deleted cell leaves its names behind in the kernel

*Hidden state, first form*

```python
# file: cell [2], run once, then deleted
known = set(district_of)
```

```python
# file: cell [3], still on the page
if row["meter_id"] not in known:
    continue
```

- For Salma the notebook works: her kernel still holds `known`
- For anyone else, and for her after a restart: `NameError: name 'known' is not defined`
- The file she sent does not contain the code that produced its own outputs

#### [day4#stale-output] An output can be older, or newer, than the code printed above it

*Hidden state, second form*

```python
# file: cell [4]
factor = 3.0
```

```python
# file: cell [8], with its saved output
anomalies = [...]   # above factor * median
print(len(anomalies), "anomalies")
# 27 anomalies
```

- **27** on the page, under "factor = 3.0"
- **18** on a clean run from top to bottom

> **What happened.** A cell further down set `factor = 2.0`, and the anomaly cell was run again afterwards. The 27 is true of a factor nobody can see beside it.

#### [day4#restart-run-all] Restart and run all, then read the numbers

*The one habit*

- **Restart** empties the kernel: every name is gone
- **Run all** runs the page in the order a reader sees it
- If it stops, the page depended on something it does not hold
- If a number changes, the old one was stale
- Then save: counts 1, 2, 3 and on tell the next reader it was done

- **And one rule of writing.** Set each name in one cell. A second question gets a second name: `strict_factor`, not `factor` again. Then no cell can change what an earlier cell means.

#### [day4#three-homes] Three homes for code, each good at one thing

*Where code lives*

- **Notebook.** For looking: a question asked once, steps you want to see, results and notes on one page. State persists between cells.
- **Script.** For repeating: the same steps on new files, by anyone, with one command. Starts empty every run.
- **Module.** For sharing: functions that other code imports, written once and tested in one place. Runs nothing by itself.

> **They work together.** A notebook that imports a tested module is a good notebook. Tomorrow's capstone is a script on top of modules.

#### [day4#choose-a-home] Four questions decide the home

*Choosing*

| Ask | If yes |
| --- | --- |
| Is the way to the answer still unknown, and asked once? | Notebook |
| Will a person read the outputs and notes together, as a page? | Notebook |
| Will it run again, on new input, by someone else or by a schedule? | Script |
| Does more than one program, or a test, need the same piece? | Module |

> **The usual journey.** Explore in a notebook, move what survives into functions in a module, and give the routine run to a script. Session 2 makes that move.

#### [day4#check-notebook-home] Which home for this task?

*Checkpoint*

**Question:** Every Sunday the branch offices send a ticket file. It must be decoded, checked and turned into a rejection log before the customer care team starts work. Nobody watches it run.

- A. A notebook that the analyst on duty opens and runs each Sunday
- B. A module with the decoding and checking functions, and nothing else
- C. A script with one command, built on functions that live in a module
- D. A notebook, because the outputs stay visible under each cell

#### [day4#lab-4-1] Find the notebook's hidden state

Lab 4.1 · 25 min

Run a notebook out of order, find the hidden-state bug, then restart and run all; then choose a home for four tasks.

[D4_1_run_notebook_out.html](https://sdaiaacademy.github.io/fn-101/labs/D4_1_run_notebook_out.html)

- [ ] Read the saved notebook and its execution counts (4 min)
- [ ] Restart and run all; find the missing name (7 min)
- [ ] Find the stale number and give factor one home (7 min)
- [ ] Choose a home for four tasks; run the check (7 min)
- [ ] ✱ Stretch: Run the notebook from the terminal with one command and compare the count with the saved one

### Session 2: Scripts, modules and an entry point

#### [day4#s2] Scripts, modules and an entry point

*Session 2*

- Explain what runs when a file is imported and when it is run, and what an entry point is for
- Write a command line with required arguments, a default and a useful exit code
- Produce a report that is byte for byte the same on two runs over the same files

#### [day4#cells-to-functions] Each cell becomes a function. What is left is the order, and that is main.

*From notebook to tool*

| In the notebook | In the package |
| --- | --- |
| The cell that reads the registry | `load_meters(path)` |
| The cell that keeps valid readings | `load_readings(path, known)` |
| The cell that finds anomalies | `find_anomalies(readings, factor)` |
| The cells that print tables | `render(...)`, which returns text |
| File names typed into cells | arguments of the command line |
| You, pressing run in order | `main()` |

> **What changed.** Names that lived in the kernel are now arguments and return values. Nothing is remembered between runs.

#### [day4#import-against-run] Importing a file runs its top level. So the top level should only define things.

*One file, two uses*

```python
# file: report_tool.py
def build_report(path):
    ...

def main():
    print(build_report("readings.csv"))

if __name__ == "__main__":
    main()
```

- `python report_tool.py`: the file is the program, `__name__` is `"__main__"`, and `main()` runs
- `import report_tool`: the same lines run, `__name__` is `"report_tool"`, and nothing is called
- So a test can import `build_report` without starting the tool

#### [day4#entry-point] An entry point is the one door through which the tool is started

*A package as a program*

```text
# file: the package
miqyas/
  __init__.py
  __main__.py     the door
  cli.py          arguments and main()
  readings.py     load and validate
  anomalies.py    the rule
  report.py       aggregate and render
```

```python
# file: miqyas/__main__.py
from miqyas.cli import main

raise SystemExit(main())
```

- `python -m miqyas` runs `__main__.py`
- `main()` returns a number, and `SystemExit` hands it to the system as the exit code

#### [day4#arguments] Arguments replace the file names typed into cells

*argparse*

```python
# file: miqyas/cli.py
report.add_argument("--readings", type=Path, required=True,
                    help="the readings file (CSV)")
report.add_argument("--factor", type=float, default=3.0,
                    help="anomaly threshold, times the median")
```

- **Converted.** `type=` turns the text of the command line into a path or a float, or refuses it with a message.
- **Required or default.** An input is required. A setting has a default that is written down once.
- **Documented.** `--help` is built from these calls: the usage text cannot drift from the code.

#### [day4#exit-codes] The exit code is how a tool tells a schedule whether it worked

*Speaking to other programs*

| Code | Meaning in Miqyas |
| --- | --- |
| 0 | The report was written |
| 2 | An input file is missing, or the arguments are wrong |
| 1 | Something unexpected: Python ended with a traceback |

- Zero means success; anything else means "do not use the output"
- A missing file is expected trouble: one clear line and code 2, not a traceback
- Rejected rows are not a failure: the report counts them, and the code is still 0

#### [day4#log-not-print] The result goes to the file. What happened on the way goes to the log.

*Messages*

```python
# file: miqyas/cli.py
log = logging.getLogger("miqyas")

log.info("%d rows accepted, %d rejected",
         len(readings), len(rejections))
log.error("no such file: %s", path)
```

- A level on every message: with `-v` you see the steps, without it only problems
- Log messages go to the error stream, so the output of the tool stays clean
- Counts and file names belong in a log. A customer's phone number or ticket text does not

> **Personal data.** A log is copied, mailed and kept for years. Yesterday's rule holds here: mask before anything is written, printed or logged.

#### [day4#same-bytes-twice] Same files in, same bytes out: a property you can test

*Reproducibility*

- No time of the run in the report: the time goes in the log
- A fixed order everywhere: sorted districts, anomalies by meter and day
- The encoding and the line ends are named when writing
- Nothing remembered between runs: no kernel, no default that grows

```bash
# file: terminal
python -m miqyas report ... --out a.md
python -m miqyas report ... --out b.md
# then compare the bytes of a.md and b.md
```

> **Why it matters.** When the report changes next month, you know the input changed, or the code did. Without this property you know nothing.

#### [day4#check-entry-point] The test run prints a report. Why?

*Checkpoint*

**Question:** A colleague's file `monthly.py` defines three functions and ends with the line `main()`. A test file starts with `from monthly import clean`. Running the tests reads the month file and prints the whole report before any test starts.

- A. pytest calls every function it finds in an imported file
- B. Importing runs the file's top level, and the call of `main()` is at the top level
- C. Importing `clean` also imports `main`, and imported functions run once
- D. The file has no `__main__.py` beside it

#### [day4#lab-4-2] Give the notebook a command line

Lab 4.2 · 25 min

Move the supplied notebook logic into a module with a command-line entry point.

[D4_2_move_supplied_notebook.html](https://sdaiaacademy.github.io/fn-101/labs/D4_2_move_supplied_notebook.html)

- [ ] Match the notebook's cells to the package's functions (4 min)
- [ ] Add the three arguments and the entry point (6 min)
- [ ] Write main: the cells' order as calls, with logging (9 min)
- [ ] Run twice, compare the bytes, run the check (6 min)
- [ ] ✱ Stretch: Add an argument that also writes every rejected row, with its reason, to a CSV file

### Session 3: Tests as a safety net

#### [day4#s3] Tests as a safety net

*Session 3*

- Write a test as an arranged input, one call and an asserted result
- Choose examples at the boundary, for empty input and for each argument of a rule
- Judge a set of tests by the wrong versions of the code it would catch

#### [day4#example-with-a-verdict] A test is an example with a verdict

*Tests*

```python
# file: at a prompt: you are the verdict
>>> is_anomaly(5.0, [1.0, 1.0, 1.0])
True
```

```python
# file: in a test: the verdict is written down
def test_far_above_is_an_anomaly():
    assert is_anomaly(5.0, [1.0, 1.0, 1.0]) is True
```

- You have run examples at the prompt all week and judged the answers by eye
- A test keeps the example and the expected answer, so a machine can judge it again
- `uv run pytest` finds the functions named `test_`, runs each, and reports the ones whose `assert` was false

#### [day4#arrange-act-assert] Arrange, act, assert: three parts, one reason to fail

*The shape of a test*

```python
# file: test_anomalies.py
def test_exactly_three_times_is_not_an_anomaly():
    history = [1.0, 1.0, 1.0]             # arrange
    result = is_anomaly(3.0, history)     # act
    assert result is False                # assert
```

- **Arrange** an input small enough to check in your head
- **Act** with one call of the thing under test
- **Assert** one fact about the result
- The **name** is the sentence the test proves: it is what a colleague reads when it fails

#### [day4#choose-examples] Mistakes live at the edges, so that is where the examples go

*Choosing examples*

- **The boundary.** Exactly three times the median, and just above it. `>` and `>=` differ at one point only.
- **Nothing.** An empty history. What should happen is a decision; the docstring states it and a test holds it.
- **Each argument.** If changing `factor` changes no test's answer, no test would notice that it is ignored.

> **A way to find them.** Read the docstring and the signature. Every promise and every argument deserves an example that would fail if it were broken.

#### [day4#median-not-mean] A good example gives different answers for the right rule and a wrong one

*An example that discriminates*

| History | Median | Mean |
| --- | --- | --- |
| 1, 1, 1 | 1.0 | 1.0 |
| 1, 1, 1, 1, 10 | 1.0 | 2.8 |

- With the first history, a rule built on the mean passes every test you write
- With the second, the value 3.5 is an anomaly by the median (above 3.0) and not by the mean (below 8.4)
- One example, chosen so that the two rules disagree

#### [day4#what-passing-proves] Passing tests prove the examples, not the program

*What a green run means*

- **What you know.** On these inputs the code gives these answers, today and after every change, checked in a second.
- **What you do not know.** Anything about inputs nobody thought of. Defect B of yesterday passed every test that used a sorted list.

- Tests and types catch different mistakes: a type checker never runs the code, a test never sees the lines it does not reach
- A test that cannot fail is worse than none: it reports safety that is not there

#### [day4#read-a-failing-test] A failing test is a traceback with the values filled in

*Reading the output*

```text
# file: terminal
    def test_exactly_three_times_is_not_an_anomaly():
        history = [1.0, 1.0, 1.0]
        result = is_anomaly(3.0, history)
>       assert result is False
E       assert True is False

test_anomalies.py:14: AssertionError
1 failed, 6 passed in 0.03s
```

- Read from the bottom, as yesterday: how many failed, which file and line, then the line marked `>`
- The `E` line shows what the assert compared: it expected False and got True
- Reproduce and shrink are already done: the test is the small failing case

#### [day4#tests-make-change-safe] Tests are what lets you, or an assistant, change code without fear

*Why keep them*

1. **Tests pass** the rule is pinned down
2. **Change the code** by hand or with an assistant
3. **Run the tests** a second, every time
4. **Still pass?** keep the change, or undo it

- The sixth step of debugging adds one test per defect, so the net grows where the code has failed before
- Code an assistant wrote for you is code you have not read line by line. Your tests are how you hold it to the rule

#### [day4#check-which-test] Which test would catch it?

*Checkpoint*

**Question:** Someone "tidies" the rule and writes `value >= factor * median(history)` where it said `>`. Which test fails?

- A. The value 5.0 with the history 1, 1, 1 is an anomaly
- B. The value 1.1 with the history 1, 1, 1 is not an anomaly
- C. The value 100.0 with an empty history is not an anomaly
- D. The value 3.0 with the history 1, 1, 1 is not an anomaly

#### [day4#lab-4-3] Pin the anomaly rule down with tests

Lab 4.3 · 25 min

Write five tests for the anomaly rule, including empty and boundary inputs.

[D4_3_write_five_tests.html](https://sdaiaacademy.github.io/fn-101/labs/D4_3_write_five_tests.html)

- [ ] Read the rule's docstring and the one supplied test (3 min)
- [ ] Write a test for the boundary and one for no history (8 min)
- [ ] Write three more: the median and the factor (8 min)
- [ ] Run the check against four wrong versions (6 min)
- [ ] ✱ Stretch: Rewrite your examples as one table with pytest's parametrize, one row per case

### Session 4: Learning with an assistant without losing the skill

#### [day4#s4] Learning with an assistant without losing the skill

*Session 4*

- State what the evidence shows about delegating to an assistant while learning
- Ask an assistant for a hint that leaves the reasoning with you
- Explain a fix in your own words, without the code and without the assistant

#### [day4#the-honest-question] An assistant can write this week's code in seconds. So what did you learn it for?

*The question of the week*

- Someone has to say whether the code is right. This week that was you, sixteen times
- Reading, tracing and debugging are the skills that judging needs
- The defects of labs 3.4 and 4.4 run without an error and print plausible numbers

- **The claim of this session.** An assistant changes how you produce code. Whether it also changes what you learn depends on how you use it, and there is evidence on that.

#### [day4#the-evidence] Learning a new library with an assistant: the task got done, less of it stayed

*A randomised experiment, 2026*

- **67%** average quiz score, coding by hand
- **50%** average quiz score, coding with an AI assistant

- Developers learnt a Python library they had not used, half with an assistant and half without
- Afterwards everyone took the same quiz on the library, without help
- The study comes from a company that builds assistants, and reports a cost of using them

Source: Anthropic, "How AI assistance impacts the formation of coding skills" (2026), arXiv 2601.20245.

#### [day4#where-the-gap-is] The largest gap was on debugging questions

*The same study*

- The quiz asked about concepts, reading code and debugging
- The group that used the assistant fell behind most where it had to find what was wrong in code
- That is the skill needed to check what an assistant hands you

- **Why this course does what it does.** Daily drills on paper. The first attempt at each debugging lab alone. A supervised check without an assistant. A capstone you walk through and change live.

#### [day4#how-you-use-it] How people used the assistant mattered, not only whether

*The same study*

- **Handing the work over.** Ask for the code, paste it, ask again when it fails. The task is finished and the reasoning was never yours.
- **Keeping the thinking.** Ask why, ask for an explanation with the code, ask about the idea and write the code yourself. Participants who worked this way kept more.

> **So the choice is yours each time.** The same tool can be an answer machine or a tutor. Which one it is depends on what you ask it for.

#### [day4#attempt-hint-explain] Attempt first, ask for a hint, explain it back

*A way of working while you learn*

1. **1 · Attempt** reproduce, shrink, a first hypothesis, in writing
2. **2 · Hint** one at a time; do what it says before the next
3. **3 · Explain** assistant closed, in your words, no code

- The attempt gives the hint something to attach to. Without it, a hint is an answer in slow motion
- The explanation is the test of whether you learnt it. If you cannot write it, you have a fix and not yet an understanding

#### [day4#ask-for-a-hint] A question that gets a hint says what you expected, what you saw and what you tried

*Asking well*

- **Gets an answer to paste.** "Here is report.py. The district counts are wrong. Fix it."
- **Gets a hint to use.** "Every district shows 18 and I expected different counts. With two meters and one anomaly both districts show it. I think the lists are shared. Do not give me code: what should I check to prove it?"

> **The course tutor, Dalil.** It is instructed to give one hint at a time and no code, and the workspace's agent instructions ask the same of any assistant opened there.

#### [day4#what-leaves-the-laptop] What you send to a hosted assistant has left the organisation

*Before you paste*

- Code you wrote for a lab: fine. A traceback: read it first, it may quote a record
- A customer's ticket, phone number or meter history: personal data, not to be sent to a service your organisation has not approved
- Shrink first. A case built by hand with two invented meters shows the defect and holds nobody's data

- **In this lab.** The tutor sends your question and the source files you name. It refuses anything under `data/`. The data here is synthetic; the habit is for the day it is not.

#### [day4#three-modes] Three modes, each with a reason

*How this course uses assistants*

- **Off.** The daily drills, the first attempt at labs 3.4 and 4.4, and the supervised check: tracing on paper and one debugging task in a locked editor.
- **Tutor.** The other labs: an assistant may give hints and explain, and is told not to give code.
- **Full.** The capstone: any tool you like. Then you run it, change it on request and read a traceback from it, live.

> **What all three protect.** That the person who signs the work can explain it.

#### [day4#check-hint-or-answer] What do you do next?

*Checkpoint*

**Question:** You are learning. A report shows the same count for every district. You have reproduced it and have no idea yet where it comes from. An assistant is open in the next window.

- A. Paste the package and ask for the corrected file
- B. Paste the package and ask which line is wrong, then fix it yourself
- C. Shrink it to a case built by hand, write a first guess, then ask for one hint on what to check
- D. Close the assistant and never use it for debugging

#### [day4#lab-4-4] Debug a third defect with the tutor

Lab 4.4 · 25 min

Get hints from the course tutor on a new defect, then explain the fix in your own words.

[D4_4_get_hints_from.html](https://sdaiaacademy.github.io/fn-101/labs/D4_4_get_hints_from.html)

- [ ] Reproduce and shrink on your own, in the log (6 min)
- [ ] Ask the tutor for one hint at a time (6 min)
- [ ] Fix the line and write the regression test (6 min)
- [ ] Close the tutor; explain the fix in words (7 min)
- [ ] ✱ Stretch: Ask the hosted tutor for the corrected code outright and note in the log what it does

#### [day4#wrap-up] Three things to keep

*Day 4 · wrap-up*

- **Restart and run all.** A notebook's page and its kernel can disagree. Read numbers only after a clean run, and move what repeats into a script on modules.
- **One command, same bytes.** Arguments, an exit code, a log, and tests at the edges of the rule. That is a tool someone else can trust.
- **Attempt, hint, explain.** Use an assistant so that the reasoning stays with you. What you can explain without it is what you have learnt.

#### [day4#next] The capstone: a tool of your own

*Next*

A new dataset, Manahil's maintenance work orders, and one brief: load, validate, report, with one command. Any tool is allowed. Then ten minutes in which you run it, change it and read a traceback from it. The brief is in `labs/capstone/`.

## Capstone: Capstone project presentations

#### [capstone#title] Capstone project presentations

*SDAIA Academy · Python for Data and AI Work*

Capstone

Data & AI Foundations Track · 4 teaching days + capstone day · 10 min talk and demo · FN-101

#### [capstone#agenda] How the day runs

*Capstone*

- **The supervised check**: one hour, on paper and in a locked editor, no assistant
- **Finishing the tool**: the brief, the public tests, the README; any tool is allowed
- **Walkthroughs**: ten minutes each: run it, change it, read a traceback
- **Review and closing**: what the tools showed, the follow-up task, what comes next

#### [capstone#supervised-check] Trace, order, debug · 60 minutes

*Supervised check · AI off*

Ten snippets to trace on paper, one function to put in order, one defect to find with a log. Laptops closed for the first two parts; a locked editor for the third.

#### [capstone#the-brief] One command that turns the work-order export into a report Mazen can trust

*The capstone*

- **In:** 505 work orders (CSV) and the crews (JSON Lines), with planted problems
- **Rules:** eight reasons to reject a row, applied in a fixed order
- **Out:** a report for a person, a summary for a program, a rejection log
- **Always:** accepted plus rejected equals the rows; two runs, the same bytes; nothing from the notes in any output

```bash
# file: terminal
python -m workorders report \
  --orders data/work_orders.csv \
  --crews data/crews.jsonl \
  --as-of 2026-10-31 --out out
```

#### [capstone#rubric] The rubric

*How the repository is scored*

| Item | Value |
| --- | --- |
| Correctness on hidden tests | 30% |
| Validation and errors | 20% |
| Structure and types | 20% |
| Reproducibility | 15% |
| README | 15% |

> **The hidden tests run your command on files you have not seen.** Other rows, the same rules. The public sample shows their shape.

#### [capstone#format] 10 minutes each, questions included

*The walkthrough · no assistant*

- **1 · Run it.** From a fresh clone: the one command, then the report. About three minutes.
- **2 · Change it.** The assessor asks for one small change. You make it live, with a test. About four minutes.
- **3 · Read a traceback.** Produced from your code, chosen by the assessor. From the last line up: what, where, what you would check first.

> **While you wait.** Read a neighbour's README and run their command. Write one thing that is clear and one question.

#### [capstone#running-order] Who presents when

*Running order*

| # | Participant | Repository |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first walkthrough*

Clone your own repository into a new folder and run the command there. Run the public tests. Read your README as a stranger would.

#### [capstone#now-presenting] Run, change, traceback

*Now presenting*

#### [capstone#review] What the tools showed

*Trainer review*

- **Strongest patterns.** What several repositories got right.
- **Common gaps.** What most tools would fix next.
- **One surprise.** Something nobody expected.

#### [capstone#what-next] Keep going

*After the course*

- **The follow-up task:** one new validation rule for Miqyas, with tests, reviewed by a peer. It is tracked: `labs/followup/`
- **Your tool stays yours:** keep it reproducible, and add the next rule you named in "what the tool does not check"
- **Next Academy courses:** FN-102 for version control, FN-104 for SQL and Arabic text normalisation, then the AI Engineering or the Data Science track

#### [capstone#thanks] Thank you

*SDAIA Academy*

Python for Data and AI Work
