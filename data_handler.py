"""
Handles all reading/writing of JSON data to disk.
Isolating file I/O in one module means the rest of the app never has
to worry about file paths, JSON parsing errors, or missing files
(reliability + maintainability).
"""

import json
import os
import shutil

from config import DATA_FILE, BUDGET_FILE, USER_FILE, BACKUP_FILE


def _ensure_file(path, default):
    """Create the file with default content if it doesn't already exist."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=2)


def load_expenses():
    """Load all expenses from disk. Returns [] if file is missing/corrupt."""
    _ensure_file(DATA_FILE, [])
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        
        print("Warning: expenses file was unreadable, starting with empty data.")
        return []


def save_expenses(expenses):
    """Save the full expense list to disk, keeping a backup of the previous version."""
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, BACKUP_FILE) 
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def load_budgets():
    """Load category budgets. Returns {} if none set yet."""
    _ensure_file(BUDGET_FILE, {})
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_budgets(budgets):
    os.makedirs(os.path.dirname(BUDGET_FILE), exist_ok=True)
    with open(BUDGET_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


def load_users():
    """Load registered users (used by auth.py)."""
    _ensure_file(USER_FILE, {})
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_users(users):
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)
