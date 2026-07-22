#!/bin/bash

display_elf_header_info() {
    echo "Header Information for '${file_name}':"
    echo "--------------------------------"
    echo "Magic Number: ${magic_number}"
    echo "Class: ${class}"
    echo "Byte Order: ${byte_order}"
    echo "Entry Point Address: ${entry_point_address}"
}
