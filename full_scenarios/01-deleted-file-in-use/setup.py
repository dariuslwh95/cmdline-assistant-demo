import os
import sys
import time
import subprocess # Keep subprocess for calling fallocate utility

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

# --- File Creation using fallocate utility ---
try:
    # Call the fallocate utility directly
    subprocess.run(
        ["fallocate", "-l", str(file_size_bytes), file_name],
        check=True, # Raise an exception for non-zero exit codes
        capture_output=True # Capture stdout/stderr to avoid polluting console
    )
    print(f"INFO: File '{file_name}' created using 'fallocate' command ({file_size_gb:.2f} GB).", flush=True)
except subprocess.CalledProcessError as e:
    print(f"ERROR: 'fallocate' command failed: {e.stderr.decode()}", file=sys.stderr)
    sys.exit(1)
except FileNotFoundError:
    print(f"ERROR: 'fallocate' command not found. Cannot create large file.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"ERROR: An unexpected error occurred during file creation: {e}", file=sys.stderr)
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
