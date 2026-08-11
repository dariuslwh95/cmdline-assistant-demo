# Scenario: Memory Exhaustion

This scenario simulates a situation where a process consumes a large amount of memory, leading to system instability and potentially triggering the OOM (Out of Memory) Killer. This is based on a real-world case where a Java application consumed nearly all available system memory.

## 1. The Script

Save the following Python script as `memory_hog.py`:

```python
import time

print("Starting to consume memory...")
megabytes_to_allocate = 2048  # Allocate 2GB
memory_hog = []
chunk_size = 1024 * 1024  # 1MB

try:
    for i in range(megabytes_to_allocate):
        memory_hog.append(b' ' * chunk_size)
        if (i + 1) % 100 == 0:
            print(f"Allocated {i + 1} MB...")
        time.sleep(0.01)
    print(f"Successfully allocated {megabytes_to_allocate} MB.")
    print("Holding memory for 5 minutes...")
    time.sleep(300)
except MemoryError:
    print("MemoryError: Could not allocate more memory.")
    print("Holding allocated memory for 5 minutes...")
    time.sleep(300)
finally:
    print("Releasing memory and exiting.")

```

## 2. How to Run

1.  Open a terminal and run the script:
    ```bash
    python3 memory_hog.py
    ```

2.  While the script is running, open another terminal and monitor the system's memory usage. You can use commands like `free -h`, `top`, or `htop`.

    ```bash
    watch -n 1 free -h
    ```

## 3. Simulating the problem

As the script allocates memory, you will see the `available` memory decrease. The system might become slow or unresponsive.

## 4. Expected Logs/Behavior for your assistant to analyze

Your assistant should be able to analyze logs from `dmesg` or `/var/log/syslog` (or equivalent) and look for OOM killer messages.

Example of what to look for in `dmesg`:

```
[ ... ] invoked oom-killer: gfp_mask=0x..., order=0, oom_score_adj=0
[ ... ] oom_kill_process+0x.../0x...
[ ... ] Out of memory: Kill process ... (python3) score ... or sacrifice child
[ ... ] Killed process ... (python3) total-vm:..., anon-rss:..., file-rss:..., shmem-rss:...
```

Your assistant could suggest:
*   Identifying the process consuming the most memory.
*   Checking for memory leaks in the application.
*   Analyzing the OOM killer logs.
*   Suggesting to increase swap or physical memory if the usage is legitimate.
