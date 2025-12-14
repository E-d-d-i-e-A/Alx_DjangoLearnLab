Social Media API - Production Deployment Guide
Table of Contents
Pre-Deployment Checklist
Option A: Heroku Deployment
Option B: VPS Deployment (DigitalOcean, AWS EC2, etc.)
Post-Deployment Configuration
Monitoring and Maintenance
Troubleshooting
Pre-Deployment Checklist
1. Update Settings for Production
[x] Set DEBUG = False
[x] Configure ALLOWED_HOSTS
[x] Set up secure SECRET_KEY from environment variable
[x] Configure database for PostgreSQL
[x] Enable security settings (SSL, HSTS, etc.)
[x] Set up static files with WhiteNoise
[x] Configure logging
2. Required Files
[x] requirements.txt - Python dependencies
[x] Procfile - Heroku configuration
[x] runtime.txt - Python version
[x] .env.example - Environment variables template
[x] .gitignore - Files to exclude from Git
[x] gunicorn_config.py - Gunicorn configuration
3. Security Checklist
[x] Generate new SECRET_KEY for production
[x] Use environment variables for sensitive data
[x] Enable HTTPS/SSL
[x] Set secure cookie flags
[x] Configure CORS properly
[x] Set up proper database credentials
Option A: Heroku Deployment
Step 1: Install Heroku CLI
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download installer from https://devcenter.heroku.com/articles/heroku-cli
Step 2: Login to Heroku
heroku login
Step 3: Create Heroku App
heroku create your-app-name
Step 4: Add PostgreSQL Database
heroku addons:create heroku-postgresql:mini
Step 5: Set Environment Variables
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set DJANGO_SECRET_KEY='your-generated-secret-key'
heroku config:set DJANGO_DEBUG=False
heroku config:set ALLOWED_HOST='your-app-name.herokuapp.com'
Step 6: Create Files for Heroku
Create Procfile in project root:
web: gunicorn social_media_api.wsgi --log-file -
release: python manage.py migrate
Create runtime.txt in project root:
python-3.11.6
Step 7: Update settings.py for Heroku
Add this at the bottom of your settings.py:
import dj_database_url

# Use Heroku's DATABASE_URL if available
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
Step 8: Deploy to Heroku
# Initialize git if not already done
git init
git add .
git commit -m "Prepare for Heroku deployment"

# Add Heroku remote
heroku git:remote -a your-app-name

# Push to Heroku
git push heroku main

# Or if using master branch
git push heroku master
Step 9: Run Migrations and Create Superuser
# Migrations run automatically via Procfile, but you can also run manually:
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Collect static files (if needed)
heroku run python manage.py collectstatic --noinput
Step 10: Open Your App
heroku open
Your API will be available at: https://your-app-name.herokuapp.com/
Option B: VPS Deployment (DigitalOcean, AWS EC2, Linode)
Step 1: Set Up Server
1. Create a VPS instance
Choose Ubuntu 22.04 LTS
At least 1GB RAM recommended
Enable SSH access
2. Connect to your server
ssh root@your-server-ip
3. Update system
sudo apt update && sudo apt upgrade -y
4. Create a new user
adduser username
usermod -aG sudo username
su - username
Step 2: Install Dependencies
# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y

# Install other tools
sudo apt install git curl -y
Step 3: Set Up PostgreSQL Database
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell, run:
CREATE DATABASE social_media_db;
CREATE USER dbuser WITH PASSWORD 'your-strong-password';
ALTER ROLE dbuser SET client_encoding TO 'utf8';
ALTER ROLE dbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO dbuser;
\q
Step 4: Clone Your Project
cd /home/username
git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
Step 5: Set Up Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Step 6: Configure Environment Variables
# Create .env file
nano .env

# Add these variables:
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
ALLOWED_HOST=your-domain.com
DB_NAME=social_media_db
DB_USER=dbuser
DB_PASSWORD=your-strong-password
DB_HOST=localhost
DB_PORT=5432
Step 7: Prepare Django Application
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Create logs directory
mkdir logs
Step 8: Configure Gunicorn
Test Gunicorn:
gunicorn --bind 0.0.0.0:8000 social_media_api.wsgi:application
If it works, press Ctrl+C to stop.
Create systemd service file:
sudo nano /etc/systemd/system/social_media_api.service
Copy the content from social_media_api.service artifact and modify paths.
Start and enable the service:
sudo systemctl start social_media_api
sudo systemctl enable social_media_api
sudo systemctl status social_media_api
Step 9: Configure Nginx
# Remove default config
sudo rm /etc/nginx/sites-enabled/default

# Create new config
sudo nano /etc/nginx/sites-available/social_media_api
Copy the content from nginx.conf artifact and modify domain.
Enable the site:
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
Step 10: Set Up SSL with Let's Encrypt
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
# Test renewal:
sudo certbot renew --dry-run
Step 11: Configure Firewall
# Allow SSH, HTTP, and HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
Post-Deployment Configuration
1. Verify Deployment
Test API endpoints:
curl https://yourdomain.com/api/accounts/login/
Check service status:
sudo systemctl status social_media_api
sudo systemctl status nginx
2. Set Up Domain DNS
Point your domain to your server:
A Record: @ → your-server-ip
A Record: www → your-server-ip
Wait for DNS propagation (can take up to 24 hours).
3. Create Admin User
# Heroku
heroku run python manage.py createsuperuser

# VPS
cd /home/username/social_media_api
source venv/bin/activate
python manage.py createsuperuser
4. Test Admin Panel
Visit: https://yourdomain.com/admin/
Monitoring and Maintenance
1. Set Up Logging
View logs on Heroku:
heroku logs --tail
View logs on VPS:
# Gunicorn logs
sudo journalctl -u social_media_api -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Django logs
tail -f /home/username/social_media_api/logs/django.log
2. Database Backups
Heroku (automatic backups):
# Capture manual backup
heroku pg:backups:capture

# Download backup
heroku pg:backups:download
VPS (PostgreSQL):
# Create backup script
nano /home/username/backup.sh

#!/bin/bash
BACKUP_DIR="/home/username/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U dbuser social_media_db > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

# Make executable
chmod +x /home/username/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /home/username/backup.sh
3. Update Application
Heroku:
git add .
git commit -m "Update message"
git push heroku main
VPS:
# Use the deploy.sh script
chmod +x deploy.sh
./deploy.sh
4. Monitor Performance
Set up monitoring tools:
New Relic
Datadog
Sentry (for error tracking)
UptimeRobot (for uptime monitoring)
Troubleshooting
Common Issues
1. 500 Internal Server Error
# Check logs
heroku logs --tail  # Heroku
sudo journalctl -u social_media_api -f  # VPS

# Common causes:
# - DEBUG=False but ALLOWED_HOSTS not set
# - Database connection issues
# - Missing environment variables
2. Static Files Not Loading
# Run collectstatic
python manage.py collectstatic --noinput

# Check STATIC_ROOT and STATIC_URL settings
# Verify WhiteNoise is in MIDDLEWARE
3. Database Connection Error
# Verify database credentials in .env
# Check PostgreSQL is running:
sudo systemctl status postgresql

# Test connection:
psql -U dbuser -d social_media_db -h localhost
4. Gunicorn Not Starting
# Check service status
sudo systemctl status social_media_api

# View detailed logs
sudo journalctl -u social_media_api -n 50

# Test manually
cd /home/username/social_media_api
source venv/bin/activate
gunicorn social_media_api.wsgi:application
5. Nginx 502 Bad Gateway
# Check if Gunicorn is running
sudo systemctl status social_media_api

# Check Nginx configuration
sudo nginx -t

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
Security Best Practices
Keep dependencies updated:
pip list --outdated
pip install -U package-name
Regular security audits:
pip install safety
safety check
Monitor logs regularly
Set up automated backups
Use strong passwords for database
Keep SSH keys secure
Enable 2FA on hosting accounts
Regular server updates:
sudo apt update && sudo apt upgrade -y
Maintenance Checklist
Daily
[ ] Check error logs
[ ] Monitor uptime
[ ] Check API response times
Weekly
[ ] Review access logs
[ ] Check disk space
[ ] Verify backups
Monthly
[ ] Update dependencies
[ ] Security audit
[ ] Performance optimization
[ ] Database cleanup
Live URL Template
After deployment, your API will be available at:
Heroku: https://your-app-name.herokuapp.com/api/
VPS: https://yourdomain.com/api/
API Endpoints:
User Registration: POST /api/accounts/register/
User Login: POST /api/accounts/login/
Posts: GET/POST /api/posts/
Feed: GET /api/feed/
Notifications: GET /api/notifications/
Additional Resources
Django Deployment Checklist
Heroku Django Documentation
DigitalOcean Django Tutorials
Gunicorn Documentation
Nginx Documentation
Support
For issues or questions:
Check the troubleshooting section above
Review server logs
Consult Django and hosting provider documentation
Create an issue on GitHub repository