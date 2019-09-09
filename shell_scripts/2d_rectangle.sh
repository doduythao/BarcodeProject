#!/bin/bash
oplist=("20,20,20" "-20,0,40" "20,-20,-20" "20,20,-20" "20,20,40" "40,40,40" "0,40,0" "20,40,0" "20,40,-20" "20,20,0" "-20,0,20" "0,0,40" "-20,0,-20" "40,0,0")

len=${#oplist[*]} #determine length of array
IFS='.' read -ra names <<<"$1"

for ((i = 0; i < len; i++)); do
  ./rotate3D ${oplist[$i]} "$1" ${names[0]}_$i.png
done
