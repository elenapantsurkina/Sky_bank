import json
import logging
import re

from src.utils import get_dict_transaction


def get_transactions_fizlicam(dict_transaction: list[dict], pattern):
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам"""

    list_transactions_fl = []
    # list_transactions_fl_json = json.dumps(list_transactions_fl)
    for trans in dict_transaction:

        if "Описание" in trans and re.match(pattern, trans["Описание"]):
            list_transactions_fl.append(trans)
            list_transactions_fl_json = json.dumps(list_transactions_fl, ensure_ascii=False)
    return list_transactions_fl_json


if __name__ == "__main__":
    list_transactions_fl_json = get_transactions_fizlicam(
        get_dict_transaction("..\\data\\operations.xlsx"), pattern=r"\b[А-Я][а-я]+\s[А-Я]\."
    )

    print(list_transactions_fl_json)
