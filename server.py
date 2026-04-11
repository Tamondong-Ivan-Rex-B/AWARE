from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import math

app = Flask(__name__)
CORS(app)

# --- GLOBAL TIME MACHINE FOR TESTING ---
# Change this date to test different weeks. 
# Set to None when you want to use Real Time:
GLOBAL_TEST_DATE = None
#GLOBAL_TEST_DATE = datetime(2026, 3, 26)

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
    role = data.get("role", "professor") # Default to professor

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required."}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = db.cursor(dictionary=True)
    try:
        # NEW: Hardcoded Admin bypass for the prototype
        # NEW: Database-driven Admin Login
        if role == "admin":
            cursor.execute("SELECT * FROM admin WHERE Username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user["Password"], password):
                return jsonify({
                    "status": "success", 
                    "role": "admin", 
                    "user": {
                        "id": user["Admin_ID"], 
                        "name": f"{user['First_Name']} {user['Last_Name']}", 
                        "username": user["Username"]
                    }
                }), 200
            else:
                return jsonify({"status": "error", "message": "Invalid admin credentials."}), 401

        elif role == "professor":
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
        # Determine which date to save (Test Date vs Real Date)
        submission_date = GLOBAL_TEST_DATE if GLOBAL_TEST_DATE else datetime.now()

        # UPDATED: We explicitly added Submission_Date to the INSERT statement
        sql = """INSERT INTO evaluation 
                 (Session_ID, Student_ID, Clarity_Score, Pacing_Score, Comprehension_Score, Engagement_Score, Study_Hours, Additional_Comments, Submission_Date) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Added submission_date to the end of the values
        val = (session_id, student_id, clarity_score, pacing_score, comprehension_score, engagement_score, study_hours, comments, submission_date)
        
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
    prof_id = request.args.get('prof_id') # NEW: Capture the ID
    
    db = get_db_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = db.cursor(dictionary=True)
    try:
        # Setup dynamic SQL filtering
        where_clause = "WHERE cs.Professor_ID = %s" if prof_id else ""
        params = (prof_id,) if prof_id else ()

        # UPDATED: Added JOIN and WHERE clause to averages
        cursor.execute(f"""
            SELECT 
                AVG(e.Pacing_Score) AS avg_pacing,
                AVG(e.Comprehension_Score) AS avg_comp
            FROM evaluation e
            JOIN class_session cs ON e.Session_ID = cs.Session_ID
            {where_clause}
        """, params)
        averages = cursor.fetchone()

        # UPDATED: Added {where_clause} and params to the main query
        cursor.execute(f"""
            SELECT 
                cs.Course_Code,
                cs.Topic,
                e.Clarity_Score,
                e.Pacing_Score,
                e.Comprehension_Score,
                e.Engagement_Score,
                e.Study_Hours,
                e.Additional_Comments AS Comments, 
                e.Submission_Date,
                CONCAT(p.First_Name, ' ', p.Last_Name) AS Professor_Name,
                CONCAT(s.First_Name, ' ', s.Last_Name) AS Student_Name
            FROM evaluation e
            JOIN class_session cs ON e.Session_ID = cs.Session_ID
            JOIN course c ON cs.Course_Code = c.Course_Code
            JOIN professor p ON cs.Professor_ID = p.Professor_ID 
            JOIN student s ON e.Student_ID = s.Student_ID
            {where_clause}
            ORDER BY e.Evaluation_ID DESC
        """, params)
        evaluations = cursor.fetchall()

        # NEW LOGIC: Calculate the week for every single evaluation
        for ev in evaluations:
            sub_date = ev.get("Submission_Date")
            if sub_date:
                week_info = calculate_week(sub_date)
                ev["Week_Status"] = week_info["status"]
                ev["Week_Number"] = week_info["week_number"]
                # Convert the datetime object to a string so it doesn't break JSON
                ev["Submission_Date"] = sub_date.strftime("%Y-%m-%d %H:%M") 
            else:
                ev["Week_Status"] = "Old Data"
                ev["Week_Number"] = 0

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

def calculate_week(target_date):
    start_date = datetime(2025, 12, 9)
    break_start = datetime(2025, 12, 20)
    break_end = datetime(2026, 1, 5)
    resume_date = datetime(2026, 1, 6)

    if target_date < start_date:
        return {"status": "Not Started", "week_number": 0}
    
    if break_start <= target_date <= break_end:
        return {"status": "Sembreak", "week_number": 0}

    if target_date < break_start:
        diff = (target_date - start_date).days
        week = math.floor(diff / 7) + 1
        return {"status": "Active", "week_number": week}

    if target_date >= resume_date:
        days_before_break = 11
        days_after_break = (target_date - resume_date).days
        total_active_days = days_before_break + days_after_break
        week = math.floor(total_active_days / 7) + 1
        
        status = "Active"
        if week == 6: status = "Prelim Exam Week"
        elif week == 12: status = "Midterm Exam Week"
        elif week == 18: status = "Final Exam Week"
        
        return {"status": status, "week_number": week}

@app.route('/api/week', methods=['GET'])
def get_week():
    # Check if a test_date was provided in the URL
    test_date_str = request.args.get('test_date')
    
    if test_date_str:
        try:
            target_date = datetime.strptime(test_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    else:
        target_date = GLOBAL_TEST_DATE if GLOBAL_TEST_DATE else datetime.now()

    result = calculate_week(target_date)
    return jsonify(result)

@app.route("/api/analytics/grades_vs_evals", methods=["GET"])
def get_grades_vs_evals():
    prof_id = request.args.get('prof_id') # NEW: Capture the ID
    
    db = get_db_connection()
    if not db:
        return jsonify({"status": "error", "message": "Database connection failed."}), 500

    cursor = db.cursor(dictionary=True)
    try:
        where_clause = "WHERE cs.Professor_ID = %s" if prof_id else ""
        params = (prof_id,) if prof_id else ()

        cursor.execute(f"""
            SELECT 
                CONCAT(s.First_Name, ' ', s.Last_Name) AS Student_Name,
                en.Course_Code,
                en.Current_Grade,
                AVG(ev.Comprehension_Score) AS Avg_Comprehension,
                SUM(ev.Study_Hours) AS Total_Study_Hours
            FROM enrollment en
            JOIN student s ON en.Student_ID = s.Student_ID
            JOIN class_session cs ON en.Course_Code = cs.Course_Code
            JOIN evaluation ev ON cs.Session_ID = ev.Session_ID AND en.Student_ID = ev.Student_ID
            {where_clause}
            GROUP BY en.Student_ID, en.Course_Code, en.Current_Grade
        """, params)
        data = cursor.fetchall()
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        print(f"Analytics Data Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, port=5001)