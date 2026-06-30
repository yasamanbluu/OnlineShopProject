from datetime import datetime
from validators import require_non_negative_number, require_positive_int, require_text


class Order:
    """کلاس سفارش"""
    
    def __init__(self, username, product, quantity, date=None):
        username = require_text(username, "Username")
        quantity = require_positive_int(quantity, "Quantity")
        product_id = require_text(product.product_id, "Product id")
        total_price = require_non_negative_number(
            product.final_price() * quantity,
            "Total price",
        )

        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            date = require_text(date, "Date")

        product.decrease_stock(quantity)

        self.username = username
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price
        self.date = date

    def to_csv_row(self):
        return {
            "username": self.username,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "date": self.date,
        }
