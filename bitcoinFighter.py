import threading
from bitcoin import *
import time

# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"  # Reset to default color

# The Bitcoin address we are hypothetically trying to brute-force
target_address = "1Dg5eLjUu8tp5Rhkq1iG9XNPoryrPLQA15"

# Counter for attempts (shared among threads)
attempts = 0
found = False
print(f"{GREEN}===================Start====================={RESET}")

def private_key_to_wif(private_key):
    # Convert the private key to WIF
    wif = encode_privkey(private_key, 'wif')
    return wif

def brute_force_worker(thread_id):
    global attempts, found
    while not found:
        # Generate a random private key
        private_key = random_key()
        
        # Get the public key from the private key
        public_key = privtopub(private_key)
        wif_key = private_key_to_wif(private_key)
        # Generate the Bitcoin address from the public key
        btc_address = pubtoaddr(public_key)
        print(f"{GREEN}>>{private_key}{RESET}")
        print(f"{GREEN}>>{wif_key}{RESET}")
        # Check if the generated address matches the target address
        if btc_address == target_address:
            found = True
            print(f"{RED}===================Start====================={RESET}")
            print(f"Thread-{thread_id}: Private Key Found: {private_key}")
            print(f"================={wif_key}")
            break
        
        # Update the attempt counter
        attempts += 1
        if attempts % 100000 == 0 and thread_id == 0:
            print(f"Attempts: {attempts} (Thread-{thread_id})")

# Number of threads to use
num_threads = 5

# List to hold our threads
threads = []

# Start the threads
for i in range(num_threads):
    thread = threading.Thread(target=brute_force_worker, args=(i,))
    threads.append(thread)
    thread.start()

# Join threads to ensure all complete before finishing
for thread in threads:
    thread.join()

print("Brute force attempt completed.")
