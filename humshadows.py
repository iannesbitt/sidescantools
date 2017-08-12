
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


    # for shadow removal
    shadowmask = 0 #auto shadow removal
    win = 31 # pixel window

    ## remove acoustic shadows (caused by distal acoustic attenuation or sound hitting shallows or shoreline)
    PyHum.rmshadows(humfile, sonpath, win, shadowmask, doplot)
