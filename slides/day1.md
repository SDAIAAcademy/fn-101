---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/slides/day1.html"
---

# Python for Data and AI Work

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
