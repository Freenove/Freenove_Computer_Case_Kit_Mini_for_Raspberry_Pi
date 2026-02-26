import time
import sys

class FAN_TASK:

    def __init__(self, config):
        self.pi_fan_mode = config.get('mode', 1)  # 0: manual, 1: temp, 2: code
        self.pi_fan_manual_mode_duty = config.get('manual_mode_duty', 255)  # 0-255
        self.pi_fan_temp_mode_threshold = config.get('temp_mode_config', {
            "fan_temp_threshold_low": 45,
            "fan_temp_threshold_high": 80,
            "fan_temp_threshold_hyst": 3,
            "fan_temp_mode_duty_low": 50,
            "fan_temp_mode_duty_high": 200
        })
        # Speed array for each effect, index corresponds to mode number
        speed = [1.0, 2.0, 1.0]  # Manual, Temp, Code mode sleep times
        while len(speed) < 3:
            speed.append(0.1)
        self.pi_fan_speed = speed
        
        try:
            from api_systemInfo import SystemInformation
            self.system_information = SystemInformation()
            if self.system_information.get_cpu_thermal_control() == 1:
                self.system_information.set_cpu_thermal_control(0)
            self.system_information.set_pi_pwm_enable(1)
            self.system_information.set_pi_pwm_duty(0)   
        except Exception as e:
            print(f"Fan initialization failed: {e}")
            sys.exit(1)
    
    def _calculate_linear_duty(self, current_temp, low_threshold, high_threshold, min_duty, max_duty):
        temp_range = high_threshold - low_threshold
        duty_range = max_duty - min_duty
        temp_position = current_temp - low_threshold
        duty = int((temp_position / temp_range) * duty_range + min_duty)
        return max(min_duty, min(max_duty, duty))
    
    def fan_run_temp_mode(self):
        try:
            while True:
                if self.pi_fan_mode != 0:
                    return  # Exit if mode changed
                    
                if self.system_information.get_cpu_thermal_control() == 1:
                    self.system_information.set_cpu_thermal_control(0)
                    self.system_information.set_pi_pwm_enable(1)
                current_temp = round(self.system_information.get_raspberry_pi_cpu_temperature(), 2)

                low_temp = self.pi_fan_temp_mode_threshold["fan_temp_threshold_low"]      # 45°C
                high_temp = self.pi_fan_temp_mode_threshold["fan_temp_threshold_high"]    # 80°C
                hysteresis = self.pi_fan_temp_mode_threshold["fan_temp_threshold_hyst"]  # 3°C
                low_temp_duty = self.pi_fan_temp_mode_threshold["fan_temp_mode_duty_low"]     # 50
                high_temp_duty = self.pi_fan_temp_mode_threshold["fan_temp_mode_duty_high"]   # 200
                
                # Calculate hysteresis thresholds
                low_temp_off = low_temp - hysteresis    # 45 - 3 = 42°C (fan off temperature)
                high_temp_off = high_temp - hysteresis  # 80 - 3 = 77°C (temperature to return to linear control from full speed)
                
                current_duty = self.system_information.get_raspberry_pi_fan_duty()
                
                # Determine duty based on temperature and current state
                if current_duty == 0 and current_temp >= low_temp:
                    # Turn on fan and enter linear control range
                    duty = self._calculate_linear_duty(current_temp, low_temp, high_temp, low_temp_duty, high_temp_duty)
                    self.system_information.set_pi_pwm_duty(duty)
                elif current_temp >= high_temp:
                    # Keep fan at maximum speed 255
                    self.system_information.set_pi_pwm_duty(255)
                elif current_duty == 255 and current_temp <= high_temp_off:
                    # Enter linear control range from full speed
                    duty = self._calculate_linear_duty(current_temp, low_temp, high_temp, low_temp_duty, high_temp_duty)
                    self.system_information.set_pi_pwm_duty(duty)
                elif current_duty > 0 and current_temp <= low_temp_off:
                    # Turn off fan
                    self.system_information.set_pi_pwm_duty(0)
                elif low_temp < current_temp < high_temp:
                    # Linear control range: adjust speed proportionally
                    duty = self._calculate_linear_duty(current_temp, low_temp, high_temp, low_temp_duty, high_temp_duty)
                    self.system_information.set_pi_pwm_duty(duty)
                elif low_temp_off < current_temp < low_temp and current_duty > 0:
                    # Keep minimum speed when between thresholds
                    self.system_information.set_pi_pwm_duty(low_temp_duty)
                
                # Sleep based on configured speed
                time.sleep(self.pi_fan_speed[0])
        except Exception as e:
            print(f"Error in temp mode: {e}")
    
    def fan_run_manual_mode(self):
        try:
            # Continuous loop until mode changes
            while True:
                if self.pi_fan_mode != 1:
                    return  # Exit if mode changed
                if self.system_information.get_cpu_thermal_control() == 1:
                    self.system_information.set_cpu_thermal_control(0)
                    self.system_information.set_pi_pwm_enable(1)
                self.system_information.set_pi_pwm_duty(self.pi_fan_manual_mode_duty)
                time.sleep(self.pi_fan_speed[1])  # Sleep based on configured speed
        except Exception as e:
            print(f"Error in manual mode: {e}")
    
    def fan_run_original_mode(self):
        try:
            while True:
                if self.pi_fan_mode != 2:
                    return  # Exit if mode changed
                if self.system_information.get_cpu_thermal_control() == 0:
                    self.system_information.set_cpu_thermal_control(1)
                    self.system_information.set_pi_pwm_enable(1)
                time.sleep(self.pi_fan_speed[2])
        except Exception as e:
            print(f"Error in original mode: {e}")

    def run_fan_loop(self):
        # Create mode function mapping
        mode_functions = {
            0: self.fan_run_temp_mode,      # Temperature
            1: self.fan_run_manual_mode,    # Manual
            2: self.fan_run_original_mode   # Code
        }
        
        last_check_time = time.time()
        check_interval = 2.0

        while True:
            current_time = time.time()
            if current_time - last_check_time >= check_interval:
                # Get corresponding function and execute
                mode_func = mode_functions.get(self.pi_fan_mode, self.fan_run_original_mode)
                if mode_func:
                    try:
                        # Execute mode function
                        mode_func()
                    except Exception as e:
                        print(f"Error in fan mode function: {e}")
            time.sleep(0.1)
    
    def stop(self):
        self.system_information.set_pi_pwm_duty(0)
        self.system_information.set_pi_pwm_enable(1)
        self.system_information.set_cpu_thermal_control(1)
        sys.exit(0)
        

if __name__ == "__main__":
    import argparse
    from api_json import ConfigManager
    
    parser = argparse.ArgumentParser(description='Fan Task Controller')
    parser.add_argument('mode', nargs='?', type=int, help='Fan mode (0-2)')
    parser.add_argument('--config-file', default='app_config.json', help='Path to config file')
    args = parser.parse_args()
    
    config_manager = ConfigManager(args.config_file)
    fan_config = config_manager.get_section('Fan')
    
    if args.mode is not None:
        if 0 <= args.mode <= 2:
            fan_config['mode'] = args.mode
            print(f"Setting Fan mode to: {args.mode}")
        else:
            print("Error: Mode must be between 0 and 2")
            sys.exit(1)
    
    fan_task = FAN_TASK(fan_config)

    try:
        fan_task.run_fan_loop()
    except KeyboardInterrupt:
        print("Stopping fan task...")
    finally:
        fan_task.stop()