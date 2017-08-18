#!/bin/bash

work="tmp" # default working directory name
pfx="R" # default directory prefix ("R" for Humminbird / PyHum)
epsg="4326" # default coordinate system output (WGS 84 Geographic)
outfile="mosaic"

while [[ $# -gt 1 ]]; do
  key="$1"

  case $key in
    -e|--epsg-code)
    epsg="$2" # EPSG code for the coordinate system of the output mosaic
    shift # next argument
    ;;
    -w|--work-dir)
    work="$2" # working directory name
    shift # past argument
    ;;
    -p|--prefix)
    pfx="$2" # prefix of the sidescan 'SON' directory (for Humminbird this is usually 'R', as in 'R00041')
    shift # past argument
    ;;
    -o|--outfile)
    pfx="$2" # output filename
    shift # past argument
    ;;
    -h|--help)
    stop=1
    echo "Takes three arguments:"
    echo "[-e | --epsg-code]        - numeric EPSG code (defaults to 4326, Geographic WGS 84)"
    echo "[-w | --work-dir]         - working directory name (will be created if doesn't already exist)"
    echo "[-p | --prefix]           - Humminbird directory prefix (generally 'R')"
    echo "[-o | --outfile]          - name of the output mosaic geotiff"
    exit 1
    shift # past argument
    ;;
    *)
    echo "Unknown argument. Use -h or --help."
    ;;
  esac
  shift
done


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
gdalwarp -srcalpha -dstalpha -t_srs EPSG:"$epsg" --config GDAL_CACHEMAX 3000 -wm 3000 tmp/*.tif "$outfile".tif
