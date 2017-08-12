#!/bin/bash

epsg=26983
temp=20
flip=0
stop=0
bin_dir="bin/sidescantools"

while [[ $# -gt 1 ]]; do
  key="$1"

  case $key in
    -e|--epsg-code)
    epsg="$2"
    shift # next argument
    ;;
    -t|--temperature)
    temp="$2"
    shift # past argument
    ;;
    -f|--flip-transducers)
    flip="$2"
    shift # past argument
    ;;
    -h|--help)
    stop=1
    echo "Takes three arguments:"
    echo "[-e | --epsg-code]        - numeric EPSG code (defaults to 26983, Maine East State Plane)"
    echo "[-t | --temperature]      - temp in degrees C (defaults to 20)"
    echo "[-f | --flip-transducers] - binary value indicating whether to flip port and starboard transducers (defaults to 0)"
    exit 1
    shift # past argument
    ;;
    *)
    echo "Unknown argument. Use -h or --help."
    ;;
  esac
  shift
done

if [ "$stop" -eq "0" ]; then
  # sidescan processing of entire folders using PyHum
  for f in *.DAT; do
    filename=$(basename "$f")
    dn="${filename%.*}"
    for dir in $dn/; do
      #echo "doing $f and directory $dir"
      "$HOME"/"$bin_dir"/humread.py -i $f -s $dir -e $epsg -t $temp -f $flip
      "$HOME"/"$bin_dir"/humcorrect.py -i $f -s $dir -t $temp
      "$HOME"/"$bin_dir"/humshadows.py -i $f -s $dir
      "$HOME"/"$bin_dir"/humtexture.py -i $f -s $dir
      "$HOME"/"$bin_dir"/hummap.py -i $f -s $dir -e $epsg
      "$HOME"/"$bin_dir"/hummaptexture.py -i $f -s $dir -e $epsg
      "$HOME"/"$bin_dir"/hume1e2.py -i $f -s $dir -e $epsg -t $temp
  
    done
  done
fi
