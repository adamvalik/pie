import os
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QDialog, QColorDialog
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtGui import QFont, QFontDatabase


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")


        layout = QVBoxLayout()

        self.color1_label = QLabel("Color 1:")
        self.color1_edit = QLineEdit()
        self.color1_button = QPushButton("Select Color")
        self.color1_button.clicked.connect(self.select_color1)

        self.color2_label = QLabel("Color 2:")
        self.color2_edit = QLineEdit()
        self.color2_button = QPushButton("Select Color")
        self.color2_button.clicked.connect(self.select_color2)

        layout.addWidget(self.color1_label)
        layout.addWidget(self.color1_edit)
        layout.addWidget(self.color1_button)
        layout.addWidget(self.color2_label)
        layout.addWidget(self.color2_edit)
        layout.addWidget(self.color2_button)

        self.setLayout(layout)

    def select_color1(self):
        color_dialog = QColorDialog()
        color = color_dialog.getColor()
        if color.isValid():
            self.color1_edit.setText(color.name())

    def select_color2(self):
        color_dialog = QColorDialog()
        color = color_dialog.getColor()
        if color.isValid():
            self.color2_edit.setText(color.name())


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
        input1_label = QLabel("Total:")
        self.input1_edit = QLineEdit()

        input2_label = QLabel("Current:")
        self.input2_edit = QLineEdit()

        self.input1_edit.textEdited.connect(self.update_chart)
        self.input2_edit.textEdited.connect(self.update_chart)

        # Create settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)

        # Apply custom styles to the widgets
        self.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #FFFFFF;
            }
            QLineEdit {
                padding: 2px;
                font-size: 15px;
                border: 1px solid #FFFFFF;
                border-radius: 4px;
            }
            QPushButton {
                padding: 2px 8px;
                font-size: 15px;
                border: 1px solid #FFFFFF;
                border-radius: 4px;
                background-color: #286090;
                color: #FFFFFF;
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
        layout.addWidget(self.settings_button)
        layout.addWidget(self.canvas)

        self.setCentralWidget(main_widget)

        # Load and set the font
        font_path = os.path.join(os.path.dirname(__file__), "Montserrat-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)

        # Check if the font file was loaded successfully
        if font_id != -1 and font_families:
            font_family = font_families[0]

            # Set the font of the QLabel objects
            font = QFont(font_family)
            input1_label.setFont(font)
            input2_label.setFont(font)
            self.settings_button.setFont(font)


        # Default colors for the pie chart
        self.color1 = "#56CA3D"
        self.color2 = "#CA3D3D"

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.color1_edit.setText(self.color1)
        settings_window.color2_edit.setText(self.color2)
        if settings_window.exec_():
            self.color1 = settings_window.color1_edit.text()
            self.color2 = settings_window.color2_edit.text()
            self.update_chart()

    def update_chart(self):
        # Get the input values from the input fields
        input1 = float(self.input1_edit.text())
        input2 = float(self.input2_edit.text())

        # Perform calculations and generate data for the pie chart
        done = input2
        tbd = input1 - input2

        # Generate the data for the pie chart
        values = [done, tbd]

        # Clear the previous plot
        self.figure.clear()

        # Create the pie chart using Matplotlib
        ax = self.figure.add_subplot(111)
        ax.pie(values, colors=[self.color1, self.color2], autopct='%1.1f%%', wedgeprops={"linewidth": 1, "edgecolor": "white"})
        ax.axis('equal')

        # Update the canvas
        self.canvas.draw()
