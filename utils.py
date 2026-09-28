"""
Small, reusable helper functions used by multiple modules:
input validation, date checking, and console formatting.
Keeping these separate avoids duplicating validation logic everywhere.
"""

from datetime import datetime

from config import DATE_FORMAT, CATEGORIES


def is_valid_amount(value):
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


def is_valid_date(value):
    try:
        datetime.strptime(value, DATE_FORMAT)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_category(value):
    return value in CATEGORIES


def print_categories():
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {cat}")


def choose_category():
    print_categories()
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice, try again.")


def print_divider(char="-", length=60):
    print(char * length)
