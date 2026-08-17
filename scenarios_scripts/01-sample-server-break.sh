#!/bin/bash
# RHEL Lab "Break" Script

# 1. Setup a dummy "leaky" service
cat <<EOF | sudo tee /etc/systemd/system/leaky-app.service
[Unit]
Description=Simulated Memory Leak Application
[Service]
ExecStart=/bin/bash -c "node_memory=\$(grep MemTotal /proc/meminfo | awk '{print \$2}'); while true; do dd if=/dev/zero bs=1M count=100 >> /dev/null; sleep 0.1; done"
MemoryMax=500M
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# 2. Simulate Chrony Drift
# Note: This simply forces an offset; chronyd will eventually correct it
sudo systemctl stop chronyd
sudo date -s "+5 minutes"
sudo systemctl start chronyd

# 3. Trigger OOM Killer (Manual trigger if service doesn't hit it)
# We will create a background process that eats RAM rapidly
echo "Starting memory stressor..."
(head -c 1G /dev/zero | tail) &

