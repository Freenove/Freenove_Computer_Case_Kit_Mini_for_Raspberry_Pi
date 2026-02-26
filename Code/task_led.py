import time
import sys

class LED_TASK:
    def __init__(self, config):
        self.pi_led_mode = config.get('mode', 6)
        self.pi_led_brightness = config.get('brightness', 255)
        self.pi_led_color = (
            config.get('red_value', 0),
            config.get('green_value', 0),
            config.get('blue_value', 255)
        )
        speed = [0.3, 0.1, 0.1, 0.1, 0.015, 0.05, 0.05, 0.3, 1.0, 0.1]
        while len(speed) < 10:
            speed.append(0.1)
        self.pi_led_speed = speed
        
        try:
            from api_ws2812 import WS2812
            self.led_strip = WS2812(led_pin=26, led_count=6, order="GRB")
            self.led_strip.setBrightness(self.pi_led_brightness)
        except Exception as e:
            print(f"LED initialization failed: {e}")
            sys.exit(1)

    def led_run_blink_mode(self):
        state = 0
        while True:
            if self.pi_led_mode != 0:
                return  # Exit if mode changed
            ledNum = self.led_strip.numPixels()
            for i in range(ledNum):
                if state == 0:
                    self.led_strip.setPixelColor(i, self.pi_led_color)
                else:
                    self.led_strip.setPixelColor(i, (0, 0, 0))
            self.led_strip.show()
            state = 1 - state 
            time.sleep(self.pi_led_speed[0])
    
    def led_run_rotate_mode(self):
        step = 0
        while True:
            if self.pi_led_mode != 1:
                return  # Exit if mode changed
            ledNum = self.led_strip.numPixels()
            step = step % ledNum
            for i in range(ledNum):
                self.led_strip.setPixelColor(i, (0, 0, 0))
            idx1 = step % ledNum
            self.led_strip.setPixelColor(idx1, self.pi_led_color)
            self.led_strip.show()
            step += 1
            time.sleep(self.pi_led_speed[1])

    def led_run_rotate_quad_mode(self):
        step = 0
        while True:
            if self.pi_led_mode != 2:
                return  # Exit if mode changed
            ledNum = self.led_strip.numPixels()
            step = step % ledNum
            for i in range(ledNum):
                self.led_strip.setPixelColor(i, (0, 0, 0))
            idx1 = step % ledNum
            idx2 = (step + ledNum // 2) % ledNum
            self.led_strip.setPixelColor(idx1, self.pi_led_color)
            self.led_strip.setPixelColor(idx2, self.pi_led_color)
            self.led_strip.show()
            step += 1
            time.sleep(self.pi_led_speed[2])

    def led_run_following_mode(self):
        step = 0
        while True:
            if self.pi_led_mode != 3:
                return  # Exit if mode changed
            ledNum = self.led_strip.numPixels()
            step = step % ledNum
            for i in range(ledNum):
                self.led_strip.setPixelColor(i, (0, 0, 0))
            for j in range(4):
                idx = (step + j * (ledNum // 4)) % ledNum
                self.led_strip.setPixelColor(idx, self.pi_led_color)
            self.led_strip.show()
            step += 1
            time.sleep(self.pi_led_speed[3])

    def led_run_breathing_mode(self):
        step = 0
        direction = 1
        while True:
            if self.pi_led_mode != 4:
                return  # Exit if mode changed
            for i in range(self.led_strip.numPixels()):
                self.led_strip.setPixelColor(i, self.pi_led_color)
            self.led_strip.setBrightness(int(self.pi_led_brightness * (step / 150)))
            self.led_strip.show()
            if direction == 1:
                if step < 150:
                    step += 1
                else:
                    direction = -1
            else:
                if step > 0:
                    step -= 1
                else:
                    direction = 1
            time.sleep(self.pi_led_speed[4])
    
    def led_run_gradual_mode(self):
        step = 0
        while True:
            if self.pi_led_mode != 5:
                return  # Exit if mode changed
            for i in range(self.led_strip.numPixels()):
                color = self.led_strip.wheel((i + step) % 255)
                self.led_strip.setPixelColor(i, color)
            self.led_strip.show()
            step = (step + 1) % 256
            time.sleep(self.pi_led_speed[5])
    
    def led_run_rainbow_mode(self):
        step = 0
        led_count = self.led_strip.numPixels()
        while True:
            if self.pi_led_mode != 6:
                return  # Exit if mode changed
            colors = []
            for i in range(led_count):
                j = (int(i * 256 / led_count) + step) % 255
                colors.append(self.led_strip.wheel(j))
            
            for i, color in enumerate(colors):
                self.led_strip.setPixelColor(i, color)
            self.led_strip.show()
            step = (step + 1) % 256
            time.sleep(self.pi_led_speed[6])

    def led_run_code_mode(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
        while True:
            if self.pi_led_mode != 7:
                return  # Exit if mode changed
            for color in colors:
                if self.pi_led_mode != 7:
                    return  # Exit if mode changed
                for i in range(self.led_strip.numPixels()):
                    self.led_strip.setPixelColor(i, color)
                self.led_strip.show()
                time.sleep(self.pi_led_speed[7])

    def led_run_close_mode(self):
        while True:
            if self.pi_led_mode != 8:
                return  # Exit if mode changed
            self.led_strip.clear()
            time.sleep(self.pi_led_speed[7])

    def run_led_loop(self):
        mode_functions = {
            0: self.led_run_blink_mode,
            1: self.led_run_rotate_mode,
            2: self.led_run_rotate_quad_mode,
            3: self.led_run_following_mode,
            4: self.led_run_breathing_mode,
            5: self.led_run_gradual_mode,
            6: self.led_run_rainbow_mode,
            7: self.led_run_code_mode,
            8: self.led_run_close_mode
        }

        while True:
            mode_func = mode_functions.get(self.pi_led_mode, self.led_run_close_mode)
            if mode_func:
                mode_func()

    def stop(self):
        self.led_strip.clear()
        time.sleep(0.1)
        self.led_strip.deinit()
        time.sleep(0.1)
        sys.exit(0)


if __name__ == "__main__":
    import argparse
    from api_json import ConfigManager
    
    parser = argparse.ArgumentParser(description='LED Task Controller')
    parser.add_argument('mode', nargs='?', type=int, help='LED mode (0-9)')
    parser.add_argument('--config-file', default='app_config.json', help='Path to config file')
    args = parser.parse_args()
    
    config_manager = ConfigManager(args.config_file)
    led_config = config_manager.get_section('LED')
    
    if args.mode is not None:
        if 0 <= args.mode <= 9:
            led_config['mode'] = args.mode
            print(f"Setting LED mode to: {args.mode}")
        else:
            print("Error: Mode must be between 0 and 9")
            sys.exit(1)
    
    led_task = LED_TASK(led_config)
    
    try:
        led_task.run_led_loop()
    except KeyboardInterrupt:
        print("LED Task stopped")
    finally:
        led_task.stop()