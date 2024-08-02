import pytest
import datetime
from pathlib import Path
from src.config import file_path
from src.utils import get_data, reader_transaction_excel, get_dict_transaction, get_user_setting
import unittest
import pandas as pd

import json
from unittest.mock import mock_open, patch


ROOT_PATH = Path(__file__).resolve().parent.parent


def test_get_data_input():
    """Проверяем, что функция корректно обрабатывает  ввод"""
    input_data = "01.01.2023 12:00:00"
    expected_output = datetime.datetime(2023, 1, 1, 12, 0, 0)
    assert get_data(input_data) == expected_output


def test_get_data_format():
    """Проверяем, что функция обрабатывает исключение при неверном формате ввода"""
    input_data = "01-01-2023 12:00:00"
    with pytest.raises(ValueError):
        get_data(input_data)


def test_get_data_empty_input():
    """Проверяем, что функция обрабатывает пустой ввод"""
    input_data = ""
    with pytest.raises(ValueError):
        get_data(input_data)


def test_reader_excel_file_not_found():
    """Проверка, что функция поднимает исключение при передаче несуществующего файла"""
    with pytest.raises(FileNotFoundError):
        reader_transaction_excel("path/to/non-existent/file.xlsx")


class TestReaderTransactionExcel(unittest.TestCase):
    @patch('pandas.read_excel')
    def test_successful_read(self, mock_read_excel):
        # Arrange
        mock_df = pd.DataFrame({'transaction_id': [1, 2, 3]})
        mock_read_excel.return_value = mock_df

        result = reader_transaction_excel('test_file.xlsx')

        self.assertEqual(result.shape, mock_df.shape)
        self.assertTrue(all(result['transaction_id'] == mock_df['transaction_id']))


def test_get_dict_transaction_file_not_found():
    """Тест проверяет обработку ошибки FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        get_dict_transaction("non_existent_file.xlsx")


class TestGetUserSetting(unittest.TestCase):
    @patch("builtins.open", mock_open(read_data='''
    {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN"]
    }
    '''))
    def test_get_user_setting(self):
        user_currencies, user_stocks = get_user_setting("path/to/file.json")
        self.assertEqual(user_currencies, ["USD", "EUR"])
        self.assertEqual(user_stocks, ["AAPL", "AMZN"])

    @patch("builtins.open", mock_open(read_data='''
    {
        "user_currencies": [],
        "user_stocks": []
    }
    '''))
    def test_get_user_setting_empty(self):
        user_currencies, user_stocks = get_user_setting("path/to/file.json")
        self.assertEqual(user_currencies, [])
        self.assertEqual(user_stocks, [])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_user_setting_file_not_found(self, mock_open):
        with self.assertRaises(FileNotFoundError):
            get_user_setting("path/to/file.json")
