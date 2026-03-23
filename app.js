// ============================================================================
// app.js - Express Application Setup
// ============================================================================

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const env = require('./config/environment');

// Import routes
const deviceRoutes = require('./routes/device.routes');
const passengerRoutes = require('./routes/passenger.routes');
const flightRoutes = require('./routes/flight.routes');
const notificationRoutes = require('./routes/notification.routes');
const audioRoutes = require('./routes/audio.routes');

const app = express();

// ============================================================================
// MIDDLEWARE
// ============================================================================

// Security
app.use(helmet());

// CORS
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Body Parser
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Request Logging
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});

// ============================================================================
// ROUTES
// ============================================================================

// API Routes
app.use('/api/devices', deviceRoutes);
app.use('/api/passengers', passengerRoutes);
app.use('/api/flights', flightRoutes);
app.use('/api/notifications', notificationRoutes);
app.use('/api/audio', audioRoutes);

// Health Check
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    environment: env.NODE_ENV
  });
});

// Root Route
app.get('/', (req, res) => {
  res.status(200).json({
    message: 'Airport Smart Band (ATAB) Server',
    version: '1.0.0',
    api_endpoints: {
      devices: '/api/devices',
      passengers: '/api/passengers',
      flights: '/api/flights',
      notifications: '/api/notifications',
      audio: '/api/audio'
    }
  });
});

// 404 Handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.method} ${req.path} does not exist`
  });
});

// Error Handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error',
    status: err.status || 500
  });
});

module.exports = app;
