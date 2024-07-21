import json
import datetime
import datetime as dt
import logging
import pandas as pd
from src.utils import get_data
from src.config import file_path


def reader_transaction_excel(file_path) -> pd.DataFrame:
    """Функция принимает на вход путь до файла и возвращает датафрейм"""
    df_transactions = pd.read_excel(file_path)
    return df_transactions



def spending_by_category(df_transactions: pd.DataFrame,
                         category: str,
                         date: [str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    df_transactions = reader_transaction_excel(file_path="..\\data\\operations.xlsx")
    if date is None:
        fin_data = dt.datetime.now()
    else:
        fin_data = get_data("26.07.2019 20:58:55")
    start_data = fin_data.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=91)
    df_transactions_by_category = df_transactions.loc[(df_transactions["Дата операции"] <= fin_data)
                                                & (df_transactions["Дата операции"] >= start_data)
                                                & (df_transactions["Категория"] == category)]
    return df_transactions_by_category


def get_transaction_dict(df_transactions_by_category: pd.DataFrame) -> list[dict]:
    """Функция принимает на вход датафрейм и возвращает словарь формата json"""
    transactions_by_category_dict = df_transactions_by_category.to_dict("records")
    transactions_by_category_json = json.dumps(transactions_by_category_dict)

    return transactions_by_category_json


if __name__ == "__main__":
    spending_by_category(reader_transaction_excel(file_path="..\\data\\operations.xlsx"),
                         "Супермаркеты")
    print(spending_by_category)
