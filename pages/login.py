from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Background")
        self.main_window = main_window
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Header
        icon = QLabel("🎓")
        icon.setFont(QFont("Segoe UI", 36))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Welcome to EduEval")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Sign in to access your dashboard")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login Card
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(400)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        card_title = QLabel("Sign In")
        card_title.setObjectName("CardTitle")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("admin@tip.edu.ph")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("PrimaryBtn")
        login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # Tell main.py to switch to Index 2 (Dashboard)
        login_btn.clicked.connect(lambda: self.main_window.switch_page(2)) 
        
        demo_text = QLabel("<b>Demo Credentials:</b><br>Admin: admin@tip.edu.ph / admin123")
        demo_text.setObjectName("DemoBox") # Links it to the global stylesheet
        
        card_layout.addWidget(card_title)
        card_layout.addWidget(QLabel("Email"))
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(QLabel("Password"))
        card_layout.addWidget(self.pass_input)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(demo_text)
        
        back_btn = QPushButton("Back to Home")
        back_btn.setStyleSheet("color: #64748b; background: transparent; border: none; font-weight: bold;")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # Tell main.py to switch to Index 0 (Landing Page)
        back_btn.clicked.connect(lambda: self.main_window.switch_page(0)) 
        
        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def clear_inputs(self):
        self.email_input.clear()
        self.pass_input.clear()
        self.main_window.switch_page(1)