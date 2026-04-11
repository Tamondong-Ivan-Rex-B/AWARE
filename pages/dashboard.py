import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Background")
        self.main_window = main_window
        
        # Master data storage for cascading filters
        self.all_evaluations = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- 1. Navbar (Integrated with Analytics Button) ---
        nav_layout = QHBoxLayout()
        title = QLabel("<b>🎓 Admin Dashboard</b><br><span style='font-size:12px; color:gray;'>A.W.A.R.E. System Live Data</span>")
        title.setFont(QFont("Segoe UI", 16))
        
        refresh_btn = QPushButton("↻ Refresh Data")
        refresh_btn.setObjectName("PrimaryBtn")
        refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_btn.clicked.connect(self.fetch_live_data)
        
        # NEW: Analytics Button
        analytics_btn = QPushButton("📊 Analytics")
        analytics_btn.setObjectName("OutlineBtn")
        analytics_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        analytics_btn.clicked.connect(self.open_analytics)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("OutlineBtn")
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_btn.clicked.connect(self.handle_logout)
        
        nav_layout.addWidget(title)
        nav_layout.addStretch()
        nav_layout.addWidget(refresh_btn)
        nav_layout.addWidget(analytics_btn)
      
        
        # --- 2. KPI ROW ---
        kpi_layout = QHBoxLayout()
        self.val_pacing, box_pacing = self.create_kpi("Avg Pacing", "0.0", "#f59e0b")
        self.val_comp, box_comp = self.create_kpi("Avg Understanding", "0.0", "#3b82f6")
        kpi_layout.addWidget(box_pacing)
        kpi_layout.addWidget(box_comp)
        
        # --- 3. Cascading Filters (Preserved Filtering System) ---
        filter_layout = QHBoxLayout()
        
        self.filter_mode = QComboBox()
        self.filter_mode.setFixedWidth(140)
        self.filter_mode.addItems(["By Course", "By Professor"])
        
        self.primary_target = QComboBox()
        self.primary_target.setFixedWidth(160)
        self.primary_target.addItem("All Courses")
        
        self.topic_filter = QComboBox()
        self.topic_filter.setFixedWidth(160)
        self.topic_filter.addItem("All Topics")
        
        self.score_filter = QComboBox()
        self.score_filter.addItems(["All Scores", "High Understanding (4-5)", "Low Understanding (1-2)"])
        
        # Connect Cascading Logic
        self.filter_mode.currentIndexChanged.connect(self.on_mode_changed)
        self.primary_target.currentIndexChanged.connect(self.on_target_changed) 
        self.topic_filter.currentIndexChanged.connect(self.apply_filters)
        self.score_filter.currentIndexChanged.connect(self.apply_filters)
        
        filter_layout.addWidget(QLabel("<b>Filter:</b>"))
        filter_layout.addWidget(self.filter_mode)
        filter_layout.addWidget(QLabel("<b>></b>"))
        filter_layout.addWidget(self.primary_target)
        filter_layout.addWidget(QLabel("<b>></b>"))
        filter_layout.addWidget(self.topic_filter)
        filter_layout.addWidget(QLabel("<b>></b>"))
        self.score_filter.setFixedWidth(150)
        filter_layout.addWidget(self.score_filter)

        # Save Table Button with dropdown menu
        save_btn = QPushButton("Save Table")
        save_btn.setObjectName("OutlineBtn")
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        menu = QMenu()

        csv_action = menu.addAction("Save as CSV")
        pdf_action = menu.addAction("Save as PDF")

        csv_action.triggered.connect(self.export_csv)
        pdf_action.triggered.connect(self.export_pdf)

        save_btn.setMenu(menu)

        filter_layout.addWidget(save_btn)
        filter_layout.addStretch()
        # --- 4. TABLE VIEW ---
        table_container = QFrame()
        table_container.setObjectName("Card")
        table_layout = QVBoxLayout(table_container)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8) 
        self.table.setHorizontalHeaderLabels([
            "Course", "Topic", "Clarity", "Pacing", "Understanding", "Engagement", "Hours", "Comments"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        table_layout.addWidget(QLabel("<b>Evaluation Data</b>"))
        table_layout.addWidget(self.table)
        
        # Assembly
        layout.addLayout(nav_layout)
        layout.addSpacing(20)
        layout.addLayout(kpi_layout)
        layout.addSpacing(10)
        layout.addLayout(filter_layout)
        layout.addWidget(table_container)

    def create_kpi(self, title, default_value, color):
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
        """Pulls data from the Flask API on port 5001"""
        try:
            response = requests.get("http://127.0.0.1:5001/api/get_dashboard_data")
            if response.status_code != 200:
                QMessageBox.warning(self, "Server Error", "Server returned an error.")
                return
                
            data = response.json()
            avgs = data.get("averages", {})
            self.val_pacing.setText(f"{float(avgs.get('avg_pacing', 0)):.1f}")
            self.val_comp.setText(f"{float(avgs.get('avg_comp', 0)):.1f}")

            self.all_evaluations = data.get("evaluations", [])
            self.on_mode_changed() 
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not connect: {e}")

    def on_mode_changed(self):
        self.primary_target.blockSignals(True)
        mode = self.filter_mode.currentText()
        self.primary_target.clear()
        
        unique_targets = set()
        for ev in self.all_evaluations:
            if mode == "By Course":
                unique_targets.add(ev.get("Course_Code", ""))
            elif mode == "By Professor":
                unique_targets.add(ev.get("Professor_Name", ""))

        self.primary_target.addItem("All Courses" if mode == "By Course" else "All Professors")
        self.primary_target.addItems(sorted(list(unique_targets)))
        self.primary_target.blockSignals(False)
        self.on_target_changed() 

    def on_target_changed(self):
        self.topic_filter.blockSignals(True)
        mode = self.filter_mode.currentText()
        target = self.primary_target.currentText()
        self.topic_filter.clear()
        self.topic_filter.addItem("All Topics")
        
        unique_topics = set()
        for ev in self.all_evaluations:
            if target in ["All Courses", "All Professors"]:
                unique_topics.add(ev.get("Topic", ""))
            elif mode == "By Course" and ev.get("Course_Code") == target:
                unique_topics.add(ev.get("Topic", ""))
            elif mode == "By Professor" and ev.get("Professor_Name") == target:
                unique_topics.add(ev.get("Topic", ""))
                
        self.topic_filter.addItems(sorted(list(unique_topics)))
        self.topic_filter.blockSignals(False)
        self.apply_filters()

    def apply_filters(self):
        mode = self.filter_mode.currentText()
        target = self.primary_target.currentText()
        topic = self.topic_filter.currentText()
        score_mode = self.score_filter.currentText()
        
        filtered = []
        for ev in self.all_evaluations:
            if mode == "By Course" and target != "All Courses" and ev.get("Course_Code") != target: continue
            if mode == "By Professor" and target != "All Professors" and ev.get("Professor_Name") != target: continue
            if topic != "All Topics" and ev.get("Topic") != topic: continue
            
            comp = int(ev.get("Comprehension_Score", 0))
            if score_mode == "High Understanding (4-5)" and comp < 4: continue
            if score_mode == "Low Understanding (1-2)" and comp > 2: continue
            filtered.append(ev)
            
        self.update_table(filtered)

    def update_table(self, data):
        self.table.setRowCount(len(data))
        for row, ev in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(ev.get("Course_Code", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(ev.get("Topic", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(ev.get("Clarity_Score", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(ev.get("Pacing_Score", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(ev.get("Comprehension_Score", ""))))
            self.table.setItem(row, 5, QTableWidgetItem(str(ev.get("Engagement_Score", ""))))
            self.table.setItem(row, 6, QTableWidgetItem(str(ev.get("Study_Hours", 0))))
            self.table.setItem(row, 7, QTableWidgetItem(str(ev.get("Comments", ""))))

    def open_analytics(self):
        """Opens the separate analytics window"""
        try:
            # FIX: Added 'pages.' to the import path
            from pages.analytics import AnalyticsWindow 
            self.analytics_window = AnalyticsWindow()
            self.analytics_window.show()
        except ImportError:
            QMessageBox.critical(self, "File Error", "Could not find pages/analytics.py. Please check your folder structure.")
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"An unexpected error occurred: {e}")

    def handle_logout(self):
        self.table.setRowCount(0)
        self.main_window.login_page.clear_inputs()
        self.main_window.switch_page(0)

    
    # Export CSV Function
    def export_csv(self):
        import csv
        from PyQt6.QtWidgets import QFileDialog

        # Open save dialog
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "report.csv", "CSV Files (*.csv)")
        if not path:
            return

        # Write table data to CSV
        with open(path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Get table headers
            headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
            writer.writerow(headers)

            # Get table rows
            for row in range(self.table.rowCount()):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

    # Export PDF Function
    def export_pdf(self):
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        from PyQt6.QtWidgets import QFileDialog

        # Open save dialog
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "report.pdf", "PDF Files (*.pdf)")
        if not path:
            return

        # Prepare document
        doc = SimpleDocTemplate(path)

        data = []

        # Get table headers
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
        data.append(headers)

        # Get table rows
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # Create table
        table = Table(data)

        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))

        # Build PDF
        doc.build([table])