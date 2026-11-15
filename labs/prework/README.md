# Pre-work: values, conditions and loops

For anyone who has not yet written and run a short program. About three hours, at your own
pace, in the week before the course. If you have programmed in any language, do the entry
quiz first: eight of ten right and you may skip the sheets.

## Set up once

1. Install uv, the tool the course uses to run Python: follow https://docs.astral.sh/uv/
   for your system. Nothing else needs installing; uv fetches Python itself.
2. Make a folder for the pre-work, and in it a file `try.py` with one line: `print(2 + 3)`.
3. In a terminal in that folder: `uv run try.py`. It prints 5. You have run a program.

If step 3 fails on your work laptop, write down the message and send it to your trainer
before the course: it is the same setup the labs use.

## The three sheets

| Sheet | What it practises |
|---|---|
| [`1_values.md`](1_values.md) | numbers and text, names, arithmetic, turning text into a number |
| [`2_conditions.md`](2_conditions.md) | `if`, `elif`, `else`, comparisons, `and`, `or`, `not` |
| [`3_loops.md`](3_loops.md) | `for` over a list, `range`, a running total, `while`, positions in a list |

For each snippet: **predict first**, on paper, what it prints. Then put it in `try.py`, run it
and compare. When your prediction was wrong, do not move on: find the line you misread. This
habit, predicting before running, is what the first day of the course is built on.

One snippet in each sheet stops with an error. Read the last line of the message, say what is
wrong, and repair it.

## The entry quiz

[`entry_quiz.md`](entry_quiz.md): ten questions, fifteen minutes, nothing run and no
assistant. Bring your answers to the first morning. The result decides nothing about your
place in the course; it tells you and your trainer where to look in the first hour.

## AI assistants

Leave them closed for the pre-work. The exercises are small on purpose: the point is that
you can say what a line does. An assistant can say it for you, and then you have not practised.

Answers for all sheets and the quiz: `labs/solutions/prework.md`.
