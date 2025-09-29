import tkinter as tk
from tkinter import messagebox
from gui import run_gui 

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "thuthu": {"password": "thu123", "role": "thuthu"},
    "docgia": {"password": "doc123", "role": "docgia"}
}

def show_login():
    login_win = tk.Tk()
    login_win.title("Đăng nhập")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Tên đăng nhập:").pack(pady=5)
    entry_username = tk.Entry(login_win)
    entry_username.pack()

    tk.Label(login_win, text="Mật khẩu:").pack(pady=5)
    entry_password = tk.Entry(login_win, show="*")
    entry_password.pack()

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if username in users and users[username]['password'] == password:
            role = users[username]['role']
            login_win.destroy()
            run_gui(user_role=role)
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    tk.Button(login_win, text="Đăng nhập", command=login).pack(pady=10)
    login_win.mainloop()
