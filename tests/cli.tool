#!/usr/bin/env python3

import sys
import argparse

import conftest


def _main(prog, *args):
    parser = argparse.ArgumentParser(
        prog=prog,
        description='A simple testing helper')
    parser.add_argument('-o', '--stdout', action='store',
                        help='Output the value to stdout.')
    parser.add_argument('-e', '--stderr', action='store',
                        help='Output the value to stderr.')
    parser.add_argument('-i', '--stdin', action='store_true',
                        help='Report everything written to stdin.')
    parser.add_argument('-x', '--exit', action='store', type=int, default=0,
                        help='Exit with the given status.')

    options = parser.parse_args(args)

    if options.stdin:
        print('STDIN:', sys.stdin.read())
    if options.stdout:
        print('STDOUT:', options.stdout)
    if options.stderr:
        print('STDERR:', options.stderr, file=sys.stderr)

    return options.exit


if __name__ == '__main__':
    sys.exit(_main(*sys.argv))
