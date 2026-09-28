"""
test_expense_manager.py
-------------------------
Basic unit tests for the expense_manager and utils modules, using
Python's built-in unittest framework. Run with:

    python -m unittest discover -s tests -v

(run from the project root, expense_tracker/)

These tests also cover the per-user data isolation fix: two different
usernames must never see or modify each other's expenses.
"""

import os
import sys
import unittest

# Allow importing modules from the project root when running tests directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
# Redirect data files to a temporary test location so tests never touch real data
config.DATA_FILE = os.path.join(config.BASE_DIR, "tests", "test_expenses.json")
config.BACKUP_FILE = os.path.join(config.BASE_DIR, "tests", "test_expenses_backup.json")

import expense_manager as em
from utils import is_valid_amount, is_valid_date, is_valid_category


class TestValidation(unittest.TestCase):
    def test_valid_amount(self):
        self.assertTrue(is_valid_amount("100"))
        self.assertTrue(is_valid_amount(49.5))

    def test_invalid_amount(self):
        self.assertFalse(is_valid_amount("-5"))
        self.assertFalse(is_valid_amount("abc"))
        self.assertFalse(is_valid_amount(""))

    def test_valid_date(self):
        self.assertTrue(is_valid_date("2026-09-27"))

    def test_invalid_date(self):
        self.assertFalse(is_valid_date("27-09-2026"))
        self.assertFalse(is_valid_date("not-a-date"))

    def test_valid_category(self):
        self.assertTrue(is_valid_category("Food"))
        self.assertFalse(is_valid_category("Not A Category"))


class TestExpenseCRUD(unittest.TestCase):
    def setUp(self):
        # Start each test with a clean slate
        if os.path.exists(config.DATA_FILE):
            os.remove(config.DATA_FILE)

    def tearDown(self):
        if os.path.exists(config.DATA_FILE):
            os.remove(config.DATA_FILE)
        if os.path.exists(config.BACKUP_FILE):
            os.remove(config.BACKUP_FILE)

    def test_add_and_get_expense(self):
        expense = em.add_expense("alice", 150, "Food", "Groceries", "2026-09-01")
        all_expenses = em.get_all_expenses("alice")
        self.assertEqual(len(all_expenses), 1)
        self.assertEqual(all_expenses[0].amount, 150)
        self.assertEqual(all_expenses[0].id, expense.id)

    def test_update_expense(self):
        expense = em.add_expense("alice", 100, "Travel", "Bus fare", "2026-09-02")
        ok = em.update_expense("alice", expense.id, amount=120)
        self.assertTrue(ok)
        updated = em.get_expense_by_id("alice", expense.id)
        self.assertEqual(updated.amount, 120)

    def test_delete_expense(self):
        expense = em.add_expense("alice", 50, "Other", "Misc", "2026-09-03")
        ok = em.delete_expense("alice", expense.id)
        self.assertTrue(ok)
        self.assertIsNone(em.get_expense_by_id("alice", expense.id))

    def test_delete_nonexistent_expense(self):
        self.assertFalse(em.delete_expense("alice", "doesnotexist"))

    def test_filter_by_category(self):
        em.add_expense("alice", 10, "Food", "Snack", "2026-09-04")
        em.add_expense("alice", 20, "Travel", "Cab", "2026-09-04")
        food_expenses = em.filter_by_category("alice", "Food")
        self.assertEqual(len(food_expenses), 1)
        self.assertEqual(food_expenses[0].category, "Food")

    def test_filter_by_month(self):
        em.add_expense("alice", 10, "Food", "Snack", "2026-09-05")
        em.add_expense("alice", 20, "Food", "Dinner", "2026-08-15")
        september = em.filter_by_month("alice", 2026, 9)
        self.assertEqual(len(september), 1)


class TestUserDataIsolation(unittest.TestCase):
    """Regression tests for the bug where all users shared one expense pool."""

    def setUp(self):
        if os.path.exists(config.DATA_FILE):
            os.remove(config.DATA_FILE)

    def tearDown(self):
        if os.path.exists(config.DATA_FILE):
            os.remove(config.DATA_FILE)
        if os.path.exists(config.BACKUP_FILE):
            os.remove(config.BACKUP_FILE)

    def test_users_do_not_see_each_others_expenses(self):
        em.add_expense("alice", 100, "Food", "Alice's lunch", "2026-09-01")
        em.add_expense("bob", 200, "Travel", "Bob's cab", "2026-09-01")

        alice_expenses = em.get_all_expenses("alice")
        bob_expenses = em.get_all_expenses("bob")

        self.assertEqual(len(alice_expenses), 1)
        self.assertEqual(len(bob_expenses), 1)
        self.assertEqual(alice_expenses[0].description, "Alice's lunch")
        self.assertEqual(bob_expenses[0].description, "Bob's cab")

    def test_user_cannot_update_another_users_expense(self):
        expense = em.add_expense("alice", 100, "Food", "Alice's lunch", "2026-09-01")
        ok = em.update_expense("bob", expense.id, amount=999)
        self.assertFalse(ok)
        # Confirm Alice's data is untouched
        self.assertEqual(em.get_expense_by_id("alice", expense.id).amount, 100)

    def test_user_cannot_delete_another_users_expense(self):
        expense = em.add_expense("alice", 100, "Food", "Alice's lunch", "2026-09-01")
        ok = em.delete_expense("bob", expense.id)
        self.assertFalse(ok)
        self.assertIsNotNone(em.get_expense_by_id("alice", expense.id))


if __name__ == "__main__":
    unittest.main()
