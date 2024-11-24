const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const db = require('./public/database');
const fs = require('fs');

const app = express();
const port = 3000;
const secretKey = 'your_secret_key';

app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 验证 JWT 令牌中间件
const authenticateToken = (req, res, next) => {
    const token = req.cookies.token;
    if (!token) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    jwt.verify(token, secretKey, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Token expired or invalid' });
        }
        req.user = user;
        next();
    });
};

// 刷新 JWT 令牌
app.post('/api/refreshToken', authenticateToken, (req, res) => {
    const user = req.user;
    const token = jwt.sign({ username: user.username, isAdmin: user.isAdmin }, secretKey, { expiresIn: '30m' });
    res.json({ token });
});

// 存储用户名
app.post('/api/users', (req, res) => {
    const { username } = req.body;
    db.run("INSERT INTO users (username) VALUES (?)", [username], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ id: this.lastID });
    });
});

// 检索用户名
app.get('/api/users', (req, res) => {
    db.all("SELECT * FROM users", [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ users: rows });
    });
});

// 注册用户
app.post('/api/register', (req, res) => {
    const { username, password } = req.body;

    // 验证密码长度
    if (password.length < 6) {
        return res.status(400).json({ error: 'Password must be at least 6 characters long' });
    }

    db.get("SELECT * FROM users WHERE username = ?", [username], (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (row) {
            return res.status(400).json({ error: 'Username already exists' });
        } else {
            db.run("INSERT INTO users (username, password) VALUES (?, ?)", [username, password], function(err) {
                if (err) {
                    return res.status(500).json({ error: err.message });
                }
                res.json({ id: this.lastID });
            });
        }
    });
});

// 用户登录
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    db.get("SELECT * FROM users WHERE username = ? AND password = ?", [username, password], (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (row) {
            // 生成 JWT 令牌，设置过期时间为30分钟
            const token = jwt.sign({ username: row.username, isAdmin: row.isAdmin }, secretKey, { expiresIn: '30m' });
            res.cookie('token', token, { httpOnly: true });
            res.json({ message: 'Login successful', user: row });
        } else {
            res.status(401).json({ error: 'Invalid username or password' });
        }
    });
});

// 用户登出
app.post('/api/logout', (req, res) => {
    res.clearCookie('token');
    res.json({ message: 'Logout successful' });
});

// 获取收藏的停车场
app.get('/api/getFavorites', authenticateToken, (req, res) => {
    db.get("SELECT favoriteParkingLots FROM users WHERE username = ?", [req.user.username], (err, row) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        const favoriteParkingLots = JSON.parse(row.favoriteParkingLots || '[]');
        res.json({ favoriteParkingLots });
    });
});

// 添加用户收藏的停车场
app.post('/api/addFavorite', authenticateToken, (req, res) => {
    const { favoriteParkingLots } = req.body;

    console.log('Received request to add favorite');
    console.log('favoriteParkingLots:', favoriteParkingLots);

    // 确保 favoriteParkingLots 是一个数组
    if (!Array.isArray(favoriteParkingLots)) {
        console.error('favoriteParkingLots is not an array');
        return res.status(400).json({ error: 'favoriteParkingLots must be an array' });
    }

    const favoriteParkingLotsStr = JSON.stringify(favoriteParkingLots);
    db.run("UPDATE users SET favoriteParkingLots = ? WHERE username = ?", [favoriteParkingLotsStr, req.user.username], function(err) {
        if (err) {
            console.error('Error updating favorite parking lots:', err.message);
            return res.status(500).json({ error: err.message });
        }
        console.log('Successfully updated favorite parking lots in database');
        res.json({ message: 'Favorites updated successfully', favoriteParkingLots });
    });
});

// 删除用户收藏的停车场
app.post('/api/removeFavorite', authenticateToken, (req, res) => {
    const { removeUid } = req.body;

    console.log('Received request to remove favorite');
    console.log('removeUid:', removeUid);

    // 从数据库中获取最新的收藏列表
    db.get("SELECT favoriteParkingLots FROM users WHERE username = ?", [req.user.username], (err, row) => {
        if (err) {
            console.error('Error fetching favorite parking lots:', err.message);
            return res.status(500).json({ error: err.message });
        }

        if (!row) {
            console.error('No user found with the given username');
            return res.status(404).json({ error: 'User not found' });
        }

        console.log('Fetched favorite parking lots from database:', row.favoriteParkingLots);

        // 获取用户的收藏停车场列表
        let favoriteParkingLots;
        try {
            favoriteParkingLots = JSON.parse(row.favoriteParkingLots || '[]');
        } catch (parseErr) {
            console.error('Error parsing favorite parking lots:', parseErr.message);
            return res.status(500).json({ error: 'Failed to parse favorite parking lots' });
        }

        console.log('Parsed favorite parking lots:', favoriteParkingLots);

        // 确保 removeUid 和收藏列表的类型匹配
        const removeUidStr = String(removeUid);
        favoriteParkingLots = favoriteParkingLots.filter(uid => String(uid) !== removeUidStr);

        console.log('Updated favorites after removal:', favoriteParkingLots);

        // 更新数据库中的收藏列表
        const favoriteParkingLotsStr = JSON.stringify(favoriteParkingLots);
        db.run("UPDATE users SET favoriteParkingLots = ? WHERE username = ?", [favoriteParkingLotsStr, req.user.username], function(err) {
            if (err) {
                console.error('Error updating favorite parking lots:', err.message);
                return res.status(500).json({ error: err.message });
            }
            console.log('Successfully updated favorite parking lots in database');
            res.json({ message: 'Favorites updated successfully', favoriteParkingLots: favoriteParkingLots });
        });
    });
});

app.get('/api/protected', authenticateToken, (req, res) => {
    res.json({ message: 'This is a protected route', user: req.user });
});

app.get('/api/status', (req, res) => {
    fs.readFile(path.join(__dirname, 'public/statusPage/status.json'), 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Error reading status.json');
        }
        res.send(JSON.parse(data));
    });
});

app.post('/api/status', (req, res) => {
    const newStatus = req.body;
    fs.readFile(path.join(__dirname, 'public/statusPage/status.json'), 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Error reading status.json');
        }
        const statusData = JSON.parse(data);
        if (!statusData[newStatus.location]) {
            statusData[newStatus.location] = [];
        }
        statusData[newStatus.location].push(newStatus);
        fs.writeFile(path.join(__dirname, 'public/statusPage/status.json'), JSON.stringify(statusData, null, 2), 'utf8', (err) => {
            if (err) {
                return res.status(500).send('Error writing to status.json');
            }
            res.send('Status reported successfully');
        });
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});