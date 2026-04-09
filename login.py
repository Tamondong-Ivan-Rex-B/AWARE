import requests
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFrame,
    QMessageBox,
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

        # --- UI Header ---
        title = QLabel("Sign In")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Login Card ---
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)

        card_title = QLabel("Welcome Back")
        card_title.setObjectName("CardTitle")
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("admin@tip.edu.ph")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("PrimaryBtn")
        login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_btn.clicked.connect(self.handle_login)

        # Helper text for testing (matches our server dictionary)
        demo_info = QLabel("Demo: admin@tip.edu.ph / admin123")
        demo_info.setStyleSheet("color: #64748b; font-size: 11px;")
        demo_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(card_title)
        card_layout.addWidget(QLabel("Email"))
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(QLabel("Password"))
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(demo_info)

        # Navigation Button
        back_btn = QPushButton("Back to Home")
        back_btn.setStyleSheet(
            "color: #64748b; background: transparent; border: none; font-weight: bold;"
        )
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.clicked.connect(lambda: self.main_window.switch_page(0))

        layout.addWidget(title)
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.pass_input.text().strip()

        # 1. Basic Local Validation
        if not email or not password:
            QMessageBox.warning(
                self, "Input Error", "Please enter both email and password."
            )
            return

        try:
            # 2. POST request to Port 5001 (Corrected to avoid 404 ghost servers)
            response = requests.post(
                "http://127.0.0.1:5001/login",
                json={"email": email, "password": password},
                timeout=5,
            )

            # 3. Handle the Response
            if response.status_code == 200:
                user_data = response.json()
                # Switch to Dashboard (Index 2) and pass the user info
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
                "Could not connect to the server. Make sure server.py is running on port 5001.",
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"An unexpected error occurred: {str(e)}"
            )

    def clear_inputs(self):
        """Clears the fields when switching pages (called by main.py)"""
        self.email_input.clear()
        self.pass_input.clear()
