# total_valid(values) returns the sum of the values that are zero or more.
# The distractor was "total = value": it replaces the sum with the last value.

def total_valid(values):
    total = 0.0
    for value in values:
        if value >= 0:
            total += value
    return total
