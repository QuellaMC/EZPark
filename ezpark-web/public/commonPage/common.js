document.addEventListener('DOMContentLoaded', () => {
    // 加载收藏数据
    loadCommon();

    // 检查 localStorage 中是否有用户信息
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
        document.getElementById('loginRegisterLink').style.display = 'none';
        document.getElementById('userInfo').style.display = 'block';
        document.getElementById('usernameDisplay').textContent = storedUsername;
    }

    document.getElementById('logoutLink').addEventListener('click', (event) => {
        event.preventDefault();
        const confirmLogout = confirm('Are you sure you want to logout?');
        if (confirmLogout) {
            fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loginRegisterLink').style.display = 'block';
                document.getElementById('userInfo').style.display = 'none';
                document.getElementById('usernameDisplay').textContent = '';
                localStorage.removeItem('username');
                localStorage.removeItem('token');
                window.location.href = 'index.html';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
});

function loadCommon() {
    fetch('/api/getFavorites', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(response => response.json())
    .then(data => {
        fetch('../res/map/json/locations.json') // 修改为实际的 JSON 文件路径
        .then(response => response.json())
        .then(locations => {
            const favoritesList = document.getElementById('favoritesList');
            favoritesList.innerHTML = '';
            if (data.favoriteParkingLots && data.favoriteParkingLots.length > 0) {
                data.favoriteParkingLots.forEach(uid => {
                    const location = locations.find(loc => loc.uid === uid);
                    if (location) {
                        const listItem = document.createElement('div');
                        listItem.className = 'favorite-item-container';
                        listItem.innerHTML = `
                            <div class="favorite-item">
                                <p>${location.name}</p>
                                <div class="favorite-item-buttons">
                                    <button onclick="navigateToParking('${location.url}')">Navigate</button>
                                    <button onclick="removeFromFavorites('${uid}')">Remove</button>
                                    <button onclick="shareParking('${location.url}')">Share</button>
                                </div>
                            </div>
                        `;
                        favoritesList.appendChild(listItem);
                    }
                });
            } else {
                favoritesList.textContent = 'No favorites found.';
            }
        })
        .catch(error => console.error('Error loading locations:', error));
    })
    .catch(error => console.error('Error:', error));
}

function navigateToParking(url) {
    // 导航到停车场的逻辑
    window.open(url, '_blank');
}

function removeFromFavorites(uid) {
    fetch('/api/removeFavorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ removeUid: uid })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
        } else {
            alert('Removed from favorites successfully');
            loadCommon();
        }
    })
    .catch(error => console.error('Error:', error));
}

function shareParking(url) {
    // 分享停车场的逻辑
    navigator.clipboard.writeText(url).then(() => {
        alert('Parking lot URL copied to clipboard');
    }).catch(err => {
        console.error('Error copying to clipboard:', err);
    });
}