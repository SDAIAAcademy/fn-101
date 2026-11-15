<!-- academy:title -->
# Python for Data and AI Work

بايثون لأعمال البيانات والذكاء الاصطناعي

Data & AI Foundations Track · SDAIA Academy · FN-101 · Level 100

REPLACE: one line under the title: what participants can do after the course

Participants write Python the way data and AI work needs it: small typed functions over collections and files, errors that fail loudly, and code moved out of notebooks into scripts that rerun. The case is a fictional regional water utility with synthetic meter readings in comma-separated values (CSV) files and bilingual service tickets in JavaScript Object Notation (JSON) Lines. Each day opens with an AI-off drill in reading, tracing or debugging code by hand, and the labs grow into a command-line tool that validates readings, flags anomalies and writes a summary report. Arabic text normalisation and SQL are left to FN-104, version control to FN-102.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/fn-101/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Explain what a short program prints, step by step, including name binding, shared mutable lists and dictionaries, and scope, given ten unseen snippets on paper, without a computer or assistant | Awareness | a trace sheet with at least eight of ten outputs correct |
| LO2 | Distinguish when a notebook, a script or an importable module is the right home for a piece of code, given four tasks described by the utility's analysts | Awareness | a choice and a one-line reason per task, matching the reference on three of four |
| LO3 | Implement typed functions that load, validate and aggregate records with lists, dictionaries, sets and comprehensions, given a month of meter readings with missing, duplicated and out-of-range values | Applied | a module that passes the provided tests and a type checker with no errors |
| LO4 | Apply exception handling and input validation so that each bad record is reported with a reason instead of crashing or passing silently, given a ticket file with malformed lines, mixed Arabic and English text and a wrong encoding | Applied | a rejection log that accounts for every input line |
| LO5 | Use a repeatable debugging method: reproduce, shrink the input, form a hypothesis, test it, fix, and add a regression check, given three seeded defects in the course codebase, with AI assistance off | Applied | a debugging log per defect and a passing regression test for each |
| LO6 | Prepare a command-line tool from an exploratory notebook, with an entry point, arguments and a written report, given the utility's analysis notebook and raw files | Applied | a script that rebuilds the same report from raw files with one command on two runs |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Read before you write | Values, names and references; Functions with clear contracts; Type hints and a checker; Parsons problems | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Collections for data work | Dictionaries for counting and grouping; Sets and membership; Comprehensions and generators; Records as data classes | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Files, text and failure | CSV and JSON Lines; Text, bytes and encodings; Exceptions that explain; A debugging method | [`slides/day3.html`](slides/day3.html) |
| Day 4 | From notebook to tool | What notebooks hide; Scripts, modules and an entry point; Tests as a safety net; Learning with an assistant without losing the skill | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a page in `labs/`, opened from the course page and from the lab slide of its session.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Trace eight snippets on paper, then check each answer in a step visualiser | [`D1_1_trace_eight_snippets.html`](labs/D1_1_trace_eight_snippets.html) |
| 1.2 | Day 1 · Session 2 | Split a 40-line script into four functions with stated inputs and outputs | [`D1_2_split_40_line.html`](labs/D1_2_split_40_line.html) |
| 1.3 | Day 1 · Session 3 | Annotate the supplied reading parser and fix every error the type checker reports | [`D1_3_annotate_supplied_reading.html`](labs/D1_3_annotate_supplied_reading.html) |
| 1.4 | Day 1 · Session 4 | Reorder scrambled lines, with distractors, into a working validation function | [`D1_4_reorder_scrambled_lines.html`](labs/D1_4_reorder_scrambled_lines.html) |
| 2.1 | Day 2 · Session 1 | Count readings per meter and district, then time a nested-loop version on 100,000 rows | [`D2_1_count_readings_per.html`](labs/D2_1_count_readings_per.html) |
| 2.2 | Day 2 · Session 2 | Find meters with no reading and readings with no known meter | [`D2_2_find_meters_no.html`](labs/D2_2_find_meters_no.html) |
| 2.3 | Day 2 · Session 3 | Stream a large readings file with a generator and compare peak memory with a list | [`D2_3_stream_large_readings.html`](labs/D2_3_stream_large_readings.html) |
| 2.4 | Day 2 · Session 4 | Model a ticket as a data class and sort tickets by priority and age | [`D2_4_model_ticket_as.html`](labs/D2_4_model_ticket_as.html) |
| 3.1 | Day 3 · Session 1 | Load readings and tickets and write a JSON summary per district, masking phone numbers before anything is written | [`D3_1_load_readings_tickets.html`](labs/D3_1_load_readings_tickets.html) |
| 3.2 | Day 3 · Session 2 | Open a ticket file that fails to decode, read it with the declared encoding and list the lines that still fail | [`D3_2_open_ticket_file.html`](labs/D3_2_open_ticket_file.html) |
| 3.3 | Day 3 · Session 3 | Reject malformed lines with a reason code so every input line is accounted for | [`D3_3_reject_malformed_lines.html`](labs/D3_3_reject_malformed_lines.html) |
| 3.4 | Day 3 · Session 4 | With AI off, find and fix two seeded defects and write a regression test for each | [`D3_4_ai_off_find.html`](labs/D3_4_ai_off_find.html) |
| 4.1 | Day 4 · Session 1 | Run a notebook out of order, find the hidden-state bug, then restart and run all | [`D4_1_run_notebook_out.html`](labs/D4_1_run_notebook_out.html) |
| 4.2 | Day 4 · Session 2 | Move the supplied notebook logic into a module with a command-line entry point | [`D4_2_move_supplied_notebook.html`](labs/D4_2_move_supplied_notebook.html) |
| 4.3 | Day 4 · Session 3 | Write five tests for the anomaly rule, including empty and boundary inputs | [`D4_3_write_five_tests.html`](labs/D4_3_write_five_tests.html) |
| 4.4 | Day 4 · Session 4 | Get hints from the course tutor on a new defect, then explain the fix in your own words | [`D4_4_get_hints_from.html`](labs/D4_4_get_hints_from.html) |
<!-- /academy:labs -->

## Capstone

A command-line tool that loads, validates and reports on a new synthetic dataset, the utility's maintenance work orders, submitted as a public repository whose README shows the command and its report, then a ten-minute walkthrough with a change the assessor requests

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- Has written and run a short program in any language, or completed the guided pre-work on values, conditions and loops

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Python runtime and project manager:** CPython with uv, CPython with pip and venv
- **Editor and notebook:** VSCodium or VS Code, JupyterLab, marimo
- **Type checking and linting:** mypy, Pyright, Ruff
- **Test runner:** pytest, unittest
- **Tracing and step debugging:** Python Tutor, pdb or the editor's debugger
- **Hint-only tutor:** an open-weight model behind a tutor instruction, an approved assistant with a tutor instruction
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- SDAIA Generative AI Guidelines: REPLACE: the address of the official text
- SDAIA Data & AI Academic Programs Standards Framework: bridging units SDF-Fundamentals and SDF-Data-Structures at Apply level: REPLACE: the address of the official text
