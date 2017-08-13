#!/home/user/anaconda2/bin/python

## Modified from Daniel Buscombe's starter script at https://github.com/dbuscombe-usgs/pyhum
## Supply .DAT file using -i and SON folder using -s
## OR cd into a directory with both .DAT/SON and process all using 'humall' (~/bin/humall)

import sys, getopt

from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory

import PyHum
import os

if __name__ == '__main__': 

    argv = sys.argv[1:]
    humfile = ''; sonpath = ''

    cs = 26983 # default to Maine East State Plane meters if no argument given

    # parse inputs to variables
    try:
       opts, args = getopt.getopt(argv,"hi:s:e:")
    except getopt.GetoptError:
         print 'error'
         sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
         print 'help'
         sys.exit()
       elif opt in ("-i"):
          humfile = arg
       elif opt in ("-s"):
          sonpath = arg
       elif opt in ("-e"):
          cs = arg


    # prompt user to supply file if no input file given
    if not humfile:
       print 'An input file is required!!!!!!'
       Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
       humfile = askopenfilename(filetypes=[("DAT files","*.DAT")]) 

    # prompt user to supply directory if no input sonpath is given
    if not sonpath:
       print 'A *.SON directory is required!!!!!!'
       Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
       sonpath = askdirectory()


    # print given arguments to screen and convert data type where necessary
    if humfile:
       print 'Input file is %s' % (humfile)

    if sonpath:
       print 'Son files are in %s' % (sonpath)

    doplot = 1 #yes

    # reading specific settings
    
    cs2cs_args = "epsg:"+str(cs)

    # for mapping
    res = 99 # grid resolution in metres
    # if res==99, the program will automatically calc res from the spatial res of the scans
    mode = 1 # gridding mode (simple nearest neighbour)
    #mode = 2 # gridding mode (inverse distance weighted nearest neighbour)
    #mode = 3 # gridding mode (gaussian weighted nearest neighbour)
    #dowrite = 1 #writing of point cloud data to file
    use_uncorrected = 0

    nn = 64 # number of nearest neighbours for gridding (used if mode > 1)
    #influence = 1 # Radius of influence used in gridding. Cut of distance in meters.
    numstdevs = 5 # Threshold number of standard deviations in sidescan intensity per grid cell up to which to accept

    ## grid and map the scans
    PyHum.map(humfile, sonpath, cs2cs_args, res, mode, nn, numstdevs, use_uncorrected) #dowrite,
