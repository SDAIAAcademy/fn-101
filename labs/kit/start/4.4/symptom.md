# A report from Mazen, the maintenance planner

"I use the Districts table of the report to send crews. This month every district shows the
same number of anomalies, and that number is the total at the bottom. Six districts cannot
all have every anomaly."

    uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md

Then read the Districts table in `out/report.md`.

This defect is new: it is not one of yesterday's two. Use the six steps and the log, as
yesterday. This time, when you are stuck, you may ask the course tutor for a hint:

    uv run ../tutor.py --recorded                          # the next recorded hint
    uv run ../tutor.py "your question, in your own words"   # a hosted model, when a key is set
