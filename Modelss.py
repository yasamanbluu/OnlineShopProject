from datetime import datetime

from shop.exceptions import StockError, ValidationError


def _require_text(value, field_name):
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} is required.")
    return str(value).strip()


def _require_positive_number(value, field_name):
    value = float(value)
    if value <= 0:
        raise ValidationError(f"{field_name} must be positive.")
    return value


def _require_non_negative_number(value, field_name):
    value = float(value)
    if value < 0:
        raise ValidationError(f"{field_name} cannot be negative.")
    return value


def _require_positive_int(value, field_name):
    value = int(value)
    if value <= 0:
        raise ValidationError(f"{field_name} must be positive.")
    return value


def _require_non_negative_int(value, field_name):
    value = int(value)
    if value < 0:
        raise ValidationError(f"{field_name} cannot be negative.")
    return value


class User:
    def __init__(self, username, password, balance, role):
        self.username = _require_text(username, "Username")
        self.password = _require_text(password, "Password")
        self.balance = _require_non_negative_number(balance, "Balance")
        self.role = _require_text(role, "Role").lower()

    def check_password(self, password):
        return self.password == password

    def add_balance(self, amount):
        amount = _require_positive_number(amount, "Amount")
        self.balance += amount

    def reduce_balance(self, amount):
        amount = _require_positive_number(amount, "Amount")
        if self.balance < amount:
            raise ValidationError("Balance is not enough.")
        self.balance -= amount

    def to_csv_row(self):
        return {
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "role": self.role,
        }


class Customer(User):
    def __init__(self, username, password, balance=0):
        super().__init__(username, password, balance, "customer")

    def buy(self, amount):
        self.reduce_balance(amount)


class Admin(User):
    def __init__(self, username, password, balance=0):
        super().__init__(username, password, balance, "admin")

    def can_manage_products(self):
        return True


class Product:
    def __init__(self, product_id, name, price, stock, category, discount_percent=0):
        self.product_id = _require_text(product_id, "Product id")
        self.name = _require_text(name, "Product name")
        self.price = _require_positive_number(price, "Price")
        self.stock = _require_non_negative_int(stock, "Stock")
        self.category = _require_text(category, "Category")
        self.discount_percent = _require_non_negative_number(
            discount_percent,
            "Discount percent"
        )

        if self.discount_percent > 100:
            raise ValidationError("Discount percent cannot be more than 100.")

    def increase_stock(self, quantity):
        quantity = _require_positive_int(quantity, "Quantity")
        self.stock += quantity

    def decrease_stock(self, quantity):
        quantity = _require_positive_int(quantity, "Quantity")
        if self.stock < quantity:
            raise StockError("Not enough stock.")
        self.stock -= quantity

    def final_price(self):
        discount_amount = self.price * self.discount_percent / 100
        return self.price - discount_amount

    def to_csv_row(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "discount_percent": self.discount_percent,
        }


class Order:
    def __init__(self, username, product_id, quantity, total_price, date):
        self.username = _require_text(username, "Username")
        self.product_id = _require_text(product_id, "Product id")
        self.quantity = _require_positive_int(quantity, "Quantity")
        self.total_price = _require_positive_number(total_price, "Total price")
        self.date = _require_text(date, "Date")

    @classmethod
    def create(cls, username, product, quantity):
        quantity = _require_positive_int(quantity, "Quantity")
        product.decrease_stock(quantity)

        return cls(
            username,
            product.product_id,
            quantity,
            product.final_price() * quantity,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def to_csv_row(self):
        return {
            "username": self.username,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "date": self.date,
        }