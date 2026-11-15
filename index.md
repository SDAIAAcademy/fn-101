---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/index.html"
---

# Python for Data and AI Work

بايثون لأعمال البيانات والذكاء الاصطناعي

Data & AI Foundations Track · 4 teaching days + capstone day · 26 hours · Level 100

Read, trace and debug Python by hand, then write small typed functions that grow into a command-line tool that reruns

Participants write Python the way data and AI work needs it: small typed functions over collections and files, errors that fail loudly, and code moved out of notebooks into scripts that rerun. The case is a fictional regional water utility with synthetic meter readings in comma-separated values (CSV) files and bilingual service tickets in JavaScript Object Notation (JSON) Lines. Each day opens with an AI-off drill in reading, tracing or debugging code by hand, and the labs grow into a command-line tool that validates readings, flags anomalies and writes a summary report. Arabic text normalisation and SQL are left to FN-104, version control to FN-102.

**Who it is for:** Beginners. Graduates and career changers entering the AI Engineering or Data Science track; computing and data graduates who pass the placement test skip the courses it covers.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Manahil Water Services.** Manahil Water Services is a fictional regional water utility with 600 meters in six districts. Its metering team checks a month of daily readings (a CSV file with missing, repeated, out-of-range and unknown-meter rows) and its customer care team works a queue of service tickets in Arabic and English (JSON Lines). Every lab works on these files and the labs grow into Miqyas, a command-line tool that validates the readings, flags anomalies and writes a report; all data is synthetic and the same on every machine.

## The course

### Day 1: Read before you write

Slides: https://sdaiaacademy.github.io/fn-101/slides/day1.md

- **Session 1: Values, names and references**
  - Trace a short program line by line with a table of names and objects
  - Predict when two names share one mutable object and when they do not
  - Distinguish rebinding a name from mutating an object
  - [Lab 1.1: Trace eight snippets (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D1_1_trace_eight_snippets.html)
- **Session 2: Functions with clear contracts**
  - Split a script into functions that each do one job
  - State a function's inputs and output in its signature and docstring
  - Explain what a function can see and change, using scope and the call stack
  - [Lab 1.2: Split a script into four functions (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D1_2_split_40_line.html)
- **Session 3: Type hints and a checker**
  - Annotate parameters and return values with built-in types
  - Read a type checker's report and find the line it points at
  - Handle a value that may be None before using it
  - [Lab 1.3: Annotate the reading parser (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D1_3_annotate_supplied_reading.html)
- **Session 4: Parsons problems**
  - Order the lines of a function so that each name is bound before it is used
  - Use indentation to say which lines belong to a branch, a loop or a try
  - Reject a distractor by saying what it would do
  - [Lab 1.4: Rebuild a validation function (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D1_4_reorder_scrambled_lines.html)

### Day 2: Collections for data work

Slides: https://sdaiaacademy.github.io/fn-101/slides/day2.md

- **Session 1: Dictionaries for counting and grouping**
  - Count and group records with a dictionary in one pass
  - Build an index from a key to a record and use it in place of a search
  - Explain why a loop inside a loop is slow on 100,000 rows, and measure it
  - [Lab 2.1: Count readings per meter and district (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D2_1_count_readings_per.html)
- **Session 2: Sets and membership**
  - Answer a membership question with a set in place of a search through a list
  - Compare two collections with difference and intersection
  - Use a tuple as a key to find repeated records
  - [Lab 2.2: Find silent meters and unknown ids (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D2_2_find_meters_no.html)
- **Session 3: Comprehensions and generators**
  - Write list, dictionary and set comprehensions with a filter
  - Write a generator function that yields records while a file is read
  - Compare the peak memory of a list and of a stream, and say when each fits
  - [Lab 2.3: Stream a large readings file (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D2_3_stream_large_readings.html)
- **Session 4: Records as data classes**
  - Model a record as a frozen data class with typed fields and a method
  - Sort records by several fields with a key function that returns a tuple
  - Leave out of a record the personal data the task does not need
  - [Lab 2.4: Model and sort the ticket queue (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D2_4_model_ticket_as.html)

### Day 3: Files, text and failure

Slides: https://sdaiaacademy.github.io/fn-101/slides/day3.md

- **Session 1: CSV and JSON Lines**
  - Read a CSV file and a JSON Lines file with the encoding and newline handling named
  - Write JSON output that is the same on every run and keeps Arabic readable
  - Mask personal data before anything is written, printed or logged
  - [Lab 3.1: Write a district summary with phones masked (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D3_1_load_readings_tickets.html)
- **Session 2: Text, bytes and encodings**
  - Explain the difference between bytes and text, and what an encoding does
  - Read a UnicodeDecodeError: the codec, the byte and the position
  - Decode a file line by line and report the lines that fail instead of ignoring them
  - [Lab 3.2: Decode a ticket file that fails (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D3_2_open_ticket_file.html)
- **Session 3: Exceptions that explain**
  - Raise and catch specific exceptions, around the one call that can fail
  - Define an exception that carries a reason code and a detail
  - Write a loader in which accepted plus rejected equals the lines of the input
  - [Lab 3.3: Reject malformed lines with a reason (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D3_3_reject_malformed_lines.html)
- **Session 4: A debugging method**
  - Read a traceback from its last line upward
  - Shrink a failing input to the smallest one that still fails
  - Write a regression test that fails on the defect and passes on the fix
  - [Lab 3.4: Find and fix two seeded defects (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D3_4_ai_off_find.html)

### Day 4: From notebook to tool

Slides: https://sdaiaacademy.github.io/fn-101/slides/day4.md

- **Session 1: What notebooks hide**
  - Read the execution counts of a saved notebook and say in which order it was run
  - Find a name that only the kernel remembers and an output that the code on screen does not produce
  - Choose a notebook, a script or a module for a task, with a one-line reason
  - [Lab 4.1: Find the notebook's hidden state (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D4_1_run_notebook_out.html)
- **Session 2: Scripts, modules and an entry point**
  - Explain what runs when a file is imported and when it is run, and what an entry point is for
  - Write a command line with required arguments, a default and a useful exit code
  - Produce a report that is byte for byte the same on two runs over the same files
  - [Lab 4.2: Give the notebook a command line (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D4_2_move_supplied_notebook.html)
- **Session 3: Tests as a safety net**
  - Write a test as an arranged input, one call and an asserted result
  - Choose examples at the boundary, for empty input and for each argument of a rule
  - Judge a set of tests by the wrong versions of the code it would catch
  - [Lab 4.3: Pin the anomaly rule down with tests (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D4_3_write_five_tests.html)
- **Session 4: Learning with an assistant without losing the skill**
  - State what the evidence shows about delegating to an assistant while learning
  - Ask an assistant for a hint that leaves the reasoning with you
  - Explain a fix in your own words, without the code and without the assistant
  - [Lab 4.4: Debug a third defect with the tutor (25 min)](https://sdaiaacademy.github.io/fn-101/labs/D4_4_get_hints_from.html)

### Capstone: Capstone project presentations

Slides: https://sdaiaacademy.github.io/fn-101/slides/capstone.md

## Capstone

A command-line tool that loads, validates and reports on a new synthetic dataset, the utility's maintenance work orders, submitted as a public repository whose README shows the command and its report, then a ten-minute walkthrough with a change the assessor requests

**What you submit:** A link to a public repository that holds the tool, its tests and a README that shows the one command and the report it writes on the supplied work-order files, and that states what the tool does not check. The commit history is part of the evidence. Then a ten-minute live walkthrough: the participant runs the tool, makes a change the assessor requests and explains a traceback the assessor chooses; the questions are inside the ten minutes.

**Rubric:**

- Correctness on hidden tests: 30%
- Validation and errors: 20%
- Structure and types: 20%
- Reproducibility: 15%
- README: 15%

## Outcomes

- **LO1** Explain what a short program prints, step by step, including name binding, shared mutable lists and dictionaries, and scope, given ten unseen snippets on paper, without a computer or assistant (Awareness) Evidence: a trace sheet with at least eight of ten outputs correct
- **LO2** Distinguish when a notebook, a script or an importable module is the right home for a piece of code, given four tasks described by the utility's analysts (Awareness) Evidence: a choice and a one-line reason per task, matching the reference on three of four
- **LO3** Implement typed functions that load, validate and aggregate records with lists, dictionaries, sets and comprehensions, given a month of meter readings with missing, duplicated and out-of-range values (Applied) Evidence: a module that passes the provided tests and a type checker with no errors
- **LO4** Apply exception handling and input validation so that each bad record is reported with a reason instead of crashing or passing silently, given a ticket file with malformed lines, mixed Arabic and English text and a wrong encoding (Applied) Evidence: a rejection log that accounts for every input line
- **LO5** Use a repeatable debugging method: reproduce, shrink the input, form a hypothesis, test it, fix, and add a regression check, given three seeded defects in the course codebase, with AI assistance off (Applied) Evidence: a debugging log per defect and a passing regression test for each
- **LO6** Prepare a command-line tool from an exploratory notebook, with an entry point, arguments and a written report, given the utility's analysis notebook and raw files (Applied) Evidence: a script that rebuilds the same report from raw files with one command on two runs

## Tools

- **Python runtime and project manager:** CPython with uv, CPython with pip and venv
- **Editor and notebook:** VSCodium or VS Code, JupyterLab, marimo
- **Type checking and linting:** mypy, Pyright, Ruff
- **Test runner:** pytest, unittest
- **Tracing and step debugging:** Python Tutor, pdb or the editor's debugger
- **Hint-only tutor:** an open-weight model behind a tutor instruction, an approved assistant with a tutor instruction

## Prerequisites

- Has written and run a short program in any language, or completed the guided pre-work on values, conditions and loops

## Sources

### National references

- [Personal Data Protection Law](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Generative AI Guideline for Government (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf)
- [Generative AI Guideline for Public (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Files/GenerativeAIPublicEN.pdf)
- [Academic Programs Standards Framework (SDAIA)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/Academic-Programs-Standards-Framework-Q3.pdf)

### Python: the language and its standard library

- [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)
- [Programming FAQ (names, objects, default values)](https://docs.python.org/3/faq/programming.html)
- [Errors and Exceptions (the Python Tutorial)](https://docs.python.org/3/tutorial/errors.html)
- [typing: support for type hints](https://docs.python.org/3/library/typing.html)
- [dataclasses: data classes](https://docs.python.org/3/library/dataclasses.html)
- [csv: CSV file reading and writing](https://docs.python.org/3/library/csv.html)
- [JSON Lines](https://jsonlines.org/)
- [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
- [PEP 686: Make UTF-8 mode default](https://peps.python.org/pep-0686/)
- [argparse: parser for command-line options](https://docs.python.org/3/library/argparse.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [pdb: the Python debugger](https://docs.python.org/3/library/pdb.html)
- [PEP 8: Style Guide for Python Code](https://peps.python.org/pep-0008/)

### Tools (examples of each capability)

- [uv, a Python package and project manager](https://docs.astral.sh/uv/)
- [mypy, a static type checker](https://mypy.readthedocs.io/en/stable/)
- [Pyright, a static type checker](https://microsoft.github.io/pyright/)
- [Ruff, a linter and formatter](https://docs.astral.sh/ruff/)
- [pytest, a test runner](https://docs.pytest.org/en/stable/)
- [Python Tutor, a step visualiser](https://pythontutor.com/)
- [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/)
- [marimo, a reactive notebook](https://marimo.io/)
- [VSCodium, an editor](https://vscodium.com/)
- [OpenRouter quickstart (one way to reach a free hosted model)](https://openrouter.ai/docs/quickstart)

### Evidence on learning to program with AI assistance

- [How AI assistance impacts the formation of coding skills (Anthropic, 2026)](https://www.anthropic.com/research/AI-assistance-coding-skills)
- [Shen and Tamkin, How AI Impacts Skill Formation (arXiv 2601.20245)](https://arxiv.org/abs/2601.20245)

---

SDAIA Academy · Data & AI Foundations Track · Python for Data and AI Work

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit 4b268e2
