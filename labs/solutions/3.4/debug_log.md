# Debugging log

The reference log. The numbers are from the reference run.

## Defect A

### Reproduce
`uv run python two_runs.py` prints "run 1: 17561 accepted, 129 rejected" and then "run 2: 0 accepted, 17690 rejected". The same file, two different answers.

### Shrink
The two good rows of `data/tiny.csv`, loaded twice in one process: the first call accepts 2, the second accepts 0 and rejects both as DUPLICATE. One call alone never shows it.

### Hypothesis
I think the set of seen (meter, day) pairs survives from the first call to the second, because `seen` is a default argument, `set()`, in the signature of `load_readings` in `miqyas/readings.py`, and a default is created once.

### Test
Printed `len(seen)` on the first line of the function: 0 on the first call, 2 on the second, although the caller passed nothing. Passing `seen=set()` by hand makes the second call accept 2.

### Fix
`seen: set[tuple[str, date]] = set()` became `seen: set[tuple[str, date]] | None = None`, with `if seen is None: seen = set()` as the first lines of the body.

### Regression
`test_defect_a_a_second_call_starts_with_nothing_seen`: fails with "the second call rejected ['DUPLICATE', 'DUPLICATE']" before the fix, passes after.

## Defect B

### Reproduce
The report of September lists M-0012 on 2026-09-26 with a median of 0.653. Sorted by hand, the two middle readings of that meter are 0.693 and 0.699: the median is 0.696. Nothing crashes and the count of anomalies is still 18; only the number is wrong.

### Shrink
`median([3.0, 1.0, 2.0])` returns 1.0. The middle value of 1, 2, 3 is 2.0. No file is needed.

### Hypothesis
I think `median` in `miqyas/anomalies.py` takes the middle position of the list as it arrives, without sorting it, because the name `ordered` is bound to `values` itself.

### Test
`median([1.0, 2.0, 3.0])` returns 2.0 and `median([3.0, 1.0, 2.0])` returns 1.0: the answer depends on the order, which a median must not.

### Fix
`ordered = values` became `ordered = sorted(values)`.

### Regression
`test_defect_b_median_does_not_depend_on_the_order`: fails before the fix, passes after. The report now gives 0.696 for M-0012.
