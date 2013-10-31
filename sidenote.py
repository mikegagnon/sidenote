#!/usr/bin/env python
#
# This is free and unencumbered software released into the public domain.
#
# Requirements:
#   markdown and smartypants
#
# Markdown:
#   pip install markdown
#   --or--
#   easy_install markdown
# See http://pythonhosted.org/Markdown/install.html
#
# Smartypants:
#   easy_install smartypants
# https://pypi.python.org/pypi/smartypants
#

import markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

import smartypants

import argparse
import codecs
import glob
import os
import re
import string
import sys

ENCODING = "utf-8"

TEMPLATE_HTML = string.Template('''
<!DOCTYPE html>
<meta charset="utf-8">
<html>
  <head>
    $html_head
    <link rel="stylesheet" type="text/css" href="css/bootstrap.css">
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="js/jquery-1.10.1.js"></script>
    <script src="js/d3.v3.js"></script>
    <script src="js/lodash.js"></script>
    <script src="js/sidenote.js"></script>
  </head>
  <body>
    <div class="btn-group addRemoveColumn">
      <button class="btn"><a href="javascript:Sidenote.more()">more columns</a></button>
      <button class="btn"><a href="javascript:Sidenote.less()">fewer columns</a></button>
    </div>
    <div class="headerbox">
$headerbox
    </div>
    <ul id="breadcrumbs" class="breadcrumb"></ul>
    <div id='column-container'>
      <a href="javascript:Sidenote.goBack()"><img id="left-arrow" class="hide-arrow" src="img/left_arrow.png"></a>
      <a href="javascript:Sidenote.goForward()"><img id="right-arrow" class="hide-arrow" src="img/right_arrow.png"></a>
      <div class='column' id="column0"></div>
    </div>
    <div class="content-storage">
$content_storage
    </div>
  </body>
</html>
''')

# Example match: [Bar](##bar)
SIDENOTE_LINK_PARSER = re.compile(r'\[(?P<linktext>[^\]]*)\]\(##(?P<identifier>[^)]*)\)')

TILDE_ANCHOR_PARSER = re.compile(r'^~(?P<identifier>[^\s]*)')

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

  # TODO: better code block detection
  # no translation of this line is part of a code block
  if re.match("^    [^\d\-*]", line) != None:
    return line

  def sidenoteLinkToMarkdown(match):
    group = match.groupdict()
    return ("[%s](javascript:Sidenote.openColumn\('#%s','#%s','%s'\))" %
      (group["linktext"],
       escapeQuotes(source),
       escapeQuotes(group["identifier"]),
       escapeQuotes(smartypants.smartyPants(group["linktext"]))))

  return SIDENOTE_LINK_PARSER.sub(sidenoteLinkToMarkdown, line)

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

def getBasename(filename):
  return os.path.splitext(os.path.basename(filename))[0]

def getMarkdownFilenames(directory):
  '''
  returns a dict that maps the pageId to the filename that contains the markdown for that pageId.
  This function does not perform 'tilde-expansion'.
  '''

  # list of markdown files
  files = filter(lambda f: f.endswith(".md"), rglob(directory))

  headerfiles = filter(lambda f: os.path.basename(f) == "header.md", files)
  if len(headerfiles) == 0:
    raise ValueError("directory must contain one file named header.md")
  elif len(headerfiles) > 1:
    raise ValueError("directory must contain one file named header.md, but " +
      "found several: %s" % headerfiles)

  mainfiles = filter(lambda f: os.path.basename(f) == "main.md", files)
  if len(mainfiles) == 0:
    raise ValueError("directory must contain one file named main.md")
  elif len(mainfiles) > 1:
    raise ValueError("directory must contain one file named main.md, but " +
      "found several: %s" % mainfiles)

  filenames = {}
  for f in files:
    pageId = getBasename(f)
    if pageId in filenames:
      raise ValueError("Filenames collide: %s and %s" % (f, filenames[pageId]))
    filenames[pageId] = f 

  return filenames

def tildeExpand(pageId, filename):
  '''
  performs the 'tilde-expansion' operation on the specified file.
  returns a dict that maps the pageId to the markdown content for that column, for each column contained in filename
  '''
  currentPageId = pageId
  columns = {
    currentPageId: []
  }

  with codecs.open(filename, encoding=ENCODING) as f:
    for line in f:
      tilde_anchor = TILDE_ANCHOR_PARSER.match(line)
      if tilde_anchor == None:
        columns[currentPageId].append(line)
      else:
        columns[currentPageId] = "".join(columns[currentPageId])
        currentPageId = tilde_anchor.groupdict()["identifier"]
        if len(currentPageId) == 0:
          # TODO: better error message
          raise ValueError("Found malformed tilde-anchor")
        columns[currentPageId] = []

  columns[currentPageId] = "".join(columns[currentPageId])

  return columns

def loadColumns(directory):
  '''
  returns a dict that maps the pageId to the markdown content for that column.
  This function performs 'tilde-expansion'.
  '''

  columns = {}

  for pageId, filename in getMarkdownFilenames(directory).iteritems():
    for newPageId, columnContent in tildeExpand(pageId, filename).iteritems():
      columns[newPageId] = columnContent

  return columns

def convertMarkdown(pageId, columnContent):
  md = markdown.markdown(columnContent,
    output_format = "html5",
    extensions=[SidenoteExtension(pageId)])

  return smartypants.smartyPants(md)

def compileSidenote(directory):

  columns = loadColumns(directory)

  if "html_head" in columns:
    html_head = columns["html_head"]
    del(columns["html_head"])
  else:
    html_head = ""

  header = convertMarkdown("header", columns["header"])
  del(columns["header"])

  convertedColumns = {}
  for pageId, markdown in columns.iteritems():
    if pageId in convertedColumns:
      raise ValueError("content column '%s' defined at least twice:" % pageId)
    convertedColumns[pageId] = convertMarkdown(pageId, markdown)

  content_storage = []
  for identifier, html in convertedColumns.iteritems():
    column = "<div id='%s'>\n%s\n</div>" % (identifier, html)
    content_storage.append(column)

  content_storage_str = "\n\n".join(content_storage)

  template_dict = {
    "html_head": html_head,
    "headerbox": header,
    "content_storage": content_storage_str
  }

  return TEMPLATE_HTML.substitute(template_dict)

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Compile a Sidenote document')
  parser.add_argument('dir', type=str,
                     help='directory containing Sidenote-Markdown files')
  args = parser.parse_args()

  stdout = codecs.getwriter(ENCODING)(sys.stdout)
  stdout.write(compileSidenote(args.dir) + "\n")
