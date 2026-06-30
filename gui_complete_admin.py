import tkinter as tk
from tkinter import messagebox, ttk
from product import Product


class AdminPanel:
    """admin panel, auto save to CSV"""

    def __init__(self, root, username, on_logout, products, orders, database):
        self.root = root
        self.username = username
        self.on_logout = on_logout
        self.products = products
        self.orders = orders
        self.database = database
        self.selected_product = None

        self.root.title(f"Admin Panel - {username}")
        self.root.geometry("1100x750")

        self.create_gui()

    def create_gui(self):
        """creating admin panel"""

        #header
        header = tk.Frame(self.root, bg="#27ae60", height=60)
        header.pack(fill=tk.X)

        tk.Label(header, text=f" Admin Panel - {self.username}",
                 bg="#27ae60", fg="white", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=20, pady=10)

        tk.Button(header, text="Logout", bg="red", fg="white",
                  command=self.on_logout, font=("Arial", 10)).pack(side=tk.RIGHT, padx=20, pady=10)

        #main content with tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #tab 1: products
        products_frame = tk.Frame(notebook)
        notebook.add(products_frame, text=" Manage Products")
        self.create_products_tab(products_frame)

        #tab 2: orders
        orders_frame = tk.Frame(notebook)
        notebook.add(orders_frame, text=" View Orders & Report")
        self.create_orders_tab(orders_frame)

    def create_products_tab(self, parent):
        """product management tab, auto-save to CSV"""

        #left: add/edit Form
        form_frame = tk.LabelFrame(parent, text="➕ Add /  Edit Product", font=("Arial", 11, "bold"))
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=False)

        #id
        tk.Label(form_frame, text="Product ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.id_entry = tk.Entry(form_frame, width=20)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        #name
        tk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, width=20)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        #price
        tk.Label(form_frame, text="Price:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.price_entry = tk.Entry(form_frame, width=20)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        #stock
        tk.Label(form_frame, text="Stock:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.stock_entry = tk.Entry(form_frame, width=20)
        self.stock_entry.grid(row=3, column=1, padx=5, pady=5)

        #category
        tk.Label(form_frame, text="Category:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.category_entry = tk.Entry(form_frame, width=20)
        self.category_entry.grid(row=4, column=1, padx=5, pady=5)

        #discount
        tk.Label(form_frame, text="Discount %:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.discount_entry = tk.Entry(form_frame, width=20)
        self.discount_entry.grid(row=5, column=1, padx=5, pady=5)

        #buttons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="➕ Add Product", bg="#27ae60", fg="white",
                  command=self.add_product, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text=" Edit Selected", bg="#3498db", fg="white",
                  command=self.edit_product, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text=" Delete Selected", bg="#e74c3c", fg="white",
                  command=self.delete_product, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Clear Form", bg="gray", fg="white",
                  command=self.clear_form, width=15).pack(side=tk.LEFT, padx=5)

        #right: products list
        list_frame = tk.LabelFrame(parent, text=" All Products", font=("Arial", 11, "bold"))
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        #scrollbar
        canvas = tk.Canvas(list_frame, height=400, bg="white")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="white")

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.products_list_frame = scrollable
        self.refresh_products_list()

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_products_list(self):
        """refreshing  product list"""
        for widget in self.products_list_frame.winfo_children():
            widget.destroy()

        #header
        header_text = f"{'ID':<6} {'Name':<18} {'Price':<12} {'Stock':<6} {'Disc%':<6} {'Cat':<12}"
        tk.Label(self.products_list_frame, text=header_text, font=("Arial", 9, "bold"),
                 bg="#ecf0f1", fg="black", justify=tk.LEFT).pack(fill=tk.X, padx=5, pady=5)

        #products
        for i, p in enumerate(self.products):
            text = f"{p.product_id:<6} {p.name:<18} ${p.price:<11.0f} {p.stock:<6} {p.discount_percent:<6} {p.category:<12}"

            btn = tk.Label(self.products_list_frame, text=text, font=("Arial", 9),
                           bg="white", fg="black", justify=tk.LEFT, cursor="hand2")

            def select_product(idx=i):
                self.select_product(idx)

            btn.pack(fill=tk.X, padx=5, pady=2)
            btn.bind("<Button-1>", lambda e, idx=i: select_product(idx))

    def select_product(self, index):
        """select a product for editing"""
        if 0 <= index < len(self.products):
            p = self.products[index]
            self.selected_product = index

            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, p.product_id)
            self.id_entry.config(state="disabled")  # Disable ID edit

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, p.name)

            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(p.price))

            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, str(p.stock))

            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, p.category)

            self.discount_entry.delete(0, tk.END)
            self.discount_entry.insert(0, str(p.discount_percent))

            messagebox.showinfo("Selected", f" Product '{p.name}' selected for editing")

    def add_product(self):
        """add a new product"""
        try:
            pid = self.id_entry.get().strip()
            name = self.name_entry.get().strip()
            price = float(self.price_entry.get())
            stock = int(self.stock_entry.get())
            category = self.category_entry.get().strip()
            discount = float(self.discount_entry.get()) if self.discount_entry.get() else 0

            if not all([pid, name, price, stock, category]):
                messagebox.showerror("Error", "Please fill all fields!")
                return

            #check if id already exists
            if any(p.product_id == pid for p in self.products):
                messagebox.showerror("Error", "Product ID already exists!")
                return

            new_product = Product(pid, name, price, stock, category, discount)
            self.products.append(new_product)

            #auto-save to CSV
            self.save_to_csv()

            messagebox.showinfo("Success", f"✅ Product '{name}' added successfully!")
            self.clear_form()
            self.refresh_products_list()

        except ValueError:
            messagebox.showerror("Error", "Invalid input! Check price and stock.")

    def edit_product(self):
        """edit the selected product"""
        if self.selected_product is None:
            messagebox.showwarning("Warning", "Please select a product first!")
            return

        try:
            idx = self.selected_product
            p = self.products[idx]

            p.name = self.name_entry.get().strip()
            p.price = float(self.price_entry.get())
            p.stock = int(self.stock_entry.get())
            p.category = self.category_entry.get().strip()
            p.discount_percent = float(self.discount_entry.get()) if self.discount_entry.get() else 0

            #auto-save to CSV
            self.save_to_csv()

            messagebox.showinfo("Success", f" Product '{p.name}' updated successfully!\n Changes saved to CSV")
            self.clear_form()
            self.refresh_products_list()

        except ValueError:
            messagebox.showerror("Error", "Invalid input!")

    def delete_product(self):
        """delete the selected product"""
        if self.selected_product is None:
            messagebox.showwarning("Warning", "Please select a product first!")
            return

        if messagebox.askyesno("Confirm", "Delete this product?"):
            idx = self.selected_product
            name = self.products[idx].name
            del self.products[idx]

            #auto-save to CSV
            self.save_to_csv()

            messagebox.showinfo("Success", f" Product '{name}' deleted!")
            self.clear_form()
            self.refresh_products_list()
            self.selected_product = None

    def save_to_csv(self):
        """auto-saving product data to CSV"""
        try:
            self.database.save_products(self.products)
            print(" Products saved to CSV automatically!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save to CSV: {e}")

    def clear_form(self):
        """clear the form"""
        self.id_entry.config(state="normal")
        self.id_entry.delete(0, tk.END)
        self.id_entry.config(state="disabled")

        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.discount_entry.delete(0, tk.END)
        self.selected_product = None

    def create_orders_tab(self, parent):
        """orders and sales report tab"""

        #filter
        filter_frame = tk.Frame(parent)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.date_filter = tk.Entry(filter_frame, width=15)
        self.date_filter.pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="🔍 Filter", bg="#3498db", fg="white",
                  command=self.filter_orders).pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="Clear Filter", bg="gray", fg="white",
                  command=self.clear_filter).pack(side=tk.LEFT, padx=5)

        #orders List
        list_frame = tk.LabelFrame(parent, text=" Orders", font=("Arial", 11, "bold"))
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #scrollbar
        canvas = tk.Canvas(list_frame, bg="white")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="white")

        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.orders_list_frame = scrollable
        self.refresh_orders_list()

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_orders_list(self):
        """refresh the orders list"""
        for widget in self.orders_list_frame.winfo_children():
            widget.destroy()

        #header
        header_text = f"{'User':<15} {'Product':<10} {'Qty':<5} {'Price':<15} {'Date':<20}"
        tk.Label(self.orders_list_frame, text=header_text, font=("Arial", 9, "bold"),
                 bg="#ecf0f1", fg="black").pack(fill=tk.X, padx=5, pady=5)

        #orders
        total = 0
        count = 0
        for order in self.orders:
            price = order.get('total_price', 0)
            if isinstance(price, str):
                price = float(price.replace(',', ''))

            text = f"{order.get('username', ''):<15} {order.get('product_id', ''):<10} {order.get('quantity', 0):<5} ${price:<14.0f} {order.get('date', ''):<20}"

            tk.Label(self.orders_list_frame, text=text, font=("Arial", 9),
                     bg="white", fg="black").pack(fill=tk.X, padx=5, pady=2)

            total += price
            count += 1

        #summary
        summary = f"\n Total Orders: {count} | Total Sales: ${total:,.0f}"
        tk.Label(self.orders_list_frame, text=summary, font=("Arial", 10, "bold"),
                 bg="#d5f4e6", fg="#27ae60").pack(fill=tk.X, padx=5, pady=10)

    def filter_orders(self):
        """filter orders by date"""
        date_str = self.date_filter.get().strip()

        if not date_str:
            messagebox.showwarning("Warning", "Enter a date!")
            return

        for widget in self.orders_list_frame.winfo_children():
            widget.destroy()

        filtered = [o for o in self.orders if o.get('date', '').startswith(date_str)]

        if not filtered:
            tk.Label(self.orders_list_frame, text="No orders found for this date!",
                     font=("Arial", 10), fg="red").pack(pady=20)
            return

        #header
        header_text = f"{'User':<15} {'Product':<10} {'Qty':<5} {'Price':<15} {'Date':<20}"
        tk.Label(self.orders_list_frame, text=header_text, font=("Arial", 9, "bold"),
                 bg="#ecf0f1", fg="black").pack(fill=tk.X, padx=5, pady=5)

        total = 0
        for order in filtered:
            price = order.get('total_price', 0)
            if isinstance(price, str):
                price = float(price.replace(',', ''))

            text = f"{order.get('username', ''):<15} {order.get('product_id', ''):<10} {order.get('quantity', 0):<5} ${price:<14.0f} {order.get('date', ''):<20}"

            tk.Label(self.orders_list_frame, text=text, font=("Arial", 9),
                     bg="white", fg="black").pack(fill=tk.X, padx=5, pady=2)

            total += price

        summary = f"\n Filtered Orders: {len(filtered)} | Total: ${total:,.0f}"
        tk.Label(self.orders_list_frame, text=summary, font=("Arial", 10, "bold"),
                 bg="#d5f4e6", fg="#27ae60").pack(fill=tk.X, padx=5, pady=10)

    def clear_filter(self):
        """clearing all applied filters"""
        self.date_filter.delete(0, tk.END)
        self.refresh_orders_list()
