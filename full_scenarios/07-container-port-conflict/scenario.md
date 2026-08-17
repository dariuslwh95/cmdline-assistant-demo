# Scenario: Container Port Conflict

**Based on:** A common operational issue where a containerized application fails to start due to a port already being in use on the host system, leading to "address already in use" or similar errors.

---

### 1. Objective
To demonstrate how `c` can help diagnose and resolve a container startup failure caused by a port conflict, guiding the user to identify the offending process and free up the port.

### 2. The Scripts
-   **`setup.sh`**: This script simulates the problem. It starts a dummy HTTP server on a specific port (e.g., 8080) in the background. Then, it attempts to launch a new container (e.g., Nginx) configured to bind to the *same* port, which will inevitably fail. The script will report this expected failure.
-   **`cleanup.sh`**: This script terminates the dummy HTTP server started by `setup.sh` and removes any lingering `failing_nginx` container, freeing up the port and restoring the system to its initial state.

### 3. The Demonstration

#### Setup
Run the setup script to create the port conflict. This script will confirm that the container failed to start due to the conflict.
```bash
bash setup.sh
```

#### The Problem: Container Failed to Start
You've just deployed a new containerized application, but it's not coming online. You check its status and logs, and see errors indicating a port binding issue.

1.  If you ran the `setup.sh` script, you would have seen output similar to:
    ```
    ...
    ERROR: for failing_nginx Cannot start service failing_nginx: driver failed programming external connectivity on endpoint failing_nginx (...): Error starting userland proxy: listen tcp 0.0.0.0:8080: bind: address already in use
    ```
    This indicates that the container failed to start because port `8080` was already in use.

2.  You can try to start the container again manually to reproduce the error (assuming `setup.sh` used `docker run --rm` which cleans up the failed container):
    ```bash
    docker run --rm --name failing_nginx -p 8080:8080 nginx:alpine
    # OR for podman
    # podman run --rm --name failing_nginx -p 8080:8080 nginx:alpine
    ```
    You will observe a similar error message.

3.  You are unsure which process is occupying port 8080.

#### Troubleshooting with `c`
You consult `c` for assistance in diagnosing this container startup issue. The `setup.sh` script has already saved the container's error output to `container_error.log`.

1.  **Ask `c` about the container error, attaching the log file.**
    ```bash
    c "My container (nginx:alpine) failed to start. I've attached the error log. Can you analyze it and tell me why it failed and what's using port 8080?" -a container_error.log
    ```
    **Expected `c` Response:** The assistant should analyze the attached `container_error.log`. It will identify the "bind: address already in use" error on port 8080. It will then explain that another process on the host machine is already listening on port 8080 and suggest using tools like `lsof -i :8080` or `netstat -tulnp | grep 8080` to identify the process.

2.  **Run the suggested command and ask for interpretation.** You execute the suggested command (e.g., `lsof`) and feed its output to `c`.
    ```bash
    sudo lsof -i :8080 | c "I ran 'lsof -i :8080' and got this output. Can you tell me what's using port 8080?"
    ```
    **Expected `c` Response:** `c` will analyze the `lsof` output. It will identify the `python3` process and its PID, clearly stating that it is the dummy HTTP server occupying port 8080. It will recommend terminating this process to free the port. (If an `sos report` were generated, `c` could similarly extract this information from the relevant network and process sections).

#### Resolution
`c` has identified the culprit. You can now confidently terminate the dummy server process.

1.  You can manually kill the process if you know its PID, or run the `cleanup.sh` script.

#### Cleanup
Run the cleanup script to terminate the dummy server and remove any failed containers.
```bash
bash cleanup.sh
```
After running the cleanup, you should be able to start your Nginx container successfully.
```bash
docker run --rm -p 8080:8080 nginx:alpine
# OR for podman
# podman run --rm -p 8080:8080 nginx:alpine
```
The Nginx container should now start without port conflicts.
