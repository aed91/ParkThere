// Initialize DOM elements for displaying parking spots
const availableSpotsList = document.getElementById('available-spots');
const takenSpotsList = document.getElementById('taken-spots');
const totalSpotsElement = document.getElementById('total-spots');
const lastUpdatedElement = document.getElementById('last-updated');

// Wait for the DOM content to load before initializing UI elements
document.addEventListener('DOMContentLoaded', function() {
  // Initialize side navigation menu for mobile devices
  const menus = document.querySelectorAll('.side-menu');
  M.Sidenav.init(menus, { edge: 'right' });

  // Initialize add recipe form (adjust if needed for your use case)
  const forms = document.querySelectorAll('.side-form');
  M.Sidenav.init(forms, { edge: 'left' });

  // Fetch parking spot data from backend API and display it
  fetchParkingSpots();
});

// Function to fetch parking spots data from the backend API
async function fetchParkingSpots() {
  try {
    const response = await fetch('/get-data'); // Corrected endpoint
    if (!response.ok) throw new Error('Network response was not ok');
    const result = await response.json();

    // Log the full response for debugging
    console.log('API Response:', result);

    // Extract the data from the API response
    const parkingData = result.csv_data[0]; // Assuming there's only one object in csv_data

    // Log the specific extracted data for debugging
    console.log('Extracted Parking Data:', parkingData);

    // Display the total spots and the last updated timestamp
    displayTotalSpots(parkingData.total_spots, parkingData.last_updated);

    // Display the number of available and occupied spots
    displaySpotCounts(parkingData.free_spots, parkingData.occupied_spots);
  } catch (error) {
    console.error('Error fetching parking spots:', error);
    // Display example data if the API fetch fails
    displaySpotCounts(0, 0);
  }
}

// Function to display total spots and last updated info
function displayTotalSpots(total, lastUpdated) {
  if (totalSpotsElement) {
    totalSpotsElement.textContent = `Total Spots: ${total}`;
  } else {
    console.error('Total spots element not found');
  }

  if (lastUpdatedElement) {
    lastUpdatedElement.textContent = `Last Updated: ${new Date(lastUpdated).toLocaleString()}`;
  } else {
    console.error('Last updated element not found');
  }
}

// Function to display the counts of available and occupied spots
function displaySpotCounts(freeSpots, occupiedSpots) {
  // Clear existing entries in the lists
  if (availableSpotsList) {
    availableSpotsList.innerHTML = '';
  } else {
    console.error('Available spots list not found');
  }

  if (takenSpotsList) {
    takenSpotsList.innerHTML = '';
  } else {
    console.error('Taken spots list not found');
  }

  // Display available spots count
  const availableLi = document.createElement('li');
  availableLi.textContent = `Available Spots: ${freeSpots}`;
  availableLi.classList.add('available'); // Add class for custom styling (green border)
  if (availableSpotsList) {
    availableSpotsList.appendChild(availableLi);
  }

  // Display occupied spots count
  const takenLi = document.createElement('li');
  takenLi.textContent = `Occupied Spots: ${occupiedSpots}`;
  takenLi.classList.add('taken'); // Add class for custom styling (red border)
  if (takenSpotsList) {
    takenSpotsList.appendChild(takenLi);
  }
}

// Initial call to display parking spots (in case the API is not available on first load)
displaySpotCounts(0, 0);

// Optional: Periodic data refresh every 5 seconds
setInterval(fetchParkingSpots, 5000);
