#
# Copyright Joshua Watt <JPEWhacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#

import py_spdx_license

import pytest


@pytest.mark.parametrize(
    "expression,error",
    [
        pytest.param(
            "MIT AND",
            r"Unexpected 'AND'",
            id="Dangling trailing AND",
        ),
        pytest.param(
            "MIT OR",
            r"Unexpected 'OR'",
            id="Dangling trailing OR",
        ),
        pytest.param(
            "MIT WITH",
            r"Unexpected 'WITH'",
            id="Dangling trailing WITH",
        ),
        pytest.param(
            "AND MIT",
            "Unexpected 'AND'",
            id="Dangling leading AND",
        ),
        pytest.param(
            "OR MIT",
            "Unexpected 'OR'",
            id="Dangling leading OR",
        ),
        pytest.param(
            "WITH MIT",
            r"Unexpected 'WITH'",
            id="Dangling leading WITH",
        ),
        pytest.param(
            " \n\t",
            r"Empty expression",
            id="Whitespace only",
        ),
        pytest.param(
            "",
            r"Empty expression",
            id="Empty string",
        ),
        pytest.param(
            "UNKNOWNID",
            r"Unknown Expression 'UNKNOWNID'",
            id="Unknown ID",
        ),
        pytest.param(
            "MIT AND UNKNOWNID",
            r"Unknown Expression 'UNKNOWNID'",
            id="Unknown ID with AND",
        ),
        pytest.param(
            "MIT OR UNKNOWNID",
            r"Unknown Expression 'UNKNOWNID'",
            id="Unknown ID with OR",
        ),
        pytest.param(
            "MIT 0BSD",
            r"Unexpected Expression",
            id="Missing conjunction",
        ),
        pytest.param(
            "( AND )",
            r"Invalid expression for parentheses",
            id="Bad compound expression",
        ),
        pytest.param(
            "MIT )",
            r"Missing matching '\('",
            id="Missing left parenthesis",
        ),
        pytest.param(
            "AND MIT )",
            r"'[(]' expected, but not found",
            id="Wrong token for left parenthesis",
        ),
    ],
)
def test_parse_error(expression, error):
    with pytest.raises(py_spdx_license.ParseError, match=error):
        py_spdx_license.parse(expression)
