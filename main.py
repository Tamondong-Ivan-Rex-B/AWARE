import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from pages.landing import LandingPage
from pages.login import LoginPage
from pages.dashboard import DashboardPage

# Demo Credentials:
# Student: student@university.edu / student123
# Admin: admin@university.edu / admin123

# ==========================================
# GLOBAL STYLE SHEET (QSS)
# ==========================================
STYLESHEET = """
    QMainWindow, QWidget#Background { background-color: #f8fafc; }
    
    QLabel { color: #0f172a; }
    QLabel#Title { font-size: 36px; font-weight: bold; }
    QLabel#Subtitle { font-size: 16px; color: #64748b; }
    QLabel#CardTitle { font-size: 16px; font-weight: bold; }
    
    QLabel#DemoBox {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 10px;
        border-radius: 6px;
        color: #0f172a;
    }
    
    QPushButton#PrimaryBtn {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton#PrimaryBtn:hover { background-color: #1e293b; }
    
    QPushButton#OutlineBtn {
        background-color: transparent;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton#OutlineBtn:hover { background-color: #f1f5f9; }
    
    QLineEdit {
        background-color: #f8fafc;
        color: #0f172a;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
    }
    QLineEdit:focus { border: 1px solid #6d28d9; }
    
    QFrame#Card {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    QFrame#KPIBox {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }

    /* --- GLOBAL TABLE STYLES --- */
    QTableWidget { 
        background-color: white; 
        color: #0f172a; 
        gridline-color: #e2e8f0; 
        font-size: 13px;
        border: none;
    }
    QTableWidget::item {
        color: #0f172a; 
    }
    QHeaderView::section { 
        background-color: #f1f5f9; 
        color: #0f172a; 
        font-weight: bold; 
        border: 1px solid #e2e8f0;
        padding: 4px;
    }
    QTableCornerButton::section {
        background-color: #f1f5f9;
    }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.W.A.R.E. Desktop Application")
        self.resize(1200, 800)
        self.setStyleSheet(STYLESHEET)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.landing_page = LandingPage(self)
        self.login_page = LoginPage(self)
        self.dashboard_page = DashboardPage(self)

        self.stacked_widget.addWidget(self.landing_page)  # Index 0
        self.stacked_widget.addWidget(self.login_page)  # Index 1
        self.stacked_widget.addWidget(self.dashboard_page)  # Index 2

    def switch_page(self, index, data=None):
        """Fixed: Now accepts 'data' so login doesn't crash the app"""
        if index == 2 and data:
            # if the DashboardPage has an update_user_info method, call it
            if hasattr(self.dashboard_page, "update_user_info"):
                self.dashboard_page.update_user_info(data)

        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
