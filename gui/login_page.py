import tkinter as tk


def show_login_page(root, open_customer_callback, open_register_callback):
    #login page
    login_frame = tk.Frame(root)

    tk.Label(login_frame, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    tk.Label(login_frame, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.pack()

    tk.Button(
        login_frame,
        text="Login",
        command=open_customer_callback,
        bg="#4CAF50",
        fg="white"
    ).pack(pady=10)

    tk.Button(
        login_frame,
        text="Register",
        command=open_register_callback
    ).pack()

    return login_frame, username_entry, password_entry