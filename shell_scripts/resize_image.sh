#!/bin/bash
shopt -s nullglob
## Don't forget / at the end of input path
## $1 is src folder, $2 is dst folder, $3 is new size. (format of imagemagick)

mkdir -p "$2"
for f in "$1"*.png "$1"*.jpg; do
  name=$(basename "$f")
  magick convert "$f" -resize "$3" "$2""$name"
done
