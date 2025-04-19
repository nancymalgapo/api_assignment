import io
import pandas as pd
import requests
import zipfile

from datetime import datetime
from typing import Tuple


def format_date(str_date: str) -> datetime:
    return datetime.strptime(str_date, '%Y-%m-%d')


def validate_currency(currency: str) -> Tuple[bool, str]:
    """
    Validates the input currency string.

    1. Checks if the length of the currency string is exactly 3.
    2. Checks if the currency is not equal to 'EUR'.

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating validity and a message.
    """
    if len(currency) != 3:
        return False, "Currency code must be exactly 3 characters long"

    if currency == "EUR":
        return False, "Currency cannot be EUR"

    return True, "Success"


def validate_date(str_date: str) -> Tuple[bool, str]:
    """
    Validates the input date string.

    1. Checks if the date is in the future.
    2. Checks if the date format is YYYY-MM-DD.

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating validity and a message.
    """
    try:
        input_date = format_date(str_date)
    except ValueError:
        return False, "Invalid date format"

    today = datetime.now()
    if input_date > today:
        return False, "Date cannot be in the future"

    return True, "Success"


def clean_data(df: pd.DataFrame):
    df = df.fillna("")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


def load_data():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
    response = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f, index_col=0)
            clean_df = clean_data(df)

    return clean_df
