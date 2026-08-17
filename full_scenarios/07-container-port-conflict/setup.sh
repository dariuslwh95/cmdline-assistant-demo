#!/bin/bash

echo "--- Setting up Container Port Conflict Scenario ---"

# Check for Docker or Podman
if command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
elif command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
else
    echo "ERROR: Docker or Podman is not installed. Please install one to run this scenario."
    exit 1
fi

echo "Using container command: $CONTAINER_CMD"

PORT=8080
DUMMY_SERVER_PID_FILE="/tmp/dummy_server_$PORT.pid"

echo "1. Starting a dummy HTTP server on port $PORT..."
# Start a simple Python HTTP server in the background
# We use nohup and & to ensure it runs even if the script exits
# We also redirect stdout/stderr to a file to keep the terminal clean
nohup python3 -m http.server $PORT > /dev/null 2>&1 &
DUMMY_SERVER_PID=$!
echo $DUMMY_SERVER_PID > $DUMMY_SERVER_PID_FILE
echo "Dummy server started with PID $DUMMY_SERVER_PID, listening on port $PORT."
echo "PID stored in $DUMMY_SERVER_PID_FILE"
sleep 2 # Give the server a moment to start

# Verify the port is in use
if ! lsof -i tcp:$PORT > /dev/null; then
    echo "ERROR: Dummy server failed to bind to port $PORT. Exiting."
    kill $DUMMY_SERVER_PID
    rm -f $DUMMY_SERVER_PID_FILE
    exit 1
fi
echo "Port $PORT is now occupied by the dummy server."

echo "2. Attempting to run a container that tries to bind to the same port $PORT..."
echo "This command is expected to fail with a port conflict error."

# Run a simple nginx container that tries to bind to the same port
# We use --rm to clean up the container automatically on exit/failure
# We do NOT run in detached mode so we can see the error immediately
$CONTAINER_CMD run --rm --name failing_nginx -p $PORT:$PORT nginx:alpine

if [ $? -ne 0 ]; then
    echo "SUCCESS: The container failed to start as expected due to port conflict."
    echo "The scenario is now set up. The dummy server is still running on port $PORT."
    echo "To clean up, run: bash cleanup.sh"
else
    echo "ERROR: The container unexpectedly started. The scenario setup failed."
    # Attempt to stop and remove the container if it somehow started
    $CONTAINER_CMD stop failing_nginx > /dev/null 2>&1
    $CONTAINER_CMD rm failing_nginx > /dev/null 2>&1
    kill $DUMMY_SERVER_PID
    rm -f $DUMMY_SERVER_PID_FILE
    exit 1
fi
