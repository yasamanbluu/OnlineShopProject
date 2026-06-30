from exceptions import InvalidDataError
from validators import require_non_negative_number, require_positive_number, require_text


class User:
    """کلاس کاربر """
    def __init__(self, username, password, balance, role):
        self.username = require_text(username, "Username")
        self.password = require_text(password, "Password")
        self.balance = require_non_negative_number(balance, "Balance")
        self.role = require_text(role, "Role").lower()

    def check_password(self, password):
        return self.password == password

    def add_balance(self, amount):
        amount = require_positive_number(amount, "Amount")
        self.balance += amount

    def reduce_balance(self, amount):
        amount = require_positive_number(amount, "Amount")
        if self.balance < amount:
            raise InvalidDataError("Balance is not enough.")
        self.balance -= amount

    def to_csv_row(self):
        return {
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "role": self.role,
        }
