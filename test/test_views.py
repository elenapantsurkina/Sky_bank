import datetime as dt
import pytest
from unittest.mock import patch
from pathlib import Path
import pandas as pd
from src.config import file_path
from src.views import get_greeting, get_expenses_cards, top_transaction, transaction_currency


ROOT_PATH = Path(__file__).resolve().parent.parent


def test_get_greeting_morning():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 8, 0, 0)
            assert get_greeting() == "Доброе утро"


def test_get_greeting_afternoon():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 14, 0, 0)
            assert get_greeting() == "Добрый день"


def test_get_greeting_evening():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 19, 0, 0)
            assert get_greeting() == "Добрый вечер"


def test_get_greeting_night():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 23, 0, 0)
            assert get_greeting() == "Доброй ночи"


@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        "Номер карты": ["*1112", "*5091"],
        "Сумма платежа": [-100, -200]
    })

def test_get_expenses_cards(sample_transactions):
    result = get_expenses_cards(sample_transactions)

    assert result[0] == {"last_digits": "*1112", "total spent": 100, "cashback": 1.0}
    assert result[1] == {"last_digits": "*5091", "total spent": 200, "cashback": 2.0}



# @pytest.fixture
# def sample_data():
#     data = {
#         "Дата операции": ["2023-04-01", "2023-04-02", "2023-04-03", "2023-04-04", "2023-04-05", "2023-04-06"],
#         "Сумма платежа": [-100, -200, -50, -300, -150, -75],
#         "Категория": ["Еда", "Транспорт", "Развлечения", "Одежда", "Коммунальные услуги", "Здоровье"],
#         "Описание": ["Обед в кафе", "Проезд на автобусе", "Поход в кино", "Покупка футболки", "Оплата счетов", "Визит к врачу"]
#     }
#     return pd.DataFrame(data)
#
# def test_top_transaction(sample_data):
#     top_transactions = top_transaction(sample_data)
#     assert len(top_transactions) == 5
#     assert top_transactions[0]["amount"] == -50
#     assert top_transactions[0]["category"] == "Развлечения"
#     assert top_transactions[0]["description"] == "Поход в кино"
#
#
# @pytest.fixture
# def sample_df():
#     data = {
#         "Дата операции": ["2023-04-01", "2023-04-15", "2023-05-01", "2023-05-15"],
#         "Сумма": [100, 200, 150, 300]
#     }
#     return pd.DataFrame(data)
#
# def test_transaction_currency(sample_df):
#     # Тест с корректными входными данными
#     result = transaction_currency(sample_df, "2023-05-01")
#     assert isinstance(result, pd.DataFrame)
#     assert len(result) == 2
#     assert (result["Дата операции"] >= pd.Timestamp("2023-05-01")).all()
#     assert (result["Дата операции"] <= pd.Timestamp("2023-06-01")).all()
#
#     # Тест с некорректными входными данными
#     with pytest.raises(ValueError):
#         transaction_currency(sample_df, "invalid_date")
