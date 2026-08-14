# Scenario: Insufficient Space on a Near-Empty Drive

**Based on:** A real-world issue where a background process consumes disk space in a way that is not visible to standard file-listing tools like `du`, causing "No space left" errors when there appears to be plenty of free space.

---

### 1. Objective
To demonstrate how `c` can help a user diagnose a confusing "No space left on device" error that conflicts with what `du` reports, leading to the discovery of a process holding a large, deleted file.

### 2. The Scripts
- **`setup.py`**: Simulates a background service that allocates a 1GB file, then "deletes" it while keeping it open. This makes the space it occupies invisible to `du` but still consumed from `df`'s perspective.
- **`cleanup.sh`**: A simple script that finds and terminates the `setup.py` "service" to release the file handle and free the disk space.

### 3. The Demonstration

#### Setup
For this scenario, imagine your current filesystem has at least 1.2GB of free space.
In your terminal, run the setup script to start the "background service". It will run for 10 minutes.
```bash
# Run the service in the background
python3 setup.py &
```
The script will confirm that it has allocated and "deleted" the 1GB file.

#### The Problem: Hitting an Invisible Wall
Now, imagine you are unaware of the background service. You need to download or create a large file.

1.  You check the free space with `df` to see what you have to work with.
    ```bash
    df -h .
    ```
    The output shows your available space has been reduced by 1GB, leaving you with (for example) only ~200MB.

2.  This is strange, as you don't remember having any large files here. You use `du` to verify.
    ```bash
    du -sh .
    ```
    `du` reports that the current directory is using virtually no space.

3.  Now you're confused. But you decide to proceed, attempting to create a 500MB file.
    ```bash
    fallocate -l 500M large_download.tmp
    ```
4.  The command fails instantly: `fallocate: large_download.tmp: fallocate failed: No space left on device`

You are now faced with a paradox: `df` says the space is used, `du` says it isn't, and the OS refuses to give you space that `du` claims is free.

#### Troubleshooting with `c`
You consult `c` immediately to make sense of the conflicting information.

1.  **Ask `c` about the paradox.**
    ```bash
    c "This makes no sense. I got a 'No space left' error trying to create a 500MB file. 'df' agrees I only have ~200MB free. But 'du' says the directory is empty! Where did my gigabyte of space go?"
    ```
    **Expected `c` Response:** The assistant should immediately identify this as a classic "deleted file held open" issue. It would explain that `df` reports the truth about the disk blocks, while `du` can only see files currently listed in the directory. It would recommend using `lsof` to find the process that is holding the invisible file.

2.  **Run the suggested command and ask for interpretation.** The `lsof` command can be intimidating, so you pipe it straight to `c`.
    ```bash
    sudo lsof | grep '(deleted)' | c "You suggested lsof. Here is the output. Can you tell me what's holding my space hostage?"
    ```
    **Expected `c` Response:** `c` will analyze the output and state clearly: "The process `python3` running the `setup.py` script (PID XXXXX) is holding a 1GB file open that has been deleted. This is why the space is consumed but not visible to `du`. To reclaim the space, this process must be stopped."

#### Resolution
`c` has solved the mystery. You now know exactly what is consuming the disk space and why it was hidden. You can confidently stop the offending "service" to resolve the issue.

#### Cleanup
Run the cleanup script to terminate the `setup.py` process.
```bash
bash cleanup.sh
```
After running the cleanup, `df -h .` will show the 1GB of space has been returned, and you can now create your 500MB file successfully.
