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
                // 清除 localStorage 中的用户名
                localStorage.removeItem('username');
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });



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