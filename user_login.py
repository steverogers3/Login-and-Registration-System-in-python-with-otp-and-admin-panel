import tkinter as tk
from tkinter import messagebox
import bcrypt, os
from cryptography.fernet import Fernet

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "logdata.txt")

SECRET_KEY = b"pb_0H7TtoNqQi0nEJBPhKBzdkHJ9jKI9XEtnHNCpeHQ="
fernet = Fernet(SECRET_KEY)

def verify_user(username,password):
    if not os.path.exists(DATA_FILE): return False

    with open(DATA_FILE,"r") as f:
        for line in f:
            u,hashed,enc,*rest=line.strip().split("|")
            if u==username:
                return bcrypt.checkpw(password.encode(), hashed.encode())
    return False

def login_ui():
    log = tk.Tk()
    log.title("User Login")
    log.geometry("300x230")

    tk.Label(log,text="Login",font=("Arial",18,"bold")).pack(pady=10)

    tk.Label(log,text="Username").pack()
    uname=tk.Entry(log); uname.pack()

    tk.Label(log,text="Password").pack()
    pwd=tk.Entry(log,show="*"); pwd.pack(pady=5)

    def login():
        if verify_user(uname.get(),pwd.get()):
            messagebox.showinfo("Success","Login Successful!")
            log.destroy()
        else:
            messagebox.showerror("Error","Invalid credentials!")

    def register_open():
        import user_register
        log.destroy()
        user_register.register_ui()

    tk.Button(log,text="Login",command=login,bg="blue",fg="white").pack(pady=8)
    tk.Button(log,text="Create Account",command=register_open).pack()

    log.mainloop()

if __name__ == "__main__":
    login_ui()
