import json
from pathlib import Path
from src.config import file_path
from src.utils import reader_transaction_excel, get_user_setting, get_currency_rates, get_stock_price
from src.views import main
from src.views import get_expenses_cards, get_greeting, top_transaction, transaction_currency

ROOT_PATH = Path(__file__).resolve().parent.parent


if __name__ == "__main__":
    df_transactions = reader_transaction_excel(file_path)
    date = "29.07.2019 22:06:27"

    user_currencies, user_stocks = get_user_setting(str(ROOT_PATH) + "/user_setting.json")

    date_json = main(df_transactions, date, user_currencies, user_stocks)

    print(date_json)
    print(file_path)
