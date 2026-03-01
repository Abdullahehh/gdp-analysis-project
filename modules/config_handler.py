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
        return False, "Year must be between 1960 and 2026."
    
    # Validate output
    valid_outputs = ['dashboard', 'file']
    if config['output'] not in valid_outputs:
        return False, f"Invalid output '{config['output']}'. Must be 'dashboard' or 'file'."

    # ADDED: Validate region format
    region = config['region'].strip()
    if not region:
        return False, "Region cannot be empty."
    
    # Info message for multi-region
    if '&' in region or ',' in region:
        print(f"ℹ Multiple regions detected: {region}")
        print(f"   Will combine data from: {', '.join([r.strip() for r in region.replace('&', ',').split(',')])}")

    # Validate data file exists
    data_file = config.get('data_file', 'gdp_with_continent_filled.csv')
    if not os.path.exists(data_file):
        return False, f"Data file not found: {data_file}"
    
    # Optional: ensure 'country' exists, even if None
    if 'country' not in config:
        config['country'] = None
    
    return True, "Configuration is valid."