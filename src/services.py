import json
import logging
import re
from src.utils import get_dict_transaction


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("get_transactions_fizlicam.log"),
        logging.StreamHandler()
    ]
)


def get_transactions_fizlicam(dict_transaction: list[dict], pattern):
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам"""
    logging.info("Вызвана функция get_transactions_fizlicam")

    list_transactions_fl = []

    for trans in dict_transaction:
        if "Описание" in trans and re.match(pattern, trans["Описание"]):
            list_transactions_fl.append(trans)

    logging.info(f"Найдено {len(list_transactions_fl)} транзакций, соответствующих паттерну")

    if list_transactions_fl:
        list_transactions_fl_json = json.dumps(list_transactions_fl, ensure_ascii=False)
        logging.info(f"Возвращен JSON со {len(list_transactions_fl)} транзакциями")
        return list_transactions_fl_json
    else:
        logging.info("Возвращен пустой список")
        return "[]"


if __name__ == "__main__":
    list_transactions_fl_json = get_transactions_fizlicam(
        get_dict_transaction("..\\data\\operations.xlsx"), pattern=r"\b[А-Я][а-я]+\s[А-Я]\."
    )

    print(list_transactions_fl_json)
