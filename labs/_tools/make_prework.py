"""Write the pre-work: three exercise sheets, the entry quiz, and their answers.

    uv run labs/_tools/make_prework.py

Every snippet is run here; what it prints (or the last line of the error it raises) is what
goes into labs/solutions/prework.md. Only the explanations are typed by hand.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]

# (snippet, explanation). A snippet that ends in an error is a "find the mistake" exercise.
VALUES = [
    ("litres = 1500\nm3 = litres / 1000\nprint(m3)", "/ always gives a number with a decimal point."),
    ("days = 30\nweeks = days // 7\nleft = days % 7\nprint(weeks, left)", "// is whole division, % is the remainder."),
    ("name = \"meter\"\nprint(name + \"-\" + \"42\")\nprint(len(name))", "+ joins two strings; len counts characters."),
    ("reading = \"0.742\"\nprint(reading * 2)", "The quotes make it text. Text times 2 is the text twice."),
    ("reading = float(\"0.742\")\nprint(reading * 2)", "float turns the text into a number first."),
    ("total = 3\ntotal = total + 2\ntotal += 1\nprint(total)", "A name can be bound again; += is short for the line above it."),
    ("price = 4\nprint(\"total: \" + price)", "Text and a number cannot be joined with +. Write str(price), or an f-string."),
]
CONDITIONS = [
    ("m3 = 0.9\nif m3 > 1:\n    print(\"high\")\nelse:\n    print(\"normal\")", "0.9 is not above 1, so the else branch runs."),
    ("m3 = 250\nif m3 > 200:\n    print(\"reject\")\nelif m3 > 100:\n    print(\"check\")\nelse:\n    print(\"accept\")",
     "The first true condition wins; the others are not looked at."),
    ("district = \"Al-Rabwa\"\nprint(district == \"al-rabwa\")\nprint(district != \"Al-Naseem\")", "Comparison of text is exact: capital letters count."),
    ("m3 = 5\nprint(0 <= m3 <= 200)\nprint(m3 > 1 and m3 < 3)\nprint(not m3 == 5)", "and needs both sides; not turns True into False."),
    ("text = \"\"\nif text:\n    print(\"has text\")\nelse:\n    print(\"empty\")", "An empty string counts as false in a condition."),
    ("m3 = 5\nif m3 = 5:\n    print(\"five\")", "= binds a name, == compares. A condition needs ==."),
]
LOOPS = [
    ("for day in [1, 2, 3]:\n    print(day * 10)", "The body runs once for each item."),
    ("total = 0\nfor value in [0.5, 1.5, 2.0]:\n    total = total + value\nprint(total)", "The print is outside the loop, so it runs once, at the end."),
    ("count = 0\nfor value in [0.5, 250.0, 1.5, 300.0]:\n    if value > 200:\n        count += 1\nprint(count)", "A condition inside a loop: two values are above 200."),
    ("for i in range(3):\n    print(i)", "range(3) gives 0, 1 and 2: three numbers, starting at zero."),
    ("values = [4, 8, 6]\nprint(values[0], values[-1], len(values))", "Positions start at 0; -1 is the last item."),
    ("n = 3\nwhile n > 0:\n    print(n)\n    n -= 1\nprint(\"done\")", "A while loop runs as long as its condition is true."),
    ("for value in [1, 2, 3]:\nprint(value)", "The body of a loop must be indented."),
]
# (question, options, index of the right one, explanation)
QUIZ = [
    ("What does `print(7 // 2, 7 % 2)` print?", ["3.5 1", "3 1", "3 0.5", "4 1"], 1, "Whole division gives 3, the remainder is 1."),
    ("After `a = 5` and `a = a + 1`, what is `a`?", ["5", "an error: a is already 5", "6", "a + 1"], 2, "The right side is computed first, then the name is bound to the result."),
    ("What is `\"12\" + \"3\"`?", ["15", "an error", "\"123\"", "\"15\""], 2, "Both are text, so + joins them."),
    ("Which line compares two values?", ["x = 3", "x == 3", "x := 3", "x => 3"], 1, "== compares; = binds a name."),
    ("How many times does the body of `for i in range(4):` run?", ["4", "3", "5", "it depends on i"], 0, "range(4) gives 0, 1, 2, 3."),
    ("`values = [10, 20, 30]`. What is `values[1]`?", ["30", "10", "an error", "20"], 3, "Positions start at 0."),
    ("Which condition is true for `m3 = 200`?", ["m3 > 200", "m3 < 200", "m3 >= 200", "m3 != 200"], 2, ">= includes the boundary."),
    ("What does `float(\"N/A\")` do?", ["gives 0.0", "gives None", "gives \"N/A\"", "raises an error"], 3, "Text that is not a number cannot be converted: Python raises a ValueError."),
    ("In `if a:` followed by an indented line and then a line that is not indented, when does the last line run?", ["only if a is true", "only if a is false", "always", "never"], 2, "Only the indented line belongs to the if."),
    ("`total = 0`, then a loop adds 2 three times, then `print(total)` after the loop. What is printed?", ["6", "2", "2 4 6", "0"], 0, "The print is after the loop and runs once."),
]
PARTS = [("1", "values", "Values, names and arithmetic", VALUES), ("2", "conditions", "Conditions", CONDITIONS),
         ("3", "loops", "Loops and lists", LOOPS)]


def run(source: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp) / "exercise.py"
        file.write_text(source, encoding="utf-8")
        done = subprocess.run([sys.executable, str(file)], capture_output=True, text=True, encoding="utf-8",
                              env=dict(os.environ, PYTHONUTF8="1"), check=False)
    if done.returncode != 0:
        return "error: " + done.stderr.strip().splitlines()[-1]
    return " / ".join(done.stdout.strip().splitlines())


def main() -> int:
    answers = ["# Pre-work: answers", "",
               "Every output below was produced by running the snippet. Check your sheet only after you have written all your answers.", ""]
    for number, name, title, items in PARTS:
        sheet = [f"# Pre-work {number}: {title}", "",
                 "Write what each snippet prints before you run it. Then run it and compare. One snippet",
                 "in each sheet stops with an error: say which, and how you would repair it.", ""]
        answers += [f"## Pre-work {number}: {title}", ""]
        for n, (source, why) in enumerate(items, start=1):
            sheet += [f"**{n}.**", "", f"```python\n{source}\n```", ""]
            answers += [f"**{n}.** `{run(source)}`. {why}", ""]
        (LABS / "prework" / f"{number}_{name}.md").write_text("\n".join(sheet), encoding="utf-8", newline="\n")
    quiz = ["# Entry quiz", "",
            "Ten questions, fifteen minutes, without running anything and without an assistant. Eight right",
            "answers mean you are ready for Day 1. With fewer, do the sheet of the questions you missed again,",
            "and tell your trainer before the course starts: nobody is turned away for the result.", ""]
    answers += ["## Entry quiz", ""]
    for n, (question, options, right, why) in enumerate(QUIZ, start=1):
        quiz += [f"**{n}.** {question}", ""] + [f"- {'ABCD'[i]}. {option}" for i, option in enumerate(options)] + [""]
        answers += [f"**{n}.** {'ABCD'[right]}. {why}", ""]
    (LABS / "prework" / "entry_quiz.md").write_text("\n".join(quiz), encoding="utf-8", newline="\n")
    (LABS / "solutions" / "prework.md").write_text("\n".join(answers), encoding="utf-8", newline="\n")
    print("pre-work written:", sum(len(items) for *_, items in PARTS), "snippets,", len(QUIZ), "quiz questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
