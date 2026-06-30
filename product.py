#from exceptions import StockError, ValidationError
from exceptions import OutOfStockError, InvalidDataError, InsufficientBalanceError

from validators import (
    require_non_negative_int,
    require_non_negative_number,
    require_positive_int,
    require_positive_number,
    require_text,
)


class Product:
    """کلاس محصول """
    def __init__(self, product_id, name, price, stock, category, discount_percent=0, image_path="", description=""):
        self.product_id = require_text(product_id, "Product id")
        self.name = require_text(name, "Product name")
        self.price = require_positive_number(price, "Price")
        self.stock = require_non_negative_int(stock, "Stock")
        self.category = require_text(category, "Category")
        self.discount_percent = 0
        self.set_discount(discount_percent)
        self.image_path = image_path  
        self.description = description  

    def increase_stock(self, quantity):
        quantity = require_positive_int(quantity, "Quantity")
        self.stock += quantity

    def decrease_stock(self, quantity):
        quantity = require_positive_int(quantity, "Quantity")
        if self.stock < quantity:
            
            raise OutOfStockError("Not enough stock.")
        self.stock -= quantity

    def set_discount(self, discount_percent):
        discount_percent = require_non_negative_number(discount_percent, "Discount percent")
        if discount_percent > 100:
            raise InvalidDataError("Discount percent cannot be more than 100.")
        self.discount_percent = discount_percent

    def final_price(self):
        return self.price * (100 - self.discount_percent) / 100

    def to_csv_row(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "discount_percent": self.discount_percent,
            "image_path": self.image_path,
            "description": self.description,
        }
