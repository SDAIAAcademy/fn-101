---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "2.4"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D2_4_model_ticket_as.html"
---

# Lab 2.4 · Model and sort the ticket queue

Model a ticket as a data class and sort tickets by priority and age.

Day 2 · Session 4: Records as data classes

### Goal

Give the service ticket a type of its own, a frozen data class with typed fields, and put the open tickets in the order customer care works them: most urgent first, oldest first within a priority.

## What you need

- The folder `2.4` of the workspace: `tickets.py` and `data/tickets.jsonl` (400 tickets, text in Arabic and English)
- AI policy: tutor. Hints and explanations of messages, no code

### Define the frozen data class and its age method 8 min

```bash
# file: terminal
cd ../2.4
```

Open `tickets.py` and write the class where the comment of step 1 is. Six fields, in the order given; the decorator makes the class a record that cannot be changed after it is built.

```python
# file: tickets.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    opened: date
    ...

    def age_days(self, today: date) -> int:
        ...
```

Subtracting one date from another gives a difference that has a `.days`. The file's lines also hold a phone number and an identity number. The queue does not need them: do not give the class those fields.

### Build tickets from the lines of the file 6 min

Write `from_record`: it takes the dictionary of one parsed line and returns a `Ticket`. Name each field when you build the record, and turn the text of `opened` into a date with `date.fromisoformat`.

```bash
# file: terminal
uv run python tickets.py
```

The script now gets as far as the queue.

### Sort the open tickets by priority, then age 7 min

Write `queue`. Keep the tickets whose status is `open`, then sort them with a key that returns a tuple: the rank of the priority (from `PRIORITY_RANK`), then the date opened, then the ticket id. Tuples compare item by item, so the second item decides only between tickets with the same first one.

```python
# file: tickets.py
return sorted(waiting, key=lambda t: (..., ..., ...))
```

Run the script and read the first five lines. Are they all urgent, and do their dates rise?

### Run the type checker and the lab check 4 min

```bash
# file: terminal
uv run mypy --strict tickets.py
uv run ../lab.py check 2.4
```

### ✱ Stretch

Count the open tickets per district and priority with a dictionary whose keys are tuples, `dict[tuple[str, str], int]`, and print the three largest counts.

## Check yourself

1. Sorting by the text of the priority would put `high` before `urgent`. Why, and what did you sort by instead?
2. What happens at `ticket.priority = "low"` on your class, and why is that useful in a queue?
3. The identity number is in the file. Where is it in your program after `from_record` has run?
