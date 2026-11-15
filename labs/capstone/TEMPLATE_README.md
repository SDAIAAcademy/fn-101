# Work orders: a report tool for Manahil's maintenance planning

One paragraph: what the tool does, for whom, and from which files.

## Run it

    uv sync
    uv run python -m workorders report --orders data/work_orders.csv --crews data/crews.jsonl --as-of 2026-10-31 --out out

What appears in `out/`, in one line per file.

## The report on the supplied files

Paste `out/report.md` here as it is written by the command above, and the three numbers from
`out/summary.json`: rows, accepted, rejected.

## The rules

The eight reasons in the order the tool applies them, each with one example row from the
supplied file (line number and what was wrong, never the note).

## What the tool does not check

Be specific. For example: whether a meter id exists, whether a crew works in the district of
the meter, whether hours are plausible for the kind of work.

## Tests

    uv run pytest

How many tests, what they cover (one line per rule is a good shape), and what they do not.

## How it is built

The modules and what each is responsible for, in a few lines. One decision you took and why.

## Use of AI tools

Which assistant or model you used, for what, and one place where you changed or rejected what
it proposed.
