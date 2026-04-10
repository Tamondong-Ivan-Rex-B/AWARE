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

# --- Login Route ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    role = data.get("role", "student")

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required."}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = db.cursor(dictionary=True)
    try:
        if role == "professor":
            cursor.execute("SELECT * FROM professor WHERE Username = %s", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user["Password"], password):
                return jsonify({
                    "status": "success",
                    "role": "professor",
                    "user": {
                        "id": user["Professor_ID"],
                        "name": f"{user['First_Name']} {user['Last_Name']}",
                        "username": user["Username"],
                        "department": user["Department"],
                    }
                }), 200
        else:  # default: student
            cursor.execute("SELECT * FROM student WHERE Username = %s", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user["Password"], password):
                return jsonify({
                    "status": "success",
                    "role": "student",
                    "user": {
                        "id": user["Student_ID"],
                        "name": f"{user['First_Name']} {user['Last_Name']}",
                        "username": user["Username"],
                        "program": user["Program"],
                        "year_level": user["Year_Level"],
                    }
                }), 200

        return jsonify({"status": "error", "message": "Incorrect username or password. Please try again."}), 401
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({"status": "error", "message": "An error occurred during login."}), 500
    finally:
        db.close()

# --- Dropdown Routes for Student Dashboard ---
@app.route("/api/get_courses", methods=["GET"])
def get_courses():
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed."}), 500
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT Course_Code, Course_Title FROM course")
        courses = cursor.fetchall()
        return jsonify(courses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/get_topics", methods=["GET"])
def get_topics():
    course_code = request.args.get('course')
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed."}), 500
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT Session_ID, Topic FROM class_session WHERE Course_Code = %s", (course_code,))
        topics = cursor.fetchall()
        return jsonify(topics), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# --- Submit Evaluation Route ---
@app.route("/submit_evaluation", methods=["POST"])
def submit_evaluation():
    data = request.json
    
    # Extract values
    student_id = data.get("student_id")
    session_id = data.get("session_id")
    clarity_score = data.get("clarity_score")
    pacing_score = data.get("pacing_score")
    comprehension_score = data.get("comprehension_score")
    engagement_score = data.get("engagement_score")
    
    # Handle optional fields (default to 0 or empty string if None/missing)
    study_hours = data.get("study_hours")
    if not study_hours or study_hours == "":
        study_hours = 0
    comments = data.get("comments", "")

    db = get_db_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = db.cursor()
    try:
        # Note: 'comments' maps to the 'Confusing_Point' column based on your aware_db.sql structure
        sql = """INSERT INTO evaluation 
                 (Session_ID, Student_ID, Clarity_Score, Pacing_Score, Comprehension_Score, Engagement_Score, Study_Hours, Confusing_Point) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (session_id, student_id, clarity_score, pacing_score, comprehension_score, engagement_score, study_hours, comments)
        
        cursor.execute(sql, val)
        db.commit()
        
        return jsonify({"status": "success", "message": "Evaluation submitted successfully!"}), 200
    except Exception as e:
        db.rollback()
        print(f"Submission Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# --- Dashboard Data Route (For Admin/Professor PyQt App) ---
@app.route("/api/get_dashboard_data", methods=["GET"])
def get_dashboard_data():
    db = get_db_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                AVG(Pacing_Score)        AS avg_pacing,
                AVG(Comprehension_Score) AS avg_comp
            FROM evaluation
        """)
        averages = cursor.fetchone()

        cursor.execute("""
            SELECT 
                cs.Course_Code,
                cs.Topic,
                e.Clarity_Score,
                e.Pacing_Score,
                e.Comprehension_Score,
                e.Engagement_Score,
                e.Study_Hours,
                e.Confusing_Point AS Comments
            FROM evaluation e
            JOIN class_session cs ON e.Session_ID = cs.Session_ID
            ORDER BY e.Evaluation_ID DESC
        """)
        evaluations = cursor.fetchall()

        return jsonify({"averages": averages, "evaluations": evaluations}), 200

    except Exception as e:
        print(f"Dashboard Data Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# --- Student Personal Stats Route ---
@app.route("/api/get_student_stats", methods=["GET"])
def get_student_stats():
    student_id = request.args.get('student_id')
    if not student_id:
        return jsonify({"error": "Missing student ID"}), 400
        
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
        
    cursor = db.cursor(dictionary=True)
    try:
        # 1. Get total number of submissions for this student
        cursor.execute("SELECT COUNT(*) as total FROM evaluation WHERE Student_ID = %s", (student_id,))
        result = cursor.fetchone()
        total_submissions = result['total'] if result else 0
        
        # 2. Get the 3 most recent submissions
        cursor.execute("""
            SELECT 
                cs.Course_Code, 
                cs.Topic, 
                e.Comprehension_Score, 
                e.Engagement_Score 
            FROM evaluation e
            JOIN class_session cs ON e.Session_ID = cs.Session_ID
            WHERE e.Student_ID = %s
            ORDER BY e.Evaluation_ID DESC
            LIMIT 3
        """, (student_id,))
        recent_evals = cursor.fetchall()
        
        return jsonify({
            "total_submissions": total_submissions,
            "recent_evals": recent_evals
        }), 200
        
    except Exception as e:
        print(f"Stats Fetch Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, port=5001)