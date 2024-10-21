const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');
const db = require('./public/database');

const app = express();
const port = 3000;
const secretKey = 'your_secret_key'; // 请使用更安全的密钥

app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
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


// 受保护的路由示例
app.get('/api/protected', authenticateToken, (req, res) => {
    res.json({ message: 'This is a protected route', user: req.user });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});