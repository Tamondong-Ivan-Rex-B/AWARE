# 🎓 A.W.A.R.E.
**Academic Weekly Analysis and Reporting Engine**
*(Final Release Version v1.0)*

> A centralized platform bridging the gap between quantitative academic grades, qualitative student well-being, and personal study habits. By shifting from massive, one-time semester surveys to anonymous, weekly "Pulse Checks," A.W.A.R.E. provides educators with accurate, honest, and actionable class feedback in real time.

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
* **Standalone Desktop Dashboard:** A compiled executable (`.exe`) allows Professors and Admins to run the analytics dashboard natively on Windows without installing Python.
* **Real-Time Synchronization:** Live synchronization of student feedback directly from the cloud.
* **Advanced Analytics:** Visualize clarity scores and engagement trends over time using interactive graphs.
* **Cascading Filters:** Deep dive into data by specific courses or topics without compromising student anonymity.
* **Secure Role-Based Access:** Encrypted passwords (via Werkzeug) and separate portals for Students, Professors, and Administrators.

---

## 🛠️ Tech Stack
* **Frontend (Student Portal):** HTML5, CSS3, Vanilla JavaScript
* **Desktop App (Admin & Professor Dashboard):** Python 3, PyQt6, PyQtGraph, Requests
* **Compilation:** PyInstaller *(Used to bundle the desktop app into a standalone .exe)*
* **Backend Server:** Flask, Flask-CORS, Render.com
* **Database Management & Security:** MySQL, Aiven.io, mysql-connector-python, DBeaver, Werkzeug

---

## 🚀 How to Use the System

### For End-Users (No Installation Required)
Because the database and API are currently hosted in the cloud, standard users do not need to configure any local environments.

1. **For Students:** Open https://aware-api.onrender.com/ on any mobile or desktop browser to log in and submit a Pulse Check.
2. **For Professors & Admins (The .exe File):**
   * Navigate to the `dist` folder in this repository.
   * Download and double-click `A.W.A.R.E..exe`.
   * The desktop application will launch instantly and securely fetch real-time analytics from the cloud database.

---

## 💻 Developer Setup & Installation
If you wish to modify the source code or run the Python scripts locally, follow these steps:

### 1. Prerequisites
Ensure you have Python 3.x installed on your machine. Clone the repository and navigate to the project folder:

    git clone https://github.com/Tamondong-Ivan-Rex-B/AWARE-System.git
    cd AWARE-System

### 2. Install Dependencies
Install all required Python libraries using pip:

    pip install flask flask-cors mysql-connector-python werkzeug PyQt6 pyqtgraph requests pyinstaller python-dotenv

### 3. Environment Variables
Create a `.env` file in the root directory to securely link the cloud database (contact the repository owner for the actual credentials):

    DB_HOST=your_aiven_host_url
    DB_PORT=your_port
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=aware_db

### 4. Running the Code
* **Option A (Testing the Dashboard):** Run the Python script directly to test UI changes.
  
      python main.py

* **Option B (Local Server Testing):** If you are testing changes to the backend API, start the local server first, then launch the dashboard.
  
      python server.py
      python main.py

### 5. Building the .exe (For Contributors)
If you make updates to the dashboard code and need to generate a new `.exe` file for users, run:

    pyinstaller --onefile --windowed main.py

*The compiled executable will be generated inside the `dist/` folder.*

---

## 📸 Screenshots

### Student Portal (Website)
| Login | Dashboard | Data Submission | Duplicate Submission Blocking |
|:---:|:---:|:---:|:---:|
| ![Login](static/images/ss%20(25).png) | ![Dashboard](static/images/ss%20(26).png) | ![Data Submission](static/images/ss%20(27).png) | ![Duplicate Submission Blocking](static/images/ss%20(28).png) |

### Professor & Admin Dashboards (Desktop Application)
| Professor and Admin Login | Admin Dashboard | Reports (.pdf) |
|:---:|:---:|:---:|
| ![Professor and Admin Login](static/images/ss%20(1).png) | ![Admin Dashboard](static/images/ss%20(2).png) | ![Reports (.pdf)](static/images/ss%20(3).png) |

### Admin CRUD (Desktop Application)
| Professors | Guardians | Students | Courses |
|:---:|:---:|:---:|:---:|
| ![Professors](static/images/ss%20(4).png) | ![Guardians](static/images/ss%20(8).png) | ![Students](static/images/ss%20(9).png) | ![Courses](static/images/ss%20(12).png) |

| Schedules | Enrollments | Sessions | Evaluations |
|:---:|:---:|:---:|:---:|
| ![Schedules](static/images/ss%20(13).png) | ![Enrollments](static/images/ss%20(14).png) | ![Sessions](static/images/ss%20(15).png) | ![Evaluations](static/images/ss%20(16).png) |

### Admin CRUD Samples and Features (Desktop Application)
| Create | Update (W/ Primary Key) | Update (W/ Foreign Key) | Filtering |
|:---:|:---:|:---:|:---:|
| ![Create](static/images/ss%20(5).png) | ![Update](static/images/ss%20(6).png) | ![Filtering](static/images/ss%20(10).png) | ![Evaluations](static/images/ss%20(7).png) |

### Data Analytics (Desktop Application)
| Outcomes | Burnout Detector | Syllabus Bottleneck |
|:---:|:---:|:---:|
| ![Outcomes](static/images/ss%20(18).png) | ![Burnout Detector](static/images/ss%20(20).png) | ![Syllabus Bottleneck](static/images/ss%20(21).png) |

| Pacing Sweet Spot | Engagement | Clarity |
|:---:|:---:|:---:|
| ![Pacing Sweet Spot](static/images/ss%20(22).png) | ![Engagement](static/images/ss%20(23).png) | ![Clarity](static/images/ss%20(24).png) |

### Advanced Analytics & Data Management
| ERD and Database Manager (DBeaver) | Hosting Platform (Render.com) | Cloud Database (Aiven.io) |
|:---:|:---:|:---:|
| ![ERD and Database Manager (DBeaver)](static/images/ss%20(31).png) | ![Hosting Platform (Render.com)](static/images/ss%20(30).png) | ![Cloud Database (Aiven.io)](static/images/ss%20(29).png) |

---

## 👥 Meet the Team
* **Escalona** - Data Integrity
* **Gestiada** - Visualization and Data Analysis
* **Interno** - Security and UI/UX
* **Monreal** - Advanced Data Filtering and Analytics
* **Tamondong** - Lead Developer, Environment Setup, & Documentation
