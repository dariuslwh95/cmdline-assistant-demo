# Command Line Assistant - Scenarios Repository

This repository contains various scenarios and scripts designed to demonstrate and test the capabilities of the Command Line Assistant. It serves as a collection of reproducible cases for understanding system behavior under different conditions and for evaluating the assistant's diagnostic and resolution suggestions.

## Repository Contents

*   **`scenarios_case/`**: This directory holds markdown files (`.md`) describing different system scenarios. Each file details a specific problem or condition, providing context and expected outcomes. These are meant for understanding the problem space.
*   **`scenarios_scripts/`**: This directory contains executable shell scripts (`.sh`) that can be used to set up or simulate the conditions described in the `scenarios_case` markdown files. These scripts are designed to be run in a controlled environment to reproduce specific system states.

## How to Use This Repository

1.  **Understand the Scenarios**: Browse the `.md` files in `scenarios_case/` to understand the various system problems and their contexts.
2.  **Reproduce Conditions**: Use the corresponding `.sh` scripts in `scenarios_scripts/` to set up the environment that triggers the scenario described in the markdown file.
    *   **Caution**: These scripts might modify your system state. Always review their contents before execution and run them in a safe, controlled environment (e.g., a virtual machine or a test container).
    *   To run a script: `bash scenarios_scripts/01-sample-server-break.sh` (replace with the desired script).
3.  **Engage the Command Line Assistant**: Once a scenario's conditions are set up, use the Command Line Assistant to diagnose the problem, analyze system logs, and suggest potential fixes. The assistant should leverage its capabilities to interpret the system's state as set by the scenario scripts.

## What is the Command Line Assistant?

The Command Line Assistant is an intelligent tool designed to assist users with diagnosing and resolving issues within command-line environments. It integrates with various system tools and services to provide context-aware suggestions, automate troubleshooting steps, and offer solutions based on observed system states. Its goal is to streamline operations, reduce diagnostic time, and empower users with expert knowledge directly in their terminal.

## Command Line Assistant Setup (Specific Environment)

The following instructions are for setting up the Command Line Assistant to connect to a specific backend endpoint, often required in enterprise or specific testing environments.

```bash
sudo vi /etc/xdg/command-line-assistant/config.toml
```
Add or update the following in `config.toml`:
```toml
endpoint = "https://demosat-ha.infra.demo.redhat.com/api/lightspeed/v1"
```
After modifying the configuration, restart the assistant service:
```bash
sudo systemctl restart clad
```

### Verify Trust (If needed)
If you still get an authentication error after the redirect, ensure your system trusts the Satellite's certificate. Since your `insights-client --test-connection` was successful, this is likely already set up, but you can double-check by ensuring the Satellite CA is in the trust store:
```bash
# Verify connection to the new endpoint
curl -v https://demosat-ha.infra.redhat.com/api/lightspeed/v1
```
