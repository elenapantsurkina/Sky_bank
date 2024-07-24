import json
import datetime
import logging
import pandas as pd
from src.config import file_path
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent


def get_data(data: str) -> datetime.datetime:
    """Функция преобразования даты"""

    data_obj = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
    return data_obj


def reader_transaction_excel(file_path) -> pd.DataFrame:
    """Функция принимает на вход путь до файла и возвращает датафрейм"""
    df_transactions = pd.read_excel(file_path)
    print(df_transactions)
    return df_transactions


def get_dict_transaction(file_path) -> list[dict]:
    """Функция преобразовывающая датафрейм в словарь pyhton"""
    df = pd.read_excel(file_path)
    dict_transaction = df.to_dict(orient="records")

    return dict_transaction


if __name__ == "__main__":
    dict_transaction = get_dict_transaction(str(ROOT_PATH) + file_path)
    print(dict_transaction)
