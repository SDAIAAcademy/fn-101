---
course: "Python for Data and AI Work"
code: "FN-101"
version: "2027.1.0"
lab: "4.3"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fn-101/labs/D4_3_write_five_tests.html"
---

# Lab 4.3 · Pin the anomaly rule down with tests

Write five tests for the anomaly rule, including empty and boundary inputs.

Day 4 · Session 3: Tests as a safety net

### Goal

The whole report rests on one rule of three lines. Write five tests that pin that rule down, then let the check swap the rule for four wrong versions of it and see how many your tests notice.

## What you need

- The folder `4.3` of the workspace: the package `miqyas/` with `is_anomaly` in `anomalies.py`, and `test_anomalies.py` with one test written
- AI policy: tutor. Ask what a boundary case is, if you need to; choosing the examples is the lab

### Read the rule's docstring and the one supplied test 3 min

```python
# file: miqyas/anomalies.py
def is_anomaly(value: float, history: list[float], factor: float = 3.0) -> bool:
    """True when value is more than factor times the median of history.

    With no history there is nothing to compare with: the answer is False.
    Exactly factor times the median is not an anomaly.
    """
```

```bash
# file: terminal
cd ../4.3
uv run pytest test_anomalies.py
```

The docstring makes three promises and the signature has three arguments. On paper, list what a wrong version of this function could get wrong. That list is your test plan.

### Write a test for the boundary and one for no history 8 min

Use a history whose median you can see without computing, such as three times 1.0. Write one test for a value exactly at factor times the median, and its neighbour just above. Then one test for an empty history. Each test has three parts: arrange the input, act with one call, assert the result.

```python
# file: test_anomalies.py
def test_exactly_three_times_the_median_is_not_an_anomaly():
    history = [1.0, 1.0, 1.0]              # arrange
    result = is_anomaly(3.0, history)      # act
    assert result is False                 # assert
```

Name each test after the sentence it proves. When it fails next year, the name is the first thing a colleague reads.

### Write three more: the median and the factor 8 min

Three questions, one test each. A clear anomaly: is it found? The median: can you build a history in which the median and the mean disagree, and a value that is an anomaly by one and not by the other? The factor: does passing `factor=2.0` change an answer?

Run the tests after each one. A new test that passes at once on the real rule is normal here; whether it is worth anything is what the next step measures.

### Run the check against four wrong versions 6 min

```bash
# file: terminal
uv run ../lab.py check 4.3
```

The check copies your tests beside four versions of the rule, each with one planted change, and runs them. For each version it says whether a test failed. A version that all your tests pass is a mistake your tests would let through: read its description, add the example that tells the two rules apart, and run the check again.

### ✱ Stretch

Rewrite your examples as one table with `pytest.mark.parametrize`: one row per case with the value, the history, the factor and the expected answer. Does the check still pass? What did you lose in the names?

## Check yourself

1. All your tests pass. What have you proved, and what have you not?
2. Which of the four wrong versions would a test with the history 1.0, 1.0, 1.0 alone never catch, and why?
3. Why is a history of 30 real readings from the month file a poor test input?
