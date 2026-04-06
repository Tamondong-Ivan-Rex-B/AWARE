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

# --- ROUTE 1: Save the Student Survey ---
@app.route('/submit_evaluation', methods=['POST'])
def submit_evaluation():
    data = request.json
    
    # Safely extract the data from the frontend JSON
    course = data.get('course')
    topics = data.get('topics')
    pacing = data.get('pacing_score')
    comprehension = data.get('comprehension_score')
    workload = data.get('workload_score')
    hours = data.get('study_hours')
    comments = data.get('comments')
    
    db = get_db_connection()
    cursor = db.cursor()
    
    # Insert the expanded data into the database
    sql = """INSERT INTO Evaluation 
             (Course_Code, Topics, Pacing_Score, Comprehension_Score, Workload_Score, Study_Hours, Comments) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    values = (course, topics, pacing, comprehension, workload, hours, comments)
    
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({"message": "Evaluation saved successfully!"})

# --- ROUTE 2: Get Analytics for the PyQt6 Dashboard ---
@app.route('/get_analytics', methods=['GET'])
def get_analytics():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True) 
    
    # Simple query to get the average comprehension score
    cursor.execute("SELECT AVG(Comprehension_Score) as average_comprehension FROM Evaluation")
    result = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return jsonify(result)

@app.route('/api/get_dashboard_data', methods=['GET'])
def get_dashboard_data():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Fetch all raw evaluations for the list
    cursor.execute("""
        SELECT Course_Code, Topics, Pacing_Score, Comprehension_Score, 
               Workload_Score, Study_Hours, Comments 
        FROM Evaluation 
        ORDER BY Evaluation_ID DESC
    """)
    evaluations = cursor.fetchall()
    
    # 2. Calculate the averages for the top KPI boxes
    cursor.execute("""
        SELECT 
            AVG(Pacing_Score) as avg_pacing,
            AVG(Comprehension_Score) as avg_comp,
            AVG(Workload_Score) as avg_workload
        FROM Evaluation
    """)
    averages = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    # Send both the raw list and the averages back to PyQt6
    return jsonify({
        "evaluations": evaluations,
        "averages": averages
    })

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)