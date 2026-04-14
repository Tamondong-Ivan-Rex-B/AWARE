import sys
import os
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, 
    QTableWidgetItem, QLabel, QPushButton, QHBoxLayout,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox,
    QHeaderView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import BASE_URL

# ==========================================
# 1. API WORKER THREAD
# ==========================================
class FetchDataWorker(QThread):
    finished_success = pyqtSignal(int, list) 
    finished_error = pyqtSignal(int, str)    

    def __init__(self, tab_index, endpoint):
        super().__init__()
        self.tab_index = tab_index
        self.endpoint = endpoint

    def run(self):
        try:
            response = requests.get(f"{BASE_URL}{self.endpoint}")
            response.raise_for_status()
            self.finished_success.emit(self.tab_index, response.json().get("data", []))
        except Exception as e:
            self.finished_error.emit(self.tab_index, str(e))

# ==========================================
# 2. POPUP DIALOGS
# ==========================================
class ProfessorDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Professor" if data else "Add Professor")
        self.resize(300, 200)
        layout = QFormLayout(self)
        self.first_name = QLineEdit(data.get("First_Name", "") if data else "")
        self.last_name = QLineEdit(data.get("Last_Name", "") if data else "")
        self.username = QLineEdit(data.get("Username", "") if data else "")
        self.department = QLineEdit(data.get("Department", "") if data else "")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Leave blank to keep current" if data else "Required")
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        layout.addRow("Department:", self.department)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)

    def get_data(self):
        payload = {"First_Name": self.first_name.text().strip(), "Last_Name": self.last_name.text().strip(), "Username": self.username.text().strip(), "Department": self.department.text().strip()}
        if self.password.text().strip(): payload["Password"] = self.password.text().strip()
        return payload

class GuardianDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Guardian" if data else "Add Guardian")
        layout = QFormLayout(self)
        self.first_name = QLineEdit(data.get("First_Name", "") if data else "")
        self.last_name = QLineEdit(data.get("Last_Name", "") if data else "")
        self.email = QLineEdit(data.get("Email", "") if data else "")
        self.phone = QLineEdit(data.get("Contact_Number", "") if data else "")
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Email:", self.email)
        layout.addRow("Contact Number:", self.phone)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)

    def get_data(self):
        return {"First_Name": self.first_name.text().strip(), "Last_Name": self.last_name.text().strip(), "Email": self.email.text().strip(), "Contact_Number": self.phone.text().strip()}

class StudentDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Student" if data else "Add Student")
        layout = QFormLayout(self)
        self.first_name = QLineEdit(data.get("First_Name", "") if data else "")
        self.last_name = QLineEdit(data.get("Last_Name", "") if data else "")
        self.username = QLineEdit(data.get("Username", "") if data else "")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Leave blank to keep current" if data else "Required")
        self.guardian_combo = QComboBox()
        self.guardian_combo.addItem("None", None)
        try:
            resp = requests.get(f"{BASE_URL}/api/admin/guardians").json().get("data", [])
            for g in resp: self.guardian_combo.addItem(f"{g['First_Name']} {g['Last_Name']}", g['Guardian_ID'])
        except: pass
        if data and data.get("Guardian_ID") != "None":
            idx = self.guardian_combo.findData(int(data.get("Guardian_ID")))
            if idx >= 0: self.guardian_combo.setCurrentIndex(idx)
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        layout.addRow("Guardian:", self.guardian_combo)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)

    def get_data(self):
        payload = {"First_Name": self.first_name.text().strip(), "Last_Name": self.last_name.text().strip(), "Username": self.username.text().strip(), "Guardian_ID": self.guardian_combo.currentData()}
        if self.password.text().strip(): payload["Password"] = self.password.text().strip()
        return payload

class CourseDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Course" if data else "Add Course")
        layout = QFormLayout(self)
        self.course_code = QLineEdit(data.get("Course_Code", "") if data else "")
        self.course_title = QLineEdit(data.get("Course_Title", "") if data else "")
        if data: self.course_code.setReadOnly(True)
        layout.addRow("Course Code:", self.course_code)
        layout.addRow("Course Title:", self.course_title)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)

    def get_data(self):
        return {"Course_Code": self.course_code.text().strip().upper(), "Course_Title": self.course_title.text().strip()}

class ScheduleDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Schedule" if data else "Add Schedule")
        layout = QFormLayout(self)
        self.course_combo = QComboBox()
        self.room_input = QLineEdit(data.get("Room_Name", "") if data else "")
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        self.start_time = QLineEdit(data.get("Start_Time", "09:00:00") if data else "09:00:00")
        self.end_time = QLineEdit(data.get("End_Time", "10:30:00") if data else "10:30:00")
        try:
            courses = requests.get(f"{BASE_URL}/api/admin/courses").json().get("data", [])
            for c in courses: self.course_combo.addItem(c["Course_Code"], c["Course_Code"])
        except: pass
        if data:
            c_idx = self.course_combo.findData(data.get("Course_Code"))
            if c_idx >= 0: self.course_combo.setCurrentIndex(c_idx)
            self.day_combo.setCurrentText(data.get("Schedule_Day"))
        layout.addRow("Course:", self.course_combo)
        layout.addRow("Room Name:", self.room_input)
        layout.addRow("Schedule Day:", self.day_combo)
        layout.addRow("Start Time:", self.start_time)
        layout.addRow("End Time:", self.end_time)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)

    def get_data(self):
        return {"Course_Code": self.course_combo.currentData(), "Room_Name": self.room_input.text().strip(), "Schedule_Day": self.day_combo.currentText(), "Start_Time": self.start_time.text().strip(), "End_Time": self.end_time.text().strip()}

class EnrollmentDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Enrollment" if data else "Add Enrollment")
        layout = QFormLayout(self)
        self.student_combo = QComboBox()
        self.course_combo = QComboBox()
        self.acad_year = QLineEdit(data.get("Academic_Year", "2025-2026") if data else "2025-2026")
        self.semester = QComboBox()
        self.semester.addItems(["1st", "2nd", "Summer"])
        if data and data.get("Semester"): self.semester.setCurrentText(str(data.get("Semester")))
        self.grade = QLineEdit(data.get("Current_Grade", "1.00") if data else "")
        try:
            students = requests.get(f"{BASE_URL}/api/admin/students").json().get("data", [])
            for s in students: self.student_combo.addItem(f"{s['First_Name']} {s['Last_Name']}", s["Student_ID"])
            courses = requests.get(f"{BASE_URL}/api/admin/courses").json().get("data", [])
            for c in courses: self.course_combo.addItem(c["Course_Code"], c["Course_Code"])
        except: pass
        if data:
            for i in range(self.student_combo.count()):
                if str(self.student_combo.itemData(i)) == str(data.get("Student_ID")):
                    self.student_combo.setCurrentIndex(i)
                    break
            c_idx = self.course_combo.findData(data.get("Course_Code"))
            if c_idx >= 0: self.course_combo.setCurrentIndex(c_idx)
        layout.addRow("Student:", self.student_combo)
        layout.addRow("Course:", self.course_combo)
        layout.addRow("Academic Year:", self.acad_year)
        layout.addRow("Semester:", self.semester)
        layout.addRow("Current Grade:", self.grade)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)

    def get_data(self):
        return {"Student_ID": self.student_combo.currentData(), "Course_Code": self.course_combo.currentData(), "Academic_Year": self.acad_year.text().strip(), "Semester": self.semester.currentText(), "Current_Grade": self.grade.text().strip()}

class SessionDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Session" if data else "Add Session")
        layout = QFormLayout(self)
        self.course_combo = QComboBox()
        self.prof_combo = QComboBox()
        self.date_input = QLineEdit(data.get("Session_Date", "2026-04-15") if data else "2026-04-15")
        self.topic_input = QLineEdit(data.get("Topic", "") if data else "")
        try:
            courses = requests.get(f"{BASE_URL}/api/admin/courses").json().get("data", [])
            for c in courses: self.course_combo.addItem(c["Course_Code"], c["Course_Code"])
            profs = requests.get(f"{BASE_URL}/api/admin/professors").json().get("data", [])
            for p in profs: self.prof_combo.addItem(f"{p['First_Name']} {p['Last_Name']}", p["Professor_ID"])
        except: pass
        if data:
            c_idx = self.course_combo.findData(data.get("Course_Code"))
            if c_idx >= 0: self.course_combo.setCurrentIndex(c_idx)
            for i in range(self.prof_combo.count()):
                if str(self.prof_combo.itemData(i)) == str(data.get("Professor_ID")):
                    self.prof_combo.setCurrentIndex(i)
                    break
            self.date_input.setText(data.get("Session_Date", ""))
            self.topic_input.setText(data.get("Topic", ""))
        layout.addRow("Course:", self.course_combo)
        layout.addRow("Professor:", self.prof_combo)
        layout.addRow("Session Date (YYYY-MM-DD):", self.date_input)
        layout.addRow("Topic:", self.topic_input)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)

    def get_data(self):
        return {"Course_Code": self.course_combo.currentData(), "Professor_ID": self.prof_combo.currentData(), "Session_Date": self.date_input.text().strip(), "Topic": self.topic_input.text().strip()}

# ==========================================
# 3. MAIN WINDOW
# ==========================================
class ManageDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚙️ A.W.A.R.E. Data Management")
        self.resize(1100, 700)
        
        self.setStyleSheet("""
        QPushButton { background-color: white; color: #5071c1; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px 15px; font-weight: bold; min-width: 60px; }
        QPushButton:hover { background-color: #f8fafc; border: 1px solid #5071c1; }
        QMessageBox { background-color: white; }
        QMessageBox QLabel { color: #5071c1; font-size: 14px; font-weight: bold; }
        QWidget { background-color: white; }
        QLabel { color: #0f172a; font-size: 13px; }
        QLineEdit, QComboBox { padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; color: #5071c1; }
        QComboBox { font-weight: bold; }
        QComboBox QAbstractItemView { color: #5071c1; background-color: white; selection-background-color: #f1f5f9; outline: none; }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #6D28D9; background: white; }
        QTableWidget { border: 1px solid #e2e8f0; border-radius: 6px; gridline-color: #e2e8f0; color: #5071c1; background-color: white; }
        QTableWidget::item { padding: 5px; }
        QTableWidget::item:selected { background-color: #f8fafc; color: #6D28D9; font-weight: bold; }
        QHeaderView::section { background-color: #f8fafc; padding: 10px; border: none; border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #5071c1; }
        QTabWidget::pane { border: 1px solid #e2e8f0; background: white; border-radius: 8px; }
        QTabBar::tab { background: #f1f5f9; color: #64748b; padding: 10px 20px; border: 1px solid #e2e8f0; border-top-left-radius: 8px; border-top-right-radius: 8px; font-weight: bold; margin-right: 2px; }
        QTabBar::tab:selected { background: #6D28D9; color: white; border-color: #6D28D9; }
        """)

        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        logo_path = os.path.join(parent_dir, "static", "images", "AWARE-icon.jpg")
        logo_label = QLabel()
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo_label.setStyleSheet("border: 1px solid navy; border-radius: 5px; margin-right: 10px; margin-top: 2px;")
        
        self.tabs.setCornerWidget(logo_label, Qt.Corner.TopRightCorner)

        self.tabs.addTab(self.create_ui_tab("Professors", ["ID", "First Name", "Last Name", "Department"], self.handle_prof_crud), "Professors")
        self.tabs.addTab(self.create_ui_tab("Guardians", ["ID", "First Name", "Last Name", "Email", "Contact Number"], self.handle_guardian_crud), "Guardians")
        self.tabs.addTab(self.create_ui_tab("Students", ["ID", "First Name", "Last Name", "Guardian ID"], self.handle_student_crud), "Students")
        self.tabs.addTab(self.create_ui_tab("Courses", ["Code", "Title"], self.handle_course_crud), "Courses")
        self.tabs.addTab(self.create_ui_tab("Schedules", ["ID", "Course", "Room Name", "Schedule Day", "Start", "End"], self.handle_schedule_crud), "Schedules")
        self.tabs.addTab(self.create_ui_tab("Enrollments", ["ID", "Student ID", "Course", "Acad. Year", "Semester", "Grade"], self.handle_enrollment_crud), "Enrollments")
        self.tabs.addTab(self.create_ui_tab("Class Sessions", ["ID", "Course", "Topic", "Date", "Prof ID"], self.handle_session_crud), "Sessions")
        self.tabs.addTab(self.create_ui_tab("Evaluations", ["ID", "Course", "Clarity", "Pacing", "Comp.", "Engage.", "Date", "Study Hrs", "Comments"], self.handle_eval_crud, hide_add_edit=True), "Evaluations")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.loaded_tabs = {i: False for i in range(8)}
        self.worker = None 
        self.on_tab_changed(0) 

    def create_ui_tab(self, name, headers, crud_router, hide_add_edit=False):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        btn_layout = QHBoxLayout()
        if not hide_add_edit:
            btn_add = QPushButton(f"➕ Add {name[:-1]}" if not name.endswith("ssions") else "➕ Add Session")
            btn_edit = QPushButton("✏️ Edit Selected")
            btn_add.clicked.connect(lambda: crud_router("ADD"))
            btn_edit.clicked.connect(lambda: crud_router("EDIT"))
            btn_layout.addWidget(btn_add)
            btn_layout.addWidget(btn_edit)
        btn_del = QPushButton("🗑️ Delete Selected")
        btn_del.clicked.connect(lambda: crud_router("DELETE"))
        btn_layout.addWidget(btn_del)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)
        setattr(self, f"{name.lower().replace(' ', '_')}_table", table)
        return tab

    def refresh_tab(self, index):
        self.loaded_tabs[index] = False 
        self.on_tab_changed(index)

    def on_tab_changed(self, index):
        if self.loaded_tabs[index]: return 
        endpoints = {0: "/api/admin/professors", 1: "/api/admin/guardians", 2: "/api/admin/students", 3: "/api/admin/courses", 4: "/api/admin/schedules", 5: "/api/admin/enrollments", 6: "/api/admin/sessions", 7: "/api/admin/evaluations"}
        if index in endpoints:
            self.worker = FetchDataWorker(index, endpoints[index])
            self.worker.finished_success.connect(self.handle_data_loaded)
            self.worker.finished_error.connect(self.handle_data_error)
            self.worker.start()

    def handle_data_error(self, tab_index, error_msg):
        print(f"Network Error on Tab {tab_index}: {error_msg}")

    def handle_data_loaded(self, idx, data):
        self.loaded_tabs[idx] = True
        if idx == 0: self.populate_exact(self.professors_table, data, ["Professor_ID", "First_Name", "Last_Name", "Department"])
        elif idx == 1: self.populate_exact(self.guardians_table, data, ["Guardian_ID", "First_Name", "Last_Name", "Email", "Contact_Number"])
        elif idx == 2: self.populate_exact(self.students_table, data, ["Student_ID", "First_Name", "Last_Name", "Guardian_ID"])
        elif idx == 3: self.populate_exact(self.courses_table, data, ["Course_Code", "Course_Title"])
        elif idx == 4: self.populate_exact(self.schedules_table, data, ["Schedule_ID", "Course_Code", "Room_Name", "Schedule_Day", "Start_Time", "End_Time"])
        elif idx == 5: self.populate_exact(self.enrollments_table, data, ["Enrollment_ID", "Student_ID", "Course_Code", "Academic_Year", "Semester", "Current_Grade"])
        elif idx == 6: self.populate_exact(self.class_sessions_table, data, ["Session_ID", "Course_Code", "Topic", "Session_Date", "Professor_ID"])
        elif idx == 7: self.populate_exact(self.evaluations_table, data, ["Evaluation_ID", "Course_Code", "Clarity_Score", "Pacing_Score", "Comprehension_Score", "Engagement_Score", "Submission_Date", "Study_Hours", "Additional_Comments"])

    def populate_exact(self, table, data, exact_keys):
        table.setRowCount(len(data))
        for r, row_data in enumerate(data):
            for c, key in enumerate(exact_keys):
                if key == "Submission_Date" and "Formatted_Date" in row_data: val = row_data.get("Formatted_Date")
                else: val = row_data.get(key)
                if val is None or val == "": val = "-"
                table.setItem(r, c, QTableWidgetItem(str(val)))

    def get_selected(self, table):
        rows = table.selectionModel().selectedRows()
        return rows[0].row() if rows else None

    def api_call(self, method, endpoint, payload=None, tab_idx=0):
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == "POST": requests.post(url, json=payload).raise_for_status()
            elif method == "PUT": requests.put(url, json=payload).raise_for_status()
            elif method == "DELETE": requests.delete(url).raise_for_status()
            QMessageBox.information(self, "Success", "Action completed!")
            self.refresh_tab(tab_idx)
        except Exception as e:
            QMessageBox.critical(self, "API Error", str(e))

    def handle_prof_crud(self, action):
        t = self.professors_table
        if action == "ADD":
            dlg = ProfessorDialog(self)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("POST", "/api/admin/professors", dlg.get_data(), 0)
        elif action == "EDIT":
            r = self.get_selected(t)
            if r is None: return QMessageBox.warning(self, "Error", "Select a row!")
            data = {"First_Name": t.item(r,1).text(), "Last_Name": t.item(r,2).text(), "Department": t.item(r,3).text()}
            dlg = ProfessorDialog(self, data)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("PUT", f"/api/admin/professors/{t.item(r,0).text()}", dlg.get_data(), 0)
        elif action == "DELETE":
            r = self.get_selected(t)
            if r is not None and QMessageBox.question(self, "Confirm", "Delete?") == QMessageBox.StandardButton.Yes: self.api_call("DELETE", f"/api/admin/professors/{t.item(r,0).text()}", tab_idx=0)

    def handle_guardian_crud(self, action):
        t = self.guardians_table
        if action == "ADD":
            dlg = GuardianDialog(self)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("POST", "/api/admin/guardians", dlg.get_data(), 1)
        elif action == "EDIT":
            r = self.get_selected(t)
            if r is None: return
            data = {"First_Name": t.item(r,1).text(), "Last_Name": t.item(r,2).text(), "Email": t.item(r,3).text(), "Contact_Number": t.item(r,4).text()}
            dlg = GuardianDialog(self, data)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("PUT", f"/api/admin/guardians/{t.item(r,0).text()}", dlg.get_data(), 1)
        elif action == "DELETE":
            r = self.get_selected(t)
            if r is not None: self.api_call("DELETE", f"/api/admin/guardians/{t.item(r,0).text()}", tab_idx=1)

    def handle_student_crud(self, action):
        t = self.students_table
        if action == "ADD":
            dlg = StudentDialog(self)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("POST", "/api/admin/students", dlg.get_data(), 2)
        elif action == "EDIT":
            r = self.get_selected(t)
            if r is None: return
            data = {"First_Name": t.item(r,1).text(), "Last_Name": t.item(r,2).text(), "Guardian_ID": t.item(r,3).text()}
            dlg = StudentDialog(self, data)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("PUT", f"/api/admin/students/{t.item(r,0).text()}", dlg.get_data(), 2)
        elif action == "DELETE":
            r = self.get_selected(t)
            if r is not None: self.api_call("DELETE", f"/api/admin/students/{t.item(r,0).text()}", tab_idx=2)

    def handle_course_crud(self, action):
        t = self.courses_table
        if action == "ADD":
            dlg = CourseDialog(self)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("POST", "/api/admin/courses", dlg.get_data(), 3)
        elif action == "EDIT":
            r = self.get_selected(t)
            if r is None: return
            data = {"Course_Code": t.item(r,0).text(), "Course_Title": t.item(r,1).text()}
            dlg = CourseDialog(self, data)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("PUT", f"/api/admin/courses/{t.item(r,0).text()}", dlg.get_data(), 3)
        elif action == "DELETE":
            r = self.get_selected(t)
            if r is not None: self.api_call("DELETE", f"/api/admin/courses/{t.item(r,0).text()}", tab_idx=3)

    def handle_schedule_crud(self, action):
        t = self.schedules_table
        if action == "ADD":
            dlg = ScheduleDialog(self)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("POST", "/api/admin/schedules", dlg.get_data(), 4)
        elif action == "EDIT":
            r = self.get_selected(t)
            if r is None: return
            data = {"Course_Code": t.item(r,1).text(), "Room_Name": t.item(r,2).text(), "Schedule_Day": t.item(r,3).text(), "Start_Time": t.item(r,4).text(), "End_Time": t.item(r,5).text()}
            dlg = ScheduleDialog(self, data)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("PUT", f"/api/admin/schedules/{t.item(r,0).text()}", dlg.get_data(), 4)
        elif action == "DELETE":
            r = self.get_selected(t)
            if r is not None: self.api_call("DELETE", f"/api/admin/schedules/{t.item(r,0).text()}", tab_idx=4)

    def handle_enrollment_crud(self, action):
        t = self.enrollments_table
        if action == "ADD":
            dlg = EnrollmentDialog(self)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("POST", "/api/admin/enrollments", dlg.get_data(), 5)
        elif action == "EDIT":
            r = self.get_selected(t)
            if r is None: return
            data = {"Student_ID": t.item(r,1).text(), "Course_Code": t.item(r,2).text(), "Academic_Year": t.item(r,3).text(), "Semester": t.item(r,4).text(), "Current_Grade": t.item(r,5).text()}
            dlg = EnrollmentDialog(self, data)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("PUT", f"/api/admin/enrollments/{t.item(r,0).text()}", dlg.get_data(), 5)
        elif action == "DELETE":
            r = self.get_selected(t)
            if r is not None: self.api_call("DELETE", f"/api/admin/enrollments/{t.item(r,0).text()}", tab_idx=5)

    def handle_session_crud(self, action):
        t = self.class_sessions_table
        if action == "ADD":
            dlg = SessionDialog(self)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("POST", "/api/admin/sessions", dlg.get_data(), 6)
        elif action == "EDIT":
            r = self.get_selected(t)
            if r is None: return
            data = {"Course_Code": t.item(r,1).text(), "Topic": t.item(r,2).text(), "Session_Date": t.item(r,3).text(), "Professor_ID": t.item(r,4).text()}
            dlg = SessionDialog(self, data)
            if dlg.exec() == QDialog.DialogCode.Accepted: self.api_call("PUT", f"/api/admin/sessions/{t.item(r,0).text()}", dlg.get_data(), 6)
        elif action == "DELETE":
            r = self.get_selected(t)
            if r is not None: self.api_call("DELETE", f"/api/admin/sessions/{t.item(r,0).text()}", tab_idx=6)

    def handle_eval_crud(self, action):
        t = self.evaluations_table
        if action == "DELETE":
            r = self.get_selected(t)
            if r is not None: self.api_call("DELETE", f"/api/admin/evaluations/{t.item(r,0).text()}", tab_idx=7)