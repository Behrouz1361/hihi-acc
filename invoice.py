import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection
import datetime

def open_invoice_window():
    window = tk.Toplevel()
    window.title("Sales Invoice - HiHi Accounting")
    window.geometry("900x600")
    window.resizable(False, False)

    # فرم مشخصات بالا
    top_frame = tk.Frame(window, padx=10, pady=10)
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="Customer Name:").grid(row=0, column=0, sticky="e")
    customer_entry = tk.Entry(top_frame, width=40)
    customer_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top_frame, text="Date:").grid(row=0, column=2, sticky="e")
    date_entry = tk.Entry(top_frame, width=20)
    date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
    date_entry.grid(row=0, column=3, padx=10)

    # فرم افزودن محصول
    product_frame = tk.Frame(window, padx=10, pady=5)
    product_frame.pack(fill="x")

    tk.Label(product_frame, text="Barcode:").grid(row=0, column=0, sticky="e")
    barcode_entry = tk.Entry(product_frame, width=30)
    barcode_entry.grid(row=0, column=1, padx=5)

    tk.Label(product_frame, text="Quantity:").grid(row=0, column=2, sticky="e")
    qty_entry = tk.Entry(product_frame, width=10)
    qty_entry.insert(0, "1")
    qty_entry.grid(row=0, column=3, padx=5)

    def add_product_to_invoice():
        barcode = barcode_entry.get().strip()
        try:
            qty = int(qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, selling_price FROM products WHERE barcode=?", (barcode,))
        result = cursor.fetchone()
        conn.close()

        if result:
            name, price = result
            subtotal = round(price * qty, 2)
            invoice_table.insert("", tk.END, values=(barcode, name, price, qty, subtotal))
            calculate_total()
            barcode_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)
            qty_entry.insert(0, "1")
        else:
            messagebox.showerror("Error", "Product not found")

    tk.Button(product_frame, text="Add Product", command=add_product_to_invoice).grid(row=0, column=4, padx=10)

    # جدول فاکتور
    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("barcode", "name", "unit_price", "quantity", "subtotal")
    invoice_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        invoice_table.heading(col, text=col.capitalize())
        invoice_table.column(col, anchor="center", width=100)
    invoice_table.pack(fill="both", expand=True)

    # مجموع نهایی
    total_var = tk.StringVar(value="0.00")

    total_frame = tk.Frame(window)
    total_frame.pack(pady=5)

    tk.Label(total_frame, text="Total:").grid(row=0, column=0)
    tk.Label(total_frame, textvariable=total_var, font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10)

    def calculate_total():
        total = 0
        for item in invoice_table.get_children():
            total += float(invoice_table.item(item)['values'][4])
        total_var.set(f"{total:.2f}")

    # دکمه ثبت فاکتور
    def save_invoice():
        customer = customer_entry.get().strip()
        date = date_entry.get().strip()
        if not customer or not invoice_table.get_children():
            messagebox.showerror("Error", "Customer and at least one product required")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT,
                date TEXT,
                total REAL
            )
        """)
        cursor.execute("INSERT INTO invoices (customer, date, total) VALUES (?, ?, ?)",
                       (customer, date, float(total_var.get())))
        invoice_id = cursor.lastrowid

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                barcode TEXT,
                name TEXT,
                unit_price REAL,
                quantity INTEGER,
                subtotal REAL
            )
        """)

        for item in invoice_table.get_children():
            data = invoice_table.item(item)['values']
            cursor.execute("""
                INSERT INTO invoice_items (invoice_id, barcode, name, unit_price, quantity, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (invoice_id, *data))

        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", f"Invoice #{invoice_id} saved successfully")
        customer_entry.delete(0, tk.END)
        for row in invoice_table.get_children():
            invoice_table.delete(row)
        calculate_total()

    tk.Button(window, text="Save Invoice", font=("Arial", 12), command=save_invoice).pack(pady=10)
