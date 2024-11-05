package NonParkingSpot;

public class NonParkingSpot {
	 private int spotNumber;
	    private String spotType;

	    public NonParkingSpot(int spotNumber, String spotType) {
	        this.spotNumber = spotNumber;
	        this.spotType = spotType;
	    }

	    public int getSpotNumber() {
	        return spotNumber;
	    }

	    public String getSpotType() {
	        return spotType;
	    }

	    
	    public String toString() {
	        return "NonParkingSpot #" + spotNumber + " - " + spotType;
	    }

}
