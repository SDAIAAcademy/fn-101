"""Aggregate the month and render the report as Markdown."""

from __future__ import annotations

from dataclasses import dataclass

from miqyas.anomalies import Anomaly
from miqyas.readings import Meter, Reading, Rejection


@dataclass(frozen=True)
class DistrictTotal:
    district: str
    meters: int
    readings: int
    total_m3: float
    anomalies: int


def anomalies_by_district(anomalies: list[Anomaly], meters: dict[str, Meter]) -> dict[str, list[Anomaly]]:
    """The anomalies of each district; a district without any has an empty list."""
    districts = sorted({meter.district for meter in meters.values()})
    groups: dict[str, list[Anomaly]] = {district: [] for district in districts}
    for anomaly in anomalies:
        groups[meters[anomaly.meter_id].district].append(anomaly)
    return groups


def district_totals(
    readings: list[Reading], anomalies: list[Anomaly], meters: dict[str, Meter]
) -> list[DistrictTotal]:
    """One line per district, in alphabetical order."""
    ids: dict[str, set[str]] = {}
    count: dict[str, int] = {}
    total: dict[str, float] = {}
    for reading in readings:
        district = meters[reading.meter_id].district
        ids.setdefault(district, set()).add(reading.meter_id)
        count[district] = count.get(district, 0) + 1
        total[district] = total.get(district, 0.0) + reading.m3
    flagged = anomalies_by_district(anomalies, meters)
    return [
        DistrictTotal(d, len(ids.get(d, set())), count.get(d, 0), round(total.get(d, 0.0), 3), len(flagged[d]))
        for d in flagged
    ]


def rejections_by_reason(rejections: list[Rejection]) -> dict[str, int]:
    """How many rows were rejected for each reason, in alphabetical order."""
    counts: dict[str, int] = {}
    for rejection in rejections:
        counts[rejection.reason] = counts.get(rejection.reason, 0) + 1
    return dict(sorted(counts.items()))


def render(
    source: str,
    readings: list[Reading],
    rejections: list[Rejection],
    anomalies: list[Anomaly],
    meters: dict[str, Meter],
    factor: float,
) -> str:
    """The whole report as text. It holds no clock time, so two runs give the same bytes."""
    lines = [
        f"# Miqyas report: {source}",
        "",
        f"Rows read: {len(readings) + len(rejections)}. Accepted: {len(readings)}. Rejected: {len(rejections)}.",
        "",
        "## Rejected rows by reason",
        "",
        "| Reason | Rows |",
        "|---|---:|",
    ]
    lines += [f"| {reason} | {rows} |" for reason, rows in rejections_by_reason(rejections).items()]
    lines += ["", "## Districts", "",
              "| District | Meters | Readings | Total m3 | Anomalies |", "|---|---:|---:|---:|---:|"]
    lines += [
        f"| {t.district} | {t.meters} | {t.readings} | {t.total_m3:.3f} | {t.anomalies} |"
        for t in district_totals(readings, anomalies, meters)
    ]
    lines += ["", f"## Anomalies (more than {factor:g} times the meter's median): {len(anomalies)}", "",
              "| Meter | District | Day | m3 | Median |", "|---|---|---|---:|---:|"]
    lines += [
        f"| {a.meter_id} | {meters[a.meter_id].district} | {a.day.isoformat()} | {a.m3:.3f} | {a.median:.3f} |"
        for a in anomalies
    ]
    return "\n".join(lines) + "\n"
