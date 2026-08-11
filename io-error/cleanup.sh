#!/bin/bash

echo "Cleaning up I/O error device..."

# Ensure LOOP_DEV_PATH is set if this script is run independently
if [ -z "$LOOP_DEV_PATH" ]; then
    echo "Attempting to find loop device from /tmp/backing_device.img for cleanup."
    LOOP_DEV_PATH=$(sudo losetup -a | grep backing_device.img | awk '{print $1}' | sed 's/://')
fi

if [ -n "$LOOP_DEV_PATH" ] && [ -e "$LOOP_DEV_PATH" ]; then
    echo "Removing dmsetup error-device..."
    sudo dmsetup remove error-device || true # Ignore errors if already removed
    echo "Detaching loop device $LOOP_DEV_PATH..."
    sudo losetup -d "$LOOP_DEV_PATH" || true # Ignore errors if already detached
else
    echo "No active loop device found for /tmp/backing_device.img or LOOP_DEV_PATH not set. Skipping loop device cleanup."
fi

if [ -f "/tmp/backing_device.img" ]; then
    echo "Removing backing file /tmp/backing_device.img..."
    rm -f /tmp/backing_device.img
else
    echo "Backing file /tmp/backing_device.img not found. Skipping file cleanup."
fi

echo "Cleanup complete."
