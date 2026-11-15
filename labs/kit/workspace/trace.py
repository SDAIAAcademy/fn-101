"""Step through a short program and show what every line changes.

    uv run ../trace.py snippets/s4.py

For each line that runs you see the line, then the names it bound or changed, and which
names share one object. It does offline what a step visualiser such as Python Tutor does in
a browser. Standard library only; meant for programs of a few dozen lines.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import FrameType
from typing import Any

SHARED = (list, dict, set)


def show(value: object) -> str:
    text = repr(value)
    return text if len(text) <= 70 else text[:67] + "..."


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1]).resolve()
    source = path.read_text(encoding="utf-8").splitlines()
    code = compile(path.read_text(encoding="utf-8"), str(path), "exec")
    before: dict[int, dict[str, str]] = {}
    step = 0

    def report(frame: FrameType) -> None:
        names = {k: v for k, v in frame.f_locals.items() if not k.startswith("__") and not callable(v)}
        old = before.get(id(frame), {})
        new = {k: show(v) for k, v in names.items()}
        for name, text in new.items():
            if old.get(name) != text:
                print(f"        {name} = {text}")
        groups: dict[int, list[str]] = {}
        for name, value in names.items():
            if isinstance(value, SHARED):
                groups.setdefault(id(value), []).append(name)
        for same in groups.values():
            if len(same) > 1 and any(old.get(n) != new[n] for n in same):
                print(f"        one object, {len(same)} names: {', '.join(same)}")
        before[id(frame)] = new

    def tracer(frame: FrameType, event: str, arg: Any) -> Any:
        nonlocal step
        if frame.f_code.co_filename != str(path):
            return None
        if event == "call":
            if frame.f_code.co_name != "<module>":
                print(f"      -> call {frame.f_code.co_name}()")
            before[id(frame)] = {}
        elif event == "line":
            report(frame)
            step += 1
            print(f"{step:3d}  line {frame.f_lineno:2d}: {source[frame.f_lineno - 1]}")
        elif event == "return":
            report(frame)
            if frame.f_code.co_name != "<module>":
                print(f"      <- {frame.f_code.co_name}() returns {show(arg)}")
        return tracer

    scope: dict[str, object] = {"__name__": "__main__"}
    sys.settrace(tracer)
    try:
        exec(code, scope)
    finally:
        sys.settrace(None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
