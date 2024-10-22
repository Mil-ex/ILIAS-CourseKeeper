import requests
from urllib.parse import urlparse
from time import sleep

class SessionManager:
    def __init__(self, config):
        self.session = requests.Session()  # Start a session for cookies and persistence
        self.config = config
        self.redirected_url = None  # Store the redirected URL after login
        self.used_urls = []

        # Load the login URL from the config
        self.login_url = self.config.get("login_url")

    def fetch_page(self, url, retries=3):
        """Fetch a page using the current session with retry mechanism."""
        for attempt in range(retries):
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"Failed to fetch page. Status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}. Retrying ({attempt + 1}/{retries})...")
                sleep(2)  # Wait before retrying
        return None

    def set_url(self, url):
        """Set the URL that the session was redirected to after login."""
        self.used_urls.append(url)
        self.redirected_url = url

    def get_current_url(self):
        """Return the current redirected URL."""
        return self.redirected_url

    def get_base_url(self):
        """Return the base URL from the login or redirected URL."""
        url = self.redirected_url if self.redirected_url else self.login_url
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"
