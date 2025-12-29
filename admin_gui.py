import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import os, pandas as pd
from reportlab.pdfgen import canvas

DATA_FILE = r"C:\Users\nikhi_yi7g\Downloads\Python Course with Notes\project\login\project\logdata.txt"



# Load Key
# Secret key for encryption/decryption (no file needed)
SECRET_KEY = b"pb_0H7TtoNqQi0nEJBPhKBzdkHJ9jKI9XEtnHNCpeHQ="
fernet = Fernet(SECRET_KEY)
# Load Users
def load_users():
    users=[]
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            parts=line.strip().split("|")
            if len(parts)>=3:       # ensure valid row
                users.append(parts)
    return users


# GUI Window
root=tk.Tk()
root.title("Admin Panel")
root.geometry("900x600")
root.config(bg="#0e1013")

title=tk.Label(root,text="Admin Control Panel",font=("Arial",22,"bold"),bg="#0e1013",fg="white")
title.pack(pady=10)

# Table
cols=["Username","Hashed","Encrypted","Mobile","Email","Age"]
table=ttk.Treeview(root,columns=cols,show="headings")

for col in cols:
    table.heading(col,text=col)
    table.column(col,width=150)

table.pack(fill="both",expand=True,padx=20,pady=20)

# Load to table
for user in load_users():
    table.insert("",tk.END,values=user)

# Decrypt Password Button
def decrypt_selected():
    item = table.focus()
    if not item:
        messagebox.showwarning("Select User","Choose a user first")
        return
    
    values = table.item(item,"values")
    encrypted = values[2]

    try:
        # Try decrypt normally
        decrypted = fernet.decrypt(encrypted.encode()).decode()

    except:
        # If fails, treat stored as plain password
        decrypted = encrypted
    
    messagebox.showinfo("Password",f"Password: {decrypted}")

import matplotlib.pyplot as plt

def show_graph():
    users = load_users()

    # collect age values only if convertible to int
    age_list = []
    for u in users:
        try:
            age_list.append(int(u[5]))   # convert to number
        except:
            pass  # skip invalid ages

    if len(age_list) == 0:
        messagebox.showwarning("No Data", "No numeric age data for graph.")
        return

    plt.figure(figsize=(6,4))
    plt.hist(age_list, bins=10)
    plt.title("User Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()
def show_graph():
    users = load_users()
    lengths = [len(u[2]) for u in users]

    plt.hist(lengths,bins=10)
    plt.title("Password Length Distribution")
    plt.show()




# Delete User
def delete_user():
    item=table.focus()
    if not item:
        return

    user=table.item(item,"values")[0]
    table.delete(item)

    users = load_users()
    users = [u for u in users if u[0]!=user]
    
    with open(DATA_FILE,"w") as f:
        for u in users:
            f.write("|".join(u)+"\n")

    messagebox.showinfo("Done","User Deleted")

# ======= STYLING =======
style = ttk.Style()
style.configure("Treeview", background="#1e1e1e", foreground="white", rowheight=28, fieldbackground="#1e1e1e")
style.configure("Treeview.Heading", background="#333", foreground="cyan", font=("Arial", 11, "bold"))
style.map("Treeview", background=[("selected", "#0078D7")])

root.configure(bg="#0d0d0d")

btn_style = dict(font=("Arial",11,"bold"), fg="white", width=15, height=1)
search_var = tk.StringVar()

def search():
    query = search_var.get().lower()
    table.delete(*table.get_children())
    for u in load_users():
        if query in u[0].lower() or query in u[1].lower() or query in u[2].lower():
            table.insert("",tk.END,values=u)

search_frame = tk.Frame(root,bg="#0d0d0d")
search_frame.pack(pady=5)

tk.Entry(search_frame,textvariable=search_var,width=40,font=("Arial",12)).grid(row=0,column=0,padx=5)
tk.Button(search_frame,text="🔍 Search",command=search,bg="#0078D7",fg="white").grid(row=0,column=1,padx=5)

def refresh_data():
    try:
        table.delete(*table.get_children())   # Clear the table

        users = load_users()                  # Reload file live

        if len(users) == 0:
            messagebox.showinfo("Info","No users found. logdata.txt is empty!")
            return

        for u in users:
            table.insert("", tk.END, values=u)

        messagebox.showinfo("Refreshed","Data refreshed!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

        root.bind("<F5>", lambda e: refresh_data())

def add_user_window():
    win = tk.Toplevel(root)
    win.title("Add User")
    win.geometry("350x400")
    win.config(bg="#0d0d0d")

    tk.Label(win,text="Add New User",font=("Arial",16,"bold"),bg="#0d0d0d",fg="cyan").pack(pady=10)

    entries = []
    fields = ["Username","Password","Mobile","Email","Age"]
    for f in fields:
        tk.Label(win,text=f,font=("Arial",11),bg="#0d0d0d",fg="white").pack()
        e = tk.Entry(win,font=("Arial",11))
        e.pack(pady=4)
        entries.append(e)

    def save_user():
        data = [e.get() for e in entries]
        if "" in data:
            messagebox.showwarning("Error","Fill all fields!")
            return

        username, password, mobile, email, age = data
        
        # Hashing for login (optional)
        import bcrypt
        hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

        encrypted = fernet.encrypt(password.encode()).decode()

        with open(DATA_FILE,"a",encoding="utf-8") as f:
            f.write(f"{username}|{hashed}|{encrypted}|{mobile}|{email}|{age}\n")

        messagebox.showinfo("Saved","User Added Successfully!")
        win.destroy()
        refresh_data()

    tk.Button(win,text="Save",bg="#0078D7",fg="white",font=("Arial",11,"bold"),command=save_user).pack(pady=15)

def view_logs():
    log_win = tk.Toplevel()
    log_win.title("Activity Logs")
    log_win.geometry("600x400")

    text = tk.Text(log_win, wrap="none")
    text.pack(fill="both", expand=True)

    try:
        with open("activity_log.txt", "r") as f:
            text.insert("1.0", f.read())
    except FileNotFoundError:
        text.insert("1.0", "No logs found yet.")



# Export PDF
def export_pdf():
    users=load_users()
    c=canvas.Canvas("export_users.pdf")
    y=800
    for u in users:
        c.drawString(50,y," | ".join(u))
        y -= 20
    c.save()
    messagebox.showinfo("Done","PDF Exported")

    # Export TXT
def export_txt():
    users = load_users()
    with open("export_users.txt","w",encoding="utf-8") as f:
        for u in users:
            f.write(" | ".join(u) + "\n")
    messagebox.showinfo("Done", "TXT Exported as export_users.txt")

# Export CSV
def export_csv():
    df = pd.DataFrame(load_users(), columns=cols)
    df.to_csv("export_users.csv", index=False, encoding="utf-8")
    messagebox.showinfo("Done", "CSV Exported as export_users.csv")


# Export Excel
def export_excel():
    df=pd.DataFrame(load_users(),columns=cols)
    df.to_excel("export_users.xlsx",index=False)
    messagebox.showinfo("Done","Excel Exported")

# Buttons
frame=tk.Frame(root,bg="#0e1013")
frame.pack()

tk.Button(frame,text="View Password",command=decrypt_selected,bg="#1e90ff",fg="white",width=15).grid(row=0,column=0,padx=10,pady=10)
tk.Button(frame,text="Delete User",command=delete_user,bg="#d9534f",fg="white",width=15).grid(row=0,column=1,padx=10,pady=10)
tk.Button(frame,text="Export PDF",command=export_pdf,bg="#5cb85c",fg="white",width=15).grid(row=0,column=2,padx=10,pady=10)
tk.Button(frame,text="Export Excel",command=export_excel,bg="#f0ad4e",fg="white",width=15).grid(row=0,column=3,padx=10,pady=10)
tk.Button(frame,text="📁 Export TXT",command=export_txt,bg="#6f42c1",**btn_style).grid(row=1,column=0,padx=10,pady=5)
tk.Button(frame,text="🧾 Export CSV",command=export_csv,bg="#20c997",**btn_style).grid(row=1,column=1,padx=10,pady=5)
tk.Button(frame,text="📈 Graph",command=show_graph,bg="#17a2b8",**btn_style).grid(row=1,column=2,padx=10,pady=5)
tk.Button(frame,text="🔄 Refresh",command=refresh_data,bg="#ffc107",**btn_style).grid(row=1,column=3,padx=10,pady=5)
tk.Button(frame,text="➕ Add User",command=add_user_window,bg="#28a745",**btn_style).grid(row=2,column=0,padx=10,pady=10)
tk.Button(frame, text="View Activity Logs", command=view_logs, bg="#00bfff",fg="white", width=15).grid(row=2,column=1,padx=10,pady=10)





root.mainloop()



