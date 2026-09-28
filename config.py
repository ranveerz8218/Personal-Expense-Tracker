"""
Central place for constants used across the Expense Tracker project.
Keeping constants here (instead of hard-coding them everywhere) makes
the project easier to maintain and modify.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "data", "expenses.json")
BUDGET_FILE = os.path.join(BASE_DIR, "data", "budgets.json")
USER_FILE = os.path.join(BASE_DIR, "data", "users.json")
BACKUP_FILE = os.path.join(BASE_DIR, "data", "expenses_backup.json")

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Education",
    "Other",
]

DATE_FORMAT = "%Y-%m-%d"

BUDGET_ALERT_THRESHOLD = 90 
