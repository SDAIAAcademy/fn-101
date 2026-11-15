---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/slides/day3.html"
---

# Python for Data and AI Work

## Day 3: Files, text and failure

Reading and writing CSV and JSON Lines, bytes and encodings, exceptions that give a reason, and a method for debugging

#### [day3#title] Files, text and failure

*SDAIA Academy · Python for Data and AI Work*

Day 3: Reading and writing CSV and JSON Lines, bytes and encodings, exceptions that give a reason, and a method for debugging

Data & AI Foundations Track · 4 teaching days + capstone day · 4 sessions · 4 labs · FN-101

#### [day3#drill-3] Read a traceback · 10 minutes

*Drill 3 · AI off*

One program, the traceback it ended with, five questions: `labs/drills/day3.md`. On paper, no computer, no assistant.

#### [day3#review-day2] Which collection answers the question?

*Review of Day 2*

**Question:** For each of 17,690 rows you must decide whether its meter id is one of the 600 registered ids. Which choice keeps the whole job to one pass with one step per row?

- A. A list of the registered ids, tested with `in`
- B. A sorted list of the registered ids, tested with `in`
- C. A set of the registered ids, tested with `in`
- D. A generator of the registered ids, tested with `in`

#### [day3#agenda] Files, text and failure

*Today*

- **Session 1 · CSV and JSON Lines**: Reading CSV and JSON Lines with the standard library, writing JSON that reruns the same, and keeping personal data out of every output
- **Session 2 · Text, bytes and encodings**: Text is bytes plus an encoding: UTF-8, the default that open uses, decoding errors, and why ignoring them is not a repair
- **Session 3 · Exceptions that explain**: Raising early with a specific exception, an exception of your own that carries a reason code, and a loop that accounts for every line
- **Session 4 · A debugging method**: Six steps that turn a symptom into a fix that stays fixed: reproduce, shrink, hypothesis, test, fix, regression

### Session 1: CSV and JSON Lines

#### [day3#s1] CSV and JSON Lines

*Session 1*

- Read a CSV file and a JSON Lines file with the encoding and newline handling named
- Write JSON output that is the same on every run and keeps Arabic readable
- Mask personal data before anything is written, printed or logged

#### [day3#open-with-names] Three things to say every time you open a text file

*Opening a file*

```python
# file: load.py
with open(path, encoding="utf-8",
          newline="") as file:
    rows = list(csv.DictReader(file))
```

- `with`: the file is closed when the block ends, also when an error happens inside it
- `encoding="utf-8"`: you decide how bytes become text, not the machine you happen to be on
- `newline=""`: for CSV, let the csv module handle line ends, so that a line break inside a quoted cell survives

> **What goes wrong.** Leave the encoding out and the same script reads Arabic on one laptop and crashes on the next. Session 2 shows it.

#### [day3#csv-everything-is-text] A CSV reader hands you text for every cell. Numbers and dates are your job.

*CSV*

```python
# file: at a prompt
>>> row = rows[0]
>>> row
{'meter_id': 'M-0001', 'date': '2026-09-01',
 'consumption_m3': '5.399'}
>>> row["consumption_m3"] * 2
'5.3995.399'
```

- `csv.DictReader` uses the header line as keys: one `dict[str, str]` per row
- CSV has no types. `'5.399'` is five characters until you call `float`
- Convert in one place, at the door, and reject there what will not convert

#### [day3#csv-is-not-split] A comma inside a cell is why line.split(",") is not a CSV reader

*Why a module, not split*

```text
# file: readings_2026_09.csv
meter_id,date,consumption_m3
M-0001,2026-09-01,5.399
M-0580,2026-09-01,"0,361"
```

|  | Third row gives |
| --- | --- |
| `line.split(",")` | four pieces: `"0` and `361"` apart |
| `csv.DictReader` | three cells; the value is `0,361` |

- A spreadsheet set to a comma as the decimal mark writes numbers this way, in quotes
- The month file has 7 such cells. The reader gets them whole; `float` then refuses them, and they are rejected as NOT_A_NUMBER with the text in the detail

#### [day3#json-lines] JSON Lines is one JSON value per line: a file you can read one record at a time

*JSON Lines*

```python
# file: load.py
with open(path, encoding="utf-8") as file:
    for line in file:
        ticket = json.loads(line)
```

- Each line stands alone: a broken line spoils one record, not the file
- Records can be appended, and streamed with a generator
- Unlike CSV, a value has a type: text, number, true or false, null, list, object

- **At Manahil.** Each of the 400 tickets is one line with ten fields. The free text is Arabic, English or both in one sentence.

#### [day3#write-reproducible] Write output that is the same bytes on every run, and that a person can read

*Writing*

```python
# file: summary.py
with open(path, "w", encoding="utf-8",
          newline="\n") as file:
    json.dump(summary, file,
              ensure_ascii=False, indent=2)
    file.write("\n")
```

- `ensure_ascii=False`: Arabic is written as Arabic, not as escapes such as `ا`
- `indent=2`: one field per line, so that two versions can be compared
- Keys in a fixed order: build the dictionary from `sorted` names
- No clock time inside the file: put that in the log

> **Same input, same bytes.** Then "did anything change?" is answered by comparing two files, and Day 4's tool can prove it reruns.

#### [day3#tickets-are-personal-data] A ticket is personal data in three places, and the third is easy to miss

*Responsible use*

- **The phone field.** Every ticket has one. Callbacks need to recognise it, not to show it: the last two digits are enough.
- **The identity field.** No report needs it. It is never copied out of the input.
- **The free text.** "Call me on 05…": 14 of the 400 texts hold a phone number the customer typed in.

> **Mask before anything is written, printed or logged.** A debug print of one ticket is a leak with a shorter name.

#### [day3#mask-before-write] A pattern that looks right finds 9 of the 14 phone numbers

*From the lab's run*

| Pattern | Found |
| --- | --- |
| `\+?[0-9]{9,}` | 9 of 14 |
| `\+?\d{9,}` | 14 of 14 |

- Five customers typed their number in Arabic-Indic digits: ٠٥٥…
- In Python, `\d` matches a digit of any script; `[0-9]` matches ten characters only
- You find this by counting what the mask caught, not by reading the pattern

> **Test a mask on the data it must protect.** Then have someone else search the output for what should not be there.

#### [day3#check-mask-where] Where does the masking go?

*Checkpoint*

**Question:** A script loads tickets, logs each ticket it processes "for debugging", builds a summary and writes it to a file. The phone numbers must not leave the program. Where is masking applied?

- A. In the function that writes the summary file
- B. Where each ticket line is first turned into a record
- C. In a second script that cleans the summary file afterwards
- D. Nowhere, if the file is only sent to colleagues

#### [day3#lab-3-1] Write a district summary with phones masked

Lab 3.1 · 25 min

Load readings and tickets and write a JSON summary per district, masking phone numbers before anything is written.

[D3_1_load_readings_tickets.html](https://sdaiaacademy.github.io/fn-101/labs/D3_1_load_readings_tickets.html)

- [ ] Load the two CSV files and the JSON Lines file (7 min)
- [ ] Mask the phone field and the phone numbers in text (8 min)
- [ ] Write the summary as JSON; read it as a reviewer (6 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Change the pattern to [0-9] and count the phone numbers that now slip through; say why

### Session 2: Text, bytes and encodings

#### [day3#s2] Text, bytes and encodings

*Session 2*

- Explain the difference between bytes and text, and what an encoding does
- Read a UnicodeDecodeError: the codec, the byte and the position
- Decode a file line by line and report the lines that fail instead of ignoring them

#### [day3#bytes-and-text] A file holds bytes. Text appears only when an encoding is applied.

*Bytes and text*

| The word عداد (meter) | Bytes |
| --- | --- |
| in UTF-8 | `d8 b9 d8 af d8 a7 d8 af` |
| in Windows-1256 | `da cf c7 cf` |

- **Text** (`str`) is a sequence of characters: 4 here
- **Bytes** are numbers from 0 to 255: 8 here, or 4
- An **encoding** is the table between the two. `encode` goes to bytes, `decode` comes back

> **The bytes do not say which table wrote them.** Someone has to tell you, or you have to find out.

#### [day3#utf8-in-one-slide] UTF-8 covers every script and is the encoding to write, always

*UTF-8*

- **One byte.** English letters, digits, punctuation: the same bytes as ASCII. `M-0042` is six bytes.
- **Two bytes.** Each Arabic letter. The letter ف is `d9 81`.
- **Not every byte order is valid.** A decoder can tell when bytes are **not** UTF-8. That is a feature: wrong input fails loudly.

- Older systems wrote one byte per Arabic letter (Windows-1256). Their files are still arriving
- Read what you are given, with the encoding it was written in. Write UTF-8

#### [day3#default-encoding-trap] open(path) without an encoding uses whatever the machine prefers

*The trap*

```python
# file: decode.py
with open(path) as file:        # which encoding?
    return [json.loads(line) for line in file]
```

- On many Windows laptops the default is a one-byte Western table (cp1252)
- On most servers and in notebooks in the cloud it is UTF-8
- So the same script works in one place and fails in the other, on the same file

> **This is changing.** PEP 686 makes UTF-8 the default from Python 3.15. Until every machine you meet runs it, and for every file that is not UTF-8, name the encoding.

#### [day3#read-a-decode-error] A decode error names the codec, the byte and the position. Use all three.

*Reading the error*

```text
# file: uv run python decode.py
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 131:
    character maps to <undefined>
```

- **The codec.** "charmap": a one-byte table was decoding. Nobody chose it; it was the default.
- **The byte.** `0x81` has no character in that table. In UTF-8 it is the second half of ف.
- **The position.** Byte 131 of what was being decoded: where to look in the file.

#### [day3#mojibake] The wrong one-byte table raises nothing and gives you the wrong text

*The quiet failure*

| The UTF-8 bytes of عداد, decoded as | Result | Error? |
| --- | --- | --- |
| UTF-8 | عداد | no |
| Windows-1256 | ط¹ط¯ط§ط¯ | no |
| cp1252, errors replaced | Ø¹Ø¯Ø§Ø¯ | no |

> **"It opened without an error" is not "it was decoded correctly".** Text like the second and third rows, in a report or a database, means a file was read with the wrong table somewhere upstream.

#### [day3#never-ignore] errors="ignore" makes the error go away by deleting the customer's words

*The tempting repair*

| Line 12 of the branch file, decoded as UTF-8 with | The text of the ticket becomes |
| --- | --- |
| `errors="strict"` (the default) | a `UnicodeDecodeError`: you are told |
| `errors="ignore"` | a few spaces, one stray letter and M-0365 |
| `errors="replace"` | rows of � marks and M-0365 |
| the encoding it was written in (Windows-1256) | الفاتورة مرتفعة جدا هذا الشهر، أرجو مراجعة قراءة العداد M-0365 |

> **Fail loudly, then report.** Decode strictly, catch the error per line, and list the lines that fail with the byte that stopped you. Then someone can decide.

#### [day3#line-by-line-report] Decode each line by itself, so that one bad line cannot hide the rest

*The method*

```python
# file: decode.py
data = Path(path).read_bytes()
for line_no, raw in enumerate(
        data.splitlines(), start=1):
    try:
        decoded.append(raw.decode(encoding))
    except UnicodeDecodeError as problem:
        failed.append(...)
```

**113 + 7** lines decoded and lines reported: all 120 accounted for

Lines 12, 22, 37, 55, 82, 84 and 94 fail, each at an Arabic letter written in Windows-1256.

#### [day3#check-decode-choice] The export fails on a few lines. What do you do?

*Checkpoint*

**Question:** A nightly file of 50,000 tickets is declared UTF-8. Tonight the load stops with a `UnicodeDecodeError` at one byte. Badr needs the queue in the morning.

- A. Add `errors="ignore"` so that the load finishes
- B. Switch the whole file to Windows-1256, which never raises
- C. Refuse the file until the sender fixes it
- D. Load the lines that decode; report the rest by line and byte

#### [day3#lab-3-2] Decode a ticket file that fails

Lab 3.2 · 25 min

Open a ticket file that fails to decode, read it with the declared encoding and list the lines that still fail.

[D3_2_open_ticket_file.html](https://sdaiaacademy.github.io/fn-101/labs/D3_2_open_ticket_file.html)

- [ ] Run the loader and read the error it raises (5 min)
- [ ] Open the file with its declared encoding (5 min)
- [ ] Decode line by line and collect each failure (9 min)
- [ ] Write the report; run the lab check (6 min)
- [ ] ✱ Stretch: Decode the failing lines as Windows-1256 and print the tickets they hold

### Session 3: Exceptions that explain

#### [day3#s3] Exceptions that explain

*Session 3*

- Raise and catch specific exceptions, around the one call that can fail
- Define an exception that carries a reason code and a detail
- Write a loader in which accepted plus rejected equals the lines of the input

#### [day3#three-ways-to-meet-bad-data] A program can meet a bad record in three ways. Only one is acceptable.

*Bad input*

- **Crash.** Line 37 is broken, so nobody gets the other 434. And tomorrow, line 52.
- **Pass silently.** Skip it, or fill in a default. The report looks complete and is wrong by an unknown amount.
- **Reject with a reason.** The run finishes, the good records are used, and each bad one is listed with where and why.

> **The rule of the house.** Accepted plus rejected equals the lines of the input. Always, and checked by the program itself.

#### [day3#exceptions-travel] An exception travels up the call stack until some caller catches it

*Exceptions*

1. **parse_value("N/A")** raises ValueError
2. **parse_row(row)** no handler: passes it on
3. **load_readings(path)** has try and except: handles it, goes on

- `raise` stops the function at once; nothing is returned
- Each caller in turn either handles it or is stopped too
- If nobody handles it, the program ends and prints the stack: the traceback
- So the place that **detects** a problem need not be the place that **decides** what to do

#### [day3#catch-specific] Catch the exception you expect, by name. A wide net catches your own mistakes too.

*Catching*

```python
# file: too wide
try:
    value = flaot(text)
except Exception:
    skipped += 1
```

```python
# file: specific
try:
    value = float(text)
except ValueError:
    skipped += 1
```

- Left: the misspelt `flaot` raises a `NameError` on every row. The net catches it, and the script reports that all 17,690 rows were "skipped"
- Right: only "this text is not a number" is handled. Anything else still stops the run and shows you where

> **A bare `except:` is the widest net of all.** The labs' checks refuse it.

#### [day3#own-exception-with-reason] An exception of your own can carry what the handler needs: a code and a detail

*Your own exception*

```python
# file: intake.py
class Rejected(Exception):
    def __init__(self, reason, detail):
        super().__init__(f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail

raise Rejected("BAD_PRIORITY",
               f"priority is {value!r}")
```

- A **reason code** for programs: it can be counted, grouped and tested
- A **detail** for people: the actual value, so that someone can repair the line
- The handler catches `Rejected` and nothing else: every other exception is a bug to see

#### [day3#raise-early-guards] Day 1's guard clauses, with raise in place of return

*Validation as guards*

```python
# file: intake.py
if ticket["priority"] not in PRIORITIES:
    raise Rejected("BAD_PRIORITY", ...)
try:
    date.fromisoformat(ticket["opened"])
except ValueError:
    raise Rejected("BAD_DATE", ...) from None
return ticket
```

- The function now returns **only** good tickets. A caller cannot forget to look at a reason
- Let the library judge: `fromisoformat` knows that September has 30 days
- Translate its `ValueError` into your own exception, with your own code
- The first guard that fires wins: one reason per line

#### [day3#try-around-one-record] The try wraps one call for one line, and the loop goes on

*The loop*

```python
# file: intake.py
for line_no, line in enumerate(file, start=1):
    try:
        accepted.append(parse_ticket(line))
    except Rejected as problem:
        rejected.append((line_no,
                         problem.reason,
                         problem.detail))
```

- Inside the loop: one bad line costs one line
- A `try` around the **whole loop** would end at the first rejection and lose every line after it
- The line number is counted here, where it is known, and stored with the reason

> **You wrote this shape an hour ago.** Decode each line, catch the decode error, collect the failure: the same loop with another exception.

#### [day3#account-for-every-line] 435 lines in: 400 accepted, 35 rejected, 0 unaccounted for

*From the lab's run*

| Reason | Lines |
| --- | --- |
| MISSING_FIELD | 8 |
| BAD_JSON | 6 |
| BAD_PRIORITY | 5 |
| BAD_DATE, BAD_METER_ID | 4 + 4 |
| EMPTY_LINE, EMPTY_TEXT | 3 + 3 |
| NOT_OBJECT | 2 |

```python
# file: intake.py
assert len(accepted) + len(rejected) == lines
```

- The program checks its own accounting on every run
- The table tells the sender what to fix first
- The log, `rejections.csv`, says which line and what was in it

#### [day3#check-except-scope] The log says 435 rejected and 0 accepted. Why?

*Checkpoint*

**Question:** A colleague's intake finishes without a crash. Every line is in the rejection log with the reason `UNKNOWN`. The loop reads: `try: accepted.append(parse_tiket(line))`, then `except Exception: rejected.append((line_no, "UNKNOWN", ""))`.

- A. Every line of the file is malformed
- B. A typo raises NameError on every line; the wide except logs it
- C. The try is inside the loop and should be around it
- D. The file was opened with the wrong encoding

#### [day3#lab-3-3] Reject malformed lines with a reason

Lab 3.3 · 25 min

Reject malformed lines with a reason code so every input line is accounted for.

[D3_3_reject_malformed_lines.html](https://sdaiaacademy.github.io/fn-101/labs/D3_3_reject_malformed_lines.html)

- [ ] Run the intake and read the first crash (4 min)
- [ ] Add the six checks, each raising a reason (10 min)
- [ ] Catch the rejection around one call per line (4 min)
- [ ] Write the rejection log; run the lab check (7 min)
- [ ] ✱ Stretch: Add a ninth reason, DUPLICATE_ID, for a ticket id that an earlier line already used

### Session 4: A debugging method

#### [day3#s4] A debugging method

*Session 4*

- Read a traceback from its last line upward
- Shrink a failing input to the smallest one that still fails
- Write a regression test that fails on the defect and passes on the fix

#### [day3#six-steps] Six steps turn "it gives wrong numbers" into a fix that stays fixed

*A method, not a talent*

- **1 · Reproduce.** One command that shows the wrong result, every time.
- **2 · Shrink.** The smallest input that still shows it.
- **3 · Hypothesis.** One sentence: "I think … because …".
- **4 · Test it.** An observation that would prove you wrong.
- **5 · Fix.** The smallest change, at the cause.
- **6 · Regression check.** A test that fails without the fix.

#### [day3#read-traceback-bottom-up] Read a traceback from its last line upward

*When it crashes*

```text
# file: the traceback of drill 3
Traceback (most recent call last):
  File "drill.py", line 22, in <module>
    print(total(rows))
  File "drill.py", line 17, in total
    result += to_number(row["consumption_m3"])
  File "drill.py", line 11, in to_number
    return float(text)
ValueError: could not convert string to float: 'N/A'
```

- **Last line.** **What** went wrong, and with which value.
- **The frame above it.** **Where**: file, line, function.
- **The frames further up.** **How we got there**: who called whom.

#### [day3#quiet-wrong-answers] The harder defects raise nothing: they give a wrong answer politely

*When it does not crash*

- **Report A.** The same file, read twice in one job. Run 1: 17,561 accepted. Run 2: 0 accepted.
- **Report B.** The report gives a median of 0.653 for meter M-0012. Sorted by hand, it is 0.696.

- No traceback to read. You start from a **difference**: what you got against what must be true
- So step 1 is to make that difference appear on demand, with one command
- And somebody has to know what "must be true" is: here, the operator and Salma

#### [day3#shrink-the-input] Shrink until the failing case fits in your head

*Step 2*

1. **17,690 rows** fails, and tells you nothing
2. **Half of them** still fails? Halve again
3. **2 rows, or 3 values** fails, and you can check it by hand

- Shrink the **data** (fewer rows, one meter), the **steps** (one function, not the whole tool) and the **calls** (does it need two?)
- Each cut either keeps the failure, so you continue, or loses it, and then you have learnt what matters
- The smallest failing case is the regression test, almost written

#### [day3#hypothesis-then-test] Say what you think is wrong before you touch the code, then try to prove yourself wrong

*Steps 3 and 4*

- **A hypothesis.** "I think the count is wrong because line 40 of report.py starts the total at 1." A file, a line, a reason.
- **A test of it.** "If so, a file of one row gives 2." Run it. One row gives 1: the hypothesis is dead, in thirty seconds, with no code changed.

```python
# file: looking inside
print("start:", len(seen))   # the quick look

breakpoint()                 # or stop here, then:
# p name    print a name
# n         next line
# s         step into a call
# c         continue      q   quit
```

#### [day3#regression-test] A regression test fails on the defect and passes on the fix. Then it stays.

*Step 6*

```python
# file: test_regression.py
def test_total_of_one_row():
    rows = [{"consumption_m3": "0.5"}]
    assert total(rows) == 0.5
```

- Write it from the shrunk case, **before** or right after the fix
- See it fail on the old code. A test you never saw fail may be testing nothing
- See it pass on the new code
- Keep it: it runs with every later change, for as long as the code lives

> **The lab's check does step 2 of that list for you.** It puts each defect back into a copy of the package and expects your test to fail there.

#### [day3#why-ai-off-here] The first attempt at a debugging lab is yours alone

*How we work*

- An assistant will often find a seeded defect in seconds. Then the lab has taught you to ask
- The skill is the six steps: you need them for the defect no assistant has seen
- The supervised check has one debugging task, in a locked editor

- **After the attempt.** Still stuck? Tomorrow's last lab uses the course tutor for hints, which you turn into your own explanation.

> **The evidence comes tomorrow.** Day 4 looks at what a controlled study found when people learnt with and without an assistant.

#### [day3#check-debug-next-step] What is the next step?

*Checkpoint*

**Question:** The district report shows Al-Rabwa with twice the readings it should have. You can make it happen every time with one command on the month file. You have not opened the code yet.

- A. Find the smallest input that still doubles: one district, a handful of rows
- B. Read the whole package from the top until something looks wrong
- C. Divide the count of that district by two in the report
- D. Write a regression test on the whole month file

#### [day3#lab-3-4] Find and fix two seeded defects

Lab 3.4 · 25 min

With AI off, find and fix two seeded defects and write a regression test for each.

[D3_4_ai_off_find.html](https://sdaiaacademy.github.io/fn-101/labs/D3_4_ai_off_find.html)

- [ ] Reproduce both reports and write what you see (5 min)
- [ ] Defect A: shrink, hypothesis, test, fix (8 min)
- [ ] Defect B: shrink, hypothesis, test, fix (7 min)
- [ ] Write a regression test for each; run the check (5 min)
- [ ] ✱ Stretch: Step through defect A with the debugger: stop on the first line of the function in each call and print what it starts with

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **Name the encoding.** Bytes become text through a table you choose. Decode strictly, report what fails, never ignore.
- **Every line is accounted for.** Reject with a code and a detail; catch only what you expect; accepted plus rejected equals the input.
- **Six steps.** Reproduce, shrink, hypothesis, test, fix, regression check. The test is what makes the fix last.

#### [day3#next] Day 4: From notebook to tool

*Next*

Tomorrow Salma's notebook becomes a command that anyone can rerun, with tests around its one rule. Lab 4.1 opens a notebook: have JupyterLab or an editor that opens notebooks ready.
