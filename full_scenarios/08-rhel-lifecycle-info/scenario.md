# Scenario: RHEL Lifecycle Information Query

**Based on:** The common need for system administrators and developers to determine the support status and lifecycle dates of Red Hat Enterprise Linux versions to ensure compliance, plan upgrades, or understand security update availability.

---

### 1. Objective
To demonstrate how `c` can assist in quickly retrieving authoritative lifecycle and support phase information for specific RHEL versions or components.

### 2. The Scripts
-   **`setup.sh`**: This script sets the context for the scenario by presenting a hypothetical RHEL version (e.g., RHEL 7.9) for which the user needs to find lifecycle information. It does not make any persistent changes to the system.
-   **`cleanup.sh`**: As the `setup.sh` makes no system changes, this script simply confirms that no cleanup is required.

### 3. The Demonstration

#### Setup
Run the setup script to understand the context of the scenario.
```bash
bash setup.sh
```
The script will output a hypothetical RHEL version (e.g., "Red Hat Enterprise Linux release 7.9 (Maipo)"), which is the focus of your query to `c`.

#### The Problem: Understanding RHEL Support Status
You are managing a system running an older version of RHEL, and you need to determine its current support status, including when its various lifecycle phases (e.g., Maintenance Support, Extended Life Cycle Support) began and ended, or when they are projected to end. This information is crucial for planning system upgrades, assessing security patch availability, or ensuring compliance. You need to quickly get this information without sifting through extensive documentation online.

#### Troubleshooting with `c`
You consult `c` for assistance in obtaining this critical lifecycle information.

1.  **Ask `c` for RHEL lifecycle information.**
    You have identified that your system is running RHEL 7.9. You want to know its lifecycle details.
    ```bash
    c "What is the lifecycle and support status for Red Hat Enterprise Linux 9.6? Include key dates like end of Maintenance Support and Extended Life Phase."
    ```
    **Expected `c` Response:** `c` should provide a summary of the RHEL 7 lifecycle, specifically for RHEL 7.9 if possible, detailing its various support phases (e.g., Full Support, Maintenance Support 1, Maintenance Support 2, Extended Life Phase, End of Life). It should cite official Red Hat documentation or a knowledge base article as its source and include relevant dates. For example, it might state that RHEL 7.9 is in Maintenance Support 2 until a certain date, followed by an Extended Life Phase, and finally End of Life.

2.  **Follow-up question (optional):** You might ask `c` about a specific component's lifecycle if it were relevant (e.g., "What is the support status for the Python 3.6 package on RHEL 7?").

#### Resolution
Based on the information provided by `c`, you can now make informed decisions regarding your RHEL 7.9 system, such as:
-   Planning an upgrade path to a newer, fully supported RHEL version.
-   Assessing the need for Extended Life Cycle Support add-ons.
-   Understanding the security implications of running a system in its Extended Life Phase or beyond.

#### Cleanup
Run the cleanup script.
```bash
bash cleanup.sh
```
The cleanup script will confirm that no actions were necessary as no system changes were made by the setup script.
