import os
import sys
import time
import errno

file_name = "large_background_file.tmp"
# Use a large but not excessive file size for the demo
file_size_mb = 1024  # 1 GB
file_size_bytes = file_size_mb * 1024 * 1024

print(f"INFO: This script simulates a background service consuming {file_size_mb}MB of disk space.")
sys.stdout.flush()

try:
    # Use fallocate for instant, non-sparse file creation, common on RHEL
    with open(file_name, "wb") as f:
        os.fallocate(f.fileno(), 0, file_size_bytes)
except AttributeError:
    # Fallback for non-Linux systems
    with open(file_name, "wb") as f:
        f.write(b'\0' * file_size_bytes)
except Exception as e:
    print(f"ERROR: Could not create the large file: {e}")
    sys.exit(1)


print(f"INFO: File '{file_name}' created ({file_size_mb}MB).")
print("INFO: Now, this 'service' will 'delete' the file but hold it open, hiding the space usage from 'du'.")
sys.stdout.flush()

try:
    # Open the file and keep the handle
    file_handle = open(file_name, 'rb')

    # Delete the file from the filesystem so it's hidden from `ls` and `du`
    os.remove(file_name)

    print(f"INFO: File '{file_name}' removed, but held open by this process.")
    print("INFO: The scenario is ready. This script will run for 10 minutes.")
    sys.stdout.flush()

    time.sleep(600)

finally:
    print("INFO: 'Service' shutting down, closing file handle.")
    sys.stdout.flush()
    if 'file_handle' in locals():
        file_handle.close()
