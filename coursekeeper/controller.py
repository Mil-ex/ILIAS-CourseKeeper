from bs4 import BeautifulSoup
from .config import Config
from urllib.parse import urljoin
import os
import requests

class Controller:
    def __init__(self, session_manager):
        """Initialize the controller with a session manager."""
        self.session_manager = session_manager
        self.config = Config()

    def show_available_groups(self):
        """Fetch and parse the dashboard content after login."""
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

        # Get the dashboard configuration from the JSON file
        dashboard_config = self.config.get('dashboard', {})
        main_content_class = dashboard_config.get("dashboard_identifier")
        group_class = dashboard_config.get("group_identifier")
        group_name_tag = dashboard_config.get("group_name_identifier")
        course_class = dashboard_config.get("course_identifier")
        course_name_class = dashboard_config.get("course_name_identifier")
        course_link_tag = dashboard_config.get("course_hyperlink")

        # Find the main dashboard section dynamically
        dashboard_main = soup.find(class_=main_content_class)
        if not dashboard_main:
            print(f"Dashboard content with class '{main_content_class}' not found.")
            return

        # Get the list of groups specified in the JSON config
        specified_groups = set(self.config.get('groups', []))  # Use a set for faster lookup

        # Keep track of processed groups to avoid duplicates
        processed_groups = set()

        # Find all groups within the dashboard and process only specified ones
        groups = dashboard_main.find_all(class_=group_class)
        for group in groups:
            group_name_element = group.find(group_name_tag)
            if group_name_element:
                group_name = group_name_element.text.strip()
                if group_name in specified_groups and group_name not in processed_groups:
                    print(f"Processing Group: {group_name}")
                    processed_groups.add(group_name)  # Mark this group as processed
                    courses = group.find_all(class_=course_class)
                    for course in courses:
                        course_name_element = course.find(class_=course_name_class)
                        if course_name_element:
                            course_name = course_name_element.text.strip()
                            course_link = course_name_element.find(course_link_tag)['href']
                            print(f"Course: {course_name}, Link: {course_link}")
                        else:
                            print("Course name or link not found.")
                else:
                    ...
            else:
                print(f"Group name element not found for a group.")

    def create_folder(self, parent_folder_name, new_folder_name):
        """Create a new folder inside the output directory specified in the config."""
        output_folder = self.config.get('output_folder', "")
        safe_folder_name = "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in new_folder_name)
        full_path = os.path.join(output_folder, parent_folder_name.replace("/","_"), safe_folder_name)

        try:
            os.makedirs(full_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating folder '{full_path}': {e}")
