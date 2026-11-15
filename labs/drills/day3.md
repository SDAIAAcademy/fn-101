# Drill 3: read a traceback

Ten minutes, on paper, without a computer and without an assistant. The program below was run and stopped with the traceback under it. Answer the five questions.

```python
import csv
import io

FILE = """meter_id,date,consumption_m3
M-0042,2026-09-01,0.742
M-0042,2026-09-02,N/A
"""


def to_number(text):
    return float(text)


def total(rows):
    result = 0.0
    for row in rows:
        result += to_number(row["consumption_m3"])
    return result


rows = list(csv.DictReader(io.StringIO(FILE)))
print(total(rows))
```


```text
Traceback (most recent call last):
  File "drill.py", line 22, in <module>
    print(total(rows))
          ~~~~~^^^^^^
  File "drill.py", line 17, in total
    result += to_number(row["consumption_m3"])
              ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "drill.py", line 11, in to_number
    return float(text)
ValueError: could not convert string to float: 'N/A'
```


1. Which exception was raised, and what does its message say?
2. In which function, and on which line of the file, did it happen?
3. Who called that function, and who called the caller? Read the frames from the bottom up.
4. How many rows had been added to the result before the failure?
5. Name two different repairs, and say what each does with the bad row.
