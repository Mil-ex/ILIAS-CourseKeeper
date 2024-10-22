from bs4 import BeautifulSoup
from .config import Config

class Parser:
    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')
        self.config = Config()  # Load configuration using the new Config class

    def find_login_form(self):
        """Find the login form based on configurable attributes from the JSON file."""
        form_config = self.config.get('login_form', {})  # Use the 'get' method

        if not form_config:
            print("Login form configuration not found.")
            return None

        form_attributes = form_config.get('form_attributes', {})
        
        if not form_attributes:
            print("Form attributes not found in configuration.")
            return None

        # # Print the page content to check the form structure if not found
        # print("Page content fetched:", self.soup.prettify())

        # Use the form attributes from the JSON to find the form dynamically
        form = self.soup.find('form', form_attributes)
        
        if form:
            print("Login form found.")
        else:
            print("Login form not found.")
        
        return form

    def find_login_fields(self, form):
        """Find the username and password fields using the 'name' property."""
        form_config = self.config.get('login_form', {})  # Use the new 'get' method

        if not form_config:
            print("Login form configuration not found.")
            return None, None

        username_field_config = form_config.get('username_field', {})
        password_field_config = form_config.get('password_field', {})

        if not username_field_config or not password_field_config:
            print("Missing username or password field in configuration.")
            return None, None

        # Find the fields in the form using their 'name' attribute
        username_field = form.find('input', {'name': username_field_config.get('name')})
        password_field = form.find('input', {'name': password_field_config.get('name')})

        if username_field and password_field:
            print("Username and password fields found.")
        else:
            print("Username or password field not found. Check the field names in configuration.")
        
        return username_field, password_field
