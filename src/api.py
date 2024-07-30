import os

import requests
from dotenv import load_dotenv

load_dotenv("..\\.env")



def get_currency_rates(currencies):
    """функция, возвращает курсы"""
    API_KEY = os.environ.get("API_KEY")
    symbols = ",".join(currencies)
    url = f"https://api.apilayer.com/currency_data/live?symbols={symbols}"

    headers = {"apikey": 'API_KEY'}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    else:
        data = response.json()
        quotes = data.get("quotes", {})
        usd = quotes.get("USDRUB")
        eur_usd = quotes.get("USDEUR")
        eur = usd / eur_usd

        return [
            {"currency": "USD", "rate": round(usd, 2)},
            {"currency": "EUR", "rate": round(eur, 2)},
        ]


def get_stock_price(stocks):
    """Функция, возвращающая курсы акций"""
    API_KEY_STOCK = os.environ.get("API_KEY_STOCK")
    stock_price = []

    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_STOCK}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

        else:
            data_ = response.json()
            stock_price.append({"stock": stock, "price": round(float(data_["Global Quote"]["05. price"]), 2)})
    return stock_price


if __name__ == "__main__":
    print(get_currency_rates(["USD", "EUR"]))

    # stock = "AAPL"
    # stock_price = get_stock_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    # API_KEY_STOCK = "1LEAU1JX6KFZ65TN"
    # stock = "AAPL"
