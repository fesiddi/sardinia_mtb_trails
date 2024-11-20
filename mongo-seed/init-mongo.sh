#!/bin/bash
set -e

echo "Restoring MongoDB dump..."

mongorestore --drop --dir=/mongo-seed

echo "MongoDB restore completed!"