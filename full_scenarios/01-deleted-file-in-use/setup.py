import os
import sys
import time

file_name = "dynamic_large_file.tmp"

# --- Dynamic Space Calculation ---
try:
    # Get filesystem stats for the current directory
    fs_stats = os.statvfs('.')
    # Available space in bytes for non-super-user
    available_space = fs_stats.f_frsize * fs_stats.f_bavail
    
    # Calculate a file size that is 90% of the available space
    # This ensures the effect is dramatic and leaves a small amount of space free
    file_size_bytes = int(available_space * 0.9)
    file_size_gb = file_size_bytes / (1024**3)

    if file_size_gb < 0.5:
        print("ERROR: Not enough free space (less than 500MB) to run this demo effectively.", file=sys.stderr)
        sys.exit(1)

except Exception as e:
    print(f"ERROR: Could not determine available disk space: {e}", file=sys.stderr)
    sys.exit(1)
# ------------------------------------

print(f"INFO: Filesystem has {available_space / (1024**3):.2f} GB free.", flush=True)
print(f"INFO: This script will simulate a service consuming 90% of that: {file_size_gb:.2f} GB.", flush=True)

try:
    with open(file_name, "wb") as f:
        os.fallocate(f.fileno(), 0, file_size_bytes)
except Exception as e:
    print(f"ERROR: Could not create the large file with fallocate: {e}", file=sys.stderr)
    print("INFO: Try running again. If this persists, your filesystem may not support fallocate.", file=sys.stderr)
    sys.exit(1)

print(f"INFO: File '{file_name}' created ({file_size_gb:.2f} GB).", flush=True)
print("INFO: Now, this 'service' will 'delete' the file but hold it open, hiding the space usage from 'du'.", flush=True)

try:
    file_handle = open(file_name, 'rb')
    os.remove(file_name)

    print(f"INFO: File '{file_name}' removed, but held open by this process.", flush=True)
    print(f"INFO: The scenario is ready. This script will run for 10 minutes.", flush=True)

    time.sleep(600)

finally:
    print("INFO: 'Service' shutting down, closing file handle.", flush=True)
    if 'file_handle' in locals():
        file_handle.close()
