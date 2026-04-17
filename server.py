import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import math

# FOR LOCAL ONLY
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
CORS(app)

# --- GLOBAL TIME MACHINE FOR TESTING ---
GLOBAL_TEST_DATE = None
# GLOBAL_TEST_DATE = date(2026, 4, 8)

# ==========================================
# SEMESTER SCHEDULE CONFIGURATION
# ==========================================
SEMESTER_START = date(2025, 12, 9)
SEMBREAK_START = date(2025, 12, 20)
SEMBREAK_END = date(2026, 1, 5)
CLASSES_RESUME = date(2026, 1, 6)
SEMESTER_END = date(2026, 4, 25)

# --- Database Connection ---
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_ca="ca.pem"
    )

# --- Login Route ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    role = data.get("role", "professor")

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required."}), 400

    try:
        db = get_db_connection()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    cursor = db.cursor(dictionary=True)
    try:
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

        else:  
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
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT Course_Code, Course_Title FROM course")
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/get_topics", methods=["GET"])
def get_topics():
    course_code = request.args.get('course')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT Session_ID, Topic FROM class_session WHERE Course_Code = %s", (course_code,))
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
        
# --- Dashboard Data Route ---
@app.route("/api/get_dashboard_data", methods=["GET"])
def get_dashboard_data():
    prof_id = request.args.get('prof_id') 
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        where_clause = "WHERE cs.Professor_ID = %s" if prof_id else ""
        params = (prof_id,) if prof_id else ()

        cursor.execute(f"""
            SELECT AVG(e.Pacing_Score) AS avg_pacing, AVG(e.Comprehension_Score) AS avg_comp
            FROM evaluation e JOIN class_session cs ON e.Session_ID = cs.Session_ID {where_clause}
        """, params)
        averages = cursor.fetchone()

        cursor.execute(f"""
            SELECT cs.Course_Code, cs.Topic, e.Clarity_Score, e.Pacing_Score, e.Comprehension_Score,
                e.Engagement_Score, e.Study_Hours, e.Additional_Comments AS Comments, e.Submission_Date,
                CONCAT(p.First_Name, ' ', p.Last_Name) AS Professor_Name,
                CONCAT(s.First_Name, ' ', s.Last_Name) AS Student_Name
            FROM evaluation e
            JOIN class_session cs ON e.Session_ID = cs.Session_ID
            JOIN course c ON cs.Course_Code = c.Course_Code
            JOIN professor p ON cs.Professor_ID = p.Professor_ID 
            JOIN student s ON e.Student_ID = s.Student_ID
            {where_clause} ORDER BY e.Evaluation_ID DESC
        """, params)
        evaluations = cursor.fetchall()

        for ev in evaluations:
            sub_date = ev.get("Submission_Date")
            if sub_date:
                week_info = calculate_week(sub_date)
                ev["Week_Status"] = week_info["status"]
                ev["Week_Number"] = week_info["week_number"]
                ev["Submission_Date"] = sub_date.strftime("%Y-%m-%d %H:%M") 
            else:
                ev["Week_Status"] = "Old Data"
                ev["Week_Number"] = 0

        return jsonify({"averages": averages, "evaluations": evaluations}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# --- Submit Evaluation Route ---
@app.route("/submit_evaluation", methods=["POST"])
def submit_evaluation():
    try:
        db = get_db_connection()
        data = request.json

        student_id = data.get("student_id")
        session_id = data.get("session_id")

        clarity_score = data.get("clarity_score")
        pacing_score = data.get("pacing_score")
        comprehension_score = data.get("comprehension_score")
        engagement_score = data.get("engagement_score")

        study_hours = data.get("study_hours", 0)

        try:
            study_hours = float(study_hours)
        except (TypeError, ValueError):
            study_hours = 0.0

        # 🔥 ADD THIS RULE (CRITICAL FOR YOUR STREAK SYSTEM)
        if study_hours < 1:
            return jsonify({
                "status": "success",
                "message": "Evaluation saved but streak NOT updated (insufficient study hours)."
            }), 200

        comments = data.get("comments", "")

        cursor = db.cursor(dictionary=True)

        # Duplicate Submission Prevention/check
        cursor.execute("""
            SELECT COUNT(*) AS count
            FROM evaluation
            WHERE Student_ID = %s AND Session_ID = %s
        """, (student_id, session_id))

        result = cursor.fetchone()

        if result["count"] > 0:
            return jsonify({"status": "error", "message": "Session already evaluated."}), 400

        # Insert evaluation
        submission_date = GLOBAL_TEST_DATE or datetime.now().date()

        cursor.execute("""
            INSERT INTO evaluation 
            (Session_ID, Student_ID, Clarity_Score, Pacing_Score, Comprehension_Score,
             Engagement_Score, Study_Hours, Additional_Comments, Submission_Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            session_id,
            student_id,
            clarity_score,
            pacing_score,
            comprehension_score,
            engagement_score,
            study_hours,
            comments,
            submission_date
        ))

        db.commit()

        # ---- STREAK LOGIC ----
        today = submission_date  # OK, but better rename for clarity

        cursor.execute("""
            SELECT streak_count, best_streak, last_study_date, freeze_count
            FROM student
            WHERE Student_ID = %s
        """, (student_id,))

        student = cursor.fetchone()

        if student:
            streak = student["streak_count"] or 0
            best = student["best_streak"] or 0
            last_date = student["last_study_date"]
            freeze_count = student["freeze_count"] or 0

            new_streak = 1
            used_freeze = False

            if last_date:
                if isinstance(last_date, str):
                    last_date = datetime.strptime(last_date, "%Y-%m-%d").date()

                diff = (today - last_date).days

                if diff == 1:
                    new_streak = streak + 1
                elif diff == 0:
                    new_streak = streak
                else:
                    if freeze_count > 0:
                        new_streak = streak
                        freeze_count -= 1
                        used_freeze = True
                    else:
                        new_streak = 1

            if streak < 3 and new_streak >= 3 and freeze_count == 0:
                freeze_count += 1

            new_best = max(best, new_streak)

            cursor.execute("""
                UPDATE student
                SET streak_count=%s,
                    best_streak=%s,
                    last_study_date=%s,
                    freeze_count=%s,
                    streak_frozen=%s
                WHERE Student_ID=%s
            """, (
                new_streak,
                new_best,
                today,
                freeze_count,
                1 if used_freeze else 0,
                student_id
            ))

            db.commit()

        return jsonify({"status": "success", "message": "Evaluation submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        try:
            db.close()
        except:
            pass
# --- Student Stats Route ---
@app.route("/api/get_student_stats", methods=["GET"])
def get_student_stats():
    student_id = request.args.get('student_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as total FROM evaluation WHERE Student_ID = %s", (student_id,))
        total_submissions = cursor.fetchone()['total']

        cursor.execute("SELECT streak_count, freeze_count, best_streak FROM student WHERE Student_ID = %s", (student_id,))
        streak_data = cursor.fetchone()
        
        cursor.execute("""
            SELECT cs.Course_Code, cs.Topic, e.Comprehension_Score, e.Engagement_Score 
            FROM evaluation e JOIN class_session cs ON e.Session_ID = cs.Session_ID
            WHERE e.Student_ID = %s ORDER BY e.Evaluation_ID DESC LIMIT 3
        """, (student_id,))
        recent_evals = cursor.fetchall()
        
        return jsonify({
            "total_submissions": total_submissions,
            "recent_evals": recent_evals,
            "streak": streak_data["streak_count"] if streak_data else 0,
            "freeze": streak_data["freeze_count"] if streak_data else 0,
            "best_streak": streak_data["best_streak"] if streak_data else 0
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# --- Date Calculation ---
def calculate_week(target_date):
    if isinstance(target_date, datetime):
        target_date = target_date.date()
    elif isinstance(target_date, str):
        target_date = datetime.strptime(target_date, '%Y-%m-%d %H:%M:%S').date()

    if target_date < SEMESTER_START or target_date > SEMESTER_END: 
        return {"status": "Semester Ended" if target_date > SEMESTER_END else "Not Started", "week_number": 0}
        
    if SEMBREAK_START <= target_date <= SEMBREAK_END: 
        return {"status": "Sembreak", "week_number": 0}
        
    if SEMESTER_START <= target_date < SEMBREAK_START:
        week = math.floor((target_date - SEMESTER_START).days / 7) + 1
        return {"status": "Active", "week_number": week}
        
    if target_date >= CLASSES_RESUME:
        week = math.floor((11 + (target_date - CLASSES_RESUME).days) / 7) + 1
        status = "Prelim Exam Week" if week == 6 else "Midterm Exam Week" if week == 12 else "Final Exam Week" if week == 18 else "Active"
        return {"status": status, "week_number": week}
        
    return {"status": "Unknown", "week_number": 0}

@app.route('/api/week', methods=['GET'])
def get_week():
    test_date_str = request.args.get('test_date')
    if test_date_str:
        try: target_date = datetime.strptime(test_date_str, '%Y-%m-%d')
        except ValueError: return jsonify({"error": "Invalid date format"}), 400
    else: target_date = GLOBAL_TEST_DATE if GLOBAL_TEST_DATE else datetime.now()
    return jsonify(calculate_week(target_date))

@app.route("/api/analytics/grades_vs_evals", methods=["GET"])
def get_grades_vs_evals():
    prof_id = request.args.get('prof_id') 
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        where_clause = "WHERE cs.Professor_ID = %s" if prof_id else ""
        params = (prof_id,) if prof_id else ()
        cursor.execute(f"""
            SELECT CONCAT(s.First_Name, ' ', s.Last_Name) AS Student_Name, en.Course_Code, en.Current_Grade,
                AVG(ev.Comprehension_Score) AS Avg_Comprehension, SUM(ev.Study_Hours) AS Total_Study_Hours
            FROM enrollment en
            JOIN student s ON en.Student_ID = s.Student_ID
            JOIN class_session cs ON en.Course_Code = cs.Course_Code
            JOIN evaluation ev ON cs.Session_ID = ev.Session_ID AND en.Student_ID = ev.Student_ID
            {where_clause} GROUP BY en.Student_ID, en.Course_Code, en.Current_Grade
        """, params)
        return jsonify({"status": "success", "data": cursor.fetchall()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: PROFESSORS
# ==========================================
@app.route('/api/admin/professors', methods=['GET', 'POST'])
def api_professors():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("SELECT Professor_ID, First_Name, Last_Name, Username, Department FROM professor ORDER BY Last_Name")
            return jsonify({"status": "success", "data": cursor.fetchall()}), 200
        elif request.method == 'POST':
            data = request.json
            hashed_pw = generate_password_hash(data['Password'])
            cursor.execute("""
                INSERT INTO professor (First_Name, Last_Name, Username, Password, Department) 
                VALUES (%s, %s, %s, %s, %s)
            """, (data['First_Name'], data['Last_Name'], data['Username'], hashed_pw, data.get('Department', '')))
            db.commit()
            return jsonify({"status": "success", "message": "Professor added!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/professors/<int:prof_id>', methods=['PUT', 'DELETE'])
def api_modify_professor(prof_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM evaluation WHERE Session_ID IN (SELECT Session_ID FROM class_session WHERE Professor_ID = %s)", (prof_id,))
            cursor.execute("DELETE FROM class_session WHERE Professor_ID = %s", (prof_id,))
            cursor.execute("DELETE FROM professor WHERE Professor_ID = %s", (prof_id,))
            db.commit()
            return jsonify({"status": "success", "message": "Professor deleted!"}), 200
        elif request.method == 'PUT':
            data = request.json
            if data.get('Password') and data['Password'].strip() != "":
                cursor.execute("UPDATE professor SET First_Name=%s, Last_Name=%s, Username=%s, Password=%s, Department=%s WHERE Professor_ID=%s",
                               (data['First_Name'], data['Last_Name'], data['Username'], generate_password_hash(data['Password']), data.get('Department', ''), prof_id))
            else:
                cursor.execute("UPDATE professor SET First_Name=%s, Last_Name=%s, Username=%s, Department=%s WHERE Professor_ID=%s",
                               (data['First_Name'], data['Last_Name'], data['Username'], data.get('Department', ''), prof_id))
            db.commit()
            return jsonify({"status": "success", "message": "Professor updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: GUARDIANS
# ==========================================
@app.route('/api/admin/guardians', methods=['GET', 'POST'])
def api_guardians():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("SELECT * FROM guardian ORDER BY Last_Name")
            return jsonify({"status": "success", "data": cursor.fetchall()}), 200
        elif request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO guardian (First_Name, Last_Name, Contact_Number, Email) VALUES (%s, %s, %s, %s)",
                           (data['First_Name'], data['Last_Name'], data.get('Contact_Number'), data.get('Email')))
            db.commit()
            return jsonify({"status": "success", "message": "Guardian added!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/guardians/<int:g_id>', methods=['PUT', 'DELETE'])
def api_modify_guardian(g_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if request.method == 'DELETE':
            cursor.execute("UPDATE student SET Guardian_ID = NULL WHERE Guardian_ID = %s", (g_id,))
            cursor.execute("DELETE FROM guardian WHERE Guardian_ID = %s", (g_id,))
            db.commit()
            return jsonify({"status": "success", "message": "Guardian deleted!"}), 200
        elif request.method == 'PUT':
            data = request.json
            cursor.execute("UPDATE guardian SET First_Name=%s, Last_Name=%s, Contact_Number=%s, Email=%s WHERE Guardian_ID=%s",
                           (data['First_Name'], data['Last_Name'], data.get('Contact_Number'), data.get('Email'), g_id))
            db.commit()
            return jsonify({"status": "success", "message": "Guardian updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: STUDENTS
# ==========================================
@app.route('/api/admin/students', methods=['GET', 'POST'])
def api_students():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT s.Student_ID, s.First_Name, s.Last_Name, s.Username, s.Guardian_ID, 
                       CONCAT(g.First_Name, ' ', g.Last_Name) AS Guardian_Name
                FROM student s LEFT JOIN guardian g ON s.Guardian_ID = g.Guardian_ID ORDER BY s.Last_Name
            """)
            return jsonify({"status": "success", "data": cursor.fetchall()}), 200
        elif request.method == 'POST':
            data = request.json
            g_id = data.get('Guardian_ID') or None
            cursor.execute("INSERT INTO student (First_Name, Last_Name, Username, Password, Guardian_ID) VALUES (%s, %s, %s, %s, %s)",
                           (data['First_Name'], data['Last_Name'], data['Username'], generate_password_hash(data['Password']), g_id))
            db.commit()
            return jsonify({"status": "success", "message": "Student added!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/students/<int:student_id>', methods=['PUT', 'DELETE'])
def api_modify_student(student_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM evaluation WHERE Student_ID = %s", (student_id,))
            cursor.execute("DELETE FROM enrollment WHERE Student_ID = %s", (student_id,))
            cursor.execute("DELETE FROM student WHERE Student_ID = %s", (student_id,))
            db.commit()
            return jsonify({"status": "success", "message": "Student deleted!"}), 200
        elif request.method == 'PUT':
            data = request.json
            g_id = data.get('Guardian_ID') or None
            if data.get('Password') and data['Password'].strip() != "":
                cursor.execute("UPDATE student SET First_Name=%s, Last_Name=%s, Username=%s, Password=%s, Guardian_ID=%s WHERE Student_ID=%s",
                               (data['First_Name'], data['Last_Name'], data['Username'], generate_password_hash(data['Password']), g_id, student_id))
            else:
                cursor.execute("UPDATE student SET First_Name=%s, Last_Name=%s, Username=%s, Guardian_ID=%s WHERE Student_ID=%s",
                               (data['First_Name'], data['Last_Name'], data['Username'], g_id, student_id))
            db.commit()
            return jsonify({"status": "success", "message": "Student updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: COURSES
# ==========================================
@app.route('/api/admin/courses', methods=['GET', 'POST'])
def api_courses():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("SELECT Course_Code, Course_Title FROM course ORDER BY Course_Code")
            return jsonify({"status": "success", "data": cursor.fetchall()}), 200
        elif request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO course (Course_Code, Course_Title) VALUES (%s, %s)", 
                           (data['Course_Code'].upper(), data.get('Course_Title', '')))
            db.commit()
            return jsonify({"status": "success", "message": "Course added!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/courses/<string:course_code>', methods=['PUT', 'DELETE'])
def api_modify_course(course_code):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM evaluation WHERE Session_ID IN (SELECT Session_ID FROM class_session WHERE Course_Code = %s)", (course_code,))
            cursor.execute("DELETE FROM class_session WHERE Course_Code = %s", (course_code,))
            cursor.execute("DELETE FROM class_schedule WHERE Course_Code = %s", (course_code,))
            cursor.execute("DELETE FROM enrollment WHERE Course_Code = %s", (course_code,))
            cursor.execute("DELETE FROM course WHERE Course_Code = %s", (course_code,))
            db.commit()
            return jsonify({"status": "success", "message": "Course deleted!"}), 200
        elif request.method == 'PUT':
            data = request.json
            cursor.execute("UPDATE course SET Course_Title = %s WHERE Course_Code = %s", 
                           (data.get('Course_Title', ''), course_code))
            db.commit()
            return jsonify({"status": "success", "message": "Course updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: SCHEDULES
# ==========================================
@app.route('/api/admin/schedules', methods=['GET', 'POST'])
def api_schedules():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            # FIX: Pulling Room_Name and Schedule_Day based on actual DB schema
            cursor.execute("""
                SELECT Schedule_ID, Course_Code, Room_Name, Schedule_Day, 
                       TIME_FORMAT(Start_Time, '%H:%i') AS Start_Time, 
                       TIME_FORMAT(End_Time, '%H:%i') AS End_Time
                FROM class_schedule ORDER BY Schedule_Day, Start_Time
            """)
            return jsonify({"status": "success", "data": cursor.fetchall()}), 200
        elif request.method == 'POST':
            data = request.json
            cursor.execute("""
                INSERT INTO class_schedule (Course_Code, Room_Name, Schedule_Day, Start_Time, End_Time) 
                VALUES (%s, %s, %s, %s, %s)
            """, (data['Course_Code'], data['Room_Name'], data['Schedule_Day'], data['Start_Time'], data['End_Time']))
            db.commit()
            return jsonify({"status": "success", "message": "Schedule added!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/schedules/<int:sched_id>', methods=['PUT', 'DELETE'])
def api_modify_schedule(sched_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM class_schedule WHERE Schedule_ID = %s", (sched_id,))
            db.commit()
            return jsonify({"status": "success", "message": "Schedule deleted!"}), 200
        elif request.method == 'PUT':
            data = request.json
            cursor.execute("""
                UPDATE class_schedule SET Course_Code=%s, Room_Name=%s, Schedule_Day=%s, Start_Time=%s, End_Time=%s 
                WHERE Schedule_ID=%s
            """, (data['Course_Code'], data['Room_Name'], data['Schedule_Day'], data['Start_Time'], data['End_Time'], sched_id))
            db.commit()
            return jsonify({"status": "success", "message": "Schedule updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: SESSIONS
# ==========================================
@app.route('/api/admin/sessions', methods=['GET', 'POST'])
def api_sessions():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            # FIX: Pulling Course_Code and Professor_ID based on actual DB Schema
            cursor.execute("""
                SELECT Session_ID, Course_Code, Professor_ID, DATE_FORMAT(Session_Date, '%Y-%m-%d') as Session_Date, Topic
                FROM class_session ORDER BY Session_Date DESC
            """)
            return jsonify({"status": "success", "data": cursor.fetchall()}), 200
        elif request.method == 'POST':
            data = request.json
            cursor.execute("INSERT INTO class_session (Course_Code, Professor_ID, Session_Date, Topic) VALUES (%s, %s, %s, %s)", 
                           (data['Course_Code'], data['Professor_ID'], data['Session_Date'], data.get('Topic', '')))
            db.commit()
            return jsonify({"status": "success", "message": "Class Session created!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/sessions/<int:session_id>', methods=['PUT', 'DELETE'])
def api_modify_session(session_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM evaluation WHERE Session_ID = %s", (session_id,))
            cursor.execute("DELETE FROM class_session WHERE Session_ID = %s", (session_id,))
            db.commit()
            return jsonify({"status": "success", "message": "Session deleted!"}), 200
        elif request.method == 'PUT':
            data = request.json
            cursor.execute("""
                UPDATE class_session SET Course_Code=%s, Professor_ID=%s, Session_Date=%s, Topic=%s WHERE Session_ID=%s
            """, (data['Course_Code'], data['Professor_ID'], data['Session_Date'], data.get('Topic', ''), session_id))
            db.commit()
            return jsonify({"status": "success", "message": "Session updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: ENROLLMENTS
# ==========================================
@app.route('/api/admin/enrollments', methods=['GET', 'POST'])
def api_enrollments():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT e.Enrollment_ID, e.Student_ID, e.Course_Code, e.Academic_Year, e.Semester, e.Current_Grade,
                       CONCAT(s.First_Name, ' ', s.Last_Name) AS Student_Name
                FROM enrollment e JOIN student s ON e.Student_ID = s.Student_ID ORDER BY s.Last_Name
            """)
            return jsonify({"status": "success", "data": cursor.fetchall()}), 200
        elif request.method == 'POST':
            data = request.json
            grade = data.get('Current_Grade') or None 
            cursor.execute("""
                INSERT INTO enrollment (Student_ID, Course_Code, Academic_Year, Semester, Current_Grade) 
                VALUES (%s, %s, %s, %s, %s)
            """, (data['Student_ID'], data['Course_Code'], data['Academic_Year'], data['Semester'], grade))
            db.commit()
            return jsonify({"status": "success", "message": "Student Enrolled!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/enrollments/<int:enroll_id>', methods=['DELETE', 'PUT'])
def api_modify_enrollment(enroll_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM enrollment WHERE Enrollment_ID = %s", (enroll_id,))
            db.commit()
            return jsonify({"status": "success", "message": "Enrollment deleted!"}), 200
        elif request.method == 'PUT':
            data = request.json
            
            cursor.execute("""
                UPDATE enrollment 
                SET Student_ID=%s, Course_Code=%s, Academic_Year=%s, Semester=%s, Current_Grade=%s 
                WHERE Enrollment_ID=%s
            """, (
                data.get('Student_ID'), 
                data.get('Course_Code'), 
                data.get('Academic_Year'), 
                data.get('Semester'), 
                data.get('Current_Grade') or None, 
                enroll_id
            ))
            db.commit()
            return jsonify({"status": "success", "message": "Enrollment updated!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# ==========================================
# ADMIN CRUD: EVALUATIONS
# ==========================================
@app.route('/api/admin/evaluations', methods=['GET'])
def api_evaluations():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT ev.*, cs.Course_Code, DATE_FORMAT(ev.Submission_Date, '%a, %b %d, %Y') AS Formatted_Date
            FROM evaluation ev LEFT JOIN class_session cs ON ev.Session_ID = cs.Session_ID ORDER BY ev.Evaluation_ID DESC
        """)
        return jsonify({"status": "success", "data": cursor.fetchall()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/admin/evaluations/<int:eval_id>', methods=['DELETE'])
def api_delete_evaluation(eval_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM evaluation WHERE Evaluation_ID = %s", (eval_id,))
        db.commit()
        return jsonify({"status": "success", "message": "Evaluation deleted!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)