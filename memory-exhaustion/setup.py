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
