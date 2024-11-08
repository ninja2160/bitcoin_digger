from bitcoin import *
import hashlib

# Target Bitcoin address you want to match
target_address = "1FjMR9gvnmZ3JYMxBbyc3aZK717b5txJoC"

# Starting 256-bit value (must be within the Bitcoin private key range)
initial_value = int('fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140', 16)
private_key_int = initial_value

# Function to convert integer to WIF (compressed and uncompressed) and derive the Bitcoin address
def get_wif_and_address(private_key_int):
    # Convert the integer to a 256-bit hexadecimal string
    private_key_hex = format(private_key_int, '064x')
    
    # Encode the private key as WIF (uncompressed)
    private_key_wif_u = encode_privkey(private_key_hex, 'wif')

    # Encode the private key as WIF (compressed)
    private_key_wif_c = encode_privkey(private_key_hex, 'wif_compressed')
    
    # Get the public key (uncompressed and compressed)
    public_key_uncompressed = privtopub(private_key_wif_u)
    public_key_compressed = privtopub(private_key_wif_c)
    
    # Generate Bitcoin addresses from the public keys
    address_uncompressed = pubtoaddr(public_key_uncompressed)
    address_compressed = pubtoaddr(public_key_compressed)
    
    return private_key_wif_u, private_key_wif_c, address_uncompressed, address_compressed


[private_key_wif_u, private_key_wif_c, address_uncompressed, address_compressed] = get_wif_and_address(private_key_int)

print(type(initial_value))
print("-1->>", private_key_wif_u)
print("-2->>", private_key_wif_c)

# while True:
#     private_key_wif_u, private_key_wif_c, address_uncompressed, address_compressed = get_wif_and_address(private_key_int)

#     if address_uncompressed == target_address:
#         print(f"Private Key Found (Uncompressed): {private_key_wif_u}")
#         break
#     elif address_compressed == target_address:
#         print(f"Private Key Found (Compressed): {private_key_wif_c}")
#         break
    
#     private_key_int += 1

#     if private_key_int > initial_value + 1000000:
#         print("Limit reached without finding the address.")
#         break
