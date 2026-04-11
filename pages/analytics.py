import requests
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QFrame, QPushButton, QHBoxLayout, QTabWidget, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A.W.A.R.E. Analytics")
        self.resize(1000, 700)
        self.setObjectName("Background")

        self.all_evaluations = []
        self.all_grade_data = []

        self.setStyleSheet("""
        #Background { background-color: white; }
        QLabel#Title { color: black; font-size: 20px; font-weight: bold; }
        QLabel#CardTitle { color: black; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        
        QComboBox {
            background-color: white;
            color: #0f172a;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 13px;
            min-width: 150px;
        }
        QComboBox:hover { border: 1px solid #94a3b8; }
        QComboBox QAbstractItemView {
            background-color: white;
            color: #0f172a;
            selection-background-color: #f1f5f9;
            selection-color: #0f172a;
            border: 1px solid #cbd5e1;
        }
        
        QTabWidget::pane { border: 1px solid #e2e8f0; background: white; border-radius: 8px; }
        
        QTabBar::tab {
            background: #f1f5f9; color: #64748b; padding: 10px 15px; 
            border: 1px solid #e2e8f0; border-bottom-color: #e2e8f0;
            border-top-left-radius: 8px; border-top-right-radius: 8px;
            font-weight: bold; margin-right: 2px; font-size: 12px;
        }
        QTabBar::tab:selected { background: #6D28D9; color: white; border-color: #6D28D9; }
        QTabBar::tab:hover:!selected { background: #e2e8f0; }
        """)

        main_layout = QVBoxLayout(self)

        # --- TOP NAVIGATION ---
        top_layout = QHBoxLayout()
        title = QLabel("📊 Advanced Diagnostics")
        title.setObjectName("Title")

        # NEW: Global Course Filter
        self.course_filter = QComboBox()
        self.course_filter.addItem("All Courses")
        ##
        self.course_filter.setFixedWidth(150)
        self.course_filter.currentIndexChanged.connect(self.update_plots)

        # NEW: Legend / Help Button
        help_btn = QPushButton("ℹ️ Legend / Help")
        help_btn.setStyleSheet("background: #e0f7fa; border: 1px solid #b2ebf2; padding: 5px 15px; border-radius: 5px; color: #00838f; font-weight: bold;")
        help_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        help_btn.clicked.connect(self.show_help)

        back_btn = QPushButton("← Back")
        back_btn.setObjectName("OutlineBtn")
        back_btn.setStyleSheet("background: transparent; border: 1px solid #e2e8f0; padding: 5px 15px; border-radius: 5px; color: black; font-weight: bold;")
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.clicked.connect(self.close)

        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(QLabel("<b>Filter:</b>"))
        top_layout.addWidget(self.course_filter)
        top_layout.addWidget(help_btn)
        top_layout.addWidget(back_btn)

        self.tabs = QTabWidget()

        # ==========================================
        # TAB 1: STUDENT OUTCOMES
        # ==========================================
        tab_outcomes = QWidget()
        layout_outcomes = QVBoxLayout(tab_outcomes)
        layout_outcomes.addWidget(QLabel("<b>Student Outcomes:</b> Comprehension vs. Actual Grade", objectName="CardTitle"))
        self.scatter_graph = pg.PlotWidget(background='w')
        self.scatter_graph.showGrid(x=True, y=True, alpha=0.3)
        self.scatter_graph.setLabel('left', 'Current Grade (%)')
        self.scatter_graph.setLabel('bottom', 'Self-Reported Comprehension (1-5)')
        self.scatter_graph.setLimits(xMin=0, yMin=0, xMax=6, yMax=105)
        self.scatter_graph.getAxis('left').setTextPen('black')
        self.scatter_graph.getAxis('bottom').setTextPen('black')
        layout_outcomes.addWidget(self.scatter_graph)
        self.tabs.addTab(tab_outcomes, "Outcomes")

        # ==========================================
        # TAB 2: BURNOUT DETECTOR
        # ==========================================
        tab_burnout = QWidget()
        layout_burnout = QVBoxLayout(tab_burnout)
        layout_burnout.addWidget(QLabel("<b>Burnout Detector:</b> Study Hours vs. Comprehension", objectName="CardTitle"))
        self.burnout_graph = pg.PlotWidget(background='w')
        self.burnout_graph.showGrid(x=True, y=True, alpha=0.3)
        self.burnout_graph.setLabel('left', 'Comprehension Score (1-5)')
        self.burnout_graph.setLabel('bottom', 'Study Hours This Week')
        self.burnout_graph.setLimits(xMin=0, yMin=0, yMax=5.5)
        self.burnout_graph.getAxis('left').setTextPen('black')
        self.burnout_graph.getAxis('bottom').setTextPen('black')
        layout_burnout.addWidget(self.burnout_graph)
        self.tabs.addTab(tab_burnout, "Burnout Detector")

        # ==========================================
        # TAB 3: SYLLABUS BOTTLENECK
        # ==========================================
        tab_bottleneck = QWidget()
        layout_bottleneck = QVBoxLayout(tab_bottleneck)
        layout_bottleneck.addWidget(QLabel("<b>Syllabus Bottleneck:</b> Clarity & Comprehension by Week", objectName="CardTitle"))
        self.bottleneck_graph = pg.PlotWidget(background='w')
        self.bottleneck_graph.showGrid(x=False, y=True, alpha=0.3)
        self.bottleneck_graph.setLabel('left', 'Average Score (1-5)')
        self.bottleneck_graph.setLabel('bottom', 'Academic Week')
        self.bottleneck_graph.setLimits(yMin=0, yMax=5.5)
        self.bottleneck_graph.getAxis('left').setTextPen('black')
        self.bottleneck_graph.getAxis('bottom').setTextPen('black')
        layout_bottleneck.addWidget(self.bottleneck_graph)
        self.tabs.addTab(tab_bottleneck, "Syllabus Bottleneck")

        # ==========================================
        # TAB 4: PACING SWEET SPOT
        # ==========================================
        tab_pacing = QWidget()
        layout_pacing = QVBoxLayout(tab_pacing)
        layout_pacing.addWidget(QLabel("<b>Pacing Sweet Spot:</b> How Course Speed Affects Engagement", objectName="CardTitle"))
        self.pacing_graph = pg.PlotWidget(background='w')
        self.pacing_graph.showGrid(x=False, y=True, alpha=0.3)
        self.pacing_graph.setLabel('left', 'Average Engagement Score')
        self.pacing_graph.setLabel('bottom', 'Pacing Rating (1=Too Slow, 3=Perfect, 5=Too Fast)')
        self.pacing_graph.setLimits(xMin=0, xMax=6, yMin=0, yMax=5.5)
        self.pacing_graph.getAxis('left').setTextPen('black')
        self.pacing_graph.getAxis('bottom').setTextPen('black')
        layout_pacing.addWidget(self.pacing_graph)
        self.tabs.addTab(tab_pacing, "Pacing Sweet Spot")

        # ==========================================
        # TAB 5: ENGAGEMENT TRENDS
        # ==========================================
        tab_engagement = QWidget()
        layout_engagement = QVBoxLayout(tab_engagement)
        layout_engagement.addWidget(QLabel("<b>Engagement:</b> Trend Over Recent Submissions", objectName="CardTitle"))
        self.line_graph = pg.PlotWidget(background='w')
        self.line_graph.showGrid(x=False, y=True, alpha=0.2)
        self.line_graph.setLimits(yMin=0, yMax=5.5)
        self.line_graph.getAxis('left').setTextPen('black')
        self.line_graph.getAxis('bottom').setTextPen('black')
        layout_engagement.addWidget(self.line_graph)
        self.tabs.addTab(tab_engagement, "Engagement")

        # ==========================================
        # TAB 6: CLARITY OVERVIEW
        # ==========================================
        tab_clarity = QWidget()
        layout_clarity = QVBoxLayout(tab_clarity)
        layout_clarity.addWidget(QLabel("<b>Clarity Overview:</b> Average Clarity Ratings", objectName="CardTitle"))
        self.bar_graph = pg.PlotWidget(background='w')
        self.bar_graph.showGrid(x=False, y=True, alpha=0.2)
        self.bar_graph.setLimits(yMin=0, yMax=5.5)
        self.bar_graph.getAxis('left').setTextPen('black')
        self.bar_graph.getAxis('bottom').setTextPen('black')
        layout_clarity.addWidget(self.bar_graph)
        self.tabs.addTab(tab_clarity, "Clarity")

        # --- ASSEMBLE ---
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tabs)

        self.fetch_data()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_data)
        self.timer.start(10000) # Increased to 10s to prevent stuttering

    def show_help(self):
        """Displays instructions based on the currently active tab."""
        current_tab_name = self.tabs.tabText(self.tabs.currentIndex())
        
        instructions = {
            "Outcomes": "<b>How to read this chart:</b><br><br>"
                        "• <b>Top-Right:</b> All Good (High grade, high understanding).<br>"
                        "• <b>Bottom-Left:</b> Needs Tutoring (Low grade, low understanding).<br>"
                        "• <b>Top-Left:</b> Imposter Syndrome (High grade, but feels lost. Needs reassurance).<br>"
                        "• <b>Bottom-Right:</b> Overconfident (Failing, but thinks they understand it. Needs an intervention).",
            
            "Burnout Detector": "<b>How to read this chart:</b><br><br>"
                                "This spots students using ineffective study methods.<br><br>"
                                "• Look at the <b>Bottom-Right quadrant</b> (High hours, low score).<br>"
                                "• These students are working extremely hard but still failing to understand the material. They are at the highest risk of burnout.",
            
            "Syllabus Bottleneck": "<b>How to read this chart:</b><br><br>"
                                   "• <b>Blue Line:</b> How clearly the Professor explained it.<br>"
                                   "• <b>Orange Line:</b> How well the Students understood it.<br><br>"
                                   "Look for sudden drops in the lines. If both lines drop in Week 5, that specific topic was too difficult and needs a review session.",
            
            "Pacing Sweet Spot": "<b>How to read this chart:</b><br><br>"
                                 "This proves how your lecture speed affects student attention.<br><br>"
                                 "You are looking for an inverted 'U' shape. Ideally, the highest engagement should happen when pacing is a 3 (Perfect).",
            
            "Engagement": "<b>How to read this chart:</b><br><br>"
                          "A simple chronological line showing the class's focus. If the line trends downward over several weeks, you may need to introduce more interactive activities.",
            
            "Clarity": "<b>How to read this chart:</b><br><br>"
                       "Displays average clarity. The bars are color-coded:<br>"
                       "• <b>Green:</b> Excellent (4-5)<br>"
                       "• <b>Yellow/Orange:</b> Average (2-3)<br>"
                       "• <b>Red:</b> Poor (Needs immediate review)"
        }

        msg = QMessageBox(self)
        msg.setWindowTitle(f"Legend: {current_tab_name}")
        msg.setText(instructions.get(current_tab_name, "No instructions available for this tab."))
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def fetch_data(self):
        """Fetches data from the API and populates the filter dropdown."""
        try:
            res = requests.get("http://127.0.0.1:5001/api/get_dashboard_data", timeout=5)
            if res.status_code == 200:
                self.all_evaluations = res.json().get("evaluations", [])
                
                # Update Course Filter options
                current_selection = self.course_filter.currentText()
                unique_courses = set([e.get("Course_Code") for e in self.all_evaluations if e.get("Course_Code")])
                
                self.course_filter.blockSignals(True)
                self.course_filter.clear()
                self.course_filter.addItem("All Courses")
                self.course_filter.addItems(sorted(list(unique_courses)))
                
                # Restore previous selection if it still exists
                idx = self.course_filter.findText(current_selection)
                if idx >= 0: self.course_filter.setCurrentIndex(idx)
                self.course_filter.blockSignals(False)

            res_grades = requests.get("http://127.0.0.1:5001/api/analytics/grades_vs_evals", timeout=5)
            if res_grades.status_code == 200:
                self.all_grade_data = res_grades.json().get("data", [])

            self.update_plots()

        except Exception as e:
            print("Analytics Fetch Error:", e)

    def update_plots(self):
        """Filters the data and redraws all 6 graphs."""
        selected_course = self.course_filter.currentText()
        
        # Apply Filters
        filtered_evals = self.all_evaluations
        filtered_grades = self.all_grade_data
        
        if selected_course != "All Courses":
            filtered_evals = [e for e in self.all_evaluations if e.get("Course_Code") == selected_course]
            filtered_grades = [g for g in self.all_grade_data if g.get("Course_Code") == selected_course]

        # ---------------------------------------------------------
        # 1. OUTCOMES (Scatter: Grades vs Comprehension)
        # ---------------------------------------------------------
        self.scatter_graph.clear()
        x_comp, y_grade = [], []
        for row in filtered_grades:
            if row.get("Current_Grade") is not None and row.get("Avg_Comprehension") is not None:
                x_comp.append(float(row["Avg_Comprehension"]))
                y_grade.append(float(row["Current_Grade"]))

        if x_comp and y_grade:
            scatter = pg.ScatterPlotItem(x=x_comp, y=y_grade, size=12, pen=pg.mkPen(None), brush=pg.mkBrush("#6D28D9"))
            self.scatter_graph.addItem(scatter)
            self.scatter_graph.addItem(pg.InfiniteLine(pos=3, angle=90, pen=pg.mkPen('gray', style=Qt.PenStyle.DashLine)))
            self.scatter_graph.addItem(pg.InfiniteLine(pos=75, angle=0, pen=pg.mkPen('gray', style=Qt.PenStyle.DashLine)))

        # ---------------------------------------------------------
        # 2. BURNOUT DETECTOR (Scatter: Hours vs Comprehension)
        # ---------------------------------------------------------
        self.burnout_graph.clear()
        b_hours, b_comp = [], []
        total_hours = 0
        for e in filtered_evals:
            try:
                h = float(e.get("Study_Hours") or 0)
                c = float(e.get("Comprehension_Score") or 0)
                if c > 0:
                    b_hours.append(h)
                    b_comp.append(c)
                    total_hours += h
            except: pass

        if b_hours:
            avg_hours = total_hours / len(b_hours)
            scatter_burnout = pg.ScatterPlotItem(x=b_hours, y=b_comp, size=14, pen=pg.mkPen('black'), brush=pg.mkBrush("#EF4444"))
            self.burnout_graph.addItem(scatter_burnout)
            self.burnout_graph.addItem(pg.InfiniteLine(pos=avg_hours, angle=90, pen=pg.mkPen('blue', style=Qt.PenStyle.DashLine, width=2)))

        # ---------------------------------------------------------
        # 3. SYLLABUS BOTTLENECK (Line: Clarity & Comp by Week)
        # ---------------------------------------------------------
        self.bottleneck_graph.clear()
        week_data = {}
        for e in filtered_evals:
            w = e.get("Week_Number", 0)
            if w > 0:
                if w not in week_data: week_data[w] = {'clarity': [], 'comp': []}
                week_data[w]['clarity'].append(float(e.get("Clarity_Score", 0)))
                week_data[w]['comp'].append(float(e.get("Comprehension_Score", 0)))

        if week_data:
            sorted_weeks = sorted(list(week_data.keys()))
            avg_clarity = [sum(week_data[w]['clarity'])/len(week_data[w]['clarity']) for w in sorted_weeks]
            avg_comp = [sum(week_data[w]['comp'])/len(week_data[w]['comp']) for w in sorted_weeks]

            self.bottleneck_graph.plot(sorted_weeks, avg_clarity, pen=pg.mkPen(color="#3B82F6", width=4), symbol='o', symbolBrush="#3B82F6", name="Clarity")
            self.bottleneck_graph.plot(sorted_weeks, avg_comp, pen=pg.mkPen(color="#F97316", width=4), symbol='s', symbolBrush="#F97316", name="Comprehension")
            self.bottleneck_graph.getAxis('bottom').setTicks([list(zip(sorted_weeks, [f"Wk {w}" for w in sorted_weeks]))])

        # ---------------------------------------------------------
        # 4. PACING SWEET SPOT (Bar: Pacing Score vs Avg Engagement)
        # ---------------------------------------------------------
        self.pacing_graph.clear()
        pacing_groups = {1: [], 2: [], 3: [], 4: [], 5: []}
        for e in filtered_evals:
            p = int(e.get("Pacing_Score", 0))
            eng = float(e.get("Engagement_Score", 0))
            if p in pacing_groups and eng > 0: pacing_groups[p].append(eng)

        p_x, p_heights, p_brushes = [], [], []
        for p_score in range(1, 6):
            p_x.append(p_score)
            p_heights.append(sum(pacing_groups[p_score]) / len(pacing_groups[p_score]) if pacing_groups[p_score] else 0)
            if p_score == 3: p_brushes.append(pg.mkBrush("#22C55E"))
            elif p_score in [2, 4]: p_brushes.append(pg.mkBrush("#FBBF24"))
            else: p_brushes.append(pg.mkBrush("#EF4444"))

        pacing_bars = pg.BarGraphItem(x=p_x, height=p_heights, width=0.6, brushes=p_brushes, pen=pg.mkPen("black"))
        self.pacing_graph.addItem(pacing_bars)
        self.pacing_graph.getAxis('bottom').setTicks([[(1, "1(Slow)"), (2, "2"), (3, "3(Perfect)"), (4, "4"), (5, "5(Fast)")]])

        # ---------------------------------------------------------
        # 5. ENGAGEMENT TRENDS (Line)
        # ---------------------------------------------------------
        self.line_graph.clear()
        chronological_evals = list(reversed(filtered_evals))
        engagement = [e.get("Engagement_Score", 0) for e in chronological_evals]
        if engagement:
            entries = list(range(1, len(engagement) + 1))
            self.line_graph.plot(entries, engagement, pen=pg.mkPen(color="#F6C85F", width=4), symbol='o', symbolBrush="#F6C85F")
            self.line_graph.getAxis('bottom').setTicks([list(zip(entries, [f"Wk {i}" for i in entries]))])

        # ---------------------------------------------------------
        # 6. CLARITY OVERVIEW (Bar)
        # ---------------------------------------------------------
        self.bar_graph.clear()
        course_scores = {}
        for e in filtered_evals:
            course = e.get("Course_Code") or "Unknown"
            if course not in course_scores: course_scores[course] = []
            course_scores[course].append(float(e.get("Clarity_Score", 0)))
        
        if course_scores:
            courses = list(course_scores.keys())
            averages = [sum(scores)/len(scores) for scores in course_scores.values()]
            x = list(range(len(courses)))
            
            bar_brushes = []
            for score in averages:
                if score < 2: bar_brushes.append(pg.mkBrush("#EF4444"))
                elif score < 3: bar_brushes.append(pg.mkBrush("#F97316"))
                elif score < 4: bar_brushes.append(pg.mkBrush("#FBBF24"))
                elif score < 4.5: bar_brushes.append(pg.mkBrush("#84CC16"))
                else: bar_brushes.append(pg.mkBrush("#22C55E"))

            bars = pg.BarGraphItem(x=x, height=averages, width=0.6, brushes=bar_brushes, pen=pg.mkPen("black"))
            self.bar_graph.addItem(bars)
            self.bar_graph.getAxis('bottom').setTicks([list(zip(x, courses))])