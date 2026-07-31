#!/usr/bin/env python3
"""
Recover one character from each binary_000 ... binary_099 by parsing
the relevant instructions in objdump's Intel-syntax output.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


LOCAL_CONSTANT_RE = re.compile(
    r"mov\s+DWORD PTR \[rbp-[^\]]+\],0x([0-9a-f]+)"
)
COMPARISON_RE = re.compile(r"cmp\s+eax,0x([0-9a-f]+)")
DIRECT_SUB_RE = re.compile(
    r"sub\s+eax,DWORD PTR \[rbp-[^\]]+\]"
)
ADD_RE = re.compile(r"add\s+eax,edx")


def signed32(value: int) -> int:
    if value >= 1 << 31:
        return value - (1 << 32)
    return value


def disassemble_main(binary: Path) -> str:
    result = subprocess.run(
        ["objdump", "-d", "-Mintel", str(binary)],
        check=True,
        text=True,
        capture_output=True,
    )

    match = re.search(
        r"<main>:\n(.*?)(?=\n\n)",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise RuntimeError(f"Could not locate main in {binary}")

    return match.group(1)


def recover_character(binary: Path) -> tuple[str, int, int, str]:
    main = disassemble_main(binary)

    constant_match = LOCAL_CONSTANT_RE.search(main)
    comparison_match = COMPARISON_RE.search(main)

    if not constant_match or not comparison_match:
        raise RuntimeError(f"Could not extract constants from {binary}")

    arithmetic_constant = int(constant_match.group(1), 16)
    target = signed32(int(comparison_match.group(1), 16))

    if DIRECT_SUB_RE.search(main):
        # input_character - arithmetic_constant == target
        character_value = target + arithmetic_constant
        operation = "sub"
    elif ADD_RE.search(main):
        # arithmetic_constant + input_character == target
        character_value = target - arithmetic_constant
        operation = "add"
    else:
        raise RuntimeError(f"Unknown arithmetic pattern in {binary}")

    if not 0 <= character_value <= 0x7F:
        raise RuntimeError(
            f"Recovered non-ASCII value {character_value} from {binary}"
        )

    return operation, arithmetic_constant, target, chr(character_value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing binary_000 through binary_099",
    )
    args = parser.parse_args()

    binaries = sorted(
        args.directory.glob("binary_*"),
        key=lambda path: int(path.name.split("_")[1]),
    )

    if len(binaries) != 100:
        raise RuntimeError(f"Expected 100 binaries, found {len(binaries)}")

    flag_characters: list[str] = []

    for binary in binaries:
        operation, constant, target, character = recover_character(binary)
        flag_characters.append(character)

        print(
            f"{binary.name}: "
            f"{operation} constant={constant} target={target} "
            f"-> {character!r}"
        )

    print("\nFLAG:")
    print("".join(flag_characters))


if __name__ == "__main__":
    main()
