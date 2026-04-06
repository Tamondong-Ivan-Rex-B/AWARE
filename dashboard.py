import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class ProfessorDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.W.A.R.E. Professor Dashboard")
        self.resize(400, 200)

        # Set up the layout
        self.layout = QVBoxLayout()

        # Create UI Elements
        self.title_label = QLabel("Class Analytics Overview")
        self.data_label = QLabel("Click the button to load live data.")
        self.refresh_btn = QPushButton("Fetch Latest Analytics")

        # Connect the button to the function
        self.refresh_btn.clicked.connect(self.fetch_data)

        # Add elements to layout
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.refresh_btn)
        self.layout.addWidget(self.data_label)
        
        self.setLayout(self.layout)

    def fetch_data(self):
        try:
            # Ask the Flask API for the data
            response = requests.get("http://localhost:5000/get_analytics")
            data = response.json()
            
            # Extract the average score and update the UI label
            avg_score = data.get('average_clarity')
            
            if avg_score is not None:
                # Format it to 2 decimal places
                self.data_label.setText(f"Current Class Clarity Average: {float(avg_score):.2f} / 5.0")
            else:
                self.data_label.setText("No evaluations submitted yet.")
                
        except Exception as e:
            self.data_label.setText("Error connecting to server. Is Flask running?")

# Run the Application
app = QApplication(sys.argv)
window = ProfessorDashboard()
window.show()
sys.exit(app.exec())