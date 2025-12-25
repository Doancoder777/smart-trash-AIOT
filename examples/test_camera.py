#!/usr/bin/env python3
"""
Example script to test the image classification module
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from modules.image_processing import CameraModule, ImageClassifier
import logging

logging.basicConfig(level=logging.INFO)


def main():
    """Test image classification"""
    print("=== Testing Image Classification Module ===\n")
    
    # Initialize camera
    print("Initializing camera...")
    camera = CameraModule(device_id=0, resolution=(640, 480))
    
    if not camera.initialize():
        print("Failed to initialize camera!")
        return
    
    print("Camera initialized successfully!\n")
    
    # Initialize classifier
    print("Initializing classifier...")
    classifier = ImageClassifier(
        model_path="models/waste_classifier.h5",
        categories=['recyclable', 'organic', 'hazardous', 'general'],
        confidence_threshold=0.7
    )
    print("Classifier initialized!\n")
    
    # Capture and classify
    print("Capturing image...")
    image = camera.capture_image()
    
    if image is None:
        print("Failed to capture image!")
        camera.release()
        return
    
    print(f"Image captured! Shape: {image.shape}\n")
    
    # Classify
    print("Classifying waste...")
    category, confidence = classifier.classify(image)
    
    print(f"\n=== Results ===")
    print(f"Category: {category}")
    print(f"Confidence: {confidence:.2%}")
    
    # Cleanup
    camera.release()
    print("\nTest completed!")


if __name__ == "__main__":
    main()
