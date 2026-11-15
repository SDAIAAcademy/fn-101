---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "3.2"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D3_2_open_ticket_file.html"
---

# Lab 3.2 · Decode a ticket file that fails

Open a ticket file that fails to decode, read it with the declared encoding and list the lines that still fail.

Day 3 · Session 2: Text, bytes and encodings

### Goal

A ticket file refuses to open. Read the error, open the file with the encoding its export declares, and then list exactly which lines still fail and at which byte, without ignoring or replacing anything.

## What you need

- The folder `3.2` of the workspace: `decode.py`, `data/tickets_branch.jsonl` (120 lines) and `data/tickets_branch.meta.json`, the note the export wrote about itself
- AI policy: tutor. An assistant may explain an error message; you write the loop

### Run the loader and read the error it raises 5 min

```bash
# file: terminal
cd ../3.2
uv run python decode.py
```

The run ends in a `UnicodeDecodeError`. Read its last line and write down three things: which codec was decoding, which byte it could not decode, and at which position. Now look at `load` in `decode.py`: where did that codec come from?

### Open the file with its declared encoding 5 min

Open `data/tickets_branch.meta.json`: the export says which encoding it wrote. At a prompt, read the whole file with that encoding.

```python
# file: at a prompt
>>> text = open("data/tickets_branch.jsonl", encoding="utf-8").read()
```

A new error, with another codec, another byte and a position far into the file. Most of the file is what it claims to be; something in it is not. A position in the whole file does not tell you which line: the next step does.

### Decode line by line and collect each failure 9 min

Write `decode_lines`. Read the file as bytes, split it into lines, and decode each line by itself inside a `try`. A line that decodes joins the first list. For a line that does not, the exception tells you where: `problem.start` is the position of the offending byte within the line.

```python
# file: decode.py
data = Path(path).read_bytes()
for line_no, raw in enumerate(data.splitlines(), start=1):
    try:
        ...
    except UnicodeDecodeError as problem:
        failed.append(Failure(line_no, problem.start, hex(raw[problem.start])))
```

Do not reach for `errors="ignore"` or `errors="replace"`: both make the error go away by damaging the text of a customer's ticket without telling anyone.

### Write the report; run the lab check 6 min

Finish `main` as its comment says: read the encoding from the meta file, call `decode_lines`, print the failures, and write `out/decode_report.json`. `dataclasses.asdict` turns a `Failure` into a dictionary. The function `load` and `LAPTOP_DEFAULT` can go.

```bash
# file: terminal
uv run python decode.py
uv run mypy --strict decode.py
uv run ../lab.py check 3.2
```

### ✱ Stretch

The failing lines came from an old branch terminal that writes Windows-1256 (`cp1256`). Decode those lines with that encoding and print the tickets they hold. Then decode a good line with `cp1256` and look at what you get: no error, and no ticket either.

## Check yourself

1. The first error named a codec that appears nowhere in the export's note. Where did it come from?
2. Why does decoding line by line find seven failures, when reading the whole file reports one?
3. A good line decoded as `cp1256` raises no error. Is it decoded correctly?
