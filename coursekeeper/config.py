import json
import os

class Config:
    def __init__(self):
        self.config_data = self.load_config()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'parser_config.json')
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print("Configuration file not found.")
            return {}

    def get_login_form_config(self):
        """Retrieve the login form configuration."""
        form_config = self.config_data.get("login_form", {})
        if not form_config:
            print("Login form configuration not found in config.json.")
        return form_config
