"""What the parser promises. Do not change this file: change parser.py."""

from parser import highest, parse_line, total

GOOD = ["M-0042;2026-09-01;0.7421", "M-0042;2026-09-02;0.5", "M-0042;2026-09-03;1.25"]
BAD = ["M-0042;2026-09-04", "M-0042;2026-09-05;", ""]


def test_a_good_line_becomes_three_values():
    assert parse_line("M-0042;2026-09-01;0.7421\n") == ("M-0042", "2026-09-01", 0.742)


def test_a_bad_line_becomes_none():
    for line in BAD:
        assert parse_line(line) is None


def test_total_skips_bad_lines():
    assert round(total(GOOD + BAD), 3) == 2.492


def test_total_of_nothing_is_zero():
    assert total([]) == 0.0


def test_highest_skips_bad_lines():
    assert highest(BAD + GOOD) == 1.25


def test_highest_of_nothing_is_none():
    assert highest([]) is None
    assert highest(BAD) is None
