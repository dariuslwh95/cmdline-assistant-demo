# Trigger an audit log entry via auditctl rule check / login attempt
auditctl -w /etc/shadow -p wa -k shadow_mon
touch /etc/shadow

echo "=================================================="
echo " 5. Injecting Common System & Service Errors"
echo "=================================================="
# A. HTTPD Error: Access denied / 403 Forbidden entry
touch /var/www/html/forbidden.html
chmod 000 /var/www/html/forbidden.html
curl -s http://localhost/forbidden.html > /dev/null || true
rm -f /var/www/html/forbidden.html

# B. MariaDB Error: Failed login attempt (populates mariadb/journal error logs)
mysql -u root -pWrongPassword -e "SHOW DATABASES;" 2>/dev/null || true

# C. Failed Systemd Service: Create a dummy service that intentionally crashes
cat <<'EOF' > /etc/systemd/system/failing-demo.service
[Unit]
Description=Failing Demo Service for SOS Report
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c "echo 'ERROR: Initialization failed due to missing configuration key!' >&2; exit 1"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start failing-demo.service || true

# D. SELinux / Permission warning (Log permission denial to journal/audit)
logger -p daemon.err -t demo_app "CRITICAL: Database connection connection string pool exhausted."
