import pytest
import pandas as pd

from datetime import datetime
from utils.helper import format_date, clean_data

def test_format_date():
    date_str = "2023-01-01"
    expected_date = datetime(2023, 1, 1)
    assert format_date(date_str) == expected_date


def test_format_date_invalid():
    date_str = "01-01-2023"
    with pytest.raises(ValueError):
        format_date(date_str)


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
