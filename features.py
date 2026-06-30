from datetime import datetime
from product import Product
from order import Order


class ShoppingCart():
    """مدیریت سبد خرید"""

    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity=1):
        """اضافه کردن محصول"""

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if product.product_id in self.items:
            self.items[product.product_id]["quantity"] += quantity
        else:
            self.items[product.product_id] = {
                "product": product,
                "quantity": quantity
            }

    def remove_item(self, product_id):
        """حذف محصول"""

        if product_id in self.items:
            del self.items[product_id]

    def get_total(self):
        """محاسبه قیمت کل"""

        total = 0

        for item in self.items.values():
            total += item["product"].final_price() * item["qty"]

        return total

    def get_item_count(self):
        """تعداد محصولات"""

        return len(self.items)

    def clear(self):
        """خالی کردن سبد"""

        self.items.clear()


class DiscountSystem:
    """سیستم تخفیف"""

    def apply_discount(self, product, discount_percent):
        """اعمال تخفیف بر محصول"""
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        product.set_discount(discount_percent)

    def calculate_savings(self, original_price, discount_percent):
        """محاسبه مقدار صرفه‌جویی"""
        return original_price * discount_percent / 100

    def get_discounted_price(self, original_price, discount_percent):
        """دریافت قیمت با تخفیف"""
        return original_price * (100 - discount_percent) / 100

    def bulk_apply_discount(self, products, discount_map):
        """اعمال تخفیف دسته‌ای {product_id: discount_percent}"""
        for product in products:
            if product.product_id in discount_map:
                product.set_discount(discount_map[product.product_id])


class ReviewSystem:
    """سیستم امتیاز و نظر"""

    def get_product_rating(self, comments):
        """محاسبه امتیاز متوسط محصول"""
        if not comments:
            return 0

        ratings = [comment.rating for comment in comments]
        return sum(ratings) / len(ratings)

    def get_review_count(self, comments):
        """تعداد نظرات"""
        return len(comments)

    def get_reviews_by_rating(self, comments, rating):
        """دریافت نظرات با امتیاز خاص"""
        return [c for c in comments if c.get("rating") == rating]

    def get_positive_reviews(self, comments):
        """نظرات مثبت (امتیاز 4-5)"""
        return [c for c in comments if c.get("rating", 0) >= 4]

    def get_negative_reviews(self, comments):
        """نظرات منفی (امتیاز 1-2)"""
        return [c for c in comments if c.get("rating", 0) <= 2]


class SalesReport:
    """گزارش فروش"""

    def get_total_sales(self, orders):
        """کل فروش"""
        return sum(order.get("total_price", 0) for order in orders)

    def get_sales_by_date(self, orders, date):
        """فروش یک تاریخ خاص"""
        day_orders = [
            order for order in orders
            if order.get("date", "").startswith(date)
        ]

        return sum(order.get("total_price", 0) for order in day_orders)

    def get_sales_between_dates(self, orders, start_date, end_date):
        """گزارش فروش بین دو تاریخ"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        total = 0
        for order in orders:
            order_date = datetime.strptime(order.get("date"), "%Y-%m-%d")
            if start <= order_date <= end:
                total += order.get("total_price", 0)
        return total

    def get_sales_by_product(self, orders):
        """فروش به تفکیک محصول"""
        sales_map = {}
        for order in orders:
            product_id = order.get("product_id")
            if product_id:
                if product_id not in sales_map:
                    sales_map[product_id] = 0
                sales_map[product_id] += order.get("total_price", 0)
        return sales_map

    def get_sales_by_user(self, orders):
        """فروش به تفکیک کاربر"""
        sales_map = {}
        for order in orders:
            username = order.get("username")
            if username:
                if username not in sales_map:
                    sales_map[username] = 0
                sales_map[username] += order.get("total_price", 0)
        return sales_map

    def get_top_products(self, orders, limit=5):
        """محصولات پرفروش"""
        sales = self.get_sales_by_product(orders)

        return sorted(
            sales.items(),
            key=lambda item: item[1],
            reverse=True
        )[:limit]

    def get_sales_count(self, orders):
        return len(orders)

    def get_average_order_value(self, orders):
        if not orders:
            return 0
        return self.get_total_sales(orders) / len(orders)


class SearchFilter:
    """جستجو و فیلتر"""

    def search_by_name(self, products, keyword):
        """جستجو بر اساس نام"""
        keyword = str(keyword).lower()

        return [product for product in products if keyword in product.name.lower()]

    def search_by_category(self, products, category):
        """فیلتر بر اساس دسته‌بندی"""
        category = str(category).lower()
        return [product for product in products if product.category.lower() == category]

    def search_by_price_range(self, products, min_price, max_price):
        """فیلتر بر اساس قیمت"""
        return [product for product in products if min_price <= product.price <= max_price]

    def advanced_search(self, products, keyword="", category="", min_price=0, max_price=float("inf")):

        results = products
        if keyword:
            results = self.search_by_name(results, keyword)
        if category:
            results = self.search_by_category(results, category)
        results = self.search_by_price_range(results, min_price, max_price)
        return results
