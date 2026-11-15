"""Take in the raw ticket file: accept the good lines, reject the rest with a reason.

    uv run python intake.py     # writes out/rejections.csv

The rule of the house: every line of the input is accounted for. A line is either accepted
or it is in the rejection log with its line number, a reason code and a detail a person can
act on. Nothing crashes the run, and nothing disappears.

Reason codes, checked in this order:
    EMPTY_LINE     the line is empty or only spaces
    BAD_JSON       the line is not valid JSON
    NOT_OBJECT     the line is JSON, and not an object (a list, a number, ...)
    MISSING_FIELD  one of the REQUIRED fields is absent
    BAD_PRIORITY   priority is not one of PRIORITIES
    BAD_DATE       opened is not a real date written as YYYY-MM-DD
    BAD_METER_ID   meter_id is not "M-" followed by four digits
    EMPTY_TEXT     text is empty or only spaces
"""

import csv
import json
import re
from datetime import date
from pathlib import Path

REQUIRED = ["ticket_id", "opened", "district", "meter_id", "priority", "status", "text"]
PRIORITIES = {"urgent", "high", "normal", "low"}
METER_ID = re.compile(r"M-[0-9]{4}")
PATH = "data/tickets_raw.jsonl"


class Rejected(Exception):
    """A line that cannot be accepted. reason is a code from the list above."""

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail


def parse_ticket(line: str) -> dict[str, str]:
    """Turn one line into a ticket, or raise Rejected with the first reason that applies."""
    if line.strip() == "":
        raise Rejected("EMPTY_LINE", "the line is empty")
    try:
        ticket = json.loads(line)
    except json.JSONDecodeError as problem:
        raise Rejected("BAD_JSON", f"{problem.msg} at character {problem.pos}") from None
    # Step 1: the six remaining checks, in the order of the list above.
    # Use date.fromisoformat for the date and METER_ID.fullmatch for the meter id.
    return ticket


def intake(path: str) -> tuple[list[dict[str, str]], list[tuple[int, str, str]]]:
    """Read the file: the accepted tickets, and (line number, reason, detail) for each rejected line."""
    accepted: list[dict[str, str]] = []
    rejected: list[tuple[int, str, str]] = []
    # Step 2: open the file as UTF-8, number the lines from 1, call parse_ticket on each,
    # and catch Rejected (and only Rejected) around that one call.
    return accepted, rejected


def write_rejections(path: str, rejected: list[tuple[int, str, str]]) -> None:
    """Write the rejection log as CSV with the header line_no,reason,detail."""
    raise NotImplementedError("step 3: csv.writer, newline='' and encoding named")


def main() -> None:
    accepted, rejected = intake(PATH)
    with open(PATH, encoding="utf-8") as file:
        lines = sum(1 for _ in file)
    Path("out").mkdir(exist_ok=True)
    write_rejections("out/rejections.csv", rejected)
    print(f"{lines} lines: {len(accepted)} accepted, {len(rejected)} rejected")
    assert len(accepted) + len(rejected) == lines, "a line is not accounted for"
    counts: dict[str, int] = {}
    for _, reason, _ in rejected:
        counts[reason] = counts.get(reason, 0) + 1
    for reason, count in sorted(counts.items()):
        print(f"  {reason:14} {count}")


if __name__ == "__main__":
    main()
