import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection

def open_report_window():
    window = tk.Toplevel()
    window.title("Reports - HiHi Accounting")
    window.geometry("800x600")
    window.resizable(False, False)

    tab_control = ttk.Notebook(window)
    tab_sales = ttk.Frame(tab_control)
    tab_inventory = ttk.Frame(tab_control)

    tab_control.add(tab_sales, text="📊 Sales Report")
    tab_control.add(tab_inventory, text="📦 Inventory Report")
    tab_control.pack(expand=1, fill="both")

    # 📊 گزارش فروش
    def load_sales_report():
        for row in sales_table.get_children():
            sales_table.delete(row)

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer, date, total FROM invoices ORDER BY date DESC")
        for row in cursor.fetchall():
            sales_table.insert("", tk.END, values=row)
        conn.close()

    sales_table = ttk.Treeview(tab_sales, columns=("id", "customer", "date", "total"), show="headings")
    for col in ("id", "customer", "date", "total"):
        sales_table.heading(col, text=col.capitalize())
        sales_table.column(col, anchor="center", width=150)
    sales_table.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Button(tab_sales, text="Reload Sales Report", command=load_sales_report).pack(pady=5)

    # 📦 گزارش موجودی کالا
    def load_inventory_report():
        for row in inventory_table.get_children():
            inventory_table.delete(row)

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, brand, quantity, selling_price FROM products ORDER BY quantity ASC")
        for row in cursor.fetchall():
            inventory_table.insert("", tk.END, values=row)
        conn.close()

    inventory_table = ttk.Treeview(tab_inventory, columns=("name", "brand", "quantity", "selling_price"), show="headings")
    for col in ("name", "brand", "quantity", "selling_price"):
        inventory_table.heading(col, text=col.capitalize())
        inventory_table.column(col, anchor="center", width=180)
    inventory_table.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Button(tab_inventory, text="Reload Inventory Report", command=load_inventory_report).pack(pady=5)

    # بارگذاری اولیه
    load_sales_report()
    load_inventory_report()
