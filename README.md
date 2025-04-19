# Exchange Rate API

### Overview
This is a simple Exchange Rate API using FastAPI

### Exchange rates
Exchange rates are provided by an external API `https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html`

Supported operations are:
- fetch all supported currencies
- get the exchange rate of all currencies from a given date
- get the exchange rate of a given pair of date and currency 
- get the exchange rates of a currency from a requested date range
- fetch information updates from ECB

### Dependencies
All dependencies are listed inside the `requirements.txt` file.

### Application setup
1. Install all dependencies by running `pip install -r requirements.txt`
2. Run the app: `uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload`

## Documentation
Once the application is up and running, FastAPI automatic docs is viewable
at the index page.

### Endpoints
| Method | Endpoint               | Description                                                               |
|--------|------------------------|---------------------------------------------------------------------------|
| GET    | /currencies            | Get a list of all supported currencies                                    | 
| GET    | /conversion-rates      | Get the conversion rate of all currencies against Euro from a given  date |  
| GET    | /exchange-rate-by-date | Get the exchange rate of a given pair of date and currency                |
| GET    | /historical-data       | Get the exchange rates of a currency from a requested date range          |

## Status codes
| Status code | Description                               |
|-------------|-------------------------------------------|
| 200         | success                                   |
| 400         | bad request, please check your request    |
| 404         | not found                                 |
| 500         | internal server error, application failed |
