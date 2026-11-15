"""The contract of the four functions. Do not change this file: change monthly_bill.py."""

from monthly_bill import bill, clean, format_bill, load_rows


def test_load_rows_returns_one_dictionary_per_data_row():
    rows = load_rows("data/sample_meter.csv")
    assert len(rows) == 30
    assert rows[0]["meter_id"] == "M-0042"
    assert set(rows[0]) == {"meter_id", "date", "consumption_m3"}


def test_clean_keeps_numbers_and_counts_the_rest():
    rows = [{"consumption_m3": "0.5"}, {"consumption_m3": ""}, {"consumption_m3": " 1.25 "}, {"consumption_m3": "N/A"}]
    assert clean(rows) == ([0.5, 1.25], 2)


def test_clean_of_nothing():
    assert clean([]) == ([], 0)


def test_bill_below_at_and_above_the_first_block():
    assert bill(0.0) == 5.0
    assert bill(15.0) == 35.0
    assert bill(20.0) == 57.5


def test_format_bill_is_four_lines_of_text():
    text = format_bill("M-0001", [1.0, 2.5], 1, 12.0)
    assert text.splitlines() == [
        "Meter M-0001",
        "Days billed: 2 skipped: 1",
        "Consumption: 3.5 m3",
        "Amount due: 12.0 SAR",
    ]
