"""The command line of Miqyas.

    python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md

The cells of the notebook have become functions in readings.py, anomalies.py and report.py.
What is left of the notebook is the order in which it ran them. That order is main().
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from miqyas.anomalies import find_anomalies  # noqa: F401
from miqyas.readings import load_meters, load_readings  # noqa: F401
from miqyas.report import render  # noqa: F401

log = logging.getLogger("miqyas")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="miqyas", description="Check a month of meter readings.")
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report", help="validate the readings and write the report")
    report.add_argument("--readings", type=Path, required=True, help="the readings file (CSV)")
    # Step 1: three more arguments.
    #   --meters   a Path, required: the meter registry (CSV)
    #   --out      a Path, required: where to write the report (Markdown)
    #   --factor   a float, default 3.0: the anomaly threshold, times the median
    report.add_argument("-v", "--verbose", action="store_true", help="log each step")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the tool; the return value is the exit code (0 done, 2 an input is missing)."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(levelname)s %(message)s")
    # Step 2: the notebook's order, as calls. Log, do not print.
    #   - if the readings file or the meters file does not exist: log.error(...) and return 2
    #   - meters = load_meters(...)                        (the notebook's first cell)
    #   - readings, rejections = load_readings(..., set(meters))      (its cleaning cell)
    #   - anomalies = find_anomalies(readings, args.factor)           (its anomaly cell)
    #   - text = render(args.readings.name, readings, rejections, anomalies, meters, args.factor)
    #   - make the folder of args.out if needed, and write text there as UTF-8 with newline="\n"
    #   - log.info what was done at each step; return 0
    raise NotImplementedError("step 2")
