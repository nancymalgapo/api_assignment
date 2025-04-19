from datetime import date
from typing import Any, Dict
from pydantic import BaseModel


class Output(BaseModel):
    message: str | None = None
    results: Any | None = None


class ConvertionRatesModel(BaseModel):
    date: date
    conversion_rates: Dict


class ExchangeRateByDateModel(BaseModel):
    date: date
    currency: str
    exchange_rate: float


class HistoricalDataModel(BaseModel):
    result: Dict
