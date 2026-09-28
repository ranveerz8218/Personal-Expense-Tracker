"""
Lets each user set a monthly budget per category and checks how much
of that budget has been used. This is the second major functional
module of the project.
"""

from data_handler import load_budgets, save_budgets
from expense_manager import get_all_expenses
from config import BUDGET_ALERT_THRESHOLD


def set_budget(username, category, amount):
    budgets = load_budgets()
    user_budgets = budgets.setdefault(username, {})
    user_budgets[category] = float(amount)
    save_budgets(budgets)


def get_budgets(username):
    budgets = load_budgets()
    return budgets.get(username, {})


def check_budget_status(username, year, month):
    
    user_budgets = get_budgets(username)
    expenses = get_all_expenses(username)
    prefix = f"{year:04d}-{month:02d}"

    spent_by_category = {}
    for e in expenses:
        if e.date.startswith(prefix):
            spent_by_category[e.category] = spent_by_category.get(e.category, 0) + e.amount

    report = []
    for category, budget in user_budgets.items():
        spent = spent_by_category.get(category, 0)
        percent = (spent / budget * 100) if budget > 0 else 0
        report.append({
            "category": category,
            "spent": spent,
            "budget": budget,
            "percent_used": round(percent, 1),
            "alert": percent >= BUDGET_ALERT_THRESHOLD,
        })
    return report
