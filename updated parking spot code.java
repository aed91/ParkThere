package ParkingSpot;

public class ParkingSpot {
	private int spotNumber;
    private boolean isOccupied;
    private String vehicleType; 

    public ParkingSpot(int spotNumber, String vehicleType) {
        this.spotNumber = spotNumber;
        this.vehicleType = vehicleType;
        this.isOccupied = false; 
    }

    public int getSpotNumber() {
        return spotNumber;
    }

    public boolean isOccupied() {
        return isOccupied;
    }

    public void occupySpot() {
        if (!isOccupied) {
            isOccupied = true;
        } else {
            System.out.println("Spot is already occupied!");
        }
    }

    public void vacateSpot() {
        if (isOccupied) {
            isOccupied = false;
        } else {
            System.out.println("Spot is already vacant!");
        }
    }

    public String getVehicleType() {
        return vehicleType;
    }

    
    public String toString() {
        return "ParkingSpot #" + spotNumber + " for " + vehicleType + " - " + (isOccupied ? "Occupied" : "Available");
    }

}