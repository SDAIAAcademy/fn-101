# Answer key

For the trainer. The numbers are from the reference run of each lab
(`uv run labs/solutions/run_all.py`); the data generator has a fixed seed, so they are the
same on every machine. Each lab page has its own trainer's notes with the common errors.

## The data in numbers

| Fact | Value |
|---|---|
| Meters in the registry; with no reading in September | 600; 12 |
| Rows in the month file; accepted; rejected | 17,690; 17,561; 129 |
| Rejected by reason | MISSING_VALUE 40, DUPLICATE 30, UNKNOWN_METER 20, OUT_OF_RANGE 18, NOT_A_NUMBER 15, BAD_DATE 6 |
| Anomalies at factor 3.0; at 2.0 | 18; 27 |
| Anomalies per district at 3.0 | Al-Faisaliyah 4, Al-Khuzama 3, Al-Murooj 3, Al-Naseem 1, Al-Rabwa 5, Al-Yasmin 2 |
| Tickets; open; urgent callbacks | 400; 246; 25 |
| Ticket texts with a phone number | 14, of which 5 in Arabic-Indic digits |
| Branch ticket file: lines; lines that are not UTF-8 | 120; 7 (lines 12, 22, 37, 55, 82, 84, 94) |
| Raw ticket file: lines; accepted; rejected | 435; 400; 35 |
| Large file: rows | 100,000 |

## Evidence per lab

| Lab | What a finished lab leaves behind | Reference |
|---|---|---|
| 1.1 | `predictions.txt` with eight outputs; `misread.md` naming the misread line for each wrong one | `solutions/1.1/` |
| 1.2 | `monthly_bill.py` as four documented functions; the supplied tests pass; importing it prints nothing | `solutions/1.2/` |
| 1.3 | `parser.py` annotated; strict type check clean; tests pass | `solutions/1.3/` |
| 1.4 | `warmup.py` and `validate.py` assembled from scrambled lines without the distractors; tests pass | `solutions/1.4/` |
| 2.1 | Counts per meter and district; a timing of the nested loop against the dictionary | `solutions/2.1/` |
| 2.2 | The 12 silent meters and the 5 unknown ids (20 rows), by set operations | `solutions/2.2/` |
| 2.3 | A generator pipeline over 100,000 rows; peak memory measured against a list | `solutions/2.3/` |
| 2.4 | A ticket data class; the queue sorted by priority, then age | `solutions/2.4/` |
| 3.1 | `out/summary.json` per district with no phone number in it, the same on two runs | `solutions/3.1/` |
| 3.2 | `out/decode_report.json`: 113 lines decoded, the 7 failing lines with position and byte | `solutions/3.2/` |
| 3.3 | `out/rejections.csv`: 35 lines with one of eight reasons; 400 + 35 = 435 | `solutions/3.3/` |
| 3.4 | `debug_log.md` for defects A and B; a regression test for each | `solutions/3.4/` |
| 4.1 | A notebook that a fresh kernel runs to the end with 18 anomalies; `finding.md`; `homes.md` | `solutions/4.1/` |
| 4.2 | `python -m miqyas report …` writing the same bytes twice; exit code 2 for a missing file | the sound package, `kit/base/miqyas/` |
| 4.3 | Six or more tests that catch the four wrong versions of the rule | `solutions/4.3/` |
| 4.4 | `debug_log.md` for defect C, `tutor_log.md`, a regression test, `explanation.md` | `solutions/4.4/` |

## The three seeded defects

| | Where | The defect | The symptom | The fix |
|---|---|---|---|---|
| A | `load_readings`, `miqyas/readings.py` | a mutable default argument, `seen = set()` | a second load in one process accepts 0 rows and rejects 17,690 as DUPLICATE | default `None`, a new set inside the function |
| B | `median`, `miqyas/anomalies.py` | the values are not sorted | the report shows 0.653 as the median of M-0012; it is 0.696 | `sorted(values)` |
| C | `anomalies_by_district`, `miqyas/report.py` | `dict.fromkeys(districts, [])`: one list for all keys | every district shows 18 anomalies | a comprehension that makes a list per district |

## Where each course outcome is evidenced

| Outcome | Evidence in the course | Where |
|---|---|---|
| LO1 | a trace sheet, eight of ten right | drills 1 and 2 (ten snippets), lab 1.1, and the supervised check |
| LO2 | a choice and a reason for four tasks, three of four matching | `homes.md` of lab 4.1: notebook, script, module, notebook |
| LO3 | a module that passes the tests and a strict type check | labs 1.3, 1.4 and 2.1 to 2.4 |
| LO4 | a rejection log that accounts for every line | labs 3.2 and 3.3 |
| LO5 | a log and a regression test per defect | labs 3.4 (A and B, AI off) and 4.4 (C, AI off for the first step) |
| LO6 | one command, the same report on two runs | lab 4.2 |

## The supervised AI-off check

The check is one hour, in the room, on paper and in a locked editor: ten unseen snippets to
trace (eight right is the mark for LO1), one Parsons problem, and one debugging task with a
log. Its items are not in this repository. The four drill sheets and lab 3.4 show the format;
write the items in the same shapes with other content, and keep them with the Academy's exam
files.

## The follow-up task: an outline, not a solution

- The new check belongs in `parse_row`, after the date has been parsed and before the meter
  is looked up, so that an unparseable date is still BAD_DATE and a future date of an unknown
  meter is FUTURE_DATE. Either order is defensible if the participant states it and tests it.
- `load_readings` takes the month's last day as an optional argument with `None` as default;
  `None` means the rule is off. The command line turns `--month 2026-09` into that day.
- The four tests: 2026-09-30 accepted; 2026-10-01 rejected with FUTURE_DATE; no month given
  and 2026-10-01 accepted; one row that breaks this rule and one other, to pin the order.
- The September report must not change by a byte: no row of that file is dated after the 30th.

## The capstone

The brief, the rules and the output contract are in `labs/capstone/README.md`. On the public
files a correct tool reports 505 rows, 447 accepted and 58 rejected: MISSING_VALUE 10,
DUPLICATE 10, NOT_A_NUMBER 8, BAD_DATE 7, OUT_OF_RANGE 7, UNKNOWN_CREW 6, CLOSED_BEFORE_OPENED 5,
UNKNOWN_KIND 5; 87 open orders are overdue on 2026-10-31. There is no reference tool in this
repository, on purpose. For the hidden tests, write a dataset with a seed of your own and
grade against it:

    uv run labs/_tools/make_capstone.py --seed <yours> --to <a folder outside the repository> --expected
    uv run labs/_tools/grade_capstone.py <the participant's repository> <that folder>
