class AuthController:
    def __init__(self, api_client):
        """
        Initializes the authentication controller with the provided API client.

        Parameters:
        - api_client (APIClient): The API client instance to interact with the backend.
        """
        self.api_client = api_client

    def login(self, email, password):
        """
        Authenticates the user by calling the API client and returns the result.

        Parameters:
        - email (str): The user's email.
        - password (str): The user's password.

        Returns:
        - (bool, str): A tuple containing a success flag and a message.
        """
        try:
            response = self.api_client.login(email, password)
            if response:
                return True, "Login successful."
            return False, "Invalid credentials."
        except Exception as e:
            return False, str(e)

    def register(self, email, password, name):
        """
        Registers a new user by calling the API client and returns the result.

        Parameters:
        - email (str): The user's email.
        - password (str): The user's password.
        - name (str): The user's name.

        Returns:
        - (bool, str): A tuple containing a success flag and a message.
        """
        try:
            response = self.api_client.register(email, password, name)
            if response:
                return True, "Registration successful."
            return False, "Registration failed."
        except Exception as e:
            return False, str(e)

    def logout(self):
        """
        Logs out the user by clearing the token from the API client.

        Returns:
        - (bool, str): A tuple containing a success flag and a message.
        """
        try:
            self.api_client.logout()
            return True, "Logout successful."
        except Exception as e:
            return False, str(e)

    def is_authenticated(self):
        """
        Checks if the user is currently authenticated.

        Returns:
        - bool: True if authenticated, False otherwise.
        """
        return self.api_client.is_authenticated()

