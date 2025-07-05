# main.py
import tkinter as tk
from tkinter import messagebox
from database import initialize_db
from login import LoginWindow

def start_gui():
    root = tk.Tk()
    root.withdraw()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        initialize_db()
        start_gui()
    except Exception as e:
        messagebox.showerror("خطا", str(e))
