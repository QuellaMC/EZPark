const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(cors()); // Allow requests from the iOS app

// Mock database
let crowdAvailability = Math.floor(Math.random() * 100); // Random availability for testing
const feedbacks = []; // Store feedback from users

// Routes
app.get('/', (req, res) => {
    res.send('EZPark Backend is Running');
});
