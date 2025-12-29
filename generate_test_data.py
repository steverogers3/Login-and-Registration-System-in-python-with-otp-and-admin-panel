# generate_key.py
from cryptography.fernet import Fernet

with open("key.key","wb") as f:
    f.write(Fernet.generate_key())

print("key.key generated ✔ Keep this file safe!")
