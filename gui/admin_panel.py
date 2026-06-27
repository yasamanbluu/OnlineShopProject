import tkinter as tk
from tkinter import messagebox, ttk


def show_admin_panel(root, back_to_login_callback):
    #admin page

    admin_frame = tk.Frame(root)

    # title
    tk.Label(
        admin_frame,
        text="Admin Panel",
        font=("Helvetica", 24, "bold")
    ).pack(pady=20)

    #back button
    tk.Button(
        admin_frame,
        text="<- Back to Login",
        command=back_to_login_callback,
        bg="#607D8B",
        fg="white"
    ).pack(pady=10)

    #product management section
    tk.Label(
        admin_frame,
        text="Product Management",
        font=("Helvetica", 16, "bold")
    ).pack(pady=10)

    #input frame
    input_frame = tk.Frame(admin_frame)
    input_frame.pack(pady=10, padx=20, fill="x")

    #product name
    tk.Label(input_frame, text="Product Name:").grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(input_frame, width=20)
    name_entry.grid(row=0, column=1, pady=5, padx=5)

    #price
    tk.Label(input_frame, text="Price:").grid(row=0, column=2, sticky="w", pady=5, padx=10)
    price_entry = tk.Entry(input_frame, width=15)
    price_entry.grid(row=0, column=3, pady=5, padx=5)

    #stock
    tk.Label(input_frame, text="Stock:").grid(row=0, column=4, sticky="w", pady=5, padx=10)
    stock_entry = tk.Entry(input_frame, width=10)
    stock_entry.grid(row=0, column=5, pady=5, padx=5)

    #add button
    tk.Button(
        admin_frame,
        text="+ Add Product",
        command=lambda: add_product(name_entry, price_entry, stock_entry),
        bg="#4CAF50",
        fg="white"
    ).pack(pady=10)

    #products list
    tk.Label(
        admin_frame,
        text="Current Products",
        font=("Helvetica", 14, "bold")
    ).pack(pady=10)

    #treeview for displaying products
    columns = ("ID", "Name", "Price", "Stock")
    tree = ttk.Treeview(admin_frame, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(pady=10, padx=20, fill="both", expand=True)

    #management buttons
    button_frame = tk.Frame(admin_frame)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Refresh",
        command=lambda: refresh_products(tree),
        bg="#2196F3",
        fg="white"
    ).pack(side="left", padx=5)

    tk.Button(
        button_frame,
        text="Edit",
        command=lambda: edit_product(tree),
        bg="#FF9800",
        fg="white"
    ).pack(side="left", padx=5)

    tk.Button(
        button_frame,
        text="Delete",
        command=lambda: delete_product(tree),
        bg="#f44336",
        fg="white"
    ).pack(side="left", padx=5)

    #filling the list
    refresh_products(tree)

    return admin_frame


def add_product(name_entry, price_entry, stock_entry):
    # add new product (for now just a message)
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    stock = stock_entry.get().strip()

    if not name or not price or not stock:
        messagebox.showerror("Error", "Please fill all fields!")
        return

    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        messagebox.showerror("Error", "Price must be a number and Stock must be an integer!")
        return

    # this part  should be  connected to database later
    messagebox.showinfo("Success", f"Product '{name}' added successfully!")

    #clear inputs
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)


def refresh_products(tree):
    # update product list (currently with sample data)
    #clear previous list
    for item in tree.get_children():
        tree.delete(item)

    #sample data (will read from database later)
    sample_products = [
        (1, "DNA extraction kit", 201, 15),
        (2, "Gene editing kit", 318, 8),
        (3, "CRISPR training set", 499.81, 10),
    ]

    for product in sample_products:
        tree.insert("", "end", values=product)


def edit_product(tree):
    #edit selected product
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a product to edit!")
        return

    #edit functionality should be added here
    messagebox.showinfo("Info", "Edit functionality coming soon!")


def delete_product(tree):
    #delete selected product
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a product to delete!")
        return

    if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
        #delete functionality should be added here
        messagebox.showinfo("Success", "Product deleted successfully!")
        refresh_products(tree)