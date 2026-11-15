---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "4.2"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D4_2_move_supplied_notebook.html"
---

# Lab 4.2 · Give the notebook a command line

Move the supplied notebook logic into a module with a command-line entry point.

Day 4 · Session 2: Scripts, modules and an entry point

### Goal

Turn the repaired notebook into a tool that whoever is on duty can run with one command. The cells have already become functions in a package; you write what is left of the notebook, the order of the calls, as a command line with arguments, logging and an exit code, and you show that two runs write the same bytes.

## What you need

- The folder `4.2` of the workspace: the repaired `analysis.ipynb`, the package `miqyas/` with `readings.py`, `anomalies.py`, `report.py` and a skeleton `cli.py`, and the data
- AI policy: tutor. Ask for hints about argparse or logging; the lines of `main` are yours

### Match the notebook's cells to the package's functions 4 min

Open the notebook beside the three modules. For each code cell, find the function that now does its work and write the pairs on paper: the loading cell, the cleaning cell, the anomaly cell, the district table. Two things the notebook did have no function: it chose the file names, and it ran the cells in order. Those two are the command line.

### Add the three arguments and the entry point 6 min

In `miqyas/cli.py`, `build_parser` has one argument. Add `--meters` and `--out`, both paths and both required, and `--factor`, a float with 3.0 as its default. Then create `miqyas/__main__.py`, the file Python runs for `python -m miqyas`:

```python
# file: miqyas/__main__.py
from miqyas.cli import main

raise SystemExit(main())
```

```bash
# file: terminal
cd ../4.2
uv run python -m miqyas report --help
```

The help text should list four arguments and `-v`. You wrote none of that text: argparse built it from your calls.

### Write main: the cells' order as calls, with logging 9 min

Follow the comments of step 2 in `main`. If an input file is missing, log an error and return 2. Otherwise load the meters, load the readings against the set of known ids, find the anomalies with `args.factor`, render the report, and write it as UTF-8 with `newline="\n"`. Use `log.info` for what each step did. No `print`: the report goes to the file, the messages to the log.

```bash
# file: terminal
uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/report.md -v
```

Read `out/report.md`: 17,561 accepted, 129 rejected, 18 anomalies, the numbers of the notebook.

### Run twice, compare the bytes, run the check 6 min

```bash
# file: terminal
uv run python -m miqyas report --readings data/readings_2026_09.csv --meters data/meters.csv --out out/second.md
uv run python -c "from pathlib import Path; print(Path('out/report.md').read_bytes() == Path('out/second.md').read_bytes())"
uv run python -m miqyas report --readings data/missing.csv --meters data/meters.csv --out out/none.md
uv run mypy --strict miqyas
uv run ../lab.py check 4.2
```

The second command must print True. The third must end with one line and no traceback. The check also runs the tool with `--factor 2` and expects 27 anomalies.

### ✱ Stretch

Add an optional argument `--rejections` that writes every rejected row to a CSV file with the columns line_no, reason and detail. An analyst who doubts a count can then open the 129 rows.

## Check yourself

1. What does `import miqyas.cli` run, and what does `python -m miqyas` run in addition?
2. Why does the report hold no date and no time of the run?
3. A scheduled job runs the tool every month. What does the job read to know whether it worked?
