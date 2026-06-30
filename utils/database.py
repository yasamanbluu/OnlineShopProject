import csv
import os
from user import User
from product import Product
from comment import Comment


class Database:
    """کلاس Database - برای خواندن و نوشتن فایل‌های CSV واقعی"""
    
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.users_file = os.path.join(data_folder, "users.csv")
        self.products_file = os.path.join(data_folder, "products.csv")
        self.orders_file = os.path.join(data_folder, "orders.csv")
        self.reviews_file = os.path.join(data_folder, "reviews.csv")  # نه comments!
    
    # ===== USERS =====
    def load_users(self):
        """خواندن تمام کاربران از users.csv"""
        users = {}
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # تبدیل balance به عدد (حذف کاما)
                    balance = float(row['balance'].replace(',', ''))
                    user = User(
                        username=row['username'],
                        password=row['password'],
                        balance=balance,
                        role=row['role']
                    )
                    users[row['username']] = user
        except FileNotFoundError:
            print(f"Warning: {self.users_file} not found")
            return {}
        return users
    
    def save_users(self, users):
        """نوشتن کاربران در users.csv"""
        with open(self.users_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['username', 'password', 'balance', 'role']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for user in users.values():
                row = user.to_csv_row()
                # فرمت قیمت‌های بزرگ با کاما
                if row['balance'] > 999999:
                    row['balance'] = f"{int(row['balance']):,}"
                writer.writerow(row)
    
    # ===== PRODUCTS =====
    def load_products(self):
        """خواندن تمام محصولات از products.csv"""
        products = []
        try:
            with open(self.products_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # تبدیل قیمت (حذف کاما)
                    price = float(row['price'].replace(',', ''))
                    stock = int(row['stock'])
                    discount = float(row.get('discount_percent', 0))
                    
                    product = Product(
                        product_id=row['product_id'],
                        name=row['name'],
                        price=price,
                        stock=stock,
                        category=row['category'],
                        discount_percent=discount,
                        image_path=row.get('image_url', ''),
                        description=row.get('description', '')
                    )
                    products.append(product)
        except FileNotFoundError:
            print(f"Warning: {self.products_file} not found")
            return []
        return products
    
    def save_products(self, products):
        """نوشتن محصولات در products.csv"""
        with open(self.products_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['product_id', 'name', 'price', 'stock', 'category', 'description', 'image_url', 'discount_percent']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                row = product.to_csv_row()
                # تبدیل image_path به image_url
                if 'image_path' in row:
                    row['image_url'] = row.pop('image_path')
                # فرمت قیمت با کاما
                if row['price'] > 999999:
                    row['price'] = f"{int(row['price']):,}"
                writer.writerow(row)
    
    # ===== ORDERS =====
    def load_orders(self):
        """خواندن تمام سفارش‌ها از orders.csv"""
        orders = []
        try:
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    order = {
                        'username': row['username'],
                        'product_id': row['product_id'],
                        'quantity': int(row['quantity']),
                        'total_price': float(row['total_price'].replace(',', '')),
                        'discount_percent': float(row.get('discount_percent', 0)),
                        'final_price': float(row.get('final_price', row['total_price']).replace(',', '')),
                        'date': row['date']
                    }
                    orders.append(order)
        except FileNotFoundError:
            print(f"Warning: {self.orders_file} not found")
            return []
        return orders
    
    def save_order(self, order):
        """نوشتن یک سفارش جدید"""
        orders = self.load_orders()
        
        # تبدیل Order object به dictionary اگر لازمه
        if hasattr(order, 'to_csv_row'):
            order_dict = order.to_csv_row()
        else:
            order_dict = order
        
        orders.append(order_dict)
        
        with open(self.orders_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['username', 'product_id', 'quantity', 'total_price', 'discount_percent', 'final_price', 'date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for o in orders:
                row = dict(o)
                # فرمت قیمت‌ها با کاما
                if row['total_price'] > 999999:
                    row['total_price'] = f"{int(row['total_price']):,}"
                if row.get('final_price', 0) > 999999:
                    row['final_price'] = f"{int(row.get('final_price', 0)):,}"
                writer.writerow(row)
    
    # ===== REVIEWS (نه Comments!) =====
    def load_reviews(self):
        """خواندن تمام نقد و نظرات از reviews.csv"""
        reviews = []
        try:
            with open(self.reviews_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    review = {
                        'username': row['username'],
                        'product_id': row['product_id'],
                        'rating': int(row['rating']),
                        'comment': row['comment'],
                        'date': row['date']
                    }
                    reviews.append(review)
        except FileNotFoundError:
            print(f"Warning: {self.reviews_file} not found")
            return []
        return reviews
    
    def save_review(self, review):
        """نوشتن نقد و نظر جدید"""
        reviews = self.load_reviews()
        
        # تبدیل Comment object به dictionary اگر لازمه
        if hasattr(review, 'to_csv_row'):
            review_dict = review.to_csv_row()
            # تبدیل comment_text به comment
            if 'comment_text' in review_dict:
                review_dict['comment'] = review_dict.pop('comment_text')
        else:
            review_dict = review
        
        reviews.append(review_dict)
        
        with open(self.reviews_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['username', 'product_id', 'rating', 'comment', 'date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reviews)
    
    # ===== QUERIES =====
    def get_reviews_for_product(self, product_id):
        """دریافت تمام نقد و نظرات یک محصول"""
        reviews = self.load_reviews()
        return [r for r in reviews if r['product_id'] == str(product_id)]
    
    def get_user_orders(self, username):
        """دریافت تمام سفارش‌های یک کاربر"""
        orders = self.load_orders()
        return [o for o in orders if o['username'] == username]
    
    def get_orders_by_date(self, date):
        """دریافت سفارش‌های یک تاریخ"""
        orders = self.load_orders()
        return [o for o in orders if o['date'].startswith(date)]
    
    def get_user_by_username(self, username):
        """دریافت یک کاربر"""
        users = self.load_users()
        return users.get(username)
    
    def get_product_by_id(self, product_id):
        """دریافت یک محصول"""
        products = self.load_products()
        for p in products:
            if p.product_id == str(product_id):
                return p
        return None
