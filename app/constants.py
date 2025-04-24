APP_TITLE = "Exchange Rate API"
APP_DESCRIPTION = """
## Exchange Rate API

Exchange rates are provided by an external API 
`https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`. 

### Supported operations are:
- fetch all supported currencies
- get the exchange rate of all currencies from a given date
- get the exchange rate of a given pair of date and currency 
- get the exchange rates of a currency from a requested date range
- fetch information updates from ECB 

This application is made possible by FastAPI.

"""
URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
