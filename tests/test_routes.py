import pytest
import json
from unittest.mock import patch
from src.app import create_app


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("src.routes.analytics_routes.requests.get")
def test_get_line_chart(mock_get, client):
    """ Covers /analytics/line for valid and error cases."""
    mock_transactions = [
        {"date": "03-11-2023", "type": "spent", "amount": 150.75, "category": "Groceries"},
        {"date": "04-11-2023", "type": "receive", "amount": 2000.00, "category": "Salary"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    response = client.get("/analytics/line?userId=1&startMonth=11-2023&endMonth=12-2023")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "incomeData" in data
    assert "expenseData" in data
    assert data["labels"] == ["11-2023", "12-2023"]
    assert data["incomeData"] == [2000.0, 0.0]
    assert data["expenseData"] == [150.75, 0.0]

    #  Test API failure (502 response)
    mock_get.return_value.status_code = 500
    response = client.get("/analytics/line?userId=1&startMonth=11-2023&endMonth=12-2023")
    assert response.status_code == 502
    assert b"Unable to fetch transactions" in response.data

    #  Test missing parameters
    response = client.get("/analytics/line?userId=1&startMonth=11-2023")  # Missing endMonth
    assert response.status_code == 400
    assert b"Missing required parameters" in response.data


@patch("src.routes.analytics_routes.requests.get")
def test_get_expense_pie_range(mock_get, client):
    """ Covers /analytics/pie/expense route."""
    mock_transactions = [
        {"date": "03-11-2023", "type": "spent", "amount": 50, "category": "Groceries"},
        {"date": "03-11-2023", "type": "spent", "amount": 20, "category": "Rent"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    response = client.get("/analytics/pie/expense?userId=1&startMonth=11-2023&endMonth=11-2023")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "data" in data
    assert data["labels"] == ["Rent", "Groceries", "Utilities", "Entertainment", "Other"]
    assert data["data"] == [20.0, 50.0, 0.0, 0.0, 0.0]

    #  Test missing parameters
    response = client.get("/analytics/pie/expense?userId=1&startMonth=11-2023")
    assert response.status_code == 400
    assert b"Missing required params" in response.data


@patch("src.routes.analytics_routes.requests.get")
def test_get_income_pie_range(mock_get, client):
    """ Covers /analytics/pie/income route."""
    mock_transactions = [
        {"date": "03-11-2023", "type": "receive", "amount": 1000, "category": "Salary"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    response = client.get("/analytics/pie/income?userId=1&startMonth=11-2023&endMonth=11-2023")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "data" in data
    assert data["labels"] == ["Salary", "Investment", "Gift", "Refund", "Other"]
    assert data["data"] == [1000.0, 0.0, 0.0, 0.0, 0.0]

    #  Test missing parameters
    response = client.get("/analytics/pie/income?userId=1&startMonth=11-2023")
    assert response.status_code == 400
    assert b"Missing required params" in response.data


@patch("src.routes.analytics_routes.requests.get")
def test_get_bar_chart(mock_get, client):
    """ Covers /analytics/bar route."""
    mock_transactions = [
        {"date": "01-01-2023", "type": "spent", "amount": 100, "category": "Groceries"},
        {"date": "15-02-2023", "type": "spent", "amount": 50, "category": "Groceries"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    response = client.get("/analytics/bar?userId=1&startMonth=01-2023&endMonth=02-2023&type=Expense&category=Groceries")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "data" in data
    assert data["labels"] == ["01-2023", "02-2023"]
    assert data["data"] == [100.0, 50.0]

    #  Test missing parameters
    response = client.get("/analytics/bar?userId=1&startMonth=01-2023")
    assert response.status_code == 400
    assert b"Missing required parameters" in response.data


@patch("src.routes.analytics_routes.requests.get")
def test_transaction_service_unavailable(mock_get, client):
    """ Simulates Transaction Service downtime (502 response)."""
    mock_get.return_value.status_code = 500

    response = client.get("/analytics/line?userId=1&startMonth=11-2023&endMonth=12-2023")
    assert response.status_code == 502
    assert b"Unable to fetch transactions" in response.data
