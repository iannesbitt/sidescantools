#!/bin/bash

EPSG=26983
TEMP=20
FLIP=0

while [[ $# -gt 1 ]]; do
  key="$1"

  case $key in
    -e|--epsg-code)
    EPSG="$2"
    shift # past argument
    ;;
    -t|--temperature)
    TEMP="$2"
    shift # past argument
    ;;
    -f|--flip-transducers)
    FLIP="$2"
    shift # past argument
    ;;
    -h|--help)
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

# sidescan processing of entire folders using PyHum
for f in *.DAT; do
  filename=$(basename "$f")
  dn="${filename%.*}"
  for dir in $dn/; do
    #echo "doing $f and directory $dir"
    ./humread.py -i $f -s $dir -e $EPSG -f $FLIP
    ./humcorrect.py -i $f -s $dir -t $TEMP
    ./humshadows.py -i $f -s $dir
    ./humtexture.py -i $f -s $dir
    ./hummap.py -i $f -s $dir -e $EPSG
    ./hummaptexture.py -i $f -s $dir -e $EPSG
    ./hume1e2.py -i $f -s $dir -e $EPSG -t $TEMP

  done
done
