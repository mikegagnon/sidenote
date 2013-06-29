#! /usr/bin/env bash
#
# Copyright 2012 Michael N. Gagnon
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obCONFIG_INSTALLED_BACKUPtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# Usage:
#    ./mknote.sh output_dir
#
# - Creates a new Sidenote document in output_dir.
# - To compile the document, execute: output_dir/sidenote.sh
# - To view the document, open: output_dir/index.html
# - To edit the document, create / edit files under: output_dir/doc/
#

# $DIR is the absolute path for the directory containing this bash script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

OUTPUT_DIR=$1

if [ -z $OUTPUT_DIR ]
  then
    echo "Error: You must specify a directory name"
    exit 1
fi

if [ -a $OUTPUT_DIR ]
  then
    echo "Error: $OUTPUT_DIR already exists."
    exit 1
fi

mkdir $OUTPUT_DIR
mkdir $OUTPUT_DIR/doc
touch $OUTPUT_DIR/doc/header.md
touch $OUTPUT_DIR/doc/main.md
cp -r $DIR/css $OUTPUT_DIR
cp -r $DIR/js $OUTPUT_DIR

# 
echo "# Header goes here" > $OUTPUT_DIR/doc/header.md
echo "Main column goes here" > $OUTPUT_DIR/doc/main.md

# Create a sidenote.sh for $OUTPUT_DIR
SIDENOTE=$DIR/sidenote.py
MAKEFILE=$OUTPUT_DIR/sidenote.sh
echo "#! /usr/bin/env bash" > $MAKEFILE
echo "$SIDENOTE $OUTPUT_DIR/doc > $OUTPUT_DIR/index.html" >> $MAKEFILE
chmod +x $MAKEFILE
$MAKEFILE

echo "Created a new Sidenote document directory: $OUTPUT_DIR"
find $OUTPUT_DIR