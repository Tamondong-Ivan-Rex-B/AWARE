import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor, QPixmap
from config import BASE_URL

class LandingPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Background") 
        self.main_window = main_window   
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        logo_path = os.path.join(parent_dir, "static", "images", "AWARE-icon.jpg")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Navbar ---
        navbar = QFrame()
        navbar.setStyleSheet("background-color: white; border-bottom: 1px solid #e2e8f0;")
        nav_layout = QHBoxLayout(navbar)
        
        logo = QLabel("<b>🎓 A.W.A.R.E.</b><br><span style='font-size:10px; color:gray;'>Anonymous Weekly Academic Review & Evaluation</span>")
        logo.setFont(QFont("Segoe UI", 14))
        
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("PrimaryBtn")
        login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_btn.clicked.connect(lambda: self.main_window.switch_page(1)) 
        
        exit_btn = QPushButton("Exit")
        exit_btn.setObjectName("OutlineBtn")
        exit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        exit_btn.clicked.connect(self.main_window.close)
        
        nav_layout.addWidget(logo)
        nav_layout.addStretch()
        nav_layout.addWidget(exit_btn)
        
        hero_widget = QWidget()
        hero_layout = QVBoxLayout(hero_widget)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.setSpacing(20)
        
        main_logo = QLabel()
        pixmap = QPixmap(logo_path)
        if not pixmap.isNull():
            main_logo.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        main_logo.setStyleSheet("border: 2px solid navy; background-color: white;")
        main_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pill = QLabel("Weekly Pulse Checks • Real-time Insights")
        pill.setStyleSheet("background-color: #e0e7ff; color: #6d28d9; padding: 5px 15px; border-radius: 15px; font-weight: bold;")
        pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Transform Education Through\nWeekly Anonymous Feedback")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("The A.W.A.R.E. system bridges quantitative grades, qualitative well-being, and study\nhabits through quick weekly pulse checks.")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        get_started_btn = QPushButton("Get Started")
        get_started_btn.setObjectName("PrimaryBtn")
        get_started_btn.setFixedWidth(150)
        get_started_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        get_started_btn.clicked.connect(lambda: self.main_window.switch_page(1))
        
        hero_layout.addStretch()
        hero_layout.addWidget(main_logo, alignment=Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(pill, alignment=Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        hero_layout.addWidget(get_started_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        hero_layout.addStretch()
        
        layout.addWidget(navbar)
        layout.addWidget(hero_widget)