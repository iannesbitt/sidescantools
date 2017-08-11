#!/bin/bash

# sidescan processing of entire folders using PyHum
for f in *.DAT; do
  filename=$(basename "$f")
  dn="${filename%.*}"
  for dir in $dn/; do
    #echo "doing $f and directory $dir"
    ./humss.py -i $f -s $dir
  done
done
