import json
import datetime as dt
import logging
import re
import pandas as pd

from src.utils import reader_transaction_excel


def get_greeting():
    """Функция- приветствие """
    hour = dt.datetime.now().hour
    if 4 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 16:
        return "Добрый день"
    elif 16 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def top_transaction(df_transactions):
    top_transaction = df_transactions.sort_values(by="Сумма платежа",ascending=True).iloc[:5]
    result_top_transaction = top_transaction.to_dict(orient="records")
    top_transaction_list = []
    for transaction in result_top_transaction:
        top_transaction_list.append(
            {
                "date": transaction["Дата операции"],
                "amount": transaction["Сумма платежа"],
                "cetegory": transaction["Категория"],
                "description": transaction["Описание"]
            }
        )


    return top_transaction_list

if __name__ == "__main__":
    result_top_transaction = top_transaction(reader_transaction_excel("..\\data\\operations.xlsx"))
    print(result_top_transaction)