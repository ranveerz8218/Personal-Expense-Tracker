"""
Core CRUD operations for expenses. Works on Expense objects
(models.py) and persists them via data_handler.py.
"""


from models import Expense
from data_handler import load_expenses, save_expenses


def add_expense(username, amount, category, description, date=None):
    
    expenses = load_expenses()
    expense = Expense(amount, category, description, owner=username, date=date)
    expenses.append(expense.to_dict())
    save_expenses(expenses)
    return expense


def get_all_expenses(username):
    
    return [Expense.from_dict(e) for e in load_expenses() if e.get("owner") == username]


def get_expense_by_id(username, expense_id):

    for e in load_expenses():
        if e["id"] == expense_id and e.get("owner") == username:
            return Expense.from_dict(e)
    return None


def update_expense(username, expense_id, amount=None, category=None, description=None, date=None):
   
    expenses = load_expenses()
    for e in expenses:
        if e["id"] == expense_id and e.get("owner") == username:
            if amount is not None:
                e["amount"] = float(amount)
            if category is not None:
                e["category"] = category
            if description is not None:
                e["description"] = description
            if date is not None:
                e["date"] = date
            save_expenses(expenses)
            return True
    return False


def delete_expense(username, expense_id):
    
    expenses = load_expenses()
    filtered = [e for e in expenses if not (e["id"] == expense_id and e.get("owner") == username)]
    if len(filtered) == len(expenses):
        return False
    save_expenses(filtered)
    return True


def filter_by_category(username, category):
    return [e for e in get_all_expenses(username) if e.category == category]


def filter_by_month(username, year, month):
    """year, month are integers, e.g. 2026, 9"""
    prefix = f"{year:04d}-{month:02d}"
    return [e for e in get_all_expenses(username) if e.date.startswith(prefix)]
