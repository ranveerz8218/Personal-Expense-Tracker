# Problem Statement

People who track expenses using notebooks, memory, or scattered notes-app
entries lose visibility into where their money goes each month. Without a
structured, searchable record, it's hard to answer simple questions like
"how much did I spend on food this month?" or "am I over my travel budget?"

This project implements a **Personal Expense Tracker**: a modular,
menu-driven Python command-line application that lets a user log expenses,
organize them by category, set monthly budgets, and generate spending
reports — applying core Problem Solving and Python Programming concepts
(top-down design, functions, control flow, data structures, file handling)
to a real, everyday problem.

## Scope of the Project

- Single-machine, command-line (CLI) application — no web server or GUI
- Local JSON files as the data store (no external database required)
- Supports multiple user accounts (simple username + PIN), each sharing
  the same category list defined in `config.py`
- Focused on personal/individual finance tracking, not multi-currency,
  tax, or business accounting features

## Target Users

- Students and individuals who want a lightweight, free way to track
  personal daily/monthly expenses without installing a heavy finance app
- Anyone comfortable using a command-line interface

## High-Level Features

1. **Authentication** — register and log in with a username and PIN
2. **Expense Management** — add, view, update, and delete expense records
   (amount, category, description, date)
3. **Budget Management** — set a monthly budget per category and check
   how much of it has been used, with an alert near/over the limit
4. **Reporting & Analytics** — view total spend, category-wise and
   month-wise breakdowns, and export a bar chart (PNG) of spending by
   category
