"""The command line of Miqyas.

    python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md
"""

from __future__ import annotations

import argparse
import csv
import logging
from pathlib import Path

from miqyas.anomalies import find_anomalies
from miqyas.readings import Rejection, load_meters, load_readings
from miqyas.report import render

log = logging.getLogger("miqyas")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="miqyas", description="Check a month of meter readings.")
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report", help="validate the readings and write the report")
    report.add_argument("--readings", type=Path, required=True, help="the readings file (CSV)")
    report.add_argument("--meters", type=Path, required=True, help="the meter registry (CSV)")
    report.add_argument("--out", type=Path, required=True, help="where to write the report (Markdown)")
    report.add_argument("--rejections", type=Path, help="also write every rejected row here (CSV)")
    report.add_argument("--factor", type=float, default=3.0, help="anomaly threshold, times the median")
    report.add_argument("-v", "--verbose", action="store_true", help="log each step")
    return parser


def write_rejections(path: Path, rejections: list[Rejection]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["line_no", "reason", "detail"])
        writer.writerows([r.line_no, r.reason, r.detail] for r in rejections)


def main(argv: list[str] | None = None) -> int:
    """Run the tool; the return value is the exit code (0 done, 2 an input is missing)."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(levelname)s %(message)s")
    for path in (args.readings, args.meters):
        if not path.is_file():
            log.error("no such file: %s", path)
            return 2
    meters = load_meters(args.meters)
    log.info("%d meters in the registry", len(meters))
    readings, rejections = load_readings(args.readings, set(meters))
    log.info("%d rows accepted, %d rejected", len(readings), len(rejections))
    anomalies = find_anomalies(readings, args.factor)
    log.info("%d anomalies at factor %g", len(anomalies), args.factor)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    text = render(args.readings.name, readings, rejections, anomalies, meters, args.factor)
    args.out.write_text(text, encoding="utf-8", newline="\n")
    if args.rejections:
        write_rejections(args.rejections, rejections)
    log.info("report written to %s", args.out)
    return 0
