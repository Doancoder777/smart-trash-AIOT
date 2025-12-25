"""
Voice Recognition Module
Handles voice commands for trash bin control
"""

import speech_recognition as sr
import pyttsx3
import logging
from typing import Optional, List


class VoiceRecognition:
    """
    Voice recognition module for processing voice commands
    """
    
    def __init__(self, language: str = "vi-VN", timeout: int = 5, 
                 phrase_time_limit: int = 3, commands: dict = None):
        """
        Initialize voice recognition module
        
        Args:
            language: Language code (e.g., 'vi-VN' for Vietnamese)
            timeout: Timeout for listening
            phrase_time_limit: Maximum time for a phrase
            commands: Dictionary of command keywords
        """
        self.language = language
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.commands = commands or {
            'open': ['mở nắp', 'mở', 'open'],
            'close': ['đóng nắp', 'đóng', 'close'],
            'classify': ['phân loại', 'classify', 'nhận diện'],
            'status': ['trạng thái', 'status']
        }
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            logging.info("Text-to-speech engine initialized")
        except Exception as e:
            logging.warning(f"Could not initialize TTS: {e}")
            self.tts_engine = None
    
    def initialize(self) -> bool:
        """
        Initialize microphone
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                logging.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            logging.info("Voice recognition initialized")
            return True
            
        except Exception as e:
            logging.error(f"Microphone initialization error: {e}")
            return False
    
    def listen(self) -> Optional[str]:
        """
        Listen for voice command
        
        Returns:
            Recognized text or None if failed
        """
        if self.microphone is None:
            logging.error("Microphone not initialized")
            return None
        
        try:
            with self.microphone as source:
                logging.info("Listening for command...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_time_limit
                )
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=self.language)
            logging.info(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            logging.debug("Listening timeout")
            return None
        except sr.UnknownValueError:
            logging.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            logging.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in voice recognition: {e}")
            return None
    
    def parse_command(self, text: str) -> Optional[str]:
        """
        Parse text to identify command
        
        Args:
            text: Recognized text
            
        Returns:
            Command name or None if no match
        """
        if text is None:
            return None
        
        text_lower = text.lower()
        
        # Check each command category
        for command_name, keywords in self.commands.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    logging.info(f"Command identified: {command_name}")
                    return command_name
        
        logging.debug(f"No command matched for: {text}")
        return None
    
    def speak(self, text: str):
        """
        Speak text using text-to-speech
        
        Args:
            text: Text to speak
        """
        if self.tts_engine is None:
            logging.debug(f"TTS not available. Would say: {text}")
            return
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS error: {e}")
    
    def get_voice_feedback(self, category: str, language: str = "vi") -> str:
        """
        Get voice feedback message for waste category
        
        Args:
            category: Waste category
            language: Language for feedback ('vi' or 'en')
            
        Returns:
            Feedback message
        """
        feedback_vi = {
            'recyclable': 'Rác có thể tái chế',
            'organic': 'Rác hữu cơ',
            'hazardous': 'Rác nguy hại',
            'general': 'Rác thông thường',
            'unknown': 'Không xác định được loại rác'
        }
        
        feedback_en = {
            'recyclable': 'Recyclable waste',
            'organic': 'Organic waste',
            'hazardous': 'Hazardous waste',
            'general': 'General waste',
            'unknown': 'Unknown waste type'
        }
        
        if language == "vi":
            return feedback_vi.get(category, 'Không xác định')
        else:
            return feedback_en.get(category, 'Unknown')
