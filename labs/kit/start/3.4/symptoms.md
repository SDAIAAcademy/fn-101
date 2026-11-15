# Two reports from the metering team

Both are about Miqyas, the package in the folder `miqyas/`. Each report describes what
somebody saw, not what is wrong. Finding what is wrong is the lab.

## Report A, from the night operator

"The nightly job reads the month's file twice, before and after the late sync. The first run
is fine. The second run of the same file accepts nothing at all."

    uv run python two_runs.py

## Report B, from Salma

"The September report lists meter M-0012 as an anomaly on the 26th, with a median of 0.653.
I sorted its thirty readings in a spreadsheet: the two in the middle are 0.693 and 0.699, so
the median is 0.696. The flag is right this time, but the number beside it is wrong, and a
wrong median will flag the wrong days in another month."

    uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md

Then look for M-0012 in `out/report.md`.
