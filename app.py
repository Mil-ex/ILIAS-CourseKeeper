from coursekeeper.authenticator import Authenticator
from coursekeeper.session_manager import SessionManager

def main():
    session_manager = SessionManager()

    authenticator = Authenticator()

    # Store credentials if not already stored
    authenticator.del_creds()
    # authenticator.store_creds()
    print(authenticator.get_creds())

    # Perform the login using the Parser and Authenticator
    authenticator.login(session_manager)

if __name__ == "__main__":
    main()
