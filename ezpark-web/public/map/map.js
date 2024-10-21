class Location {
    constructor(uid, x, y, scale, info, url, embedUrl) {
        this.uid = uid;
        this.x = x;
        this.y = y;
        this.scale = scale;
        this.info = info;
        this.url = url;
        this.embedUrl = embedUrl;
    }
}

let currentZoom = {
    x: 0,
    y: 0,
    scale: 1,
    info: ''
};
let currentLocationUid = '';
let currentEmbedUrl = '';
let locations = new Map();

fetch('../res/map/json/locations.json')
    .then(response => response.json())
    .then(data => {
        data.forEach(item => {
            const location = new Location(item.uid, item.x, item.y, item.scale, item.info, item.url, item.embedUrl);
            locations.set(item.name, location);
        });
    })
    .catch(error => console.error('Error loading locations:', error));

function zoomToLocation(location) {
    const { uid, x, y, scale, info, url, embedUrl } = location;
    currentZoom = { x, y, scale, info };
    applyZoom();
    updateCoordinatesDisplay();
    const parkingInfo = document.getElementById('parking-info');
    if (info) {
        parkingInfo.innerText = info;
        parkingInfo.style.display = 'block';
        document.getElementById('parkingButtons').style.display = 'flex';
        currentLocationUid = uid;
        mapIframe.src = embedUrl;
    } else {
        parkingInfo.style.display = 'none';
        document.getElementById('parkingButtons').style.display = 'none';
        currentLocationUid = '';
        mapIframe.src = '';
    }
}

function applyZoom() {
    const { x, y, scale, info } = currentZoom;
    const map = document.getElementById('map');
    const container = map.parentElement;

    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    const originalWidth = map.naturalWidth;
    const originalHeight = map.naturalHeight;

    const containerAspectRatio = containerWidth / containerHeight;
    const imageAspectRatio = originalWidth / originalHeight;

    const scaleFactor = Math.max(
        containerWidth / originalWidth,
        containerHeight / originalHeight
    );

    const displayedImageWidth = originalWidth * scaleFactor;
    const displayedImageHeight = originalHeight * scaleFactor;

    const cropX = (displayedImageWidth - containerWidth) / 2;
    const cropY = (displayedImageHeight - containerHeight) / 2;

    const adjustedX = x * scaleFactor - cropX;
    const adjustedY = y * scaleFactor - cropY;

    const containerCenterX = containerWidth / 2;
    const containerCenterY = containerHeight / 2;

    const offsetX = adjustedX * scale - containerCenterX;
    const offsetY = adjustedY * scale - containerCenterY;

    map.style.transform = `translate(${-offsetX}px, ${-offsetY}px) scale(${scale})`;
}

function resetZoom() {
    const map = document.getElementById('map');
    const container = map.parentElement;

    const originalWidth = map.naturalWidth;
    const originalHeight = map.naturalHeight;

    const scaleFactor = Math.max(
        container.clientWidth / originalWidth,
        container.clientHeight / originalHeight
    );

    const displayedImageWidth = originalWidth * scaleFactor;
    const displayedImageHeight = originalHeight * scaleFactor;

    const cropX = (displayedImageWidth - container.clientWidth) / 2;
    const cropY = (displayedImageHeight - container.clientHeight) / 2;

    const centerX = (container.clientWidth / 2 + cropX) / scaleFactor;
    const centerY = (container.clientHeight / 2 + cropY) / scaleFactor;

    map.style.transform = 'translate(0, 0) scale(1)';

    currentZoom = {
        x: centerX,
        y: centerY,
        scale: 1,
        info: ''
    };
    updateCoordinatesDisplay();
    document.getElementById('parking-info').style.display = 'none';
    document.getElementById('parkingButtons').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    const buttonTexts = {
        btn1: { original: "Navigate", hover: "../res/map/icon/NAV.png" },
        btn2: { original: "Add to Common", hover: "../res/map/icon/FAV.png" },
        btn3: { original: "Update Status", hover: "../res/map/icon/STA.png" },
        btn4: { original: "Share", hover: "../res/map/icon/SHR.png" }
    };

    const parkingButtons = document.getElementById('parkingButtons');
    parkingButtons.style.display = 'none';

    document.querySelectorAll('.square-button').forEach(button => {
        const btnId = button.id;
        let hoverTimeout;

        button.addEventListener('mouseover', () => {
            hoverTimeout = setTimeout(() => {
                button.textContent = buttonTexts[btnId].original;
            }, 100);
        });

        button.addEventListener('mouseout', () => {
            clearTimeout(hoverTimeout);
            setTimeout(() => {
                button.innerHTML = `<img src="${buttonTexts[btnId].hover}" class="icon" alt="${buttonTexts[btnId].original}">`;
            }, 100);
        });

        button.addEventListener('click', () => {
            if (btnId === 'btn1') {
                document.getElementById('mapModal').style.display = 'block';
            } else if (btnId === 'btn2') {
                if (currentLocationUid) {
                    fetch('/api/getFavorites', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            console.error('Error:', data.error);
                        } else {
                            const favoriteParkingLots = data.favoriteParkingLots || [];
                            if (!favoriteParkingLots.includes(currentLocationUid)) {
                                favoriteParkingLots.push(currentLocationUid);
                                fetch('/api/updateFavorites', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                                    },
                                    body: JSON.stringify({ favoriteParkingLots })
                                })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.error) {
                                        console.error('Error:', data.error);
                                    } else {
                                        alert('Added to favorites successfully');
                                    }
                                })
                                .catch(error => console.error('Error:', error));
                            } else {
                                alert('This parking lot is already in your favorites');
                            }
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }
            } else if (btnId === 'btn3') {
                // 更新停车场状态
            } else if (btnId === 'btn4') {
                // 分享停车场
            }
        });
    });

    window.addEventListener('click', function(event) {
        const modal = document.getElementById('mapModal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    document.getElementById('appleMaps').addEventListener('click', () => {
        window.open('http://maps.apple.com/?q=location', '_blank');
        document.getElementById('mapModal').style.display = 'none';
    });

    document.getElementById('googleMaps').addEventListener('click', () => {
        window.open(currentLocationUrl, '_blank');
        document.getElementById('mapModal').style.display = 'none';
    });
});

function moveMap(direction) {
    const moveStep = 50 / currentZoom.scale;
    switch (direction) {
        case 'up':
            currentZoom.y -= moveStep;
            break;
        case 'down':
            currentZoom.y += moveStep;
            break;
        case 'left':
            currentZoom.x -= moveStep;
            break;
        case 'right':
            currentZoom.x += moveStep;
            break;
    }
    updateCoordinatesDisplay();
    applyZoom();
}

function updateCoordinatesDisplay() {
    const coordinatesDisplay = document.getElementById('coordinatesDisplay');
    coordinatesDisplay.innerText = `X: ${currentZoom.x.toFixed(2)}, Y: ${currentZoom.y.toFixed(2)}`;
}

function changeZoom(direction) {
    const zoomStep = 0.2;
    if (direction === 'in') {
        currentZoom.scale += zoomStep;
    } else if (direction === 'out') {
        currentZoom.scale = Math.max(0.1, currentZoom.scale - zoomStep);
    }
    applyZoom();
    updateCoordinatesDisplay();
}

function toggleCollapsible() {
    const content = document.getElementById('collapsibleContent');
    if (content.style.maxHeight) {
        content.style.maxHeight = null;
    } else {
        content.style.maxHeight = content.scrollHeight + "px";
    }
}

window.addEventListener('resize', applyZoom);
window.addEventListener('load', resetZoom);