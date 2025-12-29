# login.py (Final fixed version with OTP)
import sys
sys.stdout.reconfigure(encoding='utf-8')

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import os
import bcrypt
from cryptography.fernet import Fernet



BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "logdata.txt")
KEY_FILE = os.path.join(BASE, "key.key")

# Load Encryption Key
with open(KEY_FILE, "rb") as file:
    key = file.read()
fernet = Fernet(key)

# OTP auto import
try:
    from otp_sender import otp_verify
    OTP_AVAILABLE = True
except:
    OTP_AVAILABLE = False


# ================= LOAD USERS =================
def load_users():
    users = []
    if not os.path.exists(DATA_FILE):
        return users

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) < 6:
                continue

            users.append({
                "username": parts[0],
                "hashed_password": parts[1],
                "encrypted_password": parts[2],
                "mobile": parts[3],
                "email": parts[4],
                "age": parts[5]
            })
    return users


# ================= SAVE USER =================
def save_user(username, hashed_password, encrypted_password, mobile, email, age):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}|{hashed_password}|{encrypted_password}|{mobile}|{email}|{age}\n")


# ================= REGISTER =================
def register():
    users = load_users()

    print("\n--- Register ---")
    username = input("Username: ")
    


    if any(u["username"] == username for u in users):
        print("❌ Username already exists")
        return

    password = input("Password (min 6 chars): ")
    if len(password) < 6:
        print("❌ Too short!")
        return

    mobile = input("Mobile: ")
    email = input("Email: ")
    age = input("Age: ")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    encrypted = fernet.encrypt(password.encode()).decode()

    save_user(username, hashed, encrypted, mobile, email, age)
    print("✔ Registered Successfully!")
    

# ================= LOGIN with OTP =================
def login():
    users = load_users()

    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = next((u for u in users if u["username"] == username), None)

    if not user:
        print("❌ User not found")
        return

    if not bcrypt.checkpw(password.encode(), user["hashed_password"].encode()):
        print("❌ Wrong Password")
        return
    
    #Call OTP system if available
    if OTP_AVAILABLE:
        if otp_verify(user["email"]):
           print(f"✔ Login Successful! Welcome {username}")
        else:
            print("❌ Login Failed (OTP incorrect)")
            return
        
    else:
        print("⚠ OTP sender missing, logged in without OTP.")

    print(f"Mobile: {user['mobile']} | Email: {user['email']} | Age: {user['age']}")



# ================= ADMIN PANEL =================
def admin_auth():
    admin_pass = "admin123"
    return input("Admin Password: ") == admin_pass


def admin_view():
    if not admin_auth():
        print("❌ Wrong admin password")
        return

    users = load_users()
    username = input("Enter username: ")

    user = next((u for u in users if u["username"] == username), None)
    if not user:
        print("❌ User not found")
        return

    decrypted = fernet.decrypt(user["encrypted_password"].encode()).decode()
    print(f"\n🔐 Password for {username}: {decrypted}")
    print(f"📱 {user['mobile']} | ✉ {user['email']} | 🧒 {user['age']}")


# ================= MENU =================
while True:
    print("\n📌 MENU:")
    print("1) Register")
    print("2) Login")
    print("3) Admin - View Password")
    print("4) Quit")

    choice = input("Select: ")

    if choice == "1": register()
    elif choice == "2": login()
    elif choice == "3": admin_view()
    elif choice == "4": break
    else: print("❌ Invalid Choice")
print("👋 Goodbye!")