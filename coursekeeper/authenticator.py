from getpass import getpass
import keyring
from urllib.parse import urljoin
from .parser import Parser

class Authenticator:
    def store_creds(self):
        """Prompt the user to enter their username and password and store them securely with keyring."""
        username, password = self.get_creds()
        if not username or not password:
            username = input("Enter your ILIAS username: ")
            password = getpass("Enter your ILIAS password: ")
            keyring.set_password("ILIAS", "username", username)
            keyring.set_password("ILIAS", "password", password)
            print("Credentials stored securely.")
        else:
            print("Credentials are already stored.")

    def get_creds(self):
        """Retrieve credentials securely from keyring."""
        username = keyring.get_password("ILIAS", "username")
        password = keyring.get_password("ILIAS", "password")
        return username, password

    def del_creds(self):
        """Delete the stored username and password from keyring."""
        try:
            keyring.delete_password("ILIAS", "username")
            keyring.delete_password("ILIAS", "password")
            print("Credentials deleted from keyring.")
        except keyring.errors.PasswordDeleteError:
            print("No credentials found to delete.")

    def login(self, session_manager):
        """Log in to ILIAS using the provided session and parser."""
        username, password = self.get_creds()
        if not username or not password:
            print("No credentials found. Please store them first.")
            return

        login_url = session_manager.login_url
        if not login_url:
            print("No login URL found.")
            return

        # Fetch login page
        login_page = session_manager.fetch_page(login_url)
        if not login_page:
            print("Failed to load login page.")
            return

        # Parse the login page
        parser = Parser(login_page)
        form = parser.find_login_form()

        if not form:
            print("Login form not found.")
            return

        # Find the fields
        username_field, password_field = parser.find_login_fields(form)
        if not username_field or not password_field:
            print("Username or password field not found.")
            return

        # Prepare login data
        login_data = {
            username_field['name']: username,
            password_field['name']: password
        }

        # Submit the login form
        action_url = form['action']
        action_url = urljoin(login_url, action_url)
        login_response = session_manager.session.post(action_url, data=login_data, allow_redirects=True)

        # After login, capture the redirected URL and update the session manager's current URL
        redirected_url = login_response.url
        session_manager.set_redirected_url(redirected_url)

        # Check if the login was successful by checking if the login form is still present
        response_page = login_response.text
        response_parser = Parser(response_page)
        response_form = response_parser.find_login_form()

        if response_form:
            print("Login failed. The login form is still present.")
        else:
            print("Login successful!")

