#!/usr/bin/env bash
#
# setup_sos_demo.sh
# Sets up sample services, triggers common system/application errors,
# and generates a populated sos report for analysis.

set -euo pipefail

# Ensure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root." >&2
   exit 1
fi

echo "=================================================="
echo " 1. Installing Required Packages"
echo "=================================================="
dnf install -y httpd mariadb-server podman sos audit

echo "=================================================="
echo " 2. Enabling and Starting Core Services"
echo "=================================================="
sudo systemctl enable --now mariadb
sudo systemctl enable --now auditd

echo "=================================================="
echo " 3. Deploying Containerized Application via Podman"
echo "=================================================="
# Pull and run container on port 8080
podman run -d --name sample-app -p 8080:8080 registry.access.redhat.com/ubi9/nginx-122 nginx -g "daemon off;"

echo "=================================================="
echo " 4. Generating Sample Traffic & Audit Logs"
echo "=================================================="
# Generate HTTPD access logs
curl -s http://localhost/ > /dev/null || true
curl -s http://localhost/non-existent-page > /dev/null || true

# Generate Podman Nginx logs
curl -s http://localhost:8080/ > /dev/null || true
