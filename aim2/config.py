"""
AIM2 Configuration Module

This module provides a centralized configuration system for the AIM2 project.
It loads configuration from a YAML file and allows overrides via environment variables.
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

# Default configuration paths to check if not specified in environment
DEFAULT_CONFIG_PATHS = [
    Path("config.yml"),
    Path("config/config.yml"),
    Path("/etc/aim2/config.yml"),
]

# The loaded configuration
_config: Optional[Dict[str, Any]] = None

def _load_config_file(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file. If None, checks default locations.
        
    Returns:
        Dict containing the configuration.
        
    Raises:
        FileNotFoundError: If the configuration file cannot be found.
        yaml.YAMLError: If the configuration file is not valid YAML.
    """
    # If no config path is provided, check environment variable or default locations
    if config_path is None:
        env_config = os.environ.get("AIM2_CONFIG")
        if env_config:
            config_path = Path(env_config)
        else:
            # Try default locations
            for path in DEFAULT_CONFIG_PATHS:
                if path.exists():
                    config_path = path
                    break
            else:
                raise FileNotFoundError(
                    "No configuration file found. Please set AIM2_CONFIG environment variable "
                    "or place a config.yml in one of the default locations."
                )
    
    # Ensure the config file exists
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Load and parse the YAML file
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}
    
    return config

def _apply_environment_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply environment variable overrides to the configuration.
    
    Environment variables should be prefixed with 'AIM2_' and use double underscores
    to denote nested keys. For example:
    - AIM2_DATABASE__HOST overrides config['database']['host']
    - AIM2_API__KEY overrides config['api']['key']
    
    Args:
        config: The base configuration dictionary.
        
    Returns:
        A new dictionary with environment overrides applied.
    """
    result = {}
    
    # Make a deep copy of the config to avoid modifying the original
    import copy
    result = copy.deepcopy(config)
    
    # Process all environment variables that start with AIM2_
    for env_key, value in os.environ.items():
        if not env_key.startswith('AIM2_'):
            continue
            
        # Remove the AIM2_ prefix and convert to lowercase
        key_parts = env_key[5:].lower().split('__')
        
        # Navigate to the appropriate level in the config
        current = result
        for part in key_parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the value, converting from string to appropriate type if needed
        if isinstance(current.get(key_parts[-1]), bool):
            current[key_parts[-1]] = value.lower() in ('true', '1', 't', 'y', 'yes')
        elif isinstance(current.get(key_parts[-1]), int):
            try:
                current[key_parts[-1]] = int(value)
            except (ValueError, TypeError):
                current[key_parts[-1]] = value
        elif isinstance(current.get(key_parts[-1]), float):
            try:
                current[key_parts[-1]] = float(value)
            except (ValueError, TypeError):
                current[key_parts[-1]] = value
        else:
            current[key_parts[-1]] = value
    
    return result

def get_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Get the application configuration.
    
    This function loads the configuration from the specified file (or the default location)
    and applies any environment variable overrides. The configuration is cached after the
    first load.
    
    Args:
        config_path: Optional path to the configuration file. If not provided,
                    checks the AIM2_CONFIG environment variable and then default locations.
                    
    Returns:
        A dictionary containing the application configuration.
        
    Raises:
        FileNotFoundError: If the configuration file cannot be found.
        yaml.YAMLError: If the configuration file is not valid YAML.
    """
    global _config
    
    # Return cached config if available
    if _config is not None:
        return _config
    
    # Load configuration from file
    config = _load_config_file(config_path)
    
    # Apply environment variable overrides
    _config = _apply_environment_overrides(config)
    
    return _config

def reload_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Reload the configuration from disk, ignoring any cached values.
    
    This is useful for development or when the configuration changes at runtime.
    
    Args:
        config_path: Optional path to the configuration file.
        
    Returns:
        A dictionary containing the reloaded application configuration.
    """
    global _config
    _config = None  # Clear the cache
    return get_config(config_path)
