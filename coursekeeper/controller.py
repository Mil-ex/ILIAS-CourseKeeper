from bs4 import BeautifulSoup
from .config import Config
import os

class Controller:
    def __init__(self, session_manager):
        """Initialize the controller with a session manager."""
        self.session_manager = session_manager
        self.config = Config()

    def perform_dashboard_tasks(self):
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

        # Get the dashboard configuration from the config file
        dashboard_config = self.config.get_dashboard_config()
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

        # Find all the groups within the dashboard
        groups = dashboard_main.find_all(class_=group_class)
        if not groups:
            print(f"No groups with class '{group_class}' found in the dashboard.")
            return

        # List of groups to filter
        specified_groups = self.config.get_groups()

        for group in groups:
            group_name = group.find(group_name_tag).text.strip()
            if group_name in specified_groups:
                print(f"Courses in Group: {group_name}")
                courses = group.find_all(class_=course_class)
                for course in courses:
                    course_name_element = course.find(class_=course_name_class)
                    if course_name_element:
                        course_name = course_name_element.text.strip()
                        course_link = course_name_element.find(course_link_tag)['href']
                        print(f"Course: {course_name}, Link: {course_link}")

                        # Follow the course link and process the course page
                        self.process_course_page(course_link)
                    else:
                        print("Course name or link not found.")

    def process_dashboard(self):
        """Print course name and hyperlink for the courses in the specified group(s)."""
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

        # Find all the groups within the dashboard
        groups = dashboard_main.find_all(class_=group_class)
        if not groups:
            print(f"No groups with class '{group_class}' found in the dashboard.")
            return

        # List of groups to filter
        specified_groups = self.config.get_groups()

        for group in groups:
            group_name = group.find(group_name_tag).text.strip()
            if group_name in specified_groups:
                print(f"Courses in Group: {group_name}")
                courses = group.find_all(class_=course_class)
                for course in courses:
                    course_name_element = course.find(class_=course_name_class)
                    if course_name_element:
                        course_name = course_name_element.text.strip()
                        course_link = course_name_element.find(course_link_tag)['href']
                        print(f"Course: {course_name}, Link: {course_link}")

                        # Follow the course link and process the course page
                        print(group_name,course_name)
                        self.process_course_page(course_link)
                    else:
                        print("Course name or link not found.")

    def process_course_page(self, course_link):
        """Fetch and process a course page based on the configuration."""
        # Fetch the course page content using the session manager
        course_page = self.session_manager.fetch_page(course_link)
        if not course_page:
            print(f"Failed to load the course page at {course_link}.")
            return

        soup = BeautifulSoup(course_page, 'html.parser')

        # Get the course configuration from the config file
        course_config = self.config.get_course_config()
        list_class = course_config.get("list_identifier")
        item_class = course_config.get("item_identifier")
        item_name_tag = course_config.get("item_name")
        item_link_tag = course_config.get("item_hyperlink")

        # Find the main list section dynamically
        course_list = soup.find(class_=list_class)
        if not course_list:
            print(f"Course list with class '{list_class}' not found.")
            return

        # Find all the course items
        items = course_list.find_all(class_=item_class)
        if not items:
            print(f"No items with class '{item_class}' found in the course.")
            return

        for item in items:
            # Gather the item name
            item_name_element = item.find(item_name_tag)
            if item_name_element:
                item_name = item_name_element.text.strip()
            else:
                item_name = None
            
            # Gather the item hyperlink
            item_link_element = item.find(item_link_tag)
            if item_link_element and item_link_element.has_attr('href'):
                item_link = item_link_element['href']
            else:
                item_link = None

            # Output results and handle missing data
            if item_name and item_link:
                print(f"Item: {item_name}, Link: {item_link}")
            elif item_name:
                print(f"Item: {item_name}, but no link found.")
            elif item_link:
                print(f"Link found: {item_link}, but no item name.")
            else:
                print("Item name or link not found.")

            # Optional: You can follow the link here if you need to process it further
            # if item_link:
            #     self.follow_item_link(item_link)


    def create_folder(self, parent_folder_name, new_folder_name):
        """Create a new folder inside the output directory specified in the config."""
        output_folder = self.config.get_output_folder()

        # Clean up the folder name to remove invalid characters
        safe_folder_name = "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in new_folder_name)

        # Construct the full path for the new folder
        full_path = os.path.join(output_folder, parent_folder_name.replace("/","_"), safe_folder_name)

        try:
            os.makedirs(full_path, exist_ok=True)
            print(f"Folder '{full_path}' created successfully.")
        except Exception as e:
            print(f"Error creating folder '{full_path}': {e}")
