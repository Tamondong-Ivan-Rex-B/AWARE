import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QMessageBox, QComboBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor


class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Background")
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Header ---
        icon = QLabel("🎓")
        icon.setFont(QFont("Segoe UI", 36))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Welcome to A.W.A.R.E.")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sign in to access your dashboard")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Login Card ---
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(12)

        card_title = QLabel("Sign In")
        card_title.setObjectName("CardTitle")

        # Role selector
        role_label = QLabel("Login As")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Student", "Professor"])
        self.role_combo.setStyleSheet("""
            QComboBox {
                background-color: #f8fafc;
                color: #0f172a;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 14px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #0f172a;
                selection-background-color: #e0e7ff;
            }
        """)
        self.role_combo.currentTextChanged.connect(self.on_role_changed)

        # Username
        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g. miguel2024")

        # Password
        password_label = QLabel("Password")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.returnPressed.connect(self.handle_login)

        # Sign In button
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("PrimaryBtn")
        login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_btn.clicked.connect(self.handle_login)

        # Demo credentials hint
        self.demo_text = QLabel(
            "<b>Demo (Student):</b> miguel2024 / student123<br>"
            "<b>Demo (Student):</b> sofia2024 / student123"
        )
        self.demo_text.setObjectName("DemoBox")
        self.demo_text.setTextFormat(Qt.TextFormat.RichText)

        card_layout.addWidget(card_title)
        card_layout.addWidget(role_label)
        card_layout.addWidget(self.role_combo)
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(login_btn)
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

    def on_role_changed(self, role_text):
        """Update the demo hint when the role dropdown changes."""
        if role_text == "Professor":
            self.demo_text.setText(
                "<b>Demo (Professor):</b> prof_rudo / prof123<br>"
                "<b>Demo (Professor):</b> prof_ada / prof123"
            )
            self.username_input.setPlaceholderText("e.g. prof_rudo")
        else:
            self.demo_text.setText(
                "<b>Demo (Student):</b> miguel2024 / student123<br>"
                "<b>Demo (Student):</b> sofia2024 / student123"
            )
            self.username_input.setPlaceholderText("e.g. miguel2024")

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.pass_input.text().strip()
        role = self.role_combo.currentText().lower()  # "student" or "professor"

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5001/login",
                json={"username": username, "password": password, "role": role},
                timeout=5,
            )

            if response.status_code == 200:
                user_data = response.json()
                self.main_window.switch_page(2, user_data)

            elif response.status_code == 401:
                QMessageBox.warning(
                    self,
                    "Login Failed",
                    "Incorrect username or password. Please try again.",
                )
            else:
                error_msg = response.json().get("message", "Unknown server error.")
                QMessageBox.critical(
                    self, "Server Error", f"Error {response.status_code}: {error_msg}"
                )

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self,
                "Connection Error",
                "Could not connect to the server.\nMake sure server.py is running on port 5001.",
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")

    def clear_inputs(self):
        """Called by main.py on logout."""
        self.username_input.clear()
        self.pass_input.clear()
        self.role_combo.setCurrentIndex(0)
