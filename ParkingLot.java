package ParkingLot;


import com.myproject.parkingmonitor.model.NonParkingSpot;

import ParkingSpot.String;

public class ParkingLot {
	public interface Spot {
		int getSpotNumber();
	}
	public class ParkingSpot implements Spot {
	    private int spotNumber;
	    private boolean isOccupied;
	    private String vehicleType;

	    public ParkingSpot(int spotNumber String vehicleType) {
	        this.spotNumber = spotNumber;
	        this.vehicleType = vehicleType;
	        this.isOccupied = false;
	    

	    
	    public int getSpotNumber() {
	        return spotNumber;
	    }

	    public boolean isOccupied() {
	        return isOccupied;
	    }

	    public void occupySpot() {
	        isOccupied = true;
	    }

	    public void vacateSpot() {
	        isOccupied = false;
	    }

	    
	    public String toString() {
	    	return "ParkingSpot #" + spotNumber + " for " + vehicleType + " - " + (isOccupied ? "Occupied" : "Available");

	    }
	}}

