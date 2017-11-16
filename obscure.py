#!/usr/bin/env python
#
# This is free and unencumbered software released into the public domain.
#

import argparse


def obscure(filename):
    pass

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='"Obscure" links in a Sidenote document')
  parser.add_argument('file', type=str,
                     help='the markdown file to obscure')
  args = parser.parse_args()

  obscure(args.file)