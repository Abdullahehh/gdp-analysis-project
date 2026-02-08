"""
Configuration Handler Module
Manages configuration from config.json
By: [YOUR PARTNER'S NAME]
"""

import json
import os


def load_config(config_path='config.json'):
 
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    return config


def validate_config(config):

    required_fields = ['data_file', 'continent', 'year', 'country', 'operation']
    
    # Use list comprehension for functional programming
    missing_fields = [field for field in required_fields if field not in config]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate operation
    valid_operations = ['average', 'sum']
    if config['operation'] not in valid_operations:
        return False, f"Invalid operation. Must be 'average' or 'sum'"
    
    # Validate year
    if not isinstance(config['year'], int):
        return False, "Year must be an integer"
    
    if config['year'] < 1960 or config['year'] > 2024:
        return False, "Year must be between 1960 and 2024"
    
    return True, "Configuration is valid"

    git add modules/config_handler.py
git commit -m "Added config handler in module"
git push origin main