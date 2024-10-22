from coursekeeper.authenticator import Authenticator
from coursekeeper.session_manager import SessionManager
from coursekeeper.controller import Controller
from coursekeeper.config import Config

def main():
    # Initialize session and authenticator
    config = Config()
    session_manager = SessionManager(config)
    authenticator = Authenticator()

    # Authenticate and log in
    authenticator.store_creds()
    if authenticator.login(session_manager):
        controller = Controller(session_manager)
        # Print courses in the specified group
        controller.show_available_groups()
    else:
        print("Login attempt failed. Please try again.")

if __name__ == "__main__":
    main()
