// 获取所有菜单链接和页面部分
const links = document.querySelectorAll('.sidebar a');
const pages = document.querySelectorAll('.page');

// 为每个菜单项添加点击事件监听器
links.forEach(link => {
    link.addEventListener('click', function(event) {
        // 阻止默认链接行为
        event.preventDefault();

        // 获取目标页面的 ID
        const targetId = this.getAttribute('data-target');
        console.log(`Target ID: ${targetId}`);

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
    });
});

links.forEach(link => {
    link.addEventListener('click', function(event) {
        // 阻止默认链接行为
        event.preventDefault();

        // 获取目标页面的 ID
        const targetId = this.getAttribute('data-target');
        console.log(`Target ID: ${targetId}`);

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
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const parkingLotMapLink = document.getElementById('parkingLotMapLink');

    parkingLotMapLink.addEventListener('click', function() {
        document.title = 'Parking Lot Map - EZPark';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const loginModal = document.getElementById('loginModal');
    const userOptionsLink = document.getElementById('userOptionsLink');
    const closeModal = document.querySelector('.close');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // 简单的用户名和密码验证
            if (username === 'admin' && password === 'password') {
                localStorage.setItem('loggedIn', 'true');
                localStorage.setItem('username', username);
                loginModal.style.display = 'none';
                updateSidebar();
            } else {
                loginError.textContent = 'Invalid username or password';
            }
        });
    }

    if (userOptionsLink) {
        userOptionsLink.addEventListener('click', function(event) {
            event.preventDefault();
            loginModal.style.display = 'block';
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', function() {
            loginModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === loginModal) {
            loginModal.style.display = 'none';
        }
    });

    function updateSidebar() {
        const username = localStorage.getItem('username');
        if (username) {
            userOptionsLink.textContent = `Welcome, ${username}`;
        }
    }

    updateSidebar();
});
