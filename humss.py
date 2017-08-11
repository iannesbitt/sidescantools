#!/home/iannesbitt/bin/anaconda2/bin/python

## Modified from Daniel Buscombe's starter script at https://github.com/dbuscombe-usgs/pyhum
## Supply .DAT file using -i and SON folder using -s
## OR cd into a directory with both .DAT/SON and process all using 'humall' (~/bin/humall)

import sys, getopt

from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import askyesno

import PyHum
import os

if __name__ == '__main__': 

    argv = sys.argv[1:]
    humfile = ''; sonpath = ''

    # parse inputs to variables
    try:
       opts, args = getopt.getopt(argv,"hi:s:")
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
       #elif opt in ("-c"):
          #cs = arg

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

    #if not cs and cs != "east" and cs != "west":
       #Tk().withdraw()
       #cs = askyesno("Coordinate System Choice","Choose Yes to use NAD83 ME East SP, or No to use NAD83 ME West SP.")

    # print given arguments to screen and convert data type where necessary
    if humfile:
       print 'Input file is %s' % (humfile)

    if sonpath:
       print 'Son files are in %s' % (sonpath)

    doplot = 1 #yes

    # reading specific settings
    
    cs2cs_args = "epsg:26984" #Maine west state plane meter
    #if cs == False:
       #cs2cs_args = "epsg:26984" #Maine west state plane meter
    #else:
       #cs2cs_args = "epsg:26983" #Maine east state plane meter
    bedpick = 1 # auto bed pick
    c = 1500 # speed of sound in (fresh) water
    t = 0.108 # length of transducer
    draft = 0.4 # draft in metres
    flip_lr = 1 # flip port and starboard
    model = 1199 # humminbird model
    calc_bearing = 0 #no
    filt_bearing = 0 #no
    chunk = 'd100' # distance, 100m
    #chunk = 'p1000' # pings, 1000
    #chunk = 'h15' # heading deviation, 15 deg

    # correction specific settings
    maxW = 1000 # rms output wattage
    dofilt = 0 # 1 = apply a phase preserving filter (WARNING!! takes a very long time for large scans)
    correct_withwater = 0 # don't retain water column in radiometric correction (1 = retains water column for radiometric corrections)
    ph = 6.7 # acidity on the pH scale
    temp = 23.8 # water temperature in degrees Celsius
    salinity = 0.0

    # for shadow removal
    shadowmask = 0 #auto shadow removal
    win = 31 # pixel window

    # for texture calcs
    shift = 10 # pixel shift
    density =win/2 # win/2 
    numclasses = 4 # number of discrete classes for contouring and k-means
    maxscale = 20 # Max scale as inverse fraction of data length (for wavelet analysis)
    notes = 4 # Notes per octave (for wavelet analysis)

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

    # for downward-looking echosounder echogram (e1-e2) analysis
    beam = 20.0
    transfreq = 200.0 # frequency (kHz) of downward looking echosounder
    integ = 5
    numclusters = 3 # number of acoustic classes to group observations


    ## read data in SON files into PyHum memory mapped format (.dat)
    PyHum.read(humfile, sonpath, cs2cs_args, c, draft, doplot, t, bedpick, flip_lr, model, calc_bearing, filt_bearing, chunk)

    ## correct scans and remove water column
    PyHum.correct(humfile, sonpath, maxW, doplot, dofilt, correct_withwater, ph, temp, salinity)

    ## remove acoustic shadows (caused by distal acoustic attenuation or sound hitting shallows or shoreline)
    PyHum.rmshadows(humfile, sonpath, win, shadowmask, doplot)

    win = 100 # reset pixel window

    ## Calculate texture lengthscale maps using the method of Buscombe et al. (2015)
    PyHum.texture(humfile, sonpath, win, shift, doplot, density, numclasses, maxscale, notes)

    ## grid and map the scans
    PyHum.map(humfile, sonpath, cs2cs_args, res, mode, nn, numstdevs, use_uncorrected) #dowrite,

    ## grid and map the texture lengthscale maps
    PyHum.map_texture(humfile, sonpath, cs2cs_args, res, mode, nn, numstdevs)

    ## calculate and map the e1 and e2 acoustic coefficients from the downward-looking sonar
    PyHum.e1e2(humfile, sonpath, cs2cs_args, ph, temp, salinity, beam, transfreq, integ, numclusters, doplot)

    res = 0
    nn = 5 # nearest neighbors used for gridding
    noisefloor = 10 # noise threshold in dB W
    weight = 1 ##based on grazing angle and inverse distance weighting

    ## create mosaic out of all chunks with weighting according to distance from nadir, grazing angle, or both
    PyHum.mosaic(humfile, sonpath, cs2cs_args, res, nn, noisefloor, weight)
