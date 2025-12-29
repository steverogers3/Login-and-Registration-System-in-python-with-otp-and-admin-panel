from cryptography.fernet import Fernet
import os


SECRET_KEY = b"pb_0H7TtoNqQi0nEJBPhKBzdkHJ9jKI9XEtnHNCpeHQ="   # your secret encryption key
fernet = Fernet(SECRET_KEY)

DATA_FILE=r"C:\Users\nikhi_yi7g\Downloads\Python Course with Notes\project\login\project\logdata.txt"

# Load users from file
def load_users():
    users = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    # Parse `|`-delimited fields
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) == 6:  # Ensure all fields are present
                        users.append({
                            "name": parts[0],
                            "hashed_password": parts[1],
                            "password": parts[2],  # Encrypted password
                            "mobile": parts[3],
                            "email": parts[4],
                            "age": parts[5]
                        })
                except Exception as e:
                    print(f"Error parsing line: {line}. Error: {e}")
                    continue
    except FileNotFoundError:
        print(f"{DATA_FILE} not found.")
    return users

# Save users to file
def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for u in users:
            # Save fields as `|`-delimited
            f.write(f"{u.get('name', '')}|{u.get('hashed_password', '')}|{u.get('password', '')}|{u.get('mobile', '')}|{u.get('email', '')}|{u.get('age', '')}\n")

# View all users (do NOT show passwords)
def view_users(users):
    if not users:
        print("No users available.")
        return
    print("\n--- All Users ---")
    for i, u in enumerate(users, 1):
        print(f"{i}. Name: {u.get('name')}, Age: {u.get('age')}, Mobile: {u.get('mobile')}, Email: {u.get('email')}")

# Show stats
def show_stats(users):
    if not users:
        print("No users available.")
        return
    
    print("\n--- Statistics ---")
    print(f"Total Users: {len(users)}")
    
    # Age stats
    ages = []
    for u in users:
        try:
            ages.append(int(u.get('age', 0)))
        except:
            pass
    
    if ages:
        print(f"Average Age: {sum(ages) / len(ages):.2f}")
        print(f"Youngest Age: {min(ages)}")
        print(f"Oldest Age: {max(ages)}")
    
    # Email domain count
    domains = {}
    for u in users:
        email = u.get('email', '')
        if '@' in email:
            domain = email.split('@')[1]
            domains[domain] = domains.get(domain, 0) + 1
    
    print("\nEmail Providers:")
    for domain, count in domains.items():
        print(f"  {domain}: {count}")

# Export to TXT (omit password)
def export_txt(users):
    if not users:
        print("No users to export.")
        return
    try:
        with open("export_users.txt", "w", encoding="utf-8") as f:
            f.write("=== USER EXPORT REPORT ===\n")
            f.write("=" * 80 + "\n\n")
            for i, u in enumerate(users, 1):
                f.write(f"{i}. Name: {u.get('name', '')}\n")
                f.write(f"   Age: {u.get('age', '')}\n")
                f.write(f"   Mobile: {u.get('mobile', '')}\n")
                f.write(f"   Email: {u.get('email', '')}\n\n")
        print("Exported to export_users.txt successfully!")
    except Exception as e:
        print(f"Error exporting to TXT: {e}")

# Export to CSV (omit password)
def export_csv(users):
    if not users:
        print("No users to export.")
        return
    try:
        with open("export_users.csv", "w", encoding="utf-8") as f:
            f.write("Name,Age,Mobile,Email\n")
            for u in users:
                name = u.get('name', '').replace(',', '')
                age = u.get('age', '')
                mobile = u.get('mobile', '')
                email = u.get('email', '')
                f.write(f"{name},{age},{mobile},{email}\n")
        print("Exported to export_users.csv successfully!")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

# Export to Excel (tab-separated, omit password)
def export_excel(users):
    if not users:
        print("No users to export.")
        return
    try:
        with open("export_users.xlsx", "w", encoding="utf-8") as f:
            f.write("Name\tAge\tMobile\tEmail\n")
            for u in users:
                f.write(f"{u.get('name','')}\t{u.get('age','')}\t{u.get('mobile','')}\t{u.get('email','')}\n")
        print("Exported to export_users.xlsx successfully!")
    except Exception as e:
        print(f"Error exporting to Excel: {e}")

# Export to PDF (uses reportlab; omits password)
def export_pdf(users):
    if not users:
        print("No users to export.")
        return
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        
        pdf_file = "export_users.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title = Paragraph("USER EXPORT REPORT", styles['Heading1'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        data = [["Name", "Age", "Mobile", "Email"]]
        for u in users[:50000]:
            data.append([
                str(u.get('name', '')),
                str(u.get('age', '')),
                str(u.get('mobile', '')),
                str(u.get('email', ''))
            ])
        
        table = Table(data, colWidths=[100, 80, 120, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        print(f"Exported {min(50000, len(users))} entries to export_users.pdf successfully!")
        
    except ImportError:
        print("reportlab not installed. Install with: pip install reportlab")
    except Exception as e:
        print(f"Error exporting to PDF: {e}")

# Delete user
def delete_user(users):
    email = input("Enter email to delete: ").strip().lower()
    found = False
    for u in users:
        if u.get('email', '').lower() == email:
            users.remove(u)
            found = True
            break
    
    if found:
        save_users(users)
        print("User deleted successfully.")
    else:
        print("User not found.")

# Admin: View decrypted password
def admin_view_password(users):
    username=input("Enter username: ").strip()

    for u in users:
        if u["name"].lower()==username.lower():
            try:
                decrypted=fernet.decrypt(u["password"].encode()).decode()
                print(f"\nPassword → {decrypted}")
            except:
                print("❌ Cannot decrypt — Password may belong to old key")

            return

    print("User not found.")

# Reset user password
def reset_user_password(users):
    email = input("Enter email to reset password: ").strip().lower()
    for u in users:
        if u.get('email', '').lower() == email:
            while True:
                new_password = input("Enter new password (min 6 chars): ").strip()
                if len(new_password) < 6:
                    print("Password too short. Try again.")
                    continue
                confirm_password = input("Confirm new password: ").strip()
                if new_password != confirm_password:
                    print("Passwords do not match. Try again.")
                    continue
                break
            try:
                # Encrypt the new password
                encrypted_password = fernet.encrypt(new_password.encode()).decode()
                u['password'] = encrypted_password
                save_users(users)
                print("Password reset successfully.")
            except Exception as e:
                print("Failed to reset password:", e)
            return
    print("User not found.")

# Admin Panel Menu
def admin_panel():
    print("Welcome to Admin Panel!")
    
    while True:
        print("\n--- Admin Panel Menu ---")
        print("1) View All Users")
        print("2) Show Statistics")
        print("3) Delete User")
        print("4) Export to TXT")
        print("5) Export to CSV")
        print("6) Export to Excel")
        print("7) Export to PDF")
        print("8) Refresh Database")
        print("9) Quit")
        print("10) Reset User Password")
        print("11) View Decrypted Password")  # New menu option
        
        choice = input("Choose option (1-11): ").strip()
        
        users = load_users()
        
        if choice == "1":
            view_users(users)
        elif choice == "2":
            show_stats(users)
        elif choice == "3":
            delete_user(users)
        elif choice == "4":
            export_txt(users)
        elif choice == "5":
            export_csv(users)
        elif choice == "6":
            export_excel(users)
        elif choice == "7":
            export_pdf(users)
        elif choice == "8":
            users = load_users()
            print(f"Database refreshed. {len(users)} users loaded.")
        elif choice == "9":
            print("Goodbye!")
            break
        elif choice == "10":
            reset_user_password(users)
        elif choice == "11":
            admin_view_password(users)
        else:
            print("Invalid option!")

# Run admin panel
if __name__ == "__main__":
    admin_panel()
