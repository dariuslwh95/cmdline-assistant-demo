# Scenario: Efficient System Information Gathering

**Based on:** A common task for a junior system administrator: collecting a snapshot of a system's state (CPU, memory, disk, processes) for review by a senior engineer.

---

### 1. Objective
To demonstrate how to use `c`'s capture mode (`--enable-capture`) to run a series of diagnostic commands and then use the workspace reference flag (`-w <index>`) to have `c` analyze and summarize the captured outputs without re-running the commands.

### 2. The Scripts
- **`setup.sh`**: (Empty) This is a read-only scenario that inspects the current state of the system. No setup is needed.
- **`cleanup.sh`**: (Empty) No cleanup is required as no changes are made to the system.

### 3. The Demonstration

#### The Task
Imagine a senior engineer has asked you to provide a quick "health report" of a server. They need to know the CPU type, current memory usage, disk capacity, and what the top processes are. Your task is to gather this raw data and then summarize it for them.

#### Phase 1: Data Collection with `--enable-capture`
First, you'll enter a special "capture" mode. This tells the assistant to save the output of every command you run.

1.  Start the session.
    ```bash
    c shell --enable-capture
    ```
    The assistant will acknowledge that it is now capturing outputs.

2.  Run the series of diagnostic commands. Don't worry about understanding the output for now; your job is just to collect it. Each command's output will be captured.

    ```bash
    # Capture 1: CPU Information
    lscpu
    
    # Capture 2: Memory Information
    free -h
    
    # Capture 3: Disk Filesystem Information
    df -h
    
    # Capture 4: Top 5 CPU-Consuming Processes
    ps aux --sort=-%cpu | head -n 6
    ```

You have now collected all the necessary data. The outputs are saved and indexed in your current session.

#### Phase 2: Analysis and Reporting with `-w`
Now, you will use the `-w` flag to reference the captured outputs by their index (1, 2, 3, etc.) and ask `c` to interpret them for you.

1.  First, ask for a summary of the CPU. You reference the first capture with `-w 1`.
    ```bash
    c -w 1 "Please summarize the CPU model name, architecture, and core count from this 'lscpu' output."
    ```
    **Expected `c` Response:** `c` will analyze the captured `lscpu` output and provide a clean, one-line summary like: "The CPU is an Intel Core i7-8750H (x86_64) with 12 cores."

2.  Next, get the memory status from the second capture.
    ```bash
    c -w 2 "How much total memory does this system have, and how much is currently available, based on this 'free' command output?"
    ```
    **Expected `c` Response:** "The system has 15Gi of total memory, with 8.5Gi currently available."

3.  Find the most stressed disk from the third capture.
    ```bash
    c -w 3 "Find the filesystem with the highest usage percentage in this 'df' output and report its status in a single line."
    ```
    **Expected `c` Response:** "The filesystem `/dev/sda1` has the highest usage at 85% (40G used / 50G total)."

4.  Finally, list the top processes from the fourth capture.
    ```bash
    c -w 4 "List the top 3 user-facing processes from this 'ps' output, ignoring system processes if possible."
    ```
    **Expected `c` Response:** `c` will parse the `ps` output and list the top 3 processes, likely ignoring things like the `ps` command itself.

#### Resolution
You have successfully separated the task of data collection from data analysis. By using `--enable-capture` and `-w`, you efficiently gathered raw data and then used the assistant to create clear, concise summaries for your report to the senior engineer, all without having to manually copy-paste or re-run commands.
