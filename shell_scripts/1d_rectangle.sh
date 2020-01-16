#!/bin/bash
oplist=("20,20,20" "-20,0,30" "20,-20,-20" "20,20,-20" "20,20,30" "0,30,0" "20,30,0" "20,30,-20" "20,20,0" "-20,0,20" "0,0,30" "-20,0,-20" "30,0,0")

IFS='.' read -ra names <<<"$1"
sname=${names[0]}
size="$(magick identify -format '%[fx:w]x%[fx:w]' "$1")"

magick convert "$1" -background white -gravity center -extent "$size" "$sname"_t.png

len=${#oplist[*]} #determine length of array

rannum=$(shuf -i 0-12 -n 1)
./rotate3D ${oplist[$rannum]} "$sname"_t.png "$sname"_.png

rm "$sname"_t.png
