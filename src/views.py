import datetime as dt
from datetime import datetime
import logging
from pathlib import Path
import pandas as pd
from src.config import file_path
from src.utils import get_data, reader_transaction_excel

ROOT_PATH = Path(__file__).resolve().parent.parent


logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\views.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


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
    """Функция вывода топ 5 транзакций по сумме платежа"""
    logger.info("Начало работы функции top_transaction")
    top_transaction = df_transactions.sort_values(by="Сумма платежа", ascending=True).iloc[:5]
    logger.info("Получен топ 5 транзакций по сумме платежа")
    result_top_transaction = top_transaction.to_dict(orient="records")
    top_transaction_list = []
    for transaction in result_top_transaction:
        top_transaction_list.append(
            {
                #"date": transaction["Дата операции"],
                "date": str((datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")).date().strftime("%d.%m.%Y")).replace('-', '.'),
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    logger.info("Сформирован список топ 5 транзакций")
    return top_transaction_list


if __name__ == "__main__":
    top_transaction_list = top_transaction(reader_transaction_excel(str(ROOT_PATH) + file_path))
    print(top_transaction_list)


def get_expenses_cards(df_transactions) -> list[dict]:
    """Функция, возвращающая расходы по каждой карте"""
    logger.info("Начало выполнения функции get_expenses_cards")

    cards_dict = (
        df_transactions.loc[df_transactions["Сумма платежа"] < 0]
        .groupby(by="Номер карты")
        .agg("Сумма платежа")
        .sum()
        .to_dict()
    )
    logger.debug(f"Получен словарь расходов по картам: {cards_dict}")

    expenses_cards = []
    for card, expenses in cards_dict.items():
        expenses_cards.append(
            {"last_digits": card, "total spent": abs(expenses), "cashback": abs(round(expenses / 100, 2))}
        )
        logger.info(f"Добавлен расход по карте {card}: {abs(expenses)}")

    logger.info("Завершение выполнения функции get_expenses_cards")
    return expenses_cards


if __name__ == "__main__":
    result_expenses_cards = get_expenses_cards(reader_transaction_excel(str(ROOT_PATH) + file_path))
    print(result_expenses_cards)


def transaction_currency(df_transactions: pd.DataFrame, data: str) -> pd.DataFrame:
    """Функция, формирующая расходы в заданном интервале"""
    logger.info(f"Вызвана функция transaction_currency с аргументами: df_transactions={df_transactions}, data={data}")
    fin_data = get_data(data)
    logger.debug(f"Получена конечная дата: {fin_data}")
    start_data = fin_data.replace(day=1)
    logger.debug(f"Получена начальная дата: {start_data}")
    fin_data = fin_data.replace(hour=0, minute=0, second=0, microsecond=0) + dt.timedelta(days=1)
    logger.debug(f"Обновлена конечная дата: {fin_data}")
    transaction_currency = df_transactions.loc[
        (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) <= fin_data)
        & (pd.to_datetime(df_transactions["Дата операции"], dayfirst=True) >= start_data)
        ]
    logger.info(f"Получен DataFrame transaction_currency: {transaction_currency}")

    return transaction_currency


if __name__ == "__main__":
    transaction_currency = transaction_currency(
        reader_transaction_excel((str(ROOT_PATH) + file_path)), "29.07.2019 22:06:27"
    )
    print(transaction_currency)
