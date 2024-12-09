import threading
from bitcoin import *
import random

# The Bitcoin address we are hypothetically trying to brute-force
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
# Flag indicating whether the private key has been found
found = False
# Number of threads to use
num_threads = 4
# Range for private keys
start_private_key = 73786976294838206464
end_private_key = 147573952589676412927

print(f"===================Start=====================")

def private_key_to_wif_c(private_key_int):
    # Convert the private key to WIF
    private_key_hex = format(private_key_int, '064x')
    wif_c = encode_privkey(private_key_hex, 'wif_compressed')
    return wif_c

def kangaroo_worker(thread_id, start_key, end_key):
    global found
    # Initialize tame kangaroo
    tame_kangaroo = start_key
    file_name = f"Thread-{thread_id}.txt"

    with open(file_name, "a") as f:
        while tame_kangaroo <= end_key and not found:
            # Tame kangaroo jumps forward
            jump_size = random.randint(1, 10)  # Fixed jump size of 1 to 10
            tame_kangaroo += jump_size

            if tame_kangaroo > end_key:
                break  # Stop if out of range
            # Convert private key to WIF and Bitcoin address
            tame_wif = private_key_to_wif_c(tame_kangaroo)
            tame_address = pubtoaddr(privtopub(tame_wif))
            # Log progress
            f.write(f"{tame_kangaroo}: {tame_wif}\n")
            # Check if tame kangaroo matches the target address
            if tame_address == target_address:
                found = True
                print(f"===================Success!=====================")
                print(f"Thread-{thread_id}: Private Key Found: {tame_wif}")
                f.write(f"Thread-{thread_id}: Private Key Found: {tame_wif}\n")
                return

# Divide range among threads
range_size = (end_private_key - start_private_key + 1) // num_threads
threads = []
# Start the threads, dividing the range of private keys among them
for i in range(num_threads):
    thread_start = start_private_key + i * range_size
    thread_end = thread_start + range_size - 1
    # Ensure the last thread covers the entire remaining range
    if i == num_threads - 1:
        thread_end = end_private_key
    thread = threading.Thread(target=kangaroo_worker, args=(i, thread_start, thread_end))
    threads.append(thread)
    thread.start()
# Join threads to ensure all complete before finishing
for thread in threads:
    thread.join()
print("Kangaroo search completed.")