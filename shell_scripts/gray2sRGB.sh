#!/bin/bash
shopt -s nullglob
## Don't forget / at the end of input path
## $1 is 1d folder
for f in "$1"*.png; do
  name=$(basename "$f")
  mybool="$(magick identify -format '%[colorspace]' "$f")"
  if [ "$mybool" = "Gray" ]; then
    convert "$f" -define png:color-type=2 "$f"
  fi
done
