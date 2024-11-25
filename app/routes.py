from flask import Blueprint, request, jsonify
from .models import Income, Expense
from . import db

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/income', methods=['POST'])
def add_income():
    data = request.get_json()
    new_income = Income(amount=data['amount'], category=data['category'], date=data['date'])
    db.session.add(new_income)
    db.session.commit()
    return jsonify({"message": "Income added successfully!"}), 201

@analytics_bp.route('/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(amount=data['amount'], category=data['category'], date=data['date'])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully!"}), 201

@analytics_bp.route('/income', methods=['GET'])
def get_incomes():
    incomes = Income.query.all()
    return jsonify([{"id": income.id, "amount": income.amount, "category": income.category, "date": income.date} for income in incomes])

@analytics_bp.route('/expense', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{"id": expense.id, "amount": expense.amount, "category": expense.category, "date": expense.date} for expense in expenses])


@analytics_bp.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    total_income = db.session.query(db.func.sum(Income.amount)).scalar() or 0
    total_expense = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    balance = total_income - total_expense

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    })
