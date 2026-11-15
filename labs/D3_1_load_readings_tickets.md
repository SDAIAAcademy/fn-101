---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "3.1"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D3_1_load_readings_tickets.html"
---

# Lab 3.1 · Write a district summary with phones masked

Load readings and tickets and write a JSON summary per district, masking phone numbers before anything is written.

Day 3 · Session 1: CSV and JSON Lines

### Goal

Read two CSV files and a JSON Lines file, and write one JSON summary per district that a colleague can open. The tickets are personal data: no phone number and no identity number may reach the file or the screen.

## What you need

- The folder `3.1` of the workspace: `summary.py`, and in `data/` the files `readings_clean.csv`, `meters.csv` and `tickets.jsonl`
- AI policy: tutor. Do not paste ticket lines into an assistant: in real work they would be customers' data

### Load the two CSV files and the JSON Lines file 7 min

```bash
# file: terminal
cd ../3.1
uv run python summary.py
```

Write `load_csv` and `load_jsonl`. Name the encoding in both; for CSV also pass `newline=""`, so that the csv module handles line ends itself. A JSON Lines file is one JSON value per line: one `json.loads` per line.

```python
# file: summary.py
with open(path, encoding="utf-8", newline="") as file:
    return list(csv.DictReader(file))
```

Look at the first line of `data/tickets.jsonl` in your editor. Which of its ten fields would you not want in an email?

### Mask the phone field and the phone numbers in text 8 min

Write `mask_phone`: every digit except the last two becomes a star, other characters stay. Then `mask_text`: people type callback numbers into the free text, so every match of the supplied pattern `PHONE` is replaced by `[phone]`.

```python
# file: at a prompt
>>> mask_phone("+966555010042")
'+**********42'
>>> mask_text("call me on 0555012345")
'call me on [phone]'
```

The supplied function `summarise` calls both for the open urgent tickets of each district. It never copies the identity number.

### Write the summary as JSON; read it as a reviewer 6 min

Write `write_json` with `json.dump`: `indent=2` so that a person can read it, `ensure_ascii=False` so that Arabic stays Arabic, the encoding named.

```bash
# file: terminal
uv run python summary.py
```

Open `out/summary.json` and read it as Abdulaziz, the data protection officer, would: search it for `055`, for `966` and for `national`. Then read two Arabic callback texts to the end.

### Run the type checker and the lab check 4 min

```bash
# file: terminal
uv run mypy --strict summary.py
uv run ../lab.py check 3.1
```

### ✱ Stretch

Change `\d` in the pattern to `[0-9]`, run again and count the phone numbers that now slip through. Find one of them in the tickets file and say what is different about its digits. Put `\d` back.

## Check yourself

1. The summary never contains the identity number. Which line of the program made sure of that?
2. Why is masking done before `json.dump` and not by editing the file afterwards?
3. What does the file look like with `ensure_ascii` left at its default?
