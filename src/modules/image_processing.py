"""
Image Processing Module for Waste Classification
Handles image capture and AI-based waste classification
"""

import cv2
import numpy as np
from tensorflow import keras
import logging
from typing import Tuple, Optional
from pathlib import Path


class ImageClassifier:
    """
    AI-powered image classifier for waste categorization
    """
    
    def __init__(self, model_path: str, categories: list, confidence_threshold: float = 0.7):
        """
        Initialize the image classifier
        
        Args:
            model_path: Path to the trained model
            categories: List of waste categories
            confidence_threshold: Minimum confidence for classification
        """
        self.categories = categories
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.model_path = model_path
        
        # Try to load model if exists
        if Path(model_path).exists():
            try:
                self.model = keras.models.load_model(model_path)
                logging.info(f"Loaded classification model from {model_path}")
            except Exception as e:
                logging.warning(f"Could not load model: {e}. Using dummy classifier.")
                self.model = None
        else:
            logging.warning(f"Model not found at {model_path}. Using dummy classifier.")
            self.model = None
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for classification
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed image
        """
        # Resize to model input size
        img_resized = cv2.resize(image, (224, 224))
        
        # Convert to RGB if needed
        if len(img_resized.shape) == 2:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2RGB)
        elif img_resized.shape[2] == 4:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGRA2RGB)
        else:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize
        img_normalized = img_resized.astype(np.float32) / 255.0
        
        # Add batch dimension
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch
    
    def classify(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Classify waste in the image
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (category, confidence)
        """
        if self.model is None:
            # Dummy classification based on simple color analysis
            return self._dummy_classify(image)
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Get prediction
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get the class with highest probability
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])
            
            if confidence >= self.confidence_threshold:
                category = self.categories[class_idx]
                return category, confidence
            else:
                return "unknown", confidence
                
        except Exception as e:
            logging.error(f"Classification error: {e}")
            return "error", 0.0
    
    def _dummy_classify(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Dummy classifier based on color analysis (fallback)
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (category, confidence)
        """
        # Calculate average color
        avg_color = np.mean(image, axis=(0, 1))
        
        # Simple heuristic based on color
        b, g, r = avg_color
        
        if g > r and g > b:
            # Green-ish: likely organic
            return "organic", 0.75
        elif b > r and b > g:
            # Blue-ish: likely recyclable (plastic bottles, etc.)
            return "recyclable", 0.72
        elif r > g and r > b:
            # Red-ish: likely hazardous
            return "hazardous", 0.70
        else:
            # Default to general waste
            return "general", 0.68


class CameraModule:
    """
    Camera module for capturing images
    """
    
    def __init__(self, device_id: int = 0, resolution: Tuple[int, int] = (640, 480)):
        """
        Initialize camera module
        
        Args:
            device_id: Camera device ID
            resolution: Camera resolution (width, height)
        """
        self.device_id = device_id
        self.resolution = resolution
        self.camera = None
        
    def initialize(self) -> bool:
        """
        Initialize camera connection
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.camera = cv2.VideoCapture(self.device_id)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            if not self.camera.isOpened():
                logging.error("Failed to open camera")
                return False
            
            logging.info(f"Camera initialized with resolution {self.resolution}")
            return True
            
        except Exception as e:
            logging.error(f"Camera initialization error: {e}")
            return False
    
    def capture_image(self) -> Optional[np.ndarray]:
        """
        Capture a single image from camera
        
        Returns:
            Captured image or None if failed
        """
        if self.camera is None or not self.camera.isOpened():
            logging.error("Camera not initialized")
            return None
        
        try:
            ret, frame = self.camera.read()
            if ret:
                return frame
            else:
                logging.error("Failed to capture frame")
                return None
                
        except Exception as e:
            logging.error(f"Image capture error: {e}")
            return None
    
    def release(self):
        """Release camera resources"""
        if self.camera is not None:
            self.camera.release()
            logging.info("Camera released")
