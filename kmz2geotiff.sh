#!/bin/bash

work="tmp" # working directory name
pfx="R" # directory prefix ("R" for Humminbird / PyHum)
epsg="4326"

mkdir "$work"

for d in "$pfx"*/; do
  for f in "$d"/*.kmz; do
    filename=$(basename "$f")
    dn="${filename%.*}"
    rn=$(basename "$d")
    cp "$d"/"$filename" "$d"/"$dn".zip
    unzip "$d"/"$dn".zip -d "$work"/"$rn$dn"
    rm "$d"/"$dn".zip
    while read north && read south && read east && read west; do
      north=${north##*'<north>'} north=${north%%'</north>'*}
      south=${south##*'<south>'} south=${south%%'</south>'*}
      east=${east##*'<east>'} east=${east%%'</east>'*}
      west=${west##*'<west>'} west=${west%%'</west>'*}
      # PyHum mixes up East and West...normally we would give gdal "$west $north $east $south" instead
      gdal_translate -a_ullr "$east" "$north" "$west" "$south" -a_srs EPSG:4326 "$work"/"$rn$dn"/files/map*.png "$work"/"$rn$dn".tif -co COMPRESS=JPEG -outsize 10% 10%
    done < <(exec grep -Fe "<north>" -e "<south>" -e "<east>" -e "<west>" "$work"/"$rn$dn"/doc.kml)
  rm -r "$work"/"$rn$dn"/
  done
done

echo "mosaicing . . ."
gdalwarp -srcalpha -dstalpha -t_srs EPSG:"$epsg" --config GDAL_CACHEMAX 3000 -wm 3000 tmp/*.tif merge.tif