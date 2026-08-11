# Scenario 04: Unresponsive Network Service

This scenario simulates a network service that becomes unresponsive, causing client connections to hang or timeout.

## 1. Setup Guide
This simulation uses `socat` to run a server.
1. Open a server terminal and start the service:
   ```bash
   04-service-unresponsive/setup.sh
   ```
2. Open a separate client terminal.

## 2. Simulate & Diagnose

1. In the server terminal, press `Ctrl+Z` to suspend the process, making it unresponsive.
2. In the client terminal, attempt a connection (it will hang):
   ```bash
   04-service-unresponsive/simulate.sh
   ```
3. Diagnose and analyze with `c`:
   ```bash
   # Check process status and pipe to c
   ps aux | grep socat | c "The connection is timing out. Analyze this process status. Is it responsive?"

   # Check network status and analyze
   ss -tlpn | grep 8888 | c "Is this port actively accepting connections? Why might connections be hanging?"
   ```

## 3. Cleanup
In the server terminal, bring the job to the foreground with `fg` and terminate it, or run:
```bash
04-service-unresponsive/cleanup.sh
```
