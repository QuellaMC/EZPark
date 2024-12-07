const radius = 70; // Radius of the circle
const circumference = 2 * Math.PI * radius;
const progressCircle = document.querySelector('.progress-ring__foreground');
const availabilityText = document.getElementById('availabilityText');

// Set the circumference of the circle
progressCircle.style.strokeDasharray = `${circumference}`;

// Function to set progress based on percentage
function setProgress(percent) {
    const offset = circumference - (percent / 100) * circumference;
    progressCircle.style.strokeDashoffset = offset;

    // Change color based on availability
    if (percent > 70) {
        progressCircle.style.stroke = "green";
    } else if (percent > 30) {
        progressCircle.style.stroke = "yellow";
    } else {
        progressCircle.style.stroke = "red";
    }

    availabilityText.textContent = `${percent}%`;
}

// Example: Fetch availability from the server
function fetchAvailability() {
    fetch('/api/crowd-level') // Replace with your API endpoint
        .then(response => response.json())
        .then(data => {
            const availability = data.availability; // Assume API returns { "availability": 70 }
            setProgress(availability);
        })
        .catch(error => {
            console.error('Error fetching availability:', error);
            availabilityText.textContent = "Error";
        });
}

// Fetch availability on page load
fetchAvailability();
