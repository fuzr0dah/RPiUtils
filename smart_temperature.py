import argparse
import subprocess
import time

import RPi.GPIO as GPIO

parser = argparse.ArgumentParser(description='Auto control cooling for RPi')
parser.add_argument('--MAX_TEMP', default=55.0, type=float, help='This is value for MAX_TEMP variable')
parser.add_argument('--HYSTERESIS', default=15.0, type=float, help='This is value for hysteresis loop variable')

args = parser.parse_args()

CONTROL_PIN = 14  # Pin number to control cooler
MAX_TEMP = args.MAX_TEMP  # Max CPU temperature
HYSTERESIS = args.HYSTERESIS  # Max CPU temperature


def get_current_temp():
    """
    Function to get current CPU temperature from cmd

    :return CPU temperature in float
    """
    temp = subprocess.check_output('cat /sys/class/thermal/thermal_zone0/temp'.split()).decode()
    return float(temp) / 1000


def main():
    is_cooler_active = False  # Set cooler off

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN, GPIO.OUT, initial=0)  # Set OUTPUT mode for gpio pin

    while True:
        temp = get_current_temp()  # Get current temperature
        print(f'Temperature = {temp}')

        # Check if need turn on/off cooler
        if (temp > MAX_TEMP and not is_cooler_active) or (temp < MAX_TEMP - HYSTERESIS and is_cooler_active):
            is_cooler_active = not is_cooler_active
            GPIO.output(CONTROL_PIN, is_cooler_active)

        time.sleep(5)  # Sleep in 5 sec


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt detected. End program...')
    finally:
        GPIO.cleanup()
