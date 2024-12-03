class NonParkingSpot:
    def __init__(self, spot_number, spot_type):
        """
        Initialize a NonParkingSpot instance.

        Args:
            spot_number (int): The number of the spot.
            spot_type (str): The type of non-parking spot (e.g., 'Exit', 'Entrance', 'Walkway').
        """
        self.spot_number = spot_number
        self.spot_type = spot_type

    def get_spot_number(self):
        """
        Get the spot number.
        """
        return self.spot_number

    def get_spot_type(self):
        """
        Get the type of the non-parking spot.
        """
        return self.spot
