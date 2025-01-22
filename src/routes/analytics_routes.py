import requests
import logging
from flask import Blueprint, request, jsonify
from ..config import TRANSACTION_SERVICE_URL
from ..utils.date_utils import parse_month_year
from ..utils.aggregator import (
    compute_line_data,
    compute_pie_data_range,
    compute_bar_data
)

analytics_blueprint = Blueprint('analytics', __name__)
logger = logging.getLogger(__name__)


@analytics_blueprint.route('/line', methods=['GET'])
def get_line_chart():
    """
    GET /analytics/line?userId=1&startMonth=01-2023&endMonth=03-2023
    Returns monthly Income vs Expenses for the given month range.
    
    Query Params:
    - userId (int)
    - startMonth (str) in MM-YYYY
    - endMonth (str) in MM-YYYY
    
    Forward the Authorization header to the Transaction microservice
    if present.
    """
    user_id = request.args.get('userId')
    start_month_str = request.args.get('startMonth')
    end_month_str = request.args.get('endMonth')

    if not (user_id and start_month_str and end_month_str):
        return jsonify({"error": "Missing required parameters (userId, startMonth, endMonth)."}), 400

    # Grab the Authorization token from incoming request (if any)
    token = request.headers.get('Authorization')
    headers = {}
    if token:
        headers["Authorization"] = token

    # Fetch transactions
    resp = requests.get(
        f"{TRANSACTION_SERVICE_URL}/transactions",
        params={"userId": user_id},
        headers=headers
    )
    if resp.status_code != 200:
        logger.error(f"Transaction Service responded with status {resp.status_code}")
        return jsonify({"error": "Unable to fetch transactions from Transaction Service"}), 502

    transactions = resp.json()
    start_m, start_y = parse_month_year(start_month_str)
    end_m, end_y = parse_month_year(end_month_str)

    data = compute_line_data(transactions, start_m, start_y, end_m, end_y)
    return jsonify(data), 200


@analytics_blueprint.route('/pie/expense', methods=['GET'])
def get_expense_pie_range():
    """
    GET /analytics/pie/expense?userId=1&startMonth=01-2024&endMonth=03-2024
    Returns the total expense breakdown by category from startMonth to endMonth.
    
    categories = ["Rent", "Groceries", "Utilities", "Entertainment", "Other"]
    
    Query Params:
    - userId (int)
    - startMonth (str) in MM-YYYY
    - endMonth (str) in MM-YYYY
    
    Forward the Authorization header to the Transaction microservice if present.
    """
    user_id = request.args.get('userId')
    start_month_str = request.args.get('startMonth')
    end_month_str = request.args.get('endMonth')

    if not (user_id and start_month_str and end_month_str):
        return jsonify({"error": "Missing required params (userId, startMonth, endMonth)."}), 400

    # Grab the Authorization token
    token = request.headers.get('Authorization')
    headers = {}
    if token:
        headers["Authorization"] = token

    # Fetch all transactions for the user
    resp = requests.get(
        f"{TRANSACTION_SERVICE_URL}/transactions",
        params={"userId": user_id},
        headers=headers
    )
    if resp.status_code != 200:
        logger.error(f"Transaction Service responded with status {resp.status_code}")
        return jsonify({"error": "Unable to fetch transactions from Transaction Service"}), 502

    transactions = resp.json()
    start_m, start_y = parse_month_year(start_month_str)
    end_m, end_y = parse_month_year(end_month_str)

    categories = ["Rent", "Groceries", "Utilities", "Entertainment", "Other"]
    
    result = compute_pie_data_range(
        transactions, start_m, start_y, end_m, end_y,
        categories, expense=True
    )
    return jsonify(result), 200


@analytics_blueprint.route('/pie/income', methods=['GET'])
def get_income_pie_range():
    """
    GET /analytics/pie/income?userId=1&startMonth=01-2024&endMonth=03-2024
    Returns the total income breakdown by category from startMonth to endMonth.
    
    categories = ["Salary", "Investment", "Gift", "Refund", "Other"]
    
    Query Params:
    - userId (int)
    - startMonth (str) in MM-YYYY
    - endMonth (str) in MM-YYYY
    
    Forward the Authorization header to the Transaction microservice if present.
    """
    user_id = request.args.get('userId')
    start_month_str = request.args.get('startMonth')
    end_month_str = request.args.get('endMonth')

    if not (user_id and start_month_str and end_month_str):
        return jsonify({"error": "Missing required params (userId, startMonth, endMonth)."}), 400

    # Grab the Authorization token
    token = request.headers.get('Authorization')
    headers = {}
    if token:
        headers["Authorization"] = token

    # Fetch all transactions for the user
    resp = requests.get(
        f"{TRANSACTION_SERVICE_URL}/transactions",
        params={"userId": user_id},
        headers=headers
    )
    if resp.status_code != 200:
        logger.error(f"Transaction Service responded with status {resp.status_code}")
        return jsonify({"error": "Unable to fetch transactions from Transaction Service"}), 502

    transactions = resp.json()
    start_m, start_y = parse_month_year(start_month_str)
    end_m, end_y = parse_month_year(end_month_str)

    categories = ["Salary", "Investments", "Gifts", "Refunds", "Other"]
    
    result = compute_pie_data_range(
        transactions, start_m, start_y, end_m, end_y,
        categories, expense=False
    )
    return jsonify(result), 200


@analytics_blueprint.route('/bar', methods=['GET'])
def get_bar_chart():
    """
    GET /analytics/bar?userId=1&startMonth=01-2023&endMonth=03-2023&type=Expense&category=Groceries
    Returns monthly totals for a single category in the selected range.
    
    type = "Income" or "Expense"
    category (Expense) could be ["Rent", "Groceries", "Utilities", "Entertainment", "Other"]
    category (Income) could be ["Salary", "Investment", "Gift", "Refund", "Other"]
    
    Query Params:
    - userId (int)
    - startMonth (str) in MM-YYYY
    - endMonth (str) in MM-YYYY
    - type (str) => "Income" or "Expense"
    - category (str)
    
    Forward the Authorization header to the Transaction microservice if present.
    """
    user_id = request.args.get('userId')
    start_month_str = request.args.get('startMonth')
    end_month_str = request.args.get('endMonth')
    chart_type = request.args.get('type')       # "Income" or "Expense"
    category = request.args.get('category')

    if not all([user_id, start_month_str, end_month_str, chart_type, category]):
        return jsonify({"error": "Missing required parameters."}), 400

    # Grab the Authorization token
    token = request.headers.get('Authorization')
    headers = {}
    if token:
        headers["Authorization"] = token

    # Fetch transactions
    resp = requests.get(
        f"{TRANSACTION_SERVICE_URL}/transactions",
        params={"userId": user_id},
        headers=headers
    )
    if resp.status_code != 200:
        logger.error(f"Transaction Service responded with status {resp.status_code}")
        return jsonify({"error": "Unable to fetch transactions from Transaction Service"}), 502

    transactions = resp.json()
    start_m, start_y = parse_month_year(start_month_str)
    end_m, end_y = parse_month_year(end_month_str)

    data = compute_bar_data(transactions, start_m, start_y, end_m, end_y, chart_type, category)
    return jsonify(data), 200
