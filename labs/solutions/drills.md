# Drills: answers

For the trainer. Every output below was produced by running the snippet.

## Drill 1: predict the output

**1.** `[1, 2] [1, 2, 3]`. Line 3 builds a new list and rebinds b. The list that a names is untouched.

**2.** `meter METER`. Strings cannot change: upper() returns a new string, and only t is rebound.

**3.** `[0] [99, 2, 3]`. Line 3 mutates the shared list; line 4 rebinds x only, so y keeps the mutated list.

**4.** `[5]`. Inside reset the parameter is rebound to a new list. The caller's list is never touched, and the returned list is thrown away.

**5.** `[]`. clear() mutates the one list that both data and values name.

## Drill 2: lists and dictionaries that share

**1.** `2`. One dictionary, two names.

**2.** `[{'m': 7}, {'m': 7}]`. The list holds the same dictionary twice: multiplying a list repeats references, it does not copy.

**3.** `{'a': 2, 'b': 1}`. get(word, 0) answers 0 for a key that is not there yet. Keys keep the order in which they were first added.

**4.** `[3, 2, 1] [1, 2, 3]`. sorted() returns a new list; sort() changes the list in place and returns None.

**5.** `(1, [2, 3])`. The tuple cannot be given other items, but the list inside it can still change.

## Drill 3: read a traceback

**1.** ValueError: could not convert string to float: 'N/A'.

**2.** In to_number, on the line `return float(text)`: the last frame of the traceback.

**3.** total called to_number (the `result += ...` line); the module's last line called total.

**4.** One: the first row (0.742) was added, the second holds N/A.

**5.** Catch ValueError inside the loop and count the row as skipped; or validate before converting and collect the row with a reason. Neither lets the row vanish without a trace.

## Drill 4: order the lines, then find the bug

**1.** The distractor is `groups[meter_id] = m3`: it replaces the list by a single number.

```python
def by_meter(readings):
    groups = {}
    for meter_id, m3 in readings:
        if meter_id not in groups:
            groups[meter_id] = []
        groups[meter_id].append(m3)
    return groups
```

**2.** It prints `2.0`: the sum of the two numbers divided by three, because `len(values)` counts the skipped row too. Count the values that were added and divide by that count; the repaired function prints `3.0`. A list that holds only None must then be handled: decide what the mean of nothing is before dividing.
