import tkinter as tk
from tkinter import messagebox
import bcrypt, os
from cryptography.fernet import Fernet

# Shared file location
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "logdata.txt")

SECRET_KEY = b"pb_0H7TtoNqQi0nEJBPhKBzdkHJ9jKI9XEtnHNCpeHQ="
fernet = Fernet(SECRET_KEY)

def register_user(username,password,mobile,email,age):
    hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
    enc = fernet.encrypt(password.encode()).decode()

    with open(DATA_FILE,"a") as f:
        f.write(f"{username}|{hashed}|{enc}|{mobile}|{email}|{age}\n")

def register_ui():
    reg = tk.Tk()
    reg.title("Register")
    reg.geometry("350x420")
    
    tk.Label(reg,text="Create Account",font=("Arial",18,"bold")).pack(pady=10)

    fields=["Username","Password","Mobile","Email","Age"]
    entries=[]

    for f in fields:
        tk.Label(reg,text=f,font=("Arial",10,"bold")).pack()
        e=tk.Entry(reg,font=("Arial",11))
        if f=="Password": e.config(show="*")
        e.pack(pady=3)
        entries.append(e)

    def submit():
        username,password,mobile,email,age=[e.get() for e in entries]

        if "" in [username,password,mobile,email,age]:
            return messagebox.showerror("Error","⚠ All fields are required!")

        # --- Mobile Validation ---
        if not mobile.isdigit():
            return messagebox.showerror("Invalid","Mobile must contain digits only!")

        if len(mobile)!=10:
            return messagebox.showerror("Invalid","Mobile must be exactly 10 digits!")

        # --- Email Validation ---
        if not email.endswith("@gmail.com"):
            return messagebox.showerror("Invalid","Email must end with @gmail.com")

        # --- Age Validation (optional recommended) ---
        if not age.isdigit() or int(age)<10 or int(age)>100:
            return messagebox.showerror("Invalid","Enter valid age (10-100)")

        # --- Everything valid now save ---
        register_user(username,password,mobile,email,age)
        messagebox.showinfo("Success","Account Created Successfully!")
        reg.destroy()

    tk.Button(reg,text="Register",command=submit,
              bg="green",fg="white",font=("Arial",12,"bold")).pack(pady=15)
    
    reg.mainloop()

if __name__ == "__main__":
    register_ui()
