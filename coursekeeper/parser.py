from bs4 import BeautifulSoup
from .config import Config

class Parser:
    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')
        self.config = Config()

    def find_login_form(self):
        """Find the login form based on configurable attributes from the JSON file."""
        form_config = self.config.get_login_form_config()
        form_attributes = form_config.get("form_attributes", {})

        if not form_attributes:
            print("Form attributes not found in configuration.")
            return None

        # Use the form_attributes from the JSON to find the form dynamically
        return self.soup.find('form', form_attributes)

    def find_login_fields(self, form):
        """Find the username and password fields using the 'name' property."""
        form_config = self.config.get_login_form_config()

        if 'username_field' not in form_config or 'password_field' not in form_config:
            print("Missing username or password field in configuration.")
            return None, None

        username_field = form.find('input', {'name': form_config['username_field']['name']})
        password_field = form.find('input', {'name': form_config['password_field']['name']})

        return username_field, password_field
