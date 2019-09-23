#!/bin/bash
shopt -s nullglob
## Don't forget / at the end of input path
## $1 is src folder. rename all of files from its name to name start from 1 to N=number of file
count=0
for f in "$1"*.png "$1"*.jpg; do
  name=$(basename "$f")
  IFS='.' read -ra names <<<"$name"
  ext=${names[1]}
  mv "$f" "$1""$count"."$ext"
  count=$((count + 1))
done
