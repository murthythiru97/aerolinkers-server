// ============================================================================
// models/Passenger.js
// ============================================================================

const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Passenger = sequelize.define('Passenger', {
  passenger_id: {
    type: DataTypes.STRING,
    primaryKey: true,
    allowNull: false,
    unique: true
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  ticket_number: {
    type: DataTypes.STRING,
    allowNull: true
  },
  flight_id: {
    type: DataTypes.STRING,
    allowNull: true
  },
  boarding_status: {
    type: DataTypes.ENUM('waiting', 'boarding', 'boarded'),
    defaultValue: 'waiting'
  },
  seat_number: {
    type: DataTypes.STRING,
    allowNull: true
  },
  device_id: {
    type: DataTypes.STRING,
    allowNull: true
  },
  check_in_time: {
    type: DataTypes.DATE,
    allowNull: true
  },
  boarding_gate: {
    type: DataTypes.STRING,
    allowNull: true
  }
}, {
  tableName: 'passengers',
  timestamps: true
});

module.exports = Passenger;
