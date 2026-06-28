import tkinter as tk
from gui_complete_login import LoginWindow
from gui_complete_customer import CustomerPanel
from gui_complete_admin import AdminPanel
from database import Database


class OnlineShop:
    """main program managing routing"""

    def __init__(self, root):
        self.root = root
        self.root.title("online shop")
        self.root.geometry("900x700")

        #load database
        try:
            self.db = Database("data")
            self.products = self.db.load_products()
            self.reviews = self.db.load_reviews()
            self.users = self.db.load_users()
            self.orders = self.db.load_orders()
            print(f"loaded {len(self.products)} products, {len(self.reviews)} reviews, {len(self.orders)} orders")
        except Exception as e:
            print(f"error loading database: {e}")
            self.products = []
            self.reviews = []
            self.users = {}
            self.orders = []

        #keep references to avoid garbage collection
        self.login_window = None
        self.customer_window = None
        self.admin_window = None

        self.show_login()

    def show_login(self):
        """show login page"""
        self.clear()

        #reload data from csv (in case admin made changes)
        try:
            self.products = self.db.load_products()
            self.reviews = self.db.load_reviews()
            self.orders = self.db.load_orders()
            print(f"reloaded: {len(self.products)} products with latest discounts")
        except Exception as e:
            print(f"could not reload: {e}")

        self.login_window = LoginWindow(self.root, self.on_login)

    def on_login(self, username, role):
        """after successful login"""
        print(f"login successful: {username} ({role})")
        if role == "admin":
            self.show_admin(username)
        else:
            self.show_customer(username)

    def show_customer(self, username):
        """show customer panel"""
        self.clear()
        self.customer_window = CustomerPanel(
            self.root,
            username,
            self.show_login,
            self.products,  #latest products with discounts
            self.reviews,
            self.db
        )

    def show_admin(self, username):
        """show admin panel"""
        self.clear()
        self.admin_window = AdminPanel(
            self.root,
            username,
            self.show_login,
            self.products,  #latest products
            self.orders,
            self.db
        )

    def clear(self):
        """clear widgets"""
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineShop(root)
    root.mainloop()