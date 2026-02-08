import json
import os

def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    return config

def validate_config(config):
    """Validate configuration parameters."""
    required_fields = ['region', 'year', 'operation', 'output']
    
    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    # Validate operation
    valid_operations = ['average', 'sum']
    if config['operation'] not in valid_operations:
        return False, f"Invalid operation '{config['operation']}'. Must be 'average' or 'sum'."

    # Validate year
    if not isinstance(config['year'], int):
        return False, "Year must be an integer."
    if config['year'] < 1960 or config['year'] > 2026:
        return False, "Year must be between 1960 and 2024."
    
    # Validate output
    valid_outputs = ['dashboard', 'file']
    if config['output'] not in valid_outputs:
        return False, f"Invalid output '{config['output']}'. Must be 'dashboard' or 'file'."

  
    if 'country' not in config:
        config['country'] = None
    
    return True, "Configuration is valid."
