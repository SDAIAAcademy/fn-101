"""Take in the raw ticket file: accept the good lines, reject the rest with a reason.

    uv run python intake.py     # writes out/rejections.csv

Every line of the input is accounted for: accepted, or in the rejection log with its line
number, a reason code and a detail a person can act on.
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
    """A line that cannot be accepted. reason is a code from the list in the lab."""

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
    if not isinstance(ticket, dict):
        raise Rejected("NOT_OBJECT", f"the line holds a {type(ticket).__name__}, not an object")
    for field in REQUIRED:
        if field not in ticket:
            raise Rejected("MISSING_FIELD", f"{field} is absent")
    if ticket["priority"] not in PRIORITIES:
        raise Rejected("BAD_PRIORITY", f"priority is {ticket['priority']!r}")
    try:
        date.fromisoformat(ticket["opened"])
    except ValueError:
        raise Rejected("BAD_DATE", f"opened is {ticket['opened']!r}") from None
    if not METER_ID.fullmatch(ticket["meter_id"]):
        raise Rejected("BAD_METER_ID", f"meter_id is {ticket['meter_id']!r}")
    if ticket["text"].strip() == "":
        raise Rejected("EMPTY_TEXT", "text is empty")
    return ticket


def intake(path: str) -> tuple[list[dict[str, str]], list[tuple[int, str, str]]]:
    """Read the file: the accepted tickets, and (line number, reason, detail) for each rejected line."""
    accepted: list[dict[str, str]] = []
    rejected: list[tuple[int, str, str]] = []
    with open(path, encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            try:
                accepted.append(parse_ticket(line))
            except Rejected as problem:
                rejected.append((line_no, problem.reason, problem.detail))
    return accepted, rejected


def write_rejections(path: str, rejected: list[tuple[int, str, str]]) -> None:
    """Write the rejection log as CSV with the header line_no,reason,detail."""
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["line_no", "reason", "detail"])
        writer.writerows(rejected)


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
