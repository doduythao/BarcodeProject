#!/bin/bash

IFS='.' read -ra names <<<"$1"
sname=${names[0]}
horizon="$(magick identify -format '%[fx:w*6.283]x%[fx:h*11]' "$1")"
vertical="$(magick identify -format '%[fx:w*5]x%[fx:h*5*6.283]' "$1")"
w="$(magick identify -format '%[fx:w]' "$1")"
h="$(magick identify -format '%[fx:h]' "$1")"

magick convert "$1" -background "#e3e3e3" -gravity center -extent "$horizon" "$sname"_h.png
magick convert "$1" -background "#e3e3e3" -gravity center -extent "$vertical" "$sname"_v.png

rannum=$(shuf -i 1-12 -n 1)

if [ "$rannum" -eq 1 ]; then
  ./cylinderize -m horizontal -p 10 -w 100 -a 10 -r "$w" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_ha.png
  magick convert "$sname"_ha.png -gravity center -crop "$(magick identify -format '%[fx:w*0.2]x%[fx:h*0.2]+0+0' "$sname"_ha.png)" +repage "$sname"_ha.png
fi
if [ "$rannum" -eq 2 ]; then
  ./cylinderize -m horizontal -p 15 -w 100 -a -15 -r "$w" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hb.png
  magick convert "$sname"_hb.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.5]+0+0' "$sname"_hb.png)" +repage "$sname"_hb.png
  magick convert "$sname"_hb.png -gravity north -crop "$(magick identify -format '%[fx:w*0.8]x%[fx:h*0.6]+0+0' "$sname"_hb.png)" +repage "$sname"_hb.png
fi

if [ "$rannum" -eq 3 ]; then
  ./cylinderize -m horizontal -p 15 -w 50 -a -15 -r "$((w*2))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hc.png
  magick convert "$sname"_hc.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.5]+0+0' "$sname"_hc.png)" +repage "$sname"_hc.png
  magick convert "$sname"_hc.png -gravity north -crop "$(magick identify -format '%[fx:w*0.8]x%[fx:h*0.5]+0+0' "$sname"_hc.png)" +repage "$sname"_hc.png
fi

if [ "$rannum" -eq 4 ]; then
  ./cylinderize -m horizontal -p 15 -w 45 -a -30 -r "$((w*2))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hd.png
  magick convert "$sname"_hd.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.5]+0+0' "$sname"_hd.png)" +repage "$sname"_hd.png
  magick convert "$sname"_hd.png -gravity north -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.3]+0+0' "$sname"_hd.png)" +repage "$sname"_hd.png
fi

if [ "$rannum" -eq 5 ]; then
  ./cylinderize -m horizontal -p 20 -w 45 -a 40 -r "$((w*2))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_he.png
  magick convert "$sname"_he.png -gravity south -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.5]+0+0' "$sname"_he.png)" +repage "$sname"_he.png
  magick convert "$sname"_he.png -gravity center -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.3]+0+0' "$sname"_he.png)" +repage "$sname"_he.png
fi

if [ "$rannum" -eq 6 ]; then
  ./cylinderize -m horizontal -p -20 -w 45 -a 30 -r "$((w*2))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hf.png
  magick convert "$sname"_hf.png -gravity south -crop "$(magick identify -format '%[fx:w*0.5]x%[fx:h*0.4]+0+0' "$sname"_hf.png)" +repage "$sname"_hf.png
  magick convert "$sname"_hf.png -gravity north -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.6]+0+0' "$sname"_hf.png)" +repage "$sname"_hf.png
fi

if [ "$rannum" -eq 7 ]; then
  ./cylinderize -m vertical -p 10 -w 100 -a 10 -r "$((h*5))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_va.png
  magick convert "$sname"_va.png -gravity center -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.2]+0+0' "$sname"_va.png)" +repage "$sname"_va.png
fi

if [ "$rannum" -eq 8 ]; then
  ./cylinderize -m vertical -p 15 -w 100 -a -15 -r "$((h*5))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vb.png
  magick convert "$sname"_vb.png -gravity center -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.2]+0+0' "$sname"_vb.png)" +repage "$sname"_vb.png
  magick convert "$sname"_vb.png -gravity west -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.7]+0+0' "$sname"_vb.png)" +repage "$sname"_vb.png
fi

if [ "$rannum" -eq 9 ]; then
  ./cylinderize -m vertical -p 15 -w 50 -a -15 -r "$((h*2*5))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vc.png
  magick convert "$sname"_vc.png -gravity center -crop "$(magick identify -format '%[fx:w*0.6]x%[fx:h*0.2]+0+0' "$sname"_vc.png)" +repage "$sname"_vc.png
  magick convert "$sname"_vc.png -gravity west -crop "$(magick identify -format '%[fx:w*0.6]x%[fx:h*0.6]+0+0' "$sname"_vc.png)" +repage "$sname"_vc.png
fi

if [ "$rannum" -eq 10 ]; then
  ./cylinderize -m vertical -p 15 -w 45 -a -30 -r "$((h*2*5))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vd.png
  magick convert "$sname"_vd.png -gravity center -crop "$(magick identify -format '%[fx:w*0.8]x%[fx:h*0.2]+0+0' "$sname"_vd.png)" +repage "$sname"_vd.png
  magick convert "$sname"_vd.png -gravity west -crop "$(magick identify -format '%[fx:w*0.4]x%[fx:h*0.7]+0+0' "$sname"_vd.png)" +repage "$sname"_vd.png
fi

if [ "$rannum" -eq 11 ]; then
  ./cylinderize -m vertical -p 20 -w 45 -a 40 -r "$((h*2*5))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_ve.png
  magick convert "$sname"_ve.png -gravity east -crop "$(magick identify -format '%[fx:w*0.35]x%[fx:h*0.15]+0+0' "$sname"_ve.png)" +repage "$sname"_ve.png
fi

if [ "$rannum" -eq 12 ]; then
  ./cylinderize -m vertical -p -20 -w 45 -a 30 -r "$((h*2*5))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vf.png
  magick convert "$sname"_vf.png -gravity east -crop "$(magick identify -format '%[fx:w*0.4]x%[fx:h*0.2]+0+0' "$sname"_vf.png)" +repage "$sname"_vf.png
  magick convert "$sname"_vf.png -gravity northwest -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.6]+0+0' "$sname"_vf.png)" +repage "$sname"_vf.png
fi

rm "$sname"_h.png "$sname"_v.png