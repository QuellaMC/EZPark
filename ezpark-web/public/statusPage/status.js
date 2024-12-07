document.addEventListener('DOMContentLoaded', () => {
    // Load parking lot status data
    loadStatus();

    // Load parking lot location options
    loadParkingLocations();

    // Get modal elements
    const modal = document.getElementById('reportModal');
    const btn = document.getElementById('reportButton');
    const span = document.getElementsByClassName('close')[0];

    // When the user clicks the button, open the modal
    btn.onclick = function() {
        modal.style.display = 'block';
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = 'none';
    }

    // When the user clicks outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // Handle report form submission
    document.getElementById('reportForm').addEventListener('submit', event => {
        event.preventDefault();
        reportStatus();
    });
});

function loadStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            const statusList = document.getElementById('statusList');
            statusList.innerHTML = '';
            for (const [location, statuses] of Object.entries(data)) {
                if (statuses.length > 0) {
                    const latestStatus = statuses[statuses.length - 1];
                    const statusElement = document.createElement('div');
                    statusElement.className = 'status-item';
                    statusElement.innerHTML = `
                        <h3>${location}</h3>
                        <p>Time: ${latestStatus.time}</p>
                        <p>Is parking tight: ${latestStatus.isTight ? 'Yes' : 'No'}</p>
                        <p>Remaining spots: ${latestStatus.remainingSpots}</p>
                    `;
                    statusList.appendChild(statusElement);
                }
            }
        })
        .catch(error => console.error('Error loading parking lot data:', error));
}

function loadParkingLocations() {
    fetch('../res/map/json/locations.json')
        .then(response => response.json())
        .then(locations => {
            const locationSelect = document.getElementById('location');
            locations.forEach(location => {
                const option = document.createElement('option');
                option.value = location.name;
                option.textContent = location.name;
                locationSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading parking locations:', error));
}

function reportStatus() {
    const time = document.getElementById('time').value;
    const location = document.getElementById('location').value;
    const remainingSpots = document.getElementById('remainingSpots').value;

    const newStatus = {
        time: time,
        isTight: remainingSpots <= 10, // Assume parking is tight if remaining spots are 10 or less
        remainingSpots: parseInt(remainingSpots)
    };

    fetch('/api/status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ location, newStatus })
    })
    .then(response => response.text())
    .then(message => {
        loadStatus();
        alert(message);
        document.getElementById('reportModal').style.display = 'none';
    })
    .catch(error => console.error('Error reporting status:', error));
}