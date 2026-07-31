#!/usr/bin/env python3
from itertools import product

PRINTABLE = range(32, 127)


def c_rem(value: int, divisor: int) -> int:
    """C-style signed remainder: division truncates toward zero."""
    return value - int(value / divisor) * divisor


def func_one(a, b, c):
    return 1003 * a * b + 13 * c + a * c - 100


def func_two(a, b, c):
    return a * c - 1337 + 101 * b - (a + b + 137) + a * b - 17381


def func_three(a, b, c):
    return a * b + c_rem(b, 19)


def func_four(a, b, c):
    return a * b * c - b * c


def func_five(a, b, c):
    return c_rem(a + b * c, 10000)


def func_six(a, b, c):
    return a * b + c - b * c


def func_seven(a, b, c):
    return a * b + c * c - c


def func_eight(a, b, c):
    return a * b * c - b * c


def func_nine(a, b, c):
    return a * b - c * b + a - 100


def func_ten(a, b, c):
    return (a + b) * c - 10000 + b


def func_eleven(a, b, c):
    return a * b * c - 1337 + a * b


def func_twelve(a, b, c):
    return a * c + 10 * b - a + 137


def func_thirteen(a, b, c):
    return c_rem(a * b * c, 10000) - 500


def func_fourteen(a, b, c):
    return a * b * c - a * b + c


def func_fifteen(a, b, c):
    return 1337 * (a + b + c) - c


def func_sixteen(a, b, c):
    return a * b + 10 * c - a * c + 500


def func_seventeen(a, b, c):
    return a * b - c * b + 101 * c


def func_eighteen(a, b, c):
    return a * b * c - b * c + 137 * a


def func_nineteen(a, b, c):
    return a + b + 137 * c - b * c


def func_twenty(a, b, c):
    return a * b + c * c - a * c


FUNCTIONS = [
    func_one, func_two, func_three, func_four, func_five,
    func_six, func_seven, func_eight, func_nine, func_ten,
    func_eleven, func_twelve, func_thirteen, func_fourteen,
    func_fifteen, func_sixteen, func_seventeen, func_eighteen,
    func_nineteen, func_twenty,
]

TARGETS_FIRST_BLOCK = [
    0x7A73E0, 0x396C, 0x295B, 0x110ABA, 0xCFD,
    0x1CB, 0x6122, 0x16B5AC, 0x5CE, 0x2D0F,
    0x10CE2F, 0x2C6F, 0x133D, 0xEE949, 0x64D5A,
    0xC6C, 0x2D63, 0x105869, 0x13B1, 0x319D,
]

TARGETS_SECOND_BLOCK = [
    0xC33BD5, 0x4201, 0x2D2D, 0x104645, 0xCA6, -865
]


def extend_sequences(sequences, function, target):
    results = []

    for sequence in sequences:
        a, b = sequence[-2:]

        for c in PRINTABLE:
            if function(a, b, c) == target:
                results.append(sequence + [c])

    return results


def solve_first_block():
    # main explicitly requires flag[0] == 'H'.
    sequences = []

    for b in PRINTABLE:
        for c in PRINTABLE:
            if func_one(ord("H"), b, c) == TARGETS_FIRST_BLOCK[0]:
                sequences.append([ord("H"), b, c])

    for index in range(1, len(TARGETS_FIRST_BLOCK)):
        sequences = extend_sequences(
            sequences,
            FUNCTIONS[index],
            TARGETS_FIRST_BLOCK[index],
        )

    return sequences


def solve_second_block():
    sequences = []

    for a, b, c in product(PRINTABLE, repeat=3):
        if func_one(a, b, c) == TARGETS_SECOND_BLOCK[0]:
            sequences.append([a, b, c])

    for index in range(1, len(TARGETS_SECOND_BLOCK)):
        sequences = extend_sequences(
            sequences,
            FUNCTIONS[index],
            TARGETS_SECOND_BLOCK[index],
        )

    return sequences


def main():
    first = solve_first_block()
    second = solve_second_block()

    if len(first) != 1 or len(second) != 1:
        raise RuntimeError(
            f"Expected one solution per block, got {len(first)} and {len(second)}"
        )

    flag = bytes(first[0] + second[0]).decode("ascii")
    print(flag)


if __name__ == "__main__":
    main()
