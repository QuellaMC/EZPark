
// 停车场信息对象
const parkingInfoData = {
    'North Parking Lot': 'North Parking Lot, \n\'N\' Permit Needed',
    'Davison Parking Lot': 'Davison Parking Lot, \n\'RH\' Permit Needed',
    'College Avenue Parking Garage': 'College Avenue Parking Garage, \n\'Garage\' Permit Needed',
    'Commons East Lot': 'Commons East Lot, \n\'RH\' Permit Needed',
    'Commons West Lot': 'Commons West Lot, \n\'G\' Permit Needed',
};

let currentZoom = {
    x: 0,
    y: 0,
    scale: 1,
    infoKey: ''
};

/**
 * 缩放到指定的坐标和缩放级别，并显示停车场信息
 * @param {number} x - 地点的X坐标（地图的原始分辨率下的坐标）
 * @param {number} y - 地点的Y坐标（地图的原始分辨率下的坐标）
 * @param {number} scale - 缩放比例（1表示原始大小，2表示放大2倍）
 * @param {string} infoKey - 停车场信息的键
 */
function zoomToLocation(location) {
    const { x, y, scale, infoKey, url } = location;
    currentZoom = { x, y, scale, infoKey};

    applyZoom();
    const parkingInfo = document.getElementById('parking-info');
    if (infoKey) {
        parkingInfo.innerText = parkingInfoData[infoKey];
        parkingInfo.style.display = 'block';
        document.getElementById('parkingButtons').style.display = 'flex'; // 显示停车按钮
        currentLocationUrl = url; // 设置当前地点的 URL
    } else {
        parkingInfo.style.display = 'none';
        document.getElementById('parkingButtons').style.display = 'none'; // 隐藏停车按钮
        currentLocationUrl = ''; // 清空当前地点的 URL
    }
}

let currentLocationUrl = '';

function applyZoom() {
    const { x, y, scale, infoKey } = currentZoom;
    const map = document.getElementById('map');
    const container = map.parentElement;

    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    // 原始地图尺寸
    const originalWidth = map.naturalWidth;
    const originalHeight = map.naturalHeight;

    // 计算容器和地图的宽高比
    const containerAspectRatio = containerWidth / containerHeight;
    const imageAspectRatio = originalWidth / originalHeight;

    // 计算图片的缩放因子（因 object-fit: cover）
    const scaleFactor = Math.max(
        containerWidth / originalWidth,
        containerHeight / originalHeight
    );

    // 计算显示的图像尺寸
    const displayedImageWidth = originalWidth * scaleFactor;
    const displayedImageHeight = originalHeight * scaleFactor;

    // 计算图像被裁剪的偏移量
    const cropX = (displayedImageWidth - containerWidth) / 2;
    const cropY = (displayedImageHeight - containerHeight) / 2;

    // 根据比例调整目标位置，考虑被裁剪的部分
    const adjustedX = x * scaleFactor - cropX;
    const adjustedY = y * scaleFactor - cropY;

    // 计算容器的中心点
    const containerCenterX = containerWidth / 2;
    const containerCenterY = containerHeight / 2;

    // 计算缩放后的地图上，指定点应位于容器中心的偏移量
    const offsetX = adjustedX * scale - containerCenterX;
    const offsetY = adjustedY * scale - containerCenterY;

    // 设置 transform 属性，实现地图的平移和缩放
    map.style.transform = `translate(${-offsetX}px, ${-offsetY}px) scale(${scale})`;
    // 显示停车场信息

}

function resetZoom() {
    map.style.transform = 'translate(0, 0) scale(1)';
    document.getElementById('parking-info').style.display = 'none';
    document.getElementById('parkingButtons').style.display = 'none'; // 隐藏停车按钮
}

document.addEventListener('DOMContentLoaded', function() {
    const buttonTexts = {
        btn1: { original: "Navigate", hover: "res/map/icon/NAV.png" },
        btn2: { original: "Add to Common", hover: "res/map/icon/FAV.png" },
        btn3: { original: "Update Status", hover: "res/map/icon/STA.png" },
        btn4: { original: "Share", hover: "res/map/icon/SHR.png" }
    };

    const parkingButtons = document.getElementById('parkingButtons');
    parkingButtons.style.display = 'none'; // 初始隐藏停车按钮

    document.querySelectorAll('.square-button').forEach(button => {
        const btnId = button.id;
        let hoverTimeout;

        // 鼠标移入事件：修改按钮内容为文字
        button.addEventListener('mouseover', () => {
            hoverTimeout = setTimeout(() => {
                button.textContent = buttonTexts[btnId].original;
            }, 100); // 0.1秒延时
        });

        // 鼠标移出事件：恢复按钮内容为图标
        button.addEventListener('mouseout', () => {
            clearTimeout(hoverTimeout);
            setTimeout(() => {
                button.innerHTML = `<img src="${buttonTexts[btnId].hover}" class="icon" alt="${buttonTexts[btnId].original}">`;
            }, 100); // 0.1秒延时
        });

        // 点击事件：处理导航按钮的特殊情况
        button.addEventListener('click', () => {
            if (btnId === 'btn1') {
                // 显示模态对话框
                document.getElementById('mapModal').style.display = 'block';
            } else {
                window.open(buttonTexts[btnId].url, '_blank');
            }
        });
    });

    // 处理模态对话框的关闭按钮
    document.querySelector('.close').addEventListener('click', () => {
        document.getElementById('mapModal').style.display = 'none';
    });

    // 处理模态对话框的 Apple Maps 按钮
    document.getElementById('appleMaps').addEventListener('click', () => {
        window.open('http://maps.apple.com/?q=location', '_blank');
        document.getElementById('mapModal').style.display = 'none';
    });

    // 处理模态对话框的 Google Maps 按钮
    document.getElementById('googleMaps').addEventListener('click', () => {
        window.open(currentLocationUrl, '_blank');
        document.getElementById('mapModal').style.display = 'none';
    });
});


// 监听窗口大小变化事件
window.addEventListener('resize', applyZoom);
window.addEventListener('load', resetZoom);

class Url {
    constructor(url_g, url_a) {
        this.url_g = url_g;
        this.url_a = url_a;
    }
}

class Location {
    constructor(x, y, scale, infoKey, Url) {
        this.x = x;
        this.y = y;
        this.scale = scale;
        this.infoKey = infoKey;
        this.url = Url;
    }
}

const locations = new Map([
    ['North Parking Lot', new Location(1089, 249, 4, 'North Parking Lot', 'https://www.google.com/maps?q=North+Parking+Lot')],
    ['Davison Parking Lot', new Location(2220, 1530, 5, 'Davison Parking Lot', 'https://www.google.com/maps?q=Davison+Parking+Lot')],
    ['College Avenue Parking Garage', new Location(768, 1311, 5, 'College Avenue Parking Garage', 'https://www.google.com/maps?q=College+Avenue+Parking+Garage')],
    ['Commons East Lot', new Location(2229, 1257, 5, 'Commons East Lot', 'https://www.google.com/maps?q=Commons+East+Lot')],
    ['Commons West Lot', new Location(1923, 1215, 5, 'Commons West Lot', 'https://www.google.com/maps?q=Commons+West+Lot')]
]);
