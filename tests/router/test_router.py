import pandas as pd

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_currencies():
    response = client.get("/currencies")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "success"
    assert "results" in data
    assert "currencies" in data["results"]

    # Check if the currencies list matches the DataFrame columns
    df = pd.DataFrame(columns=["USD","JPY","BGN","CYP","CZK","DKK","EEK","GBP","HUF","LTL","LVL","MTL",
                               "PLN","ROL","RON","SEK","SIT","SKK","CHF","ISK","NOK","HRK","RUB","TRL",
                               "TRY","AUD","BRL","CAD","CNY","HKD","IDR","ILS","INR","KRW","MXN","MYR",
                               "NZD","PHP","SGD","THB","ZAR"])
    expected_currencies = df.columns.to_list()
    assert data["results"]["currencies"] == expected_currencies


def test_get_conversion_rates():
    response = client.get("/conversion-rates?date=2023-04-16")
    assert response.status_code == 404
    assert response.json() == {"detail": "Date not found"}


def test_get_exchange_rate_by_date():
    response = client.get("/exchange-rate-by-date?currency=PLN&date=2025-04-16")
    assert response.status_code == 200
    assert response.json() == {
        "message": "success",
        "results": {
            "date": "2025-04-16",
            "currency": "PLN",
            "exchange_rate": 4.2933
        }
    }


def test_get_historical_data():
    response = client.get("/historical-data?currency=PLN&start_date=2025-04-16&end_date=2025-04-15")
    assert response.status_code == 200
    assert response.json() == {
        "message": "success",
        "results": {
            "result": {
                "2025-04-16": 4.2933,
                "2025-04-15": 4.2844
            }
        }
    }
