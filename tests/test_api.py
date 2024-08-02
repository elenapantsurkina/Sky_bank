from unittest.mock import patch, MagicMock
from src.api import get_stock_price, get_currency_rates


@patch('requests.get')
def test_successful_response(mock_get):
    mock_response = mock_response(200, {"Global Quote": {"05. price": "100.00"}})
    mock_get.return_value = mock_response

    stocks = ["AAPL", "GOOGL"]
    expected_result = [
        {"stock": "AAPL", "price": 100.00},
        {"stock": "GOOGL", "price": 100.00}
    ]

    actual_result = get_stock_price(stocks)
    assert actual_result == expected_result


@patch('requests.get')
def test_unsuccessful_response(self, mock_get):
    mock_response = self.create_mock_response(404, "Not Found")
    mock_get.return_value = mock_response

    stocks = ["AAPL", "GOOGL"]
    expected_result = []

    actual_result = get_stock_price(stocks)
    assert actual_result == expected_result


@patch('requests.get')
def test_successful_response(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "terms": "https://apilayer.com/terms",
        "privacy": "https://apilayer.com/privacy",
        "timestamp": 1683958800,
        "source": "USD",
        "quotes": {
            "USDRUB": 78.123456,
            "USDEUR": 0.9
        }
    }
    mock_get.return_value = mock_response

    currencies = ["RUB", "EUR"]
    expected_result = [
        {"currency": "USD", "rate": 78.12},
        {"currency": "EUR", "rate": 86.80}
    ]
    actual_result = get_currency_rates(currencies)
    assert actual_result == expected_result


@patch('src.api.requests')
def test_failed_response(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_get.return_value = mock_response
    currencies = ["RUB", "EUR"]
    with patch('builtins.print') as mock_print:
        actual_result = get_currency_rates(currencies)
    mock_print.assert_called_with("Запрос не был успешным. Возможная причина: Not Found")
    assert actual_result is None

@patch('src.external_api.requests')
def test_get_transaction_sum_rub1(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"result": 5917366.82}
    transaction = {"operationAmount": {"amount": "67314.70", "currency": {"code": "USD"}}}
    mock_get.get.return_value = mock_resp
    assert get_transaction_sum_rub(transaction) == 5917366.82