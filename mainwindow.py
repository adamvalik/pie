import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QDialog, QColorDialog, QCheckBox, QSlider
from PySide6.QtCore import Qt, Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtGui import QFont, QFontDatabase


class SettingsWindow(QDialog):
    save_clicked = Signal(str, str, bool, int)
    mode_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setMinimumSize(350, 200)
        self.setMaximumSize(350, 200)

        layout = QVBoxLayout()
        color1_layout = QHBoxLayout()
        color2_layout = QHBoxLayout()
        checkbox_layout = QHBoxLayout()
        slider_layout = QHBoxLayout()
        side_layout = QHBoxLayout()

        self.color1_label = QLabel("Done:")
        self.color1_edit = QLineEdit()
        self.color1_button = QPushButton("Select Color")
        self.color1_button.clicked.connect(self.select_color1)

        self.color2_label = QLabel("TBD: ")
        self.color2_edit = QLineEdit()
        self.color2_button = QPushButton("Select Color")
        self.color2_button.clicked.connect(self.select_color2)

        self.checkbox_label = QLabel("Show percentage:")
        self.show_percentage = QCheckBox()

        self.light_label = QLabel("Light")
        self.dark_label = QLabel("Dark")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.save_button = QPushButton("Save settings")
        self.save_button.clicked.connect(self.save_settings)


        # Load and set the font
        font_path = os.path.join(os.path.dirname(__file__), "Montserrat-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)

        # Check if the font file was loaded successfully
        if font_id != -1 and font_families:
            font_family = font_families[0]

            font = QFont(font_family)
            self.color1_label.setFont(font)
            self.color1_edit.setFont(font)
            self.color1_button.setFont(font)
            self.color2_label.setFont(font)
            self.color2_edit.setFont(font)
            self.color2_button.setFont(font)
            self.save_button.setFont(font)
            self.checkbox_label.setFont(font)
            self.light_label.setFont(font)
            self.dark_label.setFont(font)        


        color1_layout.addWidget(self.color1_label)
        color1_layout.addWidget(self.color1_edit)
        color1_layout.addWidget(self.color1_button)
        color2_layout.addWidget(self.color2_label)
        color2_layout.addWidget(self.color2_edit)
        color2_layout.addWidget(self.color2_button)
        checkbox_layout.addWidget(self.checkbox_label)
        checkbox_layout.addWidget(self.show_percentage)
        slider_layout.addWidget(self.light_label)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.dark_label)
        side_layout.addLayout(checkbox_layout)
        side_layout.addStretch(1)
        side_layout.addLayout(slider_layout)

        layout.addLayout(color1_layout)
        layout.addLayout(color2_layout)
        layout.addLayout(side_layout)
        layout.addWidget(self.save_button)

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
   
    def slider_value_changed(self, value):
        self.slider.setValue(value)
        self.mode_changed.emit(value)
        if value == 0:
            # Apply light mode styles
            self.setStyleSheet("""
                QDialog {
                    background-color: #E0E0E0;
                }
                QLabel {
                    font-size: 15px;
                    color: #000000;
                }
                QLineEdit {
                    padding: 2px;
                    font-size: 15px;
                    color: #000000;
                    border: 1px solid #000000;
                    border-radius: 4px;
                    background-color: #FFFFFF;
                    selection-color: yellow;
                    selection-background-color: blue;
                }
                QPushButton {
                    padding: 6px 12px;
                    font-size: 10px;
                    border: 1px solid #000000;
                    border-radius: 4px;
                    background-color: #4787BD;
                    color: #000000;
                }
                QPushButton:hover {
                    background-color: #3E76A6;
                }
                QPushButton:pressed {
                    background-color: #36668F;
                }
                QSlider {
                    background-color: transparent;
                    height: 30px;
                    padding: 0;
                }
                QSlider::groove:horizontal {
                    background-color: #333333;
                    height: 6px;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background-color: #000000;
                    width: 20px;
                    height: 20px;
                    margin: -7px 0;
                    border-radius: 10px;
                }
                QSlider::handle:horizontal:hover {
                    background-color: #333333;
                }
                QSlider::handle:horizontal:pressed {
                    background-color: #555555;
                }
                QCheckBox {
                    spacing: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
                QCheckBox::indicator:unchecked {
                    image: url(images/checkbox_unchecked_light.png);
                }
                QCheckBox::indicator:unchecked:hover {
                    image: url(images/checkbox_unchecked_hover_light.png);
                }
                QCheckBox::indicator:unchecked:pressed {
                    image: url(images/checkbox_unchecked_pressed_light.png);
                }
                QCheckBox::indicator:checked {
                    image: url(images/checkbox_checked_light.png);
                }
                QCheckBox::indicator:checked:hover {
                    image: url(images/checkbox_checked_hover_light.png);
                }
                QCheckBox::indicator:checked:pressed {
                    image: url(images/checkbox_checked_pressed_light.png);
                }
            """)

        else:
            # Apply dark mode styles
            self.setStyleSheet("""
                QDialog {
                    background-color: #333333;
                }
                QLabel {
                    font-size: 15px;
                    color: #FFFFFF;
                }
                QLineEdit {
                    padding: 2px;
                    font-size: 15px;
                    color: #FFFFFF;
                    border: 1px solid #FFFFFF;
                    border-radius: 4px;
                    background-color: #222222;
                    selection-color: yellow;
                    selection-background-color: blue;
                }
                QPushButton {
                    padding: 6px 12px;
                    font-size: 10px;
                    border: 1px solid #FFFFFF;
                    border-radius: 4px;
                    background-color: #286090;
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #1A4D73;
                }
                QPushButton:pressed {
                    background-color: #144057;
                }
                QSlider {
                    background-color: transparent;
                    height: 30px;
                    padding: 0;
                }
                QSlider::groove:horizontal {
                    background-color: #E0E0E0;
                    height: 6px;
                    border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background-color: #FFFFFF;
                    width: 20px;
                    height: 20px;
                    margin: -7px 0;
                    border-radius: 10px;
                }
                QSlider::handle:horizontal:hover {
                    background-color: #DDDDDD;
                }
                QSlider::handle:horizontal:pressed {
                    background-color: #BBBBBB;
                }
                QCheckBox {
                    spacing: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                }
                QCheckBox::indicator:unchecked {
                    image: url(images/checkbox_unchecked_dark.png);
                }
                QCheckBox::indicator:unchecked:hover {
                    image: url(images/checkbox_unchecked_hover_dark.png);
                }
                QCheckBox::indicator:unchecked:pressed {
                    image: url(images/checkbox_unchecked_pressed_dark.png);
                }
                QCheckBox::indicator:checked {
                    image: url(images/checkbox_checked_dark.png);
                }
                QCheckBox::indicator:checked:hover {
                    image: url(images/checkbox_checked_hover_dark.png);
                }
                QCheckBox::indicator:checked:pressed {
                    image: url(images/checkbox_checked_pressed_dark.png);
                }
            """)


    def save_settings(self):
        color1 = self.color1_edit.text()
        color2 = self.color2_edit.text()
        state = self.show_percentage.isChecked()
        value = self.slider.value()

        self.save_clicked.emit(color1, color2, state, value)
        self.close()




###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PIE")
        self.setMinimumSize(600, 400)
        self.setMaximumSize(600, 400)

        # Set the window flags to keep the window on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        input_layout = QHBoxLayout()

        # Create input fields
        input1_label = QLabel("Total:")
        self.input1_edit = QLineEdit()
        self.input1_edit.textEdited.connect(self.update_chart)

        input2_label = QLabel("Current:")
        self.input2_edit = QLineEdit()
        self.input2_edit.textEdited.connect(self.update_chart)

        # Create settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)

        # Apply custom styles to the widgets (default dark mode)
        self.set_mode(1)

        # Create a canvas for the matplotlib chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Add widgets to the layout
        input_layout.addWidget(input1_label)
        input_layout.addWidget(self.input1_edit)
        input_layout.addWidget(input2_label)
        input_layout.addWidget(self.input2_edit)
        input_layout.addWidget(self.settings_button)

        layout.addLayout(input_layout)
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
        self.checkbox = True
        self.mode = 1

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.slider_value_changed(self.mode)
        settings_window.color1_edit.setText(self.color1)
        settings_window.color2_edit.setText(self.color2)
        settings_window.show_percentage.setChecked(self.checkbox)
        settings_window.mode_changed.connect(self.set_mode)
        settings_window.save_clicked.connect(self.handle_settings_saved)
        settings_window.exec_()

    
    def handle_settings_saved(self, color1, color2, state, value):
        self.color1 = color1
        self.color2 = color2
        self.checkbox = state
        self.mode = value
        self.update_chart()

    def set_mode(self, value):
        if value == 0:
            # Apply light mode styles
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #E0E0E0;
                }
                QLabel {
                    font-size: 15px;
                    color: #000000;
                }
                QLineEdit {
                    padding: 2px;
                    color: #000000;
                    font-size: 15px;
                    border: 1px solid #000000;
                    border-radius: 4px;
                    background-color: #FFFFFF;
                    selection-color: yellow;
                    selection-background-color: blue;
                }
                QPushButton {
                    padding: 6px 12px;
                    font-size: 10px;
                    border: 1px solid #000000;
                    border-radius: 4px;
                    background-color: #4787BD;
                    color: #000000;
                }
                QPushButton:hover {
                    background-color: #3E76A6;
                }
                QPushButton:pressed {
                    background-color: #36668F;
                }
            """)

        else:
            # Apply dark mode styles
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #333333;
                }
                QLabel {
                    font-size: 15px;
                    color: #FFFFFF;
                }
                QLineEdit {
                    padding: 2px;
                    color: #FFFFFF;
                    font-size: 15px;
                    border: 1px solid #FFFFFF;
                    border-radius: 4px;
                    background-color: #222222;
                    selection-color: yellow;
                    selection-background-color: blue;
                }
                QPushButton {
                    padding: 6px 12px;
                    font-size: 10px;
                    border: 1px solid #FFFFFF;
                    border-radius: 4px;
                    background-color: #286090;
                    color: #FFFFFF;
                }
                QPushButton:hover {
                    background-color: #1A4D73;
                }
                QPushButton:pressed {
                    background-color: #144057;
                }
            """)

    

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
        font_properties = font_manager.FontProperties(fname="Montserrat-Regular.ttf", size=15) 


        if self.mode:
            self.figure.set_facecolor('#333333') 
            ax.set_title('(Pie Chart Title)', color='#FFFFFF', fontdict={"fontproperties": font_properties})
            if self.checkbox:
                ax.pie(values, colors=[self.color1, self.color2], autopct='%1.1f%%', wedgeprops={"linewidth": 1, "edgecolor": "white"})
            else:
                ax.pie(values, colors=[self.color1, self.color2], wedgeprops={"linewidth": 1, "edgecolor": "white"})
        else:
            self.figure.set_facecolor('#E0E0E0') 
            ax.set_title('(Pie Chart Title)', color='#000000', fontdict={"fontproperties": font_properties})
            if self.checkbox:
                ax.pie(values, colors=[self.color1, self.color2], autopct='%1.1f%%', wedgeprops={"linewidth": 1, "edgecolor": "black"})
            else:
                ax.pie(values, colors=[self.color1, self.color2], wedgeprops={"linewidth": 1, "edgecolor": "black"})

        ax.axis('equal')


        # Update the canvas
        self.canvas.draw()
