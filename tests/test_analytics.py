import pytest
from src.utils.aggregator import (
    compute_line_data,
    compute_pie_data_range,
    compute_bar_data
)
from src.utils.date_utils import parse_month_year, parse_full_date, generate_month_range


def test_parse_month_year():
    assert parse_month_year("02-2023") == (2, 2023)
    assert parse_month_year("13-2023") == (0, 0)  # invalid month
    assert parse_month_year("invalid") == (0, 0)


def test_parse_full_date():
    assert parse_full_date("03-11-2023") == (3, 11, 2023)
    assert parse_full_date("99-99-9999") == (0, 0, 0)  # invalid date
    assert parse_full_date("") == (0, 0, 0)


def test_generate_month_range():
    result = generate_month_range(1, 2023, 3, 2023)
    assert result == [(1, 2023), (2, 2023), (3, 2023)]

    result2 = generate_month_range(11, 2023, 2, 2024)
    # Should include: (11, 2023), (12, 2023), (1, 2024), (2, 2024)
    assert result2 == [(11, 2023), (12, 2023), (1, 2024), (2, 2024)]


def test_compute_line_data():
    transactions = [
        {"date": "03-11-2023", "type": "spent", "amount": 150.75, "category": "Groceries"},
        {"date": "04-11-2023", "type": "receive", "amount": 2000.00, "category": "Salary"},
        {"date": "15-12-2023", "type": "spent", "amount": 100.00, "category": "Rent"}
    ]
    result = compute_line_data(transactions, 11, 2023, 12, 2023)
    assert result["labels"] == ["11-2023", "12-2023"]
    # For 11-2023 => income=2000, expense=150.75
    # For 12-2023 => income=0, expense=100
    assert result["incomeData"] == [2000.0, 0.0]
    assert result["expenseData"] == [150.75, 100.0]


def test_compute_pie_data_range():
    transactions = [
        {"date": "03-11-2023", "type": "spent", "amount": 50, "category": "Groceries"},
        {"date": "03-11-2023", "type": "spent", "amount": 20, "category": "Rent"},
        {"date": "03-11-2023", "type": "receive", "amount": 1000, "category": "Salary"}
    ]
    categories_expense = ["Rent", "Groceries", "Utilities", "Entertainment", "Other"]
    expense_result = compute_pie_data_range(transactions, 11, 2023, 11, 2023, categories_expense, expense=True)
    # "Rent" => 20, "Groceries" => 50, "Utilities" => 0, "Entertainment" => 0, "Other" => 0
    assert expense_result["labels"] == categories_expense
    assert expense_result["data"] == [20.0, 50.0, 0.0, 0.0, 0.0]

    categories_income = ["Salary", "Investment", "Gift", "Refund", "Other"]
    income_result = compute_pie_data_range(transactions, 11, 2023, 11, 2023, categories_income, expense=False)
    # Only 1 income of 1000 for "Salary"
    assert income_result["labels"] == categories_income
    assert income_result["data"] == [1000.0, 0.0, 0.0, 0.0, 0.0]


def test_compute_bar_data():
    transactions = [
        {"date": "01-01-2023", "type": "spent", "amount": 100, "category": "Groceries"},
        {"date": "15-02-2023", "type": "spent", "amount": 50, "category": "Groceries"},
        {"date": "10-03-2023", "type": "spent", "amount": 200, "category": "Rent"}
    ]
    # Test for "Expense" + "Groceries"
    bar_result = compute_bar_data(transactions, 1, 2023, 3, 2023, "Expense", "Groceries")
    assert bar_result["labels"] == ["01-2023", "02-2023", "03-2023"]
    # Jan -> 100, Feb -> 50, Mar -> 0
    assert bar_result["data"] == [100.0, 50.0, 0.0]
