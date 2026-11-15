"""The synthetic data of Manahil Water Services, a fictional regional water utility.

Standard library only. Every number comes from one small generator with a fixed seed, written
here so that the files are the same bytes on every machine and every Python version. No real
person, meter, phone number or identity number: the phone and identity values are made up and
follow no real allocation.
"""

from __future__ import annotations

import json
from pathlib import Path

DISTRICTS = ["Al-Rabwa", "Al-Yasmin", "Al-Faisaliyah", "Al-Naseem", "Al-Murooj", "Al-Khuzama"]
DAYS = [f"2026-09-{d:02d}" for d in range(1, 31)]
PRIORITIES = ["urgent", "high", "normal", "low"]
MAX_DAILY_M3 = 200.0
SILENT = 12          # meters in the registry that sent no reading
UNKNOWN_IDS = ["M-9001", "M-9002", "M-9003", "M-9004", "M-9005"]


class Rng:
    """A linear congruential generator: the same sequence everywhere."""

    def __init__(self, seed: int) -> None:
        self.state = seed & 0xFFFFFFFFFFFFFFFF

    def next(self) -> int:
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return self.state >> 33

    def below(self, n: int) -> int:
        return self.next() % n

    def between(self, low: float, high: float) -> float:
        return low + (high - low) * (self.next() / 2**31)

    def pick(self, items: list):
        return items[self.below(len(items))]

    def sample(self, items: list, k: int) -> list:
        pool = list(items)
        chosen = []
        for _ in range(k):
            chosen.append(pool.pop(self.below(len(pool))))
        return chosen


def meters() -> list[dict[str, str]]:
    rng = Rng(101)
    rows = []
    for i in range(1, 601):
        kind = "commercial" if rng.below(100) < 15 else "residential"
        rows.append({
            "meter_id": f"M-{i:04d}",
            "district": DISTRICTS[rng.below(len(DISTRICTS))],
            "kind": kind,
            "installed": f"{2012 + rng.below(13)}-{1 + rng.below(12):02d}-{1 + rng.below(28):02d}",
        })
    return rows


def _plan() -> dict:
    """Which meters are silent, and which rows carry which planted problem."""
    rng = Rng(202)
    all_meters = meters()
    silent = sorted(m["meter_id"] for m in rng.sample(all_meters, SILENT))
    active = [m for m in all_meters if m["meter_id"] not in silent]
    base = {}
    for m in active:
        low, high = (2.0, 8.0) if m["kind"] == "commercial" else (0.3, 1.2)
        base[m["meter_id"]] = rng.between(low, high)
    # one planted problem per chosen (meter, day); all choices are distinct cells
    cells = [(m["meter_id"], d) for m in active for d in DAYS]
    chosen = rng.sample(cells, 40 + 15 + 18 + 6 + 27 + 30)
    plan = {
        "active": active, "silent": silent, "base": base,
        "missing": chosen[:40],
        "not_a_number": chosen[40:55],
        "out_of_range": chosen[55:73],
        "bad_date": chosen[73:79],
        "spikes": chosen[79:106],        # 18 strong, 9 mild
        "duplicates": chosen[106:136],
    }
    return plan


def readings_month() -> list[dict[str, str]]:
    """September 2026, one row per active meter and day, with the planted problems."""
    plan = _plan()
    rng = Rng(303)
    kind = {}
    for name in ("missing", "not_a_number", "out_of_range", "bad_date", "spikes", "duplicates"):
        for n, cell in enumerate(plan[name]):
            kind[cell] = (name, n)
    keyed = []
    index = 0
    for day in DAYS:
        for m in plan["active"]:
            meter_id = m["meter_id"]
            value = plan["base"][meter_id] * rng.between(0.8, 1.2)
            text = f"{value:.3f}"
            date_text = day
            what = kind.get((meter_id, day))
            if what:
                name, n = what
                if name == "missing":
                    text = ""
                elif name == "not_a_number":
                    text = "N/A" if n < 8 else text.replace(".", ",")
                elif name == "out_of_range":
                    text = f"-{value:.3f}" if n < 10 else f"{9000 + rng.below(999)}.000"
                elif name == "bad_date":
                    date_text = "2026-09-31" if n < 3 else f"{day[8:]}/09/2026"
                elif name == "spikes":
                    factor = rng.between(4.0, 8.0) if n < 18 else rng.between(2.2, 2.8)
                    text = f"{plan['base'][meter_id] * factor:.3f}"
            row = {"meter_id": meter_id, "date": date_text, "consumption_m3": text}
            keyed.append((index, 0, row))
            if what and what[0] == "duplicates":
                keyed.append((index + 1 + rng.below(900), 1, dict(row)))
            index += 1
    for n, meter_id in enumerate(UNKNOWN_IDS):
        for k in range(4):
            row = {"meter_id": meter_id, "date": DAYS[rng.below(30)],
                   "consumption_m3": f"{rng.between(0.3, 1.2):.3f}"}
            keyed.append((rng.below(index), 2 + n * 4 + k, row))
    keyed.sort(key=lambda item: (item[0], item[1]))
    return [row for _, _, row in keyed]


def is_valid_cell(row: dict[str, str], known: set[str]) -> str:
    """The reason a row is rejected, or "" (duplicates are decided by the caller)."""
    text = row["consumption_m3"].strip()
    if text == "":
        return "MISSING_VALUE"
    try:
        value = float(text)
    except ValueError:
        return "NOT_A_NUMBER"
    if not 0.0 <= value <= MAX_DAILY_M3:
        return "OUT_OF_RANGE"
    parts = row["date"].split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts) or not (1 <= int(parts[1]) <= 12) \
            or not (1 <= int(parts[2]) <= (30 if int(parts[1]) in (4, 6, 9, 11) else 31)):
        return "BAD_DATE"
    if row["meter_id"] not in known:
        return "UNKNOWN_METER"
    return ""


def readings_clean() -> list[dict[str, str]]:
    known = {m["meter_id"] for m in meters()}
    seen = set()
    rows = []
    for row in readings_month():
        key = (row["meter_id"], row["date"])
        if is_valid_cell(row, known) or key in seen:
            continue
        seen.add(key)
        rows.append(row)
    return rows


def readings_large(n: int = 100_000) -> list[dict[str, str]]:
    """Clean rows for the timing and memory labs: n rows over the year 2026."""
    plan = _plan()
    rng = Rng(404)
    ids = [m["meter_id"] for m in plan["active"]]
    rows = []
    for _ in range(n):
        meter_id = ids[rng.below(len(ids))]
        value = plan["base"][meter_id] * rng.between(0.8, 1.2)
        rows.append({"meter_id": meter_id,
                     "date": f"2026-{1 + rng.below(9):02d}-{1 + rng.below(28):02d}",
                     "consumption_m3": f"{value:.3f}"})
    return rows


AR_DIGITS = "٠١٢٣٤٥٦٧٨٩"

TEXTS = [
    ("ar", "تسرب مياه أمام المنزل منذ يومين، رقم العداد {meter}"),
    ("ar", "انقطاع المياه عن الحي منذ الصباح، نرجو الإفادة"),
    ("ar", "الفاتورة مرتفعة جدا هذا الشهر، أرجو مراجعة قراءة العداد {meter}"),
    ("ar", "ضغط المياه ضعيف في الدور الثاني منذ أسبوع"),
    ("ar", "العداد {meter} متوقف ولا يسجل القراءة"),
    ("ar", "لون المياه متغير وفيها رائحة، نرجو فحص الخزان"),
    ("en", "Water leaking in front of the house for two days, meter {meter}"),
    ("en", "No water in the district since this morning, please advise"),
    ("en", "The bill is much higher this month, please check the reading of meter {meter}"),
    ("en", "Low water pressure on the second floor for a week"),
    ("en", "Meter {meter} has stopped and records nothing"),
    ("mixed", "الفاتورة مرتفعة جدا this month, please check meter {meter}"),
    ("mixed", "Leak near the main valve, العداد {meter}، الرجاء الإسراع"),
    ("mixed", "طلب نقل العداد {meter} to the new address, شكرا"),
]


def tickets() -> list[dict[str, str]]:
    plan = _plan()
    rng = Rng(505)
    by_district: dict[str, list[str]] = {d: [] for d in DISTRICTS}
    for m in plan["active"]:
        by_district[m["district"]].append(m["meter_id"])
    rows = []
    for i in range(400):
        district = DISTRICTS[rng.below(len(DISTRICTS))]
        meter_id = rng.pick(by_district[district])
        roll = rng.below(100)
        priority = "urgent" if roll < 8 else "high" if roll < 30 else "normal" if roll < 80 else "low"
        day = rng.below(42)             # 20 August to 30 September 2026
        opened = f"2026-08-{20 + day:02d}" if day < 12 else f"2026-09-{day - 11:02d}"
        _, template = TEXTS[rng.below(len(TEXTS))]
        text = template.format(meter=meter_id)
        phone = f"+96655501{rng.below(10000):04d}"
        if i % 29 == 7:                 # a callback number typed into the free text
            callback = f"055501{rng.below(10000):04d}"
            if i % 3 == 0:
                callback = "".join(AR_DIGITS[int(c)] for c in callback)
                text += f"، للتواصل {callback}"
            else:
                text += f" (call me on {callback})"
        rows.append({
            "ticket_id": f"T-{20001 + i}",
            "opened": opened,
            "district": district,
            "meter_id": meter_id,
            "priority": priority,
            "channel": rng.pick(["app", "phone", "branch"]),
            "status": "open" if rng.below(100) < 60 else "closed",
            "phone": phone,
            "national_id": f"10000{rng.below(100000):05d}",
            "text": text,
        })
    return rows


def tickets_branch() -> tuple[bytes, list[int]]:
    """120 ticket lines in UTF-8, seven of them written by an old terminal in Windows-1256.

    Returns the bytes of the file and the line numbers (from 1) of the legacy lines.
    """
    rng = Rng(606)
    source = [t for t in tickets() if any(ord(c) > 0x600 for c in t["text"])][:120]
    legacy = sorted(rng.sample(list(range(3, 121)), 7))
    out = []
    for n, ticket in enumerate(source, start=1):
        record = {k: ticket[k] for k in ("ticket_id", "opened", "district", "priority", "text")}
        if n in legacy:                 # the old terminal knows no Arabic-Indic digits
            record["text"] = "".join(str(AR_DIGITS.index(c)) if c in AR_DIGITS else c for c in record["text"])
        line = json.dumps(record, ensure_ascii=False)
        data = line.encode("cp1256" if n in legacy else "utf-8")
        if n in legacy:
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                pass
            else:
                raise AssertionError("a legacy line must not be valid UTF-8")
        out.append(data)
    return b"\n".join(out) + b"\n", legacy


def tickets_raw() -> tuple[list[str], dict[int, str]]:
    """The raw ticket file of lab 3.3: 400 good lines and 35 planted bad ones.

    Returns the lines and {line number: reason code} for the bad ones.
    """
    rng = Rng(707)
    good = tickets()
    lines = [json.dumps(t, ensure_ascii=False) for t in good]

    def variant(reason: str, n: int) -> str:
        t = dict(good[rng.below(len(good))])
        t["ticket_id"] = f"T-3{reason[:1]}{n:03d}"
        if reason == "EMPTY_LINE":
            return "   " if n else ""
        if reason == "BAD_JSON":
            text = json.dumps(t, ensure_ascii=False)
            return text[: len(text) // 2] if n % 2 else text.replace('": "', '": ', 1)
        if reason == "NOT_OBJECT":
            return json.dumps([t["ticket_id"], t["text"]], ensure_ascii=False) if n else "42"
        if reason == "MISSING_FIELD":
            del t[["opened", "priority", "text", "meter_id"][n % 4]]
        elif reason == "BAD_PRIORITY":
            t["priority"] = ["عاجل", "URGENT!!", "1", "", "medium"][n % 5]
        elif reason == "BAD_DATE":
            t["opened"] = ["2026-09-31", "12/09/2026", "yesterday", "2026-13-01"][n % 4]
        elif reason == "BAD_METER_ID":
            t["meter_id"] = ["0412", "M-41", "m-0412", "M-O412"][n % 4]
        elif reason == "EMPTY_TEXT":
            t["text"] = ["", "   ", "\t"][n % 3]
        return json.dumps(t, ensure_ascii=False)

    planted = [("EMPTY_LINE", 3), ("BAD_JSON", 6), ("NOT_OBJECT", 2), ("MISSING_FIELD", 8),
               ("BAD_PRIORITY", 5), ("BAD_DATE", 4), ("BAD_METER_ID", 4), ("EMPTY_TEXT", 3)]
    extra = [(reason, variant(reason, n)) for reason, count in planted for n in range(count)]
    positions = sorted(rng.sample(list(range(5, 400)), len(extra)))
    reasons: dict[int, str] = {}
    merged: list[str] = []
    todo = list(zip(positions, extra))
    for i, line in enumerate(lines):
        while todo and todo[0][0] == i:
            _, (reason, bad) = todo.pop(0)
            merged.append(bad)
            reasons[len(merged)] = reason
        merged.append(line)
    return merged, reasons


def sample_meter() -> list[dict[str, str]]:
    """Thirty days of one residential meter, with two blanks and one "N/A" (lab 1.2)."""
    rng = Rng(808)
    rows = []
    for n, day in enumerate(DAYS):
        value = f"{0.62 * rng.between(0.8, 1.2):.3f}"
        if n in (6, 19):
            value = ""
        if n == 12:
            value = "N/A"
        rows.append({"meter_id": "M-0042", "date": day, "consumption_m3": value})
    return rows


# ------------------------------------------------------------------------------------ writing

def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = list(rows[0])
    def cell(value: str) -> str:        # a comma inside a value needs quotes, as a spreadsheet writes it
        return f'"{value}"' if "," in value else value

    text = ",".join(header) + "\n" + "".join(",".join(cell(row[h]) for h in header) + "\n" for row in rows)
    path.write_bytes(text.encode("utf-8"))


def write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_bytes(text.encode("utf-8"))


def write(name: str, folder: Path) -> None:
    """Write one named file of the case study into folder/data/."""
    data = folder / "data"
    if name == "meters":
        write_csv(data / "meters.csv", meters())
    elif name == "readings":
        write_csv(data / "readings_2026_09.csv", readings_month())
    elif name == "readings_clean":
        write_csv(data / "readings_clean.csv", readings_clean())
    elif name == "readings_large":
        write_csv(data / "readings_large.csv", readings_large())
    elif name == "tickets":
        write_jsonl(data / "tickets.jsonl", tickets())
    elif name == "tickets_branch":
        content, _ = tickets_branch()
        data.mkdir(parents=True, exist_ok=True)
        (data / "tickets_branch.jsonl").write_bytes(content)
        meta = {"file": "tickets_branch.jsonl", "encoding": "utf-8", "lines": 120,
                "exported_by": "customer care system, branch export"}
        (data / "tickets_branch.meta.json").write_bytes((json.dumps(meta, indent=2) + "\n").encode("utf-8"))
    elif name == "tickets_raw":
        lines, _ = tickets_raw()
        data.mkdir(parents=True, exist_ok=True)
        (data / "tickets_raw.jsonl").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    elif name == "sample_meter":
        write_csv(data / "sample_meter.csv", sample_meter())
    else:
        raise ValueError(name)


if __name__ == "__main__":
    month = readings_month()
    print("meters", len(meters()), "month rows", len(month), "clean", len(readings_clean()),
          "tickets", len(tickets()), "raw ticket lines", len(tickets_raw()[0]),
          "legacy lines", tickets_branch()[1])
