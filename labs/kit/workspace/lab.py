"""Start a lab from its supplied state, or check it.

    uv run lab.py list
    uv run lab.py start 2.1
    uv run lab.py check 2.1

From inside a lab folder the same file is one level up: uv run ../lab.py check 2.1
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".kit"))

import labtool  # noqa: E402

raise SystemExit(labtool.main(ROOT, sys.argv[1:]))
