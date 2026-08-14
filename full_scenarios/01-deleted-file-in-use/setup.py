import time
import os

file_name = "large_file.tmp"
file_size_mb = 500

print(f"Creating a {file_size_mb}MB file named '{file_name}'...")

# Create a large file
with open(file_name, "wb") as f:
    f.write(b'\0' * file_size_mb * 1024 * 1024)

print("File created. Opening and then deleting it...")

# Open the file and keep the handle
file_handle = open(file_name, 'r')

# Delete the file from the filesystem
os.remove(file_name)

print(f"File '{file_name}' has been deleted, but the script is holding it open.")
print("Check 'df -h' and 'du -sh .' now.")
print("The script will keep the file open for 5 minutes.")

time.sleep(300)

print("Closing file handle and exiting. The space should now be freed.")
file_handle.close()