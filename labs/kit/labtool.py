"""Build a lab's starting folder, and check the evidence when the lab is done.

Used through lab.py in the workspace:

    uv run lab.py list
    uv run lab.py start 2.1            # a fresh folder 2.1 from the supplied state
    uv run lab.py start 2.1 --discard  # throw the folder away and start again
    uv run lab.py check 2.1            # is the evidence of the lab there?

Standard library only. A check reads files and runs your code; it tells you what is missing.
It cannot judge an explanation or a debugging log: your trainer and your neighbour do that.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))

import data  # noqa: E402

LABS = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "2.4",
        "3.1", "3.2", "3.3", "3.4", "4.1", "4.2", "4.3", "4.4"]

# The files of the case study each lab starts with.
DATA = {
    "1.2": ["sample_meter"],
    "2.1": ["meters", "readings_clean", "readings_large"],
    "2.2": ["meters", "readings"],
    "2.3": ["readings_large"],
    "2.4": ["tickets"],
    "3.1": ["meters", "readings_clean", "tickets"],
    "3.2": ["tickets_branch"],
    "3.3": ["tickets_raw"],
    "3.4": ["meters", "readings"],
    "4.1": ["meters", "readings"],
    "4.2": ["meters", "readings"],
    "4.4": ["meters", "readings"],
}

# The seeded defects: (file of the package, the sound text, the defective text).
DEFECTS = {
    "D1": ("readings.py",
           "    seen: set[tuple[str, date]] | None = None,\n",
           "    seen: set[tuple[str, date]] = set(),\n"),
    "D1b": ("readings.py",
            "    if seen is None:\n        seen = set()\n",
            ""),
    "D2": ("anomalies.py",
           "    ordered = sorted(values)\n",
           "    ordered = values\n"),
    "D3": ("report.py",
           "    groups: dict[str, list[Anomaly]] = {district: [] for district in districts}\n",
           "    groups: dict[str, list[Anomaly]] = dict.fromkeys(districts, [])\n"),
}
SEEDED = {"3.4": ["D1", "D1b", "D2"], "4.4": ["D3"]}

# The variants of the anomaly rule that the tests of lab 4.3 must tell from the real one.
VARIANTS = {
    "the boundary counts as an anomaly": (
        "    return value > factor * median(history)\n",
        "    return value >= factor * median(history)\n"),
    "no history counts as an anomaly": (
        "    if not history:\n        return False\n",
        "    if not history:\n        return True\n"),
    "the mean is used in place of the median": (
        "    return value > factor * median(history)\n",
        "    return value > factor * (sum(history) / len(history))\n"),
    "the factor argument is ignored": (
        "    return value > factor * median(history)\n",
        "    return value > 3.0 * median(history)\n"),
}


def package(dest: Path, defects: list[str] | tuple[str, ...] = (), only: list[str] | None = None) -> None:
    """Copy the Miqyas package into dest/miqyas, with the named defects seeded."""
    target = dest / "miqyas"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for source in sorted((KIT / "base" / "miqyas").glob("*.py")):
        if only is not None and source.name not in only:
            continue
        text = source.read_text(encoding="utf-8")
        for name in defects:
            file, sound, defective = DEFECTS[name]
            if file == source.name:
                assert sound in text, f"{name}: the sound text is not in {file}"
                text = text.replace(sound, defective)
        (target / source.name).write_text(text, encoding="utf-8", newline="\n")


def variant(dest: Path, name: str) -> None:
    """Write the anomaly rule with one planted change into dest/miqyas/anomalies.py."""
    sound, changed = VARIANTS[name]
    file = dest / "miqyas" / "anomalies.py"
    text = file.read_text(encoding="utf-8")
    assert sound in text, name
    file.write_text(text.replace(sound, changed), encoding="utf-8", newline="\n")


def build(lab: str, dest: Path) -> None:
    """Write the starting state of one lab into dest (which must not exist)."""
    source = KIT / "start" / lab
    if source.is_dir():
        shutil.copytree(source, dest)
    else:
        dest.mkdir(parents=True)
    for name in DATA.get(lab, []):
        data.write(name, dest)
    if lab in SEEDED:
        package(dest, SEEDED[lab])
    elif lab == "4.2":
        package(dest, only=["__init__.py", "readings.py", "anomalies.py", "report.py"])
        for extra in sorted((source / "miqyas").glob("*.py")):
            shutil.copy(extra, dest / "miqyas" / extra.name)
    elif lab == "4.3":
        package(dest, only=["__init__.py", "readings.py", "anomalies.py"])


def start(root: Path, lab: str, discard: bool = False) -> Path:
    dest = root / lab
    if dest.exists():
        if not discard:
            raise SystemExit(f"{dest.name} exists. Your work is in it: keep it, or pass --discard to start again.")
        shutil.rmtree(dest)
    build(lab, dest)
    return dest


def main(root: Path, argv: list[str]) -> int:
    if not argv or argv[0] not in ("start", "check", "list") or (argv[0] != "list" and len(argv) < 2):
        print(__doc__)
        return 2
    if argv[0] == "list":
        for lab in LABS:
            print(lab, "started" if (root / lab).exists() else "not started")
        return 0
    lab = argv[1]
    if lab not in LABS:
        print(f"no lab {lab}; the labs are {LABS[0]} to {LABS[-1]}")
        return 2
    if argv[0] == "start":
        dest = start(root, lab, "--discard" in argv)
        print(f"lab {lab} starts in the folder {dest.name}: cd {dest.name}")
        return 0
    if not (root / lab).is_dir():
        print(f"lab {lab} is not started: uv run lab.py start {lab}")
        return 2
    import checks
    return checks.run(lab, root / lab)
