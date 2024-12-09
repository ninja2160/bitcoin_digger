from bitcoin import *
import random

# The Bitcoin address we are hypothetically trying to brute-force
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

# Counter for attempts
attempts = 0
found = False

# Range for private keys
start_private_key = 137573952589676412927
end_private_key =  147573952589676412927

f = open("wallet_key.txt", "a")
# Pseudo-random jump function
m = 4  # Partition size (adjustable)
S = [random.randint(1, 2**m) for _ in range(2**m)]
S = list(set(S))  # Ensure unique step sizes
T = len(S)


def jump_size(x):
    """Return jump size based on pseudo-random function."""
    return S[x % T]

def private_key_to_wif_c(private_key_int):
    """Convert the private key to WIF."""
    private_key_hex = format(private_key_int, '064x')
    wif_c = encode_privkey(private_key_hex, 'wif_compressed')
    return wif_c

def kangaroo_brute_force(start_private_key, end_private_key):
    """Kangaroo algorithm for brute-forcing a Bitcoin private key."""
    global attempts, found
    tame_private_key = start_private_key
    wild_private_key = random.randint(start_private_key, end_private_key)
    
    print(f"=================== Start Brute-Force =====================")
    
    while not found:
        # Tame Kangaroo Walk
        tame_jump = jump_size(tame_private_key)
        tame_private_key = (tame_private_key + tame_jump) % end_private_key
        tame_wif = private_key_to_wif_c(tame_private_key)
        tame_public_key = privtopub(tame_wif)
        tame_btc_address = pubtoaddr(tame_public_key)
        
        # Wild Kangaroo Walk
        wild_jump = jump_size(wild_private_key)
        wild_private_key = (wild_private_key + wild_jump) % end_private_key
        wild_wif = private_key_to_wif_c(wild_private_key)
        wild_public_key = privtopub(wild_wif)
        wild_btc_address = pubtoaddr(wild_public_key)
        
        # Increment attempts
        attempts += 1
        if attempts % 1000 == 0:
            print(f"Attempts: {attempts} | Tame Key: {tame_private_key} | Wild Key: {wild_private_key}")
        
        # Check if either matches the target address
        if tame_btc_address == target_address:
            found = True
            print(f"Private Key Found (Tame): {tame_wif}")
            return tame_wif
        if wild_btc_address == target_address:
            found = True
            print(f"Private Key Found (Wild): {wild_wif}")
            return wild_wif
    
    print(f"Brute force attempt completed. No key found.")
    return None


def main():
    # Execute the Kangaroo algorithm
    private_key_found = kangaroo_brute_force(start_private_key, end_private_key)

    if private_key_found:
        print(f"Success! Private Key: {private_key_found}")
        f.write(f"Success! Private Key: {private_key_found}")
    else:
        print(f"Failed to find the private key in the given range.")

if __name__=="__main__":
    main()