//This updated ui.js file not only initializes the navigation menus and forms but also dynamically displays the available 
//and occupied parking spots based on the provided example data. You can easily replace the example data with real data when available.

const recipes = document.querySelector('.recipes');
const availableSpotsList = document.getElementById('available-spots');
const takenSpotsList = document.getElementById('taken-spots');

document.addEventListener('DOMContentLoaded', function() {
  // Initialize side navigation menu
  const menus = document.querySelectorAll('.side-menu');
  M.Sidenav.init(menus, { edge: 'right' });

  // Initialize add recipe form
  const forms = document.querySelectorAll('.side-form');
  M.Sidenav.init(forms, { edge: 'left' });

  // Display example data for parking spots
  displayParkingSpots(exampleData);
});

// Function to display parking spots data
function displayParkingSpots(data) {
  // Clear existing entries
  availableSpotsList.innerHTML = '';
  takenSpotsList.innerHTML = '';

  // Populate available spots
  data.available.forEach(entry => {
    const li = document.createElement('li');
    li.textContent = `Row ${entry.row}: ${entry.spots} spot(s) available`;
    availableSpotsList.appendChild(li);
  });

  // Populate occupied spots
  data.taken.forEach(entry => {
    const li = document.createElement('li');
    li.textContent = `Row ${entry.row}: ${entry.spots} spot(s) occupied`;
    takenSpotsList.appendChild(li);
  });
}

// Example data structure to be passed to the display function
const exampleData = {
  available: [
    { row: "A", spots: 5 },
    { row: "B", spots: 3 },
    { row: "C", spots: 2 },
    { row: "D", spots: 4 },
    { row: "E", spots: 1 },
  ],
  taken: [
    { row: "A", spots: 2 },
    { row: "B", spots: 4 },
    { row: "C", spots: 1 },
    { row: "D", spots: 0 },
    { row: "E", spots: 3 },
  ]
};

