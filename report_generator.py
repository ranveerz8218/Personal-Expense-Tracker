"""
Reporting & analytics: totals, category/month breakdowns, and an
exported bar chart. Every function takes `username` and only
summarizes that user's own expenses.
"""
import os
from collections import defaultdict

from expense_manager import get_all_expenses

def total_spent(username):
    return sum(e.amount for e in get_all_expenses(username))

def spending_by_category(username):
    totals = defaultdict(float)
    for e in get_all_expenses(username):
        totals[e.category] += e.amount
    return dict(totals)

def spending_by_month(username):
    totals = defaultdict(float)
    for e in get_all_expenses(username):
        month_key = e.date[:7] 
        totals[month_key] += e.amount
    return dict(sorted(totals.items()))

def print_summary(username):
    expenses = get_all_expenses(username)
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\nTotal expenses recorded : {len(expenses)}")
    print(f"Total amount spent      : Rs.{total_spent(username):.2f}\n")

    print("Spending by category:")
    for category, amount in spending_by_category(username).items():
        print(f"  {category:<13}: Rs.{amount:.2f}")

    print("\nSpending by month:")
    for month, amount in spending_by_month(username).items():
        print(f"  {month}: Rs.{amount:.2f}")

def export_category_chart(username, output_path=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = spending_by_category(username)
    if not data:
        print("No data to chart yet.")
        return None

    if output_path is None:
        output_path = f"data/category_chart_{username}.png"

    categories = list(data.keys())
    amounts = list(data.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts, color="#4C72B0")
    plt.title(f"Spending by Category — {username}")
    plt.xlabel("Category")
    plt.ylabel("Amount (Rs.)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    return output_path
