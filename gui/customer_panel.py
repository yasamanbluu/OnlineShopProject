import tkinter as tk
from tkinter import messagebox


def show_customer_page(root, back_to_login_callback):
    #customer page
    cart = []

    #main window
    customer_frame = tk.Frame(root)

    tk.Label(
        customer_frame,
        text="Dr. genome's lab store",
        font=("Helvetica", 20, "bold")
    ).pack(pady=10)

    #view cart button
    tk.Button(
        customer_frame,
        text="View Cart🛒",
        command=lambda: open_cart_page(cart_frame, cart_list_frame, total_label, cart, customer_frame),
        bg="#2196F3",
        fg="white",
        font=("Helvetica", 12)
    ).pack(pady=10)

    #scrolling
    canvas = tk.Canvas(customer_frame)
    scrollbar = tk.Scrollbar(customer_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    #products
    products = [
        ("DNA extraction kit", 201, 15),
        ("Gene editing simulation kit", 318, 8),
        ("CRISPR training set", 499.81, 10),
        ("Protein analyzer", 1321, 3),
        ("Lab robot assistant", 3015, 2),
        ("Nano microscope", 841.99, 4),
        ("Longevity serum prototype", 5000, 1),
        ("Recombinant insulin pack", 191, 20),
        ("Synthetic organ starter kit", 8257.70, 1),
        ("Bio-glow bacteria culture", 145, 25)
    ]

    for name, price, stock in products:
        card = tk.Frame(scrollable_frame, bd=2, relief="ridge", padx=10, pady=10)
        card.pack(pady=8, fill="x", padx=20)

        tk.Label(card, text=name, font=("Helvetica", 12, "bold")).pack(anchor="w")
        tk.Label(card, text=f"Price: ${price}").pack(anchor="w")
        tk.Label(card, text=f"Stock: {stock}").pack(anchor="w")

        tk.Button(
            card,
            text="Add to Cart",
            command=lambda n=name, p=price: add_to_cart(n, p, cart, update_cart_display_callback),
            bg="#FF9800",
            fg="white"
        ).pack(pady=5)

    #cart page
    cart_frame = tk.Frame(root)

    tk.Label(
        cart_frame,
        text="Shopping Cart",
        font=("Helvetica", 20, "bold")
    ).pack(pady=20)

    tk.Button(
        cart_frame,
        text="← Back to Store",
        command=lambda: back_to_store(cart_frame, customer_frame),
        bg="#607D8B",
        fg="white"
    ).pack(pady=10)

    cart_list_frame = tk.Frame(cart_frame)
    cart_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

    total_label = tk.Label(cart_frame, text="Total: $0", font=("Helvetica", 16, "bold"))
    total_label.pack(pady=10)

    tk.Button(
        cart_frame,
        text="checkout",
        command=lambda: checkout(cart, update_cart_display_callback),
        bg="#4CAF50",
        fg="white",
        font=("Helvetica", 14)
    ).pack(pady=20)

    def update_cart_display_callback():
        update_cart_display(cart_list_frame, total_label, cart)

    def add_to_cart(name, price):
        cart.append((name, price))
        messagebox.showinfo("Added", f"{name} has been added to your cart")
        update_cart_display_callback()

    return customer_frame, cart_frame


def update_cart_display(cart_list_frame, total_label, cart):
    for widget in cart_list_frame.winfo_children():
        widget.destroy()

    if not cart:
        tk.Label(cart_list_frame, text="Oops! Your cart is empty", font=("Helvetica", 14)).pack(pady=20)
        total_label.config(text="Total: $0")
        return

    total = 0
    for i, (name, price) in enumerate(cart):
        item_frame = tk.Frame(cart_list_frame)
        item_frame.pack(fill="x", pady=5)

        tk.Label(item_frame, text=f"{i + 1}. {name}", font=("Helvetica", 12)).pack(side="left", padx=10)
        tk.Label(item_frame, text=f"${price:.2f}", font=("Helvetica", 12)).pack(side="left", padx=10)

        tk.Button(
            item_frame,
            text="Remove",
            command=lambda idx=i: remove_from_cart(idx, cart, update_cart_display_callback),
            bg="red",
            fg="white"
        ).pack(side="right", padx=10)

        total += price

    total_label.config(text=f"Total: ${total:.2f}")


def remove_from_cart(index, cart, update_callback):
    cart.pop(index)
    update_callback()


def checkout(cart, update_callback):
    if not cart:
        messagebox.showwarning("Cart Empty", "Oops! Your cart is empty")
        return

    total = sum(price for _, price in cart)
    messagebox.showinfo("Checkout", f"Total: ${total:.2f}\nThanks for shopping^^")
    cart.clear()
    update_callback()


def open_cart_page(cart_frame, cart_list_frame, total_label, cart, customer_frame):
    customer_frame.pack_forget()
    cart_frame.pack(fill="both", expand=True)
    update_cart_display(cart_list_frame, total_label, cart)


def back_to_store(cart_frame, customer_frame):
    cart_frame.pack_forget()
    customer_frame.pack(fill="both", expand=True)