# Drill 4: order the lines, then find the bug

Ten minutes, on paper, without a computer and without an assistant.

**1.** These lines are one function, scrambled, with one line that does not belong. `by_meter(readings)` takes pairs of (meter id, cubic metres) and returns a dictionary from each meter id to the list of its values. Write the lines in order, with their indentation, and cross out the distractor.

```python
groups[meter_id].append(m3)
groups = {}
return groups
groups[meter_id] = m3
if meter_id not in groups:
def by_meter(readings):
groups[meter_id] = []
for meter_id, m3 in readings:
```

**2.** The function below should print 3.0. Say what it prints, which line is wrong, and how you would repair it.

```python
def average(values):
    """The mean of the values that are numbers; rows that hold None are skipped."""
    total = 0.0
    for value in values:
        if value is None:
            continue
        total += value
    return total / len(values)


print(average([2.0, None, 4.0]))
```
