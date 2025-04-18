from fastapi import APIRouter, HTTPException
from app.schemas import Output
from utils.helper import load_data

df = load_data()

router = APIRouter(
    tags=["exchange_rates"]
    )

@router.get("/currencies", response_model=Output)
async def get_currencies():
    """
    Get a list of all supported currencies
    """
    currency_list = df.columns.to_list()
    result = {
        "currencies" : currency_list
    }
    return Output(message="success", results=result)


@router.get("/conversion-rates", response_model=Output)
async def get_conversion_rates(date: str):
    """
    Get the conversion rate of all currencies against Euro from a given date
    """
    if date in df.index:
        output = {
            "date": date,
            "conversion_rates": df.loc[date].to_dict()
        }
        return Output(message="success", results=output)
    else:
        raise HTTPException(status_code=404, detail="Date not found")


@router.get("/exchange-rate-by-date", response_model=Output)
async def get_exchange_rate_by_date(currency: str, date: str):
    """
    Get the exchange rate of a given pair of date and currency
    """
    value = df.loc[date, currency]
    result = {
        'date': date,
        'currency': currency,
        'exchange_rate': value
    }
    return Output(message="success", results=result)


@router.get("/historical-data", response_model=Output)
async def get_historical_data(currency: str, start_date: str, end_date: str):
    """
    Get the exchange rates of a currency from a requested date range
    """
    if currency not in df.columns:
        raise HTTPException(status_code=404, detail="Currency not found")
    date_range = df.loc[start_date:end_date, currency]
    result = {date: float(value) for date, value in zip(date_range.index, date_range.values)}

    return Output(message="success", results=result)
