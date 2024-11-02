import tkinter as tk
from src.ui.login_ui import LoginUI
from src.ui.register_ui import RegisterUI
# from src.controllers.auth_controller import AuthController
# from src.utils.api_client import ApiClient
# from src.utils.config import Config


def main(auth_controller=None):
    # Initialize the application
    root = tk.Tk()
    root.title("EZPark - Parking Management System")

    # Load configuration settings
    # config = Config()
    # api_client = ApiClient(base_url=config.api_base_url)
    # auth_controller = AuthController(api_client)

    # Initialize and display the login UI
    login_ui = LoginUI(root, auth_controller)
    login_ui.pack()

    reg_ui = RegisterUI(root, auth_controller)
    reg_ui.pack()

    # Start the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()