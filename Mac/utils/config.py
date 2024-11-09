import os

class Config:
    def __init__(self):
        """
        Initializes the configuration settings.
        """
        self.BASE_API_URL = os.getenv('EZPARK_API_URL', 'https://api.ezpark.com')
        self.TIMEOUT = 10
