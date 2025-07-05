import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import create_connection
# از فایل dashboard.py که هنوز نساخته‌ایم
from dashboard import open_dashboard

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("HiHi Accounting - Login")
        self.root.geometry("350x220")
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.frame, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.check_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=15)

        self.root.deiconify()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
