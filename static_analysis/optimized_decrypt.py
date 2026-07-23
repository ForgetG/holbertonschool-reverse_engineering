encrypted_blocks = [
    0x6F836CB672D9828E,
    0x699A77A760DA96A8,
    0x779872A077DB84BC,
    0x6184778C75D182A5,
    0x5F9070BA69DA83A8,
    0x61A86DBA4FC198A4,
    0x00F763A763C08099,
]

exponent = 0x0000FFFFFFFFFFFF
modulus = 0x0FFFFFFFFFFFFFFB

key = pow(2, exponent, modulus)

plaintext = bytearray()

for encrypted_block in encrypted_blocks:
    decrypted_block = encrypted_block ^ key
    plaintext.extend(decrypted_block.to_bytes(8, "little"))

flag = plaintext.rstrip(b"\x00").decode("ascii")

print(hex(key))
print(flag)

