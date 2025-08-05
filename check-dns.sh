#!/bin/bash

echo "🔍 Checking DNS records..."
echo ""
echo "bog-na-svyazi.ru:"
dig +short bog-na-svyazi.ru
echo ""
echo "www.bog-na-svyazi.ru:"
dig +short www.bog-na-svyazi.ru
echo ""
echo "Your DuckDNS domain:"
dig +short kostiuki.duckdns.org
echo ""
echo "Current server IP:"
curl -s ifconfig.me
echo ""