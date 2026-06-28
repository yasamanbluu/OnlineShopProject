import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from comment import Comment
from datetime import datetime
import os


class CustomerPanel:
    """customer panel with ability to add reviews"""

    def __init__(self, root, username, on_logout, products, reviews, database):
        self.root = root
        self.root.title("Customer Panel")
        self.root.geometry("1400x800")
        self.username = username
        self.on_logout = on_logout
        self.products = products
        self.reviews = reviews
        self.database = database

        self.cart = {}
        self.photo_cache = {}
        self.selected_product_for_review = None
        self.create_gui()

    def create_gui(self):
        """create customer interface"""

        #header
        top = tk.Frame(self.root, bg="#27ae60", height=50)
        top.pack(fill=tk.X)

        welcome = tk.Label(top, text=f"welcome {self.username}",
                           bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
        welcome.pack(side=tk.LEFT, padx=10, pady=10)

        logout = tk.Button(top, text="logout", bg="red", fg="white", command=self.on_logout)
        logout.pack(side=tk.RIGHT, padx=10, pady=10)

        #search
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar(self.root)
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="search", command=self.search_products, bg="#3498db", fg="white").pack(
            side=tk.LEFT)

        #main content
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #left: products
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="products:", font=("Arial", 12, "bold")).pack()

        canvas = tk.Canvas(left_frame, height=600, bg="white")
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.product_frame = scrollable_frame
        self.display_products(self.products)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #middle: reviews for Selected Product
        middle_frame = tk.LabelFrame(main_frame, text="add & view reviews", font=("Arial", 11, "bold"))
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)

        tk.Label(middle_frame, text="select product to review", font=("Arial", 9)).pack(pady=5)
        self.product_name_label = tk.Label(middle_frame, text="none", font=("Arial", 10, "bold"), fg="#27ae60")
        self.product_name_label.pack()

        #rating
        tk.Label(middle_frame, text="rating (1-5):", font=("Arial", 9)).pack(pady=(10, 0))
        self.rating_var = tk.IntVar(value=5)
        rating_scale = tk.Scale(middle_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=self.rating_var)
        rating_scale.pack(fill=tk.X, padx=5)

        #comment
        tk.Label(middle_frame, text="your comment:", font=("Arial", 9)).pack(pady=(10, 0))
        self.comment_text = tk.Text(middle_frame, height=6, width=25, font=("Arial", 8))
        self.comment_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        tk.Button(middle_frame, text="post review", bg="#27ae60", fg="white",
                  command=self.post_review, width=20).pack(pady=5)

        #reviews List
        tk.Label(middle_frame, text="all reviews:", font=("Arial", 9, "bold")).pack(pady=(10, 0))

        self.reviews_display = tk.Text(middle_frame, height=8, width=25, font=("Arial", 8), state=tk.DISABLED)
        self.reviews_display.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        #right: Cart
        right_frame = tk.Frame(main_frame, width=280, bg="#ecf0f1")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        tk.Label(right_frame, text="cart:", font=("Arial", 12, "bold"), bg="#ecf0f1").pack()
        self.cart_label = tk.Label(right_frame, text="empty", bg="white", height=15, width=35, justify=tk.LEFT,
                                   anchor="nw")
        self.cart_label.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)

        btn_frame = tk.Frame(right_frame, bg="#ecf0f1")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="checkout", bg="#27ae60", fg="white", command=self.checkout, width=15).pack(
            side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="clear", bg="orange", fg="white", command=self.clear_cart, width=15).pack(
            side=tk.LEFT, padx=2)

    def load_product_image(self, image_path, size=(120, 120)):
        """load product image"""
        try:
            if image_path in self.photo_cache:
                return self.photo_cache[image_path]

            if os.path.exists(image_path):
                img = Image.open(image_path)
                img.thumbnail(size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.photo_cache[image_path] = photo
                return photo
            else:
                return None
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def display_products(self, products):
        """display all products"""
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        for product in products:
            self.show_product(product)

    def show_product(self, product):
        """show one product with image"""
        frame = tk.Frame(self.product_frame, relief=tk.RAISED, bd=2, bg="white")
        frame.pack(fill=tk.X, pady=8, padx=5)

        content_frame = tk.Frame(frame, bg="white")
        content_frame.pack(fill=tk.X, padx=5, pady=5)

        #image
        img_frame = tk.Frame(content_frame, bg="white")
        img_frame.pack(side=tk.LEFT, padx=5)

        photo = self.load_product_image(product.image_path)
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack()
        else:
            tk.Label(img_frame, text="no image", bg="lightgray", width=15, height=8).pack()

        #info
        info_frame = tk.Frame(content_frame, bg="white")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(info_frame, text=product.name, font=("Arial", 11, "bold"), bg="white", fg="#27ae60").pack(anchor="w")
        tk.Label(info_frame, text=f"category: {product.category}", font=("Arial", 9), bg="white", fg="gray").pack(
            anchor="w")

        price_text = f"price: ${product.price:,.0f}"
        if product.discount_percent > 0:
            final = product.final_price()
            price_text += f" -> ${final:,.0f} (-{product.discount_percent}%)"
            tk.Label(info_frame, text=price_text, font=("Arial", 9, "bold"), bg="white", fg="#e74c3c").pack(anchor="w")
        else:
            tk.Label(info_frame, text=price_text, font=("Arial", 9), bg="white").pack(anchor="w")

        tk.Label(info_frame, text=f"stock: {product.stock}", font=("Arial", 9), bg="white", fg="blue").pack(anchor="w")

        #reviews
        product_reviews = [r for r in self.reviews if r.get('product_id') == str(product.product_id)]
        if product_reviews:
            avg_rating = sum(r.get('rating', 0) for r in product_reviews) / len(product_reviews)
            tk.Label(info_frame, text=f"{avg_rating:.1f} ({len(product_reviews)} reviews)",
                     font=("Arial", 9, "bold"), bg="white", fg="#f39c12").pack(anchor="w")

        if product.description:
            tk.Label(info_frame, text=f"description: {product.description}",
                     font=("Arial", 8), bg="white", fg="gray", wraplength=250, justify=tk.LEFT).pack(anchor="w")

        #buttons
        btn_frame = tk.Frame(info_frame, bg="white")
        btn_frame.pack(anchor="w", pady=5)

        def add_item():
            if product.stock > 0:
                if product.product_id in self.cart:
                    self.cart[product.product_id]["qty"] += 1
                else:
                    self.cart[product.product_id] = {
                        "product": product,
                        "qty": 1
                    }
                self.update_cart()
                messagebox.showinfo("added", f"{product.name} added to cart")
            else:
                messagebox.showwarning("out of stock", "this product is out of stock")

        def select_for_review():
            self.selected_product_for_review = product
            self.product_name_label.config(text=product.name)
            self.comment_text.delete("1.0", tk.END)
            self.rating_var.set(5)
            self.refresh_reviews_display()

        tk.Button(btn_frame, text="add to cart", bg="#27ae60", fg="white",
                  command=add_item, width=18).pack(side=tk.LEFT, padx=2)

        tk.Button(btn_frame, text="review", bg="#f39c12", fg="white",
                  command=select_for_review, width=18).pack(side=tk.LEFT, padx=2)

    def post_review(self):
        """post a review for the selected product"""
        if self.selected_product_for_review is None:
            messagebox.showwarning("select product", "please select a product first")
            return

        comment_text = self.comment_text.get("1.0", tk.END).strip()
        rating = self.rating_var.get()

        if not comment_text:
            messagebox.showwarning("empty", "please write a comment")
            return

        try:
            #create comment object
            comment = Comment(
                username=self.username,
                product_id=self.selected_product_for_review.product_id,
                comment_text=comment_text,
                rating=rating,
                date=datetime.now().strftime("%Y-%m-%d")
            )

            #add to reviews list
            self.reviews.append(comment.to_csv_row())

            #save to CSV
            self.database.save_review(comment)

            messagebox.showinfo("success", f"review posted\nrating: {rating}/5")

            #clear form
            self.comment_text.delete("1.0", tk.END)
            self.rating_var.set(5)

            #refresh display
            self.refresh_reviews_display()

            #refresh products to show updated rating
            self.display_products(self.products)

        except Exception as e:
            messagebox.showerror("error", f" couldn't post review: {e}")

    def refresh_reviews_display(self):
        """refresh the reviews display for selected product"""
        if self.selected_product_for_review is None:
            self.reviews_display.config(state=tk.NORMAL)
            self.reviews_display.delete("1.0", tk.END)
            self.reviews_display.insert("1.0", "select a product to see reviews")
            self.reviews_display.config(state=tk.DISABLED)
            return

        product_reviews = [r for r in self.reviews if
                           r.get('product_id') == str(self.selected_product_for_review.product_id)]

        self.reviews_display.config(state=tk.NORMAL)
        self.reviews_display.delete("1.0", tk.END)

        if not product_reviews:
            self.reviews_display.insert("1.0", "no reviews yet")
        else:
            text = ""
            for review in product_reviews:
                text += f"{review.get('rating')}/5 - {review.get('username')}\n"
                text += f"{review.get('comment')}\n"
                text += f"({review.get('date')})\n"
                text += "─" * 20 + "\n"
            self.reviews_display.insert("1.0", text)

        self.reviews_display.config(state=tk.DISABLED)

    def update_cart(self):
        """update cart display"""
        if not self.cart:
            self.cart_label.config(text="empty")
            return

        text = ""
        total = 0
        for pid, item in self.cart.items():
            p = item["product"]
            q = item["qty"]
            price = p.final_price() * q
            total += price
            text += f"{p.name}\n  x{q} = ${price:,.0f}\n\n"

        text += f"{'─' * 30}\n"
        text += f"total: ${total:,.0f}"
        self.cart_label.config(text=text)

    def search_products(self):
        """search products"""
        keyword = self.search_var.get().lower()
        if not keyword:
            self.display_products(self.products)
            return

        filtered = [p for p in self.products if keyword in p.name.lower() or keyword in p.category.lower()]

        if filtered:
            self.display_products(filtered)
        else:
            messagebox.showinfo("search", "no products found")
            self.display_products(self.products)

    def clear_cart(self):
        """clear cart"""
        if not self.cart:
            messagebox.showinfo("empty", "cart is already empty")
            return

        self.cart = {}
        self.update_cart()
        messagebox.showinfo("success", "cart cleared")

    def checkout(self):
        """checkout"""
        if not self.cart:
            messagebox.showwarning("empty", "cart is empty")
            return

        total = sum(
            item["product"].final_price() * item["qty"]
            for item in self.cart.values()
        )

        order_text = "order summary:\n\n"
        for item in self.cart.values():
            p = item["product"]
            q = item["qty"]
            price = p.final_price() * q
            order_text += f"{p.name} x{q} = ${price:,.0f}\n"
        order_text += f"\n{'─' * 30}\n"
        order_text += f"total: ${total:,.0f}\n\n"
        order_text += "thank you for shopping"

        messagebox.showinfo("order confirmed", order_text)
        self.cart = {}
        self.update_cart()