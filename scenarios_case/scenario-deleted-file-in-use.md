# Scenario: Discrepancy between `df` and `du` (Deleted File in Use)

This scenario demonstrates a common issue where `df` reports high disk usage, but `du` does not. This happens when a large file is deleted, but a process still holds it open. The disk space is not freed until the process closes the file handle.

## 1. The Script

Save the following Python script as `file_holder.py`:

```python
import time
import os

file_name = "large_file.tmp"
file_size_mb = 500

print(f"Creating a {file_size_mb}MB file named '{file_name}'...")

# Create a large file
with open(file_name, "wb") as f:
    f.write(b'\0' * file_size_mb * 1024 * 1024)

print("File created. Opening and then deleting it...")

# Open the file and keep the handle
file_handle = open(file_name, 'r')

# Delete the file from the filesystem
os.remove(file_name)

print(f"File '{file_name}' has been deleted, but the script is holding it open.")
print("Check 'df -h' and 'du -sh .' now.")
print("The script will keep the file open for 5 minutes.")

time.sleep(300)

print("Closing file handle and exiting. The space should now be freed.")
file_handle.close()
```

## 2. How to Run

1.  Open a terminal. Before running, check the current disk usage.
    ```bash
    df -h .
    du -sh .
    ```

2.  Run the Python script.
    ```bash
    python3 file_holder.py
    ```

3.  While the script is running (during the 5-minute sleep), open another terminal and check the disk usage again.
    ```bash
    df -h .
    du -sh .
    ```
    You will notice that `df` shows increased usage, but `du` does not account for the large file because it's no longer in the directory listing.

## 3. Expected Logs/Behavior for your assistant to analyze

There are no specific error logs for this scenario. The "symptom" is the discrepancy between `df` and `du`.

Your assistant should suggest commands to find the process holding the deleted file.

A key command for this is `lsof` (List Open Files):
```bash
# On Linux
sudo lsof +L1
# or more specifically
sudo lsof | grep '(deleted)'
```

The output of `lsof` will show the `python3` process with an open file descriptor to a file that is marked as `(deleted)`.

Example `lsof` output:
```
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NLINK  NODE NAME
python3 12345 myuser    3r   REG    8,1 524288000     0 12345 /path/to/large_file.tmp (deleted)
```

Your assistant's recommendation should be to either wait for the process to finish or, if it's safe to do so, to kill the process to release the file handle and free the disk space.
