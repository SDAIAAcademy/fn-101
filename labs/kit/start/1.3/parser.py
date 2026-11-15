"""Parse the export of the hand-held meter reader.

One line per reading, three fields separated by semicolons:

    M-0042;2026-09-03;0.742

A line with another number of fields, or with an empty value, is a bad line.
"""


def split_line(line):
    parts = line.strip().split(";")
    if len(parts) != 3:
        return None
    return parts


def parse_value(text):
    if text == "":
        return None
    return float(text)


def parse_line(line):
    parts = split_line(line)
    meter_id, day, text = parts
    value = parse_value(text)
    return meter_id, day, round(value, 3)


def total(lines):
    result = 0
    for line in lines:
        reading = parse_line(line)
        result = result + reading[2]
    return result


def highest(lines):
    best = ""
    for line in lines:
        reading = parse_line(line)
        if reading[2] > best:
            best = reading[2]
    return best
