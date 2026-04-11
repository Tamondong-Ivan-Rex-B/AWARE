"""
seed_passwords.py
-----------------
Run this script whenever you manually add new students or professors 
in phpMyAdmin using plain-text passwords. 

This script will automatically scan the database, find any unprotected 
passwords, hash them securely, and save them back.
"""

import mysql.connector
from werkzeug.security import generate_password_hash

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "aware_db",
}

def seed():
    # Connect to database
    conn = mysql.connector.connect(**DB_CONFIG)
    # Using dictionary=True makes it easier to read column names
    cursor = conn.cursor(dictionary=True) 
    update_cursor = conn.cursor() # Separate cursor for making changes

    # --- 1. SCAN STUDENTS ---
    print("Scanning student accounts...")
    cursor.execute("SELECT Student_ID, Username, Password FROM student")
    students = cursor.fetchall()

    for student in students:
        s_id = student['Student_ID']
        username = student['Username']
        current_pass = student['Password']

        # Check if the password is empty, NULL, or already properly hashed
        if current_pass is None or current_pass == "":
            print(f"  [!] Skipped Student {username} (No password set)")
        elif current_pass.startswith(('scrypt:', 'pbkdf2:')):
            pass # Already secured, do nothing quietly
        else:
            # It's plain text! Hash it and update the database.
            hashed = generate_password_hash(current_pass)
            update_cursor.execute(
                "UPDATE student SET Password = %s WHERE Student_ID = %s",
                (hashed, s_id)
            )
            print(f"  [✓] Secured password for Student: {username}")

    # --- 2. SCAN PROFESSORS ---
    print("\nScanning professor accounts...")
    cursor.execute("SELECT Professor_ID, Username, Password FROM professor")
    professors = cursor.fetchall()

    for prof in professors:
        p_id = prof['Professor_ID']
        username = prof['Username']
        current_pass = prof['Password']

        if current_pass is None or current_pass == "":
            print(f"  [!] Skipped Professor {username} (No password set)")
        elif current_pass.startswith(('scrypt:', 'pbkdf2:')):
            pass # Already secured
        else:
            # It's plain text! Hash it.
            hashed = generate_password_hash(current_pass)
            update_cursor.execute(
                "UPDATE professor SET Password = %s WHERE Professor_ID = %s",
                (hashed, p_id)
            )
            print(f"  [✓] Secured password for Professor: {username}")

    # --- 3. SCAN ADMINS ---
    print("\nScanning admin accounts...")
    cursor.execute("SELECT Admin_ID, Username, Password FROM admin")
    admins = cursor.fetchall()

    for admin in admins:
        a_id = admin['Admin_ID']
        username = admin['Username']
        current_pass = admin['Password']

        if current_pass is None or current_pass == "":
            print(f"  [!] Skipped Admin {username} (No password set)")
        elif current_pass.startswith(('scrypt:', 'pbkdf2:')):
            pass # Already secured
        else:
            # It's plain text! Hash it.
            hashed = generate_password_hash(current_pass)
            update_cursor.execute(
                "UPDATE admin SET Password = %s WHERE Admin_ID = %s",
                (hashed, a_id)
            )
            print(f"  [✓] Secured password for Admin: {username}")

    # Save changes and close connections
    conn.commit()
    cursor.close()
    update_cursor.close()
    conn.close()
    print("\nDatabase scan complete! All passwords are now secure.")

if __name__ == "__main__":
    seed()