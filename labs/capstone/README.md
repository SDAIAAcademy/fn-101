# Capstone: a tool for the maintenance work orders

Mazen Al-Buqami plans the maintenance crews of Manahil Water Services. Every month he gets an
export of work orders and a list of crews, and every month he cleans it by hand in a
spreadsheet. You build him a command-line tool that loads the export, rejects each bad row
with a reason, and writes the same report on every run.

You may use any tool, an AI assistant included. You own every line: in the walkthrough you run
the tool, change it on request and read a traceback from it, without an assistant.

## The files

| File | What it holds |
|---|---|
| [`data/work_orders.csv`](data/work_orders.csv) | 505 rows: `order_id`, `meter_id`, `crew_id`, `opened`, `closed`, `kind`, `hours`, `note`. UTF-8. An open order has an empty `closed` and an empty `hours`. `note` is free text from the field, in Arabic or English |
| [`data/crews.jsonl`](data/crews.jsonl) | One crew per line: `crew_id`, `district`, `size`. This file is clean |
| [`tests_public/`](tests_public/) | A public sample of the tests, run as `uv run pytest tests_public` from the root of your repository |
| [`TEMPLATE_README.md`](TEMPLATE_README.md) | The README of your repository, to fill in |

All of it is synthetic. Treat `note` as if it were not: field crews write customers' phone
numbers into it. **Nothing from `note` may appear in any output or log.**

## The command

Your repository holds a package named `workorders`, and this command works from its root:

    python -m workorders report --orders data/work_orders.csv --crews data/crews.jsonl --as-of 2026-10-31 --out out

`--as-of` is the day the report is made for. The tool never asks the clock. It writes three
files into the folder given with `--out`, creating the folder if needed, and ends with exit
code 0. If an input file is missing it writes one line to the error stream and ends with exit
code 2, without a traceback.

## The rules

A row is accepted, or rejected with exactly one reason. Apply the rules in this order; the
first that applies gives the reason.

| Reason | When |
|---|---|
| `MISSING_VALUE` | `order_id`, `meter_id`, `crew_id`, `opened` or `kind` is empty; or `closed` is given and `hours` is empty |
| `BAD_DATE` | `opened`, or a given `closed`, is not a date written like `2026-09-30` |
| `CLOSED_BEFORE_OPENED` | `closed` is earlier than `opened` (the same day is fine) |
| `NOT_A_NUMBER` | the order is closed and `hours` is not a number (`2,5` is not a number) |
| `OUT_OF_RANGE` | the order is closed and `hours` is not above 0 and at most 24 |
| `UNKNOWN_KIND` | `kind` is not exactly one of `leak`, `replace_meter`, `inspection`, `reconnect` |
| `UNKNOWN_CREW` | `crew_id` is not in `crews.jsonl` |
| `DUPLICATE` | an earlier accepted row has the same `order_id` |

Accepted plus rejected equals the rows of the file, on every run.

## The three outputs

**`rejections.csv`**: the header `line_no,reason,detail`, then one line per rejected row.
`line_no` is the line of the file, the header being line 1. `detail` says what was wrong, in
words of your choice, without the note.

**`summary.json`**: UTF-8, exactly these keys.

```json
{
  "as_of": "2026-10-31",
  "rows": 505,
  "accepted": 0,
  "rejected": 0,
  "rejected_by_reason": {"BAD_DATE": 0, "DUPLICATE": 0},
  "districts": {
    "Al-Rabwa": {"orders": 0, "open": 0, "closed": 0, "hours": 0.0, "median_days_to_close": 0.0}
  },
  "overdue": ["WO-10002"]
}
```

- The district of an order is the district of its crew. All six districts appear.
- `hours` is the sum over the closed orders of the district, rounded to two decimals.
- `median_days_to_close` is the median of the days from `opened` to `closed` over the closed
  orders of the district, as a number with a decimal point, or `null` if there are none.
- `overdue` lists the ids of the accepted open orders that were opened more than 14 days
  before `--as-of`, sorted.
- `rejected_by_reason` holds the reasons that occurred, with their counts.

**`report.md`**: the same facts for a person: the counts, a table per district, the number of
overdue orders. Its layout is yours. Mazen reads this one.

Two runs on the same files write the same bytes in all three.

## What you submit

A link to a public repository with the package, your own tests, the public sample, and a
README from the template that shows the one command and the report it writes, and says what
the tool does not check. Commit as you go: the history is part of the evidence. Do not commit
an environment, a cache or an output folder.

## How it is scored

| Criterion | Weight | What is looked at |
|---|---:|---|
| Correctness on hidden tests | 30 | Your command, run on files you have not seen: other rows, the same rules and outputs |
| Validation and errors | 20 | One reason per bad row, every line accounted for, specific exceptions, nothing caught and dropped, the exit codes |
| Structure and types | 20 | Small functions with one job, modules that separate loading, rules and reporting, type hints that a strict checker accepts |
| Reproducibility | 15 | One command from a fresh clone, the same bytes on two runs, no clock, no hidden state |
| README | 15 | The command, the report, what is not checked, how to run the tests |

## The walkthrough

Ten minutes, questions included, with no assistant:

1. You run the command from a fresh clone and show the report (about three minutes).
2. The assessor asks for one small change, such as a ninth reason, another threshold for
   overdue, or a new column in the report. You make it live, with a test (about four minutes).
3. The assessor shows you a traceback produced from your code and you read it from the last
   line up: what failed, where, and what you would check first (about three minutes).

## Advice

- Start from the rules table and write one test per reason before the code that passes it.
- The reasons are checked in order for a purpose: a row with an empty date is a missing
  value, not a bad date.
- Build the package the way Miqyas is built. You have read all of it.
- If an assistant wrote a function, trace it with one row by hand before you keep it.
