"""
Defines the Expense data model used throughout the application.
Using a class (instead of raw dictionaries everywhere) keeps the
data structure consistent and makes validation easier to reason about.
"""

import uuid
from datetime import datetime

from config import DATE_FORMAT


class Expense:
    def __init__(self, amount, category, description, owner, date=None, expense_id=None):
        self.id = expense_id or str(uuid.uuid4())[:8]
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.owner = owner  # username this expense belongs to
        self.date = date or datetime.now().strftime(DATE_FORMAT)

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "owner": self.owner,
            "date": self.date,
        }

    @staticmethod
    def from_dict(data):
        return Expense(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            owner=data.get("owner"),
            date=data["date"],
            expense_id=data["id"],
        )

    def __str__(self):
        return f"[{self.id}] {self.date} | {self.category:<13} | Rs.{self.amount:>10.2f} | {self.description}"
