// ============================================================================
// server.js - Server Entry Point
// ============================================================================

const app = require('./app');
const sequelize = require('./config/database');
const env = require('./config/environment');

// Import models for syncing
const Device = require('./models/Device');
const Passenger = require('./models/Passenger');
const Flight = require('./models/Flight');
const Notification = require('./models/Notification');
const Audio = require('./models/Audio');

// Sync database and start server
const startServer = async () => {
  try {
    // Sync all models with database
    await sequelize.sync({ alter: env.NODE_ENV === 'development' });
    console.log('✓ Database synchronized successfully');

    // Start Express server
    app.listen(env.PORT, () => {
      console.log('\n' + '='.repeat(60));
      console.log('🚀 Airport Smart Band (ATAB) Server Started');
      console.log('='.repeat(60));
      console.log(`\nEnvironment: ${env.NODE_ENV}`);
      console.log(`Server: http://localhost:${env.PORT}`);
      console.log(`Database: ${env.DB_NAME} @ ${env.DB_HOST}:${env.DB_PORT}`);
      console.log(`MinIO: ${env.MINIO_ENDPOINT}:${env.MINIO_PORT}`);
      console.log('\nAPI Endpoints:');
      console.log(`  • POST   /api/devices/register`);
      console.log(`  • POST   /api/devices/data`);
      console.log(`  • GET    /api/devices`);
      console.log(`  • GET    /api/devices/:device_id`);
      console.log(`  • PUT    /api/devices/:device_id`);
      console.log(`  • DELETE /api/devices/:device_id`);
      console.log(`\n  • GET    /api/passengers`);
      console.log(`  • GET    /api/flights`);
      console.log(`  • GET    /api/notifications`);
      console.log(`  • POST   /api/audio/upload`);
      console.log('\nHealth Check: GET /health');
      console.log('='.repeat(60) + '\n');
    });

  } catch (error) {
    console.error('✗ Failed to start server:', error);
    process.exit(1);
  }
};

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n\nShutting down server...');
  await sequelize.close();
  process.exit(0);
});

startServer();
