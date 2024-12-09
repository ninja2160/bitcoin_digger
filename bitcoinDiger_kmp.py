import multiprocessing
from bitcoin import *
import random
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Color variable settings
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

attempts = multiprocessing.Value('i', 0)  # Shared integer for attempts
found = multiprocessing.Value('b', False)  # Shared boolean for key found
num_processes = 7

m = 20  # Partition size (adjustable)
S = [random.randint(1, 2**m) for _ in range(2**m)]
S = list(set(S))  # Ensure unique step sizes
T = len(S)

def jump_size(x):
    return S[x % T]

def private_key_to_wif_c(private_key_int):
    private_key_hex = format(private_key_int, '064x')
    wif_c = encode_privkey(private_key_hex, 'wif_compressed')
    return wif_c

def kangaroo_brute_force(thread_id, start_private_key, end_private_key, attempts, found):
    tame_private_key = start_private_key
    wild_private_key = random.randint(start_private_key, end_private_key)

    print(f"{GREEN}=================== Start Brute-Force (Thread {thread_id}) ====================={RESET}")
    filename = f"thread-{thread_id}.txt"
    with open(filename, "a") as f:
        while not found.value:
            tame_jump = jump_size(tame_private_key)
            tame_private_key = (tame_private_key + tame_jump) % end_private_key
            tame_wif = private_key_to_wif_c(tame_private_key)
            tame_public_key = privtopub(tame_wif)
            tame_btc_address = pubtoaddr(tame_public_key)

            wild_jump = jump_size(wild_private_key)
            wild_private_key = (wild_private_key + wild_jump) % end_private_key
            wild_wif = private_key_to_wif_c(wild_private_key)
            wild_public_key = privtopub(wild_wif)
            wild_btc_address = pubtoaddr(wild_public_key)

            with attempts.get_lock():
                attempts.value += 1
            if attempts.value % 1000 == 0 and thread_id == 0:
                print(f"{GREEN}Attempts: {attempts.value} | Tame Key: {tame_private_key} | Wild Key: {wild_private_key}{RESET}")

            if tame_btc_address == target_address:
                found.value = True
                print(f"{RED}Private Key Found (Tame): {tame_wif}{RESET}")
                f.write(f"Private Key Found (Tame): {tame_wif}\n")
                return tame_wif
            if wild_btc_address == target_address:
                found.value = True
                print(f"{RED}Private Key Found (Wild): {wild_wif}{RESET}")
                f.write(f"Private Key Found (Wild): {wild_wif}\n")
                return wild_wif

    print(f"{RED}Thread {thread_id} completed. No key found.{RESET}")
    return None

def main():
    hex_start_private_key = "40000000000000000"
    hex_end_private_key =   "7ffffffffffffffff"

    start_private_key = int(hex_start_private_key, 16)
    end_private_key = int(hex_end_private_key, 16)

    range_size = (end_private_key - start_private_key + 1) // num_processes
    processes = []

    for i in range(num_processes):
        process_start = start_private_key + i * range_size
        process_end = start_private_key + (i + 1) * range_size - 1 if i < num_processes - 1 else end_private_key
        process = multiprocessing.Process(target=kangaroo_brute_force, args=(i, process_start, process_end, attempts, found))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()
