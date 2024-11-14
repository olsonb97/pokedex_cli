import yaml
from pathlib import Path

class ConfigError(Exception):
    """Exception raised for errors in the Config class."""
    def __init__(self, message="No error message provided"):
        super().__init__(message)

def _create_class(config):
    class_name = config['name']
    base_url = config['base_url'].rstrip('/')
    
    class_dict = {}
    
    def create_endpoint_attributes(parent_dict, prefix='', parent_obj=class_dict):
        for key, value in parent_dict.items():
            if isinstance(value, dict):
                # Create a new dict for nested endpoints
                nested_dict = {}
                parent_obj[key] = type(key.title(), (), nested_dict)
                create_endpoint_attributes(value, f"{prefix}{key}/", nested_dict)
            else:
                # Remove leading slash and combine with base_url
                path = value.lstrip('/')
                full_url = f"{base_url}/{prefix}{path}"
                parent_obj[key] = full_url

    create_endpoint_attributes(config['endpoints'])
    return type(class_name, (), class_dict)

def load_yaml(yaml_file_path):
    """Loads config from a YAML file and creates the API class."""
    try:
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
        
        if not isinstance(config, dict):
            raise ConfigError(f"Invalid config format: {config}")
            
        if 'name' not in config:
            raise ConfigError("Missing required 'name' key in config file")
        
        return _create_class(config)
    
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {yaml_file_path}")
    except yaml.YAMLError as e:
        raise ConfigError(f"Error parsing YAML file: {e}")
    except Exception as e:
        raise ConfigError(f"Unknown error: {e}")
    
Api = load_yaml(Path(__file__).parent / "config.yaml")