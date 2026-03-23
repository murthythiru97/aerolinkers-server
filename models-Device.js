// ============================================================================
// models/Device.js
// ============================================================================

const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Device = sequelize.define('Device', {
  device_id: {
    type: DataTypes.STRING,
    primaryKey: true,
    allowNull: false,
    unique: true
  },
  mac_address: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  status: {
    type: DataTypes.ENUM('online', 'offline', 'idle'),
    defaultValue: 'offline'
  },
  battery_level: {
    type: DataTypes.INTEGER,
    defaultValue: 100
  },
  signal_strength: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  },
  last_seen: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  },
  passenger_id: {
    type: DataTypes.STRING,
    allowNull: true
  },
  flight_id: {
    type: DataTypes.STRING,
    allowNull: true
  },
  boarding_time: {
    type: DataTypes.STRING,
    allowNull: true
  }
}, {
  tableName: 'devices',
  timestamps: true
});

module.exports = Device;
