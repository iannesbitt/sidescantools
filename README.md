# sidescantools
Simple shell wrapper for PyHum (https://github.com/dbuscombe-usgs/pyhum)

This software is partially modified from code written by Dr. Daniel Buscombe, Assistant Research Professor at Northern Arizona University, formerly a postdoc at the USGS. Some code is public domain and has been licensed as such.

## Requirements
- Unix-based command line
- Python 2.7 (Anaconda works best)
- [`PyHum`](https://github.com/dbuscombe-usgs/pyhum)
- The more RAM the better. 64GB or more would be ideal, but if like me you lack the resources for that, you can probably get away with [allocating a bunch of swap space](http://www.thegeekstuff.com/2010/08/how-to-add-swap-space/?utm_source=feedburner).

## Setup
```
cd ~/bin/                                       # replace 'bin' with the folder you'd like to install in
git clone https://github.com/iannesbitt/sidescantools.git
ln -s sidescantools/humread.py ./humread        # create links
ln -s sidescantools/humcorrect.py ./humcorrect  # create links
ln -s sidescantools/humshadows.py ./humshadows  # create links
ln -s sidescantools/humtexture.py ./humtexture  # create links
ln -s sidescantools/hummap.py ./hummap          # create links
ln -s sidescantools/hummaptexture.py ./hummaptexture # create links
ln -s sidescantools/hume1e2.py ./hume1e2        # create links
ln -s sidescantools/humall.sh ./humall          # create links

# the following adds the bin folder in your home directory to the end of the PATH variable
export PATH=$PATH:~/bin/                        # you will need to change this if you change your installation location
# to make this permanent, add the above line to the end of your ~/.bashrc file
```

*You may need to change the *`humread.py`* file if you have a different Humminbird model than the one written into the code. A note: if you have a model other than the examples given by PyHum (998, 997, 1198, 1199), experiment with different model numbers as they may work with your model based on how your specific model is set up to record data. For example, the 999 model I use actually operates similarly to the 1199, so I use *`model = 1199`* in the *`humread.py`* file.*

## Usage
### hum\*.py (single step, single file processing)
From command line:

```
humread -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/ -e 26984 -t 20 -f 1
humcorrect -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/ -t 20
humshadows -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/
humtexture -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/
hummap -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/ -e 26984
hummaptexture -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/ -e 26984
hume1e2 -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/ -e 26984 -t 20
```

where the argument `-i` precedes the path of a .DAT file, `-s` precedes the path of the comparably named data folder, the `-e` argument precedes the EPSG code, `-t` precedes the temperature in degrees C, and the `-f` argument precedes a binary digit describing whether or not to flip the port and starboard sidescan channels (in case the transducer is mounted backwards).

### humall.sh (multi-step processing for all files in current directory)
Processes all .DAT and related data folders in current directory using all steps in PyHum (read, correct, shadow removal, textural analysis, mapping, texture mapping, and e1/e2 value calculation). This is usually super memory and processor intensive, and can take a very long time. From command line:

```
cd fieldwork/data_directory/
humall -e 26984 -t 20 -f 1
```

where the `-e` argument precedes the EPSG code, `-t` precedes the temperature in degrees C, and the `-f` argument precedes a binary digit describing whether or not to flip the port and starboard sidescan channels. You must be in a data directory for this command to work properly.
