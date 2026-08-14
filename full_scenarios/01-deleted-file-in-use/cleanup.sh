#!/bin/bash
echo "INFO: Attempting to stop the background service (setup.py) to release the hidden file..."
PIDS=$(pgrep -f "setup.py")

if [ -z "$PIDS" ]; then
  echo "INFO: No running 'setup.py' script found."
else
  kill $PIDS
  echo "INFO: Sent termination signal to 'setup.py' process(es) with PIDs: $PIDS."
fi

# Explicitly remove the created file
echo "INFO: Removing the dynamically created large file..."
rm -f dynamic_large_file.tmp

echo "INFO: Cleanup complete. The disk space should now be fully free."
