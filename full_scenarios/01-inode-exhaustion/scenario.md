# Scenario: The Invisible Wall - No Space With Gigabytes Free

**Based on:** A subtle and confusing real-world issue where a filesystem has plenty of free space in gigabytes, but no new files can be created due to running out of inodes.

---

### 1. Objective
To demonstrate how `c` can instantly diagnose a non-obvious filesystem limit (inode exhaustion) that makes a user think their disk is full when it appears to be empty.

### 2. The Scripts
- **`setup.py`**: Simulates a runaway process (like a bad caching or build script) that creates hundreds of thousands of tiny, empty files. This doesn't consume much disk *space*, but it is designed to use up all the available *inodes* on the filesystem, triggering the "No space left on device" error.
- **`cleanup.sh`**: A simple script to remove the directory containing all the small files, freeing up the inodes and returning the system to normal.

### 3. The Demonstration

#### Setup
In your terminal, run the setup script. This will simulate the runaway process. Depending on your filesystem's configuration, this may take a minute or two.
```bash
python3 setup.py
```
The script will print its progress and will stop once it has (hopefully) exhausted the system's inodes.

#### The Problem: Hitting an Invisible Wall
Imagine you're a developer. After the setup script finishes, you continue with your work. You try to do something simple, like creating a log file.

1.  You attempt to create a new, empty file.
    ```bash
    touch my_test_file.txt
    ```
2.  The command immediately fails with a baffling error: `touch: cannot touch 'my_test_file.txt': No space left on device`

3.  This makes no sense. You instantly check the disk space, positive that there are gigabytes free.
    ```bash
    df -h .
    ```
    And you're right! The output shows plenty of space (e.g., `40G` available). You have tons of room. Yet you can't even create a zero-byte file. You are completely stuck.

#### Troubleshooting with `c`
This situation seems impossible, so you consult `c` right away.

1.  **Ask `c` about the paradox.**
    ```bash
    c "This is crazy. My server says 'No space left on device' when I try to create a file, but 'df -h' shows I have over 40GB free. What could possibly be wrong?"
    ```
    **Expected `c` Response:** The assistant should immediately recognize this classic symptom. It would explain that Linux filesystems have two main limits: **data blocks** (for file contents, measured by `df -h`) and **inodes** (for file metadata, one for every file/directory). It will state that you have likely exhausted your inodes and suggest you verify this with the command `df -i`.

2.  **Verify the diagnosis.** You run the command `c` suggested to check the inode usage.
    ```bash
    df -i .
    ```
    The output now shows the truth: the `IUse%` (inode usage percentage) is at 100%.

3.  **Ask `c` for the next step.** You now understand the "what" but not the "where."
    ```bash
    df -i | c "You were right, my inode usage is 100%. How can I find which directory is using all of them?"
    ```
    **Expected `c` Response:** `c` will provide a command pipeline to count the number of files in each subdirectory and sort them to find the culprit. For example: `du --inodes -S . | sort -rh | head -10`. It would explain that this command specifically counts inodes instead of data blocks.

4.  **Pinpoint the source.** You run the command, and it clearly points to the `lotsoffiles` directory created by the setup script as containing hundreds of thousands of files.

#### Resolution
`c` helped you diagnose a problem you didn't even know was possible. You went from a confusing paradox to a clear understanding of inode exhaustion and a precise location of the offending files, all within a few commands.

#### Cleanup
Run the cleanup script to delete the `lotsoffiles` directory and free up the inodes.
```bash
bash cleanup.sh
```
After running the cleanup, you can confirm that `touch my_test_file.txt` now works perfectly.
