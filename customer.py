#from exceptions import OutOfStockError, ValidationError
from exceptions import OutOfStockError, InvalidDataError, InsufficientBalanceError

from order import Order
from user import User
from validators import require_positive_int


class Customer(User):
    """کلاس مشتری"""
    
    def __init__(self, username, password, balance=0):
        super().__init__(username, password, balance, "customer")
        self.cart = []

    def view_products(self, products):
        return list(products)

    def search_products(self, products, keyword="", category=""):
        """جستجو محصول"""
        keyword = str(keyword).strip().lower()
        category = str(category).strip().lower()
        found_products = []

        for product in products:
            matches_keyword = (
                not keyword
                or keyword in product.name.lower()
                or keyword in product.product_id.lower()
            )
            matches_category = not category or category == product.category.lower()

            if matches_keyword and matches_category:
                found_products.append(product)

        return found_products

    def buy(self, product, quantity, date=None):
        """خرید مستقیم"""
        quantity = require_positive_int(quantity, "Quantity")

        if product.stock < quantity:
            raise OutOfStockError("Not enough stock.")

        total_price = product.final_price() * quantity

        if self.balance < total_price:
            raise InsufficientBalanceError("Balance is not enough.")

        order = Order(self.username, product, quantity, date)

        if total_price > 0:
            self.reduce_balance(total_price)

        return order

    def add_to_cart(self, product, quantity):
        """اضافه کردن به سبد"""
        quantity = require_positive_int(quantity, "Quantity")

        if product.stock < quantity:
            raise OutOfStockError("Not enough stock.")

        for item in self.cart:
            if item["product"] is product:
                new_quantity = item["quantity"] + quantity

                if product.stock < new_quantity:
                    raise OutOfStockError("Not enough stock.")

                item["quantity"] = new_quantity
                return

        self.cart.append({
            "product": product,
            "quantity": quantity,
        })

    def remove_from_cart(self, product):
        """حذف از سبد"""
        self.cart = [
            item for item in self.cart
            if item["product"] is not product
        ]

    def clear_cart(self):
        """خالی کردن سبد"""
        self.cart.clear()

    def cart_total(self):
        """محاسبه قیمت کل سبد"""
        total = 0

        for item in self.cart:
            product = item["product"]
            quantity = item["quantity"]
            total += product.final_price() * quantity

        return total

    def checkout(self, date=None):
        """تکمیل خرید"""
        if not self.cart:
            raise InvalidDataError("Cart is empty.")

        for item in self.cart:
            product = item["product"]
            quantity = item["quantity"]

            if product.stock < quantity:
                raise OutOfStockError("Not enough stock.")

        total_price = self.cart_total()

        if self.balance < total_price:
            raise InsufficientBalanceError("Balance is not enough.")

        orders = []

        for item in self.cart:
            product = item["product"]
            quantity = item["quantity"]
            orders.append(Order(self.username, product, quantity, date))

        self.reduce_balance(total_price)
        self.clear_cart()

        return orders
