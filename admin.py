from user import User
from validators import require_non_negative_int, require_positive_number


class Admin(User):
    """کلاس ادمین"""
    
    def __init__(self, username, password, balance=0):
        super().__init__(username, password, balance, "admin")

    def add_product(self, products, product):
        """اضافه کردن محصول جدید"""
        products.append(product)

    def remove_product(self, products, product):
        """حذف محصول"""
        if product in products:
            products.remove(product)

    def edit_price(self, product, new_price):
        """ویرایش قیمت"""
        product.price = require_positive_number(new_price, "Price")

    def edit_stock(self, product, new_stock):
        """ویرایش موجودی"""
        product.stock = require_non_negative_int(new_stock, "Stock")

    def set_discount(self, product, discount_percent):
        """تنظیم تخفیف"""
        product.set_discount(discount_percent)

    def edit_description(self, product, description):
        """ویرایش توضیح محصول"""
        product.description = str(description).strip()

    def set_image(self, product, image_path):
        """تنظیم تصویر محصول"""
        product.image_path = str(image_path).strip()

    def view_orders(self, orders):
        """مشاهده سفارش‌ها"""
        return list(orders)

    def get_sales_report(self, orders, date_filter=None):
        """گزارش فروش"""
        if date_filter:
            return [
            order for order in orders
            if order.date.startswith(date_filter)
            ]

        return list(orders)


