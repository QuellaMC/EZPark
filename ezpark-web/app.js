const express = require('express');
const path = require('path');
const app = express();

// 提供静态文件服务
app.use(express.static(path.join(__dirname, 'public')));

const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
