
class ParkingSpot:
    def __init__(self, spot_number, vehicle_type=None, spot_size="medium"):
        self.spot_number = spot_number
        self.vehicle_type = vehicle_type
        self.size = spot_size
        self.is_occupied = False

    def occupy_spot(self):
        self.is_occupied = True

    def vacate_spot(self):
        self.is_occupied = False
        self.vehicle_type = None

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Vacant"
        vehicle_info = f" for {self.vehicle_type}" if self.vehicle_type else ""
        return f"Spot #{self.spot_number} - {self.size.capitalize()} - {status}{vehicle_info}"


class NonParkingSpot:
    def __init__(self, spot_number, spot_type):
        self.spot_number = spot_number
        self.spot_type = spot_type

    def __str__(self):
        return f"NonParkingSpot #{self.spot_number} - {self.spot_type}"


if __name__ == "__main__":
    # Create parking spots (1-10 with different sizes)
    parking_spots = {}
    spot_sizes = ["small", "medium", "large"]  # Possible sizes

    for i in range(1, 11):  # Spot numbers from 1 to 10
        spot_size = spot_sizes[(i - 1) % len(spot_sizes)]  # Rotate between sizes
        parking_spots[i] = ParkingSpot(i, None, spot_size)  # Vehicle type initially not assigned

    # Create non-parking spots (11-20)
    non_parking_spots = {
        11: NonParkingSpot(11, "Entrance"),
        12: NonParkingSpot(12, "Exit"),
        13: NonParkingSpot(13, "Walkway"),
        14: NonParkingSpot(14, "Grass"),
        15: NonParkingSpot(15, "Garden"),
        16: NonParkingSpot(16, "Play Area"),
        17: NonParkingSpot(17, "Storage"),
        18: NonParkingSpot(18, "Maintenance"),
        19: NonParkingSpot(19, "Waiting Area"),
        20: NonParkingSpot(20, "Loading Zone"),
    }

    # Combine parking and non-parking spots for unified checking
    all_spots = {**parking_spots, **non_parking_spots}

    # Define vehicle size requirements
    vehicle_sizes = {
        "motorcycle": "small",
        "car": "medium",
        "truck": "large",
        
    }

    # Function to check compatibility of spot size with vehicle size
    def is_spot_suitable(spot_size, required_size):
        """Check if a parking spot can accommodate a given vehicle."""
        size_hierarchy = ["small", "medium", "large"]
        return size_hierarchy.index(spot_size) >= size_hierarchy.index(required_size)

    # Interactive menu
    while True:
        print("\nOptions:")
        print("1. Check if a spot is suitable for your vehicle type")
        print("2. View all spots")
        print("3. Exit")

        # Get user choice
        choice = input("\nEnter your choice (1/2/3): ")

        if choice == "1":
            # Check if a spot is suitable
            try:
                spot_number = int(input("Enter the spot number to check (1-20): "))
                vehicle_type = input("Enter your vehicle type (e.g., motorcycle, car, truck): ").strip().lower()

                if spot_number in parking_spots:
                    # Get the spot size and required vehicle size
                    spot_size = parking_spots[spot_number].size
                    required_size = vehicle_sizes.get(vehicle_type)

                    if not required_size:
                        print(f"Unknown vehicle type: {vehicle_type}. Please enter a valid vehicle type.")
                    elif is_spot_suitable(spot_size, required_size):
                        print(f"Yes, Spot #{spot_number} is suitable for a {vehicle_type}.")
                    else:
                        print(f"No, Spot #{spot_number} is too small for a {vehicle_type}.")
                elif spot_number in non_parking_spots:
                    print(f"Spot #{spot_number} is a non-parking spot: {non_parking_spots[spot_number].spot_type}.")
                else:
                    print("Invalid spot number! Please choose a number between 1 and 20.")
            except ValueError:
                print("Please enter a valid integer for the spot number.")

        elif choice == "2":
            # View all spots
            print("\nCurrent parking spots:")
            for spot_number, spot in parking_spots.items():
                status = "Occupied" if spot.is_occupied else "Vacant"
                print(f"Spot #{spot_number} - {spot.size.capitalize()} - {status}")

            print("\nNon-Parking Spots:")
            for spot in non_parking_spots.values():
                print(f"NonParkingSpot #{spot.spot_number} - {spot.spot_type}")

        elif choice == "3":
            # Exit the program
            print("Exiting...")
            break

        else:
            print("Invalid choice! Please enter 1, 2, or 3.")



    

 
