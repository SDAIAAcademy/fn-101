"""The nightly job checks the month's file twice: once before and once after the late sync.

    uv run python two_runs.py

Each run is independent and reads the same file, so both must report the same numbers.
"""

from pathlib import Path

from miqyas.readings import load_meters, load_readings

meters = load_meters(Path("data/meters.csv"))
for run in (1, 2):
    accepted, rejected = load_readings(Path("data/readings_2026_09.csv"), set(meters))
    print(f"run {run}: {len(accepted)} accepted, {len(rejected)} rejected")
