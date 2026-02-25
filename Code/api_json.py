# api_json.py
import json
import os
import fcntl
import threading
import time

class ConfigManager:
    def __init__(self, config_file='app_config.json'):
        """
        Initialize configuration manager
        """
        self.config_file = config_file
        self.config_data = {}
        self.lock = threading.Lock() 
        self.load_config()

    def load_config(self):
        """
        Load configuration data from JSON file with file locking
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    try:
                        fcntl.flock(f.fileno(), fcntl.LOCK_SH)  
                        content = f.read().strip()
                        if content:  
                            self.config_data = json.loads(content)
                        else:  
                            print(f"Config file {self.config_file} is empty, creating default config")
                            self.create_config_file()
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN) 
            else:
                self.create_config_file()
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {self.config_file}: {e}")
            print("Creating default configuration...")
            self.create_config_file()
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            self.create_config_file()
            self.config_data = {}

    def save_config(self):
        try:
            directory = os.path.dirname(self.config_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
                
            temp_file = self.config_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)  
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            os.rename(temp_file, self.config_file)
        except Exception as e:
            print(f"Error saving configuration file: {e}")

    def get_value(self, section, key):
        """
        Get configuration value
        
        Args:
            section (str): Configuration section name
            key (str): Configuration item name
            
        Returns:
            Configuration item value
        """
        return self.config_data.get(section, {}).get(key, None)
    
    def set_value(self, section, key, value):
        """
        Set configuration value
        
        Args:
            section (str): Configuration section name
            key (str): Configuration item name
            value: Value to set
        """
        with self.lock: 
            if section not in self.config_data:
                self.config_data[section] = {}
            self.config_data[section][key] = value
    
    def get_section(self, section):
        """
        Get entire configuration section
        
        Args:
            section (str): Configuration section name
            
        Returns:
            dict: Configuration section data
        """
        return self.config_data.get(section, {})
    
    def set_section(self, section, data):
        """
        Set entire configuration section
        
        Args:
            section (str): Configuration section name
            data (dict): Data to set
        """
        self.config_data[section] = data
    
    def get_all_config(self):
        """
        Get all configuration data
        
        Returns:
            dict: All configuration data
        """
        return self.config_data
    
    def set_all_config(self, config_data):
        """
        Set all configuration data
        
        Args:
            config_data (dict): All configuration data
        """
        self.config_data = config_data
 
    def delete_config_file(self):
        """ Delete configuration file """
        try:
            os.remove(self.config_file)
        except Exception as e:
            print(f"Error deleting configuration file: {e}")

    def create_config_file(self):
        # Initialize default values based on actual usage in app_ui.py
        led_mode_default = 6
        fan_mode_default = 2
        try:
            if not os.path.exists(self.config_file):
                self.config_data = {
                    "Monitor": {
                        "screen_orientation": 0
                    },
                    "LED": {
                        "mode": led_mode_default,
                        "red_value": 0,
                        "green_value": 0,
                        "blue_value": 255,
                        "brightness": 255
                    },
                    "Fan": {
                        "mode": fan_mode_default,
                        "manual_mode_duty": 255,
                        "temp_mode_config": {
                            "fan_temp_threshold_low": 45,
                            "fan_temp_threshold_high": 80,
                            "fan_temp_threshold_hyst": 3,
                            "fan_temp_mode_duty_low": 50,
                            "fan_temp_mode_duty_high": 200
                        }
                    }
                }
                self.save_config()
            else:
                print(f"Configuration file already exists: {self.config_file}")
        except Exception as e:
            print(f"Error creating configuration file: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()

    def end(self):
        """End method to clean up resources"""
        pass


if __name__ == '__main__':
    # Create configuration manager instance (automatically loads configuration file)
    config_manager = ConfigManager('app_config.json')

    print("=== Configuration Manager Test ===")

    all_config = config_manager.get_all_config()
    print(f"All config: {all_config}")
    print()

    led_mode = config_manager.get_value('LED', 'mode')
    print(f"LED Mode: {led_mode}")
    
    fan_mode = config_manager.get_value('Fan', 'mode')
    print(f"Fan Mode: {fan_mode}")
    print()

    led_config = config_manager.get_section('LED')
    print(f"LED config: {led_config}")
    
    fan_config = config_manager.get_section('Fan')
    print(f"Fan config: {fan_config}")
    print()

    print("Testing configuration modification...")
    config_manager.set_value('LED', 'mode', 6)
    config_manager.set_value('LED', 'brightness', 255)
    config_manager.set_value('LED', 'red_value', 0)
    config_manager.set_value('LED', 'green_value', 0)
    config_manager.set_value('LED', 'blue_value', 255)
    
    config_manager.set_value('Fan', 'mode', 2)
    config_manager.set_value('Fan', 'manual_mode_duty', 255)
    print("Configuration updated in memory.")
    print()

    print("Saving configuration to file...")
    config_manager.save_config()
    print("Configuration saved successfully.")
    print()

    print("Reloading configuration from file...")
    config_manager.load_config()
    updated_config = config_manager.get_all_config()
    print(f"Updated config: {updated_config}")
    print()

    print("Verification:")
    print(f"New LED mode: {config_manager.get_value('LED', 'mode')}")
    print(f"New LED brightness: {config_manager.get_value('LED', 'brightness')}")
    print(f"New Fan mode: {config_manager.get_value('Fan', 'mode')}")
    print(f"New Fan duty: {config_manager.get_value('Fan', 'manual_mode_duty')}")
    print()

    print("Test completed successfully!")
