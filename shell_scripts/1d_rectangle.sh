#!/bin/bash
oplist=("20,20,20" "-20,0,40" "20,-20,-20" "20,20,-20" "20,20,40" "40,40,40" "0,40,0" "20,40,0" "20,40,-20" "20,20,0" "-20,0,20" "0,0,40" "-20,0,-20" "40,0,0")

IFS='.' read -ra names <<<"$1"
sname=${names[0]}
size="$(magick identify -format '%[fx:w]x%[fx:w]' "$1")"

magick convert "$1" -background white -gravity center -extent "$size" "$sname"_t.png

len=${#oplist[*]} #determine length of array

for ((i = 0; i < len; i++)); do
  ./rotate3D ${oplist[$i]} "$sname"_t.png "$sname"_$i.png
done

rm "$sname"_t.png
