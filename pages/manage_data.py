import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QTabWidget,
    QFormLayout, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class ManageDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚙️ A.W.A.R.E. Data Management")
        self.resize(950, 650)
        
        self.setStyleSheet("""
        /* --- Popup Dialogue Boxes --- */
        QMessageBox { 
            background-color: white; 
        }
        QMessageBox QLabel { 
            color: #5071c1; /* Changes the popup text to custom blue */
            font-size: 14px; 
            font-weight: bold; 
        }
        QMessageBox QPushButton { 
            background-color: white; 
            color: #5071c1; 
            border: 1px solid #cbd5e1; 
            border-radius: 5px; 
            padding: 6px 15px; 
            font-weight: bold; 
            min-width: 60px;
        }
        QMessageBox QPushButton:hover { 
            background-color: #f8fafc; 
            border: 1px solid #5071c1; 
        }
        QWidget { background-color: white; }
        QLabel { color: #0f172a; font-size: 13px; }
        QLineEdit, QComboBox { padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; color: #0f172a; }
        QComboBox { color: #5071c1; font-weight: bold; }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #6D28D9; background: white; }
        QComboBox QAbstractItemView { background-color: white; color: #0f172a; selection-background-color: #f1f5f9; selection-color: #6D28D9; border: 1px solid #cbd5e1; outline: none; }
        QTableWidget { border: 1px solid #e2e8f0; border-radius: 6px; gridline-color: #e2e8f0; color: #5071c1; background-color: white; }
        QTableWidget::item { padding: 5px; }
        QTableWidget::item:selected { background-color: #f8fafc; color: #6D28D9; font-weight: bold; }
        QHeaderView::section { background-color: #f8fafc; padding: 10px; border: none; border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #5071c1; }
        QTabWidget::pane { border: 1px solid #e2e8f0; background: white; border-radius: 8px; }
        QTabBar::tab { background: #f1f5f9; color: #64748b; padding: 10px 20px; border: 1px solid #e2e8f0; border-bottom-color: #e2e8f0; border-top-left-radius: 8px; border-top-right-radius: 8px; font-weight: bold; margin-right: 2px; }
        QTabBar::tab:selected { background: #6D28D9; color: white; border-color: #6D28D9; }
        """)

        main_layout = QVBoxLayout(self)
        
        top_layout = QHBoxLayout()
        title = QLabel("<b>⚙️ Manage System Data</b>")
        title.setStyleSheet("font-size: 18px;")
        back_btn = QPushButton("Close")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.setStyleSheet("padding: 5px 15px; border: 1px solid #cbd5e1; border-radius: 5px; font-weight:bold; color: #0f172a;")
        back_btn.clicked.connect(self.close)
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(back_btn)
        
        self.tabs = QTabWidget()
        
        self.setup_professors_tab()
        self.setup_guardians_tab()
        self.setup_students_tab()
        self.setup_courses_tab()
        self.setup_enrollments_tab()
        self.setup_schedules_tab()
        self.setup_evaluations_tab()
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tabs)
        
        self.tabs.currentChanged.connect(self.load_all_data)
        self.load_all_data()

    # --- UI HELPER FOR 3-BUTTON LAYOUT ---
    def create_action_buttons(self, add_func, update_func, delete_func, clear_func):
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        btn_add = QPushButton("Add New")
        btn_add.setStyleSheet("background: #10B981; color: white; padding: 7px; border-radius: 5px; font-weight: bold;")
        btn_add.clicked.connect(add_func)
        
        btn_upd = QPushButton("Update Selected")
        btn_upd.setStyleSheet("background: #3B82F6; color: white; padding: 7px; border-radius: 5px; font-weight: bold;")
        btn_upd.clicked.connect(update_func)
        
        row1.addWidget(btn_add)
        row1.addWidget(btn_upd)
        
        row2 = QHBoxLayout()
        btn_del = QPushButton("Delete")
        btn_del.setStyleSheet("background: #EF4444; color: white; padding: 7px; border-radius: 5px; font-weight: bold;")
        btn_del.clicked.connect(delete_func)
        
        btn_clr = QPushButton("Clear Form")
        btn_clr.setStyleSheet("background: #E2E8F0; color: #0F172A; padding: 7px; border-radius: 5px; font-weight: bold;")
        btn_clr.clicked.connect(clear_func)
        
        row2.addWidget(btn_del)
        row2.addWidget(btn_clr)
        
        layout.addLayout(row1)
        layout.addLayout(row2)
        return layout

    # ==========================================================
    # TAB 1: PROFESSORS
    # ==========================================================
    def setup_professors_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        left_panel = QVBoxLayout()
        self.prof_id_hidden = None
        form_layout = QFormLayout()
        
        self.in_prof_first = QLineEdit()
        self.in_prof_last = QLineEdit()
        self.in_prof_user = QLineEdit()
        self.in_prof_dept = QLineEdit()
        self.in_prof_pass = QLineEdit()
        self.in_prof_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("<b>First Name:</b>", self.in_prof_first)
        form_layout.addRow("<b>Last Name:</b>", self.in_prof_last)
        form_layout.addRow("<b>Username:</b>", self.in_prof_user)
        form_layout.addRow("<b>Department:</b>", self.in_prof_dept)
        form_layout.addRow("<b>Password:</b>", self.in_prof_pass)
        left_panel.addLayout(form_layout)
        
        left_panel.addLayout(self.create_action_buttons(self.add_prof, self.update_prof, self.delete_prof, self.clear_prof))
        left_panel.addStretch()
        
        self.prof_table = QTableWidget(0, 5)
        self.prof_table.setHorizontalHeaderLabels(["ID", "First", "Last", "User", "Dept"])
        self.prof_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prof_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.prof_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.prof_table.itemSelectionChanged.connect(self.pop_prof)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.prof_table, 2)
        self.tabs.addTab(tab, "Professors")

    def clear_prof(self):
        self.prof_id_hidden = None
        for i in [self.in_prof_first, self.in_prof_last, self.in_prof_user, self.in_prof_dept, self.in_prof_pass]: i.clear()
        self.prof_table.clearSelection()

    def pop_prof(self):
        sel = self.prof_table.selectedItems()
        if sel:
            self.prof_id_hidden = int(sel[0].text())
            self.in_prof_first.setText(sel[1].text())
            self.in_prof_last.setText(sel[2].text())
            self.in_prof_user.setText(sel[3].text())
            self.in_prof_dept.setText(sel[4].text())

    def get_prof_payload(self):
        return {
            "First_Name": self.in_prof_first.text(), "Last_Name": self.in_prof_last.text(),
            "Username": self.in_prof_user.text(), "Department": self.in_prof_dept.text(), "Password": self.in_prof_pass.text()
        }

    def add_prof(self):
        p = self.get_prof_payload()
        if not p['Password']: return QMessageBox.warning(self, "Error", "Password required!")
        if requests.post("http://127.0.0.1:5001/api/admin/professors", json=p).status_code == 201: self.load_all_data()

    def update_prof(self):
        if not self.prof_id_hidden: return QMessageBox.warning(self, "Error", "Select a Professor first!")
        if requests.put(f"http://127.0.0.1:5001/api/admin/professors/{self.prof_id_hidden}", json=self.get_prof_payload()).status_code == 200: self.load_all_data()

    def delete_prof(self):
        if self.prof_id_hidden and QMessageBox.question(self, "Confirm", "Delete?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/professors/{self.prof_id_hidden}").status_code == 200: self.load_all_data()


    # ==========================================================
    # TAB 2: GUARDIANS
    # ==========================================================
    def setup_guardians_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        left_panel = QVBoxLayout()
        self.guard_id_hidden = None
        form_layout = QFormLayout()
        
        self.in_guard_first = QLineEdit()
        self.in_guard_last = QLineEdit()
        self.in_guard_phone = QLineEdit()
        self.in_guard_email = QLineEdit()
        
        form_layout.addRow("<b>First Name:</b>", self.in_guard_first)
        form_layout.addRow("<b>Last Name:</b>", self.in_guard_last)
        form_layout.addRow("<b>Phone Number:</b>", self.in_guard_phone)
        form_layout.addRow("<b>Email Address:</b>", self.in_guard_email)
        left_panel.addLayout(form_layout)
        
        left_panel.addLayout(self.create_action_buttons(self.add_guard, self.update_guard, self.delete_guard, self.clear_guard))
        left_panel.addStretch()
        
        self.guard_table = QTableWidget(0, 5)
        self.guard_table.setHorizontalHeaderLabels(["ID", "First", "Last", "Phone", "Email"])
        self.guard_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.guard_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.guard_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.guard_table.itemSelectionChanged.connect(self.pop_guard)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.guard_table, 2)
        self.tabs.addTab(tab, "Guardians")

    def clear_guard(self):
        self.guard_id_hidden = None
        for i in [self.in_guard_first, self.in_guard_last, self.in_guard_phone, self.in_guard_email]: i.clear()
        self.guard_table.clearSelection()

    def pop_guard(self):
        sel = self.guard_table.selectedItems()
        if sel:
            self.guard_id_hidden = int(sel[0].text())
            self.in_guard_first.setText(sel[1].text())
            self.in_guard_last.setText(sel[2].text())
            self.in_guard_phone.setText(sel[3].text())
            self.in_guard_email.setText(sel[4].text())

    def get_guard_payload(self):
        return {"First_Name": self.in_guard_first.text(), "Last_Name": self.in_guard_last.text(), "Contact_Number": self.in_guard_phone.text(), "Email": self.in_guard_email.text()}

    def add_guard(self):
        if requests.post("http://127.0.0.1:5001/api/admin/guardians", json=self.get_guard_payload()).status_code == 201: self.load_all_data()

    def update_guard(self):
        if not self.guard_id_hidden: return QMessageBox.warning(self, "Error", "Select a Guardian first!")
        if requests.put(f"http://127.0.0.1:5001/api/admin/guardians/{self.guard_id_hidden}", json=self.get_guard_payload()).status_code == 200: self.load_all_data()

    def delete_guard(self):
        if self.guard_id_hidden and QMessageBox.question(self, "Confirm", "Delete?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/guardians/{self.guard_id_hidden}").status_code == 200: self.load_all_data()


    # ==========================================================
    # TAB 3: STUDENTS
    # ==========================================================
    def setup_students_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        left_panel = QVBoxLayout()
        self.stud_id_hidden = None
        form_layout = QFormLayout()
        
        self.in_stud_first = QLineEdit()
        self.in_stud_last = QLineEdit()
        self.in_stud_user = QLineEdit()
        self.in_stud_guard = QComboBox()
        self.in_stud_pass = QLineEdit()
        self.in_stud_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("<b>First Name:</b>", self.in_stud_first)
        form_layout.addRow("<b>Last Name:</b>", self.in_stud_last)
        form_layout.addRow("<b>Username:</b>", self.in_stud_user)
        form_layout.addRow("<b>Guardian Name:</b>", self.in_stud_guard)
        form_layout.addRow("<b>Password:</b>", self.in_stud_pass)
        left_panel.addLayout(form_layout)
        
        left_panel.addLayout(self.create_action_buttons(self.add_stud, self.update_stud, self.delete_stud, self.clear_stud))
        left_panel.addStretch()
        
        self.stud_table = QTableWidget(0, 5)
        self.stud_table.setHorizontalHeaderLabels(["ID", "First", "Last", "User", "Guardian"])
        self.stud_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stud_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.stud_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.stud_table.itemSelectionChanged.connect(self.pop_stud)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.stud_table, 2)
        self.tabs.addTab(tab, "Students")

    def clear_stud(self):
        self.stud_id_hidden = None
        for i in [self.in_stud_first, self.in_stud_last, self.in_stud_user, self.in_stud_pass]: i.clear()
        self.in_stud_guard.setCurrentIndex(0)
        self.stud_table.clearSelection()

    def pop_stud(self):
        sel = self.stud_table.selectedItems()
        if sel:
            self.stud_id_hidden = int(sel[0].text())
            self.in_stud_first.setText(sel[1].text())
            self.in_stud_last.setText(sel[2].text())
            self.in_stud_user.setText(sel[3].text())
            idx = self.in_stud_guard.findText(sel[4].text(), Qt.MatchFlag.MatchContains)
            self.in_stud_guard.setCurrentIndex(idx if idx >= 0 else 0)

    def get_stud_payload(self):
        return {"First_Name": self.in_stud_first.text(), "Last_Name": self.in_stud_last.text(), "Username": self.in_stud_user.text(), "Password": self.in_stud_pass.text(), "Guardian_ID": self.in_stud_guard.currentData() or None}

    def add_stud(self):
        p = self.get_stud_payload()
        if not p['Password']: return QMessageBox.warning(self, "Error", "Password required!")
        if requests.post("http://127.0.0.1:5001/api/admin/students", json=p).status_code == 201: self.load_all_data()

    def update_stud(self):
        if not self.stud_id_hidden: return QMessageBox.warning(self, "Error", "Select a Student first!")
        if requests.put(f"http://127.0.0.1:5001/api/admin/students/{self.stud_id_hidden}", json=self.get_stud_payload()).status_code == 200: self.load_all_data()

    def delete_stud(self):
        if self.stud_id_hidden and QMessageBox.question(self, "Confirm", "Delete?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/students/{self.stud_id_hidden}").status_code == 200: self.load_all_data()


    # ==========================================================
    # TAB 4: COURSES
    # ==========================================================
    def setup_courses_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        left_panel = QVBoxLayout()
        self.course_id_hidden = None
        form_layout = QFormLayout()
        
        self.in_course_code = QLineEdit()
        self.in_course_title = QLineEdit()
        
        form_layout.addRow("<b>Course Code:</b>", self.in_course_code)
        form_layout.addRow("<b>Course Title:</b>", self.in_course_title)
        left_panel.addLayout(form_layout)
        
        left_panel.addLayout(self.create_action_buttons(self.add_course, self.update_course, self.delete_course, self.clear_course))
        left_panel.addStretch()
        
        self.course_table = QTableWidget(0, 2)
        self.course_table.setHorizontalHeaderLabels(["Code", "Title"])
        self.course_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.course_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.course_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.course_table.itemSelectionChanged.connect(self.pop_course)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.course_table, 2)
        self.tabs.addTab(tab, "Courses")

    def clear_course(self):
        self.course_id_hidden = None
        self.in_course_code.clear()
        self.in_course_title.clear()
        self.in_course_code.setReadOnly(False) # Re-enable typing Code
        self.course_table.clearSelection()

    def pop_course(self):
        sel = self.course_table.selectedItems()
        if sel:
            self.course_id_hidden = sel[0].text()
            self.in_course_code.setText(sel[0].text())
            self.in_course_code.setReadOnly(True) # Prevent changing Primary Key during Update!
            self.in_course_title.setText(sel[1].text())

    def add_course(self):
        c = self.in_course_code.text().strip()
        t = self.in_course_title.text().strip()
        if not c: return QMessageBox.warning(self, "Error", "Code Required!")
        if requests.post("http://127.0.0.1:5001/api/admin/courses", json={"Course_Code": c, "Course_Title": t}).status_code == 201: self.load_all_data()

    def update_course(self):
        if not self.course_id_hidden: return QMessageBox.warning(self, "Error", "Select Course first!")
        if requests.put(f"http://127.0.0.1:5001/api/admin/courses/{self.course_id_hidden}", json={"Course_Title": self.in_course_title.text()}).status_code == 200: self.load_all_data()

    def delete_course(self):
        if self.course_id_hidden and QMessageBox.question(self, "Confirm", "Delete?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/courses/{self.course_id_hidden}").status_code == 200: self.load_all_data()


    # ==========================================================
    # TAB 5: ENROLLMENTS (FIXED SEMESTER & SESSION CRASH)
    # ==========================================================
    def setup_enrollments_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        left_panel = QVBoxLayout()
        self.enroll_id_hidden = None
        form_layout = QFormLayout()
        
        self.in_enr_student = QComboBox()
        self.in_enr_course = QComboBox()
        self.in_enr_year = QLineEdit()
        self.in_enr_sem = QComboBox()
        self.in_enr_sem.addItems(["1st Semester", "2nd Semester", "Summer"])
        self.in_enr_grade = QLineEdit()
        
        form_layout.addRow("<b>Student Name:</b>", self.in_enr_student)
        form_layout.addRow("<b>Course Code:</b>", self.in_enr_course)
        form_layout.addRow("<b>School Year:</b>", self.in_enr_year)
        form_layout.addRow("<b>Semester:</b>", self.in_enr_sem)
        form_layout.addRow("<b>Grade:</b>", self.in_enr_grade)
        left_panel.addLayout(form_layout)
        
        left_panel.addLayout(self.create_action_buttons(self.add_enr, self.update_enr, self.delete_enr, self.clear_enr))
        left_panel.addStretch()
        
        self.enroll_table = QTableWidget(0, 6)
        self.enroll_table.setHorizontalHeaderLabels(["ID", "Student", "Course", "Year", "Sem", "Grade"])
        self.enroll_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.enroll_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.enroll_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.enroll_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.enroll_table.itemSelectionChanged.connect(self.pop_enr)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.enroll_table, 2)
        self.tabs.addTab(tab, "Enrollments")

    def clear_enr(self):
        self.enroll_id_hidden = None
        self.in_enr_year.clear()
        self.in_enr_grade.clear()
        self.enroll_table.clearSelection()

    def pop_enr(self):
        sel = self.enroll_table.selectedItems()
        if sel:
            self.enroll_id_hidden = int(sel[0].text())
            idx = self.in_enr_course.findText(sel[2].text(), Qt.MatchFlag.MatchContains)
            self.in_enr_course.setCurrentIndex(idx if idx >= 0 else 0)
            self.in_enr_year.setText(sel[3].text())
            
            idx_sem = self.in_enr_sem.findText(sel[4].text(), Qt.MatchFlag.MatchContains)
            self.in_enr_sem.setCurrentIndex(idx_sem if idx_sem >= 0 else 0)
            
            self.in_enr_grade.setText(sel[5].text())

    def get_enr_payload(self):
        return {
            "Student_ID": self.in_enr_student.currentData(), "Course_Code": self.in_enr_course.currentData(),
            "Academic_Year": self.in_enr_year.text().strip(), "Semester": self.in_enr_sem.currentText(), "Current_Grade": self.in_enr_grade.text().strip()
        }

    def add_enr(self):
        p = self.get_enr_payload()
        if not p['Student_ID'] or not p['Course_Code']: return QMessageBox.warning(self, "Error", "Select Student/Course")
        if requests.post("http://127.0.0.1:5001/api/admin/enrollments", json=p).status_code == 201: self.load_all_data()

    def update_enr(self):
        if not self.enroll_id_hidden: return QMessageBox.warning(self, "Error", "Select Enrollment first!")
        if requests.put(f"http://127.0.0.1:5001/api/admin/enrollments/{self.enroll_id_hidden}", json=self.get_enr_payload()).status_code == 200: self.load_all_data()

    def delete_enr(self):
        if self.enroll_id_hidden and QMessageBox.question(self, "Confirm", "Unenroll?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/enrollments/{self.enroll_id_hidden}").status_code == 200: self.load_all_data()


    # ==========================================================
    # TAB 6: SCHEDULES
    # ==========================================================
    def setup_schedules_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        left_panel = QVBoxLayout()
        self.sched_id_hidden = None
        form_layout = QFormLayout()
        
        self.in_sched_course = QComboBox()
        self.in_sched_day = QComboBox()
        self.in_sched_day.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.in_sched_start = QLineEdit()
        self.in_sched_end = QLineEdit()
        self.in_sched_room = QLineEdit()
        
        form_layout.addRow("<b>Course Code:</b>", self.in_sched_course)
        form_layout.addRow("<b>Room Number:</b>", self.in_sched_room)
        form_layout.addRow("<b>Day:</b>", self.in_sched_day)
        form_layout.addRow("<b>Start:</b>", self.in_sched_start)
        form_layout.addRow("<b>End:</b>", self.in_sched_end)
        left_panel.addLayout(form_layout)
        
        left_panel.addLayout(self.create_action_buttons(self.add_sched, self.update_sched, self.delete_sched, self.clear_sched))
        left_panel.addStretch()
        
        self.sched_table = QTableWidget(0, 6)
        self.sched_table.setHorizontalHeaderLabels(["ID", "Course", "Room", "Day", "Start", "End"])
        
        self.sched_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sched_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # ID
        self.sched_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Day
        self.sched_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Start Time
        self.sched_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # End Time
        
        self.sched_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sched_table.itemSelectionChanged.connect(self.pop_sched)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.sched_table, 2)
        self.tabs.addTab(tab, "Schedules")

    def clear_sched(self):
        self.sched_id_hidden = None
        for i in [self.in_sched_start, self.in_sched_end, self.in_sched_room]: i.clear()
        self.sched_table.clearSelection()

    def pop_sched(self):
        sel = self.sched_table.selectedItems()
        if sel:
            self.sched_id_hidden = int(sel[0].text())
            idx_c = self.in_sched_course.findText(sel[1].text(), Qt.MatchFlag.MatchContains)
            self.in_sched_course.setCurrentIndex(idx_c if idx_c >= 0 else 0)
            self.in_sched_room.setText(sel[2].text())
            idx_d = self.in_sched_day.findText(sel[3].text(), Qt.MatchFlag.MatchContains)
            self.in_sched_day.setCurrentIndex(idx_d if idx_d >= 0 else 0)
            self.in_sched_start.setText(sel[4].text())
            self.in_sched_end.setText(sel[5].text())

    def get_sched_payload(self):
        return {"Course_Code": self.in_sched_course.currentData(), "Room_Name": self.in_sched_room.text(), "Schedule_Day": self.in_sched_day.currentText(), "Start_Time": self.in_sched_start.text(), "End_Time": self.in_sched_end.text()}

    def add_sched(self):
        if requests.post("http://127.0.0.1:5001/api/admin/schedules", json=self.get_sched_payload()).status_code == 201: self.load_all_data()

    def update_sched(self):
        if not self.sched_id_hidden: return QMessageBox.warning(self, "Error", "Select Schedule first!")
        if requests.put(f"http://127.0.0.1:5001/api/admin/schedules/{self.sched_id_hidden}", json=self.get_sched_payload()).status_code == 200: self.load_all_data()

    def delete_sched(self):
        if self.sched_id_hidden and QMessageBox.question(self, "Confirm", "Delete?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/schedules/{self.sched_id_hidden}").status_code == 200: self.load_all_data()


    # ==========================================================
    # TAB 7: EVALUATIONS (DELETE ONLY)
    # ==========================================================
    def setup_evaluations_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>Moderate Evaluations</b>"))
        header_layout.addStretch()
        btn_del = QPushButton("🗑️ Delete Selected Evaluation")
        btn_del.setStyleSheet("background: #EF4444; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        btn_del.clicked.connect(self.del_eval)
        header_layout.addWidget(btn_del)
        
        # NEW: Updated to 7 columns to show the actual scores!
        self.eval_table = QTableWidget(0, 7)
        self.eval_table.setHorizontalHeaderLabels(["ID", "Course", "Clarity", "Pacing", "Comp.", "Engage.", "Date"])
        self.eval_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.eval_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.eval_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.eval_table)
        self.tabs.addTab(tab, "Evaluations")

    def del_eval(self):
        sel = self.eval_table.selectedItems()
        if sel and QMessageBox.question(self, "Warning", "Delete?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/evaluations/{sel[0].text()}").status_code == 200: self.load_all_data()


    # ==========================================================
    # DATA LOADER (SMART SEARCH)
    # ==========================================================
    def load_all_data(self):
        self.clear_prof()
        self.clear_guard()
        self.clear_stud()
        self.clear_course()
        self.clear_enr()
        self.clear_sched()
        
        try:
            guardians = requests.get("http://127.0.0.1:5001/api/admin/guardians").json().get("data", [])
            self.guard_table.setRowCount(len(guardians))
            self.in_stud_guard.blockSignals(True)
            self.in_stud_guard.clear()
            self.in_stud_guard.addItem("-- None --", None)
            for i, g in enumerate(guardians):
                self.guard_table.setItem(i, 0, QTableWidgetItem(str(g.get('Guardian_ID', ''))))
                self.guard_table.setItem(i, 1, QTableWidgetItem(g.get('First_Name', '')))
                self.guard_table.setItem(i, 2, QTableWidgetItem(g.get('Last_Name', '')))
                self.guard_table.setItem(i, 3, QTableWidgetItem(g.get('Contact_Number', '')))
                self.guard_table.setItem(i, 4, QTableWidgetItem(g.get('Email', '')))
                self.in_stud_guard.addItem(f"{g.get('First_Name', '')} {g.get('Last_Name', '')}", g.get('Guardian_ID'))
            self.in_stud_guard.blockSignals(False)

            profs = requests.get("http://127.0.0.1:5001/api/admin/professors").json().get("data", [])
            self.prof_table.setRowCount(len(profs))
            for i, p in enumerate(profs):
                self.prof_table.setItem(i, 0, QTableWidgetItem(str(p.get('Professor_ID', ''))))
                self.prof_table.setItem(i, 1, QTableWidgetItem(p.get('First_Name', '')))
                self.prof_table.setItem(i, 2, QTableWidgetItem(p.get('Last_Name', '')))
                self.prof_table.setItem(i, 3, QTableWidgetItem(p.get('Username', '')))
                self.prof_table.setItem(i, 4, QTableWidgetItem(p.get('Department', '')))

            studs = requests.get("http://127.0.0.1:5001/api/admin/students").json().get("data", [])
            self.stud_table.setRowCount(len(studs))
            self.in_enr_student.clear()
            for i, s in enumerate(studs):
                self.stud_table.setItem(i, 0, QTableWidgetItem(str(s.get('Student_ID', ''))))
                self.stud_table.setItem(i, 1, QTableWidgetItem(s.get('First_Name', '')))
                self.stud_table.setItem(i, 2, QTableWidgetItem(s.get('Last_Name', '')))
                self.stud_table.setItem(i, 3, QTableWidgetItem(s.get('Username', '')))
                self.stud_table.setItem(i, 4, QTableWidgetItem(s.get('Guardian_Name', 'None')))
                self.in_enr_student.addItem(f"{s.get('First_Name', '')} {s.get('Last_Name', '')}", s.get('Student_ID'))

            courses = requests.get("http://127.0.0.1:5001/api/admin/courses").json().get("data", [])
            self.course_table.setRowCount(len(courses))
            self.in_enr_course.clear()
            self.in_sched_course.clear()
            for i, c in enumerate(courses):
                code = c.get('Course_Code', '')
                self.course_table.setItem(i, 0, QTableWidgetItem(code))
                self.course_table.setItem(i, 1, QTableWidgetItem(c.get('Course_Title', '')))
                self.in_enr_course.addItem(code, code)
                self.in_sched_course.addItem(code, code)

            enrolls = requests.get("http://127.0.0.1:5001/api/admin/enrollments").json().get("data", [])
            self.enroll_table.setRowCount(len(enrolls))
            for i, enr in enumerate(enrolls):
                self.enroll_table.setItem(i, 0, QTableWidgetItem(str(enr.get('Enrollment_ID', ''))))
                self.enroll_table.setItem(i, 1, QTableWidgetItem(enr.get('Student_Name', '')))
                self.enroll_table.setItem(i, 2, QTableWidgetItem(enr.get('Course_Code', '')))
                self.enroll_table.setItem(i, 3, QTableWidgetItem(enr.get('Academic_Year', '')))
                self.enroll_table.setItem(i, 4, QTableWidgetItem(enr.get('Semester', '')))
                self.enroll_table.setItem(i, 5, QTableWidgetItem(str(enr.get('Current_Grade', 'N/A'))))

                sem_val = enr.get('Semester')
                self.enroll_table.setItem(i, 4, QTableWidgetItem(str(sem_val) if sem_val else "N/A"))

            scheds = requests.get("http://127.0.0.1:5001/api/admin/schedules").json().get("data", [])
            self.sched_table.setRowCount(len(scheds))
            for i, sch in enumerate(scheds):
                self.sched_table.setItem(i, 0, QTableWidgetItem(str(sch.get('Schedule_ID', ''))))
                self.sched_table.setItem(i, 1, QTableWidgetItem(sch.get('Course_Code', '')))
                self.sched_table.setItem(i, 2, QTableWidgetItem(sch.get('Room_Name', '')))
                self.sched_table.setItem(i, 3, QTableWidgetItem(sch.get('Schedule_Day', '')))
                self.sched_table.setItem(i, 4, QTableWidgetItem(str(sch.get('Start_Time', ''))))
                self.sched_table.setItem(i, 5, QTableWidgetItem(str(sch.get('End_Time', ''))))

            # SMART EVALUATION LOADER: Anonymous & Date Formatted
            evals = requests.get("http://127.0.0.1:5001/api/admin/evaluations").json().get("data", [])
            if hasattr(self, 'eval_table'):
                self.eval_table.setRowCount(len(evals))
                for i, ev in enumerate(evals):
                    self.eval_table.setItem(i, 0, QTableWidgetItem(str(ev.get('Evaluation_ID', ''))))
                    self.eval_table.setItem(i, 1, QTableWidgetItem(ev.get('Course_Code', 'Unknown')))
                    
                    # Notice how the indices shifted because Student is gone! (2, 3, 4, 5)
                    self.eval_table.setItem(i, 2, QTableWidgetItem(str(ev.get('Clarity_Score', '-'))))
                    self.eval_table.setItem(i, 3, QTableWidgetItem(str(ev.get('Pacing_Score', '-'))))
                    self.eval_table.setItem(i, 4, QTableWidgetItem(str(ev.get('Comprehension_Score', '-'))))
                    self.eval_table.setItem(i, 5, QTableWidgetItem(str(ev.get('Engagement_Score', '-'))))
                    
                    # Grab our perfectly formatted date from MySQL
                    date_str = ev.get('Formatted_Date') or "N/A"
                    self.eval_table.setItem(i, 6, QTableWidgetItem(date_str))

        except Exception as e:
            print("Error loading data:", e)