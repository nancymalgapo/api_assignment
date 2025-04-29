import pandas as pd

from datetime import datetime, timedelta, date
from utils.helper import to_string_date, validate_date, clean_data


def test_to_string_date():
    assert to_string_date(date(2023, 1, 1)) == '2023-01-01'
    assert to_string_date(date(2025, 4, 22)) == '2025-04-22'
    assert to_string_date(date(2000, 1, 1)) == '2000-01-01'
    assert to_string_date(date(1999, 12, 31)) == '1999-12-31'


def test_validate_date():
    # Test with today's date
    today_date = datetime.now().date()  # Today's date
    assert validate_date(today_date) == (True, "Success")

    # Test with an invalid date input (ex: a string)
    invalid_date = "2023-01-01"
    assert validate_date(invalid_date) == (False, "Invalid date input")

    # Test with a future date
    future_date = (datetime.now() + timedelta(days=1)).date()  # Tomorrow's date
    assert validate_date(future_date) == (False, "Date cannot be in the future")


def test_clean_data():
    # Sample data has Unnamed columns which are expected to be dropped """
    data = {
        "Unnamed: 0": [1, 2, 3],
        "Value Column": [None, 4.32, 62.5],
        "Unnamed: 1": [None, None, None]
    }
    df = pd.DataFrame(data)
    cleaned_df = clean_data(df)

    expected_data = {
        "Value Column": ["", 4.32, 62.5]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(cleaned_df, expected_df)
