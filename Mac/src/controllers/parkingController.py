class ParkingController:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_available_spaces(self):
        """
        Retrieves available parking spaces from the backend.
        """
        return self.api_client.get_parking_spaces()

    def book_space(self, parking_id, user):
        """
        Books a parking space for the given user.

        Parameters:
        - parking_id (str): The ID of the parking space.
        - user (User): The user object.

        Returns:
        - bool: True if booking is successful, False otherwise.
        """
        return self.api_client.book_parking_space(parking_id, user)
