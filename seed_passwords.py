"""
seed_passwords.py
-----------------
Run this ONCE after importing aware_db.sql to replace the placeholder
passwords with properly hashed values.

Usage:
    python seed_passwords.py

Requirements: pip install mysql-connector-python werkzeug
"""

import mysql.connector
from werkzeug.security import generate_password_hash

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "aware_db",
}

STUDENT_CREDENTIALS = [
    (2024001, "student123"),
    (2024002, "student123"),
]

PROFESSOR_CREDENTIALS = [
    (101, "prof123"),
    (102, "prof123"),
    (103, "prof123"),
]


def seed():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print("Seeding student passwords...")
    for student_id, plain_password in STUDENT_CREDENTIALS:
        hashed = generate_password_hash(plain_password)
        cursor.execute(
            "UPDATE student SET Password = %s WHERE Student_ID = %s",
            (hashed, student_id),
        )
        print(f"  Student {student_id} updated.")

    print("Seeding professor passwords...")
    for professor_id, plain_password in PROFESSOR_CREDENTIALS:
        hashed = generate_password_hash(plain_password)
        cursor.execute(
            "UPDATE professor SET Password = %s WHERE Professor_ID = %s",
            (hashed, professor_id),
        )
        print(f"  Professor {professor_id} updated.")

    conn.commit()
    cursor.close()
    conn.close()
    print("\nAll passwords seeded successfully!")


if __name__ == "__main__":
    seed()
