"""
Motor Control Module
Handles automatic lid opening/closing using servo motor
"""

import time
import logging
from typing import Optional

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    logging.warning("RPi.GPIO not available. Motor control will be simulated.")
    GPIO_AVAILABLE = False


class MotorController:
    """
    Motor controller for lid operation
    """
    
    def __init__(self, motor_pin: int, min_angle: int = 0, max_angle: int = 90):
        """
        Initialize motor controller
        
        Args:
            motor_pin: GPIO pin for servo motor
            min_angle: Minimum angle (closed position)
            max_angle: Maximum angle (open position)
        """
        self.motor_pin = motor_pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.pwm = None
        self.is_open = False
        
    def initialize(self) -> bool:
        """
        Initialize GPIO and PWM
        
        Returns:
            True if successful, False otherwise
        """
        if not GPIO_AVAILABLE:
            logging.info("GPIO not available. Motor control simulated.")
            return True
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.motor_pin, GPIO.OUT)
            
            # Setup PWM at 50Hz for servo
            self.pwm = GPIO.PWM(self.motor_pin, 50)
            self.pwm.start(0)
            
            # Initialize to closed position
            self.close_lid()
            
            logging.info(f"Motor controller initialized on pin {self.motor_pin}")
            return True
            
        except Exception as e:
            logging.error(f"Motor initialization error: {e}")
            return False
    
    def _angle_to_duty_cycle(self, angle: int) -> float:
        """
        Convert angle to PWM duty cycle
        
        Args:
            angle: Servo angle (0-180)
            
        Returns:
            Duty cycle percentage
        """
        # Standard servo: 2.5% (0°) to 12.5% (180°)
        return 2.5 + (angle / 180.0) * 10.0
    
    def _set_angle(self, angle: int):
        """
        Set servo to specific angle
        
        Args:
            angle: Target angle
        """
        if not GPIO_AVAILABLE:
            logging.info(f"Simulated: Setting motor angle to {angle}°")
            return
        
        try:
            duty_cycle = self._angle_to_duty_cycle(angle)
            self.pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.5)  # Wait for servo to reach position
            self.pwm.ChangeDutyCycle(0)  # Stop sending signal
        except Exception as e:
            logging.error(f"Error setting angle: {e}")
    
    def open_lid(self):
        """Open the trash bin lid"""
        logging.info("Opening lid...")
        self._set_angle(self.max_angle)
        self.is_open = True
        logging.info("Lid opened")
    
    def close_lid(self):
        """Close the trash bin lid"""
        logging.info("Closing lid...")
        self._set_angle(self.min_angle)
        self.is_open = False
        logging.info("Lid closed")
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        if GPIO_AVAILABLE and self.pwm is not None:
            try:
                self.pwm.stop()
                GPIO.cleanup()
                logging.info("Motor controller cleaned up")
            except Exception as e:
                logging.error(f"Cleanup error: {e}")


class UltrasonicSensor:
    """
    Ultrasonic sensor for distance measurement
    """
    
    def __init__(self, trigger_pin: int, echo_pin: int, threshold: float = 30.0):
        """
        Initialize ultrasonic sensor
        
        Args:
            trigger_pin: GPIO pin for trigger
            echo_pin: GPIO pin for echo
            threshold: Distance threshold in cm for object detection
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.threshold = threshold
    
    def initialize(self) -> bool:
        """
        Initialize GPIO pins
        
        Returns:
            True if successful, False otherwise
        """
        if not GPIO_AVAILABLE:
            logging.info("GPIO not available. Ultrasonic sensor simulated.")
            return True
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.trigger_pin, GPIO.OUT)
            GPIO.setup(self.echo_pin, GPIO.IN)
            
            # Ensure trigger is low
            GPIO.output(self.trigger_pin, False)
            time.sleep(0.1)
            
            logging.info(f"Ultrasonic sensor initialized (trigger: {self.trigger_pin}, echo: {self.echo_pin})")
            return True
            
        except Exception as e:
            logging.error(f"Ultrasonic sensor initialization error: {e}")
            return False
    
    def measure_distance(self) -> Optional[float]:
        """
        Measure distance in centimeters
        
        Returns:
            Distance in cm or None if failed
        """
        if not GPIO_AVAILABLE:
            # Simulate random distance
            import random
            distance = random.uniform(10, 50)
            logging.debug(f"Simulated distance: {distance:.2f} cm")
            return distance
        
        try:
            # Send 10μs pulse
            GPIO.output(self.trigger_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigger_pin, False)
            
            # Wait for echo
            timeout = time.time() + 0.1  # 100ms timeout
            pulse_start = time.time()
            while GPIO.input(self.echo_pin) == 0:
                pulse_start = time.time()
                if time.time() > timeout:
                    return None
            
            pulse_end = time.time()
            while GPIO.input(self.echo_pin) == 1:
                pulse_end = time.time()
                if time.time() > timeout:
                    return None
            
            # Calculate distance
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150  # Speed of sound / 2
            distance = round(distance, 2)
            
            return distance
            
        except Exception as e:
            logging.error(f"Distance measurement error: {e}")
            return None
    
    def is_object_detected(self) -> bool:
        """
        Check if object is within threshold distance
        
        Returns:
            True if object detected, False otherwise
        """
        distance = self.measure_distance()
        if distance is not None:
            is_detected = distance < self.threshold
            if is_detected:
                logging.info(f"Object detected at {distance:.2f} cm")
            return is_detected
        return False
