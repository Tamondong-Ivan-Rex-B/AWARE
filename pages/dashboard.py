import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Background")
        self.main_window = main_window
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Navbar ---
        nav_layout = QHBoxLayout()
        title = QLabel("<b>🎓 Admin Dashboard</b><br><span style='font-size:12px; color:gray;'>A.W.A.R.E. System Live Data</span>")
        title.setFont(QFont("Segoe UI", 16))
        
        refresh_btn = QPushButton("↻ Refresh Data")
        refresh_btn.setObjectName("PrimaryBtn")
        refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_btn.clicked.connect(self.fetch_live_data)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("OutlineBtn")
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # Tell main.py to switch to Index 0 (Landing Page)
        logout_btn.clicked.connect(self.handle_logout)
        
        nav_layout.addWidget(title)
        nav_layout.addStretch()
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(logout_btn)
        
        # --- KPI ROW (Averages) ---
        kpi_layout = QHBoxLayout()
        
        self.val_pacing, box_pacing = self.create_kpi("Avg Pacing", "0.0", "#f59e0b")
        self.val_comp, box_comp = self.create_kpi("Avg Understanding", "0.0", "#3b82f6")
        #self.val_workload, box_workload = self.create_kpi("Avg Workload", "0.0", "#ef4444")
        
        kpi_layout.addWidget(box_pacing)
        kpi_layout.addWidget(box_comp)
        #kpi_layout.addWidget(box_workload)
        
        # --- TABLE VIEW (Raw Evaluations) ---
        table_container = QFrame()
        table_container.setObjectName("Card")
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
        
        # Add everything to main layout
        layout.addLayout(nav_layout)
        layout.addSpacing(20)
        layout.addLayout(kpi_layout)
        layout.addSpacing(20)
        layout.addWidget(table_container)

    def create_kpi(self, title, default_value, color):
        """Creates a KPI box and returns both the value label and the box itself."""
        box = QFrame()
        box.setObjectName("KPIBox")
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

    def fetch_live_data(self):
        """Pulls data from the Flask API and populates the UI."""
        try:
            # FIX 1: Updated the port to 5001 to match server.py
            response = requests.get("http://127.0.0.1:5001/api/get_dashboard_data")
            
            if response.status_code != 200:
                QMessageBox.warning(self, "Server Error", "Server returned an error.")
                return
                
            data = response.json()
            
            # Update Averages
            avgs = data.get("averages", {})
            if avgs and avgs.get("avg_pacing") is not None:
                self.val_pacing.setText(f"{float(avgs['avg_pacing']):.1f}")
                self.val_comp.setText(f"{float(avgs['avg_comp']):.1f}")
            else:
                self.val_pacing.setText("N/A")
                self.val_comp.setText("N/A")

            # --- Update Table ---
            evaluations = data.get("evaluations", [])
            self.table.setRowCount(len(evaluations))
            
            for row_idx, eval_data in enumerate(evaluations):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(eval_data.get("Course_Code", ""))))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(eval_data.get("Topic", ""))))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(eval_data.get("Clarity_Score", ""))))
                self.table.setItem(row_idx, 3, QTableWidgetItem(str(eval_data.get("Pacing_Score", ""))))
                self.table.setItem(row_idx, 4, QTableWidgetItem(str(eval_data.get("Comprehension_Score", ""))))
                self.table.setItem(row_idx, 5, QTableWidgetItem(str(eval_data.get("Engagement_Score", ""))))
                
                # FIX 2: Handle empty values gracefully so it doesn't print "None"
                hours = eval_data.get("Study_Hours")
                hours_str = str(hours) if hours is not None else "0"
                self.table.setItem(row_idx, 6, QTableWidgetItem(hours_str)) 
                
                comments = eval_data.get("Comments")
                comments_str = str(comments) if comments is not None else ""
                self.table.setItem(row_idx, 7, QTableWidgetItem(comments_str))
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", "Cannot connect to the Flask server. Is server.py running on port 5001?")

    def handle_logout(self):
        """Wipes the login credentials and sends the user to the landing page."""
        self.main_window.login_page.clear_inputs()
        self.main_window.switch_page(0)