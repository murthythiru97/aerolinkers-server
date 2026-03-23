// ============================================================================
// config/minio.js
// ============================================================================

const { Client } = require('minio');
const env = require('./environment');

const minioClient = new Client({
  endPoint: env.MINIO_ENDPOINT,
  port: env.MINIO_PORT,
  useSSL: false,
  accessKey: env.MINIO_ACCESS_KEY,
  secretKey: env.MINIO_SECRET_KEY
});

// Ensure bucket exists
minioClient.bucketExists(env.MINIO_BUCKET, (err, exists) => {
  if (err) {
    console.error('✗ MinIO error:', err);
    return;
  }
  
  if (!exists) {
    minioClient.makeBucket(env.MINIO_BUCKET, 'us-east-1', (err) => {
      if (err) {
        console.error('✗ Failed to create MinIO bucket:', err);
      } else {
        console.log('✓ MinIO bucket created:', env.MINIO_BUCKET);
      }
    });
  } else {
    console.log('✓ MinIO bucket exists:', env.MINIO_BUCKET);
  }
});

module.exports = minioClient;
