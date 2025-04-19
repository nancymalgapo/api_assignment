from datetime import date
from typing import Any, Dict, List
from pydantic import BaseModel


class OutputModel(BaseModel):
    message: str | None = None
    results: Any | None = None


class CurrencyListModel(BaseModel):
    currencies: List


class ConvertionRatesModel(BaseModel):
    date: date
    conversion_rates: Dict


class ExchangeRateByDateModel(BaseModel):
    date: date
    currency: str
    exchange_rate: float


class HistoricalDataModel(BaseModel):
    result: Dict
