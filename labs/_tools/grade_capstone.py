"""Run a capstone submission against a hidden dataset: the "correctness on hidden tests" part.

    uv run labs/_tools/make_capstone.py --seed <your seed> --to <hidden folder> --expected
    uv run labs/_tools/grade_capstone.py <the participant's repository> <hidden folder>

The hidden folder holds work_orders.csv, crews.jsonl and expected.json, written by
make_capstone.py with a seed the participants have not seen. This script runs the
participant's command on those files, in the participant's repository, and compares what it
writes with expected.json, one line per check. The last line is the share of checks passed;
how that share becomes the 30 points of the rubric is the assessor's decision.

It runs the participant's code: use a machine and an account you would run a stranger's
script on. Standard library only; the repository's own Python environment is used when it has
one (uv run), otherwise this Python.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(repo: Path, hidden: Path, out: Path, as_of: str, orders: str = "work_orders.csv") -> subprocess.CompletedProcess[str]:
    python = ["uv", "run", "python"] if (repo / "pyproject.toml").is_file() and shutil.which("uv") else [sys.executable]
    command = [*python, "-m", "workorders", "report", "--orders", str(hidden / orders),
               "--crews", str(hidden / "crews.jsonl"), "--as-of", as_of, "--out", str(out)]
    return subprocess.run(command, cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          check=False, timeout=300)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    repo, hidden = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    expected = json.loads((hidden / "expected.json").read_text(encoding="utf-8"))
    checks: list[tuple[bool, str]] = []

    def check(ok: object, what: str) -> None:
        checks.append((bool(ok), what))

    with tempfile.TemporaryDirectory() as tmp:
        first, second = Path(tmp) / "a", Path(tmp) / "b"
        done = run(repo, hidden, first, expected["as_of"])
        check(done.returncode == 0, "the command ends with exit code 0")
        try:
            summary = json.loads((first / "summary.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            summary = {}
        check(summary, "summary.json is written and is valid JSON")
        for key in ("rows", "accepted", "rejected"):
            check(summary.get(key) == expected[key], f"{key} is {expected[key]}")
        for reason, count in expected["rejected_by_reason"].items():
            check(summary.get("rejected_by_reason", {}).get(reason, 0) == count, f"{count} rows rejected as {reason}")
        for district, wanted in expected["districts"].items():
            got = summary.get("districts", {}).get(district, {})
            check({k: got.get(k) for k in ("orders", "open", "closed")} == {k: wanted[k] for k in ("orders", "open", "closed")},
                  f"{district}: orders, open and closed")
            check(isinstance(got.get("hours"), (int, float)) and abs(got["hours"] - wanted["hours"]) < 0.01,
                  f"{district}: hours")
            check(got.get("median_days_to_close") == wanted["median_days_to_close"], f"{district}: median days to close")
        check(summary.get("overdue") == expected["overdue"], f"the {len(expected['overdue'])} overdue orders, sorted")
        try:
            with open(first / "rejections.csv", encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))
        except OSError:
            rows = []
        check(rows[:1] == [["line_no", "reason", "detail"]], "rejections.csv has the header line_no, reason, detail")
        check({row[0]: row[1] for row in rows[1:] if len(row) >= 2} == expected["rejections"],
              "every rejected line is listed with its line number and its reason")
        check(all(len(row) >= 3 and row[2].strip() for row in rows[1:]), "every rejection has a detail")
        written = {p.name: p.read_bytes() for p in sorted(first.glob("*")) if p.is_file()}
        check(not any(re.search(rb"\d{9,}", content) for content in written.values()), "no output holds a phone number")
        check((first / "report.md").is_file(), "report.md is written")
        run(repo, hidden, second, expected["as_of"])
        check(written and written == {p.name: p.read_bytes() for p in sorted(second.glob("*")) if p.is_file()},
              "a second run writes the same bytes")
        done = run(repo, hidden, Path(tmp) / "c", expected["as_of"], orders="no_such_file.csv")
        check(done.returncode == 2 and "Traceback" not in done.stderr, "a missing file: exit code 2 and no traceback")
    for ok, what in checks:
        print("ok  " if ok else "FAIL", what)
    passed = sum(1 for ok, _ in checks if ok)
    print(f"{passed} of {len(checks)} checks pass ({100 * passed // len(checks)}%)")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
