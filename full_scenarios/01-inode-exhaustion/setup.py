import os
import sys
import errno

dir_name = "lotsoffiles"
file_count = 200000  # A large number, may not be reached if inodes run out first

print(f"Attempting to create up to {file_count} small files in '{dir_name}'...")
sys.stdout.flush()

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

try:
    for i in range(file_count):
        # Create an empty file
        with open(os.path.join(dir_name, f"file_{i}.tmp"), "w") as f:
            pass
        if (i + 1) % 10000 == 0:
            print(f"Created {i + 1} files...")
            sys.stdout.flush()
    print(f"Successfully created {file_count} files without error.")
except OSError as e:
    if e.errno == errno.ENOSPC:
        print(f"\nSUCCESS (for the demo): Ran out of space at file number {i}.")
        print("The system is now in a state where it may report 'No space left on device' for new files.")
        sys.stdout.flush()
    else:
        print(f"\nAn unexpected OS error occurred: {e}")
        sys.stdout.flush()
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("\nThe setup script has finished. The scenario is ready.")
sys.stdout.flush()
