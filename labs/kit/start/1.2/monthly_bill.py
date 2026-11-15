# Monthly bill of one meter. It works, and it is one block of forty lines:
# nothing in it can be tested, reused or imported without running all of it.
# The tariff is invented for the course: 2.00 SAR per cubic metre up to 15 m3,
# 4.50 SAR above that, and a service fee of 5.00 SAR.
import csv

rows = []
f = open("data/sample_meter.csv", encoding="utf-8", newline="")
for row in csv.DictReader(f):
    rows.append(row)
f.close()

values = []
skipped = 0
for row in rows:
    text = row["consumption_m3"].strip()
    if text == "":
        skipped = skipped + 1
        continue
    try:
        values.append(float(text))
    except ValueError:
        skipped = skipped + 1

total = 0.0
for v in values:
    total = total + v

if total <= 15:
    amount = total * 2.0
else:
    amount = 15 * 2.0 + (total - 15) * 4.5
amount = amount + 5.0

meter_id = rows[0]["meter_id"]
print("Meter", meter_id)
print("Days billed:", len(values), "skipped:", skipped)
print("Consumption:", round(total, 3), "m3")
print("Amount due:", round(amount, 2), "SAR")
