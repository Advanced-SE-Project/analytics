from .date_utils import parse_full_date, generate_month_range

def compute_line_data(transactions, start_m, start_y, end_m, end_y):
    """
    Returns:
    {
      "labels": ["01-2023", "02-2023", ...],
      "incomeData": [2000.0, 2500.0, ...],
      "expenseData": [150.75, 300.0, ...]
    }
    Summarizes total income vs. expenses for each month in the range.
    """
    months = generate_month_range(start_m, start_y, end_m, end_y)
    labels = []
    income_list = []
    expense_list = []

    for (m, y) in months:
        label_str = f"{m:02d}-{y}"
        labels.append(label_str)

        monthly_income = 0.0
        monthly_expense = 0.0

        for t in transactions:
            (dd, mm, yyyy) = parse_full_date(t.get('date', '01-01-1970'))
            if mm == m and yyyy == y:
                if t['type'] == 'receive':
                    monthly_income += float(t['amount'])
                elif t['type'] == 'spent':
                    monthly_expense += float(t['amount'])
        
        income_list.append(round(monthly_income, 2))
        expense_list.append(round(monthly_expense, 2))

    return {
        "labels": labels,
        "incomeData": income_list,
        "expenseData": expense_list
    }

def compute_pie_data_range(transactions, start_m, start_y, end_m, end_y, categories, expense=True):
    """
    Sums up amounts by category over all months in [startMonth, endMonth].
    
    :param transactions: list of transaction dicts
    :param start_m, start_y: start month/year (int)
    :param end_m, end_y: end month/year (int)
    :param categories: list of category strings (e.g. ["Rent","Groceries","Utilities","Entertainment","Other"])
    :param expense: bool - True => sum 'spent', False => sum 'receive'
    
    Returns a dict like:
    {
      "labels": ["Rent", "Groceries", "Utilities", "Entertainment", "Other"],
      "data": [600, 150.75, 120, 80, 0]
    }
    """
    # Initialize totals for each category
    totals = {cat: 0.0 for cat in categories}

    # Generate a list of all (month, year) tuples
    month_tuples = generate_month_range(start_m, start_y, end_m, end_y)

    # Convert transaction data
    for t in transactions:
        day, mm, yyyy = parse_full_date(t.get('date', '01-01-1970'))

        # Check if the transaction's month/year is within our range
        if any((mm == m and yyyy == y) for (m, y) in month_tuples):
            # Check type
            if expense and t['type'] == 'spent':
                cat = t.get('category', 'Other')
                if cat not in categories:
                    cat = 'Other'
                totals[cat] += float(t['amount'])
            elif not expense and t['type'] == 'receive':
                cat = t.get('category', 'Other')
                if cat not in categories:
                    cat = 'Other'
                totals[cat] += float(t['amount'])

    # Build the result
    labels = list(totals.keys())
    data_values = [round(totals[c], 2) for c in labels]

    return {
        "labels": labels,
        "data": data_values
    }

def compute_bar_data(transactions, start_m, start_y, end_m, end_y, chart_type, category):
    """
    chart_type: "Income" or "Expense"
    category: a specific category (e.g. "Groceries" or "Salary")
    
    Returns:
    {
      "labels": ["01-2023", "02-2023", ...],
      "data": [100.0, 200.0, ...]
    }
    """
    is_expense = (chart_type.lower() == "expense")
    txn_type = 'spent' if is_expense else 'receive'

    months = generate_month_range(start_m, start_y, end_m, end_y)
    labels = []
    data_list = []

    for (m, y) in months:
        label_str = f"{m:02d}-{y}"
        labels.append(label_str)

        monthly_total = 0.0

        for t in transactions:
            (dd, mm, yyyy) = parse_full_date(t.get('date', '01-01-1970'))
            if mm == m and yyyy == y and t['type'] == txn_type:
                # Only sum if category matches
                if t.get('category') == category:
                    monthly_total += float(t['amount'])

        data_list.append(round(monthly_total, 2))

    return {
        "labels": labels,
        "data": data_list
    }
