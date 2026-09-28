# Personal Expense Tracker

A command-line Python application that helps a user record daily expenses,
set category-wise monthly budgets, and view spending reports — including
an exported bar chart.

Built as a "Build Your Own Project" submission for **Problem Solving and
Python Programming (PSPP)**, applying core course concepts: top-down
modular design, functions, control flow, data structures (lists/dicts),
file handling, and basic algorithms (searching, filtering, aggregation).

## Overview 

Manually tracking daily spending in a notebook or random notes app makes
it hard to know where money is going each month. This tool gives a
simple, structured way to log expenses, set a budget per category, and
instantly see a breakdown of spending — all from the terminal, with data
saved locally as JSON so nothing is lost between sessions.

## Features

- **User accounts** — simple username + PIN login (PIN is hashed, never stored in plain text); each user's expenses and budgets are kept fully separate from every other user's
- **Expense management (CRUD)** — add, view, update, and delete expense entries
- **Category budgets** — set a monthly budget per category and get an alert when you're close to/over it
- **Reports & analytics** — total spend, spend-by-category, spend-by-month, and an exported PNG bar chart
- **Input validation** — rejects invalid amounts, dates, and categories with clear error messages
- **Local JSON persistence** — human-readable storage with automatic backup on every save
- **Unit tested** — 14 automated tests covering validation, CRUD logic, and per-user data isolation

## Technologies / Tools Used

- Python 3
- Standard library: `json`, `hashlib`, `uuid`, `datetime`, `unittest`
- `matplotlib` for chart export
- Git / GitHub for version control

## Project Structure

```
expense_tracker/
├── main.py                    # Entry point / menu-driven CLI (controller)
├── config.py                  # Constants: file paths, categories, formats
├── models.py                  # Expense data model (class)
├── data_handler.py            # JSON persistence layer
├── expense_manager.py         # Expense CRUD operations
├── budget_manager.py          # Budget setting & tracking
├── report_generator.py        # Summaries + chart export
├── auth.py                    # Username/PIN authentication
├── utils.py                   # Input validation & helper functions
├── data/                      # JSON data files (created/used at runtime)
├── diagrams/                  # Architecture / UML / ER diagrams
├── tests/
│   └── test_expense_manager.py
└── README.md
```

## Steps to Install & Run

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd expense_tracker
   ```

2. **Install dependencies**
   ```bash
   pip install matplotlib
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **First-time use**: choose option `2) Register` to create a username + PIN,
   then log in and use the menu to add expenses, set budgets, and view reports.

## Instructions for Testing

Run the automated unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

This runs 14 tests covering input validation (amount/date/category checks),
expense CRUD operations (add, update, delete, filter by category/month), and
per-user data isolation (one user can never see, edit, or delete another
user's expenses).

## Non-Functional Requirements

| Requirement       | How it's addressed |
|--------------------|--------------------|
| Performance        | In-memory list operations for a single user's data; JSON I/O only on save/load, not per-operation |
| Security            | PINs are SHA-256 hashed before storage; input is validated before it reaches storage |
| Usability           | Clear numbered menus, category picklists (no free typing of categories), descriptive error messages |
| Reliability          | Automatic backup file on every save; corrupt/missing data files fail safe instead of crashing |
| Maintainability | Modular design — each file has a single responsibility; docstrings throughout |
| Scalability          | JSON storage can be swapped for SQLite/a real DB later without changing the CRUD function signatures |

## Future Enhancements

- Export reports to PDF/CSV
- Recurring expense support
- A simple web or GUI front-end (Tkinter/Flask) on top of the existing modules
