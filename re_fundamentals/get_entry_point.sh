#!/bin/bash

# Exit immediately on unhandled errors and undefined variables.
set -u

# Resolve the directory containing this script so that messages.sh can be
# loaded without using a hardcoded absolute path.
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# Import the reusable output functions.
# shellcheck source=messages.sh
source "${script_dir}/messages.sh"

# Require exactly one command-line argument.
if [[ $# -ne 1 ]]; then
    display_usage
    exit 1
fi

file_name="$1"

# Confirm that the supplied path refers to an existing regular file.
if [[ ! -f "$file_name" ]]; then
    display_file_not_found_error
    exit 1
fi

# Confirm that the current user can read the file.
if [[ ! -r "$file_name" ]]; then
    echo "Error: File '${file_name}' is not readable." >&2
    exit 1
fi

# readelf returns a non-zero status when the file is not a valid ELF file.
# LC_ALL=C keeps the output predictable regardless of the system language.
if ! elf_header="$(LC_ALL=C readelf -h -- "$file_name" 2>/dev/null)"; then
    display_invalid_elf_error
    exit 1
fi

# Extract the ELF magic bytes from the readelf header.
magic_number="$(
    printf '%s\n' "$elf_header" |
        awk -F: '/^[[:space:]]*Magic:/ {
            sub(/^[[:space:]]+/, "", $2)
            print $2
            exit
        }'
)"

# Extract whether the binary uses the ELF32 or ELF64 format.
class="$(
    printf '%s\n' "$elf_header" |
        awk -F: '/^[[:space:]]*Class:/ {
            sub(/^[[:space:]]+/, "", $2)
            print $2
            exit
        }'
)"

# The Data field describes both the encoding and byte order.
byte_order="$(
    printf '%s\n' "$elf_header" |
        awk -F: '/^[[:space:]]*Data:/ {
            sub(/^[[:space:]]+/, "", $2)
            print $2
            exit
        }'
)"

# Extract the virtual address at which execution begins.
entry_point_address="$(
    printf '%s\n' "$elf_header" |
        awk -F: '/^[[:space:]]*Entry point address:/ {
            sub(/^[[:space:]]+/, "", $2)
            print $2
            exit
        }'
)"

# Ensure all required ELF fields were successfully extracted.
if [[ -z "$magic_number" ||
      -z "$class" ||
      -z "$byte_order" ||
      -z "$entry_point_address" ]]; then
    display_read_error
    exit 1
fi

display_elf_header_info
