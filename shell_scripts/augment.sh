#!/bin/bash
shopt -s nullglob
## Don't forget / at the end of input path
## $1 is 1d folder, $2 is 2d folder

for f in "$1"*.png "$1"*.jpg; do
#  ./1d_rectangle.sh "$f"
  ./cylinder_1d.sh "$f"
done

#for f in "$2"*.png "$2"*.jpg; do
#  ./2d_rectangle.sh "$f"
#  ./cylinder_2d.sh "$f"
#done