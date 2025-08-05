#!/bin/bash

# Setup script for Nginx and SSL for bog-na-svyazi.ru

set -e

echo "🔧 Setting up Nginx and SSL for bog-na-svyazi.ru"

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Copy nginx config
echo "📋 Copying Nginx configuration..."
cp nginx-bog-na-svyazi.conf /etc/nginx/sites-available/bog-na-svyazi

# Enable the site
echo "✅ Enabling site..."
ln -sf /etc/nginx/sites-available/bog-na-svyazi /etc/nginx/sites-enabled/

# Test nginx config
echo "🧪 Testing Nginx configuration..."
nginx -t

# Reload nginx
echo "🔄 Reloading Nginx..."
systemctl reload nginx

# Setup SSL with Certbot
echo "🔐 Setting up SSL certificate..."
certbot --nginx -d bog-na-svyazi.ru -d www.bog-na-svyazi.ru

echo "✅ Setup complete!"
echo ""
echo "Your site should now be accessible at:"
echo "  - https://bog-na-svyazi.ru"
echo "  - https://www.bog-na-svyazi.ru"
echo ""
echo "Make sure to:"
echo "1. Point your domain DNS A records to your server IP"
echo "2. Open ports 80 and 443 in your firewall"
