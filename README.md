# 🎓 A.W.A.R.E.
**Academic Weekly Analysis and Reporting Engine**

> A centralized platform bridging the gap between quantitative academic grades, qualitative student well-being, and personal study habits. By shifting from massive, one-time semester surveys to anonymous, weekly "Pulse Checks," the system provides educators with accurate, honest, and actionable class feedback.

---
## Changelogs:

* **Cloud Migration & Architecture Update**:
We successfully migrated the A.W.A.R.E. database architecture from a local XAMPP environment to a fully managed cloud infrastructure. The database is now hosted on Aiven.io, an open-source data platform providing robust cloud MySQL services. The backend Flask API is deployed on Render.com, a unified cloud hosting platform that scales and runs our web services automatically. To manage this remote database securely and efficiently, we utilize DBeaver, an advanced open-source database management tool. This complete architectural shift allows the project to run 100% online, enabling seamless remote access for students and administrators alike.

* **Cloud Integration**: Transitioned from localhost (127.0.0.1) to secure https:// cloud endpoints.

* **API Security & CORS**: Implemented Cross-Origin Resource Sharing (flask-cors) to allow the desktop application to securely communicate with the cloud server.

* **Environment Variables**: Secured database credentials (host, user, password) using environment variables to prevent hardcoding sensitive data into public repositories.

* **Database Schema Synchronization**: Updated the cloud database and established strict Foreign Key constraints (Crow's Foot Entity-Relationship rules) directly in Aiven to ensure data integrity.

* **Standalone Executable**: Compiled the PyQt6 Admin Dashboard into a standalone .exe file using PyInstaller, allowing professors and admins to run the app on any Windows machine without needing Python installed. (Future)

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
* **Desktop App (Admin & Professor Dashboard):** Python 3, PyQt6, PyQtGraph, PyInstaller, Requests
* **Backend Server:** Flask, Flask-CORS, Render.com
* **Database Management & Security:** MySQL, Aiven.io, mysql-connector-python, DBeaver, Werkzeug

---

## 📦 Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.x and MySQL installed on your machine.
Clone the repository and navigate to the project folder:
    
    git clone https://github.com/Tamondong-Ivan-Rex-B/AWARE-System.git
    cd AWARE-System

### 2. Install Dependencies
Install all required Python libraries using pip:
    
    pip install flask flask-cors mysql-connector-python werkzeug PyQt6 pyqtgraph requests pyinstaller

<del>### 3. Database Setup
<del>1. Open your MySQL manager (e.g., phpMyAdmin, MySQL Workbench).
<del>2. Create a new database named `aware_db`.
<del>3. Import the provided `aware_db.sql` file to create the tables.
<del>4. Open your terminal and run the password seeding script to secure the dummy accounts:
    
<del>    python seed_passwords.py

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

## 📖 New Cloud Workflow
1. * **Database (Aiven)**: The MySQL database runs 24/7 in the cloud. No local servers are required. Database management is done visually through DBeaver.
2. * **Server (Render)**: The Flask API is hosted continuously on Render.com. It automatically "wakes up" whenever a student visits the website or an admin logs in.
3. * **Application**: Administrators simply double-click the AWARE_Dashboard.exe file on their own computers. The desktop app securely fetches and pushes data over the internet.
4. * **Advantage**: True remote capability. Multiple users can access the web portal and the admin dashboard simultaneously from anywhere.

---

## 📸 Screenshots (To be updated)
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
* **Gestiada** - Visualization and Data Analysis
* **Interno** - Security and UI/UX
* **Monreal** - Advanced Data Filtering and Analytics
* **Tamondong** - Environment Setup & Documentation
