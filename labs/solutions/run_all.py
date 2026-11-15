# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run the reference solution of every lab, or of the labs named.

    uv run labs/solutions/run_all.py            # all sixteen
    uv run labs/solutions/run_all.py 2.1 3.4    # these two
    uv run labs/solutions/run_all.py --keep     # leave the workspace behind and say where it is

For each lab: build a fresh workspace in a temporary folder, lay the reference files of
labs/solutions/<lab>/ over the lab's starting folder, run the scripts the lab asks the
participant to run, then run the lab's own check. The last line counts the labs that passed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent / "kit"
sys.path.insert(0, str(KIT))

import labtool  # noqa: E402

# What a participant runs in the lab folder before the check (after the reference files are in).
RUNS: dict[str, list[list[str]]] = {
    "2.1": [["python", "timing.py"]],
    "2.3": [["python", "memory.py"]],
    "3.1": [["python", "summary.py"]],
    "3.2": [["python", "decode.py"]],
    "3.3": [["python", "intake.py"]],
    "4.2": [["python", "-m", "miqyas", "report", "--readings", "data/readings_2026_09.csv",
             "--meters", "data/meters.csv", "--out", "out/report.md", "--rejections", "out/rejections.csv"]],
    "4.4": [["python", "../tutor.py", "--recorded"], ["python", "../tutor.py", "--recorded"]],
}


def sh(command: list[str], cwd: Path) -> tuple[int, str]:
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return done.returncode, (done.stdout + done.stderr).strip()


def main() -> int:
    wanted = [a for a in sys.argv[1:] if not a.startswith("--")] or labtool.LABS
    root = Path(tempfile.mkdtemp(prefix="fn101-"))
    status, output = sh([sys.executable, str(KIT / "setup.py"), "--to", str(root)], HERE)
    if status != 0:
        print(output)
        return 1
    passed = 0
    for lab in wanted:
        folder = root / lab
        overlay = HERE / lab
        if overlay.is_dir():
            shutil.copytree(overlay, folder, dirs_exist_ok=True)
        print(f"--- lab {lab}")
        for command in RUNS.get(lab, []):
            status, output = sh(["uv", "run", *command], folder)
            print("\n".join("    " + line for line in output.splitlines()[-8:]))
        status, output = sh(["uv", "run", "lab.py", "check", lab], root)
        print(output)
        passed += status == 0
    if "--keep" in sys.argv:
        print(f"workspace kept: {root}")
    else:
        shutil.rmtree(root, ignore_errors=True)
    print(f"{passed} of {len(wanted)} labs pass")
    return 0 if passed == len(wanted) else 1


if __name__ == "__main__":
    raise SystemExit(main())
