import os
import sys
import time
import subprocess # New import for dd fallback

file_name = "dynamic_large_file.tmp"

# --- Dynamic Space Calculation ---
try:
    fs_stats = os.statvfs('.')
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

# --- File Creation with Robust Fallback ---
file_created = False
try:
    with open(file_name, "wb") as f:
        # Attempt to use os.fallocate
        os.fallocate(f.fileno(), 0, file_size_bytes)
    print(f"INFO: File '{file_name}' created using os.fallocate ({file_size_gb:.2f} GB).", flush=True)
    file_created = True
except AttributeError:
    # Fallback if os.fallocate does not exist, use dd via subprocess
    print(f"INFO: os.fallocate not available. Falling back to 'dd' command. This might take a moment for {file_size_gb:.2f} GB.", flush=True)
    try:
        # Using dd to create a non-sparse file filled with zeros
        # bs=1M and count=int(size/1M) is more efficient for large files
        dd_count = int(file_size_bytes / (1024*1024))
        # Ensure count is at least 1 for very small sizes
        if dd_count == 0 and file_size_bytes > 0:
            dd_count = 1
            bs_val = file_size_bytes
        else:
            bs_val = 1024*1024 # 1MB

        result = subprocess.run(
            ["dd", "if=/dev/zero", f"of={file_name}", f"bs={bs_val}", f"count={dd_count}", "status=none"],
            check=True, # Raise an exception for non-zero exit codes
            capture_output=True # Capture stdout/stderr to avoid polluting console, though status=none might handle this
        )
        print(f"INFO: File '{file_name}' created using 'dd' command ({file_size_gb:.2f} GB).", flush=True)
        file_created = True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: 'dd' command failed: {e.stderr.decode()}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: 'dd' command not found. Cannot create large file without os.fallocate.", file=sys.stderr)
        sys.exit(1)
except OSError as e:
    # Catch actual OS errors from fallocate (e.g., permission denied, actual disk full)
    print(f"ERROR: Could not create the large file with os.fallocate: {e}", file=sys.stderr)
    print("INFO: Ensure your filesystem supports fallocate or that there's enough physical disk space.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    # Catch any other unexpected errors during file creation
    print(f"ERROR: An unexpected error occurred during file creation: {e}", file=sys.stderr)
    sys.exit(1)

if not file_created:
    print("ERROR: File could not be created by any method.", file=sys.stderr)
    sys.exit(1)

print("INFO: Now, this 'service' will 'delete' the file but hold it open, hiding the space usage from 'du'.", flush=True)
sys.stdout.flush()

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
