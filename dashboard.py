from report import open_report_window

from invoice import open_invoice_window

from product import open_product_window

from customer import open_customer_window
import tkinter as tk
from tkinter import messagebox

def open_dashboard():
    root = tk.Tk()
    root.title("HiHi Accounting - Dashboard")
    root.geometry("600x400")
    root.resizable(False, False)

    # عنوان خوش‌آمدگویی
    title = tk.Label(root, text="Welcome to HiHi Accounting Software", font=("Arial", 16), pady=20)
    title.pack()

    # ساخت دکمه‌های دسترسی به بخش‌های مختلف
    button_frame = tk.Frame(root, pady=10)
    button_frame.pack()

    # هر دکمه به یک ماژول متصل خواهد شد (فعلاً فقط پیام نشان می‌دهند)
    buttons = [
("🧑‍💼 Customers", open_customer_window),
("📦 Products", open_product_window),
        ("📋 Invoices", open_invoice_window),
        ("📊 Reports", open_report_window),

        ("⚙️ Settings", lambda: messagebox.showinfo("Coming Soon", "Settings")),
        ("🔒 Logout", root.destroy)
    ]

    for text, command in buttons:
        btn = tk.Button(button_frame, text=text, width=20, height=2, command=command)
        btn.pack(pady=5)

    root.mainloop()
