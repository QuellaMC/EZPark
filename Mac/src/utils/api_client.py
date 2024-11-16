# src/utils/api_client.py
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import json
from src.utils.config import Config


class APIClient:
    def __init__(self):
        """
        Initializes the API client with configuration settings.
        """
        self.config = Config()
        self.base_url = self.config.BASE_API_URL
        self.session = requests.Session()
        self.token = None

    def _get_headers(self):
        """
        Constructs the headers for HTTP requests, including the Authorization header if a token is available.
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def login(self, email, password):
        """
        Authenticates the user with the backend API and stores the authentication token.

        Parameters:
        - email (str): The user's email.
        - password (str): The user's password.

        Returns:
        - dict: The response data from the API.

        Raises:
        - HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.base_url}/auth/login/"
        payload = {
            'email': email,
            'password': password
        }
        try:
            response = self.session.post(url, headers=self._get_headers(), data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            data = response.json()
            self.token = data.get('token')  # 假设API返回的token字段名为'token'
            return data
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            print(f"An error occurred during login: {e}")
            raise

    def register(self, email, password, name):
        """
        Registers a new user with the backend API.

        Parameters:
        - email (str): The user's email.
        - password (str): The user's password.
        - name (str): The user's name.

        Returns:
        - dict: The response data from the API.

        Raises:
        - HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.base_url}/auth/register/"
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        try:
            response = self.session.post(url, headers=self._get_headers(), data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            data = response.json()
            self.token = data.get('token')  # 假设注册后立即返回token
            return data
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            print(f"An error occurred during registration: {e}")
            raise

    def get_parking_spaces(self):
        """
        Retrieves the list of available parking spaces from the backend API.

        Returns:
        - list: A list of parking space dictionaries.

        Raises:
        - HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.base_url}/parking_spaces/"
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('parking_spaces', [])
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            print(f"An error occurred while fetching parking spaces: {e}")
            raise

    def book_parking_space(self, parking_id, user):
        """
        Books a specific parking space for the authenticated user.

        Parameters:
        - parking_id (str): The ID of the parking space to book.
        - user (object): The user object containing necessary user information.

        Returns:
        - dict: The response data from the API.

        Raises:
        - HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.base_url}/parking_spaces/{parking_id}/book/"
        payload = {
            'user_id': user.id,  # 假设用户对象有一个'id'属性
            'parking_id': parking_id
        }
        try:
            response = self.session.post(url, headers=self._get_headers(), data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            data = response.json()
            return data
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            print(f"An error occurred while booking parking space: {e}")
            raise

    def logout(self):
        """
        Logs out the user by clearing the authentication token.
        """
        self.token = None
        self.session.headers.pop('Authorization', None)

    def is_authenticated(self):
        """
        Checks if the client is currently authenticated.

        Returns:
        - bool: True if authenticated, False otherwise.
        """
        return self.token is not None
