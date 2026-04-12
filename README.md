# 🎓 A.W.A.R.E.
**Academic Weekly Analysis and Reporting Engine**

> A centralized platform bridging the gap between quantitative academic grades, qualitative student well-being, and personal study habits. By shifting from massive, one-time semester surveys to anonymous, weekly "Pulse Checks," the system provides educators with accurate, honest, and actionable class feedback.

---

## ✨ Key Features
* **Anonymous Student Pulse Checks:** Quick, weekly web-based evaluations.
* **Real-Time Admin Dashboard:** Live synchronization of student feedback.
* **Advanced Analytics:** Visualize clarity scores and engagement trends over time.
* **Cascading Filters:** Deep dive into data by specific courses or topics without compromising student anonymity.
* **Secure Role-Based Access:** Encrypted passwords and separate portals for Students and Professors.

---

## 🛠️ Tech Stack
* **Frontend (Student Portal):** HTML5, CSS3, Vanilla JavaScript
* **Desktop App (Admin/Professor Dashboard):** Python, PyQt6, PyQtGraph
* **Backend Server:** Python, Flask, Flask-CORS
* **Database & Security:** MySQL, mysql-connector-python, Werkzeug (Password Hashing)

---

## 📦 Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.x and MySQL installed on your machine.
Clone the repository and navigate to the project folder:
    
    git clone https://github.com/Tamondong-Ivan-Rex-B/AWARE-System.git
    cd AWARE-System

### 2. Install Dependencies
Install all required Python libraries using pip:
    
    pip install flask flask-cors mysql-connector-python werkzeug PyQt6 pyqtgraph requests

### 3. Database Setup
1. Open your MySQL manager (e.g., phpMyAdmin, MySQL Workbench).
2. Create a new database named `aware_db`.
3. Import the provided `aware_db.sql` file to create the tables.
4. Open your terminal and run the password seeding script to secure the dummy accounts:
    
    python seed_passwords.py

---

## 🚀 How to Run the System
The A.W.A.R.E. system requires the server and the frontend/dashboard to run simultaneously.

### Step 1: Start the Backend Server
Open a terminal and start the Flask API. Keep this terminal open.
    
    python server.py

### Step 2: Access the Portals
* **For Students:** Open `index.html` in any modern web browser.
* **For Professors/Admins:** Open a new terminal window and launch the desktop dashboard:
    
    python main.py

---

## 📖 System Flow
1. **Deployment:** The admin starts `server.py` on the local network (or cloud).
2. **Evaluation Phase:** Students access the web portal (`index.html`) via their phones or laptops, select their current week's topic, and submit an anonymous Pulse Check.
3. **Data Processing:** The Flask server securely processes the submission and updates the MySQL database in real-time.
4. **Analysis Phase:** Professors launch the Desktop App (`main.py`) to view the live dashboard. They can use the Analytics tab to visualize engagement drops or confusing topics and adjust their teaching methods accordingly.

---

## 📸 Screenshots
| Student Web Login Portal |
|:---:|
| ![Student Web Portal](static/images/ss%20(19).png) |

| Student Web Features |
|:---:|
| ![Student Web Portal](static/images/ss%20(20).png) |
| ![Student Web Portal](static/images/ss%20(21).png) |
| Submission of Evaluation Data ![Student Web Portal](static/images/ss%20(22).png) |
| Evaluation Data sent to Admin Dashboard![Student Web Portal](static/images/ss%20(23).png) |

| Professor Desktop Login Page | Admin Desktop Login Page |
|:---:|:---:|
| ![Professor Dashboard](static/images/ss%20(3).png) | ![Admin Dashboard](static/images/ss%20(4).png) |

| Professor Desktop Dashboard | Admin Desktop Dashboard |
|:---:|:---:|
| ![Professor Dashboard](static/images/ss%20(12).png) | ![Admin Dashboard](static/images/ss%20(5).png) |


| Professor Desktop Features and Analytics | Admin Desktop Feature and Analytics |
|:---:|:---:|
| ![Professor Dashboard](static/images/ss%20(13).png) | ![Admin Dashboard](static/images/ss%20(6).png) |
| ![Professor Dashboard](static/images/ss%20(14).png) | ![Admin Dashboard](static/images/ss%20(7).png) |
| ![Professor Dashboard](static/images/ss%20(15).png) | ![Admin Dashboard](static/images/ss%20(8).png) |
| ![Professor Dashboard](static/images/ss%20(16).png) | ![Admin Dashboard](static/images/ss%20(9).png) |
| ![Professor Dashboard](static/images/ss%20(17).png) | ![Admin Dashboard](static/images/ss%20(10).png) |
| ![Professor Dashboard](static/images/ss%20(18).png) | ![Admin Dashboard](static/images/ss%20(11).png) |

| Database |
|:---:|
| ![Database](static/images/ss%20(24).png) |
---

## 👥 Meet the Team
* **Escalona** - Data Integrity
* **Gestiada** - Analytics and Data Analysis
* **Interno** - Security and UI/UX
* **Monreal** - Advanced Data Filtering and Analytics
* **Tamondong** - Environment Setup & Documentation
