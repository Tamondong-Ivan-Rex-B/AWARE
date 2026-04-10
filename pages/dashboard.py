import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor


class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Background")
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # ---------------- FILTERS ----------------
        self.course_filter = QComboBox()
        self.course_filter.addItems(["All Courses", "CPE111", "CPE112", "CPE113"])

        self.professor_filter = QComboBox()
        self.professor_filter.addItems(["All Professors", "Prof. Santos", "Prof. Reyes"])

        self.student_filter = QComboBox()
        self.student_filter.addItems(["All Students", "Juan Dela Cruz", "Maria Clara"])

        self.evaluation_filter = QComboBox()
        self.evaluation_filter.addItems(["All Evaluations", "Low Scores", "High Scores", "Needs Improvement"])

        # Connect filters
        self.course_filter.currentIndexChanged.connect(self.apply_filters)
        self.professor_filter.currentIndexChanged.connect(self.apply_filters)
        self.student_filter.currentIndexChanged.connect(self.apply_filters)
        self.evaluation_filter.currentIndexChanged.connect(self.apply_filters)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.course_filter)
        filter_layout.addWidget(self.professor_filter)
        filter_layout.addWidget(self.student_filter)
        filter_layout.addWidget(self.evaluation_filter)

        # ---------------- NAVBAR ----------------
        nav_layout = QHBoxLayout()

        title = QLabel("<b>🎓 Admin Dashboard</b><br><span style='font-size:12px; color:gray;'>A.W.A.R.E. System Live Data</span>")
        title.setFont(QFont("Segoe UI", 16))

        refresh_btn = QPushButton("↻ Refresh Data")
        refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_btn.clicked.connect(self.fetch_live_data)

        analytics_btn = QPushButton("Analytics")
        analytics_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        analytics_btn.clicked.connect(self.open_analytics)

        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_btn.clicked.connect(self.handle_logout)

        nav_layout.addWidget(title)
        nav_layout.addStretch()
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(analytics_btn)
        nav_layout.addWidget(logout_btn)

        # ---------------- KPI ----------------
        kpi_layout = QHBoxLayout()

        self.val_pacing, box_pacing = self.create_kpi("Avg Pacing", "0.0", "#f59e0b")
        self.val_comp, box_comp = self.create_kpi("Avg Understanding", "0.0", "#3b82f6")

        kpi_layout.addWidget(box_pacing)
        kpi_layout.addWidget(box_comp)

        # ---------------- TABLE ----------------
        table_container = QFrame()
        table_layout = QVBoxLayout(table_container)

        table_title = QLabel("<b>Recent Student Evaluations</b>")

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Course", "Topics", "Clarity", "Pacing", "Understanding", "Engagement", "Hours", "Comments"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table_layout.addWidget(table_title)
        table_layout.addWidget(self.table)

        # ---------------- MAIN LAYOUT ----------------
        layout.addLayout(filter_layout)
        layout.addLayout(nav_layout)
        layout.addSpacing(20)
        layout.addLayout(kpi_layout)
        layout.addSpacing(20)
        layout.addWidget(table_container)

    # ---------------- FILTER ----------------
    def apply_filters(self):
        course = self.course_filter.currentText()
        professor = self.professor_filter.currentText()
        student = self.student_filter.currentText()
        evaluation = self.evaluation_filter.currentText()

        response = requests.get("http://127.0.0.1:5000/get_data", params={
            "course": course,
            "professor": professor,
            "student": student,
            "evaluation": evaluation
        })

        if response.status_code == 200:
            data = response.json()
            self.update_table(data)

    def update_table(self, data):
        self.table.setRowCount(len(data))
        if len(data) > 0:
            self.table.setColumnCount(len(data[0]))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # ---------------- KPI ----------------
    def create_kpi(self, title, default_value, color):
        box = QFrame()
        box.setFixedHeight(100)
        box_layout = QVBoxLayout(box)

        t_label = QLabel(title)
        t_label.setStyleSheet("color: #64748b; font-size: 13px;")

        v_label = QLabel(default_value)
        v_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        v_label.setStyleSheet(f"color: {color};")

        box_layout.addWidget(t_label)
        box_layout.addWidget(v_label)

        return v_label, box

    # ---------------- DATA ----------------
    def fetch_live_data(self):
        try:
            response = requests.get("http://127.0.0.1:5001/api/get_dashboard_data")

            if response.status_code != 200:
                QMessageBox.warning(self, "Server Error", "Server returned an error.")
                return

            data = response.json()

            avgs = data.get("averages", {})
            if avgs and avgs.get("avg_pacing") is not None:
                self.val_pacing.setText(f"{float(avgs['avg_pacing']):.1f}")
                self.val_comp.setText(f"{float(avgs['avg_comp']):.1f}")
            else:
                self.val_pacing.setText("N/A")
                self.val_comp.setText("N/A")

            evaluations = data.get("evaluations", [])
            self.table.setRowCount(len(evaluations))

            for row_idx, eval_data in enumerate(evaluations):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(eval_data.get("Course_Code", ""))))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(eval_data.get("Topic", ""))))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(eval_data.get("Clarity_Score", ""))))
                self.table.setItem(row_idx, 3, QTableWidgetItem(str(eval_data.get("Pacing_Score", ""))))
                self.table.setItem(row_idx, 4, QTableWidgetItem(str(eval_data.get("Comprehension_Score", ""))))
                self.table.setItem(row_idx, 5, QTableWidgetItem(str(eval_data.get("Engagement_Score", ""))))

                hours = eval_data.get("Study_Hours")
                self.table.setItem(row_idx, 6, QTableWidgetItem(str(hours if hours else 0)))

                comments = eval_data.get("Comments")
                self.table.setItem(row_idx, 7, QTableWidgetItem(str(comments if comments else "")))

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", "Cannot connect to server.")

    # ---------------- NAVIGATION ----------------
    def handle_logout(self):
        self.main_window.login_page.clear_inputs()
        self.main_window.switch_page(0)

    def open_analytics(self):
        from pages.analytics import AnalyticsWindow
        self.analytics_window = AnalyticsWindow()
        self.analytics_window.show()
