#!/bin/bash

echo "Setting up I/O error device..."

# 1. Create a backing file
echo "Creating backing file /tmp/backing_device.img..."
dd if=/dev/zero of=/tmp/backing_device.img bs=1M count=100

# 2. Find an unused loop device and attach it
echo "Attaching loop device..."
LOOP_DEV=$(sudo losetup -fP /tmp/backing_device.img)
if [ $? -ne 0 ]; then
    echo "Error: Could not attach loop device."
    exit 1
fi
LOOP_DEV_PATH=$(sudo losetup -a | grep backing_device.img | awk '{print $1}' | sed 's/://')
echo "Using loop device: $LOOP_DEV_PATH"
export LOOP_DEV_PATH # Export for cleanup script

# 3. Use dmsetup to create a new device
echo "Creating dmsetup error-device..."
SIZE=$(sudo blockdev --getsz $LOOP_DEV_PATH)
if [ $? -ne 0 ]; then
    echo "Error: Could not get size of loop device."
    exit 1
fi
echo "0 $SIZE error" | sudo dmsetup create error-device
if [ $? -ne 0 ]; then
    echo "Error: Could not create dmsetup error-device."
    exit 1
fi

echo "I/O error device /dev/mapper/error-device created."
echo "You can now try to interact with it (e.g., sudo mkfs.ext4 /dev/mapper/error-device)"
echo "Remember to run cleanup.sh when done."
