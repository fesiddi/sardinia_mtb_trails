#!/bin/bash
set -e

# Start MongoDB server in the background
mongod --bind_ip_all &

# Wait for MongoDB to start
until mongosh --eval "print(\"MongoDB is up\")"; do
  echo "Waiting for MongoDB to start..."
  sleep 2
done

# Run the initialization script
/mongo-seed/init-mongo.sh

# Keep the container running
wait