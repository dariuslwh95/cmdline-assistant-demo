# Scenario 02: I/O Error on a Block Device

This scenario simulates a failing storage device using `dmsetup` to create a virtual block device that forces I/O errors.

## 1. Setup Guide
This setup creates a virtual device `/dev/mapper/error-device` that returns I/O errors.
Run the setup script with root privileges:
```bash
sudo 02-io-error/setup.sh
```

## 2. Diagnose & Analyze

Trigger an I/O error to generate system logs:
```bash
sudo dd if=/dev/mapper/error-device of=/dev/null bs=1M count=10
```

1. Check for I/O errors in system logs:
   ```bash
   sudo dmesg | tail -n 20
   ```

2. Analyze these logs by piping directly to `c`:
   ```bash
   sudo dmesg | tail -n 20 | c "Analyze these logs for I/O errors and suggest troubleshooting steps for a potential failing device."
   ```

Alternatively, use `-w` after running the command:
   ```bash
   sudo dmesg | tail -n 20
   c "Check the latest dmesg output for storage errors." -w 1
   ```

## 3. Cleanup

Remove the virtual devices when finished:
```bash
sudo 02-io-error/cleanup.sh
```
