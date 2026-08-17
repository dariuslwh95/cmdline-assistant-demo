# Scenario: The Phantom Space Eater

**Based on:** A real-world issue where a background process consumes disk space in a way that is not visible to standard file-listing tools, causing unexpected "No space left on device" errors. This version is dynamically sized to be effective on any filesystem.

---

### 1. Objective
To demonstrate how `c` can diagnose a "No space left on device" error when the user is faced with conflicting information from `df` (which shows the disk is full) and `du` (which shows the disk is empty).

### 2. The Scripts
- **`setup.py`**: A smart script that simulates a runaway background service. It dynamically checks the available space on your filesystem and creates a file that consumes 90% of it. It then deletes the file while keeping it open, making the consumed space invisible to `du`.
- **`cleanup.sh`**: A simple script that finds and terminates the `setup.py` "service" to release the file handle and instantly free the disk space.

### 3. The Demonstration

#### Setup
In your terminal, run the setup script as a background process. Pay attention to its output—it will tell you how much space it's consuming.
```bash
# Run the service in the background
python3 setup.py &
```

#### The Problem: Hitting the Wall
A "misbehaving service" is now running. Imagine you are unaware of it and need to create a large file.

1.  You run a quick check of your available space.
    ```bash
    df -h .
    ```
    You'll see a massive drop in available space, with only 10% of what you started with remaining. Let's say you have only **2GB** left.

2.  Alarmed, you immediately hunt for the huge file that must be responsible.
    ```bash
    du -sh .
    ```
    But `du` reports that the directory is nearly empty. This is the central paradox: `df` shows the space is gone, but `du` can't find where it went.

3.  To see which tool is "right," you try to create a file that is clearly larger than the space `df` reports as available (e.g., 3GB if `df` shows 2GB free).
    ```bash
    fallocate -l 5G large_download.tmp
    ```
4.  The command fails instantly: `fallocate: large_download.tmp: fallocate failed: No space left on device`

5.  Show a comparison between du and dh
    ```bash
    pwd
    ```

This confirms `df` is correct about the lack of space, making `du`'s conflicting report a complete mystery. You're stuck.

#### Troubleshooting with `c`
You consult `c` immediately to make sense of this impossible situation.

1.  **Ask `c` about the paradox.**
    ```bash
    c "This is baffling. The OS says 'No space left on device' and 'df' confirms I have almost no space free. But 'du' insists my directory is empty! Where could all that space have gone?"
    ```
    **Expected `c` Response:** The assistant should immediately recognize this classic "deleted file held open" issue. It would explain that `df` reports the truth about the disk blocks, while `du` can only see files currently listed in directories. It will recommend using `lsof` to find the process that is holding an invisible, deleted file open.

2.  **Run the suggested command and ask for interpretation.** The `lsof` command is notoriously verbose, so you pipe its output directly to `c` for a clean explanation.
    ```bash
    sudo lsof | grep '(deleted)' | c "You suggested lsof, and it found something. Can you interpret this output and tell me what's eating my disk space?"
    ```
    **Expected `c` Response:** `c` will analyze the output and state clearly: "The `python3` process running the `setup.py` script is holding a large file open that has been deleted. The file's size matches the amount of 'missing' space. To reclaim the space, this process must be stopped."

#### Resolution
`c` has solved the mystery. You now know exactly what is consuming the disk space and why it was hidden. You can confidently stop the offending "service" to resolve the issue.

#### Cleanup
Run the cleanup script to terminate the `setup.py` process.
```bash
bash cleanup.sh
```
After running the cleanup, `df -h .` will show that all your disk space has been returned.
