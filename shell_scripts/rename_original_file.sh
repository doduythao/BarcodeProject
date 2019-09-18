#!/bin/bash
shopt -s nullglob
## Don't forget / at the end of input path
## $1 is 1d folder, $2 is 2d folder

for f in "$1"*.png "$1"*.jpg; do
  name=$(basename "$f");
  IFS='.' read -ra names <<<"$f"
  sname=${names[0]}
  if [[ $name != *[_]* ]]; then mv "$f" "$sname"_o.png; fi
done
