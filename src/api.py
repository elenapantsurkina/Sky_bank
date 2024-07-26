import os

import requests
from dotenv import load_dotenv

load_dotenv("..\\.env")


def get_currency_rates(currencies):
    """функция, возвращает курсы"""
    API_KEY = os.environ.get("API_KEY")
    symbols = ",".join(currencies)
    url = f"https://api.apilayer.com/currency_data/live?symbols={symbols}"

    headers = {"apikey": 'KCB5FZWEnPxFIsEaZAD9cD34rKRR9YAa'}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    else:
        data = response.json()
        well = data.get("well", {})
        usd = well.get("USDRUB")
        eur_usd = well.get("USDEUR")
        eur = usd / eur_usd

        return [
            {"currency": "USD", "rate": round(usd, 2)},
            {"currency": "EUR", "rate": round(eur, 2)},
        ]


# def get_stock_price(stock):
#     """Функция, возвращающая курсы акций"""
#     stock_price = []
#     url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={s}&apikey={API_KEY_STOCK}"
#     response = requests.get(url)
#     for s in stock:
#         if status_code != 200:
#             print(f"Запрос не был успешным. Возможная причина: {response.reason}")
#
#         else:
#             data_ = response.json()
#             stock_price.append({"stock": s, "price": round(float(data_["Global Quote"]["05. price"]), 2)})
#     return stock_price


if __name__ == "__main__":
    print(get_currency_rates(["USD", "EUR"]))

#     s = "AAPL"
#     stock_price = get_stock_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
#     API_KEY_STOCK = "1LEAU1JX6KFZ65TN"
#     s = "AAPL"
