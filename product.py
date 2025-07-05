import tkinter as tk
from tkinter import messagebox, ttk
from database import create_connection

def open_product_window():
    window = tk.Toplevel()
    window.title("Product Management - HiHi Accounting")
    window.geometry("900x550")
    window.resizable(False, False)

    # فرم ورودی کالا
    form_frame = tk.Frame(window, padx=10, pady=10)
    form_frame.pack(fill="x")

    labels = ["Name", "Category", "Brand", "Model", "Cost Price", "Selling Price", "Quantity", "Warranty", "Barcode"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label + ":").grid(row=i, column=0, sticky="e", pady=4)
        entry = tk.Entry(form_frame, width=40)
        entry.grid(row=i, column=1, pady=4)
        entries[label.lower().replace(" ", "_")] = entry

    # دکمه ثبت و پاک‌کردن
    button_frame = tk.Frame(form_frame)
    button_frame.grid(row=len(labels), columnspan=2, pady=10)

    def add_product():
        data = {key: entry.get().strip() for key, entry in entries.items()}
        if not data["name"]:
            messagebox.showerror("Error", "Product name is required")
            return

        try:
            data["cost_price"] = float(data["cost_price"])
            data["selling_price"] = float(data["selling_price"])
            data["quantity"] = int(data["quantity"])
        except ValueError:
            messagebox.showerror("Error", "Invalid price or quantity format")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products 
            (name, category, brand, model, cost_price, selling_price, quantity, warranty, barcode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"], data["category"], data["brand"], data["model"],
            data["cost_price"], data["selling_price"], data["quantity"],
            data["warranty"], data["barcode"]
        ))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully")
        clear_form()
        load_products()

    def clear_form():
        for entry in entries.values():
            entry.delete(0, tk.END)

    tk.Button(button_frame, text="Add Product", width=15, command=add_product).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Clear", width=10, command=clear_form).grid(row=0, column=1, padx=5)

    # جدول نمایش کالاها
    table_frame = tk.Frame(window, padx=10)
    table_frame.pack(fill="both", expand=True)

    columns = ("id", "name", "category", "brand", "model", "cost_price", "selling_price", "quantity", "warranty", "barcode")
    product_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

    for col in columns:
        product_table.heading(col, text=col.capitalize())
        product_table.column(col, anchor="center", width=90)

    product_table.pack(fill="both", expand=True)

    # بارگذاری کالاها
    def load_products():
        for row in product_table.get_children():
            product_table.delete(row)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            product_table.insert("", tk.END, values=row)
        conn.close()

    load_products()
