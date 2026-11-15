---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "4.1"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D4_1_run_notebook_out.html"
---

# Lab 4.1 · Find the notebook's hidden state

Run a notebook out of order, find the hidden-state bug, then restart and run all; then choose a home for four tasks.

Day 4 · Session 1: What notebooks hide

### Goal

Salma's notebook shows 27 anomalies for September, and it has always worked for her. Find out what her kernel remembered that the file does not hold, repair the notebook so that it runs from top to bottom for anyone, and decide which of four tasks belong in a notebook at all.

## What you need

- The folder `4.1` of the workspace: `analysis.ipynb`, `finding.md`, `homes.md` and the data
- A way to open a notebook: JupyterLab, or an editor that opens notebooks with the workspace's environment as its kernel
- AI policy: tutor. An assistant may explain an error message; the two findings are yours

### Read the saved notebook and its execution counts 4 min

```bash
# file: terminal
cd ../4.1
uv run --with jupyterlab jupyter lab analysis.ipynb
```

Run nothing yet. Read the number in brackets beside each code cell, from the top of the page down, and write the sequence on paper. Which numbers are missing? Which cells were run after the cell below them? Note the anomaly count the page shows.

### Restart and run all; find the missing name 7 min

In the menu: **Kernel**, then **Restart Kernel and Run All Cells**. The run stops. Read the last line of the error: which name is not defined, and which cell needed it? No cell on the page defines it, and the counts told you a cell was run and is gone.

Add a cell above the cleaning cell that defines the name from what the first cell already loaded: the set of the meter ids in the registry. Write finding 1 in `finding.md`: what was missing, and why the saved file did not show it.

### Find the stale number and give factor one home 7 min

Restart and run all again. The run now reaches the end. Compare the anomaly count with the one you noted in the first step. Which cell changed `factor`, and in which order must the cells have been run for the page to show 27 under a cell that says 3.0?

Repair it so that the question "what if we were stricter?" cannot change the answer above it: give the second threshold its own name and its own list, and leave `factor` set in one cell only. Restart, run all, save. Write finding 2.

```python
# file: the last cell, repaired
strict_factor = 2.0
strict = [...]      # the same rule, with strict_factor
print(len(strict), "anomalies at the stricter factor")
```

### Choose a home for four tasks; run the check 7 min

Open `homes.md`. For each of the four tasks write one word, notebook, script or module, and one line of reason. Compare with your neighbour before you run the check.

```bash
# file: terminal
uv run ../lab.py check 4.1
```

The check runs your notebook in a fresh kernel, compares every saved output with what the code prints, and compares your four choices with the reference: three of four is the mark.

### ✱ Stretch

Run the notebook without opening it, as a scheduled job would, and read the count in the copy it writes.

```bash
# file: terminal
uv run --with nbconvert jupyter nbconvert --to notebook --execute analysis.ipynb --output run.ipynb
```

## Check yourself

1. The saved counts were 1, 3, 4, 8, 9, 7. What does each gap or step backwards tell you?
2. Why did the notebook "work" on Salma's laptop for weeks?
3. Which one habit would have caught both problems before the number went into a report?
