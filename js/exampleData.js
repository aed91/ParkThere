// exampleData.js

// Sample data for available and taken parking spots by row
const exampleData = {
    available: [
        { row: "A", spots: 5 }, // 5 spots in row A
        { row: "B", spots: 3 }, // 3 spots in row B
        { row: "C", spots: 2 }, // 2 spots in row C
    ],
    taken: [
        { row: "A", spots: 2 }, // 2 spots in row A
        { row: "B", spots: 4 }, // 4 spots in row B
    ]
};

// Function to display example data in the HTML
function displayExampleData() {
    const availableList = document.getElementById('available-spots');
    const takenList = document.getElementById('taken-spots');

    // Populate available spots
    exampleData.available.forEach(entry => {
        const li = document.createElement('li');
        li.textContent = `Row ${entry.row}: ${entry.spots} spot(s) available`;
        availableList.appendChild(li);
    });

    // Populate taken spots
    exampleData.taken.forEach(entry => {
        const li = document.createElement('li');
        li.textContent = `Row ${entry.row}: ${entry.spots} spot(s) taken`;
        takenList.appendChild(li);
    });
}

// Call the function to display the data when the script loads
displayExampleData();
