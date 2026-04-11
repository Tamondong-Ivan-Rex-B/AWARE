import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from pages.landing import LandingPage
from pages.login import LoginPage
from pages.dashboard import DashboardPage

# ==========================================
# GLOBAL STYLE SHEET (QSS)
# ==========================================
STYLESHEET = """
    QMainWindow, QWidget#Background { background-color: #f8fafc; }
    
    QLabel { color: #5071c1; }
    QLabel#Title { font-size: 36px; font-weight: bold; }
    QLabel#Subtitle { font-size: 16px; color: #64748b; }
    QLabel#CardTitle { font-size: 16px; font-weight: bold; }
    
    QLabel#DemoBox {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 10px;
        border-radius: 6px;
        color: #5071c1;
    }
    
    QPushButton#PrimaryBtn {
        background-color: #5071c1;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton#PrimaryBtn:hover { background-color: #1e293b; }
    
    QPushButton#OutlineBtn {
        background-color: transparent;
        color: #5071c1;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton#OutlineBtn:hover { background-color: #f1f5f9; }
    
    QLineEdit {
        background-color: #f8fafc;
        color: #5071c1;
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

    /* --- DROPDOWN STYLES --- */
    QComboBox {
        background-color: white;
        color: #5071c1;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 13px;
        min-width: 150px;
    }
    QComboBox:hover { border: 1px solid #94a3b8; }
    QComboBox QAbstractItemView {
        background-color: white;
        color: #5071c1;
        selection-background-color: #f1f5f9;
        selection-color: #5071c1;
        border: 1px solid #cbd5e1;
    }

    /* --- GLOBAL TABLE STYLES --- */
    QTableWidget { 
        background-color: white; 
        color: #5071c1; 
        gridline-color: #e2e8f0; 
        font-size: 13px;
        border: none;
    }
    QHeaderView::section { 
        background-color: #f1f5f9; 
        color: #5071c1; 
        font-weight: bold; 
        border: 1px solid #e2e8f0;
        padding: 4px;
    }
    
    /* --- ANALYTICS SPECIFIC --- */
    PlotWidget {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
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

        self.stacked_widget.addWidget(self.landing_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.dashboard_page)

    def switch_page(self, index, data=None):
        if index == 2 and data:
            if hasattr(self.dashboard_page, "update_user_info"):
                self.dashboard_page.update_user_info(data)
        self.stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())