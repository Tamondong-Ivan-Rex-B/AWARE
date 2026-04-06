import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QStackedWidget, QScrollArea, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor, QColor, QPainter
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis

# ==========================================
# GLOBAL STYLE SHEET (QSS)
# Maps your web CSS into desktop UI styling
# ==========================================
STYLESHEET = """
    QMainWindow { background-color: #f8fafc; }
    
    QLabel { color: #0f172a; }
    QLabel#Title { font-size: 36px; font-weight: bold; }
    QLabel#Subtitle { font-size: 16px; color: #64748b; }
    QLabel#CardTitle { font-size: 16px; font-weight: bold; }
    
    /* Primary Button Styling */
    QPushButton#PrimaryBtn {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton#PrimaryBtn:hover { background-color: #1e293b; }
    
    /* Outline / Secondary Button */
    QPushButton#OutlineBtn {
        background-color: transparent;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton#OutlineBtn:hover { background-color: #f1f5f9; }
    
    /* Input Fields */
    QLineEdit {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
    }
    QLineEdit:focus { border: 1px solid #6d28d9; }
    
    /* Cards */
    QFrame#Card {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    /* KPI Boxes */
    QFrame#KPIBox {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
"""

# ==========================================
# PAGE 1: LANDING PAGE
# ==========================================
class LandingPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Navbar ---
        navbar = QFrame()
        navbar.setStyleSheet("background-color: white; border-bottom: 1px solid #e2e8f0;")
        nav_layout = QHBoxLayout(navbar)
        
        # Use <br> instead of \n, and format the whole string as HTML
        logo = QLabel("<b>🎓 A.W.A.R.E.</b><br><span style='font-size:10px; color:gray;'>Anonymous Weekly Academic Review & Evaluation</span>")
        logo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("PrimaryBtn")
        login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_btn.clicked.connect(lambda: self.main_window.switch_page(1)) # Go to Login
        
        nav_layout.addWidget(logo)
        nav_layout.addStretch()
        nav_layout.addWidget(login_btn)
        
        # --- Hero Section ---
        hero_widget = QWidget()
        hero_layout = QVBoxLayout(hero_widget)
        hero_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_layout.setSpacing(20)
        
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
        hero_layout.addWidget(pill, alignment=Qt.AlignmentFlag.AlignCenter)
        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        hero_layout.addWidget(get_started_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        hero_layout.addStretch()
        
        layout.addWidget(navbar)
        layout.addWidget(hero_widget)

# ==========================================
# PAGE 2: ADMIN LOGIN
# ==========================================
class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
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
        card.setFixedSize(400, 350)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        card_title = QLabel("Sign In")
        card_title.setObjectName("CardTitle")
        
        email_input = QLineEdit()
        email_input.setPlaceholderText("admin@tip.edu.ph")
        
        pass_input = QLineEdit()
        pass_input.setPlaceholderText("Enter your password")
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("PrimaryBtn")
        login_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        login_btn.clicked.connect(lambda: self.main_window.switch_page(2)) # Go to Dashboard
        
        demo_text = QLabel("<b>Demo Credentials:</b><br>Admin: admin@tip.edu.ph / admin123")
        demo_text.setStyleSheet("background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; color: #64748b;")
        
        card_layout.addWidget(card_title)
        card_layout.addWidget(QLabel("Email"))
        card_layout.addWidget(email_input)
        card_layout.addWidget(QLabel("Password"))
        card_layout.addWidget(pass_input)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(demo_text)
        
        back_btn = QPushButton("Back to Home")
        back_btn.setStyleSheet("color: #64748b; background: transparent; border: none; font-weight: bold;")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.clicked.connect(lambda: self.main_window.switch_page(0)) # Go to Landing
        
        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

# ==========================================
# PAGE 3: DASHBOARD
# ==========================================
class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Navbar ---
        nav_layout = QHBoxLayout()
        title = QLabel("<b>🎓 A.W.A.R.E.</b><br><span style='font-size:10px; color:gray;'>Anonymous Weekly Academic Review & Evaluation</span>")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("OutlineBtn")
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_btn.clicked.connect(lambda: self.main_window.switch_page(0))
        
        nav_layout.addWidget(title)
        nav_layout.addStretch()
        nav_layout.addWidget(logout_btn)
        
        # --- KPI ROW ---
        kpi_layout = QHBoxLayout()
        kpi_layout.addWidget(self.create_kpi("Total Pulse Checks", "9", "#3b82f6"))
        kpi_layout.addWidget(self.create_kpi("This Week (Week 2)", "3", "#10b981"))
        kpi_layout.addWidget(self.create_kpi("Active Courses", "5", "#6d28d9"))
        kpi_layout.addWidget(self.create_kpi("Discrepancies Found", "0", "#f59e0b"))
        
        # --- CHARTS ROW ---
        charts_layout = QHBoxLayout()
        
        # Chart 1: Pacing vs Understanding
        chart1_frame = QFrame()
        chart1_frame.setObjectName("Card")
        c1_layout = QVBoxLayout(chart1_frame)
        c1_layout.addWidget(QLabel("<b>Pacing vs Understanding Trends</b><br><span style='color:gray;'>CS 101: Data Structures - Weekly progression</span>"))
        
        chart_view_1 = self.create_line_chart(
            series_data={"Pacing": ([1, 2, 3], [3.3, 4.0, 2.9], "#f59e0b"), 
                         "Understanding": ([1, 2, 3], [4.0, 3.0, 4.0], "#3b82f6")}
        )
        c1_layout.addWidget(chart_view_1)
        
        insight1 = QLabel("<b>Insight:</b> Pacing increased in Week 2, correlating with a drop in understanding.")
        insight1.setStyleSheet("background-color: #fef3c7; color: #92400e; padding: 10px; border-radius: 6px;")
        c1_layout.addWidget(insight1)
        
        # Chart 2: Well-being & Engagement
        chart2_frame = QFrame()
        chart2_frame.setObjectName("Card")
        c2_layout = QVBoxLayout(chart2_frame)
        c2_layout.addWidget(QLabel("<b>Student Well-being & Engagement</b><br><span style='color:gray;'>Tracking mental state and course engagement</span>"))
        
        chart_view_2 = self.create_line_chart(
            series_data={"Well-being": ([1, 2, 3], [4.0, 3.0, 4.0], "#10b981"),
                         "Engagement": ([1, 2, 3], [4.7, 4.0, 5.0], "#8b5cf6"),
                         "Workload": ([1, 2, 3], [3.3, 4.0, 3.0], "#ef4444")}
        )
        c2_layout.addWidget(chart_view_2)
        
        insight2 = QLabel("<b>Positive:</b> Well-being recovered in Week 3 after workload adjustment.")
        insight2.setStyleSheet("background-color: #d1fae5; color: #065f46; padding: 10px; border-radius: 6px;")
        c2_layout.addWidget(insight2)
        
        charts_layout.addWidget(chart1_frame)
        charts_layout.addWidget(chart2_frame)
        
        # Add everything to main layout
        layout.addLayout(nav_layout)
        layout.addSpacing(20)
        layout.addLayout(kpi_layout)
        layout.addSpacing(20)
        layout.addLayout(charts_layout)

    def create_kpi(self, title, value, color):
        box = QFrame()
        box.setObjectName("KPIBox")
        box.setFixedHeight(100)
        box_layout = QVBoxLayout(box)
        
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #64748b; font-size: 13px;")
        v_label = QLabel(value)
        v_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        
        box_layout.addWidget(t_label)
        box_layout.addWidget(v_label)
        return box

    def create_line_chart(self, series_data):
        chart = QChart()
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # Set up Y Axis (1 to 5 scale)
        axis_y = QValueAxis()
        axis_y.setRange(1, 5)
        axis_y.setTickCount(5)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        
        # Set up X Axis (Weeks)
        axis_x = QValueAxis()
        axis_x.setRange(1, 3)
        axis_x.setTickCount(3)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        
        for name, data in series_data.items():
            x_vals, y_vals, color_hex = data
            series = QLineSeries()
            series.setName(name)
            
            # Add data points
            for i in range(len(x_vals)):
                series.append(x_vals[i], y_vals[i])
                
            pen = series.pen()
            pen.setWidth(2)
            pen.setColor(QColor(color_hex))
            series.setPen(pen)
            
            chart.addSeries(series)
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background: transparent;")
        return chart_view

# ==========================================
# MAIN APPLICATION CONTROLLER
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.W.A.R.E. Desktop Application")
        self.resize(1200, 800)
        self.setStyleSheet(STYLESHEET)
        
        # The Stacked Widget holds all our pages like a deck of cards
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize Pages
        self.landing_page = LandingPage(self)
        self.login_page = LoginPage(self)
        self.dashboard_page = DashboardPage(self)
        
        # Add pages to the stack
        self.stacked_widget.addWidget(self.landing_page)  # Index 0
        self.stacked_widget.addWidget(self.login_page)    # Index 1
        self.stacked_widget.addWidget(self.dashboard_page)# Index 2

    def switch_page(self, index):
        """Helper function to switch views smoothly"""
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())