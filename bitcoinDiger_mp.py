from multiprocessing import Process
from bitcoin import *
import random
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
num_processes = 4
start_value = 73786976294838206464
end_value =  147573952589676412927
smaller_range_size = 3000000

def private_key_to_wif_c(private_key_int):
    private_key_hex = format(private_key_int, '064x')
    wif_c = encode_privkey(private_key_hex, 'wif_compressed')
    return wif_c

def brute_force_worker(thread_id, start_private_key, end_private_key):
    current_private_key = start_private_key
    file_name = f"Thread-{thread_id}.txt"

    with open(file_name, "w") as f:
        while current_private_key <= end_private_key:
            wif_c_key = private_key_to_wif_c(current_private_key)
            private_key = format(current_private_key, '064x')
            public_key = privtopub(wif_c_key)
            btc_address = pubtoaddr(public_key)

            print(f"{GREEN}>> {private_key}{RESET}")
            if btc_address == target_address:
                print(f"{RED}===================Success!====================={RESET}")
                print(f"{RED}Thread-{thread_id}: Private Key Found: {wif_c_key}{RESET}")
                f.write(f"Thread-{thread_id}: Private Key Found: {wif_c_key}\n")
                break

            if (current_private_key - start_private_key) % 1000 == 0:
                print(f"{GREEN}Attempts: {current_private_key - start_private_key} (Thread-{thread_id}){RESET}")

            current_private_key += 1

def main():
    start_private_key = random.randint(start_value, end_value - smaller_range_size)
    end_private_key = start_private_key + smaller_range_size

    print(f"{GREEN}===================Start====================={RESET}")
    print(f"{RED}start value : {start_private_key} {RESET}")
    print(f"{RED}end value : {end_private_key} {RESET}")
    print(f"{GREEN}==========================================={RESET}")
    range_size = (end_private_key - start_private_key + 1) // num_processes
    processes = []

    for i in range(num_processes):
        process_start = start_private_key + i * range_size
        process_end = start_private_key + (i + 1) * range_size - 1 if i < num_processes - 1 else end_private_key
        process = Process(target=brute_force_worker, args=(i, process_start, process_end))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    
    print(f"{GREEN}Brute force attempt completed.{RESET}")

if __name__ == "__main__":
    main()