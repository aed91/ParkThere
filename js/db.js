// Enable offline data persistence
db.enablePersistence()
  .catch(function(err) {
    if (err.code === 'failed-precondition') {
      // Likely due to multiple tabs open at once
      console.log('Persistence failed');
    } else if (err.code === 'unimplemented') {
      // Lack of browser support for the feature
      console.log('Persistence not available');
    }
  });

// Real-time listener for parking spots
db.collection('parkingSpots').onSnapshot(snapshot => {
  snapshot.docChanges().forEach(change => {
    if (change.type === 'added') {
      renderParkingSpot(change.doc.data(), change.doc.id);
    }
    if (change.type === 'removed') {
      removeParkingSpot(change.doc.id);
    }
    // Optional: You can also handle 'modified' changes here if needed
    if (change.type === 'modified') {
      updateParkingSpot(change.doc.data(), change.doc.id);
    }
  });
});

// Function to render a new parking spot
function renderParkingSpot(data, id) {
  const spot = document.createElement('div');
  spot.classList.add(data.status === 'available' ? 'available' : 'occupied'); // Use 'occupied' for a taken spot
  spot.textContent = `Row: ${data.row} - Spot ID: ${id} - Status: ${data.status}`;

  // Assuming there's a container to display parking spots in your HTML
  const parkingSpotContainer = document.querySelector('.parking-spots');
  const spotElement = document.createElement('div');
  spotElement.classList.add('parking-spot');
  spotElement.setAttribute('data-id', id);
  spotElement.appendChild(spot);
  
  parkingSpotContainer.appendChild(spotElement);
}

// Function to update an existing parking spot (in case of modifications)
function updateParkingSpot(data, id) {
  const spotElement = document.querySelector(`[data-id="${id}"]`);
  if (spotElement) {
    const spot = spotElement.querySelector('div');
    spot.classList.remove('available', 'occupied');
    spot.classList.add(data.status === 'available' ? 'available' : 'occupied');
    spot.textContent = `Row: ${data.row} - Spot ID: ${id} - Status: ${data.status}`;
  }
}

// Function to remove a parking spot
function removeParkingSpot(id) {
  const spotElement = document.querySelector(`[data-id="${id}"]`);
  if (spotElement) {
    spotElement.remove();
  }
}

// Form handling for adding parking spots
const form = document.querySelector('form');
form.addEventListener('submit', evt => {
  evt.preventDefault();

  // Collect data from the form
  const parkingSpot = {
    row: form.row.value, // e.g., "A"
    status: form.status.value // either 'available' or 'taken'
  };

  // Add new parking spot to Firestore
  db.collection('parkingSpots').add(parkingSpot)
    .catch(err => console.log('Error adding parking spot:', err));

  // Clear the form inputs
  form.row.value = '';
  form.status.value = '';
});

// Remove a parking spot (triggered by a click on an element with a delete button or icon)
const parkingSpotContainer = document.querySelector('.parking-spots');
parkingSpotContainer.addEventListener('click', evt => {
  if (evt.target.tagName === 'I' && evt.target.getAttribute('data-id')) {
    const id = evt.target.getAttribute('data-id');
    db.collection('parkingSpots').doc(id).delete()
      .catch(err => console.log('Error deleting parking spot:', err));
  }
});
