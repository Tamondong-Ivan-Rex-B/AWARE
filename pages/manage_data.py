import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
    QMessageBox, QTabWidget, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class ManageDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚙️ A.W.A.R.E. Data Management")
        self.resize(850, 500)
        
        self.setStyleSheet("""
        QWidget { background-color: white; }
        QLabel { color: #0f172a; font-size: 13px; }
        
        /* Input Fields */
        QLineEdit { 
            padding: 8px; 
            border: 1px solid #cbd5e1; 
            border-radius: 6px; 
            background: #f8fafc; 
            color: #0f172a; /* THIS FIXES BOTH TYPING AND PLACEHOLDER COLOR */
        }
        QLineEdit:focus { border: 1px solid #6D28D9; background: white; }
        
        /* Table Styling */
        QTableWidget { 
            border: 1px solid #e2e8f0; 
            border-radius: 6px; 
            gridline-color: #e2e8f0; 
            color: #5071c1; /* Your custom blue color for the text */
            background-color: white;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #f8fafc; /* Light gray background when clicked */
            color: #6D28D9; /* Turns purple when selected to match the Save button */
            font-weight: bold;
        }
        QHeaderView::section { 
            background-color: #f8fafc; 
            padding: 10px; 
            border: none; 
            border-bottom: 2px solid #e2e8f0; 
            font-weight: bold; 
            color: #5071c1; /* Makes the Header text blue as well */
        }
        
        /* Tab Styling (Matches Analytics) */
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
        
        # --- TOP NAV ---
        top_layout = QHBoxLayout()
        title = QLabel("<b>⚙️ Manage System Data</b>")
        title.setStyleSheet("font-size: 18px;")
        back_btn = QPushButton("Close")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #0f172a; border: 1px solid #cbd5e1; padding: 6px 15px; border-radius: 6px; font-weight: bold; }
            QPushButton:hover { background-color: #f1f5f9; border: 1px solid #94a3b8; }
        """)
        back_btn.clicked.connect(self.close)
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(back_btn)
        
        # --- TABS ---
        self.tabs = QTabWidget()
        
        # === PROFESSORS TAB ===
        prof_tab = QWidget()
        prof_layout = QHBoxLayout(prof_tab)
        
        # Left Side: The Form (C and U)
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Professor Details</b>"))
        
        self.prof_id_hidden = None # Stores ID when updating
        
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight) # Aligns the labels neatly
        form_layout.setSpacing(15)
        
        self.in_first = QLineEdit()
        self.in_first.setPlaceholderText("First Name, e.g. Juan")
        self.in_last = QLineEdit()
        self.in_last.setPlaceholderText("Last Name, e.g. Dela Cruz")
        self.in_user = QLineEdit()
        self.in_user.setPlaceholderText("Username, e.g. jdelacruz")
        self.in_pass = QLineEdit()
        self.in_pass.setPlaceholderText("Password (Leave blank to keep current)")
        self.in_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("<b>First Name:</b>", self.in_first)
        form_layout.addRow("<b>Last Name:</b>", self.in_last)
        form_layout.addRow("<b>Username:</b>", self.in_user)
        form_layout.addRow("<b>Password:</b>", self.in_pass)
        
        left_panel.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save / Add")
        self.btn_save.setStyleSheet("background: #6D28D9; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.btn_save.clicked.connect(self.save_professor)
        
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setStyleSheet("background: #EF4444; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.btn_delete.clicked.connect(self.delete_professor)
        
        self.btn_clear = QPushButton("Clear Form")
        self.btn_clear.clicked.connect(self.clear_form)
        
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_delete)
        
        left_panel.addLayout(btn_layout)
        left_panel.addWidget(self.btn_clear)
        left_panel.addStretch()
        
        # Right Side: The Table (R)
        self.prof_table = QTableWidget(0, 4)
        self.prof_table.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Username"])
        self.prof_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prof_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.prof_table.itemSelectionChanged.connect(self.populate_form_from_table)
        
        prof_layout.addLayout(left_panel, 1) # 1 part width
        prof_layout.addWidget(self.prof_table, 2) # 2 parts width
        
        self.tabs.addTab(prof_tab, "Professors")
        
        # Build UI
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tabs)
        
        self.load_professors()

    # --- CRUD LOGIC ---

    def clear_form(self):
        self.prof_id_hidden = None
        self.in_first.clear()
        self.in_last.clear()
        self.in_user.clear()
        self.in_pass.clear()
        self.prof_table.clearSelection()

    def load_professors(self):
        self.clear_form()
        try:
            res = requests.get("http://127.0.0.1:5001/api/admin/professors")
            if res.status_code == 200:
                data = res.json().get("data", [])
                self.prof_table.setRowCount(len(data))
                for row_idx, prof in enumerate(data):
                    self.prof_table.setItem(row_idx, 0, QTableWidgetItem(str(prof['Professor_ID'])))
                    self.prof_table.setItem(row_idx, 1, QTableWidgetItem(prof['First_Name']))
                    self.prof_table.setItem(row_idx, 2, QTableWidgetItem(prof['Last_Name']))
                    self.prof_table.setItem(row_idx, 3, QTableWidgetItem(prof['Username']))
        except Exception as e:
            print("Error loading professors:", e)

    def populate_form_from_table(self):
        selected = self.prof_table.selectedItems()
        if selected:
            self.prof_id_hidden = int(selected[0].text())
            self.in_first.setText(selected[1].text())
            self.in_last.setText(selected[2].text())
            self.in_user.setText(selected[3].text())
            self.in_pass.clear() # Never show the hashed password

    def save_professor(self):
        payload = {
            "First_Name": self.in_first.text(),
            "Last_Name": self.in_last.text(),
            "Username": self.in_user.text(),
            "Password": self.in_pass.text()
        }
        
        # If no ID is hidden, it's a NEW professor (CREATE)
        if self.prof_id_hidden is None:
            if not payload['Password']:
                QMessageBox.warning(self, "Error", "New professors must have a password!")
                return
            res = requests.post("http://127.0.0.1:5001/api/admin/professors", json=payload)
            
        # If an ID is hidden, we are UPDATING an existing one (UPDATE)
        else:
            res = requests.put(f"http://127.0.0.1:5001/api/admin/professors/{self.prof_id_hidden}", json=payload)

        if res.status_code in [200, 201]:
            self.load_professors()
        else:
            QMessageBox.warning(self, "Database Error", res.json().get("message", "Unknown error"))

    def delete_professor(self):
        if self.prof_id_hidden:
            confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this professor?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                res = requests.delete(f"http://127.0.0.1:5001/api/admin/professors/{self.prof_id_hidden}")
                if res.status_code == 200:
                    self.load_professors()
                else:
                    QMessageBox.warning(self, "Error", "Cannot delete. They might be assigned to active classes.")