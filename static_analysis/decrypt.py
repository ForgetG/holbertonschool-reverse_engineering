encrypted_hex = (
    "9E89846A786585866A977D797C8463807C7F6B67848BAB907B"
    "698370896B997C797C8D6C6F7E81AE866AB36D7B7F669D7E"
    "6A7F96678F9382898263B474"
)

key = b"mysecretkey"
encrypted = bytes.fromhex(encrypted_hex)

plaintext = bytearray()

for i, encrypted_byte in enumerate(encrypted):
    current_key = key[i % len(key)]
    next_key = key[(i + 1) % len(key)]

    decrypted_byte = ((encrypted_byte - next_key) & 0xFF) ^ current_key
    plaintext.append(decrypted_byte)

print(plaintext.decode())

