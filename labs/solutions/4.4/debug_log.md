# Debugging log

The reference log. The numbers are from the reference run.

## Defect C

### Reproduce
`uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md`: in the Districts table of out/report.md all six districts show 18 anomalies, and the section below it lists 18 anomalies in total. The sound numbers are 4, 3, 3, 1, 5 and 2.

### Shrink
Two meters in two districts and one anomaly, built by hand, passed to `anomalies_by_district`: both districts come back with that one anomaly. No file is needed.

### Hypothesis
I think both districts hold the same list, because `anomalies_by_district` in `miqyas/report.py` builds its dictionary with `dict.fromkeys(districts, [])`, and the `[]` there is created once and given to every key.

### Test
`groups["Al-Rabwa"] is groups["Al-Yasmin"]` printed True: one list, two keys. The first recorded hint of the tutor pointed me to "things that should be separate showing the same content", the second to the `is` operator.

### Fix
`dict.fromkeys(districts, [])` became `{district: [] for district in districts}`: the comprehension runs `[]` once per district.

### Regression
`test_defect_c_an_anomaly_is_listed_in_its_own_district_only`: fails before the fix (both districts hold the anomaly), passes after.
