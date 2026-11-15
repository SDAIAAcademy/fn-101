"""The checks of Day 3: files, encodings, rejections and the two seeded defects."""

from __future__ import annotations

import csv
import io
import json
import re
import shutil
import tempfile
from pathlib import Path

import checks as C
import data
import labtool

PHONE_RUN = re.compile(r"\+?\d{9,}")


def check_3_1(folder: Path, r: C.Report) -> None:
    C.typed(r, folder, "summary.py")
    found, why = C.probe(folder, "import summary as s\n"
                         "print(json.dumps([s.mask_phone('+966555010042'), "
                         "s.mask_text('call \\u0660\\u0665\\u0665\\u0665\\u0660\\u0661\\u0662\\u0663\\u0664\\u0665 or 0555012345 now'), "
                         "s.mask_text('meter M-0042, 3 days')]))")
    if r.need(isinstance(found, list), "summary.py can be imported", f"summary.py does not run yet: {why}"):
        assert isinstance(found, list)
        r.need(found[0] == "+**********42", "mask_phone keeps the last two digits only",
               f"mask_phone('+966555010042') gave {found[0]!r}; expected '+**********42'")
        r.need(found[1] == "call [phone] or [phone] now", "mask_text removes phone numbers, in Arabic-Indic digits too",
               f"mask_text left a number in the text: {found[1]!r}")
        r.need(found[2] == "meter M-0042, 3 days", "mask_text leaves meter ids and small numbers alone",
               f"mask_text changed a text without a phone number: {found[2]!r}")
    status, output = C.py(folder, "summary.py")
    r.need(status == 0, "summary.py runs to the end", f"summary.py stops: {C.last(output)}")
    r.need(not PHONE_RUN.search(output), "nothing printed looks like a phone number",
           "the script prints something that looks like a phone number")
    file = folder / "out" / "summary.json"
    raw = C.text_of(file)
    try:
        summary = json.loads(raw)
    except ValueError:
        summary = None
    if not r.need(isinstance(summary, dict), "out/summary.json is valid JSON", "out/summary.json is missing or is not valid JSON"):
        return
    where = {m["meter_id"]: m["district"] for m in data.meters()}
    tickets = data.tickets()
    clean = data.readings_clean()
    wrong = []
    for district in data.DISTRICTS:
        values = [float(x["consumption_m3"]) for x in clean if where[x["meter_id"]] == district]
        entry = summary.get(district, {})
        opened = [t for t in tickets if t["district"] == district and t["status"] == "open"]
        urgent = sorted((t for t in opened if t["priority"] == "urgent"), key=lambda t: (t["opened"], t["ticket_id"]))
        if entry.get("readings") != len(values) or abs(entry.get("total_m3", 0) - sum(values)) > 0.01:
            wrong.append(f"{district}: readings or total")
        if entry.get("open_tickets") != len(opened):
            wrong.append(f"{district}: open_tickets")
        if [c.get("ticket_id") for c in entry.get("callbacks", [])] != [t["ticket_id"] for t in urgent]:
            wrong.append(f"{district}: callbacks")
    r.need(not wrong, "the six districts have the expected counts, totals and callbacks",
           "the summary differs from the expected one: " + "; ".join(wrong[:3]))
    r.need(not PHONE_RUN.search(raw), "no phone number is in out/summary.json",
           f"out/summary.json still holds something that looks like a phone number: {PHONE_RUN.search(raw).group(0)[:4] + '...' if PHONE_RUN.search(raw) else ''}")
    r.need("national_id" not in raw, "no identity number is in out/summary.json", "out/summary.json holds the field national_id")
    r.need(re.search("[؀-ۿ]", raw) and "\\u06" not in raw, "Arabic text is written as Arabic, not as escapes",
           "the Arabic text is written as \\u escapes: pass ensure_ascii=False to json.dump")


def branch_failures() -> list[list[object]]:
    content, _ = data.tickets_branch()
    failures: list[list[object]] = []
    for n, raw in enumerate(content.splitlines(), start=1):
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as problem:
            failures.append([n, problem.start, hex(raw[problem.start])])
    return failures


def check_3_2(folder: Path, r: C.Report) -> None:
    C.typed(r, folder, "decode.py")
    expected = branch_failures()
    found, why = C.probe(folder, "import decode as d\n"
                         "lines, failed = d.decode_lines(d.PATH, 'utf-8')\n"
                         "print(json.dumps([len(lines), [[f.line_no, f.position, str(f.byte).lower()] for f in failed]]))")
    if r.need(isinstance(found, list), "decode_lines runs", f"decode_lines does not run yet: {why}"):
        assert isinstance(found, list)
        r.need(found[0] == 120 - len(expected), f"{120 - len(expected)} lines decode as UTF-8",
               f"decode_lines returns {found[0]} decoded lines; expected {120 - len(expected)}")
        r.need([f[0] for f in found[1]] == [f[0] for f in expected],
               f"the {len(expected)} lines that still fail are found: {', '.join(str(f[0]) for f in expected)}",
               f"the failing lines are {[f[0] for f in found[1]]}; expected {[f[0] for f in expected]} (lines count from 1)")
        r.need(found[1] == expected, "each failure names the position and the byte where decoding stopped",
               f"position or byte differ: got {found[1][:1]}, expected {expected[:1]} (use the start of the UnicodeDecodeError)")
    status, output = C.py(folder, "decode.py")
    r.need(status == 0, "decode.py runs to the end", f"decode.py stops: {C.last(output)}")
    try:
        report = json.loads(C.text_of(folder / "out" / "decode_report.json"))
    except ValueError:
        report = {}
    r.need(report.get("encoding") == "utf-8" and report.get("lines") == 120 and report.get("decoded") == 120 - len(expected)
           and [f.get("line_no") for f in report.get("failed", [])] == [f[0] for f in expected],
           "out/decode_report.json accounts for all 120 lines",
           "out/decode_report.json is missing, or its encoding, lines, decoded or failed entries are not the expected ones")
    source = C.text_of(folder / "decode.py")
    r.need(not re.search(r"errors\s*=\s*[\"'](ignore|replace)", source), "no line is decoded with errors ignored or replaced",
           "decode.py uses errors='ignore' or 'replace': that hides the failing lines instead of listing them")


def check_3_3(folder: Path, r: C.Report) -> None:
    C.typed(r, folder, "intake.py")
    lines, reasons = data.tickets_raw()
    found, why = C.probe(folder, "import intake as i\n"
                         "accepted, rejected = i.intake(i.PATH)\n"
                         "print(json.dumps([len(accepted), [[n, reason, bool(str(detail).strip())] for n, reason, detail in rejected]]))")
    if r.need(isinstance(found, list), "intake runs without crashing on any line", f"intake does not get through the file: {why}"):
        assert isinstance(found, list)
        got = {n: reason for n, reason, _ in found[1]}
        r.need(found[0] + len(found[1]) == len(lines), f"every one of the {len(lines)} lines is accounted for",
               f"{found[0]} accepted + {len(found[1])} rejected is not {len(lines)} lines")
        r.need(found[0] == len(lines) - len(reasons), f"{len(lines) - len(reasons)} lines are accepted",
               f"{found[0]} lines are accepted; expected {len(lines) - len(reasons)}")
        differ = sorted(n for n in set(got) | set(reasons) if got.get(n) != reasons.get(n))
        r.need(not differ, f"the {len(reasons)} rejected lines each carry the expected reason code",
               "reason differs at line " + ", ".join(f"{n} (got {got.get(n)}, expected {reasons.get(n)})" for n in differ[:3]))
        r.need(all(has for _, _, has in found[1]), "every rejection has a detail", "a rejection has an empty detail")
    status, output = C.py(folder, "intake.py")
    r.need(status == 0, "intake.py runs to the end", f"intake.py stops: {C.last(output)}")
    rows = list(csv.reader(io.StringIO(C.text_of(folder / "out" / "rejections.csv"))))
    r.need(rows[:1] == [["line_no", "reason", "detail"]] and {int(x[0]): x[1] for x in rows[1:] if x and x[0].isdigit()} == reasons,
           f"out/rejections.csv lists the {len(reasons)} lines with their reasons",
           "out/rejections.csv is missing, has another header, or does not list the expected lines")
    source = C.text_of(folder / "intake.py")
    r.need(not re.search(r"except\s*:|except\s+(Exception|BaseException)\b", source),
           "no bare except, and no except Exception",
           "intake.py catches everything (a bare except or except Exception): name the exception you expect")


LOG_STEPS = ["Reproduce", "Shrink", "Hypothesis", "Test", "Fix", "Regression"]


def log_complete(r: C.Report, folder: Path, defects: list[str]) -> None:
    text = re.sub(r"<!--.*?-->", "", C.text_of(folder / "debug_log.md"), flags=re.S)
    parts = re.split(r"^## +", text, flags=re.M)
    for name in defects:
        part = next((p for p in parts if p.lower().startswith(name.lower())), "")
        empty = [step for step in LOG_STEPS if not C.section_filled(part, step)]
        r.need(not empty, f"debug_log.md: all six steps are written for {name}",
               f"debug_log.md, {name}: nothing (or too little) under {', '.join(empty)}")


def fails_on(folder: Path, test_file: str, defects: list[str]) -> bool:
    """Do the participant's tests pass on the sound package and fail when it carries these defects?"""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(folder / test_file, Path(tmp) / test_file)
        if (folder / "data").is_dir():
            shutil.copytree(folder / "data", Path(tmp) / "data")
        labtool.package(Path(tmp))
        sound, _ = C.py(Path(tmp), "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file)
        labtool.package(Path(tmp), defects)
        seeded, _ = C.py(Path(tmp), "-m", "pytest", "-q", "-p", "no:cacheprovider", test_file)
    return sound == 0 and seeded == 1


MONTH = ("from pathlib import Path\n"
         "from miqyas.readings import load_meters, load_readings\n"
         "from miqyas.anomalies import find_anomalies\n"
         "from miqyas.report import anomalies_by_district\n"
         "meters = load_meters(Path('data/meters.csv'))\n"
         "a1, r1 = load_readings(Path('data/readings_2026_09.csv'), set(meters))\n"
         "a2, r2 = load_readings(Path('data/readings_2026_09.csv'), set(meters))\n"
         "found = find_anomalies(a1)\n"
         "per = {d: len(v) for d, v in anomalies_by_district(found, meters).items()}\n"
         "print(json.dumps([len(a1), len(a2), len(found), per]))")


def month_numbers(r: C.Report, folder: Path) -> list[object] | None:
    found, why = C.probe(folder, MONTH)
    if not r.need(isinstance(found, list), "the package loads the month", f"the package does not run: {why}"):
        return None
    assert isinstance(found, list)
    return found


def check_3_4(folder: Path, r: C.Report) -> None:
    log_complete(r, folder, ["Defect A", "Defect B"])
    if not r.need((folder / "test_regression.py").is_file(), "test_regression.py is there"):
        return
    C.tests(r, folder, "test_regression.py", "the regression tests, on your fixed package")
    r.need(fails_on(folder, "test_regression.py", ["D1", "D1b"]), "a regression test fails when defect A is put back",
           "no test fails when defect A is put back: the test does not guard against it")
    r.need(fails_on(folder, "test_regression.py", ["D2"]), "a regression test fails when defect B is put back",
           "no test fails when defect B is put back: the test does not guard against it")
    numbers = month_numbers(r, folder)
    if numbers:
        r.need(numbers[0] == numbers[1] == 17561, "two runs over the month both accept 17561 rows",
               f"two runs accept {numbers[0]} and {numbers[1]} rows; both should be 17561")
        r.need(numbers[2] == 18, "the month has 18 anomalies", f"the month has {numbers[2]} anomalies; expected 18")
    C.typed(r, folder, "miqyas")


C.CHECKS.update({"3.1": check_3_1, "3.2": check_3_2, "3.3": check_3_3, "3.4": check_3_4})
