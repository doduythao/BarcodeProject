#!/bin/bash
## Don't forget / at the end of input path.
## $1 scr path, $2 dst path
mkdir -p "$2"
for f in "$1"*_2.png "$1"*_2_pts.yml; do
  name=$(basename "$f")
  cp "$f" "$2""$name"
done
