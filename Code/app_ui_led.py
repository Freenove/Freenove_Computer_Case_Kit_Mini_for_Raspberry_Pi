# app_ui_led.py
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton,QRadioButton, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class LedTab(QWidget):
    # Initialize LED control interface
    def __init__(self, width=700, height=400):
        """Initialize LED control interface"""
        super().__init__()
        
        # Control area
        self.led_mode_radio_buttons_names = ["Blink", "Rotate", "Rotate Quad", "Following", "Breathing", "Gradual", "Rainbow", "Code", "Close"] # LED mode names
        self.title_label = None                     # Title label
        self.led_mode_radio_buttons = []            # Create radio button list
        self.led_lable_red_slider_label = None      # Red slider label
        self.led_lable_red_slider_value = None      # Red slider value label
        self.led_lable_green_slider_label = None    # Green slider label
        self.led_lable_green_slider_value = None    # Green slider value label
        self.led_lable_blue_slider_label = None     # Blue slider label
        self.led_lable_blue_slider_value = None     # Blue slider value label
        self.led_lable_brightness_label = None      # Brightness label
        self.led_brightness_slider = None           # Brightness slider
        self.led_brightness_value_label = None      # Brightness value label
        self.led_slider_red = None                  # Red slider
        self.led_slider_green = None                # Green slider
        self.led_slider_blue = None                 # Blue slider
        self.save_params_button = None              # Save parameters button
        
        # Variable area
        self.window_width = width               # Window width
        self.window_height = height             # Window height
        self.led_mode = 6                       # LED mode (0-8, 8 = off)
        self.led_last_mode = 8                  # Last LED mode
        self.led_slider_red_value = 0           # Red slider value
        self.led_slider_green_value = 0         # Green slider value
        self.led_slider_blue_value = 255        # Blue slider value
        self.led_brightness_value = 100         # Brightness value
        self.led_color_value = [0, 0, 255]      # LED color value
        
        # Define all styles in __init__
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
                border: none;
                outline: none;
                padding: 2px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """
        
        self.button_disabled_style = """
            QPushButton {
                background-color: #555555;
                color: #888888;
                border: none;
                outline: none;
                padding: 2px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
        """
        
        # Define slider style template
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
        self.white_slider_style = self.slider_style_template % "#FFFFFF"
        self.red_slider_style = self.slider_style_template % "#FF4040"
        self.green_slider_style = self.slider_style_template % "#40FF40"
        self.blue_slider_style = self.slider_style_template % "#4040FF"
        self.gray_slider_style = self.slider_style_template % "#555555"

        # Function area
        self.initUI()                        # Initialize interface
        self.set_led_mode(self.led_mode)


    def _create_radio_button_row(self, start_idx, end_idx, layout):
        """Create a row of radio buttons"""
        for i in range(start_idx, end_idx):
            radio_button = QRadioButton(self.led_mode_radio_buttons_names[i])
            radio_button.setStyleSheet(self.radio_button_style)
            radio_button.setMinimumSize(50, 30)
            self.led_mode_radio_buttons.append(radio_button)
            # Connect radio button to set mode function
            radio_button.toggled.connect(lambda checked, idx=i: self.set_led_mode(idx) if checked else None)
            layout.addWidget(radio_button)

    def _create_slider_with_label(self, label_text, min_val, max_val, initial_val, color_name=None):
        """Create a slider with a label"""
        label = QLabel(label_text)
        label.setStyleSheet(self.slider_label_style)
        label.setFixedWidth(90)
        
        slider = QSlider(Qt.Horizontal)
        if color_name == "red":
            slider.setStyleSheet(self.red_slider_style)
        elif color_name == "green":
            slider.setStyleSheet(self.green_slider_style)
        elif color_name == "blue":
            slider.setStyleSheet(self.blue_slider_style)
        elif color_name == "white":
            slider.setStyleSheet(self.gray_slider_style)
        else:
            slider.setStyleSheet(self.gray_slider_style)
        
        slider.setRange(min_val, max_val)
        slider.setValue(initial_val)
        
        value_label = QLabel(str(initial_val))
        value_label.setStyleSheet(self.slider_label_style)
        value_label.setFixedWidth(50)
        
        layout = QHBoxLayout()
        layout.addWidget(label, stretch=1)
        layout.addWidget(slider, stretch=9)
        layout.addWidget(value_label, stretch=1)
        layout.setSpacing(10)
        
        return label, slider, value_label, layout

    def enable_widget_with_style(self, widget, enabled_style, disabled_style, enabled):
        """Enable or disable a widget with a specific style"""
        if widget is None:
            return
            
        if enabled:
            widget.setStyleSheet(enabled_style)
            widget.setEnabled(True)
        else:
            widget.setStyleSheet(disabled_style)
            widget.setEnabled(False)

    # Initialize control interface
    def initUI(self):
        """Initialize control interface"""
        # Set screen scaling factor
        self.scale_factor = 0.6
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #333333;")  # Set black background for monitoring tab
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

        # Create three rows of radio buttons for different LED mode options
        self.led_mode_hbox_layout1 = QHBoxLayout()  # First row radio button layout
        self.led_mode_hbox_layout2 = QHBoxLayout()  # Second row radio button layout
        self.led_mode_hbox_layout3 = QHBoxLayout()  # Third row radio button layout
        
        # Create radio button rows using the helper function
        self._create_radio_button_row(0, 3, self.led_mode_hbox_layout1)  # First row (0-2)
        self._create_radio_button_row(3, 6, self.led_mode_hbox_layout2)  # Second row (3-5)
        self._create_radio_button_row(6, 9, self.led_mode_hbox_layout3)  # Third row (6-8)
        
        self.led_mode_hbox_layout1.setSpacing(10)          # Set control spacing
        self.led_mode_hbox_layout2.setSpacing(10)          # Set control spacing
        self.led_mode_hbox_layout3.setSpacing(10)          # Set control spacing

        # Add title label
        self.title_label = QLabel("LED Settings")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(self.slider_label_style)
        self.title_label.setFixedHeight(40)
        # Create a horizontal layout
        self.title_layout = QHBoxLayout()
        self.title_layout.addWidget(self.title_label) # Add title label

        # Add label, slider, slider value display - RED
        self.led_label_red_slider_label, self.led_slider_red, self.led_lable_red_slider_value, self.led_slider_red_layout = \
            self._create_slider_with_label("Red:", 0, 255, 0, "red")

        # Connect red slider value change
        self.led_slider_red.valueChanged.connect(self.on_red_slider_changed)
        
        # Add label, slider, slider value display - GREEN
        self.led_label_green_slider_label, self.led_slider_green, self.led_lable_green_slider_value, self.led_slider_green_layout = \
            self._create_slider_with_label("Green:", 0, 255, 0, "green")

        # Connect green slider value change
        self.led_slider_green.valueChanged.connect(self.on_green_slider_changed)
        
        # Add label, slider, slider value display - BLUE
        self.led_label_blue_slider_label, self.led_slider_blue, self.led_lable_blue_slider_value, self.led_slider_blue_layout = \
            self._create_slider_with_label("Blue:", 0, 255, 255, "blue")

        # Connect blue slider value change
        self.led_slider_blue.valueChanged.connect(self.on_blue_slider_changed)

        # Add brightness control as slider
        self.led_label_brightness_label, self.led_brightness_slider, self.led_brightness_value_label, self.led_brightness_layout = \
            self._create_slider_with_label("Brightness:", 0, 255, 255, "white")

        # Connect brightness slider value change
        self.led_brightness_slider.valueChanged.connect(self.on_brightness_changed)

        # Create save parameters button with same width as other controls
        self.save_params_button = QPushButton("Save Parameters")
        self.save_params_button.setStyleSheet(self.button_style)

        # Create layout for the save button that matches other controls
        self.save_button_layout = QHBoxLayout()
        # Add the button to span the full width like other controls
        self.save_button_layout.addWidget(self.save_params_button)

        # Set main layout
        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(20, 10, 20, 15)  # Set margins
        self.vbox_layout.setSpacing(10)  # Set control spacing
        self.vbox_layout.addLayout(self.led_mode_hbox_layout1)
        self.vbox_layout.addLayout(self.led_mode_hbox_layout2)
        self.vbox_layout.addLayout(self.led_mode_hbox_layout3)
        self.vbox_layout.addLayout(self.title_layout)
        self.vbox_layout.addLayout(self.led_slider_red_layout)
        self.vbox_layout.addLayout(self.led_slider_green_layout)
        self.vbox_layout.addLayout(self.led_slider_blue_layout)
        self.vbox_layout.addLayout(self.led_brightness_layout)
        self.vbox_layout.addLayout(self.save_button_layout)  # Add save button at the bottom

        # Set main window
        self.setLayout(self.vbox_layout)

    def set_save_button_enabled(self, enabled):
        self.enable_widget_with_style(self.save_params_button, self.button_style, self.button_disabled_style, enabled)
    
    # Event handlers for sliders
    def on_brightness_changed(self, value):
        self.led_brightness_value = value
        self.led_brightness_value_label.setText(str(value))
        
    def on_red_slider_changed(self, value):
        self.led_slider_red_value = value
        self.led_lable_red_slider_value.setText(str(value))
        self.update_title_color()
        
    def on_green_slider_changed(self, value):
        self.led_slider_green_value = value
        self.led_lable_green_slider_value.setText(str(value))
        self.update_title_color()
        
    def on_blue_slider_changed(self, value):
        self.led_slider_blue_value = value
        self.led_lable_blue_slider_value.setText(str(value))
        self.update_title_color()
    
    # Update title color based on current RGB values
    def update_title_color(self, state=True):
        """
        Calculate brightness from RGB values and set title label color accordingly.
        """
        rgb_values = (self.led_slider_red_value, self.led_slider_green_value, self.led_slider_blue_value)
        brightness = self._calculate_brightness(rgb_values)
        font_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
        
        font_hex = '#%02x%02x%02x' % font_color
        bg_hex = '#%02x%02x%02x' % rgb_values
        
        if state:
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {bg_hex};
                    color: {font_hex};
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 2px;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                }}
            """)
        else:
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    background-color: #333333;
                    color: #888888;
                    border: 1px solid #555555;
                    border-radius: 5px;
                    padding: 2px;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                }}
            """)

    def _calculate_brightness(self, rgb):
        """
        Calculate brightness from RGB values.
        """
        return (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000

    # Recalculate control heights when window size changes
    def resizeEvent(self, event):
        """
        Recalculate control heights when window size changes
        """
        super().resizeEvent(event)

        # Recalculate led_ui_height
        self.led_ui_height = round((self.height() - 80) // 7)
        
        # Update maximum height of controls with null checks
        if hasattr(self, 'title_label') and self.title_label:
            self.title_label.setMaximumHeight(self.led_ui_height)
        
        for i in range(len(self.led_mode_radio_buttons_names)):
            if i < len(self.led_mode_radio_buttons):
                self.led_mode_radio_buttons[i].setMaximumHeight(self.led_ui_height)
        
        # Check all slider related controls before setting properties
        controls_to_update = [
            ('led_label_brightness_label', 'setMaximumHeight'),
            ('led_lable_red_slider_label', 'setMaximumHeight'),
            ('led_lable_green_slider_label', 'setMaximumHeight'), 
            ('led_lable_blue_slider_label', 'setMaximumHeight'),
            ('led_lable_brightness_label', 'setMaximumHeight'),
            ('led_lable_red_slider_value', 'setMaximumHeight'),
            ('led_lable_green_slider_value', 'setMaximumHeight'),
            ('led_lable_blue_slider_value', 'setMaximumHeight'),
            ('led_brightness_value_label', 'setMaximumHeight'),
            ('led_brightness_slider', 'setMaximumHeight'),
            ('led_slider_red', 'setMaximumHeight'),
            ('led_slider_green', 'setMaximumHeight'),
            ('led_slider_blue', 'setMaximumHeight'),
            ('save_params_button', 'setMaximumHeight')
        ]
        
        for attr_name, method_name in controls_to_update:
            if hasattr(self, attr_name) and getattr(self, attr_name):
                getattr(getattr(self, attr_name), method_name)(self.led_ui_height)

    # Reset UI size
    def resetUiSize(self, width, height):
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor), round(self.window_height*self.scale_factor))

    # Handle window close event
    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()

    # Set LED mode
    def set_led_mode(self, mode):
        """Set LED mode"""
        for i, radio_button in enumerate(self.led_mode_radio_buttons):
            if i == mode:
                radio_button.setChecked(True)
                radio_button.setStyleSheet(self.radio_button_style)
            else:
                radio_button.setChecked(False)
                radio_button.setStyleSheet(self.radio_button_style)
        
        modes_with_sliders = ["Blink", "Rotate", "Rotate Quad", "Following", "Breathing"]
        slider_enabled = self.led_mode_radio_buttons_names[mode] in modes_with_sliders
        self.set_slider_control_state(slider_enabled)

    # Set brightness value
    def set_led_brightness_slider_value(self, value):
        """Set brightness value"""
        self.led_brightness_slider.setValue(value)
        self.led_brightness_value_label.setText(str(value))
        self.led_brightness_value = value

    def set_title_color(self, bg=(0, 0, 0), font=None):
        """Set title bar color"""
        # If font color is not specified, automatically select black or white based on background
        if font is None:
            # Calculate background brightness using standard brightness formula
            brightness = self._calculate_brightness(bg)
            # If brightness is greater than 128, use black font; otherwise use white font
            font = (0, 0, 0) if brightness > 128 else (255, 255, 255)
        
        font_color = '#%02x%02x%02x' % font
        bg_color = '#%02x%02x%02x' % tuple(bg)  
        self.title_label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {font_color};
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }}
        """)

    # Set slider control state
    def set_slider_control_state(self, state):
        """Set slider control state"""
        self.enable_widget_with_style(self.led_label_brightness_label, self.slider_label_style, self.slider_label_disabled_style, state)
        self.enable_widget_with_style(self.led_brightness_slider, self.white_slider_style, self.gray_slider_style, state)
        self.enable_widget_with_style(self.led_brightness_value_label, self.slider_label_style, self.slider_label_disabled_style, state)
        self.enable_widget_with_style(self.led_label_red_slider_label, self.slider_label_style, self.slider_label_disabled_style, state)
        self.enable_widget_with_style(self.led_slider_red, self.red_slider_style, self.gray_slider_style, state)
        self.enable_widget_with_style(self.led_lable_red_slider_value, self.slider_label_style, self.slider_label_disabled_style, state)
        self.enable_widget_with_style(self.led_label_green_slider_label, self.slider_label_style, self.slider_label_disabled_style, state)
        self.enable_widget_with_style(self.led_slider_green, self.green_slider_style, self.gray_slider_style, state)
        self.enable_widget_with_style(self.led_lable_green_slider_value, self.slider_label_style, self.slider_label_disabled_style, state)
        self.enable_widget_with_style(self.led_label_blue_slider_label, self.slider_label_style, self.slider_label_disabled_style, state)
        self.enable_widget_with_style(self.led_slider_blue, self.blue_slider_style, self.gray_slider_style, state)
        self.enable_widget_with_style(self.led_lable_blue_slider_value, self.slider_label_style, self.slider_label_disabled_style, state)
        self.update_title_color(state)

    # Set slider value and title color
    def set_led_color_slider_value(self, color):
        self.led_slider_red.setValue(color[0])
        self.led_slider_green.setValue(color[1])
        self.led_slider_blue.setValue(color[2])
        self.led_lable_red_slider_value.setText(str(color[0]))
        self.led_lable_green_slider_value.setText(str(color[1]))
        self.led_lable_blue_slider_value.setText(str(color[2]))
        self.led_slider_red_value = color[0]
        self.led_slider_green_value = color[1]
        self.led_slider_blue_value = color[2]
        self.update_title_color()

        
if __name__ == "__main__":
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')
    if screen_direction == 0:  
        window = LedTab(800, 420)
    elif screen_direction == 1: 
        window = LedTab(480, 740)
    window.show()
    sys.exit(app.exec_())