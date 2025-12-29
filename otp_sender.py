# otp_sender.py
import smtplib
import random
from email.message import EmailMessage
from datetime import datetime


# ================= CONFIG ==================
SENDER_EMAIL = "sample email"            # <--- your gmail
APP_PASSWORD = "sample key"            # <--- your app password
OTP_FILE = r"C:\Users\nikhi_yi7g\Downloads\Python Course with Notes\project\login\project\otpdata.txt"
SETTINGS_FILE = r"C:\Users\nikhi_yi7g\Downloads\Python Course with Notes\project\login\project\otp_settings.txt"
# ============================================


# Check if OTP is enabled
def otp_enabled():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return f.read().strip().split("=")[1].upper() == "ON"
    except:
        return True      # default = ON if file missing


# ========= MAIN FUNCTION (AUTO SYSTEM) =========
def otp_verify(email):
    """
    This function:
    → Generates OTP
    → Emails OTP
    → Stores in otpdata.txt
    → Asks user input
    → Returns True/False
    """

    if not otp_enabled():
        return True   # Silent bypass (no message)

    otp = str(random.randint(100000, 999999))

    # Email Content
    msg = EmailMessage()
    msg["Subject"] = "Your OTP Code"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg.set_content(f"Your OTP is: {otp}\nDo not share it.")

    # Send Email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print(f"\n📩 OTP sent to {email}")
    except Exception as e:
        print("\n❌ OTP sending failed:", e)
        return False

    # Save OTP
    with open(OTP_FILE, "a") as log:
        log.write(f"{datetime.now()} | {email} | {otp}\n")

    # Input Verification
    if input("Enter OTP: ").strip() == otp:
        return True
    return False
# ================== TEST RUN ==================
if __name__ == "__main__":
    test_email = input("Enter email to send OTP: ")
    if otp_verify(test_email):
        print("✔ OTP Verified (Test Successful)")
    else:
        print("❌ OTP Failed")

