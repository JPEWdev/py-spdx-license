#
# Copyright Joshua Watt <JPEWhacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#

import subprocess
import sys

import py_spdx_license


def test_version():
    v = subprocess.run(
        ["py-spdx-license", "--version"],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    ).stdout.strip()

    assert v == py_spdx_license.VERSION


def test_module():
    """
    Test that program can be invoked as a python module
    """
    v = subprocess.run(
        [sys.executable, "-m", "py_spdx_license", "-V"],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    ).stdout.strip()

    assert v == py_spdx_license.VERSION


GOOD_SORT_CASES = [
    (
        "(MIT AND 0BSD) AND (MIT AND 0BSD)",
        "0BSD AND MIT",
    ),
    (
        "(MIT AND 0BSD) OR (MIT AND GPL-3.0-or-later)",
        "0BSD AND MIT OR GPL-3.0-or-later AND MIT",
    ),
    (
        "(MIT OR 0BSD) AND (MIT OR GPL-3.0-or-later)",
        "(0BSD OR MIT) AND (GPL-3.0-or-later OR MIT)",
    ),
    (
        "(MIT AND 0BSD) AND (MIT AND GPL-3.0-or-later)",
        "0BSD AND GPL-3.0-or-later AND MIT",
    ),
]

BAD_SORT_CASES = [
    "UNKNOWN-LICENSE",
]


def test_sort_expressions():
    cmd = ["py-spdx-license", "sort"]
    for expression, _ in GOOD_SORT_CASES:
        cmd.append("-e")
        cmd.append(expression)

    p = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, encoding="utf-8")
    assert p.stdout.splitlines() == [expected for _, expected in GOOD_SORT_CASES]

    for c in BAD_SORT_CASES:
        p = subprocess.run(["py-spdx-license", "sort", "-e", c], encoding="utf-8")
        assert p.returncode != 0


def test_sort_stdin():
    cmd = ["py-spdx-license", "sort"]

    p = subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        input="\n".join(expression for expression, _ in GOOD_SORT_CASES),
    )
    assert p.stdout.splitlines() == [expected for _, expected in GOOD_SORT_CASES]

    for c in BAD_SORT_CASES:
        p = subprocess.run(["py-spdx-license", "sort"], encoding="utf-8", input=c)
        assert p.returncode != 0


def test_sort_file(tmp_path):
    fn = tmp_path / "good.txt"
    with fn.open("w") as f:
        f.write("\n".join(expression for expression, _ in GOOD_SORT_CASES))

    p = subprocess.run(
        ["py-spdx-license", "sort", "-F", fn],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    assert p.stdout.splitlines() == [expected for _, expected in GOOD_SORT_CASES]

    fn = tmp_path / "bad.txt"
    for c in BAD_SORT_CASES:
        with fn.open("w") as f:
            f.write(c)
        p = subprocess.run(["py-spdx-license", "sort", "-F", fn], encoding="utf-8")
        assert p.returncode != 0
