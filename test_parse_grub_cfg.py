# -*- coding: utf-8 -*-
import pytest
from grub_boot_entry_helper import parse_grub_cfg


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            [
                "menuentry 'U' {",
                "}",
            ],
            ["0\tU"],
        ),
        (
            [
                'menuentry "Arch Linux" {',
                "}",
            ],
            ["0\tArch Linux"],
        ),
        (
            ["other lines1", "menuentry 'Ubuntu' {", "insmod", "}", "other lines1"],
            ["0\tUbuntu"],
        ),
        (
            [
                "menuentry 'Ubuntu' {",
                "}",
                "menuentry 'kernel2' {",
                "}",
            ],
            ["0\tUbuntu", "1\tkernel2"],
        ),
    ],
)
def test_only_menuentry(capsys, lines, expected):
    """
    Test parse_grub_cfg with a simple GRUB configuration
    that contains only top-level menuentry.
    """
    parse_grub_cfg(lines)
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == expected


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            [
                "submenu 'Advanced options' {",
                "menuentry 'Ubuntu, with Linux 6.8.0-57-generic' {",
                "}",
                "menuentry 'Ubuntu, with Linux 6.8.0-57-generic recovery' {",
                "}",
                "}",  # close submenu
            ],
            [
                "0>0\tAdvanced options>Ubuntu, with Linux 6.8.0-57-generic",
                "0>1\tAdvanced options>Ubuntu, with Linux 6.8.0-57-generic recovery",
            ],
        ),
        (
            [
                "submenu 'Advanced options' {",
                "menuentry 'Ubuntu, with Linux 6.8.0-57-generic' {",
                "}",
                "menuentry 'Ubuntu, with Linux 6.8.0-57-generic recovery' {",
                "}",
                "}",  # close submenu
                "other lines 1",
                "submenu 'Advanced options 2' {",
                "other lines 2",
                "menuentry 'Ubuntu, with Linux xxx' {",
                "other lines 3",
                "}",
                "other lines 4",
                "}",  # close submenu
            ],
            [
                "0>0\tAdvanced options>Ubuntu, with Linux 6.8.0-57-generic",
                "0>1\tAdvanced options>Ubuntu, with Linux 6.8.0-57-generic recovery",
                "1>0\tAdvanced options 2>Ubuntu, with Linux xxx",
            ],
        ),
    ],
)
def test_submenu_entries(capsys, lines, expected):
    """
    Test parse_grub_cfg with a submenu only.
    """
    parse_grub_cfg(lines)
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == expected


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            [
                "menuentry 'Ubuntu' {",
                "}",
                "submenu 'Advanced options' {",
                "menuentry 'Ubuntu, with Linux x.y.z' {",
                "}",
                "menuentry 'Ubuntu, with Linux a.b.c' {",
                "}",
                "}",  # close submenu
                "menuentry 'Arch Linux' {",
                "}",
            ],
            [
                "0\tUbuntu",
                "1>0\tAdvanced options>Ubuntu, with Linux x.y.z",
                "1>1\tAdvanced options>Ubuntu, with Linux a.b.c",
                "2\tArch Linux",
            ],
        ),
        (
            [
                "submenu 'Advanced options' {",
                "menuentry 'Ubuntu, with Linux x.y.z' {",
                "}",
                "menuentry 'Ubuntu, with Linux a.b.c' {",
                "}",
                "}",  # close submenu
                "menuentry 'Arch Linux' {",
                "}",
            ],
            [
                "0>0\tAdvanced options>Ubuntu, with Linux x.y.z",
                "0>1\tAdvanced options>Ubuntu, with Linux a.b.c",
                "1\tArch Linux",
            ],
        ),
    ],
)
def test_mixed_entries(capsys, lines, expected):
    """
    Test parse_grub_cfg with a mixture of top-level menuentry and submenu items.
    """
    parse_grub_cfg(lines)
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == expected


@pytest.mark.parametrize(
    "lines,expected",
    [
        (
            [
                "menuentr 'Ubuntu' {",  # wrong key
                "}",
                "#menuentry 'Ubuntu' {",  # comment
                "}",
                "menuentr 'Ubuntu {",  # missing ' to close the menu entry name
                "}",
                "menuentry'Ubuntu' {",  # no blank space
                "}",
                "x menuentry'Ubuntu' {",  # line starting with other chars
                "}",
                "x submenu'Ubuntu' {",  # line starting with other chars
                "}",
                "submenuu 'Ubuntu' {",  # wrong key
                "}",
            ],
            [],
        ),
    ],
)
def test_ignore_invalid_entry(capsys, lines, expected):
    """
    Test parse_grub_cfg to ensure it only parse submenu and menuentry correct lines.
    """
    parse_grub_cfg(lines)
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == expected
