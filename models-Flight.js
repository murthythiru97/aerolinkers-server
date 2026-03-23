// ============================================================================
// models/Flight.js
// ============================================================================

const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Flight = sequelize.define('Flight', {
  flight_id: {
    type: DataTypes.STRING,
    primaryKey: true,
    allowNull: false,
    unique: true
  },
  boarding_time: {
    type: DataTypes.STRING,
    allowNull: false
  },
  departure: {
    type: DataTypes.STRING,
    allowNull: true
  },
  gate: {
    type: DataTypes.STRING,
    allowNull: true
  },
  status: {
    type: DataTypes.ENUM('on-time', 'delayed', 'cancelled', 'boarding', 'departed'),
    defaultValue: 'on-time'
  },
  aircraft: {
    type: DataTypes.STRING,
    allowNull: true
  },
  origin: {
    type: DataTypes.STRING,
    allowNull: true
  },
  destination: {
    type: DataTypes.STRING,
    allowNull: true
  },
  display_time: {
    type: DataTypes.STRING,
    allowNull: true
  },
  total_passengers: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  },
  boarded_passengers: {
    type: DataTypes.INTEGER,
    defaultValue: 0
  }
}, {
  tableName: 'flights',
  timestamps: true
});

module.exports = Flight;
