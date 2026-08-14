import os
import sys
import errno

dir_name = "lotsoffiles"
counter = 0

print(f"Starting to create files in '{dir_name}' until the filesystem runs out of inodes...")
sys.stdout.flush()

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

try:
    # This loop will continue indefinitely until the OS throws an error
    while True:
        # Create an empty file
        with open(os.path.join(dir_name, f"file_{counter}.tmp"), "w") as f:
            pass
        
        counter += 1
        
        # Provide progress feedback every 10,000 files
        if counter % 10000 == 0:
            print(f"Created {counter} files...")
            sys.stdout.flush()

except OSError as e:
    # This is the expected error when we run out of inodes or data blocks
    if e.errno == errno.ENOSPC:
        print(f"\nSUCCESS (for the demo): The OS reported 'No space left on device' after creating {counter} files.")
        print("This is the desired state for the scenario.")
        sys.stdout.flush()
    else:
        print(f"\nAn unexpected OS error occurred after creating {counter} files: {e}")
        sys.stdout.flush()
except Exception as e:
    print(f"\nAn unexpected generic error occurred after creating {counter} files: {e}")
    sys.stdout.flush()

print("\nThe setup script has finished. The scenario is ready for investigation.")
sys.stdout.flush()
