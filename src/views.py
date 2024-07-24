import json
import datetime as dt
import logging
import re
import pandas as pd
from pathlib import Path
from src.utils import reader_transaction_excel, get_data

from src.config import file_path

ROOT_PATH = Path(__file__).resolve().parent.parent


def get_greeting():
    """Функция- приветствие"""
    hour = dt.datetime.now().hour
    if 4 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def top_transaction(df_transactions):
    """Функция вывода топ 5 транзакций по сумме платежа """
    top_transaction = df_transactions.sort_values(by="Сумма платежа", ascending=True).iloc[:5]
    result_top_transaction = top_transaction.to_dict(orient="records")
    top_transaction_list = []
    for transaction in result_top_transaction:
        top_transaction_list.append(
            {
                "date": transaction["Дата операции"],
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )

    return top_transaction_list


if __name__ == "__main__":
    result_top_transaction = top_transaction(reader_transaction_excel(str(ROOT_PATH) + file_path))
    print(result_top_transaction)


def get_expenses_cards(df_transactions) -> list[dict]:
    """Функция. возвращающая расходы по каждой карте"""
    cards_dict = (
        df_transactions.loc[df_transactions["Сумма платежа"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    expenses_cards = []
    for card, expenses in cards_dict.items():
        expenses_cards.append(
            {"last_digits": card, "total spent": abs(expenses), "cashback": abs(round(expenses / 100, 2))}
        )

    return expenses_cards


if __name__ == "__main__":
    result_expenses_cards = get_expenses_cards(reader_transaction_excel(str(ROOT_PATH) + file_path))
    print(result_expenses_cards)


def transaction_current(df_transactions:pd.DataFrame, data:str) -> pd.DataFrame:
    fin_data = get_data(data)
    start_data = fin_data.replace(day=1)
    fin_data = fin_data.replace(hour=0, minute=0, second=0, microsecond=0) + dt.timedelta(days=1)
    transaction_currency = df_transactions.loc[
                                   (df_transactions["Дата операции"] <= fin_data)
                                   & (df_transactions["Дата операции"] >= start_data)]

    return transaction_currency()
