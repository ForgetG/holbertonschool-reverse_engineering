#!/usr/bin/env python3

KEY = b"kjkjf_ckzj9274jdlfdvn-dpakkk__AhfNNtdsp592"

EXPECTED_TRANSFORMED = bytes.fromhex(
    "23 05 07 08 "
    "03 2d 17 04 "
    "14 11 4e 5a "
    "56 40 35 05 "
    "0e 09 11 02 "
    "31 4c 3b 03 "
    "04 07 0d 34 "
    "32 30 25 11 "
    "00 27 20 13 "
    "3b 03 02 5a "
    "5e 4f"
)

flag = bytes(
    value ^ KEY[index % len(KEY)]
    for index, value in enumerate(EXPECTED_TRANSFORMED)
)

print(flag.decode("ascii"))
