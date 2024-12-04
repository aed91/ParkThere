// Function to fetch parking spot data from an API
async function fetchParkingData() {
  const API_URL = '/parking-data'; // API endpoint for fetching parking data
  try {
      const response = await fetch(API_URL); // Fetch data from backend API
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      const data = await response.json(); // Parse the response as JSON
      updateParkingLot(data); // Update the parking lot UI with the fetched data
  } catch (error) {
      console.error('Error fetching parking data:', error);

      // Handle offline state: Optionally show a fallback message or display cached data
      const cachedData = await getCachedParkingData();
      if (cachedData) {
          updateParkingLot(cachedData); // Use cached data to update the UI
          showErrorMessage("You are seeing cached data. The app couldn't fetch live data.");
      } else {
          showErrorMessage("Unable to fetch parking data. Please check your internet connection.");
      }
  }
}

// Function to update the UI with parking spot information
function updateParkingLot(data) {
  const parkingLotContainer = document.getElementById('parking-spot-display'); // Use existing container

  // Check if parking-spot-display element exists before attempting to update
  if (!parkingLotContainer) {
      console.error("Parking spot display container element not found.");
      return;
  }

  parkingLotContainer.innerHTML = ''; // Clear the existing parking spots

  // Check for empty or invalid data
  if (!Array.isArray(data) || data.length === 0) {
      showErrorMessage("No parking data available.");
      return;
  }

  // Use DocumentFragment for efficient DOM manipulation
  const fragment = document.createDocumentFragment();

  // Loop through each parking spot in the data
  data.forEach(spot => {
      // Validate the data for each parking spot
      if (!spot.status || (spot.status !== 'available' && spot.status !== 'occupied')) {
          return; // Skip invalid spot data
      }

      const spotDiv = document.createElement('div');
      spotDiv.classList.add('parking-spot'); // Add base class for styling

      // Apply different classes based on the status of the parking spot
      if (spot.status === 'available') {
          spotDiv.classList.add('available'); // Green border for available spots
          spotDiv.textContent = 'Available';
      } else if (spot.status === 'occupied') {
          spotDiv.classList.add('occupied'); // Red border for occupied spots
          spotDiv.textContent = 'Occupied';
      }

      fragment.appendChild(spotDiv); // Add the spot div to the fragment
  });

  parkingLotContainer.appendChild(fragment); // Append the fragment to the container
}

// Function to get cached parking data (if available)
async function getCachedParkingData() {
  const cache = await caches.open('site-dynamic-v2');
  const cachedResponse = await cache.match('/parking-data');
  if (cachedResponse) {
      return cachedResponse.json(); // Return the cached data
  }
  return null;
}

// Function to show an error message in the UI
function showErrorMessage(message) {
  const parkingLotContainer = document.getElementById('parking-spot-display'); // Use existing container

  // Check if the parking spot display container is available
  if (parkingLotContainer) {
      parkingLotContainer.innerHTML = `<p class="error-message">${message}</p>`;
  } else {
      console.error("Parking spot display container element not found to display error message.");
  }
}

// Initialize and fetch parking data when the page is loaded
document.addEventListener('DOMContentLoaded', fetchParkingData);
