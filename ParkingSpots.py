class ParkingSpot:
    def __init__(self, spot_number, vehicle_type):
        """
        Initialize a ParkingSpot instance.
        
        Args:
            spot_number (int): The number of the parking spot.
            vehicle_type (str): The type of vehicle the spot is designated for.
        """
        self.spot_number = spot_number
        self.vehicle_type = vehicle_type
        self.is_occupied = False

    def get_spot_number(self):
        """
        Get the parking spot number.
        """
        return self.spot_number

    def is_occupied(self):
        """
        Check if the parking spot is occupied.
        """
        return self.is_occupied

    def occupy_spot(self):
        """
        Mark the spot as occupied. Raise an error if it's already occupied.
        """
        if not self.is_occupied:
            self.is_occupied = True
        else:
            print("Spot is already occupied!")

    def vacate_spot(self):
        """
        Mark the spot as vacant. Raise an error if it's already vacant.
        """
        if self.is_occupied:
            self.is_occupied = False
        else:
            print("Spot is already vacant!")

    def get_vehicle_type(self):
        """
        Get the type of vehicle the spot is designated for.
        """
        return self.vehicle_type

    def __str__(self):
        """
        Return a string representation of the parking spot status.
        """
        status = "Occupied" if self.is_occupied else "Available"
        return f"ParkingSpot #{self.spot_number} for {self.vehicle_type} - {status}"

