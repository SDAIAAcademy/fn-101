"""Dalil, the course tutor: it gives hints, never the code.

    uv run ../tutor.py --recorded                          # the next recorded hint for this lab
    uv run ../tutor.py "why do two keys show the same list?"   # a free hosted model answers
    uv run ../tutor.py --file miqyas/report.py "where would you look first?"

Run it from inside a lab folder. Every question and every answer is added to tutor_log.md in
that folder: the log is part of the lab's evidence, and it is what you reread before you
write the explanation in your own words.

The hosted path needs a key in the environment and nothing else:

    TUTOR_API_KEY     (or OPENROUTER_API_KEY)   the key of a free account
    TUTOR_BASE_URL    default https://openrouter.ai/api/v1   (any chat-completions address)
    TUTOR_MODEL       default google/gemma-4-31b-it:free

Without a key, use --recorded: a fixed ladder of hints written for the lab, each one a little
more direct than the one before. Standard library only.

What leaves this computer on the hosted path: your question and the source files you name
with --file. Data files are refused (they hold customers' text), and so is any file that is
not Python or Markdown.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = "tutor_log.md"
SENDABLE = {".py", ".md"}
MAX_FILE = 12_000        # characters of one file that may be sent

RULE = """You are Dalil, the tutor of a Python course for beginners. The learner is debugging.
Your job is that the learner finds and understands the defect, not that the defect gets fixed.

Rules, in this order:
1. Never write the corrected code, a corrected line, or a patch, and never name the exact line
   to change. If asked for the answer, say that you give hints, and give a hint.
2. Give one hint at a time, three sentences at most: a question to ask of the program, an
   experiment to run (a print, a test, a tiny input), or a concept to reread.
3. Ask what the learner expected and what they saw before you say anything about the cause.
4. End with one question the learner can answer by running something.
5. Answer in the language of the question.
"""

CODE_BLOCK = re.compile(r"```.*?```", re.S)


def withhold_code(answer: str) -> str:
    """A hosted model sometimes writes code in spite of the rule: the block is not shown."""
    return CODE_BLOCK.sub("[the tutor wrote code here; it is withheld: ask for a hint in words]", answer)


def recorded(lab: str, folder: Path) -> str:
    file = ROOT / ".kit" / "hints" / f"{lab}.json"
    if not file.is_file():
        raise SystemExit(f"no recorded hints for the folder {lab}: run the tutor inside a lab folder that has them (4.4)")
    hints: list[str] = json.loads(file.read_text(encoding="utf-8"))
    log = folder / LOG
    used = log.read_text(encoding="utf-8").count("## Recorded hint") if log.is_file() else 0
    if used >= len(hints):
        return ("There are no more recorded hints. Reread the last one, run the experiment it "
                "names, and write what you saw in the log.")
    return hints[used]


def readable(names: list[str], folder: Path) -> str:
    parts = []
    for name in names:
        path = (folder / name).resolve()
        if folder.resolve() not in path.parents or "data" in path.relative_to(folder.resolve()).parts:
            raise SystemExit(f"{name}: the tutor reads source files of this lab folder only, never data")
        if path.suffix not in SENDABLE or not path.is_file():
            raise SystemExit(f"{name}: the tutor reads .py and .md files that exist; this is not one")
        parts.append(f"--- {name}\n{path.read_text(encoding='utf-8')[:MAX_FILE]}")
    return "\n\n".join(parts)


def hosted(question: str, files: str) -> str:
    key = os.environ.get("TUTOR_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("no key in TUTOR_API_KEY or OPENROUTER_API_KEY: use --recorded, "
                         "or set a key of a free account (see the lab page)")
    base = os.environ.get("TUTOR_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    model = os.environ.get("TUTOR_MODEL", "google/gemma-4-31b-it:free")
    content = question if not files else f"{question}\n\nThe files I am looking at:\n\n{files}"
    body = json.dumps({"model": model, "temperature": 0.2, "max_tokens": 300,
                       "messages": [{"role": "system", "content": RULE},
                                    {"role": "user", "content": content}]}).encode("utf-8")
    request = urllib.request.Request(base + "/chat/completions", data=body, method="POST",
                                     headers={"Authorization": f"Bearer {key}",
                                              "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            reply = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as problem:
        raise SystemExit(f"the hosted model answered {problem.code} {problem.reason}: "
                         "check the key and the model name, or use --recorded") from None
    except (urllib.error.URLError, TimeoutError) as problem:
        raise SystemExit(f"the hosted model could not be reached ({problem}): use --recorded") from None
    try:
        answer = reply["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise SystemExit("the hosted model sent an answer in a shape the tutor does not know: use --recorded") from None
    return withhold_code(str(answer).strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tutor", description="Hints for the lab you are in; never the code.")
    parser.add_argument("question", nargs="?", help="your question, in your own words, in quotes")
    parser.add_argument("--recorded", action="store_true", help="the next recorded hint (no key, no network)")
    parser.add_argument("--file", action="append", default=[], help="a source file to show the tutor; may repeat")
    args = parser.parse_args(argv)
    folder = Path.cwd()
    if folder == ROOT or folder.parent != ROOT:
        print("run the tutor from inside a lab folder, for example: cd 4.4")
        return 2
    if args.recorded:
        heading, asked, answer = "## Recorded hint", "(the next recorded hint)", recorded(folder.name, folder)
    elif args.question:
        heading, asked = "## Question", args.question
        answer = hosted(args.question, readable(args.file, folder))
    else:
        parser.print_help()
        return 2
    with open(folder / LOG, "a", encoding="utf-8", newline="\n") as log:
        log.write(f"{heading}\n\n{asked}\n\n**Tutor:** {answer}\n\n")
    sys.stdout.write(answer + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
