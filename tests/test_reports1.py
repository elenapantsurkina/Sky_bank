# import pytest
# import pandas as pd
# from src.reports1 import get_transaction_dict
#
#
# def test_get_transaction_dict():
#     data = {
#         'col1': [1.0, 2.0, 3.0],
#         'col2': [4, 5, 6]
#     }
#     df = pd.DataFrame(data)
#     result = get_transaction_dict(df)
#     expected = '[{"col1": 1.0, "col2": 4}, {"col1": 2.0, "col2": 5}, {"col1": 3.0, "col2": 6}]'
#     assert result == expected
