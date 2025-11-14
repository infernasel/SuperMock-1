"""
Configuration management for SuperMock
"""

import os
import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    """Configuration manager for SuperMock"""
    
    DEFAULT_CONFIG = {
        "server": {
            "host": "localhost",
            "port": 8081,
            "debug": False
        },
        "bot": {
            "id": 123456789,
            "first_name": "MockBot",
            "username": "mock_bot"
        },
        "user": {
            "id": 12345,
            "first_name": "TestUser",
            "username": "test_user"
        },
        "logging": {
            "enabled": True,
            "level": "INFO",
            "file": None
        },
        "features": {
            "save_history": True,
            "history_file": ".supermock_history.json"
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file:
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str):
        """Load configuration from YAML or JSON file"""
        path = Path(config_file)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(path, 'r') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                loaded_config = yaml.safe_load(f)
            elif config_file.endswith('.json'):
                loaded_config = json.load(f)
            else:
                raise ValueError("Unsupported configuration file format. Use .yaml, .yml, or .json")
        
        # Merge with default config
        self._merge_dict(self.config, loaded_config)
    
    def _merge_dict(self, base: Dict, update: Dict):
        """Recursively merge update dict into base dict"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dict(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key path"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by dot-separated key path"""
        keys = key.split('.')
        target = self.config
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        target[keys[-1]] = value
    
    def save_to_file(self, config_file: str):
        """Save configuration to file"""
        path = Path(config_file)
        
        with open(path, 'w') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                yaml.dump(self.config, f, default_flow_style=False)
            elif config_file.endswith('.json'):
                json.dump(self.config, f, indent=2)
            else:
                raise ValueError("Unsupported configuration file format. Use .yaml, .yml, or .json")
