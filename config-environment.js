// ============================================================================
// config/environment.js
// ============================================================================

require('dotenv').config();

module.exports = {
  // Server
  PORT: process.env.PORT || 7000,
  NODE_ENV: process.env.NODE_ENV || 'development',

  // Database
  DB_HOST: process.env.DB_HOST || 'localhost',
  DB_PORT: process.env.DB_PORT || 5432,
  DB_NAME: process.env.DB_NAME || 'atab_db',
  DB_USER: process.env.DB_USER || 'atab_user',
  DB_PASSWORD: process.env.DB_PASSWORD || 'password',

  // MinIO
  MINIO_ENDPOINT: process.env.MINIO_ENDPOINT || 'localhost',
  MINIO_PORT: process.env.MINIO_PORT || 9000,
  MINIO_ACCESS_KEY: process.env.MINIO_ACCESS_KEY || 'minioadmin',
  MINIO_SECRET_KEY: process.env.MINIO_SECRET_KEY || 'minioadmin',
  MINIO_BUCKET: process.env.MINIO_BUCKET || 'atab-audio'
};
