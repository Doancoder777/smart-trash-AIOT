"""
Main Controller for Smart Trash AIOT System
Integrates image processing, voice recognition, and motor control
"""

import time
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.image_processing import ImageClassifier, CameraModule
from modules.voice_recognition import VoiceRecognition
from modules.motor_control import MotorController, UltrasonicSensor
from utils.helpers import load_config, setup_logging, ensure_directories


class SmartTrashController:
    """
    Main controller for the smart trash bin system
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the smart trash controller
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = load_config(config_path)
        
        # Setup logging
        log_file = self.config.get('system', {}).get('log_file', 'logs/smart_trash.log')
        setup_logging(log_file=log_file)
        
        # Ensure required directories exist
        ensure_directories()
        
        # Initialize modules
        self.camera = None
        self.classifier = None
        self.voice = None
        self.motor = None
        self.sensor = None
        self.voice_feedback_enabled = self.config.get('system', {}).get('voice_feedback', True)
        self.auto_close_delay = self.config.get('system', {}).get('auto_close_delay', 5)
        
        logging.info("Smart Trash Controller initialized")
    
    def initialize_modules(self) -> bool:
        """
        Initialize all system modules
        
        Returns:
            True if all modules initialized successfully
        """
        success = True
        
        # Initialize camera
        cam_config = self.config.get('camera', {})
        self.camera = CameraModule(
            device_id=cam_config.get('device_id', 0),
            resolution=tuple(cam_config.get('resolution', [640, 480]))
        )
        if not self.camera.initialize():
            logging.warning("Camera initialization failed")
            success = False
        
        # Initialize classifier
        class_config = self.config.get('classification', {})
        self.classifier = ImageClassifier(
            model_path=class_config.get('model_path', 'models/waste_classifier.h5'),
            categories=class_config.get('categories', ['recyclable', 'organic', 'hazardous', 'general']),
            confidence_threshold=class_config.get('confidence_threshold', 0.7)
        )
        
        # Initialize voice recognition
        voice_config = self.config.get('voice', {})
        self.voice = VoiceRecognition(
            language=voice_config.get('language', 'vi-VN'),
            timeout=voice_config.get('timeout', 5),
            phrase_time_limit=voice_config.get('phrase_time_limit', 3),
            commands=voice_config.get('commands', {})
        )
        if not self.voice.initialize():
            logging.warning("Voice recognition initialization failed")
            success = False
        
        # Initialize motor controller
        motor_config = self.config.get('motor', {})
        self.motor = MotorController(
            motor_pin=motor_config.get('lid_motor_pin', 17),
            min_angle=motor_config.get('servo_min_angle', 0),
            max_angle=motor_config.get('servo_max_angle', 90)
        )
        if not self.motor.initialize():
            logging.warning("Motor controller initialization failed")
            success = False
        
        # Initialize ultrasonic sensor
        sensor_config = self.config.get('sensors', {})
        self.sensor = UltrasonicSensor(
            trigger_pin=sensor_config.get('ultrasonic_trigger_pin', 23),
            echo_pin=sensor_config.get('ultrasonic_echo_pin', 24),
            threshold=sensor_config.get('distance_threshold', 30)
        )
        if not self.sensor.initialize():
            logging.warning("Ultrasonic sensor initialization failed")
            success = False
        
        if success:
            logging.info("All modules initialized successfully")
        else:
            logging.warning("Some modules failed to initialize")
        
        return success
    
    def classify_waste(self) -> tuple:
        """
        Capture image and classify waste
        
        Returns:
            Tuple of (category, confidence)
        """
        if self.camera is None or self.classifier is None:
            logging.error("Camera or classifier not initialized")
            return ("error", 0.0)
        
        # Capture image
        image = self.camera.capture_image()
        if image is None:
            logging.error("Failed to capture image")
            return ("error", 0.0)
        
        # Classify
        category, confidence = self.classifier.classify(image)
        logging.info(f"Classified as: {category} (confidence: {confidence:.2f})")
        
        # Provide voice feedback
        if self.voice_feedback_enabled and self.voice:
            feedback = self.voice.get_voice_feedback(category, language="vi")
            self.voice.speak(feedback)
        
        return category, confidence
    
    def handle_voice_command(self, command: str):
        """
        Handle voice command
        
        Args:
            command: Command name
        """
        if command == 'open':
            self.open_lid()
        elif command == 'close':
            self.close_lid()
        elif command == 'classify':
            category, confidence = self.classify_waste()
            if self.voice:
                self.voice.speak(f"{category}, độ tin cậy {int(confidence * 100)} phần trăm")
        elif command == 'status':
            status = "mở" if self.motor.is_open else "đóng"
            if self.voice:
                self.voice.speak(f"Nắp thùng rác đang {status}")
    
    def open_lid(self):
        """Open the lid"""
        if self.motor:
            self.motor.open_lid()
            if self.voice and self.voice_feedback_enabled:
                self.voice.speak("Đã mở nắp")
    
    def close_lid(self):
        """Close the lid"""
        if self.motor:
            self.motor.close_lid()
            if self.voice and self.voice_feedback_enabled:
                self.voice.speak("Đã đóng nắp")
    
    def run(self):
        """
        Main control loop
        """
        logging.info("Starting Smart Trash AIOT system...")
        
        if not self.initialize_modules():
            logging.error("Failed to initialize all modules. Check configuration.")
            return
        
        if self.voice:
            self.voice.speak("Hệ thống thùng rác thông minh đã sẵn sàng")
        
        try:
            logging.info("Entering main control loop. Press Ctrl+C to exit.")
            
            while True:
                # Check for voice command
                if self.voice:
                    text = self.voice.listen()
                    if text:
                        command = self.voice.parse_command(text)
                        if command:
                            self.handle_voice_command(command)
                
                # Check ultrasonic sensor for automatic opening
                if self.sensor and not self.motor.is_open:
                    if self.sensor.is_object_detected():
                        logging.info("Object detected - auto opening lid")
                        self.open_lid()
                        
                        # Classify waste
                        time.sleep(1)  # Wait for object to be in position
                        self.classify_waste()
                        
                        # Auto close after delay
                        logging.info(f"Auto-closing in {self.auto_close_delay} seconds...")
                        time.sleep(self.auto_close_delay)
                        self.close_lid()
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logging.info("Shutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        logging.info("Cleaning up resources...")
        
        if self.camera:
            self.camera.release()
        
        if self.motor:
            self.motor.cleanup()
        
        logging.info("Cleanup complete")


def main():
    """Main entry point"""
    controller = SmartTrashController()
    controller.run()


if __name__ == "__main__":
    main()
