#!/bin/bash

echo "--- Cleaning up Container Port Conflict Scenario ---"

PORT=8080
DUMMY_SERVER_PID_FILE="/tmp/dummy_server_$PORT.pid"

# Check for Docker or Podman
if command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
elif command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
else
    echo "WARNING: Docker or Podman is not installed. Manual cleanup might be needed for containers."
    CONTAINER_CMD="" # Set to empty if neither is found
fi

# Kill dummy server if PID file exists
if [ -f "$DUMMY_SERVER_PID_FILE" ]; then
    DUMMY_SERVER_PID=$(cat "$DUMMY_SERVER_PID_FILE")
    if ps -p $DUMMY_SERVER_PID > /dev/null; then
        echo "Killing dummy server with PID $DUMMY_SERVER_PID..."
        kill $DUMMY_SERVER_PID
        sleep 1 # Give it a moment to terminate
        if ps -p $DUMMY_SERVER_PID > /dev/null; then
            echo "Dummy server PID $DUMMY_SERVER_PID still running. Force killing."
            kill -9 $DUMMY_SERVER_PID
        fi
    else
        echo "No dummy server process found with PID $DUMMY_SERVER_PID. It might have already exited."
    fi
    rm -f "$DUMMY_SERVER_PID_FILE"
    echo "Removed PID file: $DUMMY_SERVER_PID_FILE"
else
    echo "No dummy server PID file found ($DUMMY_SERVER_PID_FILE). Dummy server might not be running."
fi

# Stop and remove the failing_nginx container if it's still around
if [ -n "$CONTAINER_CMD" ]; then
    echo "Checking for and removing any lingering 'failing_nginx' container..."
    if $CONTAINER_CMD ps -a --format "{{.Names}}" | grep -q "failing_nginx"; then
        $CONTAINER_CMD stop failing_nginx > /dev/null 2>&1
        $CONTAINER_CMD rm failing_nginx > /dev/null 2>&1
        echo "Removed 'failing_nginx' container."
    else
        echo "No 'failing_nginx' container found."
    fi
fi

echo "--- Cleanup complete ---"
