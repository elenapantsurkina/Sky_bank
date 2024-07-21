import json
import logging
import re

from src.utils import get_dict_transaction

def get_transactions_fizlicam(dict_transaction: list[dict], pattern):
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам"""
    dict_transaction = get_dict_transaction("..\\data\\operations.xlsx")
    pattern = r"\b[А-Я]{2}[а-я]+\s\."
    list_transactions_fl = []
    list_transactions_fl_json = json.dumps(list_transactions_fl)
    for trans in dict_transaction:
        if "Переводы" in trans and re.match(pattern, trans["Переводы"]):
            list_transactions_fl.append(trans)
            # list_transactions_fl_json = json.dumps(list_transactions_fl)
    return list_transactions_fl_json

if __name__ == "__main__":
    list_transactions_fl_json = get_transactions_fizlicam(get_dict_transaction("..\\data\\operations.xlsx"),
                                                          pattern=r"\b[А-Я]{2}[а-я]+\s\.")

    print(list_transactions_fl_json)