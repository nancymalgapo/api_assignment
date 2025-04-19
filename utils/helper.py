import io
import pandas as pd
import requests
import zipfile

from datetime import datetime


def format_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d')


def clean_data(df):
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
