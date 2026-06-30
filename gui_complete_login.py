import tkinter as tk
from tkinter import messagebox
from database import Database


class LoginWindow:
    """login page with loading users from database"""

    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("online shop - login")
        self.root.geometry("400x250")
        self.on_login_success = on_login_success

        #load users from database
        try:
            self.db = Database("data")
            self.users = self.db.load_users()
        except Exception as e:
            messagebox.showerror("error", f"can't load database: {e}")
            self.users = {}

        self.create_gui()

    def create_gui(self):
        """create login page"""

        #title
        title = tk.Label(self.root, text="online shop", font=("Arial", 14, "bold"))
        title.pack(pady=20)

        #Username
        tk.Label(self.root, text="username:").pack()
        self.username = tk.Entry(self.root, width=30)
        self.username.pack(pady=5)

        #Password
        tk.Label(self.root, text="password:").pack()
        self.password = tk.Entry(self.root, width=30, show="*")
        self.password.pack(pady=5)

        #login button
        btn = tk.Button(self.root, text="login", width=20, bg="#27ae60", fg="white", command=self.check_login)
        btn.pack(pady=20)

        #info
        info = tk.Label(self.root, text="test: hamidi / soltani / rahmani / karimi",
                        font=("Arial", 8), fg="gray")
        info.pack()

    def check_login(self):
        """check username and password"""
        user = self.username.get().strip()
        pwd = self.password.get()

        #Check if user exists in database
        if user in self.users:
            user_obj = self.users[user]
            if user_obj.check_password(pwd):
                role = user_obj.role
                self.on_login_success(user, role)
                return

        messagebox.showerror("error", "wrong username or password")