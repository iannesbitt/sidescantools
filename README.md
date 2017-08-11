# sidescantools
Simple tools for use with PyHum (https://github.com/dbuscombe-usgs/pyhum)

This software is partially modified from code written by Dr. Daniel Buscombe, Northern Arizona University, formerly of the USGS.

## Requirements
- Unix-based command line
- Python 2.7
- [`PyHum`](https://github.com/dbuscombe-usgs/pyhum)

## Setup
```
cd ~/bin/ # replace 'bin' with the folder you'd like to install in
git clone https://github.com/iannesbitt/sidescantools.git
ln -s sidescantools/humss.py ./humss; ln -s sidescantools/humall.sh ./humall # create links
export PATH=$PATH:~/bin/ # adds the bin folder in your home directory to the end of the PATH variable
# to make this permanent, add the above line to the end of your ~/.bashrc file
```

## Usage
### humss.py (singular file processing)
From command line:

```
humss -i fieldwork/data_directory/R00001.DAT -s fieldwork/data_directory/R00001/
```

where the argument `-i` precedes the path of a .DAT file, and the `-s` argument precedes the path of the comparably named data folder.

### humall.sh (current directory processing)
Processes all .DAT and related data folders in current directory. From command line:

```
cd fieldwork/data_directory/
humall
```

You must be in a data directory for this command to work properly.
