import yaml
from pathlib import Path 
from core.exceptions import ConfigurationError

class ConfigManager:
    _instance = None 
    _config = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self, path: str = "config/settings.yaml") -> None:
        config_path = Path(path)
        if not config_path.exists():
            raise ConfigurationError(f"Config file not found: {path}")
        
        with open(config_path) as f:
            self._config = yaml.safe_load(f)


    def get(self,*keys):
        """Get a nested config value: config.get('pipeline', 'tickers')"""
        value = self._config
        for key in keys:
            value = value[key] 
        return value  

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance