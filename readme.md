# Command Line Assistant - Scenarios Repository

This repository contains scenarios and scripts designed to test and demonstrate the **Command Line Assistant** (`c`). It provides reproducible cases for understanding system behavior and evaluating the assistant's diagnostic capabilities.

## Installation of Command Line Assistant

To install or set up the Command Line Assistant:

1. **Install the CLI package**:
   ```bash
   sudo dnf install commandline-assistant
   ```

2. **Configure the endpoint**:
   ```bash
   sudo vi /etc/xdg/command-line-assistant/config.toml
   ```
   Set the endpoint:
   ```toml
   endpoint = "https://demosat-ha.infra.demo.redhat.com/api/lightspeed/v1"
   ```

3. **Restart the service**:
   ```bash
   sudo systemctl restart clad
   ```

## Repository Structure

The scenarios are numbered for easy navigation:

*   **`01-deleted-file-in-use/`**: Discrepancy between `df` and `du`.
*   **`02-io-error/`**: Simulated I/O errors on a block device.
*   **`03-memory-exhaustion/`**: Memory hogging and OOM killer simulation.
*   **`04-service-unresponsive/`**: Unresponsive network service.

## Usage

1. **Navigate to a scenario directory**:
   ```bash
   cd 01-deleted-file-in-use
   ```
2. **Read the `scenario.md`**: Each folder contains a detailed guide.
3. **Execute Setup**: Run the `setup.sh` or `setup.py` provided in the folder.
4. **Diagnose with the Assistant (`c`)**: Use pipes or the `-w` (with-output) flag as described in the `scenario.md`.
   * **Direct Pipe**: `command | c "Question"`
   * **Capture Output & Analyze**:
     ```bash
     command
     c "Question about the output" -w 1
     ```
5. **Cleanup**: Always run the provided `cleanup.sh` when finished.
