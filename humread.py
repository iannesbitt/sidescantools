
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

    flip_lr = 0 # default to 'do not flip port and starboard channels" if no argument given
    cs = 26983 # default to Maine East State Plane meters if no argument given

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
       elif opt in ("-e"):
          cs = arg
       elif opt in ("-f"):
          flip_lr = arg


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

    if not cs:
       print 'A valid EPSG number is required!!!!!!'


    # print given arguments to screen and convert data type where necessary
    if humfile:
       print 'Input file is %s' % (humfile)

    if sonpath:
       print 'Son files are in %s' % (sonpath)

    doplot = 1 #yes

    # reading specific settings
    
    cs2cs_args = "epsg:"+str(cs)

    # read-specific settings
    bedpick = 1 # auto bed pick
    c = 1500 # speed of sound in (fresh) water
    t = 0.108 # length of transducer
    draft = 0.4 # draft in metres
    model = 1199 # humminbird model
    calc_bearing = 0 #no
    filt_bearing = 0 #no
    chunk = 'd100' # distance, 100m
    #chunk = 'p1000' # pings, 1000
    #chunk = 'h15' # heading deviation, 15 deg

        ## read data in SON files into PyHum memory mapped format (.dat)
    PyHum.read(humfile, sonpath, cs2cs_args, c, draft, doplot, t, bedpick, flip_lr, model, calc_bearing, filt_bearing, chunk)
