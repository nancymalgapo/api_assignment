import io
import pandas as pd
import requests
import zipfile


def load_data():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
    response = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f, index_col=0).fillna("")
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    return df
