#!/usr/bin/env python3
"""
Example script to test motor and sensor modules
"""

import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.motor_control import MotorController, UltrasonicSensor
import logging

logging.basicConfig(level=logging.INFO)


def test_motor():
    """Test motor controller"""
    print("=== Testing Motor Controller ===\n")
    
    motor = MotorController(motor_pin=17, min_angle=0, max_angle=90)
    
    if not motor.initialize():
        print("Failed to initialize motor!")
        return
    
    print("Motor initialized!\n")
    
    # Test opening
    print("Opening lid...")
    motor.open_lid()
    print(f"Is open: {motor.is_open}")
    time.sleep(2)
    
    # Test closing
    print("\nClosing lid...")
    motor.close_lid()
    print(f"Is open: {motor.is_open}")
    time.sleep(2)
    
    # Cleanup
    motor.cleanup()
    print("\nMotor test completed!")


def test_sensor():
    """Test ultrasonic sensor"""
    print("\n=== Testing Ultrasonic Sensor ===\n")
    
    sensor = UltrasonicSensor(trigger_pin=23, echo_pin=24, threshold=30)
    
    if not sensor.initialize():
        print("Failed to initialize sensor!")
        return
    
    print("Sensor initialized!\n")
    print("Measuring distances (10 readings)...\n")
    
    for i in range(10):
        distance = sensor.measure_distance()
        if distance:
            print(f"Reading {i+1}: {distance:.2f} cm", end="")
            if sensor.is_object_detected():
                print(" - OBJECT DETECTED!")
            else:
                print()
        else:
            print(f"Reading {i+1}: Failed")
        
        time.sleep(0.5)
    
    print("\nSensor test completed!")


def main():
    """Run all tests"""
    print("=== Smart Trash Hardware Test ===\n")
    
    try:
        test_motor()
        test_sensor()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nError during test: {e}")


if __name__ == "__main__":
    main()
