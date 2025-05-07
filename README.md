## GRUB Boot Entry Helper

A simple Python script that parses GRUB2 configuration files to list each menu entry’s ID and name,
making it easier to use GRUB commands like `grub-set-default` and `grub-reboot`.

- It supports GRUB2 configuration format
- It support submenu items

For Red Hat-based distributions, consider using the `grubby` package instead.
