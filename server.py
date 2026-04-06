from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
# CORS allows your HTML website to talk to this Python server
CORS(app) 

# Helper function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Default XAMPP username
        password="",          # Default XAMPP password (blank)
        database="aware_db"
    )

# ==========================================
# 1. STUDENT PORTAL ROUTES (Web App)
# ==========================================

@app.route('/api/student_login', methods=['POST'])
def student_login():
    data = request.json
    email = data.get('email', '')
    
    # Extract the Student ID from the email (e.g., "2024001@tip.edu.ph" -> "2024001")
    student_id = email.split('@')[0] 
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Student_ID, First_Name FROM Student WHERE Student_ID = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    db.close()
    
    if student:
        return jsonify({"success": True, "student_id": student['Student_ID'], "first_name": student['First_Name']})
    else:
        return jsonify({"success": False, "message": "Student ID not found in database."}), 401


@app.route('/api/get_courses', methods=['GET'])
def get_courses():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT Course_Code, Course_Title FROM Course")
    courses = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(courses)


@app.route('/api/get_topics', methods=['GET'])
def get_topics():
    course_code = request.args.get('course') 
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    sql = "SELECT Session_ID, Topic FROM Class_Session WHERE Course_Code = %s"
    cursor.execute(sql, (course_code,))
    topics = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(topics)


@app.route('/submit_evaluation', methods=['POST'])
def submit_evaluation():
    data = request.json
    
    # Grab all data from the JS payload
    student_id = data.get('student_id')
    session_id = data.get('session_id') 
    clarity = data.get('clarity_score')
    pacing = data.get('pacing_score')
    comprehension = data.get('comprehension_score')
    engagement = data.get('engagement_score') 
    comments = data.get('comments', '')
    
    db = get_db_connection()
    cursor = db.cursor()
    
    # Insert all 4 scores into the database
    sql = """INSERT INTO Evaluation 
             (Session_ID, Student_ID, Clarity_Score, Pacing_Score, Comprehension_Score, Engagement_Score, Confusing_Point) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)""" 
             
    cursor.execute(sql, (session_id, student_id, clarity, pacing, comprehension, engagement, comments))
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({"message": "Evaluation saved successfully!"})


@app.route('/api/get_student_stats', methods=['GET'])
def get_student_stats():
    student_id = request.args.get('student_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT COUNT(*) as total FROM Evaluation WHERE Student_ID = %s", (student_id,))
    total_subs = cursor.fetchone()['total']
    
    cursor.execute("""
        SELECT c.Course_Code, s.Topic, e.Comprehension_Score, e.Engagement_Score
        FROM Evaluation e
        JOIN Class_Session s ON e.Session_ID = s.Session_ID
        JOIN Course c ON s.Course_Code = c.Course_Code
        WHERE e.Student_ID = %s
        ORDER BY e.Evaluation_ID DESC LIMIT 3
    """, (student_id,))
    recent = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return jsonify({
        "total_submissions": total_subs,
        "recent_evals": recent
    })

# ==========================================
# 2. ADMIN DASHBOARD ROUTES (PyQt6 Desktop App)
# ==========================================

@app.route('/api/get_dashboard_data', methods=['GET'])
def get_dashboard_data():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Fetch all raw evaluations using JOINs to match the new ERD
    cursor.execute("""
        SELECT c.Course_Code, s.Topic, e.Pacing_Score, e.Comprehension_Score, 
               e.Engagement_Score as Workload_Score, 'N/A' as Study_Hours, e.Confusing_Point as Comments
        FROM Evaluation e
        JOIN Class_Session s ON e.Session_ID = s.Session_ID
        JOIN Course c ON s.Course_Code = c.Course_Code
        ORDER BY e.Evaluation_ID DESC
    """)
    evaluations = cursor.fetchall()
    
    # 2. Calculate the averages for the top KPI boxes
    cursor.execute("""
        SELECT 
            AVG(Pacing_Score) as avg_pacing,
            AVG(Comprehension_Score) as avg_comp,
            AVG(Engagement_Score) as avg_workload
        FROM Evaluation
    """)
    averages = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return jsonify({
        "evaluations": evaluations,
        "averages": averages
    })

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)