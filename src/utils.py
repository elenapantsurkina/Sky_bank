import datetime
import json
import logging
from pathlib import Path
import pandas as pd
from src.config import file_path

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
