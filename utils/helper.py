import httpx
import io
import pandas as pd
import zipfile

from datetime import datetime
from typing import Tuple

from app.constants import URL


def format_date(str_date: str) -> datetime:
    return datetime.strptime(str_date, '%Y-%m-%d')


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
        return False, "Invalid date input or format"

    today = datetime.now()
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

    return clean_df
