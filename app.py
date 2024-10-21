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
    authenticator.login(session_manager)

    controller = Controller(session_manager)

    # Print courses in the specified group
    controller.process_dashboard()

if __name__ == "__main__":
    main()
