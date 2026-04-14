import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
from config import BASE_URL

# ==================
# API WORKER THREAD
# ==================
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
                timeout=15, # Gave it 15 seconds just in case Render is waking up!
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

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Header ---
        icon = QLabel("🎓")
        icon.setFont(QFont("Segoe UI", 36))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("A.W.A.R.E. Admin Portal")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sign in to access the professor dashboard")
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

        # Role Dropdown
        role_label = QLabel("Login As")
        self.role_input = QComboBox()
        self.role_input.addItems(["Professor", "Admin"])
        self.role_input.setStyleSheet("padding: 8px; border: 1px solid #e2e8f0; border-radius: 6px; background: #f8fafc;")

        # Username Input
        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. prof_rudo")

        # Password Input
        password_label = QLabel("Password")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.returnPressed.connect(self.handle_login)

        # Sign In button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("PrimaryBtn")
        self.login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_btn.clicked.connect(self.handle_login)

        # Demo credentials hint
        self.demo_text = QLabel(
            "<b>Demo (Admin):</b> admin / admin123<br>"
            "<b>Demo (Admin):</b> rsuberec / prof123<br>"
            "<b>Demo (Professor):</b> refer to database / prof123"
        )
        self.demo_text.setObjectName("DemoBox")
        self.demo_text.setTextFormat(Qt.TextFormat.RichText)

        card_layout.addWidget(card_title)
        card_layout.addWidget(role_label)
        card_layout.addWidget(self.role_input)
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.demo_text)

        # Back button
        back_btn = QPushButton("← Back to Home")
        back_btn.setStyleSheet(
            "color: #64748b; background: transparent; border: none; font-weight: bold;"
        )
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.clicked.connect(lambda: self.main_window.switch_page(0))

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_login(self):
        """Starts the background worker to handle the login request."""
        # Prevent double-clicking
        if self.worker is not None and self.worker.isRunning():
            return

        username = self.username_input.text().strip()
        password = self.pass_input.text().strip()
        role = self.role_input.currentText().lower()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        # Disable UI and show loading text
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
        """Re-enables the login button after the worker is done."""
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Sign In")

    def clear_inputs(self):
        """Wipes the text boxes clean when someone logs out."""
        self.username_input.clear()
        self.pass_input.clear()
        self.reset_login_btn()