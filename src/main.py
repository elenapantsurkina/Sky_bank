import json
import datetime
import logging
import pandas as pd
import re
from src.utils import get_greeting,
from src.api import get_stock_price, get_currency_rates
from


def main(df_transactions, user_currencies, user_stocks):
    "Главная функция, делающая вывод на главную страницу"
    greeting = get_greeting()
    transactions = get_
