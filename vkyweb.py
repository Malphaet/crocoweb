#!/usr/bin/env python

Copyleft (c) 2016 Cocobug All Rights Reserved.

import argparse

parser = argparse.ArgumentParser(description='Website on-the-fly & static generator')
subparsers = parser.add_subparsers(help='Commands')

# create the parser for the "a" command
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('bar', type=int, help='bar help')
