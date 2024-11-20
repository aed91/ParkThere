// Sample data for parking spots (used if API is unavailable)
const exampleData = [
  { spot_id: 1, status: 'available', row: "A", x: 0, y: 0 },
  { spot_id: 2, status: 'taken', row: "A", x: 1, y: 0 },
  { spot_id: 3, status: 'available', row: "B", x: 0, y: 1 },
  { spot_id: 4, status: 'taken', row: "B", x: 1, y: 1 },
  { spot_id: 5, status: 'available', row: "C", x: 0, y: 2 },
  // More sample data...
];

// Initialize DOM elements for displaying parking spots
const availableSpotsList = document.getElementById('available-spots');
const takenSpotsList = document.getElementById('taken-spots');

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
    const response = await fetch('/api/parking-spots');
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();
    displayParkingSpots(data); // Pass the fetched data to display function
  } catch (error) {
    console.error('Error fetching parking spots:', error);
    // Display example data if the API fetch fails
    displayParkingSpots(exampleData);
  }
}

// Function to display parking spots data
function displayParkingSpots(data) {
  // Clear existing entries in the lists
  availableSpotsList.innerHTML = '';
  takenSpotsList.innerHTML = '';

  // Sort spots by row and status
  const availableSpots = data.filter(spot => spot.status === 'available');
  const takenSpots = data.filter(spot => spot.status === 'taken');

  // Populate available spots list
  availableSpots.forEach(entry => {
    const li = document.createElement('li');
    li.textContent = `Row ${entry.row}: Spot ${entry.spot_id} is available`;
    li.classList.add('available'); // Add class for custom styling (green border)
    availableSpotsList.appendChild(li);
  });

  // Populate taken spots list
  takenSpots.forEach(entry => {
    const li = document.createElement('li');
    li.textContent = `Row ${entry.row}: Spot ${entry.spot_id} is occupied`;
    li.classList.add('taken'); // Add class for custom styling (red border)
    takenSpotsList.appendChild(li);
  });
}

// Initial call to display parking spots (in case the API is not available on first load)
displayParkingSpots(exampleData);
