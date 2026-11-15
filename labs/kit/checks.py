"""The evidence each lab asks for, checked by running your code.

Every check runs your files in a separate Python process, so a crash in your code is a
message here and not a crash of the check. The expected values are computed from the data
generator, never typed in.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import data
import labtool

KIT = Path(__file__).resolve().parent


class Report:
    def __init__(self) -> None:
        self.lines: list[tuple[bool, str]] = []

    def need(self, ok: object, good: str, bad: str = "") -> bool:
        self.lines.append((bool(ok), good if ok else (bad or "missing: " + good)))
        return bool(ok)

    @property
    def failed(self) -> int:
        return sum(1 for ok, _ in self.lines if not ok)


def py(folder: Path, *args: str, timeout: int = 300) -> tuple[int, str]:
    """Run Python in the lab folder; return the exit code and everything it printed."""
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        done = subprocess.run([sys.executable, *args], cwd=folder, env=env, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, f"stopped after {timeout} seconds"
    return done.returncode, (done.stdout + done.stderr).strip()


def probe(folder: Path, code: str, timeout: int = 300) -> tuple[object, str]:
    """Run a short script in the lab folder; it prints one JSON value on its last line."""
    status, output = py(folder, "-c", "import json, sys\nsys.path.insert(0, '')\n" + code, timeout=timeout)
    if status != 0:
        return None, output.splitlines()[-1] if output else f"exit code {status}"
    try:
        return json.loads(output.splitlines()[-1]), ""
    except (ValueError, IndexError):
        return None, "your code printed something the check could not read"


def last(output: str) -> str:
    return output.splitlines()[-1] if output else ""


def text_of(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def unchanged(r: Report, folder: Path, lab: str, name: str) -> bool:
    """A supplied file (tests, usually) must be the one the kit wrote."""
    kit = (KIT / "start" / lab / name).read_bytes().replace(b"\r\n", b"\n")
    mine = (folder / name).read_bytes().replace(b"\r\n", b"\n") if (folder / name).is_file() else b""
    return r.need(kit == mine, f"{name} is the supplied file",
                  f"{name} was changed or is missing: restore it (it is in the kit) and change your code instead")


def tests(r: Report, folder: Path, what: str, label: str = "") -> bool:
    status, output = py(folder, "-m", "pytest", "-q", "-p", "no:cacheprovider", *what.split())
    return r.need(status == 0, f"{label or what}: the tests pass ({last(output)})",
                  f"{label or what}: the tests do not pass: {last(output)}")


def typed(r: Report, folder: Path, what: str) -> bool:
    status, output = py(folder, "-m", "mypy", "--strict", "--no-incremental", *what.split())
    return r.need(status == 0, f"{what}: the type checker is satisfied in strict mode",
                  f"{what}: the type checker reports: {last(output)} (run: uv run mypy --strict {what})")


def words(text: str) -> int:
    return len(re.findall(r"\w+", text))


def section_filled(text: str, heading: str, least: int = 4) -> bool:
    """Is there something written under a Markdown heading that starts with these words?"""
    match = re.search(rf"^#+\s*{re.escape(heading)}.*?\n(.*?)(?=^#+\s|\Z)", text, re.I | re.M | re.S)
    body = re.sub(r"<!--.*?-->", "", match.group(1), flags=re.S) if match else ""
    return words(body) >= least


# ------------------------------------------------------------------------------------ day 1

def norm(text: str) -> str:
    return re.sub(r"\s+", "", text.replace('"', "'"))


def check_1_1(folder: Path, r: Report) -> None:
    expected = {}
    for n in range(1, 9):
        _, output = py(folder, str(KIT / "start" / "1.1" / "snippets" / f"s{n}.py"))
        expected[f"s{n}"] = " / ".join(output.splitlines())
    answers = dict(re.findall(r"^(s\d)\s*:[ \t]*(.*)$", text_of(folder / "predictions.txt"), re.M))
    given = [k for k in expected if answers.get(k, "").strip()]
    r.need(len(given) == 8, "predictions.txt has an answer for all eight snippets",
           f"predictions.txt has {len(given)} of 8 answers")
    wrong = [k for k in given if norm(answers[k]) != norm(expected[k])]
    notes = dict(re.findall(r"^(s\d)\s*:[ \t]*(.*)$", text_of(folder / "misread.md"), re.M))
    r.need(True, f"{len(given) - len(wrong)} of {len(given)} predictions match what Python prints"
           + (f"; not matching: {', '.join(wrong)}" if wrong else ""))
    missing = [k for k in wrong if words(notes.get(k, "")) < 4]
    r.need(not missing, "misread.md says, for each wrong prediction, which line was misread",
           f"misread.md needs a line for: {', '.join(missing)} (which line did you misread, and how?)")


def check_1_2(folder: Path, r: Report) -> None:
    unchanged(r, folder, "1.2", "test_bill.py")
    tests(r, folder, "test_bill.py")
    status, output = py(folder, "-c", "import monthly_bill")
    r.need(status == 0 and output == "", "importing monthly_bill prints nothing and runs nothing",
           "importing monthly_bill still prints or fails: the script part belongs under if __name__ == \"__main__\":")
    found, why = probe(folder, "import monthly_bill as m\n"
                       "print(json.dumps({n: bool(getattr(getattr(m, n, None), '__doc__', None)) "
                       "for n in ['load_rows', 'clean', 'bill', 'format_bill']}))")
    if r.need(isinstance(found, dict), "monthly_bill can be imported", f"monthly_bill cannot be imported: {why}"):
        assert isinstance(found, dict)
        bare = [n for n, has in found.items() if not has]
        r.need(not bare, "the four functions each have a docstring that states inputs and output",
               f"no docstring (or no function) for: {', '.join(bare)}")
    with tempfile.TemporaryDirectory() as tmp:
        original = Path(tmp) / "original.py"
        shutil.copy(KIT / "start" / "1.2" / "monthly_bill.py", original)
        _, before = py(folder, str(original))
    _, after = py(folder, "monthly_bill.py")
    r.need(before == after and before, "the script prints the same bill as before the change",
           "the script no longer prints the same bill as the original: compare the two outputs line by line")


def check_1_3(folder: Path, r: Report) -> None:
    unchanged(r, folder, "1.3", "test_parser.py")
    tests(r, folder, "test_parser.py")
    status, output = py(folder, "-m", "mypy", "--strict", "--no-incremental", "parser.py")
    r.need(status == 0, f"the type checker is satisfied in strict mode ({last(output)})",
           f"the type checker reports: {last(output)}")
    source = text_of(folder / "parser.py")
    r.need("type: ignore" not in source and not re.search(r"\bAny\b", source),
           "no error was silenced: no 'type: ignore' and no Any",
           "an error was silenced with 'type: ignore' or Any: fix the code the checker points at")


DISTRACTORS = {"warmup.py": ["total = value"],
               "validate.py": ["if value < 0 and value > 200:", "except TypeError:", "value = float(row)"]}


def check_1_4(folder: Path, r: Report) -> None:
    for name, test in (("warmup.py", "test_warmup.py"), ("validate.py", "test_validate.py")):
        unchanged(r, folder, "1.4", test)
        tests(r, folder, test)
        supplied = {line.strip() for line in text_of(KIT / "start" / "1.4" / name).splitlines()}
        mine = [line.strip() for line in text_of(folder / name).splitlines()
                if line.strip() and not line.strip().startswith("#")]
        added = [line for line in mine if line not in supplied]
        r.need(not added, f"{name} uses only the supplied lines",
               f"{name} has a line that was not supplied: {added[0] if added else ''}")
        used = [line for line in DISTRACTORS[name] if line in mine]
        r.need(not used, f"{name} leaves the distractors out",
               f"{name} still holds a distractor: {used[0] if used else ''}")


# ------------------------------------------------------------------------------------ day 2

def district_of() -> dict[str, str]:
    return {m["meter_id"]: m["district"] for m in data.meters()}


LOAD = ("import csv\n"
        "def rows(path):\n"
        "    with open(path, encoding='utf-8', newline='') as f:\n"
        "        return list(csv.DictReader(f))\n")


def check_2_1(folder: Path, r: Report) -> None:
    typed(r, folder, "count.py")
    clean = data.readings_clean()
    per_meter: dict[str, int] = {}
    per_district: dict[str, int] = {}
    where = district_of()
    for row in clean:
        per_meter[row["meter_id"]] = per_meter.get(row["meter_id"], 0) + 1
        per_district[where[row["meter_id"]]] = per_district.get(where[row["meter_id"]], 0) + 1
    found, why = probe(folder, LOAD + "import count, time\n"
                       "readings = rows('data/readings_clean.csv'); meters = rows('data/meters.csv')\n"
                       "large = rows('data/readings_large.csv')\n"
                       "a = dict(count.count_per_meter(readings)); b = dict(count.count_per_district(readings, meters))\n"
                       "t = time.perf_counter(); count.count_per_district(large, meters); t = time.perf_counter() - t\n"
                       "print(json.dumps([a, b, t]))")
    if not r.need(isinstance(found, list), "count.py runs", f"count.py does not run yet: {why}"):
        return
    assert isinstance(found, list)
    r.need(found[0] == per_meter, f"count_per_meter is right for all {len(per_meter)} meters",
           "count_per_meter does not give the expected counts (M-0001 should have "
           f"{per_meter.get('M-0001')})")
    r.need(found[1] == per_district, "count_per_district is right for the six districts",
           f"count_per_district does not give the expected counts: {found[1]}")
    r.need(found[2] < 2.0, f"count_per_district takes {found[2]:.2f} seconds on 100,000 rows",
           f"count_per_district takes {found[2]:.1f} seconds on 100,000 rows: is there still a loop inside the loop?")
    times = dict(re.findall(r"^(nested|dictionary)\s*:\s*([0-9.]+)", text_of(folder / "timings.txt"), re.M))
    r.need(len(times) == 2 and float(times["nested"]) > float(times["dictionary"]),
           "timings.txt holds both timings, and the nested loop is the slower one",
           "timings.txt is missing or incomplete: run timing.py")


def check_2_2(folder: Path, r: Report) -> None:
    typed(r, folder, "coverage_report.py")
    known = {m["meter_id"] for m in data.meters()}
    month = data.readings_month()
    reading_ids = {row["meter_id"] for row in month}
    seen: set[tuple[str, str]] = set()
    repeated: set[tuple[str, str]] = set()
    for row in month:
        key = (row["meter_id"], row["date"])
        (repeated if key in seen else seen).add(key)
    found, why = probe(folder, LOAD + "import coverage_report as c\n"
                       "readings = rows('data/readings_2026_09.csv'); meters = rows('data/meters.csv')\n"
                       "print(json.dumps([list(c.silent_meters(readings, meters)), list(c.unknown_meters(readings, meters)),"
                       " sorted(list(k) for k in c.repeated_keys(readings))]))")
    if not r.need(isinstance(found, list), "coverage_report.py runs", f"coverage_report.py does not run yet: {why}"):
        return
    assert isinstance(found, list)
    r.need(found[0] == sorted(known - reading_ids), f"silent_meters finds the {len(known - reading_ids)} meters, sorted",
           f"silent_meters returns {len(found[0])} meters; expected {len(known - reading_ids)}, sorted")
    r.need(found[1] == sorted(reading_ids - known), f"unknown_meters finds the {len(reading_ids - known)} ids, sorted",
           f"unknown_meters returns {found[1][:6]}; expected {len(reading_ids - known)} ids, sorted")
    r.need(found[2] == sorted(list(k) for k in repeated), f"repeated_keys finds the {len(repeated)} repeated (meter, date) pairs",
           f"repeated_keys returns {len(found[2])} pairs; expected {len(repeated)}")
    source = text_of(folder / "coverage_report.py")
    r.need(not re.search(r"for .*:\s*\n\s+for ", source), "no loop inside a loop",
           "there is a loop inside a loop: a set answers 'is it in there?' without one")


def check_2_3(folder: Path, r: Report) -> None:
    typed(r, folder, "stream.py")
    total = sum(float(row["consumption_m3"]) for row in data.readings_large())
    found, why = probe(folder, "import inspect, tracemalloc, stream\n"
                       "path = 'data/readings_large.csv'\n"
                       "gen = inspect.isgeneratorfunction(stream.read_values)\n"
                       "tracemalloc.start(); a = stream.total_stream(path); _, p1 = tracemalloc.get_traced_memory(); tracemalloc.stop()\n"
                       "tracemalloc.start(); b = stream.total_list(path); _, p2 = tracemalloc.get_traced_memory(); tracemalloc.stop()\n"
                       "print(json.dumps([gen, a, b, p1, p2]))")
    if not r.need(isinstance(found, list), "stream.py runs", f"stream.py does not run yet: {why}"):
        return
    assert isinstance(found, list)
    gen, a, b, p1, p2 = found
    r.need(gen, "read_values is a generator function", "read_values does not yield: it still builds and returns a list")
    r.need(abs(a - total) < 1e-6 and abs(b - total) < 1e-6, f"both totals are {total:.3f} m3",
           f"the totals differ from the expected {total:.3f}: stream {a}, list {b}")
    r.need(p1 * 20 < p2, f"peak memory: stream {p1 / 1024:.0f} KiB, list {p2 / 1024:.0f} KiB",
           f"the stream's peak ({p1 / 1024:.0f} KiB) is not far below the list's ({p2 / 1024:.0f} KiB): something still holds every row")
    r.need(re.search(r"stream.*\d", text_of(folder / "memory.txt")) and re.search(r"list.*\d", text_of(folder / "memory.txt")),
           "memory.txt holds both peaks", "memory.txt is missing or incomplete: run memory.py")


RANK = {"urgent": 0, "high": 1, "normal": 2, "low": 3}


def check_2_4(folder: Path, r: Report) -> None:
    typed(r, folder, "tickets.py")
    tickets = [t for t in data.tickets() if t["status"] == "open"]
    tickets.sort(key=lambda t: (RANK[t["priority"]], t["opened"], t["ticket_id"]))
    found, why = probe(folder, "import dataclasses, datetime, tickets as T\n"
                       "rows = [json.loads(line) for line in open('data/tickets.jsonl', encoding='utf-8')]\n"
                       "all_ = [T.from_record(row) for row in rows]\n"
                       "q = T.queue(all_)\n"
                       "frozen = False\n"
                       "try:\n    all_[0].priority = 'low'\n"
                       "except dataclasses.FrozenInstanceError:\n    frozen = True\n"
                       "print(json.dumps({'dc': dataclasses.is_dataclass(T.Ticket), 'frozen': frozen,\n"
                       " 'fields': [f.name for f in dataclasses.fields(T.Ticket)],\n"
                       " 'date': isinstance(all_[0].opened, datetime.date),\n"
                       " 'age': all_[0].age_days(datetime.date(2026, 10, 1)), 'opened': all_[0].opened.isoformat(),\n"
                       " 'queue': [t.ticket_id for t in q]}))")
    if not r.need(isinstance(found, dict), "tickets.py runs", f"tickets.py does not run yet: {why}"):
        return
    assert isinstance(found, dict)
    r.need(found["dc"] and found["frozen"], "Ticket is a frozen data class",
           "Ticket must be a data class with frozen=True: a record that cannot change by accident")
    r.need(not {"phone", "national_id"} & set(found["fields"]), "Ticket keeps no phone number and no identity number",
           "Ticket has a phone or identity field: the queue does not need it, so the record does not carry it")
    from datetime import date
    first = data.tickets()[0]
    age = (date(2026, 10, 1) - date.fromisoformat(first["opened"])).days
    r.need(found["date"] and found["age"] == age, f"opened is a date, and age_days counts {age} days for {first['ticket_id']}",
           f"opened must be a date and age_days must count days: got {found['age']} for {first['ticket_id']}, expected {age}")
    want = [t["ticket_id"] for t in tickets]
    r.need(found["queue"] == want, f"queue holds the {len(want)} open tickets, most urgent and oldest first ({', '.join(want[:3])}, …)",
           f"queue starts with {found['queue'][:3]} and has {len(found['queue'])} tickets; expected {want[:3]} and {len(want)}")


CHECKS = {"1.1": check_1_1, "1.2": check_1_2, "1.3": check_1_3, "1.4": check_1_4,
          "2.1": check_2_1, "2.2": check_2_2, "2.3": check_2_3, "2.4": check_2_4}


def run(lab: str, folder: Path) -> int:
    if lab not in CHECKS:
        print(f"lab {lab} has no check")
        return 2
    report = Report()
    CHECKS[lab](folder, report)
    for ok, line in report.lines:
        print(("  ok   " if ok else "  TODO ") + line)
    if report.failed:
        print(f"lab {lab}: {report.failed} to do")
        return 1
    print(f"PASS lab {lab}")
    return 0
