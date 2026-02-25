# app_ui_fan.py
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QSlider, QLabel, QPushButton, QRadioButton, QLineEdit
from PyQt5.QtCore import Qt

class FanTab(QWidget):
    def __init__(self, width=700, height=400):
        super().__init__()
        
        self.fan_mode_radio_buttons_names = ["Temp Mode", "Manual Mode", "Default Mode"]
        self.fan_mode_radio_buttons = []
        
        self.window_width = width
        self.window_height = height

        self.fan_temp_mode_threshold_low = [0, 50]
        self.fan_temp_mode_threshold_high = [50, 100]
        self.fan_temp_threshold_hyst = [1, 5]
        
        self.radio_button_style = """
            QRadioButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
        """
        self.radio_button_disabled_style = """
            QRadioButton {
                background-color: #666666;
                color: #888888;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
        """
        self.slider_label_style = """
            background-color: #444444;
            color: white;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 2px;
            font-size: 14px;
            font-weight: bold;
        """
        self.slider_label_disabled_style = """
            background-color: #333333;
            color: #888888;
            border: 1px solid #555555;
            border-radius: 5px;
            padding: 2px;
            font-size: 14px;
            font-weight: bold;
        """
        self.button_style = """
            QPushButton {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """
        self.button_disabled_style = """
            QPushButton {
                background-color: #333333;
                color: #888888;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
            }
        """
        self.line_edit_style = """
            QLineEdit {
                background-color: #444444;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        """
        self.line_edit_disabled_style = """
            QLineEdit {
                background-color: #333333;
                color: #888888;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
        """
        self.slider_style_template = """
            QSlider {
                border: 2px solid #444444;
                border-radius: 5px;
                background-color: #333333;
                padding: 2px;
            }
            QSlider::groove:horizontal { 
                background: #555555;
                height: 20px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: %s;
                width: 40px;
                height: 20px;
                margin-top: -8px;
                margin-bottom: -8px;
            }
        """
        
        self.red_slider_style = self.slider_style_template % "#87CEEB"
        self.blue_slider_style = self.slider_style_template % "#FF6347"
        self.yellow_slider_style = self.slider_style_template % "#45B7D1"
        self.gray_slider_style = self.slider_style_template % "#555555"

        self.save_params_button = None

        self.init_ui()
        self.set_fan_mode(0)

    def init_ui(self):
        self.scale_factor = 0.6
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #333333;")
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

        self.fan_mode_hbox_layout = QHBoxLayout()
        for i in range(3):
            radio_button = QRadioButton(self.fan_mode_radio_buttons_names[i])
            radio_button.setStyleSheet(self.radio_button_style)
            radio_button.toggled.connect(lambda checked, idx=i: self.set_fan_mode(idx) if checked else None)
            
            self.fan_mode_radio_buttons.append(radio_button)
            self.fan_mode_radio_buttons[i].setMinimumSize(50, 30)
            self.fan_mode_hbox_layout.addWidget(self.fan_mode_radio_buttons[i])
        self.fan_mode_hbox_layout.setSpacing(10)
        self.fan_mode_hbox_layout.setStretch(0,1)
        self.fan_mode_hbox_layout.setStretch(1,1)
        self.fan_mode_hbox_layout.setStretch(2,1)

        temp_layout = self.create_temperature_controls(self.line_edit_style, self.button_style)

        low_speed_layout = self.create_speed_slider("Low Speed:", 0, 100, 50, "#87CEEB")
        high_speed_layout = self.create_speed_slider("High Speed:", 101, 255, 175, "#FF6347")

        fan_manual_layout = self.create_fan_control_slider("Fan Duty:", 0, 255, 0, "#45B7D1")

        self.slider_area_layout = QVBoxLayout()
        self.slider_area_layout.setSpacing(10)
        self.slider_area_layout.addLayout(temp_layout)
        self.slider_area_layout.addLayout(low_speed_layout)
        self.slider_area_layout.addLayout(high_speed_layout)
        self.slider_area_layout.addLayout(fan_manual_layout)
        self.slider_area_layout.setStretch(0, 1)
        self.slider_area_layout.setStretch(1, 1)
        self.slider_area_layout.setStretch(2, 1)
        self.slider_area_layout.setStretch(3, 1)

        self.save_params_button = QPushButton("Save Parameters")
        self.save_params_button.setStyleSheet(self.button_style)

        self.save_button_layout = QHBoxLayout()
        self.save_button_layout.addWidget(self.save_params_button)

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(20, 10, 20, 10)
        self.vbox_layout.setSpacing(10)
        self.vbox_layout.addLayout(self.fan_mode_hbox_layout)
        self.slider_area_layout.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout.addLayout(self.slider_area_layout)
        self.vbox_layout.addLayout(self.save_button_layout)  
        self.vbox_layout.setStretch(0,1)
        self.vbox_layout.setStretch(1,7)
        self.vbox_layout.setStretch(2,1)

        self.setLayout(self.vbox_layout)
        
    def set_save_button_enabled(self, enabled):
        self.enable_widget_with_style(self.save_params_button, self.button_style, self.button_disabled_style, enabled)

    def create_temperature_controls(self, line_edit_style, button_style):
        self.fan_case_low_temp_label = QLabel("Low Temp")
        self.fan_case_low_temp_label.setStyleSheet(self.slider_label_style)
        self.fan_case_high_temp_label = QLabel("High Temp")
        self.fan_case_high_temp_label.setStyleSheet(self.slider_label_style)
        self.fan_case_temp_schmitt_label = QLabel("Schmitt")
        self.fan_case_temp_schmitt_label.setStyleSheet(self.slider_label_style)

        self.fan_case_low_temp_input = QLineEdit()
        self.fan_case_low_temp_input.setStyleSheet(line_edit_style)
        self.fan_case_low_temp_input.setText(str(45))
        self.fan_case_low_temp_input.setAlignment(Qt.AlignCenter)
        self.fan_case_low_temp_input.setEnabled(False)
        self.fan_case_low_temp_input.setReadOnly(True)
        
        self.fan_case_high_temp_input = QLineEdit()
        self.fan_case_high_temp_input.setStyleSheet(line_edit_style)
        self.fan_case_high_temp_input.setText(str(80))
        self.fan_case_high_temp_input.setAlignment(Qt.AlignCenter)
        self.fan_case_high_temp_input.setEnabled(False)
        self.fan_case_high_temp_input.setReadOnly(True)
        
        self.fan_case_temp_schmitt_input = QLineEdit()
        self.fan_case_temp_schmitt_input.setStyleSheet(line_edit_style)
        self.fan_case_temp_schmitt_input.setText(str(3))
        self.fan_case_temp_schmitt_input.setAlignment(Qt.AlignCenter)
        self.fan_case_temp_schmitt_input.setEnabled(False)
        self.fan_case_temp_schmitt_input.setReadOnly(True)

        self.fan_case_low_temp_minus_btn = QPushButton("-")
        self.fan_case_low_temp_minus_btn.setStyleSheet(button_style)
        self.fan_case_low_temp_plus_btn = QPushButton("+")
        self.fan_case_low_temp_plus_btn.setStyleSheet(button_style)
        self.fan_case_high_temp_minus_btn = QPushButton("-")
        self.fan_case_high_temp_minus_btn.setStyleSheet(button_style)
        self.fan_case_high_temp_plus_btn = QPushButton("+")
        self.fan_case_high_temp_plus_btn.setStyleSheet(button_style)
        self.fan_case_temp_schmitt_minus_btn = QPushButton("-")
        self.fan_case_temp_schmitt_minus_btn.setStyleSheet(button_style)
        self.fan_case_temp_schmitt_plus_btn = QPushButton("+")
        self.fan_case_temp_schmitt_plus_btn.setStyleSheet(button_style)

        self.fan_case_low_temp_minus_btn.setAutoRepeat(True)
        self.fan_case_low_temp_plus_btn.setAutoRepeat(True)
        self.fan_case_high_temp_minus_btn.setAutoRepeat(True)
        self.fan_case_high_temp_plus_btn.setAutoRepeat(True)
        self.fan_case_temp_schmitt_minus_btn.setAutoRepeat(True)
        self.fan_case_temp_schmitt_plus_btn.setAutoRepeat(True)

        self.fan_case_low_temp_minus_btn.setAutoRepeatDelay(500)
        self.fan_case_low_temp_minus_btn.setAutoRepeatInterval(100)
        self.fan_case_high_temp_minus_btn.setAutoRepeatDelay(500)
        self.fan_case_high_temp_minus_btn.setAutoRepeatInterval(100)
        self.fan_case_temp_schmitt_minus_btn.setAutoRepeatDelay(500)
        self.fan_case_temp_schmitt_minus_btn.setAutoRepeatInterval(100)
        self.fan_case_low_temp_plus_btn.setAutoRepeatDelay(500)
        self.fan_case_low_temp_plus_btn.setAutoRepeatInterval(100)
        self.fan_case_high_temp_plus_btn.setAutoRepeatDelay(500)
        self.fan_case_high_temp_plus_btn.setAutoRepeatInterval(100)
        self.fan_case_temp_schmitt_plus_btn.setAutoRepeatDelay(500)
        self.fan_case_temp_schmitt_plus_btn.setAutoRepeatInterval(100)

        self.fan_case_low_temp_minus_btn.clicked.connect(self.decrease_low_temp)
        self.fan_case_low_temp_plus_btn.clicked.connect(self.increase_low_temp)
        self.fan_case_high_temp_minus_btn.clicked.connect(self.decrease_high_temp)
        self.fan_case_high_temp_plus_btn.clicked.connect(self.increase_high_temp)
        self.fan_case_temp_schmitt_minus_btn.clicked.connect(self.decrease_schmitt)
        self.fan_case_temp_schmitt_plus_btn.clicked.connect(self.increase_schmitt)

        temp_settings_layout = QHBoxLayout()
        
        low_temp_layout = QHBoxLayout()
        low_temp_layout.addWidget(self.fan_case_low_temp_minus_btn)
        low_temp_layout.addWidget(self.fan_case_low_temp_input)
        low_temp_layout.addWidget(self.fan_case_low_temp_plus_btn)
        low_temp_layout.setStretch(0, 1)
        low_temp_layout.setStretch(1, 1)
        low_temp_layout.setStretch(2, 1)
        low_temp_layout.setSpacing(5)

        high_temp_layout = QHBoxLayout()
        high_temp_layout.addWidget(self.fan_case_high_temp_minus_btn)
        high_temp_layout.addWidget(self.fan_case_high_temp_input)
        high_temp_layout.addWidget(self.fan_case_high_temp_plus_btn)
        high_temp_layout.setStretch(0, 1)
        high_temp_layout.setStretch(1, 1)
        high_temp_layout.setStretch(2, 1)
        high_temp_layout.setSpacing(5)
        
        schmitt_layout = QHBoxLayout()
        schmitt_layout.addWidget(self.fan_case_temp_schmitt_minus_btn)
        schmitt_layout.addWidget(self.fan_case_temp_schmitt_input)
        schmitt_layout.addWidget(self.fan_case_temp_schmitt_plus_btn)
        schmitt_layout.setStretch(0, 1)
        schmitt_layout.setStretch(1, 1)
        schmitt_layout.setStretch(2, 1)
        schmitt_layout.setSpacing(5)
        
        low_temp_vbox = QVBoxLayout()
        low_temp_vbox.addWidget(self.fan_case_low_temp_label)
        low_temp_vbox.addLayout(low_temp_layout)
        low_temp_vbox.setSpacing(10)
        
        high_temp_vbox = QVBoxLayout()
        high_temp_vbox.addWidget(self.fan_case_high_temp_label)
        high_temp_vbox.addLayout(high_temp_layout)
        high_temp_vbox.setSpacing(10)
        
        schmitt_vbox = QVBoxLayout()
        schmitt_vbox.addWidget(self.fan_case_temp_schmitt_label)
        schmitt_vbox.addLayout(schmitt_layout)
        schmitt_vbox.setSpacing(10)
        
        temp_settings_layout.addLayout(low_temp_vbox)
        temp_settings_layout.addLayout(high_temp_vbox)
        temp_settings_layout.addLayout(schmitt_vbox)
        temp_settings_layout.setSpacing(10)
        temp_settings_layout.setStretch(0, 1)
        temp_settings_layout.setStretch(1, 1)
        temp_settings_layout.setStretch(2, 1)
        
        return temp_settings_layout

    def create_speed_slider(self, label_text, min_val, max_val, default_val, color):
        slider_label = QLabel(label_text)
        slider_label.setStyleSheet(self.slider_label_style)
        slider_label.setFixedWidth(120)
        
        slider = QSlider(Qt.Horizontal)
        slider.setStyleSheet(self.slider_style_template % color)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)
        
        value_label = QLabel(str(default_val))
        value_label.setStyleSheet(self.slider_label_style)
        value_label.setFixedWidth(60)
        
        layout = QHBoxLayout()
        layout.addWidget(slider_label)
        layout.addWidget(slider)
        layout.addWidget(value_label)
        layout.setSpacing(10)
        
        if label_text == "Low Speed:":
            self.fan_case_low_speed_slider_label = slider_label
            self.fan_case_low_speed_slider = slider
            self.fan_case_low_speed_slider_value = value_label
            self.fan_case_low_speed_slider.valueChanged.connect(self.on_temp_mode_low_speed_changed)
        elif label_text == "High Speed:":
            self.fan_case_high_speed_slider_label = slider_label
            self.fan_case_high_speed_slider = slider
            self.fan_case_high_speed_slider_value = value_label
            self.fan_case_high_speed_slider.valueChanged.connect(self.on_temp_mode_high_speed_changed)
        return layout

    def create_fan_control_slider(self, label_text, min_val, max_val, default_val, color):
        self.fan_manual_slider_label = QLabel(label_text)
        self.fan_manual_slider_label.setStyleSheet(self.slider_label_style)
        self.fan_manual_slider_label.setFixedWidth(120)
        
        self.fan_manual_slider = QSlider(Qt.Horizontal)
        self.fan_manual_slider.setStyleSheet(self.slider_style_template % color)
        self.fan_manual_slider.setRange(min_val, max_val)
        self.fan_manual_slider.setValue(default_val)
        
        self.fan_manual_slider_value = QLabel(str(default_val))
        self.fan_manual_slider_value.setStyleSheet(self.slider_label_style)
        self.fan_manual_slider_value.setFixedWidth(60)

        layout = QHBoxLayout()
        layout.addWidget(self.fan_manual_slider_label)
        layout.addWidget(self.fan_manual_slider)
        layout.addWidget(self.fan_manual_slider_value)
        layout.setSpacing(10)

        self.fan_manual_slider.valueChanged.connect(self.on_manual_mode_duty_changed)
        
        return layout

    def decrease_low_temp(self):
        try:
            value = int(self.fan_case_low_temp_input.text())
            value -= 1
            min_val = self.fan_temp_mode_threshold_low[0]
            if value < min_val:
                value = min_val
            high_temp = int(self.fan_case_high_temp_input.text()) 
            hyst_temp = int(self.fan_case_temp_schmitt_input.text())
            if value >= (high_temp-hyst_temp):
                value = (high_temp-hyst_temp) - 1
            self.fan_case_low_temp_input.setText(str(value))
        except ValueError:
            self.fan_case_low_temp_input.setText(str(45))

    def increase_low_temp(self):
        try:
            value = int(self.fan_case_low_temp_input.text())
            value += 1
            max_val = self.fan_temp_mode_threshold_low[1]
            if value > max_val:
                value = max_val
            high_temp = int(self.fan_case_high_temp_input.text())
            hyst_temp = int(self.fan_case_temp_schmitt_input.text())
            if value >= (high_temp-hyst_temp):
                value = (high_temp-hyst_temp) - 1
            self.fan_case_low_temp_input.setText(str(value))
        except ValueError:
            self.fan_case_low_temp_input.setText(str(45))

    def decrease_high_temp(self):
        try:
            value = int(self.fan_case_high_temp_input.text())
            value -= 1
            min_val = self.fan_temp_mode_threshold_high[0]
            if value < min_val:
                value = min_val
            low_temp = int(self.fan_case_low_temp_input.text())
            hyst_temp = int(self.fan_case_temp_schmitt_input.text())
            if value <= (low_temp+hyst_temp):
                value = (low_temp+hyst_temp) + 1
            self.fan_case_high_temp_input.setText(str(value))
        except ValueError:
            self.fan_case_high_temp_input.setText(str(80))

    def increase_high_temp(self):
        try:
            value = int(self.fan_case_high_temp_input.text())
            value += 1
            max_val = self.fan_temp_mode_threshold_high[1]
            if value > max_val:
                value = max_val
            low_temp = int(self.fan_case_low_temp_input.text())
            hyst_temp = int(self.fan_case_temp_schmitt_input.text())
            if value <= (low_temp+hyst_temp):
                value = (low_temp+hyst_temp) + 1
            self.fan_case_high_temp_input.setText(str(value))
        except ValueError:
            self.fan_case_high_temp_input.setText(str(80))

    def decrease_schmitt(self):
        try:
            value = int(self.fan_case_temp_schmitt_input.text())
            value -= 1
            min_val = self.fan_temp_threshold_hyst[0]
            if value < min_val:
                value = min_val
            self.fan_case_temp_schmitt_input.setText(str(value))
        except ValueError:
            self.fan_case_temp_schmitt_input.setText(str(3))

    def increase_schmitt(self):
        try:
            value = int(self.fan_case_temp_schmitt_input.text())
            value += 1

            high_temp = int(self.fan_case_high_temp_input.text())
            low_temp = int(self.fan_case_low_temp_input.text())
            max_val = self.fan_temp_threshold_hyst[1]
            if value > max_val:
                value = max_val
            if value >= (high_temp-low_temp):
                value = (high_temp-low_temp) - 1
            self.fan_case_temp_schmitt_input.setText(str(value))

        except ValueError:
            self.fan_case_temp_schmitt_input.setText(str(3))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fan_ui_height = max(20, round((self.height() - 80) // 7))  

        for i in range(len(self.fan_mode_radio_buttons_names)):
            self.fan_mode_radio_buttons[i].setMaximumHeight(self.fan_ui_height)

        controls_to_resize = [
            self.fan_case_low_temp_label, self.fan_case_high_temp_label, self.fan_case_temp_schmitt_label,
            self.fan_case_low_temp_minus_btn, self.fan_case_low_temp_plus_btn,
            self.fan_case_high_temp_minus_btn, self.fan_case_high_temp_plus_btn,
            self.fan_case_temp_schmitt_minus_btn, self.fan_case_temp_schmitt_plus_btn,
            self.fan_case_low_temp_input, self.fan_case_high_temp_input, self.fan_case_temp_schmitt_input,
            self.fan_case_low_speed_slider_label, self.fan_case_low_speed_slider_value,
            self.fan_case_low_speed_slider,
            self.fan_case_high_speed_slider_label, self.fan_case_high_speed_slider_value,
            self.fan_case_high_speed_slider,
            self.fan_manual_slider_label, self.fan_manual_slider_value,
            self.fan_manual_slider,
            self.save_params_button  
        ]
        
        for control in controls_to_resize:
            if control:
                control.setMaximumHeight(self.fan_ui_height)

    def resetUiSize(self, width, height):
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))
        
    def closeEvent(self, event):
        event.accept()
    
    def set_case_weight_temp(self, temp_threshold):
        self.fan_case_low_temp_input.setText(str(temp_threshold[0]))
        self.fan_case_high_temp_input.setText(str(temp_threshold[1]))
        self.fan_case_temp_schmitt_input.setText(str(temp_threshold[2]))
    
    def set_case_weight_slider_value(self, value):
        self.fan_case_low_speed_slider.setValue(value[0])
        self.fan_case_high_speed_slider.setValue(value[1])  
        self.fan_case_low_speed_slider_value.setText(str(value[0]))
        self.fan_case_high_speed_slider_value.setText(str(value[1]))  

    def set_manual_weight_slider_value(self, speed):
        self.fan_manual_slider.setValue(speed)
        self.fan_manual_slider_value.setText(str(speed))

    def enable_widget_with_style(self, widget, enabled_style, disabled_style, enabled):
        if widget is None:
            return
        if enabled:
            widget.setStyleSheet(enabled_style)
            widget.setEnabled(True)
        else:
            widget.setStyleSheet(disabled_style)
            widget.setEnabled(False)

    def set_fan_mode(self, mode):
        temp_mode_enabled = (mode == 0)
        manual_mode_enabled = (mode == 1)
        default_mode_enabled = (mode == 2)
        
        for i in range(len(self.fan_mode_radio_buttons)):
            self.fan_mode_radio_buttons[i].setChecked(True if i == mode else False)
        
        self.enable_widget_with_style(self.fan_case_low_temp_label, self.slider_label_style, self.slider_label_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_high_temp_label, self.slider_label_style, self.slider_label_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_temp_schmitt_label, self.slider_label_style, self.slider_label_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_low_temp_input, self.line_edit_style, self.line_edit_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_high_temp_input, self.line_edit_style, self.line_edit_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_temp_schmitt_input, self.line_edit_style, self.line_edit_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_low_temp_minus_btn, self.button_style, self.button_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_low_temp_plus_btn, self.button_style, self.button_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_high_temp_minus_btn, self.button_style, self.button_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_high_temp_plus_btn, self.button_style, self.button_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_temp_schmitt_minus_btn, self.button_style, self.button_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_temp_schmitt_plus_btn, self.button_style, self.button_disabled_style, temp_mode_enabled)
        
        self.enable_widget_with_style(self.fan_case_low_speed_slider_label, self.slider_label_style, self.slider_label_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_low_speed_slider, self.red_slider_style, self.gray_slider_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_low_speed_slider_value, self.slider_label_style, self.slider_label_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_high_speed_slider_label, self.slider_label_style, self.slider_label_disabled_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_high_speed_slider, self.blue_slider_style, self.gray_slider_style, temp_mode_enabled)
        self.enable_widget_with_style(self.fan_case_high_speed_slider_value, self.slider_label_style, self.slider_label_disabled_style, temp_mode_enabled)
        
        self.enable_widget_with_style(self.fan_manual_slider_label, self.slider_label_style, self.slider_label_disabled_style, manual_mode_enabled)
        self.enable_widget_with_style(self.fan_manual_slider, self.yellow_slider_style, self.gray_slider_style, manual_mode_enabled)
        self.enable_widget_with_style(self.fan_manual_slider_value, self.slider_label_style, self.slider_label_disabled_style, manual_mode_enabled)

        self.enable_widget_with_style(self.save_params_button, self.button_style, self.button_disabled_style, True)
    
    def on_temp_mode_low_speed_changed(self, value):
        self.fan_case_low_speed_slider_value.setText(str(value))
        
    def on_temp_mode_high_speed_changed(self, value):
        self.fan_case_high_speed_slider_value.setText(str(value))
        
    def on_manual_mode_duty_changed(self, value):
        self.fan_manual_slider_value.setText(str(value))
        

if __name__ == "__main__":
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')
    if screen_direction == 0:  
        window = FanTab(800, 420)
    elif screen_direction == 1: 
        window = FanTab(480, 740)
    
    window.show()
    sys.exit(app.exec_())