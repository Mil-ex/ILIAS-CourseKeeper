import os
import json

class Config:
    def __init__(self):
        self.config_data = self.load_config()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print("Configuration file not found.")
            return {}

    def get_login_form_config(self):
        return self.config_data.get("login_form", {})

    def get_dashboard_config(self):
        return self.config_data.get("dashboard", {})

    def get_login_url(self):
        return self.config_data.get("login_url", "")

    def get_groups(self):
        return self.config_data.get("groups", [])
