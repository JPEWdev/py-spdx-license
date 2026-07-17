#
# Copyright Joshua Watt <JPEWhacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#

import subprocess
from pathlib import Path

TOP_DIR = Path(__file__).parent.parent


def test_black():
    subprocess.run(["black", "--check", "."], check=True, cwd=TOP_DIR)


def test_flake8():
    files = subprocess.run(
        ["git", "ls-files", "*.py"],
        check=True,
        cwd=TOP_DIR,
        encoding="utf-8",
        stdout=subprocess.PIPE,
    ).stdout.splitlines()

    subprocess.run(["flake8"] + files, check=True, cwd=TOP_DIR)
