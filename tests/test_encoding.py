# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileCopyrightText: Joshua Watt <JPEWhacker@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: MIT

import subprocess
import sys

import py_spdx_license

import pytest


@pytest.mark.skipif(
    sys.version_info < (3, 10), reason="EncodingWarning is new in Python 3.10"
)
def test_import_does_not_use_locale_encoding():
    """
    Test that the bundled license data is not read with the locale encoding,
    which cannot decode it under a legacy locale such as ja_JP.eucJP
    """
    subprocess.run(
        [
            sys.executable,
            "-X",
            "warn_default_encoding",
            "-W",
            "error::EncodingWarning",
            "-c",
            "import py_spdx_license",
        ],
        check=True,
    )


def test_non_ascii_name():
    """
    Test that a license name with non-ASCII characters is decoded as UTF-8
    """
    lic = py_spdx_license.get_license("LiLiQ-P-1.1")
    assert lic["name"] == "Licence Libre du Québec – Permissive version 1.1"
