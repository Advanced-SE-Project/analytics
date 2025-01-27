import pytest
from src.utils.aggregator import (
    compute_line_data,
    compute_pie_data_range,
    compute_bar_data
)
from src.utils.date_utils import parse_month_year, parse_full_date, generate_month_range

def test_parse_month_year():
    # aggregator expects "YYYY-MM". e.g. "2023-02" => (month=2, year=2023)
    assert parse_month_year("2023-02") == (2, 2023)
    assert parse_month_year("2023-13") == (0, 0)  # invalid month
    assert parse_month_year("invalid") == (0, 0)

def test_parse_full_date():
    # aggregator expects "YYYY-MM-DD". e.g. "2023-03-11" => day=11, month=3, year=2023
    # But your parse_full_date code does y,m,d= splitted => day= int(d), month= int(m), year=int(y)
    # => "2023-03-11" => y="2023", m="03", d="11" => day=11, month=3, year=2023
    assert parse_full_date("2023-03-11") == (11, 3, 2023)
    assert parse_full_date("9999-99-99") == (0, 0, 0)
    assert parse_full_date("") == (0, 0, 0)

def test_generate_month_range():
    result = generate_month_range(1, 2023, 3, 2023)
    assert result == [(1, 2023), (2, 2023), (3, 2023)]

    result2 = generate_month_range(11, 2023, 2, 2024)
    # => (11,2023), (12,2023), (1,2024), (2,2024)
    assert result2 == [(11, 2023), (12, 2023), (1, 2024), (2, 2024)]

def test_compute_line_data():
    # aggregator sees transaction["date"] => e.g. "2023-11-03"
    # parse_full_date => (3, 11, 2023)
    # range => parse_month_year("2023-11") => (11,2023) .. parse_month_year("2023-12") => (12,2023)
    # labels => ["11-2023","12-2023"]
    transactions = [
        {"date": "2023-11-03", "type": "spent", "amount": 150.75, "category": "Groceries"},
        {"date": "2023-11-04", "type": "receive", "amount": 2000.00, "category": "Salary"},
        {"date": "2023-12-15", "type": "spent", "amount": 100.00, "category": "Rent"}
    ]
    result = compute_line_data(transactions, 11, 2023, 12, 2023)
    assert result["labels"] == ["11-2023", "12-2023"]
    # For 11-2023 => income=2000, expense=150.75
    # For 12-2023 => income=0, expense=100
    assert result["incomeData"] == [2000.0, 0.0]
    assert result["expenseData"] == [150.75, 100.0]

def test_compute_pie_data_range():
    # aggregator sees "2023-11-03" => day=3, month=11 => in range => aggregator sums
    transactions = [
        {"date": "2023-11-03", "type": "spent", "amount": 50, "category": "Groceries"},
        {"date": "2023-11-03", "type": "spent", "amount": 20, "category": "Rent"},
        {"date": "2023-11-03", "type": "receive", "amount": 1000, "category": "Salary"}
    ]
    categories_expense = ["Rent", "Groceries", "Utilities", "Entertainment", "Other"]
    expense_result = compute_pie_data_range(transactions, 11, 2023, 11, 2023, categories_expense, expense=True)
    assert expense_result["labels"] == categories_expense
    assert expense_result["data"] == [20.0, 50.0, 0.0, 0.0, 0.0]

    categories_income = ["Salary", "Investments", "Gifts", "Refunds", "Other"]
    income_result = compute_pie_data_range(transactions, 11, 2023, 11, 2023, categories_income, expense=False)
    assert income_result["labels"] == categories_income
    assert income_result["data"] == [1000.0, 0.0, 0.0, 0.0, 0.0]

def test_compute_bar_data():
    # aggregator => parse_month_year("2023-01") => (1,2023)..(3,2023)
    # => labels => ["01-2023","02-2023","03-2023"]
    transactions = [
        {"date": "2023-01-01", "type": "spent", "amount": 100, "category": "Groceries"},
        {"date": "2023-02-15", "type": "spent", "amount": 50, "category": "Groceries"},
        {"date": "2023-03-10", "type": "spent", "amount": 200, "category": "Rent"}
    ]
    # For "Expense" + "Groceries" => Jan=100, Feb=50, Mar=0
    bar_result = compute_bar_data(transactions, 1, 2023, 3, 2023, "Expense", "Groceries")
    assert bar_result["labels"] == ["01-2023", "02-2023", "03-2023"]
    assert bar_result["data"] == [100.0, 50.0, 0.0]