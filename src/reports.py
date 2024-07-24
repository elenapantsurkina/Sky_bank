import json
import datetime
import datetime as dt
import logging
import pandas as pd
from src.utils import get_data
from src.config import file_path
from src.utils import reader_transaction_excel
from pathlib import Path
import numpy as np

ROOT_PATH = Path(__file__).resolve().parent.parent


def spending_by_category(df_transactions: pd.DataFrame, category: str, date: [str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    if date is None:
        fin_data = dt.datetime.now()
    else:
        fin_data = get_data(date)
    start_data = fin_data.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=91)

    df_temp = df_transactions.loc[
        df_transactions["Категория"] == category
    ]  # временный датафрейм с отбором по категории
    column = 0  # это номер колонки с датой транзакции
    for row in range(0, df_temp.shape[0]):
        c = df_temp.iloc[row, column]
        dat = get_data(c)  # получаем дату из колонкм
        if not ((dat <= fin_data) and (dat >= start_data)):
            df_temp.iloc[row, column] = np.nan  # если дата не в интервале, то заменяем ее на пустое значение

    col = np.array(
        ["Дата операции"]
    )  # задаём колонку в виде массива NumPy, если в ней NaN, то удалим далее все строки
    df_transactions_by_category = df_temp.dropna(axis=0, subset=col)  # удаляем лишние строки
    return df_transactions_by_category


def get_transaction_dict(df_transactions_by_category: pd.DataFrame) -> list[dict]:
    """Функция принимает на вход датафрейм и возвращает словарь формата json"""

    rows_count = df_transactions_by_category.shape[0]  # Получение количества строк в DataFrame
    column_names = df_transactions_by_category.columns.tolist()
    transactions_by_category_dict = list()
    for row in range(0, rows_count):
        row_dict = dict()
        for column in range(0, len(column_names)):
            val = df_transactions_by_category.iloc[row, column]
            if isinstance(val, np.float64):
                val = float(val)
            elif isinstance(val, np.int64):
                val = int(val)
            row_dict[column_names[column]] = val
        transactions_by_category_dict.append(row_dict)
        transactions_by_category_json = json.dumps(transactions_by_category_dict, ensure_ascii=False)
    return transactions_by_category_json


if __name__ == "__main__":
    sp = spending_by_category(reader_transaction_excel(str(ROOT_PATH) + file_path), "Аптеки", "26.07.2019 20:58:55")
    print(sp)

    transactions_by_category_json = get_transaction_dict(sp)
    print(transactions_by_category_json)
