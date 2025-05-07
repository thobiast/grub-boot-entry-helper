#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to display GRUB menu entry IDs and name.

Useful for obtaining values for grub-set-default and grub-reboot commands.

- It supports GRUB2 configuration format
- It support submenu items

For Red Hat-based distributions, consider using the 'grubby' package instead.
"""

import argparse
import re

menuentry_re = re.compile(r"^\s*menuentry\s+(['\"])((?:(?!\1).)*?)\1")
submenu_re = re.compile(r"^\s*submenu\s+(['\"])((?:(?!\1).)*?)\1")


def parse_parameters():
    """Parse command-line parameters."""
    parser = argparse.ArgumentParser(
        description="Show GRUB menu entry id and name.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to GRUB configuration file",
        default="/boot/grub/grub.cfg",
        dest="grub_cfg_file",
    )

    return parser.parse_args()


def read_grub_cfg_file(filename):
    """
    Reads and filters non-empty, non-comment lines from a GRUB configuration file.

    Returns:
        list[str]: List of filtered lines from the file.
    """
    try:
        with open(filename, "r") as file:
            # Strip lines and ignore empty lines and comments
            lines = [
                line.strip() for line in file if line.strip() and not line.startswith("#")
            ]
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        exit(1)
    return lines


def parse_grub_cfg(lines):
    """
    Parse the GRUB config files for menu entries and submenu items.

    Args:
        lines (list[str]): The list of strings that contains the GRUB conf file
    """
    brace_count = 0
    menu_entry_index = 0
    submenu_entry_index = 0
    submenu_entry_title = None

    for line in lines:
        menuentry_match = menuentry_re.match(line)
        submenu_match = submenu_re.match(line)
        if menuentry_match:
            brace_count += 1
            # If inside a submenu, print using submenu context (indices and title)
            if submenu_entry_title:
                print(
                    f"{menu_entry_index}>{submenu_entry_index}\t{submenu_entry_title}>{menuentry_match.group(2)}"
                )
                submenu_entry_index += 1
            # Top-level menu entry
            else:
                print(f"{menu_entry_index}\t{menuentry_match.group(2)}")
        if submenu_match:
            # Start a new submenu block
            brace_count += 1
            submenu_entry_title = submenu_match.group(2)

        if line.startswith("}") and brace_count > 0:
            brace_count -= 1
            # When a block (submenu or menu) ends, if brace_count is 0, it ends the current
            # top-level entry. That way, increase menu_entry_index and reset submenu info
            # for the next loop
            if brace_count == 0:
                menu_entry_index += 1
                submenu_entry_title = None
                submenu_entry_index = 0


##############################################################################
# Main
##############################################################################
def main():
    args = parse_parameters()

    lines = read_grub_cfg_file(args.grub_cfg_file)
    parse_grub_cfg(lines)


##############################################################################
# Run from command line
##############################################################################
if __name__ == "__main__":
    main()

# vim: ts=4
