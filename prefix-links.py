#!/usr/bin/env python
#
# This is free and unencumbered software released into the public domain.
#
# Sometimes you want to include one sidenote document into another.
# One way you could do that is copy the .md files from one project into another.
# However, this creates a risk of link-tag collisions. I.e. one project
# defines ~foo and the other project also defines ~foo.
#
# prefix-links.py solves this problem. It takes a .md file as input, then
# prefixes each link tag with a random string. Therefore ~foo becomes 
# ~4C5FGAL2foo
#
# Then you can safely include .md files from multiple projects into another
# project
#

from sidenote import *

import argparse
import random
import re
import string

# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def obscure(filename):
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        newline = ""

        # tokenize the line into links and non-links
        for part in LINK_PARSER.split(line):
            if LINK_PARSER.match(part):
                newpart = part.replace("(##", "(##" + key)
                newline += newpart
            else:
                newline += part

        if TILDE_ANCHOR_PARSER.match(newline):
            newline = newline.replace("~", "~" + key)

        print newline,


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='"Obscure" links in a Sidenote document')
    parser.add_argument('file', type=str,
                       help='the markdown file to obscure')
    args = parser.parse_args()

    obscure(args.file)
