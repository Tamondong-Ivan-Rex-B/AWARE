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
        self.resize(950, 600)
        
        self.setStyleSheet("""
        QWidget { background-color: white; }
        QLabel { color: #0f172a; font-size: 13px; }
        QLineEdit { padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; color: #0f172a; }
        QComboBox { padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; color: #5071c1; font-weight: bold; }
        QLineEdit { padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; color: #0f172a; }
        
        /* The main dropdown button */
        QComboBox { padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; background: #f8fafc; color: #5071c1; font-weight: bold; }
        
        /* NEW: The dropdown list that pops open */
        QComboBox QAbstractItemView {
            background-color: white;
            color: #0f172a; /* Dark slate text so you can read the names */
            selection-background-color: #f1f5f9; /* Light gray highlight when hovering */
            selection-color: #6D28D9; /* Turns purple when you hover over a name */
            border: 1px solid #cbd5e1;
            outline: none; /* Removes the dotted line when clicking */
        }
        
        QLineEdit:focus, QComboBox:focus { border: 1px solid #6D28D9; background: white; }
        QTableWidget { border: 1px solid #e2e8f0; border-radius: 6px; gridline-color: #e2e8f0; color: #5071c1; background-color: white; }
        QTableWidget::item { padding: 5px; }
        QTableWidget::item:selected { background-color: #f8fafc; color: #6D28D9; font-weight: bold; }
        QHeaderView::section { background-color: #f8fafc; padding: 10px; border: none; border-bottom: 2px solid #e2e8f0; font-weight: bold; color: #5071c1; }
        QTabWidget::pane { border: 1px solid #e2e8f0; background: white; border-radius: 8px; }
        QTabBar::tab {
            background: #f1f5f9; color: #64748b; padding: 10px 20px; 
            border: 1px solid #e2e8f0; border-bottom-color: #e2e8f0;
            border-top-left-radius: 8px; border-top-right-radius: 8px;
            font-weight: bold; margin-right: 2px;
        }
        QTabBar::tab:selected { background: #6D28D9; color: white; border-color: #6D28D9; }
        QTabBar::tab:hover:!selected { background: #e2e8f0; }
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
        self.setup_guardians_tab() # NEW
        self.setup_students_tab()  # Moved after Guardians so the dropdown loads properly!
        self.setup_courses_tab()
        self.setup_sessions_tab()    # NEW
        self.setup_enrollments_tab() # NEW
        self.setup_schedules_tab()   # NEW
        self.setup_evaluations_tab() # NEW
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tabs)
        
        self.tabs.currentChanged.connect(self.load_all_data)
        self.load_all_data()

    # ==========================================================
    # TAB 1: PROFESSORS
    # ==========================================================
    def setup_professors_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Professor Details</b>"))
        self.prof_id_hidden = None
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.in_prof_first = QLineEdit()
        self.in_prof_last = QLineEdit()
        self.in_prof_user = QLineEdit()
        self.in_prof_dept = QLineEdit() # NEW
        self.in_prof_dept.setPlaceholderText("e.g. Computer Engineering")
        self.in_prof_pass = QLineEdit()
        self.in_prof_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("<b>First Name:</b>", self.in_prof_first)
        form_layout.addRow("<b>Last Name:</b>", self.in_prof_last)
        form_layout.addRow("<b>Username:</b>", self.in_prof_user)
        form_layout.addRow("<b>Department:</b>", self.in_prof_dept) # NEW
        form_layout.addRow("<b>Password:</b>", self.in_prof_pass)
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save / Add")
        btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_save.clicked.connect(self.save_professor)
        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_professor)
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_prof_form)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(btn_clear)
        left_panel.addStretch()
        
        self.prof_table = QTableWidget(0, 5) # Updated columns
        self.prof_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Username", "Dept."])
        self.prof_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prof_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.prof_table.itemSelectionChanged.connect(self.populate_prof_form)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.prof_table, 2)
        self.tabs.addTab(tab, "Professors")

    def clear_prof_form(self):
        self.prof_id_hidden = None
        for i in [self.in_prof_first, self.in_prof_last, self.in_prof_user, self.in_prof_dept, self.in_prof_pass]: i.clear()
        self.prof_table.clearSelection()

    def populate_prof_form(self):
        selected = self.prof_table.selectedItems()
        if selected:
            self.prof_id_hidden = int(selected[0].text())
            self.in_prof_first.setText(selected[1].text())
            self.in_prof_last.setText(selected[2].text())
            self.in_prof_user.setText(selected[3].text())
            self.in_prof_dept.setText(selected[4].text())
            self.in_prof_pass.clear()

    def save_professor(self):
        payload = {
            "First_Name": self.in_prof_first.text(), "Last_Name": self.in_prof_last.text(),
            "Username": self.in_prof_user.text(), "Department": self.in_prof_dept.text(), "Password": self.in_prof_pass.text()
        }
        if self.prof_id_hidden is None:
            if not payload['Password']: return QMessageBox.warning(self, "Error", "Password required!")
            res = requests.post("http://127.0.0.1:5001/api/admin/professors", json=payload)
        else:
            res = requests.put(f"http://127.0.0.1:5001/api/admin/professors/{self.prof_id_hidden}", json=payload)
        
        if res.status_code in [200, 201]: self.load_all_data()

    def delete_professor(self):
        if self.prof_id_hidden and QMessageBox.question(self, "Confirm", "Delete professor?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/professors/{self.prof_id_hidden}").status_code == 200:
                self.load_all_data()

    # ==========================================================
    # TAB 2: GUARDIANS (NEW)
    # ==========================================================
    def setup_guardians_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Guardian Details</b>"))
        self.guard_id_hidden = None
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.in_guard_first = QLineEdit()
        self.in_guard_last = QLineEdit()
        self.in_guard_phone = QLineEdit()
        self.in_guard_email = QLineEdit()
        
        form_layout.addRow("<b>First Name:</b>", self.in_guard_first)
        form_layout.addRow("<b>Last Name:</b>", self.in_guard_last)
        form_layout.addRow("<b>Contact #:</b>", self.in_guard_phone)
        form_layout.addRow("<b>Email:</b>", self.in_guard_email)
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save / Add")
        btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_save.clicked.connect(self.save_guardian)
        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_guardian)
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_guard_form)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(btn_clear)
        left_panel.addStretch()
        
        self.guard_table = QTableWidget(0, 5)
        self.guard_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Phone", "Email"])
        self.guard_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.guard_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.guard_table.itemSelectionChanged.connect(self.populate_guard_form)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.guard_table, 2)
        self.tabs.addTab(tab, "Guardians")

    def clear_guard_form(self):
        self.guard_id_hidden = None
        for i in [self.in_guard_first, self.in_guard_last, self.in_guard_phone, self.in_guard_email]: i.clear()
        self.guard_table.clearSelection()

    def populate_guard_form(self):
        selected = self.guard_table.selectedItems()
        if selected:
            self.guard_id_hidden = int(selected[0].text())
            self.in_guard_first.setText(selected[1].text())
            self.in_guard_last.setText(selected[2].text())
            self.in_guard_phone.setText(selected[3].text())
            self.in_guard_email.setText(selected[4].text())

    def save_guardian(self):
        payload = {
            "First_Name": self.in_guard_first.text(), "Last_Name": self.in_guard_last.text(),
            "Contact_Number": self.in_guard_phone.text(), "Email": self.in_guard_email.text()
        }
        if self.guard_id_hidden is None:
            res = requests.post("http://127.0.0.1:5001/api/admin/guardians", json=payload)
        else:
            res = requests.put(f"http://127.0.0.1:5001/api/admin/guardians/{self.guard_id_hidden}", json=payload)
        
        if res.status_code in [200, 201]: self.load_all_data()

    def delete_guardian(self):
        if self.guard_id_hidden and QMessageBox.question(self, "Confirm", "Delete guardian?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/guardians/{self.guard_id_hidden}").status_code == 200:
                self.load_all_data()

    # ==========================================================
    # TAB 3: STUDENTS (UPDATED WITH GUARDIAN DROPDOWN)
    # ==========================================================
    def setup_students_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Student Details</b>"))
        self.stud_id_hidden = None
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.in_stud_first = QLineEdit()
        self.in_stud_last = QLineEdit()
        self.in_stud_user = QLineEdit()
        self.in_stud_guard = QComboBox() # NEW: Dropdown for Guardians
        self.in_stud_pass = QLineEdit()
        self.in_stud_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("<b>First Name:</b>", self.in_stud_first)
        form_layout.addRow("<b>Last Name:</b>", self.in_stud_last)
        form_layout.addRow("<b>Username:</b>", self.in_stud_user)
        form_layout.addRow("<b>Guardian:</b>", self.in_stud_guard) # NEW
        form_layout.addRow("<b>Password:</b>", self.in_stud_pass)
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save / Add")
        btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_save.clicked.connect(self.save_student)
        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_student)
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_stud_form)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(btn_clear)
        left_panel.addStretch()
        
        self.stud_table = QTableWidget(0, 5) # Increased to 5
        self.stud_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Username", "Guardian"])
        self.stud_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stud_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.stud_table.itemSelectionChanged.connect(self.populate_stud_form)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.stud_table, 2)
        self.tabs.addTab(tab, "Students")

    def clear_stud_form(self):
        self.stud_id_hidden = None
        for i in [self.in_stud_first, self.in_stud_last, self.in_stud_user, self.in_stud_pass]: i.clear()
        self.in_stud_guard.setCurrentIndex(0)
        self.stud_table.clearSelection()

    def populate_stud_form(self):
        selected = self.stud_table.selectedItems()
        if selected:
            self.stud_id_hidden = int(selected[0].text())
            self.in_stud_first.setText(selected[1].text())
            self.in_stud_last.setText(selected[2].text())
            self.in_stud_user.setText(selected[3].text())
            
            # Find the matching guardian in the dropdown
            guard_text = selected[4].text()
            index = self.in_stud_guard.findText(guard_text, Qt.MatchFlag.MatchContains)
            if index >= 0: self.in_stud_guard.setCurrentIndex(index)
            else: self.in_stud_guard.setCurrentIndex(0)

    def save_student(self):
        guard_data = self.in_stud_guard.currentData() # Gets the hidden Guardian_ID
        payload = {
            "First_Name": self.in_stud_first.text(), "Last_Name": self.in_stud_last.text(),
            "Username": self.in_stud_user.text(), "Password": self.in_stud_pass.text(),
            "Guardian_ID": guard_data if guard_data else None
        }
        if self.stud_id_hidden is None:
            if not payload['Password']: return QMessageBox.warning(self, "Error", "Password required!")
            res = requests.post("http://127.0.0.1:5001/api/admin/students", json=payload)
        else:
            res = requests.put(f"http://127.0.0.1:5001/api/admin/students/{self.stud_id_hidden}", json=payload)
        
        if res.status_code in [200, 201]: self.load_all_data()

    def delete_student(self):
        if self.stud_id_hidden and QMessageBox.question(self, "Confirm", "Delete student?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/students/{self.stud_id_hidden}").status_code == 200:
                self.load_all_data()

    # ==========================================================
    # TAB 4: COURSES
    # ==========================================================
    def setup_courses_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Course Details</b>"))
        form_layout = QFormLayout()
        self.in_course_code = QLineEdit()
        form_layout.addRow("<b>Course Code:</b>", self.in_course_code)
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Add Course")
        btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_save.clicked.connect(self.save_course)
        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_course)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        left_panel.addLayout(btn_layout)
        left_panel.addStretch()
        
        self.course_table = QTableWidget(0, 1)
        self.course_table.setHorizontalHeaderLabels(["Course Code"])
        self.course_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.course_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.course_table.itemSelectionChanged.connect(lambda: self.in_course_code.setText(self.course_table.selectedItems()[0].text() if self.course_table.selectedItems() else ""))
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.course_table, 2)
        self.tabs.addTab(tab, "Courses")

    def save_course(self):
        code = self.in_course_code.text().strip()
        if code and requests.post("http://127.0.0.1:5001/api/admin/courses", json={"Course_Code": code}).status_code == 201:
            self.in_course_code.clear()
            self.load_all_data()

    def delete_course(self):
        code = self.in_course_code.text().strip()
        if code and QMessageBox.question(self, "Confirm", "Delete course?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/courses/{code}").status_code == 200:
                self.in_course_code.clear()
                self.load_all_data()
    
    # ==========================================================
    # TAB 5: CLASS SESSIONS (Course + Professor)
    # ==========================================================
    def setup_sessions_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Create Class Session</b>"))
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # DROPDOWNS FOR FOREIGN KEYS!
        self.in_sess_course = QComboBox() 
        self.in_sess_prof = QComboBox()
        
        form_layout.addRow("<b>Course:</b>", self.in_sess_course)
        form_layout.addRow("<b>Professor:</b>", self.in_sess_prof)
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Create Session")
        btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_save.clicked.connect(self.save_session)
        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_session)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        left_panel.addLayout(btn_layout)
        left_panel.addStretch()
        
        self.sess_table = QTableWidget(0, 3)
        self.sess_table.setHorizontalHeaderLabels(["Session ID", "Course", "Professor"])
        self.sess_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sess_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.sess_table, 2)
        self.tabs.addTab(tab, "Class Sessions")

    def save_session(self):
        course = self.in_sess_course.currentData()
        prof_id = self.in_sess_prof.currentData()
        if not course or not prof_id: return QMessageBox.warning(self, "Error", "Please select a Course and Professor.")
        
        res = requests.post("http://127.0.0.1:5001/api/admin/sessions", json={"Course_Code": course, "Professor_ID": prof_id})
        if res.status_code == 201: self.load_all_data()

    def delete_session(self):
        selected = self.sess_table.selectedItems()
        if selected and QMessageBox.question(self, "Confirm", "Delete this Session?") == QMessageBox.StandardButton.Yes:
            session_id = selected[0].text()
            if requests.delete(f"http://127.0.0.1:5001/api/admin/sessions/{session_id}").status_code == 200:
                self.load_all_data()

    # ==========================================================
    # TAB: ENROLLMENTS (UPDATED TO MATCH DB)
    # ==========================================================
    def setup_enrollments_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Enroll Student</b>"))
        self.enroll_id_hidden = None
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.in_enr_student = QComboBox()
        self.in_enr_course = QComboBox() # Changed from Session to Course
        
        self.in_enr_year = QLineEdit()
        self.in_enr_year.setPlaceholderText("e.g. 2025-2026")
        
        self.in_enr_sem = QComboBox()
        self.in_enr_sem.addItems(["1st Semester", "2nd Semester", "Summer"])
        
        self.in_enr_grade = QLineEdit()
        self.in_enr_grade.setPlaceholderText("e.g. 85.5")
        
        form_layout.addRow("<b>Student:</b>", self.in_enr_student)
        form_layout.addRow("<b>Course:</b>", self.in_enr_course)
        form_layout.addRow("<b>Acad Year:</b>", self.in_enr_year)
        form_layout.addRow("<b>Semester:</b>", self.in_enr_sem)
        form_layout.addRow("<b>Grade:</b>", self.in_enr_grade)
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save / Enroll")
        btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_save.clicked.connect(self.save_enrollment)
        btn_delete = QPushButton("Unenroll")
        btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_enrollment)
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_enroll_form)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(btn_clear)
        left_panel.addStretch()
        
        self.enroll_table = QTableWidget(0, 6)
        self.enroll_table.setHorizontalHeaderLabels(["ID", "Student", "Course", "Year", "Sem", "Grade"])
        self.enroll_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.enroll_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.enroll_table.itemSelectionChanged.connect(self.populate_enroll_form)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.enroll_table, 2)
        self.tabs.addTab(tab, "Enrollments")

    def clear_enroll_form(self):
        self.enroll_id_hidden = None
        self.in_enr_year.clear()
        self.in_enr_grade.clear()
        self.enroll_table.clearSelection()

    def populate_enroll_form(self):
        selected = self.enroll_table.selectedItems()
        if selected:
            self.enroll_id_hidden = int(selected[0].text())
            # Find matching course
            course_text = selected[2].text()
            index = self.in_enr_course.findText(course_text, Qt.MatchFlag.MatchContains)
            if index >= 0: self.in_enr_course.setCurrentIndex(index)
            
            self.in_enr_year.setText(selected[3].text())
            
            sem_text = selected[4].text()
            index_sem = self.in_enr_sem.findText(sem_text, Qt.MatchFlag.MatchContains)
            if index_sem >= 0: self.in_enr_sem.setCurrentIndex(index_sem)
            
            self.in_enr_grade.setText(selected[5].text())

    def save_enrollment(self):
        stud_id = self.in_enr_student.currentData()
        course = self.in_enr_course.currentData()
        payload = {
            "Student_ID": stud_id, "Course_Code": course, 
            "Academic_Year": self.in_enr_year.text().strip(),
            "Semester": self.in_enr_sem.currentText(),
            "Current_Grade": self.in_enr_grade.text().strip()
        }
        
        if self.enroll_id_hidden is None:
            if not stud_id or not course: return QMessageBox.warning(self, "Error", "Select Student and Course.")
            res = requests.post("http://127.0.0.1:5001/api/admin/enrollments", json=payload)
        else:
            res = requests.put(f"http://127.0.0.1:5001/api/admin/enrollments/{self.enroll_id_hidden}", json=payload)
        
        if res.status_code in [200, 201]: self.load_all_data()

    def delete_enrollment(self):
        if self.enroll_id_hidden and QMessageBox.question(self, "Confirm", "Unenroll student?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/enrollments/{self.enroll_id_hidden}").status_code == 200:
                self.load_all_data()

    # ==========================================================
    # TAB: CLASS SCHEDULES (UPDATED TO MATCH DB)
    # ==========================================================
    def setup_schedules_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Schedule Details</b>"))
        self.sched_id_hidden = None
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.in_sched_course = QComboBox() # Changed from Session to Course
        self.in_sched_day = QComboBox()
        self.in_sched_day.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        self.in_sched_start = QLineEdit()
        self.in_sched_start.setPlaceholderText("e.g. 09:00")
        self.in_sched_end = QLineEdit()
        self.in_sched_end.setPlaceholderText("e.g. 12:00")
        self.in_sched_room = QLineEdit()
        self.in_sched_room.setPlaceholderText("e.g. Room 402")
        
        form_layout.addRow("<b>Course:</b>", self.in_sched_course)
        form_layout.addRow("<b>Room Name:</b>", self.in_sched_room)
        form_layout.addRow("<b>Day:</b>", self.in_sched_day)
        form_layout.addRow("<b>Start Time:</b>", self.in_sched_start)
        form_layout.addRow("<b>End Time:</b>", self.in_sched_end)
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save / Add")
        btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_save.clicked.connect(self.save_schedule)
        btn_delete = QPushButton("Delete")
        btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_schedule)
        btn_clear = QPushButton("Clear")
        btn_clear.clicked.connect(self.clear_sched_form)
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_delete)
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(btn_clear)
        left_panel.addStretch()
        
        self.sched_table = QTableWidget(0, 6)
        self.sched_table.setHorizontalHeaderLabels(["ID", "Course", "Room", "Day", "Start", "End"])
        self.sched_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sched_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.sched_table.itemSelectionChanged.connect(self.populate_sched_form)
        
        layout.addLayout(left_panel, 1)
        layout.addWidget(self.sched_table, 2)
        self.tabs.addTab(tab, "Schedules")

    def clear_sched_form(self):
        self.sched_id_hidden = None
        for i in [self.in_sched_start, self.in_sched_end, self.in_sched_room]: i.clear()
        self.sched_table.clearSelection()

    def populate_sched_form(self):
        selected = self.sched_table.selectedItems()
        if selected:
            self.sched_id_hidden = int(selected[0].text())
            
            course_text = selected[1].text()
            index = self.in_sched_course.findText(course_text, Qt.MatchFlag.MatchContains)
            if index >= 0: self.in_sched_course.setCurrentIndex(index)
            
            self.in_sched_room.setText(selected[2].text())
            
            day_text = selected[3].text()
            index_day = self.in_sched_day.findText(day_text, Qt.MatchFlag.MatchContains)
            if index_day >= 0: self.in_sched_day.setCurrentIndex(index_day)
            
            self.in_sched_start.setText(selected[4].text())
            self.in_sched_end.setText(selected[5].text())

    def save_schedule(self):
        payload = {
            "Course_Code": self.in_sched_course.currentData(),
            "Room_Name": self.in_sched_room.text(),
            "Schedule_Day": self.in_sched_day.currentText(),
            "Start_Time": self.in_sched_start.text(),
            "End_Time": self.in_sched_end.text()
        }
        if not payload['Course_Code']: return QMessageBox.warning(self, "Error", "Select a Course.")
        
        if self.sched_id_hidden is None:
            res = requests.post("http://127.0.0.1:5001/api/admin/schedules", json=payload)
        else:
            res = requests.put(f"http://127.0.0.1:5001/api/admin/schedules/{self.sched_id_hidden}", json=payload)
        
        if res.status_code in [200, 201]: self.load_all_data()

    def delete_schedule(self):
        if self.sched_id_hidden and QMessageBox.question(self, "Confirm", "Delete schedule?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/schedules/{self.sched_id_hidden}").status_code == 200:
                self.load_all_data()

    # ==========================================================
    # TAB: EVALUATIONS (BULLETPROOF UI)
    # ==========================================================
    def setup_evaluations_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>Review & Moderate Evaluations</b><br><span style='color:gray;'>Admins can only delete fake/inappropriate evaluations.</span>"))
        header_layout.addStretch()
        
        self.btn_del_eval = QPushButton("🗑️ Delete Selected Evaluation")
        self.btn_del_eval.setStyleSheet("background: #EF4444; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.btn_del_eval.clicked.connect(self.delete_evaluation)
        header_layout.addWidget(self.btn_del_eval)
        
        self.eval_table = QTableWidget(0, 3) # Simplified to just ID, Student, and Course
        self.eval_table.setHorizontalHeaderLabels(["Eval ID", "Student Name", "Course Code"])
        self.eval_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.eval_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.eval_table)
        self.tabs.addTab(tab, "Evaluations (Moderation)")

    def delete_evaluation(self):
        selected = self.eval_table.selectedItems()
        if not selected: return QMessageBox.warning(self, "Error", "Select an evaluation to delete.")
        
        eval_id = selected[0].text()
        if QMessageBox.question(self, "Warning", "Permanently delete this evaluation record?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/evaluations/{eval_id}").status_code == 200:
                self.load_all_data()

    def clear_enroll_form(self):
        self.enroll_id_hidden = None
        self.in_enr_grade.clear()
        self.enroll_table.clearSelection()

    def populate_enroll_form(self):
        selected = self.enroll_table.selectedItems()
        if selected:
            self.enroll_id_hidden = int(selected[0].text())
            self.in_enr_grade.setText(selected[3].text())

    def save_enrollment(self):
        stud_id = self.in_enr_student.currentData()
        sess_id = self.in_enr_session.currentData()
        grade = self.in_enr_grade.text().strip()
        
        if self.enroll_id_hidden is None:
            if not stud_id or not sess_id: return QMessageBox.warning(self, "Error", "Select Student and Session.")
            res = requests.post("http://127.0.0.1:5001/api/admin/enrollments", json={
                "Student_ID": stud_id, "Session_ID": sess_id, "Current_Grade": grade
            })
        else:
            res = requests.put(f"http://127.0.0.1:5001/api/admin/enrollments/{self.enroll_id_hidden}", json={"Current_Grade": grade})
        
        if res.status_code in [200, 201]: self.load_all_data()

    def delete_enrollment(self):
        if self.enroll_id_hidden and QMessageBox.question(self, "Confirm", "Unenroll student?") == QMessageBox.StandardButton.Yes:
            if requests.delete(f"http://127.0.0.1:5001/api/admin/enrollments/{self.enroll_id_hidden}").status_code == 200:
                self.load_all_data()

    # ==========================================================
    # DATA LOADER
    # ==========================================================
    def load_all_data(self):
        self.clear_prof_form()
        self.clear_guard_form()
        self.clear_stud_form()
        
        try:
            # 1. Load Guardians
            res_guard = requests.get("http://127.0.0.1:5001/api/admin/guardians")
            guardians = res_guard.json().get("data", []) if res_guard.status_code == 200 else []
            self.guard_table.setRowCount(len(guardians))
            
            self.in_stud_guard.blockSignals(True)
            self.in_stud_guard.clear()
            self.in_stud_guard.addItem("-- No Guardian --", None) # Default empty option
            
            for i, g in enumerate(guardians):
                self.guard_table.setItem(i, 0, QTableWidgetItem(str(g['Guardian_ID'])))
                self.guard_table.setItem(i, 1, QTableWidgetItem(g['First_Name']))
                self.guard_table.setItem(i, 2, QTableWidgetItem(g['Last_Name']))
                self.guard_table.setItem(i, 3, QTableWidgetItem(g.get('Contact_Number', '')))
                self.guard_table.setItem(i, 4, QTableWidgetItem(g.get('Email', '')))
                
                # Add to Student Dropdown
                self.in_stud_guard.addItem(f"{g['First_Name']} {g['Last_Name']} (ID: {g['Guardian_ID']})", g['Guardian_ID'])
            self.in_stud_guard.blockSignals(False)

            # 2. Load Professors
            res_prof = requests.get("http://127.0.0.1:5001/api/admin/professors")
            profs = res_prof.json().get("data", []) if res_prof.status_code == 200 else []
            self.prof_table.setRowCount(len(profs))
            for i, p in enumerate(profs):
                self.prof_table.setItem(i, 0, QTableWidgetItem(str(p['Professor_ID'])))
                self.prof_table.setItem(i, 1, QTableWidgetItem(p['First_Name']))
                self.prof_table.setItem(i, 2, QTableWidgetItem(p['Last_Name']))
                self.prof_table.setItem(i, 3, QTableWidgetItem(p['Username']))
                self.prof_table.setItem(i, 4, QTableWidgetItem(p.get('Department', '')))

            # 3. Load Students
            res_stud = requests.get("http://127.0.0.1:5001/api/admin/students")
            studs = res_stud.json().get("data", []) if res_stud.status_code == 200 else []
            self.stud_table.setRowCount(len(studs))
            for i, s in enumerate(studs):
                self.stud_table.setItem(i, 0, QTableWidgetItem(str(s['Student_ID'])))
                self.stud_table.setItem(i, 1, QTableWidgetItem(s['First_Name']))
                self.stud_table.setItem(i, 2, QTableWidgetItem(s['Last_Name']))
                self.stud_table.setItem(i, 3, QTableWidgetItem(s['Username']))
                self.stud_table.setItem(i, 4, QTableWidgetItem(s.get('Guardian_Name') or "None"))

            # 4. Load Courses
            res_course = requests.get("http://127.0.0.1:5001/api/admin/courses")
            courses = res_course.json().get("data", []) if res_course.status_code == 200 else []
            self.course_table.setRowCount(len(courses))
            for i, c in enumerate(courses):
                self.course_table.setItem(i, 0, QTableWidgetItem(c['Course_Code']))
                
            # 5. Load Class Sessions (And populate dropdowns)
            self.in_sess_course.clear()
            self.in_sess_prof.clear()
            self.in_enr_session.clear()
            
            for c in courses: # Populate course dropdown for Sessions
                self.in_sess_course.addItem(c['Course_Code'], c['Course_Code'])
            for p in profs: # Populate professor dropdown for Sessions
                self.in_sess_prof.addItem(f"{p['First_Name']} {p['Last_Name']}", p['Professor_ID'])

            res_sess = requests.get("http://127.0.0.1:5001/api/admin/sessions")
            sessions = res_sess.json().get("data", []) if res_sess.status_code == 200 else []
            self.sess_table.setRowCount(len(sessions))
            
            for i, sess in enumerate(sessions):
                self.sess_table.setItem(i, 0, QTableWidgetItem(str(sess['Session_ID'])))
                self.sess_table.setItem(i, 1, QTableWidgetItem(sess['Course_Code']))
                self.sess_table.setItem(i, 2, QTableWidgetItem(sess['Professor_Name']))
                
                # Add this session to the Enrollment dropdown (e.g. "CPE111 - Rudo")
                display_text = f"{sess['Course_Code']} - {sess['Professor_Name']}"
                self.in_enr_session.addItem(display_text, sess['Session_ID'])

            # 6. Load Enrollments
            self.in_enr_student.clear()
            self.in_enr_course.clear()
            for s in studs: self.in_enr_student.addItem(f"{s['First_Name']} {s['Last_Name']}", s['Student_ID'])
            for c in courses: self.in_enr_course.addItem(c['Course_Code'], c['Course_Code'])

            res_enr = requests.get("http://127.0.0.1:5001/api/admin/enrollments")
            enrollments = res_enr.json().get("data", []) if res_enr.status_code == 200 else []
            self.enroll_table.setRowCount(len(enrollments))
            for i, enr in enumerate(enrollments):
                self.enroll_table.setItem(i, 0, QTableWidgetItem(str(enr['Enrollment_ID'])))
                self.enroll_table.setItem(i, 1, QTableWidgetItem(enr['Student_Name']))
                self.enroll_table.setItem(i, 2, QTableWidgetItem(enr['Course_Code']))
                self.enroll_table.setItem(i, 3, QTableWidgetItem(enr.get('Academic_Year', 'N/A')))
                self.enroll_table.setItem(i, 4, QTableWidgetItem(enr.get('Semester', 'N/A')))
                grade = str(enr['Current_Grade']) if enr['Current_Grade'] is not None else "N/A"
                self.enroll_table.setItem(i, 5, QTableWidgetItem(grade))

            # 7. Load Schedules
            self.in_sched_course.clear()
            for c in courses: self.in_sched_course.addItem(c['Course_Code'], c['Course_Code'])
            
            res_sched = requests.get("http://127.0.0.1:5001/api/admin/schedules")
            schedules = res_sched.json().get("data", []) if res_sched.status_code == 200 else []
            self.sched_table.setRowCount(len(schedules))
            for i, sch in enumerate(schedules):
                self.sched_table.setItem(i, 0, QTableWidgetItem(str(sch['Schedule_ID'])))
                self.sched_table.setItem(i, 1, QTableWidgetItem(sch['Course_Code']))
                self.sched_table.setItem(i, 2, QTableWidgetItem(sch['Room_Name']))
                self.sched_table.setItem(i, 3, QTableWidgetItem(sch['Schedule_Day']))
                self.sched_table.setItem(i, 4, QTableWidgetItem(str(sch['Start_Time'])))
                self.sched_table.setItem(i, 5, QTableWidgetItem(str(sch['End_Time'])))

            # 8. Load Evaluations (Bulletproof)
            res_eval = requests.get("http://127.0.0.1:5001/api/admin/evaluations")
            evals = res_eval.json().get("data", []) if res_eval.status_code == 200 else []
            self.eval_table.setRowCount(len(evals))
            for i, ev in enumerate(evals):
                self.eval_table.setItem(i, 0, QTableWidgetItem(str(ev['Evaluation_ID'])))
                self.eval_table.setItem(i, 1, QTableWidgetItem(ev.get('Student_Name', 'Unknown')))
                self.eval_table.setItem(i, 2, QTableWidgetItem(ev.get('Course_Code', 'Unknown')))
        except Exception as e:
            print("Error loading data:", e)