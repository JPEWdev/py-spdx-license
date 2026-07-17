#
# Copyright Joshua Watt <JPEWhacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#

import argparse
import sys
from pathlib import Path

import py_spdx_license


def handle_sort(args):
    def read_expressions():
        if args.expression:
            yield from args.expression
        elif args.infile:
            for p in args.infile:
                with p.open("r") as f:
                    yield from f
        else:
            yield from sys.stdin

    for e in read_expressions():
        try:
            if args.match:
                n = py_spdx_license.parse_match(e)
            else:
                n = py_spdx_license.parse(e)
        except py_spdx_license.ParseError as e:
            print(e.format())
            return 1

        print(n.sort().to_string())

    return 0


def main():
    parser = argparse.ArgumentParser("SPDX License Tool")
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=py_spdx_license.VERSION,
    )

    subparsers = parser.add_subparsers(title="command", required=True)

    sort_parser = subparsers.add_parser(
        "sort", help="Sort and simplify license expression"
    )
    sort_parser.add_argument(
        "--match",
        "-m",
        help="Parse as a match expression",
        action="store_true",
    )
    sort_input_group = sort_parser.add_mutually_exclusive_group()
    sort_input_group.add_argument(
        "-e",
        "--expression",
        help="Expression to sort",
        action="append",
        default=[],
    )
    sort_input_group.add_argument(
        "-F",
        "--file",
        dest="infile",
        type=Path,
        help="Read licenses from file (one per line)",
        action="append",
        default=[],
    )
    sort_parser.set_defaults(func=handle_sort)

    args = parser.parse_args()

    return args.func(args)
