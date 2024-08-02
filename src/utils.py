import datetime
import json
import logging
from pathlib import Path
import pandas as pd
from src.config import file_path
import os
import requests
from dotenv import load_dotenv

load_dotenv("..\\.env")

ROOT_PATH = Path(__file__).resolve().parent.parent

logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data(data: str) -> datetime.datetime:
    """Функция преобразования даты"""
    logger.info(f"Получена строка даты: {data}")
    try:
        data_obj = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
        logger.info(f"Преобразована в объект datetime: {data_obj}")
        return data_obj
    except ValueError as e:
        logger.error(f"Ошибка преобразования даты: {e}")
        raise e


def reader_transaction_excel(file_path) -> pd.DataFrame:
    """Функция принимает на вход путь до файла и возвращает датафрейм"""
    logger.info(f"Вызвана функция получения транзакций из файла {file_path}")
    try:
        df_transactions = pd.read_excel(file_path)
        logger.info(f"Файл {file_path} найден, данные о транзакциях получены")

        return df_transactions
    except FileNotFoundError:
        logger.info(f"Файл {file_path} не найден")
        raise


def get_dict_transaction(file_path) -> list[dict]:
    """Функция преобразовывающая датафрейм в словарь pyhton"""
    logger.info(f"Вызвана функция get_dict_transaction с файлом {file_path}")
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Файл {file_path}  прочитан")
        dict_transaction = df.to_dict(orient="records")
        logger.info(f"Датафрейм  преобразован в список словарей")
        return dict_transaction
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        raise
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise


if __name__ == "__main__":
    dict_transaction = get_dict_transaction(str(ROOT_PATH) + file_path)
    print(dict_transaction)


def get_user_setting(path):
    """Функция перевода настроек пользователя(курс и акции) из json объекта"""
    logger.info(f"Вызвана функция с файлом {path}")
    with open(path, "r", encoding="utf-8") as f:
        user_setting = json.load(f)
        logger.info(f"Получены настройки пользователя")
    return user_setting["user_currencies"], user_setting["user_stocks"]
#
#
# def get_currency_rates(currencies):
#     """функция, возвращает курсы"""
#     logger.info("Вызвана функция для получения курсов")
#     API_KEY = os.environ.get("API_KEY")
#     symbols = ",".join(currencies)
#     url = f"https://api.apilayer.com/currency_data/live?symbols={symbols}"
#
#     headers = {"apikey": API_KEY}
#     response = requests.get(url, headers=headers)
#     status_code = response.status_code
#     if status_code != 200:
#         print(f"Запрос не был успешным. Возможная причина: {response.reason}")
#
#     else:
#         data = response.json()
#         quotes = data.get("quotes", {})
#         usd = quotes.get("USDRUB")
#         eur_usd = quotes.get("USDEUR")
#         eur = usd / eur_usd
#         logger.info("Функция завершила свою работу")
#
#         return [
#             {"currency": "USD", "rate": round(usd, 2)},
#             {"currency": "EUR", "rate": round(eur, 2)},
#         ]
#
#
# def get_stock_price(stocks):
#     """Функция, возвращающая курсы акций"""
#     logger.info("Вызвана функция возвращающая курсы акций")
#     API_KEY_STOCK = os.environ.get("API_KEY_STOCK")
#     stock_price = []
#     for stock in stocks:
#         url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_STOCK}"
#         response = requests.get(url)
#         if response.status_code != 200:
#             print(f"Запрос не был успешным. Возможная причина: {response.reason}")
#
#         else:
#             data_ = response.json()
#             stock_price.append({"stock": stock, "price": round(float(data_["Global Quote"]["05. price"]), 2)})
#     logger.info("Функция завершила свою работу")
#     return stock_price
#
#
# if __name__ == "__main__":
#     print(get_currency_rates(["USD", "EUR"]))
#
#     stock = "AAPL"
#     stock_price = get_stock_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
#     API_KEY_STOCK = "1LEAU1JX6KFZ65TN"
