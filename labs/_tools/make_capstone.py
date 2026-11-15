"""Write the capstone's dataset: maintenance work orders with planted problems.

    uv run labs/_tools/make_capstone.py                       # the public files, into labs/capstone/data/
    uv run labs/_tools/make_capstone.py --seed 7 --to <folder> --expected

The first form rewrites the files every participant starts from. The second is for the
assessor: another seed gives another dataset under the same rules, and --expected also writes
expected.json, the summary a correct tool must produce (as-of date included). Keep that
folder outside any public repository: it is the hidden test. labs/_tools/grade_capstone.py
runs a submission against it.

The expected summary is computed here from the rows as they are generated, not by a tool
under test. Standard library only; the same seed gives the same bytes on every machine.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent / "capstone" / "data"

DISTRICTS = ["Al-Rabwa", "Al-Yasmin", "Al-Faisaliyah", "Al-Naseem", "Al-Murooj", "Al-Khuzama"]
KINDS = ["leak", "replace_meter", "inspection", "reconnect"]
REASONS = ["MISSING_VALUE", "BAD_DATE", "CLOSED_BEFORE_OPENED", "NOT_A_NUMBER", "OUT_OF_RANGE",
           "UNKNOWN_KIND", "UNKNOWN_CREW", "DUPLICATE"]
NOTES = ["", "", "", "valve stiff, replaced", "customer not at home, came back next day",
         "تم استبدال العداد", "تسرب عند الوصلة، تم الإصلاح", "no access to the meter box, gate locked",
         "العميل طلب الاتصال قبل الزيارة", "seal broken, reported to the supervisor"]
AS_OF = date(2026, 10, 31)
FIRST_DAY = date(2026, 9, 1)
OVERDUE_DAYS = 14


class Dice:
    """A small generator of our own, so that the files do not depend on a Python version."""

    def __init__(self, seed: int) -> None:
        self.state = (seed * 2654435761 + 97) % 2**32

    def below(self, n: int) -> int:
        self.state = (self.state * 1664525 + 1013904223) % 2**32
        return (self.state >> 8) % n

    def pick(self, items: list[str]) -> str:
        return items[self.below(len(items))]


def median(values: list[int]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    return float(ordered[middle]) if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2


def build(seed: int) -> tuple[str, str, dict[str, object]]:
    dice = Dice(seed)
    crews = [{"crew_id": f"C-{n + 1:02d}", "district": DISTRICTS[n % 6], "size": 2 + dice.below(3)} for n in range(9)]
    district_of = {str(c["crew_id"]): str(c["district"]) for c in crews}
    good = 420 + dice.below(60)
    rows: list[list[str]] = []
    facts: list[tuple[str, str, date, date | None, float]] = []     # crew, order id, opened, closed, hours
    for n in range(good):
        order_id = f"WO-{10001 + n}"
        crew = dice.pick(sorted(district_of))
        opened = FIRST_DAY + timedelta(days=dice.below(55))
        is_open = dice.below(100) < 22
        closed = None if is_open else min(opened + timedelta(days=dice.below(12)), AS_OF)
        hours = 0.0 if is_open else (2 + dice.below(30)) / 4
        note = dice.pick(NOTES)
        if dice.below(100) < 4:           # a phone number left in a note by a field crew
            note = (note + " " if note else "") + f"call 05550{dice.below(100000):05d}"
        rows.append([order_id, f"M-{1 + dice.below(600):04d}", crew, opened.isoformat(),
                     closed.isoformat() if closed else "", dice.pick(KINDS), "" if is_open else f"{hours:g}", note])
        facts.append((crew, order_id, opened, closed, hours))
    # The planted problems: each bad row breaks one rule only, so its reason does not depend on
    # the order in which a tool applies the rules.
    planted: list[tuple[list[str], str]] = []

    def bad(reason: str, count: int) -> None:
        for _ in range(count):
            row = list(rows[dice.below(good)])
            row[0] = f"WO-{20001 + len(planted)}"
            if reason == "MISSING_VALUE":
                row[[1, 2, 3, 5][dice.below(4)]] = ""
            elif reason == "BAD_DATE":
                row[3] = dice.pick(["31/09/2026", "2026-13-01", "yesterday", "2026-02-30"])
            elif reason == "CLOSED_BEFORE_OPENED":
                row[4] = (date.fromisoformat(row[3]) - timedelta(days=1 + dice.below(5))).isoformat()
                row[6] = row[6] or "2"
            elif reason == "NOT_A_NUMBER":
                row[4] = row[4] or row[3]
                row[6] = dice.pick(["2,5", "two", "N/A", "3h"])
            elif reason == "OUT_OF_RANGE":
                row[4] = row[4] or row[3]
                row[6] = dice.pick(["0", "-1.5", "24.5", "80"])
            elif reason == "UNKNOWN_KIND":
                row[5] = dice.pick(["Leak", "repair", "meter", "inspect"])
            elif reason == "UNKNOWN_CREW":
                row[2] = dice.pick(["C-00", "C-17", "crew 3", "c-01"])
            elif reason == "DUPLICATE":
                row[0] = rows[dice.below(good)][0]
            planted.append((row, reason))

    for reason, least in zip(REASONS, [9, 6, 5, 7, 6, 5, 4, 8]):
        bad(reason, least + dice.below(4))
    # Mix the bad rows in. A duplicate must come after the row it repeats, so the first wins.
    lines = [(row, "") for row in rows]
    for row, reason in planted:
        first = next(i for i, (other, _) in enumerate(lines) if other[0] == row[0]) + 1 if reason == "DUPLICATE" else 0
        lines.insert(first + dice.below(len(lines) - first + 1), (row, reason))
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["order_id", "meter_id", "crew_id", "opened", "closed", "kind", "hours", "note"])
    writer.writerows(row for row, _ in lines)
    crews_text = "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in crews)

    by_reason = {reason: sum(1 for _, r in lines if r == reason) for reason in REASONS}
    districts: dict[str, dict[str, object]] = {}
    for district in sorted(DISTRICTS):
        mine = [f for f in facts if district_of[f[0]] == district]
        done = [f for f in mine if f[3] is not None]
        districts[district] = {
            "orders": len(mine), "open": len(mine) - len(done), "closed": len(done),
            "hours": round(sum(f[4] for f in done), 2),
            "median_days_to_close": median([(f[3] - f[2]).days for f in done if f[3] is not None]),
        }
    overdue = sorted(f[1] for f in facts if f[3] is None and (AS_OF - f[2]).days > OVERDUE_DAYS)
    expected: dict[str, object] = {
        "as_of": AS_OF.isoformat(), "rows": len(lines), "accepted": good, "rejected": len(planted),
        "rejected_by_reason": by_reason, "districts": districts, "overdue": overdue,
        "rejections": {str(n): reason for n, (_, reason) in enumerate(lines, start=2) if reason},
    }
    return out.getvalue(), crews_text, expected


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the capstone's dataset.")
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--to", type=Path, default=PUBLIC)
    parser.add_argument("--expected", action="store_true", help="also write expected.json (the assessor's key)")
    args = parser.parse_args()
    orders, crews, expected = build(args.seed)
    args.to.mkdir(parents=True, exist_ok=True)
    (args.to / "work_orders.csv").write_text(orders, encoding="utf-8", newline="\n")
    (args.to / "crews.jsonl").write_text(crews, encoding="utf-8", newline="\n")
    if args.expected:
        (args.to / "expected.json").write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
    reasons = expected["rejected_by_reason"]
    print(f"{args.to.name}: {expected['rows']} rows, {expected['accepted']} accepted, {expected['rejected']} rejected {reasons}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
