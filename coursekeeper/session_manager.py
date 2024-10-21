import requests
import os

class SessionManager:
    def __init__(self):
        self.session = requests.Session()  # Start a session for cookies and persistence
        self.login_url, self.course_links = self.load_links()  # Load URLs from the file

    def load_links(self):
        """Load the login URL and course links from the links.txt file."""
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'links.txt')
        login_url = None
        course_links = []

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("login_url:"):
                        login_url = line.split(":", 1)[1].strip()
                    elif line.startswith("-"):
                        course_link = line.split("-", 1)[1].strip()
                        if course_link:
                            course_links.append(course_link)

        except FileNotFoundError:
            print("Error: links.txt file not found.")
        
        if not login_url:
            print("Error: login_url not found in links.txt.")
        
        return login_url, course_links

    def fetch_page(self, url):
        """Fetch a page using the current session."""
        response = self.session.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None
