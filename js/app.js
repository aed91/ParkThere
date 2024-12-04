/* Check if service worker is supported on the browser. 
   The purpose is to enable offline capabilities and enhance performance 
   by utilizing the service worker for caching and background sync. */
   if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js')
        .then(() => console.log('Service worker registered'))
        .catch(error => console.error('Service worker not registered', error));
}


/* Function to fetch parking spot data from the backend API */
async function fetchParkingData() {
    const API_URL = 'http://127.0.0.1:5000/get-data'; // Updated API endpoint for fetching parking data
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Fetched data:', data); // Log the fetched data to ensure it's correct
        updateParkingLot(data); // Update the parking lot UI with the fetched data
        cacheParkingData(data); // Optionally cache the fetched data
    } catch (error) {
        console.error('Error fetching parking data:', error);
        
        // Handle offline state: Optionally show a fallback message or display cached data
        handleOfflineState();
    }
}

/* Function to update the UI with parking spot information */
function updateParkingLot(data) {
    const parkingLotContainer = document.getElementById('parking-lot');
    parkingLotContainer.innerHTML = ''; // Clear existing spots

    if (!Array.isArray(data) || data.length === 0) {
        showErrorMessage("No parking data available.");
        return;
    }

    const fragment = document.createDocumentFragment();

    data.forEach(spot => {
        if (!spot.status || (spot.status !== 'available' && spot.status !== 'occupied')) return; // Skip invalid spots

        const spotDiv = document.createElement('div');
        spotDiv.classList.add('parking-spot');

        if (spot.status === 'available') {
            spotDiv.classList.add('available');
            spotDiv.textContent = 'Available';
        } else if (spot.status === 'occupied') {
            spotDiv.classList.add('occupied');
            spotDiv.textContent = 'Occupied';
        }

        fragment.appendChild(spotDiv);
    });

    parkingLotContainer.appendChild(fragment);
}

/* Cache the fetched parking data for offline use */
async function cacheParkingData(data) {
    try {
        const cache = await caches.open('site-dynamic-v2');
        cache.put('/parking-data', new Response(JSON.stringify(data)));
    } catch (error) {
        console.error('Error caching parking data:', error);
    }
}

/* Function to get cached parking data (if available) */
async function getCachedParkingData() {
    try {
        const cache = await caches.open('site-dynamic-v2');
        const cachedResponse = await cache.match('/parking-data');
        return cachedResponse ? cachedResponse.json() : null;
    } catch (error) {
        console.error('Error getting cached parking data:', error);
        return null;
    }
}

/* Function to handle offline state */
async function handleOfflineState() {
    const cachedData = await getCachedParkingData();
    if (cachedData) {
        updateParkingLot(cachedData);
        showErrorMessage("You are seeing cached data. The app couldn't fetch live data.");
    } else {
        showErrorMessage("Unable to fetch parking data. Please check your internet connection.");
    }
}

/* Function to show an error message in the UI */
function showErrorMessage(message) {
    const parkingLotContainer = document.getElementById('parking-lot');
    parkingLotContainer.innerHTML = `<p class="error-message">${message}</p>`;
}

/* Initialize and fetch parking data when the page is loaded */
document.addEventListener('DOMContentLoaded', fetchParkingData);
