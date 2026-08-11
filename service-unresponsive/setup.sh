#!/bin/bash

echo "Starting socat echo server on port 8888..."
socat TCP4-LISTEN:8888,fork,reuseaddr EXEC:'/bin/cat' &
echo $! > /tmp/socat_pid.txt
echo "socat server started with PID $(cat /tmp/socat_pid.txt). Press Ctrl+Z in this terminal to suspend it and simulate unresponsiveness."
echo "Use 'fg' to bring it back. Run cleanup.sh to stop it completely."
