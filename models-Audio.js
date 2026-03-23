// ============================================================================
// models/Audio.js
// ============================================================================

const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Audio = sequelize.define('Audio', {
  audio_id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  device_id: {
    type: DataTypes.STRING,
    allowNull: false
  },
  passenger_id: {
    type: DataTypes.STRING,
    allowNull: true
  },
  file_name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  file_path: {
    type: DataTypes.STRING,
    allowNull: false
  },
  file_size: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  mime_type: {
    type: DataTypes.STRING,
    allowNull: false
  },
  duration: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  audio_type: {
    type: DataTypes.ENUM('voice-profile', 'notification', 'alert', 'announcement'),
    defaultValue: 'voice-profile'
  },
  uploaded_at: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  },
  processed: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  }
}, {
  tableName: 'audio_files',
  timestamps: true
});

module.exports = Audio;
