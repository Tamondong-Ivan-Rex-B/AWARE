# 🎓 A.W.A.R.E.
**Academic Weekly Analysis and Reporting Engine**
*(Final Release Version)*

> A centralized platform bridging the gap between quantitative academic grades, qualitative student well-being, and personal study habits. By shifting from massive, one-time semester surveys to anonymous, weekly "Pulse Checks," the system provides educators with accurate, honest, and actionable class feedback.

---

## ☁️ System Architecture & Cloud Integration
For our final release, the A.W.A.R.E. infrastructure has been fully migrated from a local XAMPP environment to a robust, fully managed cloud architecture:
* **Database (Aiven.io):** Our MySQL database runs 24/7 securely in the cloud. We utilize **DBeaver** for visual database management and schema synchronization with strict Foreign Key constraints.
* **Backend API (Render.com):** The Flask server is continuously hosted on Render.com, acting as the bridge between the database and the frontend applications over secure `https://` endpoints. 
* **API Security:** Implemented Cross-Origin Resource Sharing (`flask-cors`) and secured database credentials via environment variables to protect sensitive data.
* **True Remote Capability:** Multiple students and administrators can access the web portal and desktop dashboard simultaneously from anywhere with an internet connection.

---

## ✨ Key Features
* **Anonymous Student Pulse Checks:** Quick, weekly web-based evaluations accessible via mobile or desktop browsers.
* **Real-Time Admin Dashboard:** Live synchronization of student feedback directly from the cloud.
* **Advanced Analytics:** Visualize clarity scores and engagement trends over time using interactive graphs.
* **Cascading Filters:** Deep dive into data by specific courses or topics without compromising student anonymity.
* **Secure Role-Based Access:** Encrypted passwords (via Werkzeug) and separate portals for Students, Professors, and Administrators.

---

## 🛠️ Tech Stack
* **Frontend (Student Portal):** HTML5, CSS3, Vanilla JavaScript
* **Desktop App (Admin & Professor Dashboard):** Python 3, PyQt6, PyQtGraph, Requests, PyInstaller *(for future standalone .exe compilation)*
* **Backend Server:** Flask, Flask-CORS, Render.com
* **Database Management & Security:** MySQL, Aiven.io, mysql-connector-python, DBeaver, Werkzeug

---

## 📦 Installation & Local Development Setup

Because the database and API are currently hosted in the cloud, you no longer need to set up a local database to use the software. However, to run the source code on your machine:

### 1. Prerequisites
Ensure you have Python 3.x installed on your machine.
Clone the repository and navigate to the project folder:

    git clone https://github.com/Tamondong-Ivan-Rex-B/AWARE-System.git
    cd AWARE-System

### 2. Install Dependencies
Install all required Python libraries using pip:

    pip install flask flask-cors mysql-connector-python werkzeug PyQt6 pyqtgraph requests pyinstaller python-dotenv

### 3. Environment Variables
Create a .env file in the root directory to securely link the cloud database (ask the repository owner for the actual credentials):

    DB_HOST=your_aiven_host_url
    DB_PORT=your_port
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=aware_db

---

## 🚀 How to Run the System

### Option A: End-User Experience (Cloud)
1. **Students:** Simply open the hosted web address on any mobile or desktop browser to access `index.html` and submit a Pulse Check.
2. **Professors/Admins:** Double-click the compiled `AWARE_Dashboard.exe` or run the desktop script `main.py` to fetch real-time data:

    python main.py

### Option B: Developer Mode (Local Server Testing)
If you are testing changes to the backend API:
1. Start the Flask API locally: `python server.py`
2. Launch the desktop dashboard in a new terminal: `python main.py`

---

## 📸 Screenshots

### Student Portal (Web)
| Login | Dashboard Features | Evaluation Phase | Data Submission |
|:---:|:---:|:---:|:---:|
| ![Login](static/images/ss%20(19).png) | ![Features](static/images/ss%20(20).png) | ![Evaluating](static/images/ss%20(22).png) | ![Success](static/images/ss%20(23).png) |

### Professor & Admin Dashboards (Desktop App)
| Professor Login | Admin Login | Professor Dashboard | Admin Dashboard |
|:---:|:---:|:---:|:---:|
| ![Prof Login](static/images/ss%20(3).png) | ![Admin Login](static/images/ss%20(4).png) | ![Prof Dash](static/images/ss%20(12).png) | ![Admin Dash](static/images/ss%20(5).png) |

### Advanced Analytics & Data Management
| Data Filtering | Visual Analytics | Cloud Database (Aiven/DBeaver) |
|:---:|:---:|:---:|
| ![Filtering](static/images/ss%20(13).png) | ![Analytics](static/images/ss%20(16).png) | ![Database](static/images/ss%20(24).png) |

---

## 👥 Meet the Team
* **Escalona** - Data Integrity
* **Gestiada** - Visualization and Data Analysis
* **Interno** - Security and UI/UX
* **Monreal** - Advanced Data Filtering and Analytics
* **Tamondong** - Environment Setup & Documentation
