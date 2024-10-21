from bs4 import BeautifulSoup
from .config import Config

class Controller:
    def __init__(self, session_manager):
        """Initialize the controller with a session manager."""
        self.session_manager = session_manager
        self.config = Config()

    def get_dashboard_groups(self):
        """Fetch and parse the dashboard content after login."""
        
        # After login, the session manager should already have the redirected dashboard URL
        dashboard_url = self.session_manager.get_current_url()  # Retrieve the current URL after login
        
        if not dashboard_url:
            print("No dashboard URL available after login.")
            return

        # Fetch the dashboard page content
        dashboard_page = self.session_manager.fetch_page(dashboard_url)
        
        if not dashboard_page:
            print("Failed to fetch the dashboard page.")
            return

        soup = BeautifulSoup(dashboard_page, 'html.parser')

        # Get the dashboard configuration from the config file
        dashboard_config = self.config.get_dashboard_config()
        main_content_class = dashboard_config.get("main_content_class")
        item_group_class = dashboard_config.get("item_group_class")
        header_tag = dashboard_config.get("header_tag")

        # Find the main dashboard section dynamically
        dashboard_main = soup.find(class_=main_content_class)
        if not dashboard_main:
            print(f"Dashboard content with class '{main_content_class}' not found.")
            return

        # Find all the items within the dashboard
        item_groups = dashboard_main.find_all(class_=item_group_class)
        if not item_groups:
            print(f"No item groups with class '{item_group_class}' found in the dashboard.")
            return

        headers = []
        for item in item_groups:
            # For each item, gather the header based on the specified tag (e.g., <h3>)
            header = item.find(header_tag)
            if header:
                header_text = header.text.strip()
                headers.append(header_text)
                print(f"Found header: {header_text}")
            else:
                print(f"No header with tag '{header_tag}' found for this item.")

        if headers:
            print("\nDashboard Headers:")
            for idx, header in enumerate(headers, start=1):
                print(f"{idx}. {header}")
        else:
            print("No headers found in the dashboard.")

