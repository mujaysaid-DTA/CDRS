const express = require('express');
const cors = require('cors');
const incidentRoutes = require('./routes/incidentRoutes');
const resourceRoutes = require('./routes/resourceRoutes');
const authRoutes = require('./routes/authRoutes');

const app = express();

// Middleware
app.use(cors()); 
app.use(express.json());

// Routes
app.use('/api/v1/incidents', incidentRoutes);
app.use('/api/v1/resources', resourceRoutes);
app.use('/api/v1/auth', authRoutes);

// Health Check
app.get('/', (req, res) => {
  res.send('✅ Disaster Response API is active');
});

module.exports = app;
