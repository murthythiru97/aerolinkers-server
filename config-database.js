// ============================================================================
// config/database.js
// ============================================================================

const { Sequelize } = require('sequelize');
const env = require('./environment');

const sequelize = new Sequelize(
  env.DB_NAME,
  env.DB_USER,
  env.DB_PASSWORD,
  {
    host: env.DB_HOST,
    port: env.DB_PORT,
    dialect: 'postgres',
    logging: false,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
);

// Test connection
sequelize.authenticate()
  .then(() => {
    console.log('✓ PostgreSQL connection established successfully');
  })
  .catch(err => {
    console.error('✗ Unable to connect to PostgreSQL:', err);
  });

module.exports = sequelize;
