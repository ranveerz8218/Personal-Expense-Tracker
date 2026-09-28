"""
Very simple username + PIN authentication so each user's expenses stay
separate. 
"""

import hashlib

from data_handler import load_users, save_users


def _hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def register(username, pin):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = _hash_pin(pin)
    save_users(users)
    return True, "Registration successful."


def login(username, pin):
    users = load_users()
    if username not in users:
        return False, "User not found."
    if users[username] != _hash_pin(pin):
        return False, "Incorrect PIN."
    return True, "Login successful."


def login_menu():
    print("=== Welcome to Personal Expense Tracker ===")
    while True:
        choice = input("1) Login  2) Register  3) Exit\nChoose: ").strip()
        if choice == "1":
            username = input("Username: ").strip()
            pin = input("PIN: ").strip()
            ok, msg = login(username, pin)
            print(msg)
            if ok:
                return username
        elif choice == "2":
            username = input("Choose a username: ").strip()
            pin = input("Choose a 4+ digit PIN: ").strip()
            if len(pin) < 4:
                print("PIN must be at least 4 characters.")
                continue
            ok, msg = register(username, pin)
            print(msg)
        elif choice == "3":
            return None
        else:
            print("Invalid choice.")
