from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)


# --- Database Connection ---
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="aware_db"
        )
    except mysql.connector.Error as err:
        print(f"MySQL Connection Error: {err}")
        return None


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # 1. Hardcoded Demo Credentials (Fallback)
    DEMO_USERS = {
        "admin@tip.edu.ph": "admin123",
        "student@tip.edu.ph": "student123",
        "admin@university.edu": "admin123",
        "student@university.edu": "student123",
    }

    # check hardcoded first
    if email in DEMO_USERS and DEMO_USERS[email] == password:
        return jsonify(
            {"status": "success", "user": {"name": "Demo User", "email": email}}
        ), 200

    # 2. Database Lookup (Real Authentication)
    db = get_db_connection()
    if db:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
            user = cursor.fetchone()

            # Verify hashed password
            if user and check_password_hash(user["password"], password):
                return jsonify(
                    {
                        "status": "success",
                        "user": {"name": user["name"], "email": user["email"]},
                    }
                ), 200
        except Exception as e:
            print(f"Database Query Error: {e}")
        finally:
            db.close()

    # 3. Fail if neither worked
    return jsonify(
        {
            "status": "error",
            "message": "Incorrect username or password. Please try again.",
        }
    ), 401


# --- Sign Up Route ---
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    db = get_db_connection()
    if not db:
        return jsonify(
            {"status": "error", "message": "Database connection failed"}
        ), 500

    cursor = db.cursor()
    try:
        # check if email exists
        cursor.execute("SELECT id FROM students WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify(
                {"status": "error", "message": "Email already registered"}
            ), 409

        # security: Hash the password
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password),
        )
        db.commit()
        return jsonify({"status": "success", "message": "User created!"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
