import tkinter as tk
from gui.login_page import show_login_page
from gui.customer_panel import show_customer_page

def main():
    root = tk.Tk()
    root.title("Online Store")
    root.geometry("600x700")

    current_frame = None
    login_frame = None
    customer_frame = None
    register_frame = None

    def open_customer():
        nonlocal current_frame, login_frame, register_frame, customer_frame
        if login_frame:
            login_frame.pack_forget()
        if register_frame:
            register_frame.pack_forget()
        if not customer_frame:
            customer_frame, _ = show_customer_page(root, back_to_login)
        customer_frame.pack(fill="both", expand=True)
        current_frame = customer_frame

    def open_register():
        nonlocal current_frame, login_frame, register_frame
        if login_frame:
            login_frame.pack_forget()
        # register page
        register_frame = tk.Frame(root)
        tk.Label(register_frame, text="Create Account", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(register_frame, text="Username").pack()
        tk.Entry(register_frame).pack()
        tk.Label(register_frame, text="Password").pack()
        tk.Entry(register_frame, show="*").pack()
        tk.Button(register_frame, text="Create Account").pack(pady=10)
        tk.Button(register_frame, text="Back", command=back_to_login).pack()
        register_frame.pack(fill="both", expand=True)
        current_frame = register_frame

    def back_to_login():
        nonlocal current_frame, register_frame, customer_frame, login_frame
        if register_frame:
            register_frame.pack_forget()
        if customer_frame:
            customer_frame.pack_forget()
        if not login_frame:
            login_frame, _, _ = show_login_page(root, open_customer, open_register)
        login_frame.pack(fill="both", expand=True)
        current_frame = login_frame

    #login page
    login_frame, _, _ = show_login_page(root, open_customer, open_register)
    login_frame.pack(fill="both", expand=True)
    current_frame = login_frame

    root.mainloop()


if __name__ == "__main__":
    main()