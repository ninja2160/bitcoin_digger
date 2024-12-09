import threading
from bitcoin import *
import time
import random

#color variable settting
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
#used only thread
#  
# The Bitcoin address we are hypothetically trying to brute-force
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
# Counter for attempts (shared among threads)
attempts = 0
found = False
# Number of threads to use
num_threads = 4
# Original range start and end values
start_value = 137573952589676412927
end_value = 147573952589676412927
# Define the smaller range size
smaller_range_size = 1000000
# Generate a random start point for the smaller range within the main range
start_private_key = random.randint(start_value, end_value - smaller_range_size)
# Define the end point of the smaller range
end_private_key = start_private_key + smaller_range_size

print(f"{GREEN}===================Start====================={RESET}")

def private_key_to_wif_c(private_key_int):
    # Convert the private key to WIF
    private_key_hex = format(private_key_int, '064x')
    wif_c = encode_privkey(private_key_hex, 'wif_compressed')
    return wif_c

def brute_force_worker(thread_id, start_private_key, end_private_key):
    global attempts, found
    current_private_key = start_private_key
    fileName = "Thread-{}.txt"
    f = open(fileName.format(thread_id), "w")
    
    while current_private_key <= end_private_key and not found:
        # Get the public key from the private key

        # Convert the integer to a 256-bit hexadecimal string
        wif_c_key = private_key_to_wif_c(current_private_key)
        private_key = format(current_private_key, '064x')
        public_key = privtopub(wif_c_key)
        # Generate the Bitcoin address from the public key
        btc_address = pubtoaddr(public_key)
        # print(f"{GREEN}>> {wif_c_key}{RESET}")
        # Check if the generated address matches the target address
        # write private key in file
        print(f"{GREEN}>>{private_key}{RESET}")
        # data = "{}\n"
        # f.write(data.format(private_key))
        if btc_address == target_address:
            found = True
            print(f"{RED}===================Success!====================={RESET}")
            print(f"{RED}Thread-{thread_id}: Private Key Found: {wif_c_key}{RESET}")
            data = "Thread-{}: Private Key Found: {}"
            f.write(data.format(thread_id, wif_c_key))
            break
        # Update the attempt counter
        attempts += 1
        if attempts % 1000 == 0 and thread_id == 0:
            print(f"{GREEN}Attempts: {attempts} (Thread-{thread_id}){RESET}")
        current_private_key += 1
    f.close()

def main():
    range_size = (end_private_key - start_private_key + 1) // num_threads
    # List to hold our threads
    threads = []

    # Start the threads, dividing the range of private keys among them
    for i in range(num_threads):
        thread_start = start_private_key + i * range_size
        # Ensure the last thread covers the remaining range
        thread_end = start_private_key + (i + 1) * range_size - 1 if i < num_threads - 1 else end_private_key
        thread = threading.Thread(target=brute_force_worker, args=(i, thread_start, thread_end))
        threads.append(thread)
        thread.start()

    # Join threads to ensure all complete before finishing
    for thread in threads:
        thread.join()

    print("Brute force attempt completed.")

if __name__=="__main__":
    main()