---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
deck: "day4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/slides/day4.html"
---

# Python for Data and AI Work

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
