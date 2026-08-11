#!/bin/bash

echo "Attempting to connect to the service on localhost:8888..."
echo "This connection should hang or timeout if the server is suspended."
nc localhost 8888
echo "Connection attempt finished."
