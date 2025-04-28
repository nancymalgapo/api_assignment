import pandas as pd

from io import StringIO
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


client = TestClient(app)

csv_data = '''Date,USD,JPY,BGN,CYP,CZK,DKK,EEK,GBP,HUF,LTL,LVL,MTL,PLN,ROL,RON,SEK,SIT,SKK,CHF,ISK,NOK,HRK,RUB,TRL,TRY,AUD,BRL,CAD,CNY,HKD,IDR,ILS,INR,KRW,MXN,MYR,NZD,PHP,SGD,THB,ZAR
2025-04-25,1.1357,162.8,1.9558,N/A,24.929,7.4656,N/A,0.8531,406.53,N/A,N/A,N/A,4.2683,N/A,4.9776,11.0015,N/A,N/A,0.9421,144.9,11.8415,N/A,N/A,N/A,43.6289,1.7797,6.4566,1.5754,8.2773,8.8089,19140.75,4.1124,97.0205,1634.83,22.2874,4.9676,1.9063,63.918,1.493,38.091,21.3608
2025-04-24,1.1376,162.16,1.9558,N/A,24.977,7.4655,N/A,0.855,407.3,N/A,N/A,N/A,4.2748,N/A,4.9769,10.911,N/A,N/A,0.9392,144.9,11.8285,N/A,N/A,N/A,43.584,1.7823,6.4678,1.5769,8.2925,8.826,19170.72,4.1477,97.0793,1632.79,22.2856,4.9747,1.9026,64.222,1.4924,38.041,21.2838
2025-04-23,1.1415,161.68,1.9558,N/A,25.015,7.4658,N/A,0.85793,409.03,N/A,N/A,N/A,4.2915,N/A,4.9772,10.9395,N/A,N/A,0.9382,144.9,11.891,N/A,N/A,N/A,43.7076,1.7814,6.5127,1.5789,8.3199,8.8567,19263.67,4.1849,97.4838,1623.36,22.3248,5.0123,1.9063,64.56,1.4961,38.086,21.2326
2025-04-22,1.1476,161.05,1.9558,N/A,25.081,7.4656,N/A,0.85858,409.38,N/A,N/A,N/A,4.28,N/A,4.9773,10.9153,N/A,N/A,0.9318,144.9,11.8885,N/A,N/A,N/A,43.9069,1.7945,6.6516,1.5891,8.3929,8.9027,19328.11,4.2682,97.785,1635.54,22.559,5.0397,1.9141,64.963,1.5011,38.14,21.3719
2025-04-17,1.136,161.98,1.9558,N/A,25.009,7.4672,N/A,0.85873,407.6,N/A,N/A,N/A,4.2743,N/A,4.9776,11.0278,N/A,N/A,0.9291,145.1,11.9655,N/A,N/A,N/A,43.2604,1.7845,6.681,1.5773,8.29,8.8195,19162.33,4.1852,97.0185,1609.12,22.6247,5.0069,1.9118,64.387,1.4905,37.8,21.3927
'''
mock_data = pd.read_csv(StringIO(csv_data), index_col=0)


@patch('app.services.data_cache.DataCache.get_data', return_value=mock_data)
def test_get_currencies(mock_load_data):
    response = client.get("/api/currencies")

    data = response.json()
    assert data["message"] == "success"
    assert "results" in data
    assert "currencies" in data["results"]
    assert isinstance(data["results"]["currencies"], list)

    df = pd.DataFrame(columns=["USD","JPY","BGN","CYP","CZK","DKK","EEK","GBP","HUF","LTL","LVL","MTL",
    "PLN","ROL","RON","SEK","SIT","SKK","CHF","ISK","NOK","HRK","RUB","TRL",
    "TRY","AUD","BRL","CAD","CNY","HKD","IDR","ILS","INR","KRW","MXN","MYR",
    "NZD","PHP","SGD","THB","ZAR"])
    expected_currencies = df.columns.to_list()
    assert data["results"]["currencies"] == expected_currencies


@patch('app.services.data_cache.DataCache.get_data', return_value=mock_data)
def test_get_conversion_rates(mock_load_data):
    # Valid
    response = client.get("/api/conversion-rates?date=2025-04-17")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "success"
    assert data["results"]["conversion_rates"]["USD"] == 1.136


    # Not found
    response = client.get("/api/conversion-rates?date=2023-04-16")
    assert response.status_code == 404
    assert response.json() == {"detail": "Date not found"}


@patch('app.services.data_cache.DataCache.get_data', return_value=mock_data)
def test_get_exchange_rate_by_date(mock_load_data):
    response = client.get("/api/exchange-rate-by-date?currency=PLN&date=2025-04-17")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data["results"]["exchange_rate"], (float, int))
    assert data == {
        "message": "success",
        "results": {
            "date": "2025-04-17",
            "currency": "PLN",
            "exchange_rate": 4.2743
        }
    }


@patch('app.services.data_cache.DataCache.get_data', return_value=mock_data)
def test_get_historical_data(mock_load_data):
    response = client.get("/api/historical-data?currency=PLN&high_date=2025-04-25&low_date=2025-04-24")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data["results"], dict)
    assert data == {
        "message": "success",
        "results": {
            "result": {
                "2025-04-25": 4.2683,
                "2025-04-24": 4.2748
            }
        }
    }
