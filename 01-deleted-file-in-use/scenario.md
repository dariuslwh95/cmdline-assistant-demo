# Scenario 01: Discrepancy between `df` and `du` (Deleted File in Use)

This scenario demonstrates a common issue where `df` reports high disk usage, but `du` does not. This happens when a large file is deleted, but a process still holds it open.

## 1. Setup Guide
This scenario simulates the file handling issue. 
Run the setup script:
```bash
python3 01-deleted-file-in-use/setup.py
```
This script creates a 500MB file, opens it, and then deletes it while holding the file descriptor open for 5 minutes.

## 2. Diagnose & Analyze

While the script holds the file open, perform these steps in another terminal:

1. Check for the disk discrepancy:
   ```bash
   df -h .
   du -sh .
   ```

2. Identify the process holding the deleted file and pipe it to `c`:
   ```bash
   sudo lsof | grep '(deleted)' | c "Analyze this diagnostic output. Which process is holding the deleted file, and how can I free the disk space?"
   ```

Alternatively, you can run the command first and then use the `-w` flag:
   ```bash
   sudo lsof | grep '(deleted)'
   c "Analyze the latest output to identify the process holding deleted files and suggest a fix." -w 1
   ```

## 3. Cleanup
The script automatically exits after 5 minutes, releasing the handle.
