from datetime import date
from fastapi import APIRouter, status
from app.schemas import (OutputModel, CurrencyListModel, ConvertionRatesModel, ExchangeRateByDateModel,
                         HistoricalDataModel)
from app.errors import NotFoundException, BadRequestException, InternalServerErrorException
from app.services.data_cache import DataCache
from utils.helper import validate_currency, validate_date, to_string_date

data_cache = DataCache()
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
        df = await data_cache.get_data()
        currency_list = df.columns.to_list()
        result = CurrencyListModel(
            currencies=currency_list
        )
        return OutputModel(message="success", results=result)
    except Exception as e:
        raise InternalServerErrorException(detail=str(e))


@router.get("/conversion-rates", response_model=OutputModel, status_code=status.HTTP_200_OK)
async def get_conversion_rates(input_date: date):
    """
    Get the conversion rate of all currencies against Euro from a given date
    """
    is_valid, msg = validate_date(input_date)
    if not is_valid:
        raise BadRequestException(detail=msg)
    else:
        df = await data_cache.get_data()
        str_date = to_string_date(input_date)
        if str_date in df.index:
            output = ConvertionRatesModel(
                date=input_date,
                conversion_rates=df.loc[str_date].to_dict()
            )
            return OutputModel(message="success", results=output)
        else:
            raise NotFoundException(detail="Date not found")


@router.get("/exchange-rate-by-date", response_model=OutputModel, status_code=status.HTTP_200_OK)
async def get_exchange_rate_by_date(currency: str, input_date: date):
    """
    Get the exchange rate of a given pair of date and currency
    """
    try:
        df = await data_cache.get_data()
        currency = currency.upper()
        is_valid_currency, _ = validate_currency(currency)
        is_valid_date, _ = validate_date(input_date)
        if not is_valid_date or not is_valid_currency:
            raise BadRequestException(detail=f"Given currency/date is invalid")
        elif currency not in df.columns:
            raise BadRequestException(detail=f"Given currency is unsupported")
        else:
            value = df.loc[input_date.strftime('%Y-%m-%d'), currency]
            result = ExchangeRateByDateModel(
                date=input_date,
                currency=currency,
                exchange_rate=value
            )

            return OutputModel(message="success", results=result)
    except KeyError:
        raise InternalServerErrorException(detail="Date not yet available")


@router.get("/historical-data", response_model=OutputModel, status_code=status.HTTP_200_OK)
async def get_historical_data(currency: str, high_date: date, low_date: date):
    """
    Get the exchange rates of a currency from a requested date range
    """
    df = await data_cache.get_data()
    currency = currency.upper()
    is_valid_currency, msg = validate_currency(currency)

    if not is_valid_currency or currency not in df.columns:
        raise NotFoundException(detail=f"Currency not found or {msg}")

    if high_date > low_date:
        _range = df.sort_index().loc[to_string_date(low_date):to_string_date(high_date), currency]
        if not _range.empty:
            result = HistoricalDataModel(
                result={_date.strftime('%Y-%m-%d'): float(value)
                        for _date, value in zip(_range.index, _range.values)}
            )
            return OutputModel(message="success", results=result)
        else:
            raise NotFoundException(detail="No exchange rates found for the given range")
    else:
        raise BadRequestException(detail="The high date cannot be less than or equal to the low date.")
