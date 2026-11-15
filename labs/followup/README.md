# Follow-up task: one new validation rule, with tests, reviewed by a peer

Two weeks after the course, alone at your desk. About two hours of work and half an hour of
review. It is tracked: your trainer records that the three parts below were handed in.

## The task

Add one rule to Miqyas, the tool of the labs. Work in a copy of your lab folder `4.4` (the
package with the three defects fixed), under version control if you have it.

**The rule.** A reading dated after the last day of the month the file is for is rejected with
the reason `FUTURE_DATE`. The month is given to the tool, not read from the clock: add an
argument `--month 2026-09` to the command. Without the argument the rule is not applied and
the report is what it was.

The September file has no such row, so your tests need rows you write yourself.

## What to hand in

1. **The change**: the rule in `miqyas/readings.py`, the argument in `miqyas/cli.py`, type
   hints that the strict checker accepts.
2. **Tests**: at least four, in a file `test_future_date.py`: the last day of the month
   (accepted), the first day of the next month (rejected, with the reason), a call without
   the month (accepted), and one that shows where the new rule stands in the order of the
   existing rules. All earlier tests still pass, and the report on the September file is
   byte for byte what it was.
3. **A peer review**: exchange your change with one other participant. Each writes for the
   other, in a file `REVIEW.md`: one thing that is right and why, one input the tests do not
   cover, and one question about a line. The author answers the question in the same file.

## The method

Use the week's order of work: write the tests first and watch them fail, then the rule. If you
use an assistant, use it as in lab 4.4: your attempt, then a hint, then your own explanation,
which here is the answer to your reviewer's question.

## For the trainer

Evidence to record per participant: the diff, the output of `uv run pytest` and of
`uv run mypy --strict miqyas`, and `REVIEW.md` with both parts. A reference outline, not a
reference solution, is in `labs/solutions/answer_key.md`: where the rule goes in the order,
and the four tests' cases.
