#!/bin/bash

IFS='.' read -ra names <<<"$1"
sname=${names[0]}
horizon="$(magick identify -format '%[fx:w*3*6.283]x%[fx:w*10]' "$1")"
vertical="$(magick identify -format '%[fx:w*10]x%[fx:w*3*6.283]' "$1")"
w="$(magick identify -format '%[fx:w]' "$1")"
h="$(magick identify -format '%[fx:w]' "$1")"

magick convert "$1" -background "#e3e3e3" -gravity center -extent "$horizon" "$sname"_h.png
magick convert "$1" -background "#e3e3e3" -gravity center -extent "$vertical" "$sname"_v.png

./cylinderize -m vertical -p 10 -w 100 -a 10 -r "$((w*3))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_ha.png
magick convert "$sname"_ha.png -gravity center -crop "$(magick identify -format '%[fx:w*0.15]x%[fx:h*0.2]+0+0' "$sname"_ha.png)" +repage "$sname"_ha.png
magick convert "$sname"_ha.png -gravity southeast -crop "$(magick identify -format '%[fx:w*0.7]x%[fx:h*0.7]+0+0' "$sname"_ha.png)" +repage "$sname"_ha.png

./cylinderize -m vertical -p 15 -w 100 -a -15 -r "$((w*3))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hb.png
magick convert "$sname"_hb.png -gravity center -crop "$(magick identify -format '%[fx:w*0.2]x%[fx:h*0.3]+0+0' "$sname"_hb.png)" +repage "$sname"_hb.png
magick convert "$sname"_hb.png -gravity southwest -crop "$(magick identify -format '%[fx:w*0.5]x%[fx:h*0.6]+0+0' "$sname"_hb.png)" +repage "$sname"_hb.png

./cylinderize -m vertical -p 15 -w 50 -a -15 -r "$((w*6))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hc.png
magick convert "$sname"_hc.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.3]+0+0' "$sname"_hc.png)" +repage "$sname"_hc.png
magick convert "$sname"_hc.png -gravity southwest -crop "$(magick identify -format '%[fx:w*0.4]x%[fx:h*0.5]+0+0' "$sname"_hc.png)" +repage "$sname"_hc.png

./cylinderize -m vertical -p 15 -w 50 -a -30 -r "$((w*6))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hd.png
magick convert "$sname"_hd.png -gravity center -crop "$(magick identify -format '%[fx:w*0.4]x%[fx:h*0.25]+0+0' "$sname"_hd.png)" +repage "$sname"_hd.png
magick convert "$sname"_hd.png -gravity southwest -crop "$(magick identify -format '%[fx:w*0.25]x%[fx:h*0.6]+0+0' "$sname"_hd.png)" +repage "$sname"_hd.png

./cylinderize -m vertical -p 20 -w 50 -a 40 -r "$((w*6))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_he.png
magick convert "$sname"_he.png -gravity center -crop "$(magick identify -format '%[fx:w*0.5]x%[fx:h*0.5]+0+0' "$sname"_he.png)" +repage "$sname"_he.png
magick convert "$sname"_he.png -gravity east -crop "$(magick identify -format '%[fx:w*0.25]x%[fx:h*0.4]+0+0' "$sname"_he.png)" +repage "$sname"_he.png

./cylinderize -m vertical -p 20 -w 43 -a 50 -r "$((w*7))" -v background -b white -f "#e3e3e3" "$sname"_h.png "$sname"_hf.png
magick convert "$sname"_hf.png -gravity east -crop "$(magick identify -format '%[fx:w*0.25]x%[fx:h*0.3]+0+0' "$sname"_hf.png)" +repage "$sname"_hf.png
magick convert "$sname"_hf.png -gravity west -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.5]+0+0' "$sname"_hf.png)" +repage "$sname"_hf.png

#######################################################################################################################

./cylinderize -m horizontal -p 10 -w 100 -a 10 -r "$((h*3))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_va.png
magick convert "$sname"_va.png -gravity center -crop "$(magick identify -format '%[fx:w*0.25]x%[fx:h*0.15]+0+0' "$sname"_va.png)" +repage "$sname"_va.png

./cylinderize -m horizontal -p 15 -w 100 -a -15 -r "$((h*3))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vb.png
magick convert "$sname"_vb.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.15]+0+0' "$sname"_vb.png)" +repage "$sname"_vb.png
magick convert "$sname"_vb.png -gravity northeast -crop "$(magick identify -format '%[fx:w*0.6]x%[fx:h*0.6]+0+0' "$sname"_vb.png)" +repage "$sname"_vb.png

./cylinderize -m horizontal -p 15 -w 50 -a -15 -r "$((h*6))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vc.png
magick convert "$sname"_vc.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.25]+0+0' "$sname"_vc.png)" +repage "$sname"_vc.png
magick convert "$sname"_vc.png -gravity northeast -crop "$(magick identify -format '%[fx:w*0.5]x%[fx:h*0.5]+0+0' "$sname"_vc.png)" +repage "$sname"_vc.png

./cylinderize -m horizontal -p 15 -w 50 -a -30 -r "$((h*6))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vd.png
magick convert "$sname"_vd.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.4]+0+0' "$sname"_vd.png)" +repage "$sname"_vd.png
magick convert "$sname"_vd.png -gravity northeast -crop "$(magick identify -format '%[fx:w*0.6]x%[fx:h*0.2]+0+0' "$sname"_vd.png)" +repage "$sname"_vd.png

./cylinderize -m horizontal -p 20 -w 50 -a 40 -r "$((h*6))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_ve.png
magick convert "$sname"_ve.png -gravity center -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.5]+0+0' "$sname"_ve.png)" +repage "$sname"_ve.png
magick convert "$sname"_ve.png -gravity southeast -crop "$(magick identify -format '%[fx:w*0.6]x%[fx:h*0.2]+0+0' "$sname"_ve.png)" +repage "$sname"_ve.png

./cylinderize -m horizontal -p -20 -w 43 -a 50 -r "$((h*7))" -v background -b white -f "#e3e3e3" "$sname"_v.png "$sname"_vf.png
magick convert "$sname"_vf.png -gravity south -crop "$(magick identify -format '%[fx:w*0.3]x%[fx:h*0.25]+0+0' "$sname"_vf.png)" +repage "$sname"_vf.png
magick convert "$sname"_vf.png -gravity north -crop "$(magick identify -format '%[fx:w]x%[fx:h*0.4]+0+0' "$sname"_vf.png)" +repage "$sname"_vf.png

rm "$sname"_h.png "$sname"_v.png