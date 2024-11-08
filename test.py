# import threading
from bitcoin import *
import time

# The Bitcoin address we are hypothetically trying to brute-force
target_address = "1PTXoboEq4EBU6inmrgK92pzCWZGc78yb8"

# Counter for attempts (shared among threads)
# attempts = 0
found = False

# def brute_force_worker(thread_id):
# global attempts, found
while not found:
    # Generate a random private key
    # private_key = random_key()
    private_key = "L4P2WgVwTaqCKUkcQvGxbNFaWcJPzQCFk2oPNMeq59z9WS7sZ9Uo"
    # Get the public key from the private key
    public_key = privtopub(private_key)
    
    # Generate the Bitcoin address from the public key
    btc_address = pubtoaddr(public_key)
    
    # Check if the generated address matches the target address
    if btc_address == target_address:
        found = True
        print(f"Private Key Found: {private_key}")
        break
    
    # Update the attempt counter
    # attempts += 1
    # if attempts % 100000 == 0 and thread_id == 0:
    #     print(f"Attempts: {attempts} (Thread-{thread_id})")

# Number of threads to use
# num_threads = 4

# List to hold our threads
# threads = []

# # Start the threads
# for i in range(num_threads):
#     thread = threading.Thread(target=brute_force_worker, args=(i,))
#     threads.append(thread)
#     thread.start()

# # Join threads to ensure all complete before finishing
# for thread in threads:
#     thread.join()

# print("Brute force attempt completed.")
