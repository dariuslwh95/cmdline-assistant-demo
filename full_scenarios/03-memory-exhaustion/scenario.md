# Scenario 03: Memory Exhaustion

This scenario simulates a process that rapidly consumes system memory, potentially triggering the OOM (Out of Memory) Killer.

## 1. Setup Guide
Run the provided Python script to simulate high memory usage:
```bash
python3 03-memory-exhaustion/setup.py
```

## 2. Diagnose & Analyze

While the script runs, monitor memory usage and analyze with `c`.

1. Check system memory state:
   ```bash
   free -h
   ```

2. Analyze memory usage or system logs with `c`:
   ```bash
   # Option 1: Pipe current memory usage
   free -h | c "Analyze this memory usage. Is this critical?"

   # Option 2: Analyze system logs for OOM events
   sudo dmesg | grep -i "oom" | tail -n 10 | c "Are there OOM killer events here? Explain them."
   ```

Alternatively, use `-w` if you've already captured the logs:
   ```bash
   sudo dmesg | tail -n 50
   c "Analyze the logs above for OOM killer activity." -w 1
   ```

## 3. Cleanup
The script will automatically release memory and exit after 5 minutes.
