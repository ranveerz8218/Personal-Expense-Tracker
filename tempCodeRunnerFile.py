"""
Entry point of the app. Shows the CLI menu and routes each choice to
the manager modules, passing `username` so each user sees only their
own data.
"""

from datetime import datetime

import auth
import expense_manager as em
import budget_manager as bm
import report_generator as rg
from utils import is_valid_amount, is_valid_date, choose_category, print_divider
from config import DATE_FORMAT


def add_expense_flow(username):
    print_divider()
    amount = input("Amount spent (Rs.): ").strip()
    if not is_valid_amount(amount):
        print("Invalid amount. Must be a positive number.")
        return
    category = choose_category()
    description = input("Description (e.g. 'Lunch with friends'): ").strip()
    date = input(f"Date [{DATE_FORMAT}] (leave blank for today): ").strip()
    if date and not is_valid_date(date):
        print("Invalid date format.")
        return
    expense = em.add_expense(username, amount, category, description, date or None)
    print(f"Added: {expense}")


def view_expenses_flow(username):
    print_divider()
    expenses = em.get_all_expenses(username)
    if not expenses:
        print("No expenses yet.")
        return
    for e in expenses:
        print(e)


def update_expense_flow(username):
    print_divider()
    expense_id = input("Enter expense ID to update: ").strip()
    existing = em.get_expense_by_id(username, expense_id)
    if not existing:
        print("Expense not found.")
        return
    print(f"Current: {existing}")
    amount = input("New amount (blank to keep): ").strip()
    description = input("New description (blank to keep): ").strip()
    date = input("New date (blank to keep): ").strip()

    if amount and not is_valid_amount(amount):
        print("Invalid amount, update cancelled.")
        return
    if date and not is_valid_date(date):
        print("Invalid date, update cancelled.")
        return

    ok = em.update_expense(
        username,
        expense_id,
        amount=amount or None,
        description=description or None,
        date=date or None,
    )
    print("Updated." if ok else "Update failed.")


def delete_expense_flow(username):
    print_divider()
    expense_id = input("Enter expense ID to delete: ").strip()
    ok = em.delete_expense(username, expense_id)
    print("Deleted." if ok else "Expense not found.")


def budget_flow(username):
    print_divider()
    print("1) Set a category budget  2) View budget status this month")
    choice = input("Choose: ").strip()
    if choice == "1":
        category = choose_category()
        amount = input("Monthly budget amount (Rs.): ").strip()
        if not is_valid_amount(amount):
            print("Invalid amount.")
            return
        bm.set_budget(username, category, amount)
        print(f"Budget for {category} set to Rs.{float(amount):.2f}")
    elif choice == "2":
        now = datetime.now()
        status = bm.check_budget_status(username, now.year, now.month)
        if not status:
            print("No budgets set yet.")
            return
        for row in status:
            flag = "  ALERT: near/over budget!" if row["alert"] else ""
            print(f"  {row['category']:<13}: Rs.{row['spent']:.2f} / Rs.{row['budget']:.2f} "
                  f"({row['percent_used']}%){flag}")


def report_flow(username):
    print_divider()
    rg.print_summary(username)
    choice = input("\nExport category spending chart as PNG? (y/n): ").strip().lower()
    if choice == "y":
        path = rg.export_category_chart(username)
        if path:
            print(f"Chart saved to: {path}")


def main_menu(username):
    menu = """
=========== Personal Expense Tracker ===========
1. Add expense
2. View all expenses
3. Update an expense
4. Delete an expense
5. Budget management
6. Reports & analytics
7. Logout / Exit
==================================================
"""
    while True:
        print(menu)
        choice = input(f"({username}) Choose an option: ").strip()
        try:
            if choice == "1":
                add_expense_flow(username)
            elif choice == "2":
                view_expenses_flow(username)
            elif choice == "3":
                update_expense_flow(username)
            elif choice == "4":
                delete_expense_flow(username)
            elif choice == "5":
                budget_flow(username)
            elif choice == "6":
                report_flow(username)
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid option, please choose 1-7.")
        except Exception as exc:
            print(f"Something went wrong: {exc}")


if __name__ == "__main__":
    user = auth.login_menu()
    if user:
        main_menu(user)
