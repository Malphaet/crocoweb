#!/usr/bin/env python

# Copyleft (c) 2016 Cocobug All Rights Reserved.

import argparse,os,sys
from generator import *


def vprint(*x):
    if args.verbose:
        print(x)


parser = argparse.ArgumentParser(description='Website on-the-fly & static generator')
#subparsers = parser.add_subparsers(help='Commands')

# The argparse should look like this:
# vkyweb.py PATH_TO_WEBSITE --update(only update) --verbose(show as much as possible) --dry(don't actually write anything) -d(destination if not current folder) -m(custom model) -l(only use theese languages)
parser.add_argument('website_path',metavar="path_to_the_website",type=str,help="Path to the website to parse")
parser.add_argument("--verbose",action="store_true",help="Verbosity to display")
parser.add_argument('--update',action="store_true",help="Only update, don't rewrite")
parser.add_argument("--dry",action="store_true",help="Dry run, don't write anything")
parser.add_argument("-d",metavar="destination",type=str,default=".",help="Destination to write to")
parser.add_argument("-l",metavar="langs",type=str,nargs="+",help="List of langs to generate the site to")
args=parser.parse_args()

# Make tree
if not (os.path.exists(args.website_path)):
    if args.verbose:
        print "O"
        print("Path {} does not exist".format(args.website_path))
    sys.exit()
website=tree_parser.makeWebsite(args.website_path)
#website.print_webtree(lang="fr",prefix=" * ")

# Walk & generate
if args.verbose:
    print("Website will be generated in {}".format(args.l))

#for every lang, do a mix of print_webtree and makeContainer
    #container=model.makeContainer(s)
