#!/bin/bash

# Script to prepare minimal deployment package

set -e

SERVER_USER=$1
SERVER_HOST=$2
SERVER_PATH=$3
SERVER_PORT=${4:-22}  # Default to 22 if not specified

if [ -z "$SERVER_USER" ] || [ -z "$SERVER_HOST" ] || [ -z "$SERVER_PATH" ]; then
    echo "Usage: ./prepare-deployment.sh <user> <host> <path> [port]"
    echo "Example: ./prepare-deployment.sh user 192.168.1.100 /home/user/bog-na-svyazi"
    echo "Example with port: ./prepare-deployment.sh user 192.168.1.100 /home/user/bog-na-svyazi 2222"
    exit 1
fi

echo "📦 Preparing deployment package..."

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "Using temp directory: $TEMP_DIR"

# Copy essential files
echo "Copying essential files..."
cp -r app.py config.py process_query.py requirements.txt Dockerfile docker-compose.yml deploy.sh $TEMP_DIR/
cp -r static templates preprocessing $TEMP_DIR/

# Copy data directory (without large JSON files if they exist)
mkdir -p $TEMP_DIR/data
cp data/*.json $TEMP_DIR/data/ 2>/dev/null || echo "No JSON files in data/"

# Copy only the latest finetuning model
echo "Copying finetuned model..."
mkdir -p $TEMP_DIR/finetuning/models
cp -r finetuning/models/rbt2-31072025_220714 $TEMP_DIR/finetuning/models/

# Create feedback directory
mkdir -p $TEMP_DIR/feedback

# Show package size
echo "Package size:"
du -sh $TEMP_DIR

# Transfer to server
echo "🚀 Transferring to $SERVER_USER@$SERVER_HOST:$SERVER_PATH (port $SERVER_PORT)"
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "mkdir -p $SERVER_PATH"
rsync -avz --progress -e "ssh -p $SERVER_PORT" $TEMP_DIR/ $SERVER_USER@$SERVER_HOST:$SERVER_PATH/

# Cleanup
rm -rf $TEMP_DIR

echo "✅ Deployment package transferred!"
echo ""
echo "Next steps:"
echo "1. SSH into your server: ssh $SERVER_USER@$SERVER_HOST"
echo "2. Navigate to: cd $SERVER_PATH"
echo "3. Run: ./deploy.sh"