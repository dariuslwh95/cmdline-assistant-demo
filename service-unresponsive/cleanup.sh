#!/bin/bash

echo "Cleaning up unresponsive service scenario..."

if [ -f "/tmp/socat_pid.txt" ]; then
    PID=$(cat /tmp/socat_pid.txt)
    if ps -p $PID > /dev/null; then
        echo "Killing socat process with PID $PID..."
        kill $PID
        # Wait for the process to actually terminate
        for i in {1..10}; do
            ps -p $PID > /dev/null || break
            sleep 0.1
        done
        ps -p $PID > /dev/null && echo "Warning: socat process $PID might still be running."
    else
        echo "socat process with PID $PID not found. It might have already exited."
    fi
    rm -f /tmp/socat_pid.txt
else
    echo "No socat PID file found (/tmp/socat_pid.txt). No process to kill."
fi

echo "Cleanup complete."
