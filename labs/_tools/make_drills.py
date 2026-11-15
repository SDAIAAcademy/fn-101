"""Write the four daily drill sheets and their answers.

    uv run labs/_tools/make_drills.py

Every snippet is run here, and what it really prints (or the traceback it really raises) is
what goes into labs/solutions/drills.md. Nothing in the answers is typed by hand except the
explanations.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]

DAY1 = [
    ("a = [1, 2]\nb = a\nb = b + [3]\nprint(a, b)",
     "Line 3 builds a new list and rebinds b. The list that a names is untouched."),
    ("s = \"meter\"\nt = s\nt = t.upper()\nprint(s, t)",
     "Strings cannot change: upper() returns a new string, and only t is rebound."),
    ("x = [1, 2, 3]\ny = x\ny[0] = 99\nx = [0]\nprint(x, y)",
     "Line 3 mutates the shared list; line 4 rebinds x only, so y keeps the mutated list."),
    ("def reset(values):\n    values = []\n    return values\n\n\ndata = [5]\nreset(data)\nprint(data)",
     "Inside reset the parameter is rebound to a new list. The caller's list is never touched, and the returned list is thrown away."),
    ("def clear(values):\n    values.clear()\n\n\ndata = [5]\nclear(data)\nprint(data)",
     "clear() mutates the one list that both data and values name."),
]

DAY2 = [
    ("d = {\"a\": 1}\ne = d\ne[\"b\"] = 2\nprint(len(d))",
     "One dictionary, two names."),
    ("rows = [{\"m\": 1}] * 2\nrows[0][\"m\"] = 7\nprint(rows)",
     "The list holds the same dictionary twice: multiplying a list repeats references, it does not copy."),
    ("counts = {}\nfor word in [\"a\", \"b\", \"a\"]:\n    counts[word] = counts.get(word, 0) + 1\nprint(counts)",
     "get(word, 0) answers 0 for a key that is not there yet. Keys keep the order in which they were first added."),
    ("a = [3, 1, 2]\nb = sorted(a)\na.sort(reverse=True)\nprint(a, b)",
     "sorted() returns a new list; sort() changes the list in place and returns None."),
    ("t = (1, [2])\nt[1].append(3)\nprint(t)",
     "The tuple cannot be given other items, but the list inside it can still change."),
]

DAY3_SCRIPT = '''import csv
import io

FILE = """meter_id,date,consumption_m3
M-0042,2026-09-01,0.742
M-0042,2026-09-02,N/A
"""


def to_number(text):
    return float(text)


def total(rows):
    result = 0.0
    for row in rows:
        result += to_number(row["consumption_m3"])
    return result


rows = list(csv.DictReader(io.StringIO(FILE)))
print(total(rows))
'''

DAY3_QUESTIONS = [
    ("Which exception was raised, and what does its message say?",
     "ValueError: could not convert string to float: 'N/A'."),
    ("In which function, and on which line of the file, did it happen?",
     "In to_number, on the line `return float(text)`: the last frame of the traceback."),
    ("Who called that function, and who called the caller? Read the frames from the bottom up.",
     "total called to_number (the `result += ...` line); the module's last line called total."),
    ("How many rows had been added to the result before the failure?",
     "One: the first row (0.742) was added, the second holds N/A."),
    ("Name two different repairs, and say what each does with the bad row.",
     "Catch ValueError inside the loop and count the row as skipped; or validate before converting and "
     "collect the row with a reason. Neither lets the row vanish without a trace."),
]

DAY4_PARSONS = [
    "def by_meter(readings):",
    "    groups = {}",
    "    for meter_id, m3 in readings:",
    "        if meter_id not in groups:",
    "            groups[meter_id] = []",
    "        groups[meter_id].append(m3)",
    "    return groups",
]
DAY4_SCRAMBLE = [5, 1, 6, 3, 0, 4, 2]
DAY4_DISTRACTOR = "groups[meter_id] = m3"

DAY4_BUG = '''def average(values):
    """The mean of the values that are numbers; rows that hold None are skipped."""
    total = 0.0
    for value in values:
        if value is None:
            continue
        total += value
    return total / len(values)


print(average([2.0, None, 4.0]))
'''


def run(source: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp) / "drill.py"
        file.write_text(source, encoding="utf-8")
        env = dict(os.environ, PYTHONUTF8="1")
        done = subprocess.run([sys.executable, "drill.py"], cwd=tmp, env=env, capture_output=True, text=True, encoding="utf-8")
    text = (done.stdout + done.stderr).strip()
    text = re.sub(r'File "[^"]*drill\.py"', 'File "drill.py"', text)
    return text


def fence(text: str, language: str = "python") -> str:
    return f"```{language}\n{text}\n```\n"


def predict_sheet(day: int, title: str, items: list[tuple[str, str]]) -> tuple[str, str]:
    sheet = [f"# Drill {day}: {title}", "",
             "Ten minutes, on paper, without a computer and without an assistant. Write what each snippet prints.", ""]
    answers = [f"## Drill {day}: {title}", ""]
    for n, (source, why) in enumerate(items, start=1):
        sheet += [f"**{n}.**", "", fence(source)]
        answers += [f"**{n}.** `{run(source)}`. {why}", ""]
    return "\n".join(sheet), "\n".join(answers)


def main() -> int:
    sheets: dict[int, str] = {}
    answers = ["# Drills: answers", "",
               "For the trainer. Every output below was produced by running the snippet.", ""]
    for day, title, items in ((1, "predict the output", DAY1), (2, "lists and dictionaries that share", DAY2)):
        sheets[day], answer = predict_sheet(day, title, items)
        answers.append(answer)

    traceback = run(DAY3_SCRIPT)
    assert "ValueError" in traceback and "0.742" not in traceback.splitlines()[-1]
    sheet = ["# Drill 3: read a traceback", "",
             "Ten minutes, on paper, without a computer and without an assistant. "
             "The program below was run and stopped with the traceback under it. Answer the five questions.", "",
             fence(DAY3_SCRIPT.strip()), "", fence(traceback, "text"), ""]
    answers += ["## Drill 3: read a traceback", ""]
    for n, (question, answer) in enumerate(DAY3_QUESTIONS, start=1):
        sheet.append(f"{n}. {question}")
        answers += [f"**{n}.** {answer}", ""]
    sheets[3] = "\n".join(sheet) + "\n"

    correct = "\n".join(DAY4_PARSONS)
    assert run(correct + "\n\nprint(by_meter([(\"a\", 1.0), (\"b\", 2.0), (\"a\", 3.0)]))") == "{'a': [1.0, 3.0], 'b': [2.0]}"
    scrambled = [DAY4_PARSONS[i].strip() for i in DAY4_SCRAMBLE]
    scrambled.insert(3, DAY4_DISTRACTOR)
    wrong = run(DAY4_BUG)
    fixed = DAY4_BUG.replace("    total = 0.0\n", "    total = 0.0\n    count = 0\n") \
        .replace("        total += value\n", "        total += value\n        count += 1\n") \
        .replace("len(values)", "count")
    right = run(fixed)
    assert (wrong, right) == ("2.0", "3.0"), (wrong, right)
    sheets[4] = "\n".join([
        "# Drill 4: order the lines, then find the bug", "",
        "Ten minutes, on paper, without a computer and without an assistant.", "",
        "**1.** These lines are one function, scrambled, with one line that does not belong. "
        "`by_meter(readings)` takes pairs of (meter id, cubic metres) and returns a dictionary "
        "from each meter id to the list of its values. Write the lines in order, with their indentation, "
        "and cross out the distractor.", "",
        fence("\n".join(scrambled)),
        "**2.** The function below should print 3.0. Say what it prints, which line is wrong, and how you would repair it.", "",
        fence(DAY4_BUG.strip()),
    ])
    answers += ["## Drill 4: order the lines, then find the bug", "",
                "**1.** The distractor is `" + DAY4_DISTRACTOR + "`: it replaces the list by a single number.", "",
                fence(correct),
                f"**2.** It prints `{wrong}`: the sum of the two numbers divided by three, because `len(values)` "
                f"counts the skipped row too. Count the values that were added and divide by that count; "
                f"the repaired function prints `{right}`. A list that holds only None must then be handled: "
                "decide what the mean of nothing is before dividing.", ""]

    (LABS / "drills").mkdir(exist_ok=True)
    for day, text in sheets.items():
        (LABS / "drills" / f"day{day}.md").write_text(text, encoding="utf-8", newline="\n")
    (LABS / "solutions" / "drills.md").write_text("\n".join(answers), encoding="utf-8", newline="\n")
    print("wrote", len(sheets), "sheets and the answers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
