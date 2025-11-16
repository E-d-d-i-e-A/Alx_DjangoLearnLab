# Deployment Configuration for HTTPS

## Overview
This document provides instructions for deploying the LibraryProject with HTTPS support using various web servers.

## Prerequisites
- Domain name registered and DNS configured
- SSL/TLS certificate obtained (e.g., from Let's Encrypt, commercial CA)
- Web server installed (Nginx or Apache)
- Django application deployed

## Option 1: Nginx Configuration

### 1. Install Nginx
```bash
sudo apt update
sudo apt install nginx
```

### 2. Obtain SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 3. Nginx Configuration File
Create/edit: `/etc/nginx/sites-available/libraryproject`
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect all HTTP requests to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS Server Block
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificate Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS Header (configured in Django, but can also be set here)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Additional Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Static Files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }
    
    # Media Files
    location /media/ {
        alias /path/to/your/project/media/;
    }
    
    # Proxy to Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Enable Configuration
```bash
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Auto-Renewal for Let's Encrypt
```bash
sudo certbot renew --dry-run
```

---

## Option 2: Apache Configuration

### 1. Install Apache and Enable SSL
```bash
sudo apt update
sudo apt install apache2
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod proxy
sudo a2enmod proxy_http
```

### 2. Obtain SSL Certificate
```bash
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

### 3. Apache Configuration File
Create/edit: `/etc/apache2/sites-available/libraryproject-ssl.conf`
```apache
# HTTP to HTTPS Redirect
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect all HTTP to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    # SSL Security Settings
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite HIGH:!aNULL:!MD5
    SSLHonorCipherOrder on
    
    # HSTS Header
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    
    # Security Headers
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    
    # Static Files
    Alias /static /path/to/your/project/staticfiles
    <Directory /path/to/your/project/staticfiles>
        Require all granted
    </Directory>
    
    # Media Files
    Alias /media /path/to/your/project/media
    <Directory /path/to/your/project/media>
        Require all granted
    </Directory>
    
    # Proxy to Django
    ProxyPreserveHost On
    ProxyPass /static !
    ProxyPass /media !
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # Set X-Forwarded-Proto for Django
    RequestHeader set X-Forwarded-Proto "https"
</VirtualHost>
```

### 4. Enable Configuration
```bash
sudo a2ensite libraryproject-ssl.conf
sudo apache2ctl configtest
sudo systemctl restart apache2
```

---

## Option 3: Gunicorn with Systemd

### 1. Install Gunicorn
```bash
pip install gunicorn
```

### 2. Create Gunicorn Service
Create: `/etc/systemd/system/libraryproject.service`
```ini
[Unit]
Description=LibraryProject Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/venv/bin"
ExecStart=/path/to/your/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    LibraryProject.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl start libraryproject
sudo systemctl enable libraryproject
sudo systemctl status libraryproject
```

---

## Django Configuration for Production

### 1. Update settings.py
Ensure these settings are configured in `settings.py`:
```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# If behind proxy (Nginx/Apache)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### 2. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 3. Run Migrations
```bash
python manage.py migrate
```

---

## SSL Certificate Options

### Option A: Let's Encrypt (Free, Recommended)
```bash
sudo certbot --nginx -d yourdomain.com
# OR
sudo certbot --apache -d yourdomain.com
```

**Pros:**
- Free
- Automatic renewal
- Widely trusted

**Cons:**
- 90-day validity (requires auto-renewal)

### Option B: Commercial SSL Certificate
1. Purchase from Certificate Authority (e.g., DigiCert, Comodo)
2. Generate CSR (Certificate Signing Request)
3. Submit CSR to CA
4. Receive certificate files
5. Install on web server

### Option C: Self-Signed Certificate (Development Only)
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

**Warning:** Not trusted by browsers. Use only for local development!

---

## Testing HTTPS Configuration

### 1. SSL Labs Test
Visit: https://www.ssllabs.com/ssltest/
Enter your domain and check SSL rating (aim for A+ grade)

### 2. Check Certificate
```bash
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

### 3. Test HSTS
```bash
curl -I https://yourdomain.com | grep -i strict
```

### 4. Test HTTP Redirect
```bash
curl -I http://yourdomain.com
# Should see 301 redirect to https://
```

### 5. Check Security Headers
```bash
curl -I https://yourdomain.com
```

Look for:
- `Strict-Transport-Security`
- `X-Frame-Options`
- `X-Content-Type-Options`
- `X-XSS-Protection`

---

## Troubleshooting

### Issue: "Too many redirects"
**Cause:** Both Django and web server redirecting to HTTPS
**Solution:** Disable `SECURE_SSL_REDIRECT` in Django, let web server handle redirects

### Issue: Static files not loading
**Cause:** HTTPS mixed content (loading HTTP resources on HTTPS page)
**Solution:** Ensure all resources use HTTPS or relative URLs

### Issue: "Not Secure" warning in browser
**Cause:** Invalid or expired SSL certificate
**Solution:** Check certificate validity, renew if needed

### Issue: HSTS not working
**Cause:** Not accessing via HTTPS first
**Solution:** Visit site via HTTPS first to receive HSTS header

---

## Security Checklist

Before going live:

- [ ] SSL certificate installed and valid
- [ ] HTTP redirects to HTTPS working
- [ ] HSTS headers configured (1 year)
- [ ] Secure cookies enabled
- [ ] Security headers configured
- [ ] `DEBUG = False` in production
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] Static files served over HTTPS
- [ ] SSL Labs test shows A+ rating
- [ ] Certificate auto-renewal configured
- [ ] Firewall configured (ports 80, 443 open)

---

## Maintenance

### Certificate Renewal (Let's Encrypt)
Automatic renewal runs via cron:
```bash
sudo certbot renew
```

Check renewal status:
```bash
sudo certbot certificates
```

### Monitor Certificate Expiry
Set up monitoring to alert 30 days before expiry

### Update Django
```bash
pip install --upgrade django
python manage.py check --deploy
```

---

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP HTTPS Best Practices](https://owasp.org/www-project-web-security-testing-guide/)

## Author
**Edidiong Aquatang**
- GitHub: [@E-d-d-i-e-A](https://github.com/E-d-d-i-e-A)
- ALX Software Engineering Program
