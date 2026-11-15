# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Build the lab workspace of the course, beside the course folder.

    uv run labs/kit/setup.py                 # writes ../manahil-labs with all sixteen labs
    uv run labs/kit/setup.py --to <folder>   # somewhere else
    uv run labs/kit/setup.py --force         # replace the kit of an existing workspace

Your lab folders are never touched by a second run: only what is missing is written. To start
one lab again, use `uv run lab.py start <lab> --discard` inside the workspace.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))

import labtool  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the lab workspace.")
    parser.add_argument("--to", type=Path, default=KIT.parents[2] / "manahil-labs")
    parser.add_argument("--force", action="store_true", help="replace the workspace's copy of the kit")
    parser.add_argument("--only", help="build one lab, for example 2.1")
    args = parser.parse_args()
    root: Path = args.to.resolve()
    root.mkdir(parents=True, exist_ok=True)
    kit_copy = root / ".kit"
    if kit_copy.exists() and args.force:
        shutil.rmtree(kit_copy)
    if not kit_copy.exists():
        shutil.copytree(KIT, kit_copy, ignore=shutil.ignore_patterns("__pycache__", "workspace", "setup.py"))
    for source in sorted((KIT / "workspace").iterdir()):
        if source.is_file() and (args.force or not (root / source.name).exists()):
            shutil.copy(source, root / source.name)
    built = []
    for lab in labtool.LABS:
        if args.only and lab != args.only:
            continue
        if not (root / lab).exists():
            labtool.build(lab, root / lab)
            built.append(lab)
    print(f"workspace: {root.name} ({len(built)} lab folders written, {len(labtool.LABS) - len(built)} kept)")
    print(f"next: cd into {root.name}, then: uv run lab.py list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
