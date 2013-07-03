#!/usr/bin/env python
#
# Copyright 2013 Michael N. Gagnon
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# Idea: write code to intercept #links so that way we don't have rewrite any
# markdown and people can share links better.



# Requirements:
#   pip install markdown
#   --or--
#   easy_install markdown
# See http://pythonhosted.org/Markdown/install.html
#
import markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

import argparse
import glob
import os
import re
import string

TEMPLATE_HTML = string.Template('''
<!DOCTYPE html>
<meta charset="utf-8">
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/jquery-1.10.1.js"></script>
    <script src="js/d3.v3.js"></script>
    <script src="js/lodash.js"></script>
    <script src="js/sidenote.js"></script>
  </head>
  <body>
    <div class="headerbox">
$headerbox
    </div>
    <div class="addRemoveColumn">
      <a href="javascript:Sidenote.more()">more columns</a> /
      <a href="javascript:Sidenote.less()">fewer columns</a>
    </div>
    <div id="breadcrumbs"></div>
    <div id='column-container'>
      <div class='column' id="column0"></div>
    </div>
    <div class="content-storage">
$content_storage
    </div>
  </body>
</html>
''')

# Example match: [Bar](##bar)
sidenoteLinkParser = re.compile(r'\[(?P<linktext>[^\]]*)\]\(##(?P<identifier>[^)]*)\)')

def escapeQuotes(s):
  replaceSingeQuotes = re.sub("'", "\\'", s)
  return re.sub('"', '\\"', replaceSingeQuotes) 

def toMarkdown(source, line):
  '''
  Replaces all sidenote links with markdown links.
  A sidenote link is a link like this: [Bar](##bar)
  It is replaced with a link (in markdown syntax) that opens up a sidenote
  column.
  '''

  if line.startswith("    "):
    return line

  def sidenoteLinkToMarkdown(match):
    group = match.groupdict()
    return ("[%s](javascript:Sidenote.openColumn\('#%s','#%s','%s'\))" %
      (group["linktext"],
       escapeQuotes(source),
       escapeQuotes(group["identifier"]),
       escapeQuotes(group["linktext"])))

  return sidenoteLinkParser.sub(sidenoteLinkToMarkdown, line)

class SidenotePreprocessor(Preprocessor):
  def __init__(self, source):
    self.source = source
  def run(self, lines):
    return [toMarkdown(self.source, line) for line in lines]

class SidenoteExtension(Extension):
  def __init__(self, source):
    self.source = source
  def extendMarkdown(self, md, md_globals):
    md.preprocessors["SidenotePreprocessor"] = SidenotePreprocessor(self.source)

def rglob(directory):
  matches = set([])
  items = glob.glob(os.path.join(directory, "*"))
  for item in items:
    subitems = glob.glob(os.path.join(item, "*"))
    if len(subitems) == 0:
      matches.add(item)
    else:
      matches |= rglob(item)

  return matches

def getMarkdownFilenames(directory):
  '''
  returns (headerFilename, otherFiles)
  '''

  # list of markdown files
  files = filter(lambda f: f.endswith(".md"), rglob(directory))

  headerfiles = filter(lambda f: os.path.basename(f) == "header.md", files)
  if len(headerfiles) == 0:
    raise ValueError("directory must contain one file named header.md")
  elif len(headerfiles) > 1:
    raise ValueError("directory must contain one file named header.md, but " +
      "found several: %s" % headerfiles)
  else:
    headerfile = headerfiles[0]
  files.remove(headerfile)

  mainfiles = filter(lambda f: os.path.basename(f) == "main.md", files)
  if len(mainfiles) == 0:
    raise ValueError("directory must contain one file named main.md")
  elif len(mainfiles) > 1:
    raise ValueError("directory must contain one file named main.md, but " +
      "found several: %s" % mainfiles)

  return (headerfile, files)

def getBasename(filename):
  return os.path.splitext(os.path.basename(filename))[0]

def convertMarkdown(filename):
  with open(filename) as f:
    return markdown.markdown(f.read(),
      output_format = "html5",
      extensions=[SidenoteExtension(getBasename(filename))])

def compileSidenote(directory):

  headerfile, files = getMarkdownFilenames(directory)

  header = convertMarkdown(headerfile)

  contentColumns = {}
  for filename in files:
    basename = getBasename(filename)
    if basename in contentColumns:
      raise ValueError("content column '%s' defined at least twice: %s and %s" %
        (basename, contentColumns[basename], filename))
    contentColumns[basename] = convertMarkdown(filename)

  content_storage = []
  for identifier, html in contentColumns.iteritems():
    column = "<div id='%s'>\n%s\n</div>" % (identifier, html)
    content_storage.append(column)

  content_storage_str = "\n\n".join(content_storage)

  template_dict = {
    "headerbox": header,
    "content_storage": content_storage_str
  }

  return TEMPLATE_HTML.substitute(template_dict)

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Compile a Sidenote document')
  parser.add_argument('dir', type=str,
                     help='directory containing Sidenote-Markdown files')
  args = parser.parse_args()

  print compileSidenote(args.dir)
