---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/slides/day2.html"
---

# Python for Data and AI Work

## Day 2: Collections for data work

Dictionaries, sets, comprehensions, generators and data classes on a month of readings and a ticket queue

#### [day2#title] Collections for data work

*SDAIA Academy · Python for Data and AI Work*

Day 2: Dictionaries, sets, comprehensions, generators and data classes on a month of readings and a ticket queue

Data & AI Foundations Track · 4 teaching days + capstone day · 4 sessions · 4 labs · FN-101

#### [day2#drill-2] Lists and dictionaries that share · 10 minutes

*Drill 2 · AI off*

Five snippets on paper: `labs/drills/day2.md`. No computer, no assistant. Write what each prints.

#### [day2#review-day1] One list or two?

*Review of Day 1*

**Question:** A function `clean(rows)` runs `rows.sort()` and returns `rows[:10]`. A caller writes `top = clean(month)`. Afterwards, what is true of `month`?

- A. It is unchanged: the function worked on its own copy
- B. It is sorted, and still has all its rows
- C. It is sorted and cut to ten rows
- D. It is the same object as `top`

#### [day2#agenda] Collections for data work

*Today*

- **Session 1 · Dictionaries for counting and grouping**: A dictionary as an index: counting, grouping, and why one lookup replaces a loop
- **Session 2 · Sets and membership**: Sets answer membership and difference questions directly: what is missing, what is unknown, what repeats
- **Session 3 · Comprehensions and generators**: Comprehensions build a collection in one expression; generators hand over one item at a time and keep memory flat
- **Session 4 · Records as data classes**: A data class gives a record named, typed fields; sorting with a key puts a queue in working order

### Session 1: Dictionaries for counting and grouping

#### [day2#s1] Dictionaries for counting and grouping

*Session 1*

- Count and group records with a dictionary in one pass
- Build an index from a key to a record and use it in place of a search
- Explain why a loop inside a loop is slow on 100,000 rows, and measure it

#### [day2#dict-is-an-index] A dictionary answers "what belongs to this key?" in one step

*Dictionaries*

```python
# file: index.py
district_of = {
    "M-0001": "Al-Rabwa",
    "M-0002": "Al-Yasmin",
}
print(district_of["M-0002"])
print("M-9001" in district_of)
```

- Each **key** appears once and leads to one **value**
- Looking up a key does not search: it goes straight there
- `in` asks whether a key exists, without raising an error
- Keys keep the order in which they were added

> **Think "index", like the back of a book.** You do not read the book to find a word; you look the word up.

#### [day2#counting-pattern] Counting: one pass, one dictionary, get with a default

*Pattern 1*

```python
# file: count.py
counts: dict[str, int] = {}
for reading in readings:
    meter_id = reading["meter_id"]
    counts[meter_id] = counts.get(meter_id, 0) + 1
```

- `counts.get(key, 0)`: the count so far, or 0 for a key not seen yet
- `counts[key] += 1` alone raises `KeyError` on the first reading of a meter
- `collections.Counter(…)` is this loop, ready made

- **On the month.** 588 meters have readings in the clean file; M-0001 has 30, one per day of September (lab 2.1).

#### [day2#grouping-pattern] Grouping: the value is a list, and each record joins the list of its key

*Pattern 2*

```python
# file: group.py
by_meter: dict[str, list[float]] = {}
for reading in readings:
    value = float(reading["consumption_m3"])
    meter_id = reading["meter_id"]
    by_meter.setdefault(meter_id, []).append(value)
```

- `setdefault(key, [])` returns the list of the key, creating an empty one the first time
- After the loop, `by_meter["M-0042"]` is that meter's whole month
- This is how Miqyas finds each meter's median before it looks for anomalies

> **What goes wrong.** `dict.fromkeys(ids, [])` gives every key the **same** list. Yesterday's aliasing, in a dictionary.

#### [day2#index-then-lookup] To combine two files, index one of them and look up from the other

*Pattern 3*

1. **1 · Index** meters.csv becomes meter id → district, once
2. **2 · Walk** each reading, one after another
3. **3 · Look up** the district of its meter, in one step

```python
# file: count.py
district_of = {m["meter_id"]: m["district"] for m in meters}
for reading in readings:
    district = district_of[reading["meter_id"]]
```

#### [day2#nested-loop-cost] The same counts, a hundred times slower: a loop inside a loop

*From the lab's run*

- **2.3 s** nested loop: for each of 100,000 readings, search 600 meters
- **0.024 s** dictionary: index 600 meters once, then one lookup per reading
- **300** comparisons per reading, on average, in the nested version

> **It gets worse with size.** Ten times the meters makes the nested version ten times slower again. The dictionary version hardly notices.

#### [day2#why-lookup-is-fast] The key itself says where its value is stored

*Why one step*

- Python turns the key into a number, its **hash**, and uses it as an address
- So finding a key costs about the same in 600 entries as in 600,000
- The price: a key must never change. Text, numbers and tuples can be keys; lists and dictionaries cannot

```python
# file: at a prompt
>>> {["M-0001", "2026-09-01"]: 0.7}
TypeError: unhashable type: 'list'
>>> {("M-0001", "2026-09-01"): 0.7}
{('M-0001', '2026-09-01'): 0.7}
```

#### [day2#missing-keys] Three ways to ask for a key, and they fail differently on purpose

*When the key is not there*

| You write | Key missing | Use it when |
| --- | --- | --- |
| `district_of[meter_id]` | raises `KeyError` | a missing key is a fault you want to hear about |
| `district_of.get(meter_id)` | gives `None` | missing is normal and you handle `None` next |
| `meter_id in district_of` | gives `False` | you only need to know |

> **At Manahil.** Twenty rows of the month carry a meter id that is not in the registry. A loud `KeyError` finds them; a quiet `get` with a default district would hide them in a total.

#### [day2#check-index-outside-loop] Why is this version still slow?

*Checkpoint*

**Question:** A colleague replaces the nested loop. Inside `for reading in readings:` the first line is now `district_of = {m["meter_id"]: m["district"] for m in meters}`, then a lookup. The counts are right; 100,000 rows still take seconds.

- A. The index is rebuilt for every reading, which walks all the meters each time
- B. Dictionary lookups are slow when the dictionary has 600 keys
- C. Comprehensions are slower than loops
- D. 100,000 rows are too many for a Python loop

#### [day2#lab-2-1] Count readings per meter and district

Lab 2.1 · 25 min

Count readings per meter and district, then time a nested-loop version on 100,000 rows.

[D2_1_count_readings_per.html](https://sdaiaacademy.github.io/fn-101/labs/D2_1_count_readings_per.html)

- [ ] Count the readings of each meter in one pass (7 min)
- [ ] Build an index of meters; count per district (8 min)
- [ ] Time both versions on 100,000 rows (6 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Group the readings by district into lists of values and print each district's highest reading

### Session 2: Sets and membership

#### [day2#s2] Sets and membership

*Session 2*

- Answer a membership question with a set in place of a search through a list
- Compare two collections with difference and intersection
- Use a tuple as a key to find repeated records

#### [day2#set-is-membership] A set holds each value once and answers "is it in there?" in one step

*Sets*

```python
# file: known.py
known = {m["meter_id"] for m in meters}
print(len(known))             # 600
print("M-0042" in known)      # True
print("M-9001" in known)      # False
```

- A set is a dictionary with keys and no values
- `x in a_list` walks the list; `x in a_set` goes straight to the answer
- No order, no positions, no repeats: only membership

> **You have used one already.** Yesterday's `validate_reading(row, known)` took the registry as a set, for exactly this question.

#### [day2#set-algebra] Three operators answer what is missing, what is extra and what is shared

*Comparing two collections*

| Expression | Reads as | At Manahil |
| --- | --- | --- |
| `registered` | ids in the registry | 600 |
| `reporting` | ids that appear in the month's readings | 593 |
| `registered - reporting` | registered and silent | 12 |
| `reporting - registered` | reporting and unknown | 5 |
| `registered & reporting` | in both | 588 |
| `registered \| reporting` | in either | 605 |

#### [day2#two-findings-two-owners] The same operator, two different problems, two different owners

*What the two differences mean*

- **12 meters sent nothing.** Registered, and not one row in September. A dead meter, an empty house, a reader that never synchronised. A question for **the field team**.
- **5 ids are unknown.** M-9001 to M-9005, four rows each. A registry that is behind, or a mistyped id. A problem in **the data**, and those 20 rows cannot be billed to anyone.

> **A check that finds something must say who acts on it.** Miqyas rejects the 20 rows with the reason UNKNOWN_METER; the silent meters go into a list for the field team.

#### [day2#dedup-and-order] A set drops repeats and forgets order: sort before you show it

*What a set gives up*

```python
# file: at a prompt
>>> ids = ["M-0002", "M-0001", "M-0002"]
>>> set(ids)
{'M-0002', 'M-0001'}
>>> sorted(set(ids))
['M-0001', 'M-0002']
```

- `set(a_list)` is the shortest way to drop repeats
- The order you see printed is not promised, and can differ between runs
- `sorted(…)` turns any collection into a list in a fixed order

> **A report must be the same on two runs.** Anything that leaves your function for a file or a screen goes through `sorted` first.

#### [day2#seen-set-pattern] Finding repeats: remember what you have seen, as a set of tuples

*Pattern*

```python
# file: coverage_report.py
seen: set[tuple[str, str]] = set()
repeated: set[tuple[str, str]] = set()
for reading in readings:
    key = (reading["meter_id"], reading["date"])
    if key in seen:
        repeated.add(key)
    seen.add(key)
```

- The identity of a reading is the **pair**: this meter, this date
- A tuple cannot change, so it can be a member of a set
- `set()` makes an empty set; `{}` is an empty dictionary

- **On the month.** 30 pairs appear more than once. Miqyas keeps the first row of each and rejects the repeat as DUPLICATE.

#### [day2#choosing-a-collection] Choose the collection by the question you will ask of it

*Four collections*

| You will ask | Use | Example |
| --- | --- | --- |
| what is at position 3? what comes next? | `list` | the rows of a file, in file order |
| what belongs to this key? | `dict` | meter id → district; district → count |
| is it in there? what differs? | `set` | the known meter ids |
| a few values that travel together and never change | `tuple` | (meter id, date) |

> **Changing your mind is cheap.** `set(a_list)`, `sorted(a_set)`, `list(a_dict)`, `dict(pairs)` convert in one call.

#### [day2#check-set-difference] Which expression finds them?

*Checkpoint*

**Question:** Badr has the set `ticketed` (meter ids named in open tickets) and Salma the set `flagged` (meter ids with an anomaly). They want the meters that have an anomaly and **no** open ticket, to call those customers first.

- A. ticketed & flagged
- B. ticketed - flagged
- C. ticketed | flagged
- D. flagged - ticketed

#### [day2#lab-2-2] Find silent meters and unknown ids

Lab 2.2 · 25 min

Find meters with no reading and readings with no known meter.

[D2_2_find_meters_no.html](https://sdaiaacademy.github.io/fn-101/labs/D2_2_find_meters_no.html)

- [ ] Build the two sets of meter ids (5 min)
- [ ] Find the meters with no reading (5 min)
- [ ] Find the readings with no known meter (5 min)
- [ ] Find the repeated meter and date pairs (6 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: List the meters that have fewer than 30 different dates, with the number of dates each has

### Session 3: Comprehensions and generators

#### [day2#s3] Comprehensions and generators

*Session 3*

- Write list, dictionary and set comprehensions with a filter
- Write a generator function that yields records while a file is read
- Compare the peak memory of a list and of a stream, and say when each fits

#### [day2#comprehension-forms] A comprehension builds a collection in one expression: what, from where, which

*Comprehensions*

```python
# file: forms.py
values = [float(r["consumption_m3"]) for r in rows]                 # a list
high = [v for v in values if v > 5.0]                               # with a filter
known = {m["meter_id"] for m in meters}                             # a set
district_of = {m["meter_id"]: m["district"] for m in meters}        # a dictionary
```

- **What.** The expression at the front: one item of the result.
- **From where.** `for … in …`: the same line as in a loop.
- **Which.** An optional `if` at the end keeps only some.

#### [day2#when-a-loop-reads-better] One expression and one condition fit a comprehension; anything more wants a loop

*Judgement*

- **Comprehension.** Transform each item, or keep some. The reader sees the whole idea on one line.
- **Loop.** Counting and grouping, a `try` around each item, two results at once, an early exit, or a line that no longer fits on the screen.

```python
# file: too much
ok = [float(r["consumption_m3"]) for r in rows if r["consumption_m3"].strip() != ""
      and r["meter_id"] in known and 0 <= float(r["consumption_m3"]) <= 200]
```

> **What goes wrong.** The line above converts twice, crashes on `N/A`, and cannot say why a row was left out.

#### [day2#generator-function] A function with yield hands over one value, then waits to be asked again

*Generators*

```python
# file: stream.py
def read_values(path):
    with open(path, encoding="utf-8",
              newline="") as file:
        for row in csv.DictReader(file):
            yield float(row["consumption_m3"])
```

- `return` ends a function; `yield` **pauses** it, with all its names kept
- The next request resumes it on the line after the `yield`
- At any moment, one row exists. The file stays open until the loop is done

#### [day2#lazy-nothing-runs] Calling a generator function runs nothing: the work happens when values are asked for

*Laziness*

- call: `values = read_values("data/readings_large.csv")` no file is opened yet
- next(values): opens the file, reads one row, gives `0.606` and pauses
- next(values): reads one more row, gives `0.544` and pauses
- sum(values): asks again and again until the file ends: the total of everything **left**

> **`for` and `sum` ask for you.** You rarely write `next`; every loop over a generator is this conversation.

#### [day2#memory-list-vs-stream] The same total of 100,000 rows, with two hundred times less memory

*From the lab's run*

| Item | Value |
| --- | --- |
| List of all rows | 35,900 KiB |
| Stream, one row at a time | 160 KiB |

- Both give **137,769.165** cubic metres
- A file ten times as long: the list needs ten times the memory, the stream the same 160 KiB
- A year of every meter's hourly readings does not fit in a list on a laptop. It does fit in a stream

#### [day2#one-pass-only] A generator can be walked once. Then it is empty.

*The price*

```python
# file: at a prompt
>>> values = read_values(path)
>>> sum(values)
137769.165
>>> sum(values)
0
>>> len(values)
TypeError: object of type 'generator' has no len()
```

- No length, no positions, no second pass
- Need two results? Compute both in **one** loop, or call the function again for a fresh generator
- Need to sort, or to find a median? You need all the values: use a list

> **The silent zero.** A second pass does not raise an error. It quietly gives the result for no data.

#### [day2#generator-expression] Round brackets make a comprehension lazy

*The short form*

```python
# file: two ways
total = sum([float(r["consumption_m3"])
             for r in rows])

total = sum(float(r["consumption_m3"])
            for r in rows)
```

- First: build a list of 100,000 numbers, add them, throw the list away
- Second: hand each number to `sum` as it is made
- Works with `sum`, `max`, `min`, `any`, `all`, `sorted`, `set`

#### [day2#check-generator-twice] What does the report show?

*Checkpoint*

**Question:** A script does `values = read_values(path)`, then `highest = max(values)`, then `total = sum(values)`, and prints both. The file holds 100,000 good readings.

- A. The right highest value and the right total
- B. The right highest value, then an error on the second line
- C. The right highest value and a total of 0
- D. A highest value of 0 and the right total

#### [day2#lab-2-3] Stream a large readings file

Lab 2.3 · 25 min

Stream a large readings file with a generator and compare peak memory with a list.

[D2_3_stream_large_readings.html](https://sdaiaacademy.github.io/fn-101/labs/D2_3_stream_large_readings.html)

- [ ] Run the list version and read how it works (4 min)
- [ ] Write the generator that yields one value per row (8 min)
- [ ] Add up the stream; compare the two totals (4 min)
- [ ] Measure both peaks of memory (5 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Use the generator twice in a row and explain what the second pass returns

### Session 4: Records as data classes

#### [day2#s4] Records as data classes

*Session 4*

- Model a record as a frozen data class with typed fields and a method
- Sort records by several fields with a key function that returns a tuple
- Leave out of a record the personal data the task does not need

#### [day2#dict-records-fail-late] A dictionary as a record accepts any mistake until the line that uses it

*Records*

```python
# file: queue.py
ticket = json.loads(line)
ticket["priorty"] = "urgent"
if ticket["opened"] < "2026-09-01":
    ...
```

- Line 2 misspells the field and **adds a new key**. No error, ever
- Line 3 compares dates as text. It works only while every file writes year-month-day
- Nothing says which fields a ticket has, or what type each is
- The checker sees `dict[str, str]` and can help with none of it

#### [day2#dataclass-basics] A data class is a record with named, typed fields, written in six lines

*Data classes*

```python
# file: tickets.py
@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    opened: date
    district: str
    priority: str
    status: str
    text: str
```

- The decorator writes the constructor, a readable printout and `==` for you
- `Ticket(ticket_id="T-20001", opened=…)` builds one; `t.priority` reads a field
- A misspelt field is an `AttributeError` at run time and an error from the checker before

#### [day2#frozen-records] frozen=True makes a record that nobody can change behind your back

*Frozen*

```python
# file: at a prompt
>>> t.priority = "low"
dataclasses.FrozenInstanceError:
    cannot assign to field 'priority'
>>> urgent = replace(t, priority="urgent")
```

- Yesterday: a shared mutable object changes for every name that holds it
- A frozen record can be shared freely: there is nothing to mutate
- A "change" makes a new record with `dataclasses.replace`, like `upper()` on a string
- Frozen records can be keys of a dictionary and members of a set

#### [day2#methods-on-records] A method is a function that lives with the data it needs

*Behaviour that belongs to the record*

```python
# file: tickets.py
    def age_days(self, today: date) -> int:
        """Whole days from the day the
        ticket was opened to today."""
        return (today - self.opened).days
```

- `self` is the record the method was called on: `t.age_days(today)`
- `today` comes in as a parameter. A method that asked the clock would give a different answer tomorrow, and could not be tested
- `opened` is a `date`, so subtraction gives days. As text it would give an error

- **On the queue.** The oldest open urgent ticket, T-20087, is 41 days old on the course's "today", 1 October 2026 (lab 2.4).

#### [day2#sort-with-key] sorted needs to know what to compare: give it a key function

*Sorting*

```python
# file: sorting.py
RANK = {"urgent": 0, "high": 1,
        "normal": 2, "low": 3}

by_text = sorted(tickets,
                 key=lambda t: t.priority)
by_rank = sorted(tickets,
                 key=lambda t: RANK[t.priority])
```

- The key function is called once per item; items are ordered by what it returns
- By text: high, low, normal, urgent. Alphabetical, and useless
- By rank: urgent first, because 0 is the smallest
- `lambda t: …` is a function small enough to write in place

#### [day2#tuple-keys-multi-sort] A key that returns a tuple sorts by the first item, then the second, then the third

*Sorting by several fields*

```python
# file: tickets.py
sorted(waiting, key=lambda t: (PRIORITY_RANK[t.priority], t.opened, t.ticket_id))
```

| Ticket | Rank | Opened | Age in days | District |
| --- | --- | --- | --- | --- |
| T-20087 | 0 urgent | 2026-08-21 | 41 | Al-Yasmin |
| T-20274 | 0 urgent | 2026-08-24 | 38 | Al-Naseem |
| T-20066 | 0 urgent | 2026-08-25 | 37 | Al-Khuzama |
| T-20196 | 0 urgent | 2026-08-26 | 36 | Al-Naseem |

> **The last item breaks ties.** Two urgent tickets of the same day would otherwise come out in file order; the ticket id makes the queue the same on every run.

#### [day2#carry-only-what-you-need] A record carries only the fields the task needs

*Responsible use*

- **In the file.** Ten fields per ticket, among them a phone number and an identity number: personal data.
- **In `Ticket`.** Six fields. The queue is ordered by priority and age; it needs to call nobody and identify nobody.

- What is never copied into the record cannot be printed, logged or written by mistake
- The free **text** of a ticket can hold a phone number too. Tomorrow's first lab masks it before anything is written

> **The data here is synthetic.** The habit is real: Abdulaziz, the data protection officer, reads your output files, not your intentions.

#### [day2#check-sort-key] Which key puts the queue in working order?

*Checkpoint*

**Question:** Customer care works the most urgent tickets first and, within a priority, the oldest first. `RANK` gives urgent 0 and low 3. Which call is right?

- A. sorted(waiting, key=lambda t: (t.priority, t.opened))
- B. sorted(waiting, key=lambda t: (RANK[t.priority], t.opened))
- C. sorted(waiting, key=lambda t: (RANK[t.priority], t.opened), reverse=True)
- D. sorted(waiting, key=lambda t: (t.opened, RANK[t.priority]))

#### [day2#lab-2-4] Model and sort the ticket queue

Lab 2.4 · 25 min

Model a ticket as a data class and sort tickets by priority and age.

[D2_4_model_ticket_as.html](https://sdaiaacademy.github.io/fn-101/labs/D2_4_model_ticket_as.html)

- [ ] Define the frozen data class and its age method (8 min)
- [ ] Build tickets from the lines of the file (6 min)
- [ ] Sort the open tickets by priority, then age (7 min)
- [ ] Run the type checker and the lab check (4 min)
- [ ] ✱ Stretch: Count the open tickets per district and priority with a dictionary whose keys are tuples

#### [day2#wrap-up] Three things to keep

*Day 2 · wrap-up*

- **Choose by the question.** A dictionary for "what belongs to this key", a set for "is it in there", a list for order. One lookup replaces a loop.
- **Stream what you use once.** A generator keeps memory flat and can be walked once. Sort, median and second passes need a list.
- **Records have names and types.** A frozen data class with only the fields the task needs; a tuple key puts them in order.

#### [day2#next] Day 3: Files, text and failure

*Next*

Tomorrow the files stop being clean: wrong encodings, broken lines, and two defects planted in the code. Drill 3 is a traceback to read on paper.
