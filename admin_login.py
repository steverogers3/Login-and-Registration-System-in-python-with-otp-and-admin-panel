import tkinter as tk
from tkinter import messagebox
from admin_gui import open_admin_panel  # Import admin panel launcher

# Credentials (You can store in file/database later)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"

def login():
    user = username.get()
    pwd = password.get()

    if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()
        open_admin_panel()     # OPEN MAIN ADMIN GUI
    else:
        messagebox.showerror("Error", "Invalid Username or Password!")

root = tk.Tk()
root.title("Admin Login")
root.geometry("350x250")
root.config(bg="#111")

tk.Label(root,text="Admin Login",font=("Arial",18,"bold"),bg="#111",fg="cyan").pack(pady=10)

username = tk.Entry(root,font=("Arial",12))
username.pack(pady=8)
username.insert(0,"admin")

password = tk.Entry(root,font=("Arial",12),show="*")
password.pack(pady=7)
password.insert(0,"12345")

tk.Button(root,text="Login",command=login,bg="#0078D7",fg="white",font=("Arial",12,"bold")).pack(pady=15)

root.mainloop()
