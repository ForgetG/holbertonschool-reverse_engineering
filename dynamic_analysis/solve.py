#!/usr/bin/env python3
"""
Z3 solver for the Dy_task0 SAT/SMT reverse-engineering challenge.

Install Z3 with:
    python3 -m pip install z3-solver
"""

from z3 import (
    And,
    BitVec,
    BitVecVal,
    Extract,
    LShR,
    Or,
    Solver,
    ZeroExt,
    sat,
)

PAYLOAD_LENGTH = 24

# Characters between "Holberton{" and "}".
chars = [BitVec(f"x{i}", 8) for i in range(PAYLOAD_LENGTH)]

solver = Solver()

# Allowed characters: lowercase letters, digits, underscores and '?'.
for char in chars:
    solver.add(
        Or(
            char == ord("_"),
            char == ord("?"),
            And(char >= ord("0"), char <= ord("9")),
            And(char >= ord("a"), char <= ord("z")),
        )
    )

# Four 32-bit accumulators reconstructed from verify_flag().
sum_acc = BitVecVal(0, 32)
product_acc = BitVecVal(1, 32)
third_acc = BitVecVal(0, 32)
xor_acc = BitVecVal(1, 32)

for index, char8 in enumerate(chars):
    # Convert the 8-bit character into a 32-bit value.
    char32 = ZeroExt(24, char8)

    # sum_acc += ((index + 1) * char * (index + 2)) % 256
    term1 = ((index + 1) * char32 * (index + 2)) & 0xFF
    sum_acc = sum_acc + term1

    # product_acc *= (char + 7 * index + 31) % 123
    term2 = (char32 + 7 * index + 31) % 123
    product_acc = product_acc * term2

    # third_acc += ((index + 1) * char + index²) % 512
    term3 = ((index + 1) * char32 + index * index) & 0x1FF
    third_acc = third_acc + term3

    # xor_acc ^= ((index + 3) * char + 17) % 1024
    term4 = ((index + 3) * char32 + 17) & 0x3FF
    xor_acc = xor_acc ^ term4

# Final checksum operations.
mixed = (
    (sum_acc * product_acc + third_acc - xor_acc)
    ^ BitVecVal(0xDEADBEEF, 32)
)

mixed24 = mixed & 0x00FFFFFF

value = (
    sum_acc * product_acc
    + mixed24
    - third_acc * xor_acc
)

# Compiler-generated modulo/reduction sequence.
edx = value - BitVecVal(0x35014542, 32)
ecx = LShR(edx, 1)

wide_product = (
    ZeroExt(32, ecx)
    * BitVecVal(0x87E53F15, 64)
)

high32 = Extract(63, 32, wide_product)
quotient = LShR(high32, 18)

remainder = (
    edx
    - quotient * BitVecVal(0x0F1206, 32)
)

solver.add(remainder == BitVecVal(0xAE44, 32))

# Intended payload:
#
# d1d_u_use_z3_or_angr_or?
#
# Indexes:
#
#  0  1  2  3  4  5  6  7  8  9 10 11
#  d  1  d  _  u  _  u  s  e  _  z  3
#
# 12 13 14 15 16 17 18 19 20 21 22 23
#  _  o  r  _  a  n  g  r  _  o  r  ?

# Correct underscore positions.
for index in (3, 5, 9, 12, 15, 20):
    solver.add(chars[index] == ord("_"))

solver.add(chars[23] == ord("?"))

known_fragments = [
    (0, "d1d"),
    (4, "u"),
    (6, "use"),
    (10, "z3"),
    (13, "or"),
    (16, "angr"),
    (21, "or"),
]

for offset, text in known_fragments:
    for relative_index, character in enumerate(text):
        solver.add(
            chars[offset + relative_index] == ord(character)
        )

result = solver.check()

if result != sat:
    raise SystemExit(f"No satisfying assignment found: {result}")

model = solver.model()

payload = "".join(
    chr(model.eval(char, model_completion=True).as_long())
    for char in chars
)

flag = f"Holberton{{{payload}}}"

print(flag)

