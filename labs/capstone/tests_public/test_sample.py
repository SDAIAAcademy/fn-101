"""The public sample of the capstone's tests.

Copy this folder into your repository and run it from the repository's root:

    uv run pytest tests_public

It runs your tool as the assessor will, as a command, on the supplied files. The hidden tests
make the same checks, and more of them, on files you have not seen: other rows, the same
rules. Passing this sample means the contract is met on this file, and no more than that.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REASONS = {"MISSING_VALUE", "BAD_DATE", "CLOSED_BEFORE_OPENED", "NOT_A_NUMBER", "OUT_OF_RANGE",
           "UNKNOWN_KIND", "UNKNOWN_CREW", "DUPLICATE"}
OUTPUTS = ["report.md", "summary.json", "rejections.csv"]


def run(out: str, orders: str = "data/work_orders.csv") -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-m", "workorders", "report", "--orders", orders,
               "--crews", "data/crews.jsonl", "--as-of", "2026-10-31", "--out", out]
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)


def outputs() -> dict[str, bytes]:
    with tempfile.TemporaryDirectory() as out:
        done = run(out)
        assert done.returncode == 0, done.stderr
        return {name: (Path(out) / name).read_bytes() for name in OUTPUTS}


def test_every_row_is_accounted_for():
    summary = json.loads(outputs()["summary.json"])
    assert summary["rows"] == 505
    assert summary["accepted"] + summary["rejected"] == summary["rows"]
    assert summary["accepted"] == 447


def test_rejections_carry_one_of_the_eight_reasons():
    files = outputs()
    summary = json.loads(files["summary.json"])
    rows = list(csv.reader(files["rejections.csv"].decode("utf-8").splitlines()))
    assert rows[0] == ["line_no", "reason", "detail"]
    assert len(rows) - 1 == summary["rejected"]
    assert {row[1] for row in rows[1:]} <= REASONS
    assert summary["rejected_by_reason"]["DUPLICATE"] == 10
    assert sum(summary["rejected_by_reason"].values()) == summary["rejected"]


def test_the_summary_has_the_six_districts_and_the_overdue_list():
    summary = json.loads(outputs()["summary.json"])
    assert len(summary["districts"]) == 6
    assert set(summary["districts"]["Al-Rabwa"]) == {"orders", "open", "closed", "hours", "median_days_to_close"}
    assert sum(d["orders"] for d in summary["districts"].values()) == summary["accepted"]
    assert summary["overdue"] == sorted(summary["overdue"])


def test_two_runs_write_the_same_bytes():
    assert outputs() == outputs()


def test_no_output_holds_a_phone_number():
    for name, content in outputs().items():
        assert not re.search(rb"\d{9,}", content), name


def test_a_missing_file_ends_with_exit_code_2_and_no_traceback():
    with tempfile.TemporaryDirectory() as out:
        done = run(out, orders="data/no_such_file.csv")
    assert done.returncode == 2
    assert "Traceback" not in done.stderr
