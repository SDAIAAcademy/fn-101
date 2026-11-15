"""Do not change this file: change validate.py."""

from validate import validate_reading

KNOWN = {"M-0001", "M-0002"}


def row(value, meter="M-0001"):
    return {"meter_id": meter, "date": "2026-09-01", "consumption_m3": value}


def test_a_good_row():
    assert validate_reading(row("0.742"), KNOWN) == ""
    assert validate_reading(row(" 12 "), KNOWN) == ""


def test_the_edges_of_the_range_are_good():
    assert validate_reading(row("0"), KNOWN) == ""
    assert validate_reading(row("200"), KNOWN) == ""


def test_missing_value():
    assert validate_reading(row(""), KNOWN) == "MISSING_VALUE"
    assert validate_reading(row("   "), KNOWN) == "MISSING_VALUE"


def test_not_a_number():
    assert validate_reading(row("N/A"), KNOWN) == "NOT_A_NUMBER"
    assert validate_reading(row("0,742"), KNOWN) == "NOT_A_NUMBER"


def test_out_of_range():
    assert validate_reading(row("-0.5"), KNOWN) == "OUT_OF_RANGE"
    assert validate_reading(row("200.001"), KNOWN) == "OUT_OF_RANGE"


def test_unknown_meter_is_checked_last():
    assert validate_reading(row("0.5", "M-9001"), KNOWN) == "UNKNOWN_METER"
    assert validate_reading(row("", "M-9001"), KNOWN) == "MISSING_VALUE"
