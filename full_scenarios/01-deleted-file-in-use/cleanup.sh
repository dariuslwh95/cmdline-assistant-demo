#!/bin/bash
echo "INFO: Attempting to stop the background service (setup.py) to release the hidden file..."
PIDS=$(pgrep -f "setup.py")

if [ -z "$PIDS" ]; then
  echo "INFO: No running 'setup.py' script found."
else
  kill $PIDS
  echo "INFO: Sent termination signal to 'setup.py' process(es) with PIDs: $PIDS."
  echo "INFO: The disk space should now be free."
fi
