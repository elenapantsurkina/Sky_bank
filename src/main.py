import json
import datetime
import logging
import pandas as pd
import re
from src.utils import reader_transaction_excel
from src.api import get_stock_price, get_currency_rates
from src.views import get_greeting, top_transaction, get_expenses_cards, transaction_currency
from src.config import file_path
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent



def main(df_transactions, date, user_currencies, user_stocks):
    "Главная функция, делающая вывод на главную страницу"
    greeting = get_greeting()
    transactions = transaction_currency(df_transactions, date)
    cards = get_expenses_cards(df_transactions)
    top_transaction = top_transaction(df_transactions)
    currency_rates = get_currency_rates(user_currencies)
    stock_prices = get_stock_price(user_stocks)

    date_json = json.dumps({
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transaction,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        },
        indent=4,
        ensure_ascii=False,
    )
    return date_json

if __name__ == "__main__":
    df_transactions = reader_transaction_excel(str(ROOT_PATH) + file_path)
    date = "29.07.2019 22:06:27"
    user_currencies = "USD", "EUR"
    user_stocks = "AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"
    date_json = main(df_transactions, date, user_currencies, user_stocks)
    print(date_json)
