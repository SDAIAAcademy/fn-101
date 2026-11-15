<!-- academy:title -->
# Python for Data and AI Work

بايثون لأعمال البيانات والذكاء الاصطناعي

Data & AI Foundations Track · SDAIA Academy · FN-101 · Level 100

Read, trace and debug Python by hand, then write small typed functions that grow into a command-line tool that reruns

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

**Manahil Water Services (مناهل لخدمات المياه).** A fictional regional water utility with 600 meters in six districts. Its metering team checks a month of daily readings (a CSV file of 17,690 rows, 129 of them bad for six different reasons) and its customer care team works a queue of 400 service tickets in Arabic and English (JSON Lines). The labs grow into Miqyas (مقياس), a command-line tool that validates the readings, flags anomalies and writes the same report on every run. All data is synthetic, written by a generator with a fixed seed; no person, meter, phone number or identity number is real.

## How the course is organised

- **Pre-work** (`labs/prework/`): tracing and syntax exercises on values, conditions and loops, ending in an entry quiz.
- **Each day** opens with a ten-minute drill done on paper with AI off (`labs/drills/`), then four sessions of about 25 minutes of concepts and a 25-minute lab.
- **Every lab** starts from its own supplied folder in the lab workspace and has a check that runs the participant's code; `labs/README.md` says how to build the workspace.
- **AI policy.** AI off for the daily drills, the first attempt at each debugging lab and the supervised check. AI tutor in the other labs: the repository's agent instructions tell an assistant to give hints, not code. AI full in the capstone, which the participant walks through and changes live.
- **Assessment.** A supervised AI-off check (tracing, a Parsons problem and one debugging task in a locked editor) for 30%, the capstone repository for 50% and the live walkthrough for 20%. Passing needs 70% overall and at least 60% on the AI-off check.
- **Follow-up** (`labs/followup/`): one new validation rule with tests, reviewed by a peer.
- **Left to other courses:** Arabic text normalisation and SQL (FN-104), version control (FN-102).

<!-- academy:labs -->
## Labs

Every lab is a page in `labs/`, opened from the course page and from the lab slide of its session.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Trace eight snippets | [`D1_1_trace_eight_snippets.html`](labs/D1_1_trace_eight_snippets.html) |
| 1.2 | Day 1 · Session 2 | Split a script into four functions | [`D1_2_split_40_line.html`](labs/D1_2_split_40_line.html) |
| 1.3 | Day 1 · Session 3 | Annotate the reading parser | [`D1_3_annotate_supplied_reading.html`](labs/D1_3_annotate_supplied_reading.html) |
| 1.4 | Day 1 · Session 4 | Rebuild a validation function | [`D1_4_reorder_scrambled_lines.html`](labs/D1_4_reorder_scrambled_lines.html) |
| 2.1 | Day 2 · Session 1 | Count readings per meter and district | [`D2_1_count_readings_per.html`](labs/D2_1_count_readings_per.html) |
| 2.2 | Day 2 · Session 2 | Find silent meters and unknown ids | [`D2_2_find_meters_no.html`](labs/D2_2_find_meters_no.html) |
| 2.3 | Day 2 · Session 3 | Stream a large readings file | [`D2_3_stream_large_readings.html`](labs/D2_3_stream_large_readings.html) |
| 2.4 | Day 2 · Session 4 | Model and sort the ticket queue | [`D2_4_model_ticket_as.html`](labs/D2_4_model_ticket_as.html) |
| 3.1 | Day 3 · Session 1 | Write a district summary with phones masked | [`D3_1_load_readings_tickets.html`](labs/D3_1_load_readings_tickets.html) |
| 3.2 | Day 3 · Session 2 | Decode a ticket file that fails | [`D3_2_open_ticket_file.html`](labs/D3_2_open_ticket_file.html) |
| 3.3 | Day 3 · Session 3 | Reject malformed lines with a reason | [`D3_3_reject_malformed_lines.html`](labs/D3_3_reject_malformed_lines.html) |
| 3.4 | Day 3 · Session 4 | Find and fix two seeded defects | [`D3_4_ai_off_find.html`](labs/D3_4_ai_off_find.html) |
| 4.1 | Day 4 · Session 1 | Find the notebook's hidden state | [`D4_1_run_notebook_out.html`](labs/D4_1_run_notebook_out.html) |
| 4.2 | Day 4 · Session 2 | Give the notebook a command line | [`D4_2_move_supplied_notebook.html`](labs/D4_2_move_supplied_notebook.html) |
| 4.3 | Day 4 · Session 3 | Pin the anomaly rule down with tests | [`D4_3_write_five_tests.html`](labs/D4_3_write_five_tests.html) |
| 4.4 | Day 4 · Session 4 | Debug a third defect with the tutor | [`D4_4_get_hints_from.html`](labs/D4_4_get_hints_from.html) |
<!-- /academy:labs -->

## Capstone

A command-line tool that loads, validates and reports on a new synthetic dataset, the utility's maintenance work orders, submitted as a public repository whose README shows the command and its report, then a ten-minute walkthrough with a change the assessor requests

**Submission:** A link to a public repository that holds the tool, its tests and a README that shows the one command and the report it writes on the supplied work-order files, and that states what the tool does not check. The commit history is part of the evidence. Then a ten-minute live walkthrough: the participant runs the tool, makes a change the assessor requests and explains a traceback the assessor chooses; the questions are inside the ten minutes.

**Rubric of the repository:** correctness on hidden tests 30, validation and errors 20, structure and types 20, reproducibility 15, README 15. The brief, the data and a sample of public tests are in `labs/capstone/`.

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
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf and https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf
- SDAIA Generative AI Guidelines: for government, https://sdaia.gov.sa/en/SDAIA/about/Files/GenAIGuidelinesForGovernmentENCompressed.pdf ; for the public, https://sdaia.gov.sa/en/SDAIA/about/Files/GenerativeAIPublicEN.pdf
- SDAIA Data & AI Academic Programs Standards Framework: bridging units SDF-Fundamentals and SDF-Data-Structures at Apply level: https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/Academic-Programs-Standards-Framework-Q3.pdf
