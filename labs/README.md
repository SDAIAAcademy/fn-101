# Labs

Sixteen labs of 25 minutes on one case, Manahil Water Services, done in a terminal and an
editor on a laptop. No lab needs a GPU, a paid service or a downloaded model. One lab (4.4)
can use a free hosted model and works without it.

## Build the workspace

You need [uv](https://docs.astral.sh/uv/) and nothing else; uv fetches Python.

    uv run labs/kit/setup.py

This writes a folder `manahil-labs` beside the course folder: one sub-folder per lab with its
supplied starting state and its data, and one Python project for all of them. Then:

    cd ../manahil-labs
    uv sync                    # once, with a network: pytest, mypy, ruff and the notebook kernel
    uv run lab.py list
    uv run lab.py check 1.2    # is the evidence of lab 1.2 there?
    uv run lab.py start 1.2 --discard    # throw your folder away and start the lab again

Every lab starts from its own folder, so a lab you did not finish never blocks the next one.
The data is written by a generator with a fixed seed (`labs/kit/data.py`): the same files on
every machine, all synthetic.

## What is where

| Path | What it is |
|---|---|
| `D1_1_….html` to `D4_4_….html` | The sixteen lab pages: goal, steps with minutes, a stretch, questions, notes for the trainer |
| `kit/` | The workspace builder: starting files (`start/`), the reference package Miqyas (`base/`), the checks, the data generator, the tutor's recorded hints |
| `solutions/` | A reference answer for every lab, the answers of the drills and of the pre-work, and `answer_key.md` |
| `drills/` | The four ten-minute paper drills that open the days, done with AI off |
| `prework/` | Exercises and an entry quiz for those who have not programmed before |
| `followup/` | The tracked task after the course: one new rule, with tests and a peer review |
| `capstone/` | The capstone's brief, data, public sample tests and README template |
| `_tools/` | Scripts that write the drills, the pre-work, the notebooks and the capstone data; a grader for the capstone; a stand-in for a hosted model |

## For trainers: run every reference solution

    uv run labs/solutions/run_all.py            # all sixteen; the last line counts the labs that pass
    uv run labs/solutions/run_all.py 3.4 4.4    # these two

It builds a fresh workspace in a temporary folder, lays each reference answer over the lab's
starting state, runs what the participant would run, then the lab's own check.

## The tutor and hosted models

Lab 4.4 uses `tutor.py`. `uv run ../tutor.py --recorded` needs no key and no network. A
question in quotes is sent to a hosted model through a chat-completions address; set
`TUTOR_API_KEY` (or `OPENROUTER_API_KEY`) to the key of a free account, and `TUTOR_MODEL` if
the default free model is not offered any more. Only the question and the source files named
with `--file` are sent; data files are refused.

The workspace holds an `AGENTS.md` that tells any coding assistant opened there to act as a
tutor: hints, not code. Assistants are off for the drills, for the first attempt at labs 3.4
and 4.4, and for the supervised check.

## Opening the notebook of lab 4.1

    cd 4.1
    uv run --with jupyterlab jupyter lab analysis.ipynb

An editor that opens notebooks works as well; choose the environment of `manahil-labs` as the
kernel.
