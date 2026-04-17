import os
import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QMessageBox, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QCursor, QPixmap
from config import BASE_URL

# ==========================================
# API WORKER THREAD
# ==========================================
class LoginWorker(QThread):
    finished_success = pyqtSignal(dict)
    finished_auth_error = pyqtSignal(str)
    finished_server_error = pyqtSignal(str)

    def __init__(self, username, password, role):
        super().__init__()
        self.username = username
        self.password = password
        self.role = role

    def run(self):
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"username": self.username, "password": self.password, "role": self.role},
                timeout=15, 
            )
            if response.status_code == 200:
                self.finished_success.emit(response.json())
            elif response.status_code == 401:
                self.finished_auth_error.emit("Incorrect username or password. Please try again.")
            else:
                error_msg = response.json().get("message", "Unknown server error.")
                self.finished_server_error.emit(f"Error {response.status_code}: {error_msg}")
        except requests.exceptions.ConnectionError:
            self.finished_server_error.emit("Could not connect to the server.\nMake sure server.py is running.")
        except Exception as e:
            self.finished_server_error.emit(f"An unexpected error occurred:\n{str(e)}")

# ==========================================
# MAIN LOGIN PAGE
# ==========================================
class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Background")
        self.main_window = main_window
        self.worker = None

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        logo_path = os.path.join(parent_dir, "static", "images", "AWARE-icon.jpg")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel()
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            icon.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon.setStyleSheet("border: 2px solid navy; background-color: white;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Welcome to A.W.A.R.E.")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sign in to access the portal")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Login Card ---
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(12)

        card_title = QLabel("System Sign In")
        card_title.setObjectName("CardTitle")

        role_label = QLabel("Login As")
        self.role_input = QComboBox()
        self.role_input.addItems(["Professor", "Admin"])
        self.role_input.setStyleSheet("padding: 8px; border: 1px solid #e2e8f0; border-radius: 6px; background: #f8fafc;")

        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. prof_rudo")

        password_label = QLabel("Password")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.returnPressed.connect(self.handle_login)

        self.show_pass_cb = QCheckBox("Show Password")
        self.show_pass_cb.setStyleSheet("color: #64748b; font-size: 12px;")
        self.show_pass_cb.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.show_pass_cb.toggled.connect(self.toggle_password_visibility)

        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("PrimaryBtn")
        self.login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_btn.clicked.connect(self.handle_login)

        card_layout.addWidget(card_title)
        card_layout.addWidget(role_label)
        card_layout.addWidget(self.role_input)
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(self.show_pass_cb) 
        card_layout.addWidget(self.login_btn)

        back_btn = QPushButton("← Back to Home")
        back_btn.setStyleSheet("color: #64748b; background: transparent; border: none; font-weight: bold;")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.clicked.connect(lambda: self.main_window.switch_page(0))

        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def toggle_password_visibility(self, checked):
        if checked:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_login(self):
        if self.worker is not None and self.worker.isRunning(): return
        username = self.username_input.text().strip()
        password = self.pass_input.text().strip()
        role = self.role_input.currentText().lower()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        self.login_btn.setEnabled(False)
        self.login_btn.setText("Authenticating...")

        self.worker = LoginWorker(username, password, role)
        self.worker.finished_success.connect(self.on_login_success)
        self.worker.finished_auth_error.connect(self.on_auth_error)
        self.worker.finished_server_error.connect(self.on_server_error)
        self.worker.start()

    def on_login_success(self, user_data):
        self.reset_login_btn()
        self.main_window.switch_page(2, user_data)

    def on_auth_error(self, error_msg):
        self.reset_login_btn()
        QMessageBox.warning(self, "Login Failed", error_msg)

    def on_server_error(self, error_msg):
        self.reset_login_btn()
        QMessageBox.critical(self, "Server Error", error_msg)

    def reset_login_btn(self):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In")

    def clear_inputs(self):
        self.username_input.clear()
        self.pass_input.clear()
        self.show_pass_cb.setChecked(False) 
        self.reset_login_btn()