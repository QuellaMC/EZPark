document.addEventListener('DOMContentLoaded', () => {
    // 获取所有菜单链接和页面部分
    const links = document.querySelectorAll('.sidebar a');
    const pages = document.querySelectorAll('.page');

    // 为每个菜单项添加点击事件监听器
    links.forEach(link => {
        link.addEventListener('click', function(event) {
            // 获取目标页面的 ID
            const targetId = this.getAttribute('data-target');
            console.log(`Target ID: ${targetId}`);

            // 如果目标 ID 为 null，允许默认链接行为
            if (!targetId) {
                console.error('Target ID is null');
                return;
            }

            // 检查是否点击了 "My Common" 链接
            if (targetId === 'page4') {
                const token = localStorage.getItem('token');
                if (!token) {
                    // 如果未登录，显示登录模态框并阻止导航
                    event.preventDefault();
                    document.getElementById('authModal').style.display = 'block';
                    return;
                }
            }

            // 阻止默认链接行为
            event.preventDefault();

            // 隐藏所有页面
            pages.forEach(page => {
                page.classList.remove('active');
            });

            // 显示目标页面
            const targetPage = document.getElementById(targetId);
            if (targetPage) {
                targetPage.classList.add('active');
            } else {
                console.error(`No element found with ID: ${targetId}`);
            }

            // 根据目标页面的 ID 动态更改标题
            if (targetId === 'home') {
                document.title = 'EZPark';
            } else if (targetId === 'page1') {
                document.title = 'Parking Lot Map - EZPark';
            } else if (targetId === 'page2') {
                document.title = 'Curbside Parking - EZPark';
            } else if (targetId === 'page3') {
                document.title = 'Share Parking Status - EZPark';
            } else if (targetId === 'page4') {
                document.title = 'My Common - EZPark';
            }
        });
    });

    // 登录/注册模态框相关逻辑
    const authModal = document.getElementById('authModal');
    const loginFormContainer = document.getElementById('loginFormContainer');
    const registerFormContainer = document.getElementById('registerFormContainer');
    const loginRegisterLink = document.getElementById('loginRegisterLink');
    const userInfo = document.getElementById('userInfo');
    const usernameDisplay = document.getElementById('usernameDisplay');
    const logoutLink = document.getElementById('logoutLink');
    const closeButtons = document.querySelectorAll('.close');
    const showRegisterForm = document.getElementById('showRegisterForm');
    const showLoginForm = document.getElementById('showLoginForm');
    const footer = document.getElementById('footer');

    // 检查 localStorage 中是否有用户信息
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
        loginRegisterLink.style.display = 'none';
        userInfo.style.display = 'block';
        usernameDisplay.textContent = storedUsername;
    }

    loginRegisterLink.addEventListener('click', () => {
        authModal.style.display = 'block';
        loginFormContainer.style.display = 'block';
        registerFormContainer.style.display = 'none';
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            authModal.style.display = 'none';
        });
    });

    window.addEventListener('click', (event) => {
        if (event.target === authModal) {
            authModal.style.display = 'none';
        }
    });

    showRegisterForm.addEventListener('click', (event) => {
        event.preventDefault();
        loginFormContainer.style.display = 'none';
        registerFormContainer.style.display = 'block';
    });

    showLoginForm.addEventListener('click', (event) => {
        event.preventDefault();
        loginFormContainer.style.display = 'block';
        registerFormContainer.style.display = 'none';
    });

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            const loginError = document.getElementById('loginError');
            if (data.error) {
                loginError.textContent = data.error;
            } else {
                loginError.textContent = data.message;
                loginError.style.color = 'green';
                authModal.style.display = 'none';
                loginRegisterLink.style.display = 'none';
                userInfo.style.display = 'block';
                usernameDisplay.textContent = data.user.username;
                // 存储用户名到 localStorage
                localStorage.setItem('username', data.user.username);
                localStorage.setItem('token', data.token); // 存储 token
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('registerForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;

        fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            const registerError = document.getElementById('registerError');
            if (data.error) {
                registerError.textContent = data.error;
            } else {
                registerError.textContent = data.message;
                registerError.style.color = 'green';
                authModal.style.display = 'none';
                loginRegisterLink.style.display = 'none';
                userInfo.style.display = 'block';
                usernameDisplay.textContent = username;
                // 存储用户名到 localStorage
                localStorage.setItem('username', username);
                localStorage.setItem('token', data.token); // 存储 token
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    logoutLink.addEventListener('click', (event) => {
        event.preventDefault();
        const confirmLogout = confirm('Are you sure you want to logout?');
        if (confirmLogout) {
            fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                loginRegisterLink.style.display = 'block';
                userInfo.style.display = 'none';
                usernameDisplay.textContent = '';
                // 清除 localStorage 中的用户名和 token
                localStorage.removeItem('username');
                localStorage.removeItem('token');
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    // 定期检查用户的登录状态
    setInterval(checkLoginStatus, 60000); // 每分钟检查一次

    // 定期刷新 JWT 令牌
    setInterval(refreshToken, 300000); // 每5分钟刷新一次令牌

    // 初始检查当前页面
    const activePage = document.querySelector('.page.active');
    if (activePage && activePage.id !== 'home') {
        footer.style.display = 'none';
    }
});

function loadFavorites() {
    fetch('/api/getFavorites', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const favoritesList = document.getElementById('favoritesList');
        favoritesList.innerHTML = '';
        if (data.favoriteParkingLots && data.favoriteParkingLots.length > 0) {
            data.favoriteParkingLots.forEach(uid => {
                const listItem = document.createElement('li');
                listItem.textContent = `Parking Lot UID: ${uid}`;
                favoritesList.appendChild(listItem);
            });
        } else {
            favoritesList.textContent = 'No favorites found.';
        }
    })
    .catch(error => console.error('Error:', error));
}

function checkLoginStatus() {
    fetch('/api/checkToken', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(response => {
        if (response.status === 401) {
            // 如果未认证，清除本地存储并更新页面显示
            localStorage.removeItem('username');
            localStorage.removeItem('token');
            document.getElementById('loginRegisterLink').style.display = 'block';
            document.getElementById('userInfo').style.display = 'none';
            alert('Your session has expired. Please log in again.');
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.username) {
            document.getElementById('loginRegisterLink').style.display = 'none';
            document.getElementById('userInfo').style.display = 'block';
            document.getElementById('usernameDisplay').textContent = data.username;
        }
    })
    .catch(error => {
        console.error('Error checking login status:', error);
    });
}

function refreshToken() {
    fetch('/api/refreshToken', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(response => {
        if (response.status === 401) {
            // 如果未认证，清除本地存储并更新页面显示
            localStorage.removeItem('username');
            localStorage.removeItem('token');
            document.getElementById('loginRegisterLink').style.display = 'block';
            document.getElementById('userInfo').style.display = 'none';
            alert('Your session has expired. Please log in again.');
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.token) {
            localStorage.setItem('token', data.token); // 更新 token
        }
    })
    .catch(error => {
        console.error('Error refreshing token:', error);
    });
}