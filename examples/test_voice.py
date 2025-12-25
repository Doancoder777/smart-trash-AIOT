#!/usr/bin/env python3
"""
Example script to test the voice recognition module
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.voice_recognition import VoiceRecognition
import logging

logging.basicConfig(level=logging.INFO)


def main():
    """Test voice recognition"""
    print("=== Testing Voice Recognition Module ===\n")
    
    # Initialize voice recognition
    print("Initializing voice recognition...")
    voice = VoiceRecognition(
        language="vi-VN",
        timeout=5,
        phrase_time_limit=3
    )
    
    if not voice.initialize():
        print("Failed to initialize voice recognition!")
        return
    
    print("Voice recognition initialized!\n")
    
    # Test listening
    print("Available commands:")
    for cmd, keywords in voice.commands.items():
        print(f"  {cmd}: {', '.join(keywords)}")
    
    print("\n" + "="*50)
    print("Listening for commands... (speak now)")
    print("="*50 + "\n")
    
    for i in range(3):
        print(f"Attempt {i+1}/3...")
        text = voice.listen()
        
        if text:
            print(f"Heard: '{text}'")
            command = voice.parse_command(text)
            
            if command:
                print(f"Command recognized: {command}")
                
                # Test voice feedback
                if command == "classify":
                    feedback = voice.get_voice_feedback("recyclable", "vi")
                    print(f"Voice feedback: {feedback}")
                    voice.speak(feedback)
            else:
                print("No matching command found")
        else:
            print("No speech detected")
        
        print()
    
    print("Test completed!")


if __name__ == "__main__":
    main()
