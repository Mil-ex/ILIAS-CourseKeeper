import os
import json

class Config:
    def __init__(self):
        self.config_data = self.load_config()

    def load_config(self):
        """Load the JSON configuration file only once."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print("Configuration file not found.")
            return {}

    def get(self, key, default=None):
        return self.config_data.get(key, default)
