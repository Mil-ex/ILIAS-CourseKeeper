import requests

class SessionManager:
    def __init__(self, config):
        """Initialize the session manager with a session and configuration."""
        self.session = requests.Session()  # Start a session for cookies and persistence
        self.config = config
        self.login_url = self.config.get_login_url()
        self.current_url = self.login_url  # Start by tracking the login URL

    def fetch_page(self, url):
        """Fetch a page using the current session and update the current URL."""
        response = self.session.get(url)
        if response.status_code == 200:
            self.current_url = response.url  # Update the current URL to the one fetched
            return response.text
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None

    def get_current_url(self):
        """Return the current URL after redirection."""
        return self.current_url

    def set_redirected_url(self, url):
        """Set the URL after a redirection, e.g., post-login."""
        self.current_url = url
