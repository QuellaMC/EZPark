// Submit feedback
app.post('/api/feedback', (req, res) => {
    const { feedback } = req.body;

    if (!feedback) {
        return res.status(400).json({ message: 'Feedback is required' });
    }

    // Store the feedback (in memory for now)
    feedbacks.push({ feedback, timestamp: new Date() });
    console.log('Received feedback:', feedback);

    res.json({ message: 'Feedback submitted successfully!' });
});

// View all feedback (for debugging or admin)
app.get('/api/feedback', (req, res) => {
    res.json(feedbacks);
});
