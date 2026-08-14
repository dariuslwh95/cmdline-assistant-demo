#!/bin/bash
echo "Cleaning up the directory with numerous small files..."
if [ -d "lotsoffiles" ]; then
  rm -rf lotsoffiles
  echo "Directory 'lotsoffiles' has been removed."
else
  echo "Directory 'lotsoffiles' not found. Nothing to clean up."
fi
