
hex_number = "0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140"

# Convert the hexadecimal number to an integer
int_number = int(hex_number, 16)

# Increment the integer by 1
incremented_number = int_number + 1

# Convert the incremented number back to a hexadecimal format
incremented_hex_number = hex(incremented_number)

print(incremented_hex_number)