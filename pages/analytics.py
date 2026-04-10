import requests
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QFrame, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor


class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analytics Dashboard")
        self.resize(1000, 700)
        self.setObjectName("Background")

        self.setStyleSheet("""
        #Background {
            background-color: white;
        }
        QLabel#Title {
            color: black;
            font-size: 20px;
            font-weight: bold;
        }
        QLabel#CardTitle {
            color: black;
            font-size: 14px;
        }
        QFrame#Card {
            background-color: #f9fafb;
            border-radius: 10px;
            padding: 10px;
        }
        """)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        title = QLabel("📊 Analytics Overview")
        title.setObjectName("Title")

        back_btn = QPushButton("← Back")
        back_btn.setObjectName("OutlineBtn")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.clicked.connect(self.close)

        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(back_btn)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)

        #  BAR GRAPH 
        bar_label = QLabel("Average Clarity per Course")
        bar_label.setObjectName("CardTitle")

        self.bar_graph = pg.PlotWidget()
        self.bar_graph.setBackground('w')
        self.bar_graph.setMinimumHeight(250)
        self.bar_graph.showGrid(x=False, y=True, alpha=0.2)
        self.bar_graph.setLabel('left', 'Clarity Score')
        self.bar_graph.setLabel('bottom', 'Courses')
        self.bar_graph.setYRange(0, 5)

        # FIX: axis color
        self.bar_graph.getAxis('left').setTextPen('black')
        self.bar_graph.getAxis('bottom').setTextPen('black')

        #  LINE GRAPH 
        line_label = QLabel("Engagement Trend Over Weeks")
        line_label.setObjectName("CardTitle")

        self.line_graph = pg.PlotWidget()
        self.line_graph.setBackground('w')
        self.line_graph.setMinimumHeight(250)
        self.line_graph.showGrid(x=False, y=True, alpha=0.2)
        self.line_graph.setLabel('left', 'Engagement Score')
        self.line_graph.setLabel('bottom', 'Weeks')
        self.line_graph.setYRange(0, 5)

        # FIX: axis color
        self.line_graph.getAxis('left').setTextPen('black')
        self.line_graph.getAxis('bottom').setTextPen('black')

        #  LAYOUT 
        card_layout.addWidget(bar_label)
        card_layout.addWidget(self.bar_graph)
        card_layout.addWidget(line_label)
        card_layout.addWidget(self.line_graph)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(card)

        #  DATA LOAD 
        self.load_data()

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(5000)

    def load_data(self):
        try:
            res = requests.get("http://127.0.0.1:5001/api/get_dashboard_data")

            if res.status_code != 200:
                print("Server error:", res.status_code)
                return

            data = res.json()
            evaluations = data.get("evaluations", []) or []

            # BAR GRAPH 
            self.bar_graph.clear()

            course_scores = {}

            for e in evaluations:
                course = e.get("Course_Code") or "Unknown"
                clarity = e.get("Clarity_Score", 0)

                if course not in course_scores:
                    course_scores[course] = []

                course_scores[course].append(clarity)

            if course_scores:
                courses = list(course_scores.keys())
                averages = [
                    sum(scores) / len(scores)
                    for scores in course_scores.values()
                ]

                x = list(range(len(courses)))

                bars = pg.BarGraphItem(
                    x=x,
                    height=averages,
                    width=0.6,
                    brush=pg.mkBrush("#2E86AB"),
                    pen=pg.mkPen("#1B4F72")  # smoother look
                )

                self.bar_graph.addItem(bars)
                self.bar_graph.getAxis('bottom').setTicks([list(zip(x, courses))])
            else:
                self.bar_graph.setTitle("No Data")

            #  LINE GRAPH 
            self.line_graph.clear()

            engagement = [
                e.get("Engagement_Score", 0)
                for e in evaluations
            ]

            if engagement:
                weeks = list(range(1, len(engagement) + 1))

                self.line_graph.plot(
                    weeks,
                    engagement,
                    pen=pg.mkPen(color="#F6C85F", width=4),
                    symbol='o',
                    symbolBrush="#F6C85F",
                )

                self.line_graph.getAxis('bottom').setTicks(
                    [list(zip(weeks, [f"W{w}" for w in weeks]))]
                )
            else:
                self.line_graph.setTitle("No Data")

        except Exception as e:
            print("Analytics Error:", e)