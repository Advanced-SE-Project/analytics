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
        {"date": "2023-11-03", "type": "spent", "amount": 150.75, "category": "Groceries"},
        {"date": "2023-11-04", "type": "receive", "amount": 2000.00, "category": "Salary"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    # The aggregator expects startMonth=11-2023..endMonth=12-2023 => "MM-YYYY"
    # parse_month_year -> (11,2023)..(12,2023)
    response = client.get("/analytics/line?userId=1&startMonth=11-2023&endMonth=12-2023")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "incomeData" in data
    assert "expenseData" in data

    # The test expects Nov => income=2000, expense=150.75; Dec => income=0, expense=0
    # So the labels => ["2023-11","2023-12"]
    assert data["labels"] == ["2023-11", "2023-12"]
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

    # If the aggregator sees "03-11-2023", it gets year=2023, month=11, day=3. Actually "YYYY-MM-DD"
    # is "2023-11-03". We fix the test data so the aggregator sees month=11 => matches range=11-2023.
    mock_transactions = [
        {"date": "2023-11-03", "type": "spent", "amount": 50, "category": "Groceries"},
        {"date": "2023-11-03", "type": "spent", "amount": 20, "category": "Rent"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    response = client.get("/analytics/pie/expense?userId=1&startMonth=11-2023&endMonth=11-2023")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "data" in data
    # The aggregator sums 20 => Rent, 50 => Groceries
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
        {"date": "2023-11-03", "type": "receive", "amount": 1000, "category": "Salary"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    response = client.get("/analytics/pie/income?userId=1&startMonth=11-2023&endMonth=11-2023")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "data" in data
    # aggregator -> 1000 => Salary
    assert data["labels"] == ["Salary", "Investments", "Gifts", "Refunds", "Other"]
    assert data["data"] == [1000.0, 0.0, 0.0, 0.0, 0.0]

    #  Test missing parameters
    response = client.get("/analytics/pie/income?userId=1&startMonth=11-2023")
    assert response.status_code == 400
    assert b"Missing required params" in response.data

@patch("src.routes.analytics_routes.requests.get")
def test_get_bar_chart(mock_get, client):
    """ Covers /analytics/bar route."""
    mock_transactions = [
        # aggregator sees "2023-01-01" => day=1, month=1 => OK for Jan
        {"date": "2023-01-01", "type": "spent", "amount": 100, "category": "Groceries"},
        # aggregator sees "2023-02-15" => day=15, month=2 => OK for Feb
        {"date": "2023-02-15", "type": "spent", "amount": 50, "category": "Groceries"}
    ]

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_transactions

    response = client.get("/analytics/bar?userId=1&startMonth=01-2023&endMonth=02-2023&type=Expense&category=Groceries")
    assert response.status_code == 200
    data = json.loads(response.data)

    assert "labels" in data
    assert "data" in data
    # aggregator => month=1 => total=100, month=2 => total=50
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
