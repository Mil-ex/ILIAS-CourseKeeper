from coursekeeper.authenticator import Authenticator
from coursekeeper.session_manager import SessionManager
from coursekeeper.controller import Controller
from coursekeeper.config import Config

def main():
    # Load configuration
    config = Config()

    # Initialize session and authenticator
    session_manager = SessionManager(config)
    authenticator = Authenticator()

    # Authenticate and log in
    authenticator.store_creds()
    authenticator.login(session_manager)

    # Perform tasks with the controller
    controller = Controller(session_manager)
    controller.get_dashboard_groups()

    # Now you can access groups from config.json
    groups = config.get_groups()
    print(f"Groups: {groups}")

if __name__ == "__main__":
    main()
