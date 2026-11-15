"""Parse the export of the hand-held meter reader.

One line per reading, three fields separated by semicolons:

    M-0042;2026-09-03;0.742

A line with another number of fields, or with an empty value, is a bad line.
"""


def split_line(line: str) -> list[str] | None:
    parts = line.strip().split(";")
    if len(parts) != 3:
        return None
    return parts


def parse_value(text: str) -> float | None:
    if text == "":
        return None
    return float(text)


def parse_line(line: str) -> tuple[str, str, float] | None:
    parts = split_line(line)
    if parts is None:
        return None
    meter_id, day, text = parts
    value = parse_value(text)
    if value is None:
        return None
    return meter_id, day, round(value, 3)


def total(lines: list[str]) -> float:
    result = 0.0
    for line in lines:
        reading = parse_line(line)
        if reading is not None:
            result = result + reading[2]
    return round(result, 3)


def highest(lines: list[str]) -> float | None:
    best: float | None = None
    for line in lines:
        reading = parse_line(line)
        if reading is not None and (best is None or reading[2] > best):
            best = reading[2]
    return best
