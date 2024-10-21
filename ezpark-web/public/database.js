const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// 数据库文件路径
const dbPath = path.resolve(__dirname, 'data', 'database.db');

// 连接到 SQLite 数据库
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Could not connect to database', err);
    } else {
        console.log('Connected to database');
    }
});

db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        isAdmin BOOLEAN DEFAULT 0,
        favoriteParkingLots TEXT,
        contributionPoints INTEGER DEFAULT 0
    )`);
});

module.exports = db;