#!/bin/bash

# Social Media API Deployment Script
# Run this script on your server to deploy/update the application

echo "Starting deployment..."

# Navigate to project directory
cd /home/username/social_media_api

# Activate virtual environment
source venv/bin/activate

# Pull latest code from GitHub
echo "Pulling latest code..."
git pull origin main

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running migrations..."
python manage.py migrate

# Restart Gunicorn service
echo "Restarting Gunicorn..."
sudo systemctl restart social_media_api

# Restart Nginx (if needed)
echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "Deployment completed successfully!"
echo "Check status with: sudo systemctl status social_media_api"