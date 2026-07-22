#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

export LC_ALL=C

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
messages_file="${script_directory}/messages.sh"

if [[ ! -r "$messages_file" ]]; then
    echo "Error: unable to read '${messages_file}'." >&2
    exit 1
fi

source "$messages_file"

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <ELF_file>" >&2
    exit 1
fi

file_name="$1"

if [[ ! -f "$file_name" ]]; then
    echo "Error: file '$file_name' does not exist." >&2
    exit 1
fi

if [[ ! -r "$file_name" ]]; then
    echo "Error: file '$file_name' is not readable." >&2
    exit 1
fi

if ! elf_header="$(readelf --file-header --wide "$file_name" 2>/dev/null)"; then
    echo "Error: file '$file_name' is not a valid ELF file." >&2
    exit 1
fi

magic_number="$(
    printf '%s\n' "$elf_header" |
    sed -n 's/^[[:space:]]*Magic:[[:space:]]*//p' |
    head -n 1
)"

class="$(
    printf '%s\n' "$elf_header" |
    sed -n 's/^[[:space:]]*Class:[[:space:]]*//p' |
    head -n 1
)"

byte_order="$(
    printf '%s\n' "$elf_header" |
    sed -n 's/^[[:space:]]*Data:[[:space:]]*//p' |
    sed "s/^2's complement,[[:space:]]*//" |
    head -n 1
)"

entry_point_address="$(
    printf '%s\n' "$elf_header" |
    sed -n 's/^[[:space:]]*Entry point address:[[:space:]]*//p' |
    head -n 1
)"

if [[ -z "$magic_number" || -z "$class" || -z "$byte_order" || -z "$entry_point_address" ]]; then
    echo "Error: unable to extract all required ELF header fields from '$file_name'." >&2
    exit 1
fi

display_elf_header_info
