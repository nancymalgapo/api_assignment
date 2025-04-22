from fastapi import APIRouter, status
from app.schemas import (OutputModel, CurrencyListModel, ConvertionRatesModel, ExchangeRateByDateModel,
                         HistoricalDataModel)
from app.errors import NotFoundException, BadRequestException, InternalServerErrorException
from utils.helper import load_data, validate_date, format_date

data_cache = None

async def get_data():
    global data_cache
    if data_cache is None:
        data_cache = await load_data()
    return data_cache

router = APIRouter(
    prefix="/api",
    tags=["exchange_rates"]
    )

@router.get("/currencies", response_model=OutputModel, status_code=status.HTTP_200_OK)
async def get_currencies():
    """
    Get a list of all supported currencies
    """
    try:
        df = await get_data()
        currency_list = df.columns.to_list()
        result = CurrencyListModel(
            currencies=currency_list
        )
        return OutputModel(message="success", results=result)
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))


@router.get("/conversion-rates", response_model=OutputModel, status_code=status.HTTP_200_OK)
async def get_conversion_rates(date: str):
    """
    Get the conversion rate of all currencies against Euro from a given date
    """
    is_valid, msg = validate_date(date)
    if not is_valid:
        raise BadRequestException(detail=msg)
    else:
        df = await get_data()
        if date in df.index:
            output = ConvertionRatesModel(
                date=format_date(date),
                conversion_rates=df.loc[date].to_dict()
            )
            return OutputModel(message="success", results=output)
        else:
            raise NotFoundException(detail="Date not found")


@router.get("/exchange-rate-by-date", response_model=OutputModel, status_code=status.HTTP_200_OK)
async def get_exchange_rate_by_date(currency: str, date: str):
    """
    Get the exchange rate of a given pair of date and currency
    """
    try:
        df = await get_data()
        currency = currency.upper()
        is_valid_date, _ = validate_date(date)
        if not is_valid_date or currency not in df.columns:
            raise BadRequestException(detail=f"Given currency/date is invalid")
        else:
            value = df.loc[date, currency]
            result = ExchangeRateByDateModel(
                date=format_date(date),
                currency=currency,
                exchange_rate=value
            )

            return OutputModel(message="success", results=result)
    except KeyError:
        raise InternalServerErrorException(detail="Date not yet available")


@router.get("/historical-data", response_model=OutputModel, status_code=status.HTTP_200_OK)
async def get_historical_data(currency: str, high_date: str, low_date: str):
    """
    Get the exchange rates of a currency from a requested date range
    """
    df = await get_data()
    currency = currency.upper()

    if currency not in df.columns:
        raise NotFoundException(detail="Currency not found")

    if format_date(high_date) > format_date(low_date):
        _range = df.loc[high_date:low_date, currency]
        if not _range.empty:
            result = HistoricalDataModel(
                result={_date: float(value) for _date, value in zip(_range.index, _range.values)}
            )
            return OutputModel(message="success", results=result)
        else:
            raise NotFoundException(detail="No exchange rates found for the given range")
    else:
        raise BadRequestException(detail="The high date cannot be less than or equal to the low date.")
