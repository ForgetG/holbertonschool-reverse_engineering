#!/usr/bin/env python3

encrypted = bytes.fromhex(
    "49 00 ed eb 78 a3 f0 4e "
    "4a 99 13 50 f8 56 96 45 "
    "85 15 e9 60 aa f8 ab 0d "
    "68 28 d3 73 68 30 48 ce "
    "6d 8d d0 29 7a a5 23 73 "
    "d8 56 ea e1 5f 60 5a"
)


def prng(state: int) -> tuple[int, int]:
    state = (state * 0x41C64E6D + 0x3039) & 0x7FFFFFFF
    key = (state >> 16) & 0xFF
    return state, key


def ror8(value: int, amount: int) -> int:
    amount %= 8
    return ((value >> amount) | (value << (8 - amount))) & 0xFF


state = 0x3039
plaintext = bytearray()

for encrypted_byte in encrypted:
    state, key = prng(state)

    value = (encrypted_byte + 0x5B) & 0xFF
    value = ror8(value, 3)
    value ^= key

    plaintext.append(value)

print(plaintext.decode())
