---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
deck: "capstone"
day: 5
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/slides/capstone.html"
---

# Python for Data and AI Work

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
