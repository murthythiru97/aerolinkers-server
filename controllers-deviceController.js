// ============================================================================
// controllers/deviceController.js
// ============================================================================

const Device = require('../models/Device');
const Notification = require('../models/Notification');
const { Op } = require('sequelize');

// Register new device
exports.registerDevice = async (req, res) => {
  try {
    const { device_id, mac_address, passenger_id, flight_id, boarding_time } = req.body;

    if (!device_id || !mac_address) {
      return res.status(400).json({
        error: 'device_id and mac_address are required'
      });
    }

    const [device, created] = await Device.findOrCreate({
      where: { device_id },
      defaults: {
        device_id,
        mac_address,
        status: 'online',
        battery_level: 100,
        passenger_id,
        flight_id,
        boarding_time,
        last_seen: new Date()
      }
    });

    if (created) {
      // Create notification
      await Notification.create({
        device_id,
        passenger_id,
        flight_id,
        message: `Device ${device_id} registered successfully`,
        type: 'info'
      });
    }

    res.status(created ? 201 : 200).json({
      success: true,
      message: created ? 'Device registered' : 'Device already exists',
      device
    });

  } catch (error) {
    console.error('Register device error:', error);
    res.status(500).json({ error: error.message });
  }
};

// Send sensor data
exports.sendSensorData = async (req, res) => {
  try {
    const {
      device_id,
      passenger_id,
      flight_id,
      boarding_time,
      battery_level,
      signal_strength
    } = req.body;

    if (!device_id) {
      return res.status(400).json({ error: 'device_id is required' });
    }

    // Update device
    const device = await Device.findByPk(device_id);

    if (!device) {
      return res.status(404).json({ error: 'Device not found' });
    }

    await device.update({
      status: 'online',
      battery_level: battery_level || device.battery_level,
      signal_strength: signal_strength || device.signal_strength,
      passenger_id: passenger_id || device.passenger_id,
      flight_id: flight_id || device.flight_id,
      boarding_time: boarding_time || device.boarding_time,
      last_seen: new Date()
    });

    // Check battery warning
    if (battery_level && battery_level < 20) {
      await Notification.create({
        device_id,
        passenger_id,
        flight_id,
        message: `Low battery warning: ${battery_level}%`,
        type: 'warning',
        priority: 'high'
      });
    }

    res.status(200).json({
      success: true,
      message: 'Sensor data received',
      device
    });

  } catch (error) {
    console.error('Send sensor data error:', error);
    res.status(500).json({ error: error.message });
  }
};

// Get all devices
exports.getAllDevices = async (req, res) => {
  try {
    const devices = await Device.findAll({
      order: [['updatedAt', 'DESC']]
    });

    res.status(200).json({
      success: true,
      count: devices.length,
      devices
    });

  } catch (error) {
    console.error('Get all devices error:', error);
    res.status(500).json({ error: error.message });
  }
};

// Get specific device
exports.getDevice = async (req, res) => {
  try {
    const { device_id } = req.params;
    const device = await Device.findByPk(device_id);

    if (!device) {
      return res.status(404).json({ error: 'Device not found' });
    }

    res.status(200).json({
      success: true,
      device
    });

  } catch (error) {
    console.error('Get device error:', error);
    res.status(500).json({ error: error.message });
  }
};

// Update device
exports.updateDevice = async (req, res) => {
  try {
    const { device_id } = req.params;
    const updates = req.body;

    const device = await Device.findByPk(device_id);

    if (!device) {
      return res.status(404).json({ error: 'Device not found' });
    }

    await device.update(updates);

    res.status(200).json({
      success: true,
      message: 'Device updated',
      device
    });

  } catch (error) {
    console.error('Update device error:', error);
    res.status(500).json({ error: error.message });
  }
};

// Delete device
exports.deleteDevice = async (req, res) => {
  try {
    const { device_id } = req.params;

    const device = await Device.findByPk(device_id);

    if (!device) {
      return res.status(404).json({ error: 'Device not found' });
    }

    await device.destroy();

    res.status(200).json({
      success: true,
      message: 'Device deleted'
    });

  } catch (error) {
    console.error('Delete device error:', error);
    res.status(500).json({ error: error.message });
  }
};

// Get devices by flight
exports.getDevicesByFlight = async (req, res) => {
  try {
    const { flight_id } = req.params;

    const devices = await Device.findAll({
      where: { flight_id },
      order: [['updatedAt', 'DESC']]
    });

    res.status(200).json({
      success: true,
      count: devices.length,
      flight_id,
      devices
    });

  } catch (error) {
    console.error('Get devices by flight error:', error);
    res.status(500).json({ error: error.message });
  }
};

// Update device status
exports.updateDeviceStatus = async (req, res) => {
  try {
    const { device_id } = req.params;
    const { status } = req.body;

    if (!['online', 'offline', 'idle'].includes(status)) {
      return res.status(400).json({ error: 'Invalid status' });
    }

    const device = await Device.findByPk(device_id);

    if (!device) {
      return res.status(404).json({ error: 'Device not found' });
    }

    await device.update({ status });

    res.status(200).json({
      success: true,
      message: `Device status updated to ${status}`,
      device
    });

  } catch (error) {
    console.error('Update device status error:', error);
    res.status(500).json({ error: error.message });
  }
};
