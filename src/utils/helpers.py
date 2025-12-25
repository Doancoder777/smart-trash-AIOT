"""
Utility functions for the Smart Trash AIOT system
"""

import yaml
import logging
from pathlib import Path
from typing import Any, Dict


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return {}


def setup_logging(log_file: str = None, level: int = logging.INFO):
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file
        level: Logging level
    """
    # Create logs directory if needed
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )
    
    logging.info("Logging configured")


def ensure_directories():
    """Ensure required directories exist"""
    directories = ['models', 'logs', 'data']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep in models directory
        if directory == 'models':
            gitkeep_path = Path(directory) / '.gitkeep'
            if not gitkeep_path.exists():
                gitkeep_path.touch()
