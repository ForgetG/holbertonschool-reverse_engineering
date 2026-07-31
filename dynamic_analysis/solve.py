#!/usr/bin/env python3

from z3 import (
    BitVec,
    BitVecVal,
    Or,
    SolverFor,
    SignExt,
    SRem,
    URem,
    sat,
)

CHAR_COUNT = 24
WIDTH = 32


def bv32(value: int):
    """Create a 32-bit bit-vector constant."""
    return BitVecVal(value & 0xFFFFFFFF, WIDTH)


# Each unknown flag character is represented by one byte.
chars = [BitVec(f"char_{i}", 8) for i in range(CHAR_COUNT)]

# QF_BV means quantifier-free bit-vector logic.
solver = SolverFor("QF_BV")

# Limit characters to readable ASCII.
for char in chars:
    solver.add(char >= 0x21)
    solver.add(char <= 0x7E)

# Optional, but often useful for CTF flags:
# letters, digits and underscore only.
for char in chars:
    solver.add(
        Or(
            char == ord("_"),
            char >= ord("0"),
            char <= ord("9"),
            char >= ord("A"),
            char <= ord("Z"),
            char >= ord("a"),
            char <= ord("z"),
        )
    )

accumulator_a = bv32(0)
accumulator_b = bv32(1)
accumulator_c = bv32(0)
accumulator_d = bv32(1)

for i, char8 in enumerate(chars):
    # The assembly uses movsx, so the byte is sign-extended.
    character = SignExt(24, char8)
    index = bv32(i)

    # a += ((i + 1) * character * (i + 2)) % 256
    expression_a = (
        (index + bv32(1))
        * character
        * (index + bv32(2))
    )

    accumulator_a = accumulator_a + SRem(
        expression_a,
        bv32(256),
    )

    # b *= (character + 7*i + 31) % 123
    expression_b = (
        character
        + bv32(7) * index
        + bv32(31)
    )

    accumulator_b = accumulator_b * SRem(
        expression_b,
        bv32(123),
    )

    # c += ((i + 1) * character + i*i) % 512
    expression_c = (
        (index + bv32(1)) * character
        + index * index
    )

    accumulator_c = accumulator_c + SRem(
        expression_c,
        bv32(512),
    )

    # d ^= ((i + 3) * character + 17) % 1024
    expression_d = (
        (index + bv32(3)) * character
        + bv32(17)
    )

    accumulator_d = accumulator_d ^ SRem(
        expression_d,
        bv32(1024),
    )


# First combination:
#
# ((a * b + c - d) ^ 0xDEADBEEF) & 0xFFFFFF
temporary = (
    (
        accumulator_a * accumulator_b
        + accumulator_c
        - accumulator_d
    )
    ^ bv32(0xDEADBEEF)
) & bv32(0x00FFFFFF)

# Second combination:
#
# a*b + temporary - c*d
combined = (
    accumulator_a * accumulator_b
    + temporary
    - accumulator_c * accumulator_d
)

# The assembly subtracts 0x35014542.
# In 32-bit arithmetic that is equivalent to adding 0xCAFEBABE.
combined = combined + bv32(0xCAFEBABE)

# The compiler's magic-number sequence calculates unsigned % 987654.
final_value = URem(combined, bv32(987654))

solver.add(final_value == bv32(0xAE44))

print("[*] Solving...")

if solver.check() != sat:
    print("[-] No solution found.")
    raise SystemExit(1)

model = solver.model()

middle = "".join(
    chr(model.eval(char, model_completion=True).as_long())
    for char in chars
)

flag = f"Holberton{{{middle}}}"

print(f"[+] Middle: {middle}")
print(f"[+] Flag:   {flag}")

# Print useful diagnostics.
print("\n[+] Accumulator values:")
print(
    "    A =",
    hex(model.eval(accumulator_a, model_completion=True).as_long()),
)
print(
    "    B =",
    hex(model.eval(accumulator_b, model_completion=True).as_long()),
)
print(
    "    C =",
    hex(model.eval(accumulator_c, model_completion=True).as_long()),
)
print(
    "    D =",
    hex(model.eval(accumulator_d, model_completion=True).as_long()),
)
print(
    "    Final =",
    hex(model.eval(final_value, model_completion=True).as_long()),
)

