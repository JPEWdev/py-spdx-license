#
# Copyright Joshua Watt <JPEWhacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#

import py_spdx_license

import pytest


@pytest.mark.parametrize(
    "expression,expected",
    [
        pytest.param(
            "MIT AND MIT",
            "MIT",
            id="Duplicate AND",
        ),
        pytest.param(
            "MIT OR MIT",
            "MIT",
            id="Duplicate OR",
        ),
        pytest.param(
            "MIT AND 0BSD",
            "0BSD AND MIT",
            id="AND reorder",
        ),
        pytest.param(
            "MIT OR 0BSD",
            "0BSD OR MIT",
            id="OR reorder",
        ),
        pytest.param(
            "(MIT AND 0BSD) AND (MIT AND 0BSD)",
            "0BSD AND MIT",
            id="Duplicate AND expressions",
        ),
        pytest.param(
            "(MIT AND 0BSD) OR (MIT AND GPL-3.0-or-later)",
            "0BSD AND MIT OR GPL-3.0-or-later AND MIT",
            id="Reorder with AND subexpressions",
        ),
        pytest.param(
            "(MIT OR 0BSD) AND (MIT OR GPL-3.0-or-later)",
            "(0BSD OR MIT) AND (GPL-3.0-or-later OR MIT)",
            id="Reorder with OR subexpressions",
        ),
        pytest.param(
            "(MIT AND 0BSD) AND (MIT AND GPL-3.0-or-later)",
            "0BSD AND GPL-3.0-or-later AND MIT",
            id="Reduction with balanced AND subexpressions",
        ),
        pytest.param(
            "(MIT OR 0BSD) OR (MIT OR GPL-3.0-or-later)",
            "0BSD OR GPL-3.0-or-later OR MIT",
            id="Reduction with balanced OR subexpressions",
        ),
        pytest.param(
            "((MIT OR 0BSD) OR MIT) OR GPL-3.0-or-later",
            "0BSD OR GPL-3.0-or-later OR MIT",
            id="Reorder with nested expressions (left)",
        ),
        pytest.param(
            "MIT OR (0BSD OR (MIT OR GPL-3.0-or-later))",
            "0BSD OR GPL-3.0-or-later OR MIT",
            id="Reorder with nested expression (right)",
        ),
        pytest.param(
            "MIT OR (0BSD OR MIT) OR GPL-3.0-or-later",
            "0BSD OR GPL-3.0-or-later OR MIT",
            id="Reduction with OR subexpression",
        ),
        pytest.param(
            "(MIT AND (0BSD OR MIT)) AND (0BSD AND GPL-3.0-or-later)",
            "0BSD AND GPL-3.0-or-later AND MIT AND (0BSD OR MIT)",
            id="Sorting Conjunctions (single OR)",
        ),
        pytest.param(
            "(MIT OR (0BSD AND MIT)) OR (0BSD OR GPL-3.0-or-later)",
            "0BSD AND MIT OR 0BSD OR GPL-3.0-or-later OR MIT",
            id="Sorting Conjunctions (single AND)",
        ),
        pytest.param(
            "(MIT AND ((0BSD OR MIT) AND LGPL-3.0-or-later)) AND (0BSD AND GPL-3.0-or-later)",
            "0BSD AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND (0BSD OR MIT)",
            id="Sorting Conjunctions (deep OR)",
        ),
        pytest.param(
            "(MIT AND ((0BSD OR MIT) AND LGPL-3.0-or-later)) AND ((0BSD AND (0BSD OR MIT)) AND GPL-3.0-or-later)",
            "0BSD AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND (0BSD OR MIT)",
            id="Reducing Conjunctions (deep OR)",
        ),
        pytest.param(
            # GPL-3.0-later is split across an otherwise sorted list; make sure
            # it can be detected and merged
            "(0BSD AND GPL-3.0-or-later) AND (GPL-3.0-or-later AND MIT)",
            "0BSD AND GPL-3.0-or-later AND MIT",
            id="Reducing evenly split conjunctions",
        ),
        pytest.param(
            "GPL-3.0-or-later WITH GCC-exception-3.1 AND GPL-3.0-or-later WITH GCC-exception-3.1",
            "GPL-3.0-or-later WITH GCC-exception-3.1",
            id="Reduction of duplicate WITH",
        ),
        pytest.param(
            "GPL-3.0-or-later WITH GCC-exception-3.1 AND GPL-3.0-or-later",
            "GPL-3.0-or-later AND GPL-3.0-or-later WITH GCC-exception-3.1",
            id="Do not reduce WITH and non-WITH",
        ),
    ],
)
def test_sort(expression, expected):
    actual = py_spdx_license.parse(expression).sort()
    assert actual.to_string() == expected
