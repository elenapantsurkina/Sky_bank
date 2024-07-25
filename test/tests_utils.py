import pytest
import datetime
import json
import logging
from pathlib import Path
import pandas as pd
from src.config import file_path
from src.utils import get_data

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