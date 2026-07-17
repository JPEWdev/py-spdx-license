#
# Copyright Joshua Watt <JPEWhacker@gmail.com>
#
# SPDX-License-Identifier: MIT
#

import argparse
import sys
from pathlib import Path

import py_spdx_license


def read_expressions(args):
    if args.expression:
        yield from args.expression
    elif args.infile:
        for p in args.infile:
            with p.open("r") as f:
                yield from f
    else:
        yield from sys.stdin


def handle_sort(args):
    for e in read_expressions(args):
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


def handle_ast(args):
    for e in read_expressions(args):
        try:
            if args.match:
                n = py_spdx_license.parse_match(e)
            else:
                n = py_spdx_license.parse(e)
        except py_spdx_license.ParseError as e:
            print(e.format())
            return 1

        if args.sort:
            n = n.sort()

        def walk(node, indent=""):
            print(f"{indent}{node.__class__.__name__} - '{node.token.value}'")
            for c in node.children:
                walk(c, indent + "  ")

        walk(n)

    return 0


def add_input_group(parser):
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "-e",
        "--expression",
        help="License expression",
        action="append",
        default=[],
    )
    input_group.add_argument(
        "-F",
        "--file",
        dest="infile",
        type=Path,
        help="Read expression from file (one per line)",
        action="append",
        default=[],
    )


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
    add_input_group(sort_parser)
    sort_parser.set_defaults(func=handle_sort)

    ast_parser = subparsers.add_parser(
        "ast", help="Print abstract syntax tree for an expression"
    )
    ast_parser.add_argument("--sort", "-s", help="Sort expression", action="store_true")
    ast_parser.add_argument(
        "--match", "-m", help="Parse as match expression", action="store_true"
    )
    add_input_group(ast_parser)
    ast_parser.set_defaults(func=handle_ast)

    args = parser.parse_args()

    return args.func(args)
