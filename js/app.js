/* Check if service worker is supported on the browser. 
   The purpose is to enable offline capabilities and enhance performance 
   by utilizing the service worker for caching and background sync. */
   if ('serviceWorker' in navigator) {
    // Register the service worker for offline and caching functionality
    navigator.serviceWorker.register('/sw.js')
        .then((reg) => {
            console.log('Service worker registered', reg);
        })
        .catch((err) => {
            console.log('Service worker not registered', err);
        });
}

/* Function to fetch parking spot data from the backend API */
async function fetchParkingData() {
    try {
        const response = await fetch('https://your-api-endpoint.com/parking-data');  // Replace with actual API endpoint
        const data = await response.json();  // Parse the response as JSON
        updateParkingLot(data);  // Update the parking lot UI with the fetched data
    } catch (error) {
        console.error('Error fetching parking data:', error);
        
        // Handle offline state: Optionally show a fallback message or display cached data
        const cachedData = await getCachedParkingData();
        if (cachedData) {
            updateParkingLot(cachedData);  // Use cached data to update the UI
        } else {
            showErrorMessage("Unable to fetch parking data. Please check your internet connection.");
        }
    }
}

/* Function to update the UI with parking spot information */
function updateParkingLot(data) {
    const parkingLotContainer = document.getElementById('parking-lot');  // Reference to the container where spots will be displayed
    parkingLotContainer.innerHTML = '';  // Clear the existing parking spots

    // Loop through each parking spot in the data
    data.forEach(spot => {
        const spotDiv = document.createElement('div');
        spotDiv.classList.add('parking-spot');  // Add base class for styling

        // Apply different classes based on the status of the parking spot
        if (spot.status === 'available') {
            spotDiv.classList.add('available');  // Green border for available spots
            spotDiv.textContent = 'Available';
        } else if (spot.status === 'occupied') {
            spotDiv.classList.add('occupied');  // Red border for occupied spots
            spotDiv.textContent = 'Occupied';
        }

        parkingLotContainer.appendChild(spotDiv);  // Add the spot div to the container
    });
}

/* Function to get cached parking data (if available) */
async function getCachedParkingData() {
    const cache = await caches.open('site-dynamic-v2');
    const cachedResponse = await cache.match('/parking-data');
    if (cachedResponse) {
        return cachedResponse.json();  // Return the cached data
    }
    return null;
}

/* Function to show an error message in the UI */
function showErrorMessage(message) {
    const parkingLotContainer = document.getElementById('parking-lot');
    parkingLotContainer.innerHTML = `<p class="error-message">${message}</p>`;
}

/* Initialize and fetch parking data when the page is loaded */
document.addEventListener('DOMContentLoaded', fetchParkingData);
