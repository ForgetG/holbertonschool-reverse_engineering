#!/bin/bash

display_elf_header_info() {
    echo "Header Information for '${file_name}':"
    echo "--------------------------------"
    echo "Magic Number: ${magic_number}"
    echo "Class: ${class}"
    echo "Byte Order: ${byte_order}"
    echo "Entry Point Address: ${entry_point_address}"
}

display_usage() {
    echo "Usage: $0 <ELF_file>" >&2
}

display_file_not_found_error() {
    echo "Error: File '${file_name}' does not exist or is not a regular file." >&2
}

display_invalid_elf_error() {
    echo "Error: File '${file_name}' is not a valid ELF binary." >&2
}

display_read_error() {
    echo "Error: Unable to read ELF header information from '${file_name}'." >&2
}
