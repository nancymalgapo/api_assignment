import httpx
import io
import pandas as pd
import zipfile

from datetime import datetime, date
from typing import Tuple

from app.constants import URL


def to_string_date(input_date: date) -> str:
    return input_date.strftime('%Y-%m-%d')


def validate_currency(currency: str) -> Tuple[bool, str]:
    """
        Validates the input currency string.

        1. Checks if the currency has length of only 3.
        2. Checks if the currency is not equal to EUR.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating validity and a message.
    """
    if len(currency) == 3 and currency != "EUR":
        return True, "Success"
    else:
        return False, "Invalid currency input or format"

def validate_date(input_date: date) -> Tuple[bool, str]:
    """
        Validates the input date string.

        1. Checks if the date is in the future.
        2. Checks if the date is a valid date object.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating validity and a message.
    """
    if not isinstance(input_date, date):
        return False, "Invalid date input"

    today = datetime.now().date()
    if input_date > today:
        return False, "Date cannot be in the future"

    return True, "Success"


def clean_data(df: pd.DataFrame):
    df = df.fillna("")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


async def load_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f, index_col=0)
            clean_df = clean_data(df)
            clean_df.index = pd.to_datetime(clean_df.index)

    return clean_df
