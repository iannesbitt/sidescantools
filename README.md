# sidescantools
Simple shell wrapper for PyHum (https://github.com/dbuscombe-usgs/pyhum)

This software is partially modified from code written by Dr. Daniel Buscombe, Assistant Research Professor at Northern Arizona University, formerly a postdoc at the USGS. Some code is public domain and has been licensed as such.

## Requirements
- Unix-based command line
- Python 2.7 (Anaconda works best)
- [`gdal`](http://www.gdal.org/)
- [`PyHum`](https://github.com/dbuscombe-usgs/pyhum)
- The more RAM the better. 32GB or more would be ideal, but you can probably get away with [allocating a bunch of swap space](http://www.thegeekstuff.com/2010/08/how-to-add-swap-space/?utm_source=feedburner).

## Setup
```
sudo apt install gdal-bin libgdal-dev           # in case you don't already have GDAL installed
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
ln -s sidescantools/kmz2geotiff.sh ./kmz2geotiff #create links

# the following adds the bin folder in your home directory to the end of the PATH variable
export PATH=$PATH:~/bin/                        # you will need to change this if you change your installation location
# to make this permanent, add the above line to the end of your ~/.bashrc file
```

*You may need to change the* `humread.py` *file if you have a different Humminbird model than the one written into the code. A note: if you have a model other than the examples given by PyHum (998, 997, 1198, 1199), experiment with different model numbers as they may work with your model based on how your specific model is set up to record data. For example, the 999 model I use actually operates similarly to the 1199, so I use* `model = 1199` *in the* `humread.py` *file.*

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
# or
humall --epsg-code 26984 --temperature 20 --flip-transducers 1
```

where the `-e` or `--epsg-code` argument precedes the EPSG code, `-t` or `--temperature` precedes the temperature in degrees C, and the `-f` or `--flip-transducers` argument precedes a binary digit describing whether or not to flip the port and starboard sidescan channels. You must be in a data directory for this command to work properly.

### kmz2geotiff.sh (shell script that utilizes GDAL to translate KMZ images to GeoTIFF)
Takes all KMZ archives with regular map images in them (not texture map images) in folders with the given prefix (defaults to "R", as Humminbird directories are typically named) and outputs as GeoTIFF in the given working directory. The `gdal_translate` step downsamples each sidescan image, as often they have far more pixel resolution than is necessary. The final step of the script uses `gdalwarp` to write all output GeoTIFFs in the working directory to a single mosaic. This can take some time depending on how many images there are, and the resultant merged image can be quite large (GB). This script will generally ignore KMZ files that are related to texture maps (though it will take a peek inside them to make sure).

```
cd fieldwork/data_directory/
kmz2geotiff -e 26919 -w work_dir -p R -o mosaic_name
# or
kmz2geotiff --epsg-code 26919 --work-dir work_dir --prefix R --outfile mosaic_name
```

where the `-e` or `--epsg-code` argument precedes the EPSG code, `-w` or `--work-dir` precedes the given name of the your working directory (the script will make a new directory with this name), and `-o` or `--outfile` denotes the name of the GeoTIFF mosaic created from the extracted KMZ images. You must be in a data directory for this command to work properly.
