#!/bin/sh
set -e

# create site dir 
mkdir -p _site

# construct the site
cat header.html > _site/index.html
python3 parse.py --rank >> _site/index.html 
cat laptophead.html >> _site/index.html
find . -type f -name "*.txt" -exec python3 parse.py "{}" >> _site/index.html \;
cat footer.html >> _site/index.html
cp favicon.ico _site/favicon.ico
cp styles.css _site/styles.css
echo "Build complete: _site directory generated."

