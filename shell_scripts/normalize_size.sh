#!/bin/bash
shopt -s nullglob
## Don't forget / at the end of input path
## $1 is src folder, $2 is dst folder.
array1=("white" "#e3e3e3")
array2=("center" "south" "north" "west" "east" "northeast" "northwest" "southeast" "southwest")

mkdir -p "$2"
for f in "$1"*.png "$1"*.jpg; do
  name=$(basename "$f")
  IFS='.' read -ra names <<<"$name"
  sname=${names[0]}
  rannum1=$(shuf -i 0-1 -n 1)
  rannum2=$(shuf -i 0-8 -n 1)
  w="$(magick identify -format '%[fx:w]' "$f")"
  h="$(magick identify -format '%[fx:h]' "$f")"
  if [ "$w" -lt 800 ] && [ "$h" -lt 450 ];
  then
    magick convert "$f" -gravity ${array2[$rannum2]} -background ${array1[$rannum1]} -extent 1280x720 "$2""$sname".png
  else
    magick convert "$f" -resize 800x450 -gravity ${array2[$rannum2]} -background ${array1[$rannum1]} -extent 1280x720 "$2""$sname".png
  fi
done
