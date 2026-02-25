
# app_ui.py
import os
import sys
import time
import subprocess

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtCore import Qt, QTimer

from app_ui_monitor import MonitoringTab             # Import monitoring interface
from app_ui_led import LedTab                        # Import LED interface
from app_ui_fan import FanTab                        # Import fan control interface

from api_json import ConfigManager                   # Import configuration management module
from api_systemInfo import SystemInformation         # Import system information module
from api_service import ServiceGenerator             # Import background task generator module

class MainWindow(QMainWindow):
    def __init__(self, width=800, height=420):
        super().__init__()
        self.ui_main_width = width
        self.ui_main_height = height
        self.setWindowTitle("Freenove_Computer_Case_Kit_Mini_for_Raspberry_Pi")   # Set window title
        self.setGeometry(0, 0, self.ui_main_width, self.ui_main_height)          # Set window size
        self.setMinimumSize(self.ui_main_width, self.ui_main_height)             # Set minimum size
        self.system_info = SystemInformation()                                   # Create system information object
        self.convert_to_fahrenheit = False                                       # Whether to convert to Fahrenheit
        self.is_show_monitor_ui = True                                           # Whether to show monitoring interface
        
        # Create two service generator instances for LED and FAN respectively
        self.led_service_generator = ServiceGenerator(
            filename="task_led.py",
            service_name="task_led.service"
        )
        self.fan_service_generator = ServiceGenerator(
            filename="task_fan.py",
            service_name="task_fan.service"
        )
        
        self.color_combinations = [
            ('#FF6B6B', '#FFD1D1'),  # Red
            ('#4ECEB4', '#D1F2D1'),  # Green
            ('#45B7D1', '#D1EBF0'),  # Blue
            ('#DDA0DD', '#F0E0F0'),  # Plum
            ('#FFA500', '#FFE5B4'),  # Orange
            ('#333333', '#333333'),  # Gray
            ('#EAEA77', '#FFFFF0'),  # Yellow
            ('#4ECDC4', '#D1F0EE'),  # Blue-green
            
            ('#F7DC6F', '#FBF5D9')   # Gold
        ]
        self.metric_labels = [
            "CPU Usage",     # CPU usage
            "RAM Usage",     # Memory usage
            "CPU Temp",      # Raspberry Pi temperature
            "Storage Usage", # Storage usage
            "RPi PWM",       # Raspberry Pi fan PWM
            ""               # None
        ]

        self.led_tab = None                                          # Create LED interface object
        self.fan_tab = None                                          # Create fan control interface object

        if self.is_show_monitor_ui:
            self.monitoring_tab = None                                   # Create monitoring interface object
            self.monitor_update_data_timer = QTimer(self)                # Create monitor interface data update timer
            self.monitor_update_data_timer_is_running = True             # Whether timer is running

        self.led_mode = 0                                            # LED mode
        self.led_slider_color = [0, 0, 0]                            # LED slider color values
        self.led_brightness = 255                                    # LED brightness
        self.fan_mode = 0                                            # Fan mode
        self.fan_manual_mode_duty = 255                              # Fan manual mode duty cycle values for 3 fan groups
        self.fan_temp_mode_threshold = [30, 50, 3]                   # Fan temperature mode threshold parameters
        self.fan_temp_mode_duty = [75, 125, 175]                     # Fan temperature mode duty cycle parameters

        self.init_ui()                                               # Initialize UI
        self.load_ui_config()                                        # Load UI parameters
        self.load_ui_events()                                        # Set events

    def init_ui(self):
        # Set black background for main window
        self.setStyleSheet("""
            background-color: #333333;
            border: 1px solid #444444;
            outline: none;
        """)
        # Create tab widget
        self.tab_widget = QTabWidget()

        if self.is_show_monitor_ui:
            # Create monitor tab
            self.monitoring_tab = MonitoringTab(self.width(), self.height())
            self.monitoring_tab.setFocusPolicy(Qt.NoFocus)
            for i in range(len(self.metric_labels)):
                self.monitoring_tab.setCircleProgressValue(i, 0, self.metric_labels[i], "")
                self.monitoring_tab.setCircleProgressColor(i, self.color_combinations[i])

        # Create led tab
        self.led_tab = LedTab(self.width(), self.height())
        self.led_tab.setFocusPolicy(Qt.NoFocus)

        # Create fan tab
        self.fan_tab = FanTab(self.width(), self.height())
        self.fan_tab.setFocusPolicy(Qt.NoFocus)

        # Add tab to tab widget
        if self.is_show_monitor_ui:
            self.tab_widget.addTab(self.monitoring_tab, "Monitor")
        self.tab_widget.addTab(self.led_tab, "LED")
        self.tab_widget.addTab(self.fan_tab, "Fan")
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #333333;
                background-color: #333333;
            }
            QTabBar::tab {
                background-color: #444444;
                color: white;
                padding: 2px;
                border: 1px solid #333333;
                font-size: 16px;
                font-weight: bold;
                height: 50px;
                width: 80px;
            }
            QTabBar::tab:selected {
                background-color: #555555;
                color: white;
            }
        """)

        # Set central widget
        self.setCentralWidget(self.tab_widget)
        
    def load_ui_config(self):
        """Load configuration"""
        self.showMaximized()
        self.screen_resolution = QApplication.desktop().screenGeometry()
        width = self.screen_resolution.width()
        height = self.screen_resolution.height()

        self.showNormal()
        if width > height:
            self.ui_main_width = 800
            self.ui_main_height = 420
        else:
            self.ui_main_width = 480
            self.ui_main_height = 740

        # Load Monitor interface parameters
        self.setFixedSize(self.ui_main_width, self.ui_main_height)
        if self.is_show_monitor_ui:
            self.monitoring_tab.resetUiSize(self.width(), self.height())
        self.led_tab.resetUiSize(self.width(), self.height())
        self.fan_tab.resetUiSize(self.width(), self.height())

        # Load configuration
        config_data = self.get_all_json_config()
        led_config = config_data.get('LED')
        fan_config = config_data.get('Fan')
        # Load LED configuration
        self.led_mode = led_config.get('mode', 6)
        self.led_slider_color[0] = led_config.get('red_value', 0)
        self.led_slider_color[1] = led_config.get('green_value', 0)
        self.led_slider_color[2] = led_config.get('blue_value', 255)
        self.led_brightness = led_config.get('brightness', 255)
        # Load Fan configuration - fix: Use correct section name 'Fan' instead of 'fan'
        self.fan_mode = fan_config.get('mode', 2)
        temp_config = fan_config.get('temp_mode_config', {})
        self.fan_temp_mode_threshold[0] = temp_config.get('fan_temp_threshold_low', 45)
        self.fan_temp_mode_threshold[1] = temp_config.get('fan_temp_threshold_high', 80)
        self.fan_temp_mode_threshold[2] = temp_config.get('fan_temp_threshold_hyst', 3)
        self.fan_temp_mode_duty[0] = temp_config.get('fan_temp_mode_duty_low', 50)
        self.fan_temp_mode_duty[1] = temp_config.get('fan_temp_mode_duty_high', 200)
        self.fan_manual_mode_duty = fan_config.get('manual_mode_duty', 255)

        # Load LED interface parameters
        self.led_tab.set_led_mode(self.led_mode)                               # Configure radio buttons based on mode
        self.led_tab.set_led_color_slider_value(self.led_slider_color)         # Set slider values
        self.led_tab.set_title_color(self.led_slider_color)                    # Set title color
        self.led_tab.set_led_brightness_slider_value(self.led_brightness)      # Set brightness
        if self.led_mode in range(5,9,1):                                      # If mode is 5-8, disable sliders
            self.led_tab.update_title_color(False)
            
        # Load fan interface parameters
        self.fan_tab.set_fan_mode(self.fan_mode)
        self.fan_tab.set_case_weight_temp(self.fan_temp_mode_threshold)
        self.fan_tab.set_case_weight_slider_value(self.fan_temp_mode_duty)
        self.fan_tab.set_manual_weight_slider_value(self.fan_manual_mode_duty)

        # Create services on startup
        self.led_service_generator.create_service_on_rpi()
        self.fan_service_generator.create_service_on_rpi()
        self.led_service_generator.restart_service_on_rpi()
        self.fan_service_generator.restart_service_on_rpi()
        
    def load_ui_events(self):
        """Handle events"""
        if self.is_show_monitor_ui:
            # Monitor interface signals and slot functions
            self.monitor_update_data_timer.timeout.connect(self.update_monitor_data_event)          # Connect to slot function
            self.monitor_update_data_timer.start(1000)                                              # Start timer, update data every second
    
        # LED interface signals and slot functions
        for i in range(len(self.led_tab.led_mode_radio_buttons_names)):  
            self.led_tab.led_mode_radio_buttons[i].clicked.connect(self.led_radio_clicked_event)
        self.led_tab.led_slider_red.sliderReleased.connect(self.led_slider_release_event)
        self.led_tab.led_slider_green.sliderReleased.connect(self.led_slider_release_event)
        self.led_tab.led_slider_blue.sliderReleased.connect(self.led_slider_release_event)
        self.led_tab.led_brightness_slider.sliderReleased.connect(self.led_slider_release_event)
        self.led_tab.save_params_button.clicked.connect(self.led_save_params_event)
    
        # Fan interface signals and slot functions
        for i in range(len(self.fan_tab.fan_mode_radio_buttons_names)):  
            self.fan_tab.fan_mode_radio_buttons[i].clicked.connect(self.fan_radio_clicked_event)
        self.fan_tab.fan_case_low_temp_minus_btn.clicked.connect(self.fan_config_change_event)
        self.fan_tab.fan_case_low_temp_plus_btn.clicked.connect(self.fan_config_change_event)
        self.fan_tab.fan_case_high_temp_minus_btn.clicked.connect(self.fan_config_change_event)
        self.fan_tab.fan_case_high_temp_plus_btn.clicked.connect(self.fan_config_change_event)
        self.fan_tab.fan_case_temp_schmitt_minus_btn.clicked.connect(self.fan_config_change_event)
        self.fan_tab.fan_case_temp_schmitt_plus_btn.clicked.connect(self.fan_config_change_event)
        self.fan_tab.fan_case_low_speed_slider.sliderReleased.connect(self.fan_config_change_event)
        self.fan_tab.fan_case_high_speed_slider.sliderReleased.connect(self.fan_config_change_event)
        self.fan_tab.fan_manual_slider.sliderReleased.connect(self.fan_config_change_event)
        self.fan_tab.save_params_button.clicked.connect(self.fan_save_params_event)

    # UI display related signals and slot functions
    def celsius_to_fahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    def update_monitor_data_event(self):
        """Periodically update monitor interface display data"""
        try:
            # Get system information
            cpu_usage = self.system_info.get_raspberry_pi_cpu_usage()       # CPU usage
            memory_info = self.system_info.get_raspberry_pi_memory_usage()  # Memory usage information
            ram_usage = memory_info[0] if isinstance(memory_info, list) else memory_info
            rpi_temp = self.system_info.get_raspberry_pi_cpu_temperature()  # Raspberry Pi CPU temperature
            disk_info = self.system_info.get_raspberry_pi_disk_usage()      # Disk usage information
            disk_usage = disk_info[0] if isinstance(disk_info, list) else disk_info
            rpi_temp_fahrenheit = self.celsius_to_fahrenheit(rpi_temp)
            
            # Get fan PWM information
            rpi_fan_pwm = self.system_info.get_raspberry_pi_fan_duty()      # Raspberry Pi fan PWM
            
            # Update progress controls
            # CPU usage
            self.monitoring_tab.setCircleProgressValue(0, cpu_usage, self.metric_labels[0], f"{cpu_usage:.1f}%")
            
            # Memory usage
            self.monitoring_tab.setCircleProgressValue(1, ram_usage, self.metric_labels[1], f"{ram_usage:.1f}%")

            # Raspberry Pi temperature 
            if self.convert_to_fahrenheit == False:
                self.monitoring_tab.setCircleProgressValue(2, min(100, rpi_temp/80*100), self.metric_labels[2], f"{rpi_temp:.1f}°C")
            else:
                self.monitoring_tab.setCircleProgressValue(2, min(100, rpi_temp/80*100), self.metric_labels[2], f"{rpi_temp_fahrenheit:.1f}°F")
            
            # Storage usage
            self.monitoring_tab.setCircleProgressValue(3, disk_usage, self.metric_labels[3], f"{disk_usage:.1f}%")
            
            # Raspberry Pi fan PWM (0-255 range)
            rpi_fan_percent = (rpi_fan_pwm / 255) * 100 if rpi_fan_pwm >= 0 else 0
            self.monitoring_tab.setCircleProgressValue(4, rpi_fan_percent, self.metric_labels[4], f"{rpi_fan_percent:.1f}%")
        
        except Exception as e:
            print(f"Error updating data: {e}")

    def update_monitor_colors_event(self):
        """Periodically update LED colors to circular progress bars"""
        try:
            # Get LED tab color values
            if hasattr(self.led_tab, 'led_color_value'): # Check if attribute exists
                r, g, b = self.led_slider_color
                hex_color = f"#{r:02X}{g:02X}{b:02X}"
                if hasattr(self.monitoring_tab, 'setCircleProgressColor'):
                    for i in range(5):  # Only 5 progress bars in this version
                        self.monitoring_tab.setCircleProgressColor(i, [hex_color, '#444444'])
        except Exception as e:
            print(f"Error updating LED colors: {e}")
    
    # LED interface signals and slot functions
    def led_radio_clicked_event(self):
        """Handle LED radio button click event"""
        sender_button = self.sender()
        for i in range(len(self.led_tab.led_mode_radio_buttons_names)):
            if sender_button.text() == self.led_tab.led_mode_radio_buttons_names[i]:
                self.led_mode = i
        self.led_slider_color[0] = int(self.led_tab.led_slider_red.value())
        self.led_slider_color[1] = int(self.led_tab.led_slider_green.value())
        self.led_slider_color[2] = int(self.led_tab.led_slider_blue.value())
        self.led_brightness = int(self.led_tab.led_brightness_slider.value())

        led_config = [
            ('LED', 'mode', self.led_mode),
            ('LED', 'red_value', self.led_slider_color[0]),
            ('LED', 'green_value', self.led_slider_color[1]),
            ('LED', 'blue_value', self.led_slider_color[2]),
            ('LED', 'brightness', self.led_brightness)
        ]
        self.set_all_json_config(led_config)
        
    def led_slider_release_event(self):
        """Handle LED slider release event"""
        self.led_slider_color[0] = self.led_tab.led_slider_red.value()
        self.led_slider_color[1] = self.led_tab.led_slider_green.value()
        self.led_slider_color[2] = self.led_tab.led_slider_blue.value()
        self.led_tab.set_led_color_slider_value(self.led_slider_color)
        self.led_brightness = self.led_tab.led_brightness_slider.value()
        self.led_tab.set_led_brightness_slider_value(self.led_brightness)
        led_config = [
            ('LED', 'mode', self.led_mode),
            ('LED', 'red_value', self.led_slider_color[0]),
            ('LED', 'green_value', self.led_slider_color[1]),
            ('LED', 'blue_value', self.led_slider_color[2]),
            ('LED', 'brightness', self.led_brightness)
        ]
        self.set_all_json_config(led_config)
        
    def led_save_params_event(self):
        """Handle save config button click event"""
        try:
            self.led_service_generator.restart_service_on_rpi()
            self.led_tab.set_save_button_enabled(False)
            time.sleep(1)
            self.led_tab.set_save_button_enabled(True)
        except:
            pass
    
    # FAN interface signals and slot functions
    def fan_radio_clicked_event(self):
        """Handle FAN mode switch event"""
        sender_button = self.sender()
        for i in range(len(self.fan_tab.fan_mode_radio_buttons_names)):
            if sender_button.text() == self.fan_tab.fan_mode_radio_buttons_names[i]:
                self.fan_mode = i
        self.fan_tab.set_fan_mode(self.fan_mode)
        self.fan_temp_mode_threshold[0] = int(self.fan_tab.fan_case_low_temp_input.text())
        self.fan_temp_mode_threshold[1] = int(self.fan_tab.fan_case_high_temp_input.text())
        self.fan_temp_mode_threshold[2] = int(self.fan_tab.fan_case_temp_schmitt_input.text())
        self.fan_temp_mode_duty[0] = int(self.fan_tab.fan_case_low_speed_slider.value())
        self.fan_temp_mode_duty[1] = int(self.fan_tab.fan_case_high_speed_slider.value())
        temp_mode_config = {
            'fan_temp_threshold_low': self.fan_temp_mode_threshold[0],
            'fan_temp_threshold_high': self.fan_temp_mode_threshold[1],
            'fan_temp_threshold_hyst': self.fan_temp_mode_threshold[2],
            'fan_temp_mode_duty_low': self.fan_temp_mode_duty[0],
            'fan_temp_mode_duty_high': self.fan_temp_mode_duty[1]
        }
        self.fan_manual_mode_duty = int(self.fan_tab.fan_manual_slider.value())
        fan_config = [
            ('Fan', 'mode', self.fan_mode),
            ('Fan', 'manual_mode_duty', self.fan_manual_mode_duty),
            ('Fan', 'temp_mode_config', temp_mode_config)
        ]
        self.set_all_json_config(fan_config)
        
    def fan_config_change_event(self):
        self.fan_temp_mode_threshold[0] = int(self.fan_tab.fan_case_low_temp_input.text())
        self.fan_temp_mode_threshold[1] = int(self.fan_tab.fan_case_high_temp_input.text())
        self.fan_temp_mode_threshold[2] = int(self.fan_tab.fan_case_temp_schmitt_input.text())
        self.fan_temp_mode_duty[0] = int(self.fan_tab.fan_case_low_speed_slider.value())
        self.fan_temp_mode_duty[1] = int(self.fan_tab.fan_case_high_speed_slider.value())
        self.fan_manual_mode_duty = int(self.fan_tab.fan_manual_slider.value())

        temp_config = {
            'fan_temp_threshold_low': self.fan_temp_mode_threshold[0],
            'fan_temp_threshold_high': self.fan_temp_mode_threshold[1],
            'fan_temp_threshold_hyst': self.fan_temp_mode_threshold[2],
            'fan_temp_mode_duty_low': self.fan_temp_mode_duty[0],
            'fan_temp_mode_duty_high': self.fan_temp_mode_duty[1]
         }
        fan_config = [
            ('Fan', 'mode', self.fan_mode),
            ('Fan', 'manual_mode_duty', self.fan_manual_mode_duty),
            ('Fan', 'temp_mode_config', temp_config)
        ]
        self.set_all_json_config(fan_config)
        
    def fan_save_params_event(self):
        """Handle save config button click event"""
        try:
            self.fan_service_generator.restart_service_on_rpi()
            self.fan_tab.set_save_button_enabled(False)
            time.sleep(1)
            self.fan_tab.set_save_button_enabled(True)
        except:
            pass

    def get_all_json_config(self):
        config_manager = ConfigManager()
        return config_manager.get_all_config()
        
    def set_all_json_config(self, config_data):
        config_manager = ConfigManager()
        for section, key, value in config_data:
            config_manager.set_value(section, key, value)
        config_manager.save_config()
        
    def closeEvent(self, event):
        """Handle window close event"""
        if self.is_show_monitor_ui and self.monitor_update_data_timer_is_running:  # If timer is running, stop timer and save config
            self.monitor_update_data_timer.stop()
            self.monitor_update_data_timer_is_running = False
        try:
            self.led_service_generator.restart_service_on_rpi()
            if self.led_mode == 8:
                time.sleep(0.5)
                self.led_service_generator.stop_service_on_rpi()
                
            self.fan_service_generator.restart_service_on_rpi()
            if self.fan_mode == 2:
                time.sleep(0.5)
                self.fan_service_generator.stop_service_on_rpi()
        except:
            pass
        os.system('sudo rm __pycache__ -rf')
        event.accept()
        
    def keyPressEvent(self, event):
        """Handle keyboard key press events"""
        # Check if Ctrl+C is pressed
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.close()  # Trigger window close
        else:
            super().keyPressEvent(event)  # Call parent class keyboard event handler


if __name__ == "__main__":
    os.system('sudo chmod 700 /run/user/1000')
    app = QApplication(sys.argv)
    screens = app.screens()
    dsi_screen = None
    for screen in screens:
        if "DSI" in screen.name().upper():
            dsi_screen = screen
            break
    window = MainWindow()
    window.show()
    if dsi_screen:
        window.move(dsi_screen.geometry().topLeft()) 
    sys.exit(app.exec_())