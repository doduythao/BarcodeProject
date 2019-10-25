#!/bin/bash
oplist=("20,20,20" "-20,0,40" "20,-20,-20" "20,20,-20" "20,20,40" "40,40,40" "0,40,0" "20,40,0" "20,40,-20" "20,20,0" "-20,0,20" "0,0,40" "-20,0,-20" "40,0,0")

IFS='.' read -ra names <<<"$1"
sname=${names[0]}
size="$(magick identify -format '%[fx:w]x%[fx:w]' "$1")"

magick convert "$1" -background white -gravity center -extent "$size" "$sname"_t.png

len=${#oplist[*]} #determine length of array

rannum=$(shuf -i 0-13 -n 1)
./rotate3D ${oplist[$rannum]} "$sname"_t.png "$sname"_.png

rm "$sname"_t.png
