import pytest

import pandas as pd
import datetime as dt
from src.reports import spending_by_category


def test_spending_by_category():
    # Создаем тестовый DataFrame
    data = {
        "Дата операции": ["01-01-2023", "15-01-2023", "01-02-2023", "01-03-2023", "01-06-2023"],
        "Сумма": [100, 150, 200, 250, 300],
        "Категория": ["Еда", "Еда", "Транспорт", "Еда", "Транспорт"]
    }
    df = pd.DataFrame(data)

    # Тестируем функцию без указанной даты
    result = spending_by_category(df, "Еда")
    expected_result = df.loc[
        df["Категория"] == "Еда" & df["Дата операции"].between("01-01-2023", dt.datetime.now().strftime("%d-%m-%Y"))]

    assert len(result) == 3  # Должно вернуть три записи основываясь на тестовых данных
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result.reset_index(drop=True))

    # Тестируем функцию с указанной датой
    result_with_date = spending_by_category(df, "Еда", "15-02-2023")
    expected_result_with_date = df.loc[
        df["Категория"] == "Еда" & df["Дата операции"].between("15-11-2022", "15-02-2023")]

    assert len(result_with_date) == 2  # Должно вернуть две записи основываясь на тестовых данных
    pd.testing.assert_frame_equal(result_with_date.reset_index(drop=True),
                                  expected_result_with_date.reset_index(drop=True))
