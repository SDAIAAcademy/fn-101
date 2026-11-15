"""Do not change this file: change warmup.py."""

from warmup import total_valid


def test_adds_the_values_that_are_zero_or_more():
    assert total_valid([1.5, -2.0, 0.0, 2.5]) == 4.0


def test_nothing_gives_zero():
    assert total_valid([]) == 0.0
