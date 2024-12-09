# import threading
from bitcoin import *
import time

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

# The Bitcoin address we are hypothetically trying to brute-force
target_address = "19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA"

# Counter for attempts (shared among threads)
# attempts = 0
found = False

def private_key_to_wif_c(private_key_hex):
    # Convert the private key to WIF
    # private_key_hex = format(private_key_int, '064x')
    wif_c = encode_privkey(private_key_hex, 'wif_compressed')
    return wif_c
current_private_key = 0x0000000000000000000000000000000000000000000000000000000000000013
wif_c_key = private_key_to_wif_c(current_private_key)
public_key = privtopub(wif_c_key)
btc_address = pubtoaddr(public_key)
print(wif_c_key)
print(btc_address)
# while not found:
#     # Generate a random private key
#     # private_key = random_key()
#     private_key = "KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFU76rnZwVdz"
#     # Get the public key from the private key
#     public_key = privtopub(private_key)
    
#     # Generate the Bitcoin address from the public key
#     btc_address = pubtoaddr(public_key)
#     print(btc_address)
#     # Check if the generated address matches the target address
#     if btc_address == target_address:
#         found = True
#         print(f"Private Key Found: {private_key}")
#         break
    
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
