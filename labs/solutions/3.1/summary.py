"""Write one summary per district from the readings, the registry and the tickets.

    uv run python summary.py        # writes out/summary.json

The tickets are personal data: each holds a phone number and an identity number, and people
type phone numbers into the free text too. Nothing of that may reach the output file or the
screen. The summary lists, per district, the open urgent tickets to call back, with the phone
masked and the text cleaned.
"""

import csv
import json
import re
from pathlib import Path

Row = dict[str, str]

# A phone number in free text: an optional plus sign, then nine or more digits in a row.
PHONE = re.compile(r"\+?\d{9,}")


def load_csv(path: str) -> list[Row]:
    """Read a CSV file; return one dictionary of strings per data row."""
    with open(path, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def load_jsonl(path: str) -> list[Row]:
    """Read a JSON Lines file; return one dictionary per line."""
    with open(path, encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def mask_phone(phone: str) -> str:
    """Replace every digit except the last two with a star: '+966555010042' -> '+**********42'."""
    digits = sum(1 for character in phone if character.isdigit())
    masked = []
    seen = 0
    for character in phone:
        if character.isdigit():
            seen += 1
            masked.append(character if seen > digits - 2 else "*")
        else:
            masked.append(character)
    return "".join(masked)


def mask_text(text: str) -> str:
    """Replace every phone number in free text with '[phone]'."""
    return PHONE.sub("[phone]", text)


def summarise(readings: list[Row], meters: list[Row], tickets: list[Row]) -> dict[str, dict[str, object]]:
    """One entry per district, in alphabetical order. Supplied: it uses your two mask functions."""
    district_of = {meter["meter_id"]: meter["district"] for meter in meters}
    summary: dict[str, dict[str, object]] = {}
    for district in sorted(set(district_of.values())):
        values = [float(r["consumption_m3"]) for r in readings if district_of[r["meter_id"]] == district]
        open_tickets = [t for t in tickets if t["district"] == district and t["status"] == "open"]
        urgent = sorted((t for t in open_tickets if t["priority"] == "urgent"),
                        key=lambda t: (t["opened"], t["ticket_id"]))
        summary[district] = {
            "readings": len(values),
            "total_m3": round(sum(values), 3),
            "open_tickets": len(open_tickets),
            "callbacks": [
                {"ticket_id": t["ticket_id"], "opened": t["opened"],
                 "phone": mask_phone(t["phone"]), "text": mask_text(t["text"])}
                for t in urgent
            ],
        }
    return summary


def write_json(path: str, summary: dict[str, dict[str, object]]) -> None:
    """Write the summary as indented JSON in UTF-8, with Arabic kept readable."""
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)
        file.write("\n")


def main() -> None:
    readings = load_csv("data/readings_clean.csv")
    meters = load_csv("data/meters.csv")
    tickets = load_jsonl("data/tickets.jsonl")
    summary = summarise(readings, meters, tickets)
    Path("out").mkdir(exist_ok=True)
    write_json("out/summary.json", summary)
    for district, entry in summary.items():
        print(f"{district:15} {entry['readings']:>5} readings {entry['open_tickets']:>3} open tickets")


if __name__ == "__main__":
    main()
