# sidescantools
Simple shell wrapper for PyHum (https://github.com/dbuscombe-usgs/pyhum)

This software is partially modified from code written by Dr. Daniel Buscombe, Northern Arizona University, formerly of the USGS.

## Requirements
- Unix-based command line
- Python 2.7
- [`PyHum`](https://github.com/dbuscombe-usgs/pyhum)
- The more RAM the better. 64GB or more would be ideal, but if like me you lack the resources for that, you can probably get away with [allocating a bunch of swap space](http://www.thegeekstuff.com/2010/08/how-to-add-swap-space/?utm_source=feedburner).

## Setup
```
cd ~/bin/ # replace 'bin' with the folder you'd like to install in
git clone https://github.com/iannesbitt/sidescantools.git
ln -s sidescantools/humss.py ./humss; ln -s sidescantools/humall.sh ./humall # create links
export PATH=$PATH:~/bin/ # adds the bin folder in your home directory to the end of the PATH variable
# to make this permanent, add the above line to the end of your ~/.bashrc file
```

## Usage
### humss.py (single step processing)
From command line:

```
humread -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/ -e 26984 -t 20 -f 1
```

where the argument `-i` precedes the path of a .DAT file, `-s` precedes the path of the comparably named data folder, the `-e` argument precedes the EPSG code, `-t` precedes the temperature in degrees C, and the `-f` argument precedes a binary digit describing whether or not to flip the port and starboard sidescan channels (in case the transducer is mounted backwards).

### humall.sh (current directory processing)
Processes all .DAT and related data folders in current directory using all steps in PyHum (read, correct, shadow removal, textural analysis, mapping, texture mapping, and e1/e2 value calculation). This is usually super memory and processor intensive, and can take a very long time. From command line:

```
cd fieldwork/data_directory/
humall -e 26984 -t 20 -f 1
```

where the `-e` argument precedes the EPSG code, `-t` precedes the temperature in degrees C, and the `-f` argument precedes a binary digit describing whether or not to flip the port and starboard sidescan channels. You must be in a data directory for this command to work properly.
