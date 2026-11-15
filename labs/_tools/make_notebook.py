"""Write Salma's analysis notebook: the stale one lab 4.1 starts from, and the repaired one.

    uv run labs/_tools/make_notebook.py

The saved outputs and execution counts are not typed in: the cells are run here, in the order
a real session ran them (one cell later deleted, one "what if" cell run before going back),
and what each cell last printed is what the file keeps. Standard library only.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LABS / "kit"))

import data  # noqa: E402

TITLE = ("# September readings: anomalies\n\n"
         "Salma's working notebook for the monthly check. It reads the month's file and the meter "
         "registry from `data/`, keeps the valid readings, and lists the readings that are far above "
         "what their meter usually shows.")
LOAD = '''import csv
from datetime import date
from statistics import median

with open("data/meters.csv", encoding="utf-8", newline="") as file:
    district_of = {row["meter_id"]: row["district"] for row in csv.DictReader(file)}
with open("data/readings_2026_09.csv", encoding="utf-8", newline="") as file:
    rows = list(csv.DictReader(file))
print(len(rows), "rows,", len(district_of), "meters")'''
KNOWN = 'known = set(district_of)'
CLEAN = '''readings = []          # (meter_id, date, m3) for every row that is kept
seen = set()
for row in rows:
    try:
        m3 = float(row["consumption_m3"])
        date.fromisoformat(row["date"])
    except ValueError:
        continue
    key = (row["meter_id"], row["date"])
    if not 0 <= m3 <= 200 or row["meter_id"] not in known or key in seen:
        continue
    seen.add(key)
    readings.append((row["meter_id"], row["date"], m3))
print(len(readings), "readings kept")'''
FACTOR = 'factor = 3.0       # a reading is an anomaly above this many times its meter\'s median'
FIND = '''by_meter = {}
for meter_id, day, m3 in readings:
    by_meter.setdefault(meter_id, []).append(m3)
anomalies = [(meter_id, day, m3) for meter_id, day, m3 in readings
             if m3 > factor * median(by_meter[meter_id])]
print(len(anomalies), "anomalies")'''
TABLE = '''per_district = {}
for meter_id, day, m3 in anomalies:
    district = district_of[meter_id]
    per_district[district] = per_district.get(district, 0) + 1
for district in sorted(per_district):
    print(f"{district:15} {per_district[district]}")'''
WHAT_IF_TITLE = "## What if we were stricter?\n\nTry a lower factor and look at the count again."
WHAT_IF = 'factor = 2.0'
WHAT_IF_FIXED_TITLE = ("## What if we were stricter?\n\nA second question gets a second name. "
                       "`factor` is set in one cell only, so every cell above means the same thing on every run.")
WHAT_IF_FIXED = '''strict_factor = 2.0
strict = [(meter_id, day, m3) for meter_id, day, m3 in readings
          if m3 > strict_factor * median(by_meter[meter_id])]
print(len(strict), "anomalies at the stricter factor")'''


def session(order: list[str], cells: dict[str, str]) -> dict[str, tuple[int, str]]:
    """Run the named cells in this order; return, per cell, its last execution count and output."""
    scope: dict[str, object] = {}
    last: dict[str, tuple[int, str]] = {}
    for count, name in enumerate(order, start=1):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            exec(cells[name], scope)
        last[name] = (count, out.getvalue())
    return last


def markdown(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(source: str, run: tuple[int, str] | None) -> dict:
    outputs = []
    if run and run[1]:
        outputs.append({"name": "stdout", "output_type": "stream", "text": run[1].splitlines(keepends=True)})
    return {"cell_type": "code", "execution_count": run[0] if run else None, "metadata": {},
            "outputs": outputs, "source": source.splitlines(keepends=True)}


def notebook(cells: list[dict]) -> str:
    book = {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}
    for n, cell in enumerate(cells):
        cell["id"] = f"cell-{n:02d}"
    return json.dumps(book, ensure_ascii=False, indent=1) + "\n"


def main() -> int:
    cells = {"load": LOAD, "known": KNOWN, "clean": CLEAN, "factor": FACTOR, "find": FIND, "table": TABLE,
             "what_if": WHAT_IF, "what_if_fixed": WHAT_IF_FIXED}
    here = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        for name in ("meters", "readings"):
            data.write(name, Path(tmp))
        os.chdir(tmp)
        try:
            # The session that left the notebook stale: the cell that defined `known` was run and
            # later deleted; the what-if cell was run, then the two cells above it were run again.
            stale = session(["load", "known", "clean", "factor", "find", "table", "what_if", "find", "table"], cells)
            fixed = session(["load", "known", "clean", "factor", "find", "table", "what_if_fixed"], cells)
        finally:
            os.chdir(here)
    assert stale["find"][1] == "27 anomalies\n" and fixed["find"][1] == "18 anomalies\n", (stale["find"], fixed["find"])
    start = notebook([markdown(TITLE), code(LOAD, stale["load"]), code(CLEAN, stale["clean"]),
                      code(FACTOR, stale["factor"]), code(FIND, stale["find"]), code(TABLE, stale["table"]),
                      markdown(WHAT_IF_TITLE), code(WHAT_IF, stale["what_if"])])
    done = notebook([markdown(TITLE), code(LOAD, fixed["load"]), code(KNOWN, fixed["known"]),
                     code(CLEAN, fixed["clean"]), code(FACTOR, fixed["factor"]), code(FIND, fixed["find"]),
                     code(TABLE, fixed["table"]), markdown(WHAT_IF_FIXED_TITLE),
                     code(WHAT_IF_FIXED, fixed["what_if_fixed"])])
    for path, text in ((LABS / "kit" / "start" / "4.1" / "analysis.ipynb", start),
                       (LABS / "solutions" / "4.1" / "analysis.ipynb", done),
                       (LABS / "kit" / "start" / "4.2" / "analysis.ipynb", done)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    print("stale:", {k: (v[0], v[1].strip()[:40]) for k, v in stale.items()})
    print("fixed:", {k: (v[0], v[1].strip()[:40]) for k, v in fixed.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
