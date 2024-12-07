// Get crowd-level data
app.get('/api/crowd-level', (req, res) => {
    res.json({ availability: crowdAvailability });
});

// Simulate crowd updates every 10 seconds
setInterval(() => {
    crowdAvailability = Math.floor(Math.random() * 100); // Randomly change availability
    console.log(`Updated crowd availability: ${crowdAvailability}`);
}, 10000); // Every 10 seconds
