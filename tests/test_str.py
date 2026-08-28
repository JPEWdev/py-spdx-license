# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileCopyrightText: Joshua Watt <JPEWhacker@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: MIT

import py_spdx_license


def test_str(capsys):
    expr = "MIT OR Apache-2.0"
    parsed = py_spdx_license.parse(expr)

    assert str(parsed) == parsed.to_string()
    assert str(parsed) == expr
    assert f"{parsed}" == expr

    print(parsed)
    captured = capsys.readouterr()
    assert captured.out.strip() == expr

    assert str(parsed.sort()) == parsed.sort().to_string()
    assert str(parsed.sort()) == "Apache-2.0 OR MIT"
