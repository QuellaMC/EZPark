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