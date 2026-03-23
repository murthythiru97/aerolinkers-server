// ============================================================================
// routes/device.routes.js
// ============================================================================

const express = require('express');
const router = express.Router();
const deviceController = require('../controllers/deviceController');

// POST /api/devices/register - Register new device
router.post('/register', deviceController.registerDevice);

// POST /api/devices/data - Send sensor data
router.post('/data', deviceController.sendSensorData);

// GET /api/devices - Get all devices
router.get('/', deviceController.getAllDevices);

// GET /api/devices/:device_id - Get specific device
router.get('/:device_id', deviceController.getDevice);

// PUT /api/devices/:device_id - Update device
router.put('/:device_id', deviceController.updateDevice);

// DELETE /api/devices/:device_id - Delete device
router.delete('/:device_id', deviceController.deleteDevice);

// GET /api/devices/flight/:flight_id - Get devices for flight
router.get('/flight/:flight_id', deviceController.getDevicesByFlight);

// PATCH /api/devices/:device_id/status - Update device status
router.patch('/:device_id/status', deviceController.updateDeviceStatus);

module.exports = router;
