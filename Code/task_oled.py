from api_oled import OLED
from api_systemInfo import SystemInformation
from api_json import ConfigManager
import signal
import time
import sys
import argparse

class OLED_TASK:
    def __init__(self, config):
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        # Initialize OLED and Expansion objects
        self.oled = None
        self.font_size = 12
        self.cleanup_done = False
        
        # Store config values passed from outside
        screen1_config = config.get('screen1', {})
        screen2_config = config.get('screen2', {})
        screen3_config = config.get('screen3', {})
        screen4_config = config.get('screen4', {})
        
        self.screen1_data_format = screen1_config.get('data_format', 0)
        self.screen1_time_format = screen1_config.get('time_format', 0)
        self.screen2_interchange = screen2_config.get('interchange', 0)
        self.screen3_interchange = screen3_config.get('interchange', 0)
        self.screen4_interchange = screen4_config.get('interchange', 0)
        
        # Store display timing configs
        self.screen1_duration = screen1_config.get('display_time', 3.0)
        self.screen2_duration = screen2_config.get('display_time', 3.0)
        self.screen3_duration = screen3_config.get('display_time', 3.0)
        self.screen4_duration = screen4_config.get('display_time', 3.0)
        
        self.screen1_is_run_on_oled = screen1_config.get('is_run_on_oled', True)
        self.screen2_is_run_on_oled = screen2_config.get('is_run_on_oled', True)
        self.screen3_is_run_on_oled = screen3_config.get('is_run_on_oled', True)
        self.screen4_is_run_on_oled = screen4_config.get('is_run_on_oled', True)

        # Cache hwmon path lookup for performance
        self._fan_pwm_path = None

        try:
            self.oled = OLED(rotate_angle=180)
        except Exception as e:
            print(f"OLED initialization failed: {e}")
            sys.exit(1)

        try:
            self.system_information = SystemInformation()
        except Exception as e:
            print(f"System information initialization failed: {e}")
            sys.exit(1)

    def signal_handler(self, signum, frame):
        self.stop()

    def format_date(self, date_str):
        """Format date based on data_format configuration"""
        # Split the date string (assuming it's in Year-Month-Day format)
        year, month, day = date_str.split('-')
        if self.screen1_data_format == 0:  # Year-Month-Day
            return f"{year}-{month}-{day}"
        elif self.screen1_data_format == 1:  # Month-Day-Year
            return f"{month}-{day}-{year}"
        elif self.screen1_data_format == 2:  # Day-Month-Year
            return f"{day}-{month}-{year}"
        else:  # Default to Year-Month-Day
            return f"{year}-{month}-{day}"

    def format_time(self, time_str):
        """Format time based on time_format configuration"""
        # For simplicity, assume time_str is in HH:MM:SS format
        if self.screen1_time_format == 0:  # HH:MM:SS
            return time_str  # Return full time
        elif self.screen1_time_format == 1:  # 12-hour format
            # Convert 24-hour to 12-hour format
            hour, minute, second = time_str.split(':')
            hour = int(hour)
            am_pm = "AM" if hour < 12 else "PM"
            if hour == 0:
                hour = 12
            elif hour > 12:
                hour -= 12
            return f"{am_pm} {hour}:{minute}:{second}"
        else:  # Default to # HH:MM:SS
            return time_str

    def oled_ui_1_show(self, date, weekday, time):
        self.oled.clear()

        # Draw a large box, same size as screen, no fill, then draw 2 horizontal lines, dividing into 3 rows
        self.oled.draw_rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline="white")
        self.oled.draw_line(((0, 16), (self.oled.width-1, 16)), fill="white")
        self.oled.draw_line(((0, 48), (self.oled.width-1, 48)), fill="white")
        
        # Format date and time according to configuration
        formatted_date = self.format_date(date)
        formatted_time = self.format_time(time)

        # First row writes date, second row writes time, third row writes weekday
        self.oled.draw_text(formatted_date, position=((0,0),(128,16)), directory="center", offset=(0, 1), font_size=self.font_size)
        if self.screen1_time_format == 1:
            self.oled.draw_text(formatted_time, position=((0,16),(128,48)), directory="center", offset=(0, 5), font_size=18)
        else:
            self.oled.draw_text(formatted_time, position=((0,16),(128,48)), directory="center", offset=(0, 2), font_size=24)
        self.oled.draw_text(weekday, position=((0,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.show()

    def oled_ui_2_show(self, ip_address, cpu_usage, memory_usage, disk_usage):
        self.oled.clear()

        # Draw basic interface outline
        self.oled.draw_rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline="white")
        self.oled.draw_line(((0, 16), (self.oled.width-1, 16)), fill="white")
        self.oled.draw_line(((43,16),(43, self.oled.height-1)), fill="white")
        self.oled.draw_line(((86,16),(86, self.oled.height-1)), fill="white")

        # Write Raspberry Pi IP address in first row
        self.oled.draw_text("IP:"+ip_address, position=((0,0),(128,16)),  directory="center", offset=(0, 0), font_size=self.font_size)

        # Use stored config value
        self.screen2_interchange = self.screen2_interchange

        # Define positions based on interchange setting
        if self.screen2_interchange == 1:
            # Order: CPU, DISK, MEM
            cpu_pos = ((0,16),(42,32))
            mem_pos = ((87,16),(128,32))
            disk_pos = ((43,16),(86,32))
            cpu_circle_pos = (21,46)
            mem_circle_pos = (107,46)
            disk_circle_pos = (64,46)
        elif self.screen2_interchange == 2:
            # Order: MEM, CPU, DISK
            cpu_pos = ((43,16),(86,32))
            mem_pos = ((0,16),(42,32))
            disk_pos = ((87,16),(128,32))
            cpu_circle_pos = (64,46)
            mem_circle_pos = (21,46)
            disk_circle_pos = (107,46)
        elif self.screen2_interchange == 3:
            # Order: DISK, CPU, MEM
            cpu_pos = ((43,16),(86,32))
            mem_pos = ((87,16),(128,32))
            disk_pos = ((0,16),(42,32))
            cpu_circle_pos = (64,46)
            mem_circle_pos = (107,46)
            disk_circle_pos = (21,46)
        elif self.screen2_interchange == 4:
            # Order: MEM, DISK, CPU
            cpu_pos = ((87,16),(128,32))
            mem_pos = ((0,16),(42,32))
            disk_pos = ((43,16),(86,32))
            cpu_circle_pos = (107,46)
            mem_circle_pos = (21,46)
            disk_circle_pos = (64,46)
        elif self.screen2_interchange == 5:
            # Order: DISK, MEM, CPU
            cpu_pos = ((87,16),(128,32))
            mem_pos = ((43,16),(86,32))
            disk_pos = ((0,16),(42,32))
            cpu_circle_pos = (107,46)
            mem_circle_pos = (64,46)
            disk_circle_pos = (21,46)
        else:
            # Default: CPU, MEM, DISK
            cpu_pos = ((0,16),(42,32))
            mem_pos = ((43,16),(86,32))
            disk_pos = ((87,16),(128,32))
            cpu_circle_pos = (21,46)
            mem_circle_pos = (64,46)
            disk_circle_pos = (107,46)
        
        # Draw text labels in specified positions
        self.oled.draw_text("CPU",  position=cpu_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("MEM",  position=mem_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.draw_text("DISK", position=disk_pos, directory="center", offset=(0, 0), font_size=self.font_size)
        
        # Draw percentage circles in corresponding positions
        self.oled.draw_circle_with_percentage(cpu_circle_pos, 16, cpu_usage, outline="white", fill="white")
        self.oled.draw_circle_with_percentage(mem_circle_pos, 16, memory_usage, outline="white", fill="white")
        self.oled.draw_circle_with_percentage(disk_circle_pos, 16, disk_usage, outline="white", fill="white")
        self.oled.show()
    
    def oled_ui_3_show(self, pi_temperature, pi_duty):
        self.oled.clear()

        # Draw basic interface outline
        self.oled.draw_rectangle((0, 0, self.oled.width-1, self.oled.height-1), outline="white")
        self.oled.draw_line(((64, 0), (64, self.oled.height-1)), fill="white")

        # Use stored config value
        self.screen3_interchange = self.screen3_interchange

        if self.screen3_interchange == 1:
            # First row first column shows Duty, first row second column shows Temp
            self.oled.draw_text("Duty", position=((0,0),(64,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            self.oled.draw_text("Temp", position=((65,0),(128,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            # Draw a dial in the center of each column of the second row
            self.oled.draw_dial(center_xy=(32,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=pi_duty, start_value=0, end_value=100)
            self.oled.draw_dial(center_xy=(96,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=pi_temperature, start_value=0, end_value=100)
            # First row first column shows Duty, first row second column shows Temp
            self.oled.draw_text("{}%".format(int(pi_duty*100/255)), position=((0,48),(64,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            self.oled.draw_text("{}℃".format(round(pi_temperature)), position=((65,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
        else:
            # First row first column shows Temp, first row second column shows Duty
            self.oled.draw_text("Temp", position=((0,0),(64,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            self.oled.draw_text("Duty", position=((65,0),(128,16)), directory="center", offset=(0, 0), font_size=self.font_size)
            # Draw a dial in the center of each column of the second row
            self.oled.draw_dial(center_xy=(32,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=pi_temperature, start_value=0, end_value=100)
            self.oled.draw_dial(center_xy=(96,34), radius=16, angle=(225, 315), directory="CW", tick_count=10, percentage=pi_duty, start_value=0, end_value=100)
            # First row first column shows Temp, first row second column shows Duty
            self.oled.draw_text("{}℃".format(round(pi_temperature)), position=((0,48),(64,64)), directory="center", offset=(0, 0), font_size=self.font_size)
            self.oled.draw_text("{}%".format(int(pi_duty*100/255)), position=((65,48),(128,64)), directory="center", offset=(0, 0), font_size=self.font_size)
        self.oled.show()

    def run_oled_loop(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        screen_start_time = time.time()  # Record the start time of current screen
        current_screen = 0  # Current screen index
        
        while True:
            # Update data every 0.3 seconds
            current_date = self.system_information.get_raspberry_pi_date()
            current_weekday = self.system_information.get_raspberry_pi_weekday()
            current_time = self.system_information.get_raspberry_pi_time()

            ip_address = self.system_information.get_raspberry_pi_ip_address()
            cpu_usage = self.system_information.get_raspberry_pi_cpu_usage()
            memory_usage = self.system_information.get_raspberry_pi_memory_usage()
            disk_usage = self.system_information.get_raspberry_pi_disk_usage()

            cpu_temperature = self.system_information.get_raspberry_pi_cpu_temperature()
            current_pi_duty = self.system_information.get_raspberry_pi_fan_duty()
            
            # Determine which screens need to be displayed according to stored configuration
            active_screens = []
            screen_durations = []
            screen_functions = []
            
            if self.screen1_is_run_on_oled:
                active_screens.append(0)
                screen_durations.append(self.screen1_duration)
                screen_functions.append(lambda: self.oled_ui_1_show(current_date, current_weekday, current_time))
            
            if self.screen2_is_run_on_oled:
                active_screens.append(1)
                screen_durations.append(self.screen2_duration)
                screen_functions.append(lambda: self.oled_ui_2_show(ip_address, cpu_usage, memory_usage[0], disk_usage[0]))
            
            if self.screen3_is_run_on_oled:
                active_screens.append(2)
                screen_durations.append(self.screen3_duration)
                # Call modified oled_ui_3_show, passing temperature and PI fan duty
                screen_functions.append(lambda: self.oled_ui_3_show(cpu_temperature, current_pi_duty))
            
            # Skip if no active screens
            if not active_screens:
                time.sleep(0.3)
                continue
            
            # Get the current active screen index
            current_active_index = current_screen % len(active_screens)
            
            # Check if screen needs to be switched (based on time instead of counter)
            elapsed_time = time.time() - screen_start_time
            if elapsed_time >= screen_durations[current_active_index]:
                current_screen = (current_screen + 1) % len(active_screens)
                current_active_index = current_screen % len(active_screens)
                screen_start_time = time.time()
            
            # Update OLED every 0.3 seconds
            try:
                # Use the function of current active screen
                screen_functions[current_active_index]()
            except Exception as e:
                print(f"Display error: {e}")
            
            time.sleep(0.3)  # Base interval of 0.3 second

    def stop(self):
        # Perform cleanup operations
        if self.cleanup_done:
            return
        self.cleanup_done = True
        try:
            if self.oled:
                self.oled.close()
        except Exception as e:
            print(e)
        time.sleep(0.1)
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OLED Task Controller')
    parser.add_argument('--config-file', default='app_config.json', help='Path to config file')
    args = parser.parse_args()
    
    config_manager = ConfigManager(args.config_file)
    oled_config = config_manager.get_section('OLED') or {}

    oled_task = OLED_TASK(oled_config)
    
    try:
        oled_task.run_oled_loop()
    except KeyboardInterrupt:
        print("OLED Task stopped")
    finally:
        oled_task.stop()