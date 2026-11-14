#
# SPDX-FileContributor: Arthit Suriyawongkul
# SPDX-FileCopyrightText: Joshua Watt <JPEWhacker@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-License-Identifier: MIT
#

import py_spdx_license

import pytest


def test_replacements():
    # Made from the names on the License List. A new List that changes this
    # needs a look: each entry is a claim about what an ID means. A bare ID
    # (GPL-2.0), AGPL-3.0, GFDL-1.3 and the "-with-" IDs are not here: the
    # List does not say if they are only or or later
    assert py_spdx_license.DEPRECATED_REPLACEMENTS == {
        "GPL-1.0+": "GPL-1.0-or-later",
        "GPL-2.0+": "GPL-2.0-or-later",
        "GPL-3.0+": "GPL-3.0-or-later",
        "LGPL-2.0+": "LGPL-2.0-or-later",
        "LGPL-2.1+": "LGPL-2.1-or-later",
        "LGPL-3.0+": "LGPL-3.0-or-later",
        "StandardML-NJ": "SMLNJ",
    }


def lic(license_id, name, pages=("page",), *, deprecated=False):
    return {
        "licenseId": license_id,
        "name": name,
        "seeAlso": list(pages),
        "isDeprecatedLicenseId": deprecated,
    }


@pytest.mark.parametrize(
    "licenses,expected",
    [
        pytest.param([lic("New", "A")], {"Old": "New"}, id="same name and page"),
        pytest.param([lic("New", "a")], {"Old": "New"}, id="name in another case"),
        pytest.param([lic("New", "A"), lic("New2", "A")], {}, id="two with the name"),
        pytest.param([lic("New", "B")], {}, id="no ID with the name"),
        pytest.param([lic("New", "A", ["other"])], {}, id="no shared page"),
        pytest.param([lic("New", "A", deprecated=True)], {}, id="new is deprecated"),
        pytest.param([lic("Old-only", "A")], {}, id="bare ID, -only form"),
        pytest.param([lic("Old-or-later", "A")], {}, id="bare ID, -or-later form"),
    ],
)
def test_replacement_rules(monkeypatch, licenses, expected):
    listed = [lic("Old", "A", deprecated=True), *licenses]
    monkeypatch.setattr(
        py_spdx_license.ast, "_LICENSES", {x["licenseId"].lower(): x for x in listed}
    )
    assert py_spdx_license.ast._deprecated_replacements() == expected


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("GPL-2.0+", "GPL-2.0-or-later"),
        ("StandardML-NJ", "SMLNJ"),
        (
            "(GPL-2.0+ WITH GCC-exception-2.0 OR MIT) AND Apache-2.0",
            "(GPL-2.0-or-later WITH GCC-exception-2.0 OR MIT) AND Apache-2.0",
        ),
        ("StandardML-NJ+ AND GPL-2.0+", "SMLNJ+ AND GPL-2.0-or-later"),
        # Not upgraded
        ("MIT+", "MIT+"),
        ("MIT", "MIT"),
        ("GPL-2.0-or-later", "GPL-2.0-or-later"),
        ("GPL-2.0", "GPL-2.0"),
        ("GPL-2.0 WITH GCC-exception-2.0", "GPL-2.0 WITH GCC-exception-2.0"),
    ],
)
def test_upgrade(expression, expected):
    assert py_spdx_license.parse(expression).upgrade().to_string() == expected


@pytest.mark.parametrize(
    "expression", ["GPL-2.0++", "GPL-2.0++ WITH GCC-exception-2.0"]
)
def test_plus_after_a_plus_id_is_refused(expression):
    # "GPL-2.0+" is an ID, "+" cannot follow it; the upgrade must not turn it
    # into the valid-looking "GPL-2.0-or-later+"
    with pytest.raises(py_spdx_license.ParseError):
        py_spdx_license.parse(expression)


def test_upgrade_returns_a_new_tree():
    node = py_spdx_license.parse("MIT OR gpl-2.0+")
    upgraded = node.upgrade()

    # "gpl-2.0+" is one token and one deprecated ID, not "gpl-2.0" and "+"
    assert node.right.ident == "GPL-2.0+"
    assert node.right.deprecated
    assert upgraded.right.ident == "GPL-2.0-or-later"
    assert not upgraded.right.deprecated
    # An error message points at the text the writer typed
    assert upgraded.right.get_range() == (7, 15)


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("MIT AND GPL-2.0+ AND GPL-2.0-or-later", "GPL-2.0-or-later AND MIT"),
        # A chain where the upgrade makes a duplicate: first, middle, nested
        ("MIT OR GPL-2.0+ OR GPL-2.0-or-later", "GPL-2.0-or-later OR MIT"),
        ("GPL-2.0+ OR MIT OR GPL-2.0-or-later", "GPL-2.0-or-later OR MIT"),
        ("Zlib OR GPL-2.0+ OR GPL-2.0-or-later", "GPL-2.0-or-later OR Zlib"),
        ("GPL-2.0+ OR (GPL-2.0-or-later OR MIT)", "GPL-2.0-or-later OR MIT"),
        ("(GPL-2.0+ OR MIT) OR GPL-2.0-or-later", "GPL-2.0-or-later OR MIT"),
        ("GPL-2.0 AND GPL-2.0-only", "GPL-2.0 AND GPL-2.0-only"),
    ],
)
def test_sort_upgrades(expression, expected):
    assert py_spdx_license.parse(expression).sort().to_string() == expected
