"""Monthly bill of one meter, as four functions and a short main.

The tariff is invented for the course: 2.00 SAR per cubic metre up to 15 m3,
4.50 SAR above that, and a service fee of 5.00 SAR.
"""

import csv


def load_rows(path):
    """Read the readings file at path; return one dictionary of strings per data row."""
    with open(path, encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def clean(rows):
    """Take rows; return (the consumption values that are numbers, how many rows were skipped)."""
    values = []
    skipped = 0
    for row in rows:
        text = row["consumption_m3"].strip()
        try:
            values.append(float(text))
        except ValueError:
            skipped += 1
    return values, skipped


def bill(total_m3):
    """Take a month's consumption in cubic metres; return the amount due in SAR."""
    if total_m3 <= 15:
        amount = total_m3 * 2.0
    else:
        amount = 15 * 2.0 + (total_m3 - 15) * 4.5
    return amount + 5.0


def format_bill(meter_id, values, skipped, amount):
    """Take the facts of one bill; return the four lines of the bill as one string."""
    return "\n".join([
        f"Meter {meter_id}",
        f"Days billed: {len(values)} skipped: {skipped}",
        f"Consumption: {round(sum(values), 3)} m3",
        f"Amount due: {round(amount, 2)} SAR",
    ])


def main():
    rows = load_rows("data/sample_meter.csv")
    values, skipped = clean(rows)
    print(format_bill(rows[0]["meter_id"], values, skipped, bill(sum(values))))


if __name__ == "__main__":
    main()
