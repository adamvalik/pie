import matplotlib.pyplot as plt
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PIE")
        self.setMinimumSize(300, 200)
        self.setMaximumSize(600, 400)

        # Set the window flags to keep the window on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint)    

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        input_layout = QHBoxLayout()

        # Create input fields
        input1_label = QLabel("total: ")
        self.input1_edit = QLineEdit()

        input2_label = QLabel("current: ")
        self.input2_edit = QLineEdit()

        self.input1_edit.textEdited.connect(self.update_chart)
        self.input2_edit.textEdited.connect(self.update_chart)

         # Apply custom styles to the widgets
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #FFFFFF;
            }
            QLineEdit {
                padding: 8px;
                font-size: 16px;
                border: 2px solid #CCCCCC;
                border-radius: 5px;
            }
            QPushButton {
                padding: 8px;
                font-size: 16px;
                background-color: #009688;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00796B;
            }
        """)

        # Create a canvas for the matplotlib chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Add widgets to the layout
        input_layout.addWidget(input1_label)
        input_layout.addWidget(self.input1_edit)
        input_layout.addWidget(input2_label)
        input_layout.addWidget(self.input2_edit)

        layout.addLayout(input_layout)
        layout.addWidget(self.canvas)

        self.setCentralWidget(main_widget)

    def update_chart(self):
        # Get the input values from the input fields
        input1 = float(self.input1_edit.text())
        input2 = float(self.input2_edit.text())

        # Perform calculations and generate data for the pie chart
        done = input2
        tbd = input1 - input2

        # Generate the data for the pie chart
        labels = ['done', 'tbd']
        values = [done, tbd]

        # Clear the previous plot
        self.figure.clear()

        # Create the pie chart using Matplotlib
        ax = self.figure.add_subplot(111)
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.axis('equal')

        # Update the canvas
        self.canvas.draw()
