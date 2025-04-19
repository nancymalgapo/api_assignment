import pytest
import pandas as pd

from datetime import datetime, timedelta
from utils.helper import format_date, validate_currency, validate_date, clean_data

def test_format_date():
    date_str = "2023-01-01"
    expected_date = datetime(2023, 1, 1)
    assert format_date(date_str) == expected_date

    date_str = "01-01-2023"
    with pytest.raises(ValueError):
        format_date(date_str)


def test_validate_currency():
    # Test with a valid currency
    assert validate_currency("USD") == (True, "Success")

    # Test with EUR currency
    assert validate_currency("EUR") == (False, "Currency cannot be EUR")

    # Test with an invalid currency length
    assert validate_currency("$USD") == (False, "Currency code must be exactly 3 characters long")


def test_validate_date():
    # Test with today's date
    today_date_str = datetime.now().strftime('%Y-%m-%d')  # Today's date
    assert validate_date(today_date_str) == (True, "Success")

    # Test with a date not compliant to YYYY-MM-DD format
    date_str = "01/01/2023"
    assert validate_date(date_str) == (False, "Invalid date format")

    # Test with a future date
    future_date_str = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')  # Tomorrow's date
    assert validate_date(future_date_str) == (False, "Date cannot be in the future")

    # Test with an empty string
    date_str = ""
    assert validate_date(date_str) == (False, "Invalid date format")


def test_clean_data():
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
